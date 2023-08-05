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

from collections import defaultdict
from dataclasses import fields, MISSING, asdict
from string import Template
from typing import TYPE_CHECKING, Mapping, List, Iterable, MutableMapping

from .data import AppEntry, AppData, ConfigPath, AppEntryRef, _FORK_ATTR, _GROUP_ATTR
from .exception import _CircularReferenceError, AppDataMissingFieldError, \
    AppDataFieldValueTypeError, AppDataCircularReferenceError, ConfigElementTypeError, ConfigExcessiveAttributeError, \
    ConfigRequiredAttributesNotFoundError, ConfigDuplicatedEntryIdentityError, ConfigIncompleteBranchesError

if TYPE_CHECKING:
    from typing import Sequence, FrozenSet, Set, MutableSet, Any, Optional, Tuple, Iterator

    from .system import AppDataReader

_fork_eliminations = {field.name: field.metadata[_FORK_ATTR] for field in fields(AppEntryRef)}
_group_by = frozenset((field.name for field in fields(AppEntryRef) if field.metadata.get(_GROUP_ATTR)))
_fork_set = frozenset(_fork_eliminations.values())


class _LazyExpandedDict(Mapping):

    def __iter__(self):
        return iter(self.raw)

    def __len__(self):
        return len(self.raw)

    def __new__(cls, raw: Mapping, refined: Mapping = None):
        if raw is not None:
            return super().__new__(cls, raw, refined)
        else:
            return None

    def __init__(self, raw: Mapping, refined: Mapping = None):
        self.raw = raw
        self.refined = refined
        self._final = {}
        self._breaker = object()

    def _format_helper(self, data):
        if isinstance(data, str):
            if self.refined is not None:
                template = Template(data)
                data = template.safe_substitute(self.refined)
            while True:
                prev = data
                template = Template(prev)
                data = template.safe_substitute(self)
                if prev == data:
                    return data
        elif isinstance(data, list):
            return [self._format_helper(e) for e in data]
        else:
            return data

    def __getitem__(self, key):
        data = self._final.get(key)
        if data is self._breaker:
            raise _CircularReferenceError
        if data is not None:
            return data
        raw_data = self.raw.get(key)
        if raw_data is None:
            raise KeyError
        self._final[key] = self._breaker
        final_data = self._format_helper(raw_data)
        self._final[key] = final_data
        return final_data


# TODO: support type unions <AP>
def _validate_types(v, t, f_name: str, paths: Sequence[ConfigPath], position: int = None) -> None:
    ot = getattr(t, '__origin__', None)
    if ot is None:
        if not isinstance(v, t):
            raise AppDataFieldValueTypeError(paths, f_name, position, t, type(v))
    else:
        if issubclass(ot, Iterable):
            if isinstance(v, ot):
                if len(t.__args__) == 1:
                    for p, sv in enumerate(v):
                        _validate_types(sv, t.__args__[0], f_name, paths, p)
                else:
                    raise RuntimeError('Unsupported generic type', t)
            else:
                raise AppDataFieldValueTypeError(paths, f_name, None, ot, type(v))
        else:
            raise RuntimeError('Unsupported generic type', t)


def create_app_entry(namespaces: Iterable[Mapping], paths: Sequence[ConfigPath]) -> AppEntry:
    lazy_dicts = []
    ld = None
    for d in namespaces:
        ld = _LazyExpandedDict(d, ld)
        lazy_dicts.append(ld)
    if len(lazy_dicts) > 1:
        lazy_dicts[0].refined = lazy_dicts[-1]
        lazy_dicts.reverse()
    data = {}
    for field in fields(AppEntry):
        value = None
        try:
            for d in lazy_dicts:
                value = d.get(field.name)
                if value is not None:
                    break
        except _CircularReferenceError:
            raise AppDataCircularReferenceError(paths, field.name, None)
        if value is not None:
            try:
                _validate_types(value, eval(field.type), field.name, paths, None)
            except NameError:
                raise RuntimeError(f'Unknown type {field.type}, probably lacking import')
            data[field.name] = value
        else:
            if field.default is MISSING and field.default_factory is MISSING:
                raise AppDataMissingFieldError(paths, field.name, None)
    return AppEntry(**data)


class _Indexer:

    def __init__(self, start=0):
        self._c = start

    @property
    def current(self) -> int:
        return self._c

    def inc(self) -> None:
        self._c += 1


def _process_config_data(parent_index: Optional[int], path: ConfigPath, branch_fork_set: FrozenSet[str],
                         branch_attrs: FrozenSet[str], config_data: Any, c: _Indexer) -> Iterator[Optional[int],
                                                                                                  int, ConfigPath, Set,
                                                                                                  bool, Mapping]:
    if isinstance(config_data, list):
        for n, config_item in enumerate(config_data):
            current_path = path.index(n)
            if isinstance(config_item, MutableMapping):
                current_branch_attrs = set()
                for key in config_item:
                    if key in branch_attrs:
                        raise ConfigExcessiveAttributeError(current_path.attribute(key))
                    if key in branch_fork_set:
                        raise ConfigExcessiveAttributeError(current_path.attribute(key))
                    if key in _fork_eliminations:
                        if _fork_eliminations[key] in config_item:
                            raise ConfigExcessiveAttributeError(current_path.attribute(_fork_eliminations[key]))
                        current_branch_attrs |= {key}
                current_branch_attrs = branch_attrs | current_branch_attrs
                if _group_by > current_branch_attrs:
                    raise ConfigRequiredAttributesNotFoundError(current_path, _group_by - current_branch_attrs)
                next_branches = []
                for key in config_item:
                    if key in _fork_set:
                        next_branches.append((key, config_item[key]))
                for key, _ in next_branches:
                    config_item.pop(key)
                current_index = c.current
                c.inc()
                yield parent_index, current_index, current_path, current_branch_attrs, not next_branches, config_item
                for key, next_branch in next_branches:
                    next_path = current_path.attribute(key)
                    next_branch_fork_set = branch_fork_set | frozenset([key])
                    yield from _process_config_data(current_index, next_path, next_branch_fork_set,
                                                    current_branch_attrs, next_branch, c)
            else:
                raise ConfigElementTypeError(current_path, dict, type(config_item))
    else:
        raise ConfigElementTypeError(path, list, type(config_data))


