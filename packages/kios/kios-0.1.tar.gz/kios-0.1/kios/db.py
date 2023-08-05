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
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, UniqueConstraint, select, bindparam
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlite3 import OperationalError as sq3_OperationalError

from .data import NetworkProtocol, TransportProtocol, NETWORK_PROTOCOL, TRANSPORT_PROTOCOL, PORT_NUMBER, EXECUTABLE_NAME
from .exception import BusyDatabaseError, ExecutableAssignedError

if TYPE_CHECKING:
    from typing import Iterable, Mapping, Any, Iterator, Optional

    from sqlalchemy.orm.session import Session

    from .factory import SessionFactory

Base = declarative_base()


class App(Base):
    __tablename__ = 'app'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Executable(Base):
    __tablename__ = 'executable'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    app_id = Column(Integer, ForeignKey(App.id, ondelete='CASCADE'), nullable=False)
    app = relationship(App, back_populates='executables')


App.executables = relationship(Executable, back_populates='app', passive_deletes=True,
                               order_by=Executable.name)


class Port(Base):
    __tablename__ = 'port'
    __table_args__ = (UniqueConstraint('app_id', 'network_protocol', 'transport_protocol', 'number',
                                       sqlite_on_conflict='IGNORE'),)
    id = Column(Integer, primary_key=True)
    network_protocol = Column(Enum(NetworkProtocol), nullable=False)
    transport_protocol = Column(Enum(TransportProtocol), nullable=False)
    number = Column(Integer, nullable=False)
    app_id = Column(Integer, ForeignKey(App.id, ondelete='CASCADE'), nullable=False)
    app = relationship(App, back_populates='ports')


App.ports = relationship(Port, back_populates='app', passive_deletes=True,
                         order_by=Port.number & Port.transport_protocol & Port.network_protocol)

_port_t = Port.__table__
_executable_t = Executable.__table__

session: ContextVar[Session] = ContextVar('session', default=None)


class SessionManager:

    def __init__(self, session_factory: SessionFactory):
        self._sf = session_factory

    @contextmanager
    def database_session(self) -> Iterator[Session]:
        s = session.get()
        if s is None:
            s = None
            token = None
            try:
                s = self._sf()
                token = session.set(s)
                yield s
                s.commit()
            except Exception:
                s.rollback()
                raise
            finally:
                if token is not None:
                    session.reset(token)
                if s is not None:
                    s.close()
        else:
            raise RuntimeError('Session is already present in the current context')


@contextmanager
def present_session() -> Iterator[Session]:
    s = session.get()
    try:
        if s is not None:
            yield s
        else:
            raise RuntimeError('No database session in the current context')
    except OperationalError as e:
        if isinstance(e.orig, sq3_OperationalError):
            msg, = e.orig.args
            # best we can do with sqlite3
            if msg == 'database is locked':
                raise BusyDatabaseError from e
        raise


_app_id_select = select([bindparam(NETWORK_PROTOCOL, type_=Enum(NetworkProtocol)),
                         bindparam(TRANSPORT_PROTOCOL, type_=Enum(TransportProtocol)),
                         bindparam(PORT_NUMBER, type_=Integer),
                         _executable_t.c.app_id]).where(_executable_t.c.name == bindparam(EXECUTABLE_NAME))
_port_insert = _port_t.insert().from_select([_port_t.c.network_protocol, _port_t.c.transport_protocol,
                                             _port_t.c.number, _port_t.c.app_id], _app_id_select)


class PersistenceManager:

    @staticmethod
    def save_port_data(ports: Iterable[Mapping[str, Any]], *, commit=False) -> None:
        with present_session() as s:
            s.execute(_port_insert, ports)
            if commit:
                s.commit()

    @staticmethod
    def add_executable_to_app(app_name: str, exec_name: str, force: bool) -> None:
        with present_session() as s:
            app = s.query(App).filter(App.name == app_name).one_or_none()
            if app is None:
                app = App(name=app_name)
                s.add(app)
            executable = s.query(Executable).filter(Executable.name == exec_name).one_or_none()
            if executable is None:
                executable = Executable(name=exec_name)
                s.add(executable)
            elif executable.app is not app and not force:
                raise ExecutableAssignedError(executable.app.name, exec_name)
            executable.app = app

    @staticmethod
    def purge_app(name: str) -> None:
        with present_session() as s:
            s.query(App).filter(App.name == name).delete(synchronize_session=False)

    @staticmethod
    def list_apps() -> Iterable[App]:
        with present_session() as s:
            return s.query(App).order_by(App.name).all()

    @staticmethod
    def get_app(name: str) -> Optional[App]:
        with present_session() as s:
            return s.query(App).filter(App.name == name).one_or_none()

    @staticmethod
    def remove_executable(name: str) -> None:
        with present_session() as s:
            s.query(Executable).filter(Executable.name == name).delete(synchronize_session=False)

