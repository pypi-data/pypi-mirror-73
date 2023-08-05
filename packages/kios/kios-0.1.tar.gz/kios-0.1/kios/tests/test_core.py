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

from unittest import TestCase
from unittest.mock import patch, NonCallableMock, call, DEFAULT, Mock

from kios import factory
from kios.core import KiosCore, set_platform_defaults, main
from kios import config
from kios.data import NetworkProtocol, TransportProtocol, Application, Platform
from kios.db import App, Executable, Port
from kios.exception import DoRollback, ExecutableAssignedError
from kios.protocol import Feedback
from .helper import DBTestMixin, get_test_data, TestOperationControl, path_config_intervals, get_test_file_path, \
    patch_config_app_platform

_data_se = [get_test_data('win_netstat2.txt'), get_test_data('win_netstat2.txt')]

patch_data_file = patch('kios.config.data_file', new=get_test_file_path('win_netstat.txt'))


@patch_config_app_platform
class PortActionsTestCase(DBTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        with factory.session_manager().database_session() as s:
            app1 = App(name='app1')
            app1.executables = [Executable(name='app1.exe')]
            app2 = App(name='app2')
            app2.executables = [Executable(name='app2.exe')]
            app3 = App(name='app3')
            app3.executables = [Executable(name='app3.exe')]
            s.add_all([app1, app2, app3])
        self.core = KiosCore()

    @path_config_intervals
    @patch('kios.factory.data_source', autospec=True, **{'return_value.get_port_data.side_effect': _data_se * 2})
    def test_scanning(self, data_source):
        self.core.scan(TestOperationControl())
        self.verify_state()
        self.core.scan(TestOperationControl())
        self.verify_state()

    @patch('kios.config.data_file', new=get_test_file_path('win_netstat2.txt'))
    def test_importing(self):
        self.core.import_(TestOperationControl())
        self.verify_state()
        self.core.import_(TestOperationControl())
        self.verify_state()

    @patch_data_file
    def test_importing2(self):
        self.core.import_(TestOperationControl())
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(Port).count(), 4)

    @patch_data_file
    @patch('kios.config.import_batch_size', new=2)
    def test_importing3(self):
        with self.assertRaises(DoRollback):
            self.core.import_(TestOperationControl(1))
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(Port).count(), 0)

    def verify_state(self):
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(Port).join(App).join(Executable)
                             .filter(Executable.name == 'app3.exe', Port.network_protocol == NetworkProtocol.IPv6,
                                     Port.transport_protocol == TransportProtocol.UDP, Port.number == 3).count(), 1)


class AppActionsTestCase(DBTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.core = KiosCore()

    def test_addition(self):
        self.core.add('testapp1', 'testapp.exe', False)
        self.verify_state()
        self.core.add('testapp1', 'testapp.exe', False)
        self.verify_state()

    def test_addition2(self):
        self.core.add('testapp1', 'testapp.exe', False)
        self.verify_state()
        with self.assertRaises(ExecutableAssignedError) as c:
            self.core.add('testapp2', 'testapp.exe', False)
        self.assertEqual(c.exception.app_name, 'testapp1')
        self.assertEqual(c.exception.exec_name, 'testapp.exe')
        self.verify_state()

    def test_addition3(self):
        self.core.add('testapp1', 'testapp.exe', False)
        self.verify_state()
        self.core.add('testapp2', 'testapp.exe', True)
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(App).count(), 2)
            self.assertEqual(s.query(App).filter(App.name == 'testapp1').count(), 1)
            app2 = s.query(App).filter(App.name == 'testapp2').one()
            self.assertEqual(s.query(Executable).count(), 1)
            self.assertEqual(s.query(Executable).filter(Executable.name == 'testapp.exe',
                                                        Executable.app == app2).count(), 1)

    def verify_state(self):
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(App).count(), 1)
            app = s.query(App).filter(App.name == 'testapp1').one()
            self.assertEqual(s.query(Executable).count(), 1)
            self.assertEqual(s.query(Executable).filter(Executable.name == 'testapp.exe',
                                                        Executable.app == app).count(), 1)


