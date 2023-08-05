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

from contextlib import contextmanager
from enum import Enum, auto
from ipaddress import ip_address
import re
from typing import TYPE_CHECKING

from transitions import Machine, MachineError

from .data import NETWORK_PROTOCOL, TRANSPORT_PROTOCOL, PORT_NUMBER, EXECUTABLE_NAME, NetworkProtocol, \
    TransportProtocol, ConnectionState
from .exception import UnexpectedLineError

if TYPE_CHECKING:
    from typing import Optional

_protocol = rf'(?P<proto>' + '|'.join(pr.name for pr in TransportProtocol) + ')'
_spacing = r'(?: +)'
_state = r'(?P<state>' + '|'.join(st.name for st in ConnectionState) + ')'
_hex_number = r'(?:(?:\d|[a-fA-F])+)'
_local_ip4_address = r'(?P<local_ipv4_address>\d+\.\d+\.\d+\.\d+)'
_foreign_ip4_address = r'(?:\d+\.\d+\.\d+\.\d+)'
_ip6_delimiter = r'(?:::|:)'
_ip6_zone = r'(?:%\d+)'
_local_ip6_address = rf'(?:\[(?P<local_ipv6_address>(?:{_hex_number}?{_ip6_delimiter})+{_hex_number}?)' \
                     rf'{_ip6_zone}?\])'
_foreign_ip6_address = rf'(?:\[(?:{_hex_number}?{_ip6_delimiter})+{_hex_number}?{_ip6_zone}?\])'
_local_port = r'(?P<local_port>\d+)'
_foreign_port = r'(?:\d+)'
_local_address = f'(?:(?:{_local_ip4_address}|{_local_ip6_address}):{_local_port})'
_wildcard_address = r'(?:\*:\*)'
_foreign_address = f'(?:(?:(?:{_foreign_ip4_address}|{_foreign_ip6_address}):{_foreign_port})|{_wildcard_address})'
_network_entry = rf'(?:^{_spacing}?{_protocol}{_spacing}{_local_address}{_spacing}{_foreign_address}' \
                 rf'(?:{_spacing}{_state}?)?$)'
_process_name = r'(?P<proc_name>.+)'
_process_entry = rf'(?:^{_spacing}?\[{_process_name}\]$)'
_generic_entry = rf'(?:^.+$)'
_data_entry = rf'(?:{_network_entry}|{_process_entry}|{_generic_entry})'
_data_entry_line_re = re.compile(_data_entry)


class PortCollector:

    def __init__(self):
        self.reset()

    def __call__(self, file_name: Optional[str], net_proto: NetworkProtocol, ip_addr: str,
                 transport_proto: TransportProtocol, port_number: int,
                 connection_state: Optional[ConnectionState]) -> None:
        ad = ip_address(ip_addr)
        if (connection_state == ConnectionState.LISTENING or transport_proto == TransportProtocol.UDP) \
                and not ad.is_loopback:
            self.port_data.append({EXECUTABLE_NAME: file_name, NETWORK_PROTOCOL: net_proto,
                                   TRANSPORT_PROTOCOL: transport_proto, PORT_NUMBER: port_number})

    def reset(self):
        self.port_data = []


class _NetstatState(Enum):
    INITIAL = auto()
    WAITING_NET = auto()
    WAITING_PROC = auto()
    DONE = auto()


class _NetstatModel:

    def __init__(self, pc: PortCollector):
        self._cb = pc
        self._reset()

    def on_exit_WAITING_PROC(self):
        self._cb(self.proc_name, self.network_protocol, self.ip_addr, self.transport_protocol, self.local_port,
                 self.conn_state)
        self._reset()

    def _reset(self):
        self.network_protocol = None
        self.ip_addr = None
        self.transport_protocol = None
        self.local_port = None
        self.conn_state = None
        self.proc_name = None


class WindowsNetstatPortDataParser:

    def __init__(self, pc: PortCollector):
        self._model = _NetstatModel(pc)
        states = [_NetstatState.INITIAL, _NetstatState.WAITING_NET, _NetstatState.WAITING_PROC, _NetstatState.DONE]
        transitions = [['start', [_NetstatState.INITIAL, _NetstatState.DONE], _NetstatState.WAITING_NET],
                       ['handle_net', [_NetstatState.WAITING_NET, _NetstatState.WAITING_PROC],
                        _NetstatState.WAITING_PROC],
                       ['handle_proc', _NetstatState.WAITING_PROC, _NetstatState.WAITING_NET],
                       ['finish', [_NetstatState.INITIAL, _NetstatState.WAITING_NET, _NetstatState.WAITING_PROC],
                        _NetstatState.DONE]]
        self._machine = Machine(model=self._model, states=states, transitions=transitions,
                                initial=_NetstatState.INITIAL)

    def _handle_data(self, proto, ipv4_addr, ipv6_addr, port, conn_state, proc_name):
        if proto is not None:
            self._model.handle_net()
            if ipv6_addr is None:
                self._model.network_protocol = NetworkProtocol.IPv4
                self._model.ip_addr = ipv4_addr
            else:
                self._model.network_protocol = NetworkProtocol.IPv6
                self._model.ip_addr = ipv6_addr
            self._model.transport_protocol = TransportProtocol[proto]
            self._model.local_port = int(port)
            try :
                self._model.conn_state = ConnectionState[conn_state] if conn_state is not None else None
            except KeyError:
                self._model.conn_state = None
        if proc_name is not None:
            self._model.proc_name = proc_name
            self._model.handle_proc()

    def extract_data(self, data: str):
        self._model.start()
        for line_no, line in enumerate(data.splitlines()):
            self._consume_line(line, line_no + 1)
        self._model.finish()

    def _consume_line(self, line: str, line_no: int):
        line = line.rstrip()
        match = _data_entry_line_re.match(line)
        if match:
            proto, ipv4_addr, ipv6_addr, port, conn_state, proc_name = match.groups()
            try:
                self._handle_data(proto, ipv4_addr, ipv6_addr, port, conn_state, proc_name)
            except MachineError:
                raise UnexpectedLineError(line, line_no)

    @contextmanager
    def line_stream_consumer(self):
        self._model.start()
        yield self._consume_line
        self._model.finish()
