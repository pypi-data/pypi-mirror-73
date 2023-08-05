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

from typing import TYPE_CHECKING

from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream
from antlr4.error.Errors import ParseCancellationException

from .envparse.EnvLexer import EnvLexer
from .envparse.EnvParserListener import EnvParserListener
from .exception import PathEntryError, PathError, InconsistentUserPathEntryDataError, \
    InconsistentActualPathEntryDataError, InconsistentUserPathExtensionError, InconsistentPathEntryExtensionError, \
    InvalidPathEntryError, InvalidSystemPathError, InvalidUserPathError
from .factory import EnvParser

if TYPE_CHECKING:
    from typing import List, Container, Sequence, Tuple
    
    from thespiae.conf.data import AppData, AppEntry
    from .protocol import Feedback
    from .system import PathManager


class _EntryListener(EnvParserListener):

    def __init__(self):
        self._processed_entries = []
        self._raw_entries = []

    def enterEntry(self, ctx: EnvParser.EntryContext) -> None:
        ns = ctx.UNQUOTED_STRING()
        if ns:
            raw = processed = ns.getText()
        else:
            raw = ctx.DOUBLE_QUOTED_STRING().getText()
            processed = raw[1:-1]
        self._raw_entries.append(raw)
        self._processed_entries.append(processed)

    @property
    def raw_entries(self) -> List[str]:
        return self._raw_entries

    @property
    def processed_entries(self) -> List[str]:
        return self._processed_entries


def _parser(path: str, build_trees=True) -> EnvParser:
    return EnvParser(CommonTokenStream(EnvLexer(InputStream(path))), build_parse_trees=build_trees)


def get_path_entries(path_string: str, raw: bool) -> List[str]:
    walker = ParseTreeWalker()
    ls = _EntryListener()
    p = _parser(path_string)
    try:
        walker.walk(ls, p.path())
    except ParseCancellationException:
        raise PathError
    return ls.raw_entries if raw else ls.processed_entries


def get_single_path_entry(data: str, raw: bool) -> str:
    walker = ParseTreeWalker()
    ls = _EntryListener()
    try:
        walker.walk(ls, _parser(data).single_entry())
    except ParseCancellationException:
        raise PathEntryError
    return ls.raw_entries[0] if raw else ls.processed_entries[0]


def construct_new_user_path(system_path_entries: Container[str], raw_user_path_entries: Sequence[str],
                            user_path_entries: Sequence[str], raw_actual_entries: Sequence[str],
                            actual_entries: Sequence[str], obsolete_entries: Container[str]):
    new_user_path_entries = []
    if len(raw_user_path_entries) != len(user_path_entries):
        raise InconsistentUserPathEntryDataError
    if len(raw_actual_entries) != len(actual_entries):
        raise InconsistentActualPathEntryDataError
    for raw_entry, entry in zip(raw_user_path_entries, user_path_entries):
        if entry in actual_entries or entry not in obsolete_entries:
            new_user_path_entries.append(raw_entry)
    for raw_entry, entry in zip(raw_actual_entries, actual_entries):
        if entry not in system_path_entries and entry not in user_path_entries:
            new_user_path_entries.append(raw_entry)
    return ';'.join(new_user_path_entries)


class PathProcessor:

    def __init__(self, manager: PathManager):
        self.manager = manager

    def _extract_path_data(self, entry: AppEntry) -> Tuple[List[str], List[str]]:
        single_raw_entries = []
        single_entries = []
        if entry.path_entries:
            for path_entry in entry.path_entries:
                try:
                    single_raw_entry = get_single_path_entry(path_entry, True)
                except PathEntryError:
                    raise InvalidPathEntryError(entry, path_entry)
                else:
                    single_raw_entries.append(single_raw_entry)
                    extended_entry = self.manager.extend_path_data(single_raw_entry)
                    try:
                        single_entry = get_single_path_entry(extended_entry, False)
                    except PathEntryError:
                        raise InconsistentPathEntryExtensionError(entry, path_entry, extended_entry)
                    else:
                        single_entries.append(single_entry)
        return single_raw_entries, single_entries

    def process_path_changes(self, config: AppData, fb: Feedback) -> None:
        raw_actual_entries = []
        actual_entries = []
        raw_obsolete_entries = []
        obsolete_entries = []
        fb.report_path_analysis()
        for e in config.to_install:
            raw, extended = self._extract_path_data(e)
            raw_actual_entries += raw
            actual_entries += extended
        for e in config.to_uninstall:
            raw, extended = self._extract_path_data(e)
            raw_obsolete_entries += raw
            obsolete_entries += extended
        try:
            system = get_path_entries(self.manager.extend_path_data(self.manager.get_system_path()), False)
        except PathError:
            raise InvalidSystemPathError
        else:
            raw_user_path = self.manager.get_user_path()
            try:
                raw_user_path_entries = get_path_entries(raw_user_path, True)
                user_path = self.manager.extend_path_data(raw_user_path)
                user_path_entries = get_path_entries(user_path, False)
            except PathError:
                raise InvalidUserPathError
            else:
                try:
                    new_user_path = construct_new_user_path(set(system), raw_user_path_entries, user_path_entries,
                                                            raw_actual_entries, actual_entries, set(obsolete_entries))
                except InconsistentUserPathEntryDataError:
                    raise InconsistentUserPathExtensionError(raw_user_path, user_path)
                else:
                    if new_user_path != raw_user_path:
                        fb.confirm_user_path_update(raw_user_path, new_user_path)
                        self.manager.set_user_path(new_user_path)
                        self.manager.notify_path_change()
                        fb.report_user_path_updated()
                    else:
                        fb.report_user_path_no_changes()
