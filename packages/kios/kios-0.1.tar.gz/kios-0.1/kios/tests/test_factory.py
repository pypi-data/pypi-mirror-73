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
from unittest.mock import patch, Mock

from kios import config
from kios.db import App, PersistenceManager
from kios.exception import UnsupportedAppPlatformError
from kios import factory
from .helper import patch_config_app_platform, temp_db_real_session_factory
from kios.parser import WindowsNetstatPortDataParser, PortCollector
from kios.system import WindowsNetstatDataSource


class SessionFactoryTestCase(TestCase):

    def test_session_factory_lifecycle(self):
        with temp_db_real_session_factory() as sf:
            s = sf()
            try:
                self.assertEqual(s.query(App).count(), 0)
                r = s.execute('PRAGMA foreign_keys')
                fk, = r.fetchone()
                self.assertTrue(bool(fk))
                r = s.execute('PRAGMA busy_timeout')
                bt, = r.fetchone()
                self.assertEqual(bt, config.db_busy_timeout)
            finally:
                s.close()
            sf.dispose()
            with self.assertRaises(RuntimeError):
                sf()

    @patch('kios.config.db_busy_timeout', new='test')
    def test_session_factory_lifecycle2(self):
        with self.assertRaises(RuntimeError):
            with temp_db_real_session_factory():
                pass

    @patch('kios.config.db_file', new=None)
    def test_missing_db_file_path(self):
        with self.assertRaises(UnsupportedAppPlatformError):
            factory.SessionFactory()


class DataObjectTestCase(TestCase):

    @patch_config_app_platform
    def test_creating_data_source(self):
        self.assertTrue(isinstance(factory.data_source(), WindowsNetstatDataSource))

    def test_creating_data_source2(self):
        with self.assertRaises(UnsupportedAppPlatformError):
            factory.data_source()

    @patch_config_app_platform
    def test_creating_data_parser(self):
        self.assertTrue(isinstance(factory.data_parser(Mock(spec_set=PortCollector)), WindowsNetstatPortDataParser))

    def test_creating_data_parser2(self):
        with self.assertRaises(UnsupportedAppPlatformError):
            factory.data_parser(Mock(spec_set=PortCollector))

    def test_creating_persistence_manager(self):
        self.assertTrue(isinstance(factory.persistence_manager(), PersistenceManager))
