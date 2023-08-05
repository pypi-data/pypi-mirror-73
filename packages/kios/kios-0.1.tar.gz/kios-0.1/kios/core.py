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

from typing import TYPE_CHECKING
from sys import platform

from .cli import CLI
from .data import Platform, Application
from . import config, factory
from .operation import find_and_save_ports, save_ports_from_data_file

if TYPE_CHECKING:
    from .protocol import OperationControl, Feedback


class KiosCore:

    def __init__(self):
        self._sm = factory.session_manager()

    def scan(self, control: OperationControl):
        with self._sm.database_session():
            find_and_save_ports(control)

    def import_(self, control: OperationControl):
        with self._sm.database_session():
            save_ports_from_data_file(control)

    def add(self, app_name: str, exec_name: str, force: bool):
        with self._sm.database_session():
            factory.persistence_manager().add_executable_to_app(app_name, exec_name, force)

    def purge(self, app_name: str):
        with self._sm.database_session():
            factory.persistence_manager().purge_app(app_name)

    def list_(self, fb: Feedback):
        with self._sm.database_session():
            for app in factory.persistence_manager().list_apps():
                fb.app_entry(app.name)

    def show_app(self, name: str, fb: Feedback):
        with self._sm.database_session():
            app = factory.persistence_manager().get_app(name)
            if app is not None:
                fb.app_entry(app.name)
                for port in app.ports:
                    fb.port_entry(port.network_protocol, port.transport_protocol, port.number)
                for executable in app.executables:
                    fb.executable_entry(executable.name)

    def remove_executable(self, exec_name: str):
        with self._sm.database_session():
            factory.persistence_manager().remove_executable(exec_name)


def set_platform_defaults():
    if platform == 'win32':
        config.platform = Platform.WINDOWS
        config.app = Application.NETSTAT
        config.db_file = r'%LOCALAPPDATA%\kios\kios.db'


def main():
    set_platform_defaults()
    CLI(KiosCore()).run()
