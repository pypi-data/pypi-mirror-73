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

from signal import SIGINT

from unittest import TestCase
from unittest.mock import patch, NonCallableMock, DEFAULT

from kios.cli import ConsoleOperationControl, CLIFeedback, CLI, _info, _error
from kios import config
from kios.core import KiosCore
from kios.data import NetworkProtocol, TransportProtocol
from kios.exception import DoRollback, ExecutableAssignedError, ToolError, BusyDatabaseError, \
    UnsupportedAppPlatformError, UnexpectedLineError
from .helper import patch_config_app_platform, TestConsoleOperationControl, inside_test_console_operation_control


class OperationControlTestCase(TestCase):

    def setUp(self) -> None:
        self.oc = ConsoleOperationControl()

    def test_interruption(self):
        self.assertFalse(self.oc.interrupted)
        self.oc.interrupt(1, 2)
        self.assertTrue(self.oc.interrupted)

    @patch('kios.cli.signal', autospec=True)
    def test_signal_management(self, signal):
        with self.oc:
            signal.assert_called_once_with(SIGINT, self.oc.interrupt)
            prev = signal.return_value
            signal.reset_mock()
        signal.assert_called_once_with(SIGINT, prev)

    def test_exception_handling(self):
        with self.oc:
            raise DoRollback

    def test_exception_handling2(self):
        with self.assertRaises(Exception):
            with self.oc:
                raise Exception

    def test_feedback_pass(self):
        self.oc.feedback_pass_done()


class CLIFeedbackTestCase(TestCase):

    def setUp(self) -> None:
        self.f = CLIFeedback()

    @patch('kios.cli._info', autospec=True)
    def test_reporting_app_list(self, _info):
        self.f.app_entry('app1')
        self.f.app_entry('app2')
        self.f.report_list()
        _info.assert_called()

    @patch('kios.cli._info', autospec=True)
    def test_reporting_app_details(self, _info):
        self.f.app_entry('app1')
        self.f.port_entry(NetworkProtocol.IPv4, TransportProtocol.TCP, 1)
        self.f.executable_entry('app1.exe')
        self.f.report_details()
        _info.assert_called()

    def test_reporting_app_details2(self):
        with self.assertRaises(RuntimeError):
            self.f.app_entry('app1')
            self.f.app_entry('app2')
            self.f.report_details()

    @patch('kios.cli._info', autospec=True)
    def test_reporting_app_details3(self, _info):
        self.f.report_details()
        _info.assert_called()


def patch_output(t):
    pex = patch('builtins.exit', autospec=True)
    pio = patch.multiple('kios.cli', _info=DEFAULT, _error=DEFAULT, autospec=True)
    return pex(pio(t))


class _CoreMixin:

    def setUp(self) -> None:
        self.core = NonCallableMock(spec_set=KiosCore)


@patch_config_app_platform
@patch('kios.cli.ConsoleOperationControl', new=TestConsoleOperationControl)
@patch_output
class CLIOperationTestCase(_CoreMixin, TestCase):

    @patch('kios.config.port_scan_interval', new=None)
    @patch('sys.argv', new=['kios', 'scan', '15'])
    def test_scanning(self, exit, _info, _error):

        def check_inside_context(oc):
            inside_test_console_operation_control(oc)
            self.assertEqual(config.port_scan_interval, 15)

        self.core.scan.side_effect = check_inside_context
        CLI(self.core).run()
        self.core.scan.assert_called_once()
        _info.assert_called()
        _error.assert_not_called()
        exit.assert_not_called()

    @patch('sys.argv', new=['kios', 'scan'])
    def test_scanning2(self, exit, _info, _error):
        self.core.scan.side_effect = ToolError('abc')
        CLI(self.core).run()
        self.core.scan.assert_called_once()
        _info.assert_called()
        _error.assert_called()
        exit.assert_called_once_with(1)

    @patch('kios.config.data_file', new=None)
    @patch('sys.argv', new=['kios', 'import', r'abc.txt'])
    def test_importing(self, exit, _info, _error):

        def check_inside_context(oc):
            inside_test_console_operation_control(oc)
            self.assertEqual(config.data_file, 'abc.txt')

        self.core.import_.side_effect = check_inside_context
        CLI(self.core).run()
        self.core.import_.assert_called_once()
        _info.assert_called()
        _error.assert_not_called()
        exit.assert_not_called()

    @patch('kios.config.data_file', new=None)
    @patch('sys.argv', new=['kios', 'import', r'abc.txt'])
    def test_importing2(self, exit, _info, _error):
        def check_inside_context(oc):
            inside_test_console_operation_control(oc)
            self.assertEqual(config.data_file, 'abc.txt')
            oc.interrupt()

        self.core.import_.side_effect = check_inside_context
        CLI(self.core).run()
        self.core.import_.assert_called_once()
        _info.assert_called()
        _error.assert_not_called()
        exit.assert_not_called()


