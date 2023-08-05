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

from functools import partial
from os.path import expandvars
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen

from . import config
from .data import Platform, Application
from .db import PersistenceManager, SessionManager, Base
from .exception import UnsupportedAppPlatformError
from .parser import WindowsNetstatPortDataParser
from .system import WindowsNetstatDataSource

if TYPE_CHECKING:
    from .parser import PortCollector


def data_source():
    if config.app == Application.NETSTAT and config.platform == Platform.WINDOWS:
        return WindowsNetstatDataSource()
    else:
        raise UnsupportedAppPlatformError


def data_parser(pc: PortCollector):
    if config.app == Application.NETSTAT and config.platform == Platform.WINDOWS:
        return WindowsNetstatPortDataParser(pc)
    else:
        raise UnsupportedAppPlatformError


def persistence_manager():
    return PersistenceManager()


def _errormaker():
    raise RuntimeError('Unable to create new session with disposed engine')


def _on_connect_handler(busy_timeout, conn, _):
    conn.isolation_level = None
    if config.db_debug:
        conn.set_trace_callback(print)
    cur = conn.cursor()
    try:
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute(f'PRAGMA busy_timeout = {busy_timeout}')
    finally:
        cur.close()


def _on_begin_handler(conn):
    conn.execute("BEGIN")


def engine(db_url: str):
    busy_timeout = config.db_busy_timeout
    if not isinstance(busy_timeout, int):
        raise RuntimeError(f'kios.config.db_busy_timeout has unexpected type {type(busy_timeout)}, int expected')
    e = create_engine(db_url, echo=config.db_debug, isolation_level=config.db_isolation)
    listen(e, "connect", partial(_on_connect_handler, busy_timeout))
    listen(e, "begin", _on_begin_handler)
    # TODO: look into embedding alembic <AP>
    Base.metadata.create_all(e)
    return e


class SessionFactory:

    def __init__(self):
        db_file = config.db_file
        if db_file is None:
            raise UnsupportedAppPlatformError
        p = Path(expandvars(db_file))
        p.parent.mkdir(parents=True, exist_ok=True)
        self.engine = engine(f'sqlite:///{str(p)}')
        self._sf = sessionmaker(bind=self.engine)

    def __call__(self):
        return self._sf()

    def dispose(self):
        self._sf = _errormaker
        self.engine.dispose()


def session_manager():
    return SessionManager(SessionFactory())
