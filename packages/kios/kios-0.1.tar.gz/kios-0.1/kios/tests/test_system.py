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

from subprocess import CalledProcessError
from unittest import TestCase
from unittest.mock import patch

from kios.exception import ToolError
from kios.system import WindowsNetstatDataSource
from .helper import get_test_data


class WindowsNetstatDataSourceTestCase(TestCase):
    ds = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.ds = WindowsNetstatDataSource()

    @patch(target='kios.system.run', autospec=True)
    def test_getting_data(self, run):
        data = get_test_data('win_netstat.txt')
        type(run.return_value).stdout = data
        self.assertEqual(self.ds.get_port_data(), data)
        run.assert_called_once_with(['netstat', '-a', '-n', '-b'], capture_output=True, text=True)

    @patch(target='kios.system.run', autospec=True)
    def test_getting_data2(self, run):
        run.return_value.stdout = 'test'
        run.return_value.check_returncode.side_effect = CalledProcessError(1, [])
        with self.assertRaises(ToolError) as c:
            self.ds.get_port_data()
        self.assertEqual(c.exception.msg, 'test')

    @patch(target='kios.system.run', autospec=True)
    def test_getting_data3(self, run):
        run.return_value.check_returncode.side_effect = CalledProcessError(2, [])
        with self.assertRaises(Exception):
            self.ds.get_port_data()
