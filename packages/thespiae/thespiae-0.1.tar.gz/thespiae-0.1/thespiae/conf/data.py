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

from dataclasses import dataclass, field, fields
from re import finditer
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Tuple

_FORK_ATTR = 'fork_attr'
_GROUP_ATTR = 'group_attr'


class ConfigPath:
    __slots__ = ['_path']

    def __init__(self, path: str = None):
        if path:
            p_end = 0
            parts = []
            for match in finditer(r'(?P<root>\$)|\[(?P<index>\d+)\]|\.(?P<attribute>[A-Za-z]+)', path):
                start, end = match.span()
                if start != p_end:
                    self._path_error(path, p_end)
                root = match.group('root')
                if root:
                    if start == 0:
                        parts.append((None, None))
                    else:
                        self._path_error(path, p_end)
                else:
                    index = match.group('index')
                    if index is not None:
                        parts.append((int(index), None))
                    else:
                        attribute = match.group('attribute')
                        if attribute:
                            parts.append((None, attribute))
                        else:
                            self._path_error(path, p_end)
                p_end = end
            if p_end != len(path):
                self._path_error(path, p_end)
            self._path = tuple(parts)
        else:
            self._path = ()

    @staticmethod
    def _path_error(path: str, pos: int) -> None:
        raise ValueError(f'Invalid path \'{path}\' at position {pos}')

    def index(self, index: int) -> ConfigPath:
        np = __class__()
        np._path = self._path + ((index, None),)
        return np

    def attribute(self, attribute: str) -> ConfigPath:
        np = __class__()
        np._path = self._path + ((None, attribute),)
        return np

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._path == other._path
        return False

    def __hash__(self):
        return hash(self._path)

    def __len__(self):
        return len(self._path)

    def __str__(self):
        items = []
        for index, attribute in self._path:
            if index is not None:
                items.append(f'[{index}]')
            elif attribute is not None:
                items.append(f'.{attribute}')
            else:
                items.append('$')
        return ''.join(items)

    def __repr__(self):
        return f'{__class__.__name__}(\'{self}\')'


@dataclass(frozen=True)
class AppEntryRef:
    name: str = field(metadata={_FORK_ATTR: 'names', _GROUP_ATTR: True})
    version: str = field(default=None, metadata={_FORK_ATTR: 'versions'})
    architecture: str = field(default=None, metadata={_FORK_ATTR: 'architectures'})

    def __str__(self):
        entries = []
        for ref_field in fields(self.__class__):
            if hasattr(self, ref_field.name):
                val = getattr(self, ref_field.name)
                if val is not None:
                    entries.append(str(val))
        return ':'.join(entries)


@dataclass(frozen=True)
class AppEntry(AppEntryRef):
    keep: bool = False
    skip: bool = False
    installer_url: str = None
    package_url: str = None
    uninstaller_path: str = None
    product_code: str = None
    file_hash: str = None
    command: str = None
    install_args: List[str] = None
    uninstall_args: List[str] = None
    list_args: List[str] = None
    installed_list_entry: str = None
    path_entries: List[str] = None
    file_url: str = None
    file_directory: str = None
    file_name: str = None
    archive_url: str = None
    archive_format: str = None
    unpack_directory: str = None

    @property
    def ref(self) -> AppEntryRef:
        return AppEntryRef(self.name, self.version, self.architecture)


class AppData:

    def __init__(self, app_entries: Iterable[AppEntry]):
        self._to_install = tuple((entry for entry in app_entries if not entry.skip and entry.keep))
        self._to_uninstall = tuple((entry for entry in app_entries if not entry.skip and not entry.keep))

    @property
    def to_install(self) -> Tuple[AppEntry, ...]:
        return self._to_install

    @property
    def to_uninstall(self) -> Tuple[AppEntry, ...]:
        return self._to_uninstall
