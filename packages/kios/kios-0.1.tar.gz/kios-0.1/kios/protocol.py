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

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .data import NetworkProtocol, TransportProtocol


class OperationControl(Protocol):
    interrupted: bool

    @abstractmethod
    def feedback_pass_done(self):
        raise NotImplementedError


class Feedback(Protocol):

    @abstractmethod
    def app_entry(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def port_entry(self, np: NetworkProtocol, tp: TransportProtocol, number: int):
        raise NotImplementedError

    @abstractmethod
    def executable_entry(self, name: str):
        raise NotImplementedError
