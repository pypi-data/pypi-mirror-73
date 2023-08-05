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
from contextvars import ContextVar
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from unittest.mock import patch

from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker

from kios.cli import ConsoleOperationControl
from kios.data import Application, Platform
from kios import config
from kios import factory
from kios.protocol import OperationControl
from .singleton import engine

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_test_data(file_name: str):
    with open_test_file(file_name) as f:
        return f.read()


def open_test_file(file_name: str):
    return open(get_test_file_path(file_name), 'rt')


def get_test_file_path(file_name: str):
    return Path(__file__).parent / file_name


def _restart_nested_transaction(s, tr):
    if tr.nested and tr.parent is not None and not tr.parent.nested:
        s.expire_all()
        s.begin_nested()


path_config_intervals = patch.multiple(config, port_scan_interval=0, port_scan_wake_up_interval=0)
patch_config_app_platform = patch.multiple(config, app=Application.NETSTAT, platform=Platform.WINDOWS)


class TestOperationControl(OperationControl):

    def __init__(self, iterations: int = 2):
        self.interrupted = False
        self._current = 0
        self._max = iterations

    def feedback_pass_done(self):
        self._current += 1
        if self._current >= self._max:
            self.interrupted = True


inside_test_operation_control = ContextVar('inside_test_operation_control', default=None)


class TestConsoleOperationControl(ConsoleOperationControl):

    def __enter__(self):
        self._t = inside_test_operation_control.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        inside_test_operation_control.reset(self._t)


def inside_test_console_operation_control(oc):
    stored_oc = inside_test_operation_control.get()
    if stored_oc is None or stored_oc is not oc:
        raise AssertionError('Wrong or missing test console operation control context')


# don't rely on SingletonThreadPool
test_connection = ContextVar('test_connection', default=None)


class TestSessionFactory:

    def __init__(self):
        self._sm = sessionmaker()
        listen(self._sm, 'after_transaction_end', _restart_nested_transaction)

    def __call__(self) -> Session:
        conn = test_connection.get()
        if conn is not None:
            session = self._sm(bind=conn)
            session.begin_nested()
            return session
        else:
            raise RuntimeError('No test connection found in the current context')

    def dispose(self):
        pass


class DBTestMixin:

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self._sf_patcher = patch('kios.factory.SessionFactory', new=TestSessionFactory)
        self._sf_patcher.start()
        old_conn = test_connection.get()
        if old_conn is not None:
            # if some tearDown got skipped (due to exception), clean up
            old_conn.close()
        conn = engine.connect()
        self._token = test_connection.set(conn)
        self._tr = conn.begin()

    def tearDown(self, *args, **kwargs):
        super().tearDown(*args, **kwargs)
        self._tr.rollback()
        conn = test_connection.get()
        test_connection.reset(self._token)
        conn.close()
        self._sf_patcher.stop()


@contextmanager
def temp_db_real_session_factory():
    with TemporaryDirectory() as d:
        p = Path(d) / 'test.db'
        with patch('kios.config.db_file', new=str(p)):
            sf = factory.SessionFactory()
            try:
                yield sf
            finally:
                sf.dispose()

