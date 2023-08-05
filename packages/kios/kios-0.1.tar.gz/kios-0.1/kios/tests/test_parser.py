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

from unittest import TestCase
from unittest.mock import Mock, call

from kios.data import NetworkProtocol, TransportProtocol, ConnectionState, NETWORK_PROTOCOL, TRANSPORT_PROTOCOL, \
    PORT_NUMBER, EXECUTABLE_NAME
from kios.parser import PortCollector, WindowsNetstatPortDataParser
from kios.exception import UnexpectedLineError
from .helper import get_test_data, open_test_file, patch_config_app_platform


class PortCollectorTestCase(TestCase):

    def setUp(self) -> None:
        self.pc = PortCollector()

    def test_callback_capability(self):
        self.pc('test.exe', NetworkProtocol.IPv4, '0.0.0.0', TransportProtocol.TCP, 1, ConnectionState.LISTENING)
        self.pc(None, NetworkProtocol.IPv6, '::', TransportProtocol.TCP, 2, ConnectionState.ESTABLISHED)
        self.pc('test2.exe', NetworkProtocol.IPv6, '2001:db8::1000', TransportProtocol.UDP, 3, None)
        self.pc('test.exe', NetworkProtocol.IPv4, '127.0.0.1', TransportProtocol.TCP, 1, ConnectionState.LISTENING)
        self.pc(None, NetworkProtocol.IPv6, '::1', TransportProtocol.TCP, 2, ConnectionState.LISTENING)
        self.assertSequenceEqual(self.pc.port_data, [{EXECUTABLE_NAME: 'test.exe',
                                                      NETWORK_PROTOCOL: NetworkProtocol.IPv4,
                                                      TRANSPORT_PROTOCOL: TransportProtocol.TCP, PORT_NUMBER: 1},
                                                     {EXECUTABLE_NAME: 'test2.exe',
                                                      NETWORK_PROTOCOL: NetworkProtocol.IPv6,
                                                      TRANSPORT_PROTOCOL: TransportProtocol.UDP, PORT_NUMBER: 3}])
        self.pc.reset()
        self.assertEqual(len(self.pc.port_data), 0)


@patch_config_app_platform
class WindowsNetstatPortDataParserTestCase(TestCase):
    expected_calls = [call('app1.exe', NetworkProtocol.IPv4, '0.0.0.0', TransportProtocol.TCP, 1,
                           ConnectionState.LISTENING),
                      call(None, NetworkProtocol.IPv4, '0.0.0.0', TransportProtocol.TCP, 2,
                           ConnectionState.LISTENING),
                      call('app2.exe', NetworkProtocol.IPv4, '0.0.0.0', TransportProtocol.TCP, 3,
                           ConnectionState.ESTABLISHED),
                      call(None, NetworkProtocol.IPv4, '0.0.0.0', TransportProtocol.TCP, 4,
                           ConnectionState.ESTABLISHED),
                      call('app3.exe', NetworkProtocol.IPv6, '::', TransportProtocol.TCP, 15,
                           ConnectionState.CLOSE_WAIT),
                      call('app1.exe', NetworkProtocol.IPv6, '::', TransportProtocol.TCP, 1,
                           ConnectionState.LISTENING),
                      call(None, NetworkProtocol.IPv6, '::', TransportProtocol.TCP, 2,
                           ConnectionState.LISTENING),
                      call('app2.exe', NetworkProtocol.IPv4, '0.0.0.0', TransportProtocol.UDP, 1, None),
                      call(None, NetworkProtocol.IPv4, '1.2.3.4', TransportProtocol.UDP, 2, None),
                      call('app1.exe', NetworkProtocol.IPv6, 'fe80::a1:b2:c3:d4', TransportProtocol.UDP, 1, None),
                      call(None, NetworkProtocol.IPv6, 'fe80::a1:b2:c3:d4', TransportProtocol.UDP, 2, None)]

    def setUp(self) -> None:
        self.pc = Mock(spec_set=PortCollector)()
        self.dp = WindowsNetstatPortDataParser(self.pc)

    def test_data_parsing(self):
        data = get_test_data('win_netstat.txt')

        self.dp.extract_data(data)
        self.assertEqual(self.pc.call_count, 11)
        self.pc.assert_has_calls(self.expected_calls, any_order=True)
        # verify that parser can do multiple parses
        self.pc.reset_mock()
        self.dp.extract_data(data)
        self.assertEqual(self.pc.call_count, 11)
        self.pc.assert_has_calls(self.expected_calls, any_order=True)

    def test_line_stream_parsing(self):
        with open_test_file('win_netstat.txt') as data_file:
            with self.dp.line_stream_consumer() as consume:
                for line_no, line in enumerate(data_file):
                    consume(line, line_no)
        self.assertEqual(self.pc.call_count, 11)
        self.pc.assert_has_calls(self.expected_calls, any_order=True)

    def test_unexpected_data_handling(self):
        data = get_test_data('win_netstat3.txt')
        with self.assertRaises(UnexpectedLineError) as c:
            self.dp.extract_data(data)
        self.assertEqual(c.exception.line_no, 6)
        self.assertEqual(c.exception.line, ' [app3.exe]')

    def test_unexpected_data_handling2(self):
        with self.assertRaises(UnexpectedLineError) as c:
            with open_test_file('win_netstat3.txt') as data_file:
                with self.dp.line_stream_consumer() as consume:
                    for line_no, line in enumerate(data_file):
                        consume(line, line_no + 1)
        self.assertEqual(c.exception.line_no, 6)
        self.assertEqual(c.exception.line, ' [app3.exe]')
