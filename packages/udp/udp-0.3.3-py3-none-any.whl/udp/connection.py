# -*- coding: utf-8 -*-
#
#   UDP: User Datagram Protocol
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

import time
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Optional


class ConnectionStatus(IntEnum):
    """
        @enum ConnectionStatus

        @abstract Defined for indicating connection status

        @discussion connection status.

            Default     - 'initialized', or sent timeout
            Connecting  - sent 'PING', waiting for response
            Connected   - got response recently
            Expired     - long time, needs maintaining (still connected)
            Maintaining - sent 'PING', waiting for response
            Error       - long long time no response, connection lost

        Bits:
            0000 0001 - indicates sent something just now
            0000 0010 - indicates sent something not too long ago

            0001 0000 - indicates received something just now
            0010 0000 - indicates received something not too long ago

            (All above are just some advices to help choosing numbers :P)
    """

    Default = 0x00      # 0000 0000
    Connecting = 0x01   # 0000 0001, sent just now
    Connected = 0x11    # 0001 0001, received just now
    Maintaining = 0x21  # 0010 0001, received not long ago, sent just now
    Expired = 0x22      # 0010 0010, received not long ago, needs sending
    Error = 0x03        # 0000 0011, long time no response

    @classmethod
    def is_connected(cls, status: int) -> bool:
        return (status & 0x30) != 0  # received something not long ago

    @classmethod
    def is_expired(cls, status: int) -> bool:
        return (status & 0x01) == 0  # sent nothing in a period

    @classmethod
    def is_error(cls, status: int) -> bool:
        return status == cls.Error.value  # sent for a long time, but received nothing


"""
    Finite States:

            //===============\\          (Sent)          //==============\\
            ||               || -----------------------> ||              ||
            ||    Default    ||                          ||  Connecting  ||
            || (Not Connect) || <----------------------- ||              ||
            \\===============//         (Timeout)        \\==============//
                                                              |       |
            //===============\\                               |       |
            ||               || <-----------------------------+       |
            ||     Error     ||          (Error)                 (Received)
            ||               || <-----------------------------+       |
            \\===============//                               |       |
                A       A                                     |       |
                |       |            //===========\\          |       |
                (Error) +----------- ||           ||          |       |
                |                    ||  Expired  || <--------+       |
                |       +----------> ||           ||          |       |
                |       |            \\===========//          |       |
                |       (Timeout)           |         (Timeout)       |
                |       |                   |                 |       V
            //===============\\     (Sent)  |            //==============\\
            ||               || <-----------+            ||              ||
            ||  Maintaining  ||                          ||  Connected   ||
            ||               || -----------------------> ||              ||
            \\===============//       (Received)         \\==============//
"""


class DatagramPacket:

    def __init__(self, data: bytes, address: tuple):
        super().__init__()
        self.__data = data
        self.__address = address

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def offset(self) -> int:
        return 0

    @property
    def length(self) -> int:
        return len(self.__data)

    @property
    def address(self) -> tuple:
        return self.__address

    @property
    def ip(self) -> str:
        return self.__address[0]

    @property
    def port(self) -> int:
        return self.__address[1]