def _combine_for_total(branch: FrozenSet[FrozenSet[str]], flat_branch: FrozenSet[str], total: FrozenSet[str],
                       group: FrozenSet[str], remaining_parts: Sequence[FrozenSet[str]]) -> \
        Iterator[FrozenSet[FrozenSet[str]]]:
    if flat_branch == total:
        yield branch
    else:
        feasible_remaining = []
        for re in remaining_parts:
            if not flat_branch.isdisjoint(re) and flat_branch & re > group:
                continue
            feasible_remaining.append(re)
        for n, re in enumerate(feasible_remaining):
            nb = branch | frozenset((re,))
            nfb = flat_branch | re
            yield from _combine_for_total(nb, nfb, total, group, feasible_remaining[n + 1:])


def _enumerate_leaf_index_combinations(combination: MutableSet[FrozenSet[str]],
                                       part_map: Mapping[FrozenSet[str], Set[int]]) -> Iterator[Set[int]]:
    if not combination:
        yield set()
    else:
        parts_key = combination.pop()
        part_ids = part_map[parts_key]
        for part_id in part_ids:
            for next_part_ids in _enumerate_leaf_index_combinations(set(combination), part_map):
                next_part_ids.add(part_id)
                yield next_part_ids


def _walk_branch(index: int, included_indices: Set[int],
                 merged: List[Tuple[Mapping, ConfigPath, Tuple[int, int]]],
                 tree_list: List[Tuple[int, Tuple[Mapping, ConfigPath, Tuple[int, int]]]]) -> None:
    if index in included_indices or index is None:
        return
    else:
        prev_index, data = tree_list[index]
        merged.append(data)
        included_indices.add(index)
        _walk_branch(prev_index, included_indices, merged, tree_list)


def _merge_config_branches(leaf_indices: Set[int],
                           tree_list: List[Tuple[int, Tuple[Mapping, ConfigPath, Tuple[int, int]]]]) -> \
        Tuple[List[Mapping], List[ConfigPath], int]:
    merged = []
    included = set()
    for leaf_index in leaf_indices:
        _walk_branch(leaf_index, included, merged, tree_list)
    merged.sort(key=lambda e: e[2])
    namespaces = []
    paths = []
    for ns, pth, _ in merged:
        namespaces.append(ns)
        paths.append(pth)
    return namespaces, paths, merged[-1][2][1]


def get_app_config_from(config_data) -> AppData:
    config_tree_list = []
    leaf_indices = defaultdict(lambda: defaultdict(set))
    all_branch_attributes = defaultdict(set)
    group_key = None
    for parent_index, current_index, path, branch_attributes, is_leaf, data in \
            _process_config_data(None, ConfigPath('$'), frozenset(), frozenset(), config_data, _Indexer()):
        config_tree_list.append((parent_index, (data, path, (len(path), current_index))))
        if parent_index is None:
            group_key = path
        if is_leaf:
            leaf_indices[group_key][frozenset(branch_attributes)].add(current_index)
            all_branch_attributes[group_key].update(branch_attributes)
    app_entries = []
    app_entry_paths = {}
    for group_key in leaf_indices:
        branch_attributes = frozenset(all_branch_attributes[group_key])
        leaf_indices_by_branch_attribute_sets = leaf_indices[group_key]
        branch_attribute_sets = frozenset(leaf_indices_by_branch_attribute_sets.keys())
        branch_attribute_set_combinations = set(_combine_for_total(frozenset(), frozenset(), branch_attributes,
                                                                   _group_by, list(branch_attribute_sets)))
        not_used_attribute_sets = branch_attribute_sets - {ba_set for ba_set_c in branch_attribute_set_combinations
                                                           for ba_set in ba_set_c}
        if not_used_attribute_sets:
            paths = []
            for attr_set in not_used_attribute_sets:
                for leaf_index in leaf_indices_by_branch_attribute_sets[attr_set]:
                    paths.append(config_tree_list[leaf_index][1][1])
                raise ConfigIncompleteBranchesError(paths, branch_attributes - attr_set)
        for branch_attribute_sets_combination in branch_attribute_set_combinations:
            for leaf_index_combination in \
                    _enumerate_leaf_index_combinations(set(branch_attribute_sets_combination),
                                                       leaf_indices_by_branch_attribute_sets):
                namespaces, paths, sort_key = _merge_config_branches(leaf_index_combination, config_tree_list)
                app_entry = create_app_entry(namespaces, paths)
                entry_key = app_entry.ref
                if entry_key not in app_entry_paths:
                    app_entries.append((app_entry, sort_key))
                    app_entry_paths[entry_key] = paths
                else:
                    raise ConfigDuplicatedEntryIdentityError(app_entry_paths[entry_key], paths, asdict(entry_key))
    app_entries.sort(key=lambda ae: ae[1])
    return AppData([ae[0] for ae in app_entries])


class ConfigProcessor:

    def __init__(self, app_data_reader: AppDataReader):
        self.reader = app_data_reader

    def process_config(self, file_path: str) -> AppData:
        data = self.reader.read(file_path)
        return get_app_config_from(data)
