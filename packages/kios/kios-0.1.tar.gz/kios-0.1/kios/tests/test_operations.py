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
from unittest.mock import patch, call

from kios import config
from kios.data import EXECUTABLE_NAME, NETWORK_PROTOCOL, TRANSPORT_PROTOCOL, PORT_NUMBER, NetworkProtocol, \
    TransportProtocol
from kios.exception import DoRollback, UnexpectedLineError
from kios.operation import find_and_save_ports, save_ports_from_data_file
from .helper import get_test_data, TestOperationControl, get_test_file_path, patch_config_app_platform

_data_se = [get_test_data('win_netstat.txt'), get_test_data('win_netstat2.txt')]


path_config_data_file = patch('kios.config.data_file', new=get_test_file_path('win_netstat.txt'))

part1 = [{EXECUTABLE_NAME: 'app1.exe', NETWORK_PROTOCOL: NetworkProtocol.IPv4,
          TRANSPORT_PROTOCOL: TransportProtocol.TCP, PORT_NUMBER: 1},
         {EXECUTABLE_NAME: None, NETWORK_PROTOCOL: NetworkProtocol.IPv4,
          TRANSPORT_PROTOCOL: TransportProtocol.TCP, PORT_NUMBER: 2},
         {EXECUTABLE_NAME: 'app1.exe', NETWORK_PROTOCOL: NetworkProtocol.IPv6,
          TRANSPORT_PROTOCOL: TransportProtocol.TCP, PORT_NUMBER: 1}]
part2 = [{EXECUTABLE_NAME: None, NETWORK_PROTOCOL: NetworkProtocol.IPv6,
          TRANSPORT_PROTOCOL: TransportProtocol.TCP, PORT_NUMBER: 2},
         {EXECUTABLE_NAME: 'app2.exe', NETWORK_PROTOCOL: NetworkProtocol.IPv4,
          TRANSPORT_PROTOCOL: TransportProtocol.UDP, PORT_NUMBER: 1},
         {EXECUTABLE_NAME: None, NETWORK_PROTOCOL: NetworkProtocol.IPv4,
          TRANSPORT_PROTOCOL: TransportProtocol.UDP, PORT_NUMBER: 2}]
part3 = [{EXECUTABLE_NAME: 'app1.exe', NETWORK_PROTOCOL: NetworkProtocol.IPv6,
          TRANSPORT_PROTOCOL: TransportProtocol.UDP, PORT_NUMBER: 1},
         {EXECUTABLE_NAME: None, NETWORK_PROTOCOL: NetworkProtocol.IPv6,
          TRANSPORT_PROTOCOL: TransportProtocol.UDP, PORT_NUMBER: 2}]
port_data1 = [*part1, *part2, *part3]
port_data2 = [{EXECUTABLE_NAME: 'app3.exe', NETWORK_PROTOCOL: NetworkProtocol.IPv6,
               TRANSPORT_PROTOCOL: TransportProtocol.UDP, PORT_NUMBER: 3}]


@patch_config_app_platform
@patch('kios.factory.persistence_manager', autospec=True)
class OperationsTestCase(TestCase):

    @patch('kios.operation.time', autospec=True, side_effect=[0, 1, 6, 10, 0, 1, 6, 10])
    @patch('kios.operation.sleep', autospec=True)
    @patch('kios.factory.data_source', autospec=True, **{'return_value.get_port_data.side_effect': _data_se})
    def test_find_and_save_ports_behavior(self, data_source, sleep, time, persistence_manager):
        find_and_save_ports(TestOperationControl())
        sleep.assert_called_once_with(config.port_scan_wake_up_interval)
        self.assertEqual(persistence_manager.return_value.save_port_data.call_count, 2)
        persistence_manager.return_value.save_port_data.assert_has_calls([call(port_data1, commit=True),
                                                                          call(port_data2, commit=True)])
        self.assertEqual(data_source.return_value.get_port_data.call_count, 2)

    @path_config_data_file
    def test_save_ports_from_data_file_behavior(self, persistence_manager):
        save_ports_from_data_file(TestOperationControl())
        self.assertEqual(persistence_manager.return_value.save_port_data.call_count, 1)
        persistence_manager.return_value.save_port_data.assert_has_calls([call(port_data1)])

    @path_config_data_file
    @patch('kios.config.import_batch_size', new=3)
    def test_save_ports_from_data_file_behavior2(self, persistence_manager):
        save_ports_from_data_file(TestOperationControl(3))
        self.assertEqual(persistence_manager.return_value.save_port_data.call_count, 3)
        persistence_manager.return_value.save_port_data.assert_has_calls([call(part1), call(part2), call(part3)])

    @path_config_data_file
    @patch('kios.config.import_batch_size', new=3)
    def test_save_ports_from_data_file_behavior3(self, persistence_manager):
        with self.assertRaises(DoRollback):
            save_ports_from_data_file(TestOperationControl(2))
        self.assertEqual(persistence_manager.return_value.save_port_data.call_count, 2)
        persistence_manager.return_value.save_port_data.assert_has_calls([call(part1), call(part2)])

    @patch('kios.config.data_file', new=None)
    def test_save_ports_from_data_file_behaviour4(self, persistence_manager):
        with self.assertRaises(RuntimeError):
            save_ports_from_data_file(TestOperationControl())
        persistence_manager.return_value.save_port_data.assert_not_called()

    @patch('kios.config.data_file', new=get_test_file_path('win_netstat3.txt'))
    def test_save_ports_from_data_file_behaviour5(self, persistence_manager):
        with self.assertRaises(UnexpectedLineError) as c:
            save_ports_from_data_file(TestOperationControl())
        persistence_manager.return_value.save_port_data.assert_not_called()
        self.assertEqual(c.exception.line_no, 6)
        self.assertEqual(c.exception.line, ' [app3.exe]')