class Connection:

    EXPIRES = 28  # seconds

    """
        Max count for caching packages
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Each UDP data package is limited to no more than 576 bytes, so set the
        MAX_CACHE_SPACES to about 200,000 means it would take up to 100MB memory
        for caching in one connection.
    """
    MAX_CACHE_SPACES = 1024 * 200

    def __init__(self, local_address: tuple, remote_address: tuple):
        super().__init__()
        self.__local_address = local_address
        self.__remote_address = remote_address
        # connecting status
        self.__status = ConnectionStatus.Default
        # initialize times to expired
        now = time.time()
        self.__last_sent_time = now - self.EXPIRES - 1
        self.__last_received_time = now - self.EXPIRES - 1
        # received packages
        self.__cargoes = []

    @property
    def local_address(self) -> tuple:
        """ local ip, port """
        return self.__local_address

    @property
    def remote_address(self) -> tuple:
        """ remote ip, port """
        return self.__remote_address

    def is_connected(self, now: float) -> bool:
        status = self.get_status(now=now)
        return ConnectionStatus.is_connected(status=status)

    def is_expired(self, now: float) -> bool:
        status = self.get_status(now=now)
        return ConnectionStatus.is_expired(status=status)

    def is_error(self, now: float) -> bool:
        status = self.get_status(now=now)
        return ConnectionStatus.is_error(status=status)

    def get_status(self, now: float):
        """
        Get connection status

        :param now: timestamp in seconds
        :return: new status
        """
        # pre-checks
        if now < self.__last_received_time + self.EXPIRES:
            # received response recently
            if now < self.__last_sent_time + self.EXPIRES:
                # sent recently, set status = 'connected'
                self.__status = ConnectionStatus.Connected
            else:
                # long time no sending, set status = 'expired'
                self.__status = ConnectionStatus.Expired
            return self.__status
        if self.__status != ConnectionStatus.Default:
            # any status except 'initialized'
            if now > self.__last_received_time + (self.EXPIRES << 2):
                # long long time no response, set status = 'error'
                self.__status = ConnectionStatus.Error
                return self.__status
        # check with current status
        if self.__status == ConnectionStatus.Default:
            # case: 'default'
            if now < self.__last_sent_time + self.EXPIRES:
                # sent recently, change status to 'connecting'
                self.__status = ConnectionStatus.Connecting
        elif self.__status == ConnectionStatus.Connecting:
            # case: 'connecting'
            if now > self.__last_sent_time + self.EXPIRES:
                # long time no sending, change status to 'not_connect'
                self.__status = ConnectionStatus.Default
        elif self.__status == ConnectionStatus.Connected:
            # case: 'connected'
            if now > self.__last_received_time + self.EXPIRES:
                # long time no response, needs maintaining
                if now < self.__last_sent_time + self.EXPIRES:
                    # sent recently, change status to 'maintaining'
                    self.__status = ConnectionStatus.Maintaining
                else:
                    # long time no sending, change status to 'maintain_expired'
                    self.__status = ConnectionStatus.Expired
        elif self.__status == ConnectionStatus.Expired:
            # case: 'maintain_expired'
            if now < self.__last_sent_time + self.EXPIRES:
                # sent recently, change status to 'maintaining'
                self.__status = ConnectionStatus.Maintaining
        elif self.__status == ConnectionStatus.Maintaining:
            # case: 'maintaining'
            if now > self.__last_sent_time + self.EXPIRES:
                # long time no sending, change status to 'maintain_expired'
                self.__status = ConnectionStatus.Expired
        return self.__status

    def update_sent_time(self, now: float):
        self.__last_sent_time = now

    def update_received_time(self, now: float):
        self.__last_received_time = now

    def receive(self) -> Optional[DatagramPacket]:
        """
        Get received data package from buffer, non-blocked

        :return: received data and source address
        """
        if len(self.__cargoes) > 0:
            return self.__cargoes.pop(0)

    def cache(self, packet: DatagramPacket) -> Optional[DatagramPacket]:
        # 1. check memory cache status
        ejected = None
        if self._is_cache_full(count=len(self.__cargoes)):
            # drop the first package
            ejected = self.__cargoes.pop(0)
        # 2. append the new package to the end
        self.__cargoes.append(packet)
        return ejected

    def _is_cache_full(self, count: int) -> bool:
        return count > self.MAX_CACHE_SPACES


class ConnectionHandler(ABC):

    @abstractmethod
    def connection_status_changed(self, connection: Connection,
                                  old_status: ConnectionStatus, new_status: ConnectionStatus):
        """
        Call when connection status changed

        :param connection:
        :param old_status:
        :param new_status:
        """
        pass

    @abstractmethod
    def connection_received_data(self, connection: Connection):
        """
        Call when received data from a connection

        :param connection:
        """
        pass
