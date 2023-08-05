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

from unittest import TestCase
from unittest.mock import patch, DEFAULT

from thespiae import core


@patch.multiple(core, CLI=DEFAULT, parse_config_file=DEFAULT, handle_software_changes=DEFAULT,
                update_user_path=DEFAULT, autospec=True)
class TestMain(TestCase):

    def test_main(self, CLI, parse_config_file, handle_software_changes, update_user_path):
        core.main()
        params = CLI.return_value.__enter__.return_value.params
        fb = CLI.return_value.__enter__.return_value.feedback
        parse_config_file.assert_called_once_with(params.config_file)
        handle_software_changes.assert_called_once_with(params.data_dir, parse_config_file.return_value, fb)
        update_user_path.assert_called_once_with(parse_config_file.return_value, fb)