@patch_config_app_platform
@patch_output
class ManagementTestCase(_CoreMixin, TestCase):

    @patch('sys.argv', new=['kios', 'add', 'app1', 'app.exe'])
    def test_adding_apps(self, exit, _info, _error):
        CLI(self.core).run()
        self.core.add.assert_called_once_with('app1', 'app.exe', False)
        _info.assert_not_called()
        _error.assert_not_called()
        exit.assert_not_called()

    @patch('sys.argv', new=['kios', 'add', 'app2', 'app.exe'])
    def test_adding_apps2(self, exit, _info, _error):
        self.core.add.side_effect = ExecutableAssignedError('app2', 'app.exe')
        CLI(self.core).run()
        self.core.add.assert_called_once_with('app2', 'app.exe', False)
        _info.assert_not_called()
        _error.assert_called_once()
        exit.assert_called_once_with(1)

    @patch('sys.argv', new=['kios', 'add', '--force', 'app2', 'app.exe'])
    def test_adding_apps3(self, exit, _info, _error):
        CLI(self.core).run()
        self.core.add.assert_called_once_with('app2', 'app.exe', True)
        _info.assert_not_called()
        _error.assert_not_called()
        exit.assert_not_called()

    @patch('sys.argv', new=['kios', 'purge', 'app1'])
    def test_purging_apps(self, exit, _info, _error):
        CLI(self.core).run()
        self.core.purge.assert_called_once_with('app1')
        _info.assert_not_called()
        _error.assert_not_called()
        exit.assert_not_called()

    @patch('kios.cli.CLIFeedback', autospec=True)
    @patch('sys.argv', new=['kios', 'list'])
    def test_listing_apps(self, CLIFeedback, exit, _info, _error):
        CLI(self.core).run()
        fb = CLIFeedback.return_value
        self.core.list_.assert_called_once_with(fb)
        fb.report_list.assert_called_once()
        _error.assert_not_called()
        exit.assert_not_called()

    @patch('kios.cli.CLIFeedback', autospec=True)
    @patch('sys.argv', new=['kios', 'show', 'app'])
    def test_showing_details(self, CLIFeedback, exit, _info, _error):
        CLI(self.core).run()
        fb = CLIFeedback.return_value
        self.core.show_app.assert_called_once_with('app', fb)
        fb.report_details.assert_called_once()
        _error.assert_not_called()
        exit.assert_not_called()

    @patch('sys.argv', new=['kios', 'remove', 'app.exe'])
    def test_removing_executables(self, exit, _info, _error):
        CLI(self.core).run()
        self.core.remove_executable.assert_called_once_with('app.exe')
        _info.assert_not_called()
        _error.assert_not_called()
        exit.assert_not_called()


class SkippedExceptionMessageTestCase(TestCase):

    def test_busy_db_message(self):
        str(BusyDatabaseError())

    def test_unsupported_app_platform_message(self):
        str(UnsupportedAppPlatformError())

    def test_unexpected_line_message(self):
        str(UnexpectedLineError('abc', 1))


@patch('builtins.print', autospec=True)
@patch.multiple('kios.cli', stdout=DEFAULT, stderr=DEFAULT, autospec=True)
class OutputTestCase(TestCase):

    def test_info(self, print, stdout, stderr):
        _info('abc')
        print.assert_called_once_with('abc', file=stdout)

    def test_error(self, print, stdout, stderr):
        _error('abc')
        print.assert_called_once_with('abc', file=stderr)