class AppActionsTestCase2(DBTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        with factory.session_manager().database_session() as s:
            app = App(name='test1')
            app2 = App(name='test2')
            app.ports = [Port(network_protocol=NetworkProtocol.IPv4, transport_protocol=TransportProtocol.UDP,
                              number=1),
                         Port(network_protocol=NetworkProtocol.IPv6, transport_protocol=TransportProtocol.TCP,
                              number=2)]
            app.executables = [Executable(name='test1.exe'), Executable(name='test1_helper.exe')]
            s.add(app)
            app2.ports = [Port(network_protocol=NetworkProtocol.IPv6, transport_protocol=TransportProtocol.UDP,
                               number=3),
                          Port(network_protocol=NetworkProtocol.IPv4, transport_protocol=TransportProtocol.TCP,
                               number=4)]
            app2.executables = [Executable(name='test2.exe'), Executable(name='test2_helper.exe')]
            s.add(app2)
        self.core = KiosCore()

    def test_purging(self):
        self.core.purge('test1')
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(App).count(), 1)
            self.assertEqual(s.query(Executable).count(), 2)
            self.assertEqual(s.query(Port).count(), 2)
            app2 = s.query(App).filter(App.name == 'test2').one()
            self.assertEqual(s.query(Executable).filter(Executable.name == 'test2.exe',
                                                        Executable.app == app2).count(), 1)
            self.assertEqual(s.query(Executable).filter(Executable.name == 'test2_helper.exe',
                                                        Executable.app == app2).count(), 1)
            self.assertEqual(s.query(Port).filter(Port.network_protocol == NetworkProtocol.IPv6,
                                                  Port.transport_protocol == TransportProtocol.UDP,
                                                  Port.number == 3, Port.app == app2).count(), 1)
            self.assertEqual(s.query(Port).filter(Port.network_protocol == NetworkProtocol.IPv4,
                                                  Port.transport_protocol == TransportProtocol.TCP,
                                                  Port.number == 4, Port.app == app2).count(), 1)

    def test_listing_apps(self):
        fb = NonCallableMock(spec_set=Feedback)
        self.core.list_(fb)
        self.assertEqual(fb.app_entry.call_count, 2)
        fb.app_entry.assert_has_calls([call('test1'), call('test2')])

    def test_showing_app(self):
        fb = NonCallableMock(spec_set=Feedback)
        self.core.show_app('test1', fb)
        fb.app_entry.called_once_with('test1')
        self.assertEqual(fb.port_entry.call_count, 2)
        fb.port_entry.assert_has_calls([call(NetworkProtocol.IPv4, TransportProtocol.UDP, 1),
                                        call(NetworkProtocol.IPv6, TransportProtocol.TCP, 2)], any_order=True)
        self.assertEqual(fb.executable_entry.call_count, 2)
        fb.executable_entry.assert_has_calls([call('test1.exe'), call('test1_helper.exe')], any_order=True)

    def test_showing_app2(self):
        fb = NonCallableMock(spec_set=Feedback)
        self.core.show_app('test3', fb)
        self.assertEqual(len(fb.method_calls), 0)

    def test_removing(self):
        self.core.remove_executable('test1_helper.exe')
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(App).count(), 2)
            self.assertEqual(s.query(Executable).count(), 3)
            self.assertEqual(s.query(Port).count(), 4)
            app = s.query(App).filter(App.name == 'test1').one()
            self.assertEqual(s.query(Executable).filter(Executable.app == app).count(), 1)
            self.assertEqual(s.query(Executable).filter(Executable.name == 'test1.exe',
                                                        Executable.app == app).count(), 1)


class OtherTestCase(TestCase):

    @patch.multiple(config, platform=None, app=None)
    @patch('kios.core.platform', new='win32')
    def test_setting_platform_defaults(self):
        set_platform_defaults()
        self.assertEqual(config.app, Application.NETSTAT)
        self.assertEqual(config.platform, Platform.WINDOWS)

    @patch.multiple('kios.core', set_platform_defaults=DEFAULT, CLI=DEFAULT, KiosCore=DEFAULT, autospec=True)
    def test_main(self, set_platform_defaults, CLI, KiosCore):
        o = Mock()
        o.attach_mock(set_platform_defaults, 'spd')
        o.attach_mock(CLI, 'cli')
        o.attach_mock(KiosCore, 'kc')
        main()
        self.assertSequenceEqual(o.mock_calls, [call.spd(), call.kc(),
                                                *call.cli(KiosCore.return_value).run().call_list()])

