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

from thespiae.cli import CLI
from thespiae.conf import parse_config_file
from thespiae.install import handle_software_changes
from thespiae.path import update_user_path


def main():
    with CLI('thespiae') as ui:
        config_data = parse_config_file(ui.params.config_file)
        handle_software_changes(ui.params.data_dir, config_data, ui.feedback)
        update_user_path(config_data, ui.feedback)
