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
from unittest.mock import patch

from sqlalchemy.exc import OperationalError

from kios.exception import BusyDatabaseError
from kios.data import TRANSPORT_PROTOCOL, NETWORK_PROTOCOL, PORT_NUMBER, EXECUTABLE_NAME, NetworkProtocol, \
    TransportProtocol
from kios.db import PersistenceManager, App, Executable, Port, present_session, session
from kios import factory

from .helper import DBTestMixin, temp_db_real_session_factory


class SessionManagerTestCase(DBTestMixin, TestCase):

    def test_commit(self):
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(App).count(), 0)
            app = App(name='testapp')
            s.add(app)
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(App).count(), 1)

    def test_rollback(self):
        with self.assertRaises(Exception):
            with factory.session_manager().database_session() as s:
                self.assertEqual(s.query(App).count(), 0)
                app = App(name='testapp')
                s.add(app)
                raise Exception
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(App).count(), 0)

    def test_existing_session(self):
        with factory.session_manager().database_session():
            with self.assertRaises(RuntimeError):
                with factory.session_manager().database_session():
                    pass


class PresentSessionTestCase(TestCase):

    def test_no_present_session(self):
        with self.assertRaises(RuntimeError):
            with present_session():
                pass

    @patch('kios.config.db_busy_timeout', new=1)
    def test_error_handling(self):
        with temp_db_real_session_factory() as sf:
            s1 = sf()
            s2 = sf()
            token = session.set(s2)
            try:
                s1.add(App(name='app1'))
                s1.flush()
                with self.assertRaises(BusyDatabaseError):
                    with present_session() as s:
                        s.add(App(name='app2'))
                        s.flush()
                s2.rollback()
                with self.assertRaises(OperationalError):
                    with present_session() as s:
                        s.execute('ashdiaushd')
            finally:
                session.reset(token)
                s1.close()
                s2.close()


class PersistenceManagerTestCase(DBTestMixin, TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pm = PersistenceManager()

    def setUp(self):
        super().setUp()
        with factory.session_manager().database_session() as s:
            app = App(name='testapp')
            app.executables = [Executable(name='testapp.exe'), Executable(name='testapp_helper.exe')]
            s.add(app)
            s.flush()
            self.app_id = app.id

    def test_saving_port_data(self):
        with factory.session_manager().database_session():
            port_data = [{TRANSPORT_PROTOCOL: TransportProtocol.UDP, NETWORK_PROTOCOL: NetworkProtocol.IPv4,
                          PORT_NUMBER: 1, EXECUTABLE_NAME: 'testapp.exe'},
                         {TRANSPORT_PROTOCOL: TransportProtocol.TCP, NETWORK_PROTOCOL: NetworkProtocol.IPv6,
                          PORT_NUMBER: 1, EXECUTABLE_NAME: 'testapp_helper.exe'}]
            self.pm.save_port_data(port_data)
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(Port).count(), 2)
            self.assertEqual(s.query(Port).filter(Port.app_id == self.app_id, Port.number == 1,
                                                  Port.network_protocol == NetworkProtocol.IPv4,
                                                  Port.transport_protocol == TransportProtocol.UDP).count(), 1)
            self.assertEqual(s.query(Port).filter(Port.app_id == self.app_id, Port.number == 1,
                                                  Port.network_protocol == NetworkProtocol.IPv6,
                                                  Port.transport_protocol == TransportProtocol.TCP).count(), 1)

    def test_saving_port_data2(self):
        with self.assertRaises(Exception):
            with factory.session_manager().database_session():
                port_data = [{TRANSPORT_PROTOCOL: TransportProtocol.TCP, NETWORK_PROTOCOL: NetworkProtocol.IPv6,
                              PORT_NUMBER: 1, EXECUTABLE_NAME: 'testapp_helper.exe'}]
                self.pm.save_port_data(port_data, commit=True)
                raise Exception
        with factory.session_manager().database_session() as s:
            self.assertEqual(s.query(Port).count(), 1)
            self.assertEqual(s.query(Port).filter(Port.app_id == self.app_id, Port.number == 1,
                                                  Port.network_protocol == NetworkProtocol.IPv6,
                                                  Port.transport_protocol == TransportProtocol.TCP).count(), 1)
