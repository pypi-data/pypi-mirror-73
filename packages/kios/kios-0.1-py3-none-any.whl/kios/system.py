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

from subprocess import run, CalledProcessError

from .exception import ToolError


class WindowsNetstatDataSource:

    @staticmethod
    def get_port_data() -> str:
        res = None
        try:
            res = run(['netstat', '-a', '-n', '-b'], capture_output=True, text=True)
            res.check_returncode()
            return res.stdout
        except CalledProcessError as e:
            if e.returncode == 1 and res is not None:
                raise ToolError(res.stdout) from e
            else:
                raise
