#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2020 Andrey Pleshakov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import annotations

from enum import Enum, auto

NETWORK_PROTOCOL = 'network_protocol'
TRANSPORT_PROTOCOL = 'transport_protocol'
PORT_NUMBER = 'port_number'
EXECUTABLE_NAME = 'executable_name'


class NetworkProtocol(Enum):
    IPv4 = auto()
    IPv6 = auto()


class TransportProtocol(Enum):
    UDP = auto()
    TCP = auto()


class ConnectionState(Enum):
    LISTENING = auto()
    ESTABLISHED = auto()
    SYN_SENT = auto()
    CLOSE_WAIT = auto()
    TIME_WAIT = auto()
    CLOSED = auto()
    FIN_WAIT_1 = auto()
    FIN_WAIT_2 = auto()
    LAST_ACK = auto()
    SYN_RECEIVED = auto()


class Platform(Enum):
    WINDOWS = auto()


class Application(Enum):
    NETSTAT = auto()
