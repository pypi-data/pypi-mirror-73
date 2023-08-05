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

from gettext import translation

t = translation('kios', fallback=True)
_ = t.gettext


class KiosError(Exception):
    pass


class DoRollback(Exception):
    pass


class UnsupportedAppPlatformError(KiosError):

    def __str__(self):
        return _('Unsupported application and platform')


class BusyDatabaseError(KiosError):

    def __str__(self):
        return _('Database is busy, please try again later')


class ExecutableAssignedError(KiosError):

    def __init__(self, app_name: str, exec_name):
        super().__init__(app_name, exec_name)
        self.app_name = app_name
        self.exec_name = exec_name

    def __str__(self):
        return _('Executable {exec_name} is associated with application {app_name}'.format(exec_name=self.exec_name,
                                                                                           app_name=self.app_name))


class ToolError(KiosError):

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return _('Error running port scan application: {msg}').format(msg=self.msg)


class UnexpectedLineError(KiosError):

    def __init__(self, line, line_no):
        super().__init__(line, line_no)
        self.line = line
        self.line_no = line_no

    def __str__(self):
        return _('Unexpected line {line_no}: {line}').format(line=self.line, line_no=self.line_no)

