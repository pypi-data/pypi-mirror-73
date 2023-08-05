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

import builtins
from unittest import TestCase
from unittest.mock import patch, DEFAULT

from thespiae.conf import system as ts
from .singleton import real_app_data_reader as app_data_reader


class AppDataReaderTestCase(TestCase):

    @patch.multiple(builtins, open=DEFAULT)
    @patch.multiple(ts, safe_load=DEFAULT)
    def test_reading_config_file(self, safe_load, open):
        open.return_value.__enter__.return_value = open.return_value
        app_data_reader.read('test_path')
        open.assert_called_once_with('test_path', mode='tr')
        safe_load.assert_called_once_with(open.return_value)
