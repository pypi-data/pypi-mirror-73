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

from os.path import join, dirname, isabs

from yaml import safe_load

from .singleton import app_data_reader


def get_test_file_path(file_name: str):
    if isabs(file_name):
        return file_name
    else:
        return join(dirname(__file__), file_name if file_name.endswith('.yml') else file_name + '.yml')


def load_yaml_from_test_dir(file_name: str):
    with open(get_test_file_path(file_name), mode='rb') as f:
        return safe_load(f)


def set_app_data_reader_data(path: str):
    app_data_reader.read.side_effect = lambda _: load_yaml_from_test_dir(path)


class AppDataReaderResetMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app_data_reader.reset_mock(side_effect=True)
        app_data_reader.read.reset_mock(side_effect=True)
