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

from string import Template
from typing import TYPE_CHECKING

from .singleton import path_manager

if TYPE_CHECKING:
    from typing import Mapping

complex_string = ' "a bc"; def;\'g;h\';'


class PathManagerMockResetMixin:

    def setUp(self, *args, **kwarg):
        super().setUp(*args, **kwarg)
        path_manager.reset_mock(return_value=True, side_effect=True)
        path_manager.get_system_path.reset_mock(return_value=True, side_effect=True)
        path_manager.get_user_path.reset_mock(return_value=True, side_effect=True)
        path_manager.extend_path_data.reset_mock(return_value=True, side_effect=True)


class ExtensionTemplate(Template):
    delimiter = ''
    idpattern = '%[^=%]+%'


def _helper(data: str, path_extensions: Mapping[str, str]):
    prev = ''
    while prev != data:
        prev = data
        data = ExtensionTemplate(data).safe_substitute(path_extensions)
    return data


def set_path_manager_data(full_extended_path: str, user_path: str, path_extensions: Mapping[str, str]):
    path_manager.get_system_path.return_value = full_extended_path
    path_manager.get_user_path.return_value = user_path
    path_extensions = {'%{}%'.format(key): path_extensions[key] for key in path_extensions}
    path_manager.extend_path_data.side_effect = lambda arg: _helper(arg, path_extensions)
