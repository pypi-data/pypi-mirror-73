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

from time import sleep, time
from typing import TYPE_CHECKING

from . import config, factory
from .exception import DoRollback
from .parser import PortCollector

if TYPE_CHECKING:
    from .protocol import OperationControl


def find_and_save_ports(control: OperationControl) -> None:
    ds = factory.data_source()
    pc = PortCollector()
    dp = factory.data_parser(pc)
    pm = factory.persistence_manager()
    while not control.interrupted:
        dp.extract_data(ds.get_port_data())
        if pc.port_data:
            pm.save_port_data(pc.port_data, commit=True)
            pc.reset()
        scan_done_time = time()
        control.feedback_pass_done()
        while not control.interrupted and time() - scan_done_time < config.port_scan_interval:
            sleep(config.port_scan_wake_up_interval)


def save_ports_from_data_file(control: OperationControl) -> None:
    sf = config.data_file
    if sf is not None:
        pc = PortCollector()
        dp = factory.data_parser(pc)
        pm = factory.persistence_manager()
        bs = config.import_batch_size
        with open(sf, 'rt') as fo:
            with dp.line_stream_consumer() as consume:
                for line_no, line in enumerate(fo):
                    if control.interrupted:
                        raise DoRollback
                    consume(line, line_no + 1)
                    if len(pc.port_data) >= bs:
                        pm.save_port_data(pc.port_data)
                        pc.reset()
                        control.feedback_pass_done()
                if pc.port_data:
                    pm.save_port_data(pc.port_data)
                    control.feedback_pass_done()
    else:
        raise RuntimeError('No data file is specified in the config')
