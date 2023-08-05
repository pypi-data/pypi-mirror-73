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

from argparse import ArgumentParser
from enum import Enum, auto
from gettext import translation
from signal import signal, SIGINT
from sys import stdout, stderr
from typing import TYPE_CHECKING

from . import config
from .data import Platform, Application, NetworkProtocol, TransportProtocol
from .exception import DoRollback, KiosError
from .protocol import Feedback, OperationControl

if TYPE_CHECKING:
    from .core import KiosCore

t = translation('kios', fallback=True)
_ = t.gettext


class _Action(Enum):
    NOTHING = auto()
    SCAN = auto()
    IMPORT = auto()
    ADD = auto()
    PURGE = auto()
    LIST = auto()
    SHOW = auto()
    REMOVE = auto()


class ConsoleOperationControl(OperationControl):

    def __init__(self):
        self._interrupted = False

    def interrupt(self, *_) -> None:
        self._interrupted = True

    @property
    def interrupted(self) -> bool:
        return self._interrupted

    def feedback_pass_done(self):
        pass

    def __enter__(self):
        self._ph = signal(SIGINT, self.interrupt)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal(SIGINT, self._ph)
        if exc_val is not None and isinstance(exc_val, DoRollback):
            return True


def _info(data):
    print(data, file=stdout)


def _error(data):
    print(data, file=stderr)


class CLIFeedback(Feedback):

    def __init__(self):
        self.apps = []
        self.executables = []
        self.ports = []

    def app_entry(self, name: str):
        self.apps.append(name)

    def port_entry(self, np: NetworkProtocol, tp: TransportProtocol, number: int):
        self.ports.append((np, tp, number))

    def executable_entry(self, name: str):
        self.executables.append(name)

    def report_list(self):
        _info(_('Known applications:'))
        for name in self.apps:
            _info(f' {name}')

    def report_details(self):
        if len(self.apps) == 1:
            _info(_('Data for {app}').format(app=self.apps[0]))
            _info(_('Ports:'))
            for np, tp, n in self.ports:
                _info(f' {np.name}\t{tp.name}\t{n}')
            _info(_('Executables:'))
            for fn in self.executables:
                _info(f' {fn}')
        elif not self.apps:
            _info(_('No application found'))
        else:
            raise RuntimeError('Can\'t report details for multiple applications')


class CLI:

    def __init__(self, core: KiosCore):
        parser = ArgumentParser('kios')
        parser.set_defaults(action=_Action.NOTHING)
        parser.add_argument('--db_file', default=config.db_file,
                            help=_('path to a custom sqlite database file to use'))
        s_parsers = parser.add_subparsers()
        scan_parser = s_parsers.add_parser('scan', help=_('scan for ports applications listen at'))
        scan_parser.add_argument('interval', type=int, metavar='INTERVAL', nargs='?', default=config.port_scan_interval,
                                 help=_('time between scanner sweeps in seconds'))
        scan_parser.set_defaults(action=_Action.SCAN)
        import_parser = s_parsers.add_parser('import',
                                             help=_('process port data captured in a file'))
        import_parser.add_argument('file', metavar='FILE', help=_('path to a capture file'))
        import_parser.add_argument('--platform', choices=[item.name.lower() for item in Platform],
                                   default=config.platform.name.lower(),
                                   help=_('platform the output has been captured on'))
        import_parser.add_argument('--app', choices=[item.name.lower() for item in Application],
                                   default=config.app.name.lower(),
                                   help=_('application used to produce the captured output'))
        import_parser.set_defaults(action=_Action.IMPORT)
        add_parser = s_parsers.add_parser('add', help=_('add new application and executable or attach executable to an '
                                                        'existing app'))
        add_parser.add_argument('--force', default=False, action='store_true', help=_('reassign the executable to the '
                                                                                      'specified app'))
        add_parser.add_argument('app_name', metavar='APP_NAME', default=False, help=_('name of an application to '
                                                                                      '(create and) attach the '
                                                                                      'executable to'))
        add_parser.add_argument('exec_name', metavar='EXEC_NAME', default=False, help=_('name of an executable file to '
                                                                                        'associate with the '
                                                                                        'application'))
        add_parser.set_defaults(action=_Action.ADD)
        purge_parser = s_parsers.add_parser('purge', help=_('delete all information about application with a '
                                                            'specified name, including associated executables and '
                                                            'collected port data'))
        purge_parser.add_argument('app_name', metavar='APP_NAME', help=_('name of an application to purge'))
        purge_parser.set_defaults(action=_Action.PURGE)
        list_parser = s_parsers.add_parser('list', help=_('print names of known applications'))
        list_parser.set_defaults(action=_Action.LIST)
        show_parser = s_parsers.add_parser('show', help=_('print known ports and assigned executables for application '
                                                          'with a specified name'))
        show_parser.add_argument('app_name', metavar='APP_NAME', help=_('name of an application to print data on'))
        show_parser.set_defaults(action=_Action.SHOW)
        remove_parser = s_parsers.add_parser('remove', help=_('remove executable with a specified name'))
        remove_parser.add_argument('exec_name', metavar='EXECUTABLE_NAME', help=_('name of an executable to remove'))
        remove_parser.set_defaults(action=_Action.REMOVE)
        self._ns = parser.parse_args()
        self._core = core

    def run(self):
        config.db_file = self._ns.db_file
        try:
            act = self._ns.action
            if act == _Action.SCAN:
                config.port_scan_interval = self._ns.interval
                _info(_('Scanning system each {port_scan_interval} second(s), Ctrl+C to stop...')
                      .format(port_scan_interval=config.port_scan_interval))
                with ConsoleOperationControl() as control:
                    self._core.scan(control)
                _info(_('Done'))
            elif act == _Action.IMPORT:
                config.platform = Platform[self._ns.platform.upper()]
                config.app = Application[self._ns.app.upper()]
                config.data_file = self._ns.file
                _info(_('Importing {app} ({plat}) data from {df}, Ctrl+C to interrupt...')
                      .format(app=config.app.name.lower(), plat=config.platform.name.lower(), df=config.data_file))
                control = ConsoleOperationControl()
                with control:
                    self._core.import_(control)
                if control.interrupted:
                    _info(_('Interrupted'))
                else:
                    _info(_('Done'))
            elif act == _Action.ADD:
                self._core.add(self._ns.app_name, self._ns.exec_name, self._ns.force)
            elif act == _Action.PURGE:
                self._core.purge(self._ns.app_name)
            elif act == _Action.LIST:
                fb = CLIFeedback()
                self._core.list_(fb)
                fb.report_list()
            elif act == _Action.SHOW:
                fb = CLIFeedback()
                self._core.show_app(self._ns.app_name, fb)
                fb.report_details()
            elif act == _Action.REMOVE:
                self._core.remove_executable(self._ns.exec_name)
        except KiosError as e:
            _error(str(e))
            exit(1)
