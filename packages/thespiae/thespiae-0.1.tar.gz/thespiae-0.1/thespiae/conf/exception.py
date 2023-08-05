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

from dataclasses import dataclass, field
from gettext import translation
from typing import TYPE_CHECKING

from thespiae.exception import ThespiaeError, generate___str__

if TYPE_CHECKING:
    from typing import Sequence, Collection, Mapping, Any

    from .data import AppEntry, ConfigPath

t = translation('thespiae', fallback=True)
_ = t.gettext


@generate___str__
@dataclass(frozen=True)
class AppEntryMixin:
    app_entry: AppEntry = field(metadata={'format': _('configuration entry for: {0.ref}')})


@generate___str__
@dataclass(frozen=True)
class _ConfigPathsMixin:
    config_paths: Sequence[ConfigPath] = field(metadata={'format': _('corresponding paths: {}')})


@generate___str__
@dataclass(frozen=True)
class _ConfigPathMixin:
    config_path: Sequence[ConfigPath] = field(metadata={'format': _('corresponding path: {}')})


@generate___str__
@dataclass(frozen=True)
class _ExpectedValueTypeMixin:
    expected: type = field(metadata={'format': _('expected value type: {0.__name__}')})
    received: type = field(metadata={'format': _('received value type: {0.__name__}')})


@generate___str__
@dataclass(frozen=True)
class _FieldMixin:
    field_name: str = field(metadata={'format': _('config field name: {}')})
    field_index: str = field(metadata={'format': _('collection index: {}')})


@generate___str__(_('Required field is missing'))
@dataclass(frozen=True)
class AppDataMissingFieldError(_FieldMixin, _ConfigPathsMixin, ThespiaeError):
    pass


@generate___str__(_('Unexpected config value'))
@dataclass(frozen=True)
class AppDataFieldValueTypeError(_ExpectedValueTypeMixin, _FieldMixin, _ConfigPathsMixin, ThespiaeError):
    pass


@generate___str__(_('Circular field reference'))
@dataclass(frozen=True)
class AppDataCircularReferenceError(_FieldMixin, _ConfigPathsMixin, ThespiaeError):
    pass


@generate___str__(_('Invalid configuration field value'))
@dataclass(frozen=True)
class ConfigElementTypeError(_ExpectedValueTypeMixin, _ConfigPathMixin, ThespiaeError):
    pass


@generate___str__(_('Excessive configuration attribute found'))
@dataclass(frozen=True)
class ConfigExcessiveAttributeError(_ConfigPathMixin, ThespiaeError):
    pass


@generate___str__(_('Required config attributes not found'))
@dataclass(frozen=True)
class ConfigRequiredAttributesNotFoundError(_ConfigPathMixin, ThespiaeError):
    attributes: Collection[str] = field(metadata={'format': _('missing field names: {}')})


@generate___str__(_('Another configuration entry with the same identity has been found'))
@dataclass(frozen=True)
class ConfigDuplicatedEntryIdentityError(_ConfigPathsMixin, ThespiaeError):
    another_paths: Sequence[ConfigPath] = field(metadata={'format': _('another paths: {}')})
    identity_values: Mapping[str, Any] = field(metadata={'format': _('identity field values: {}')})


@generate___str__(_('Unable to complete config branches with required identity attributes'))
@dataclass(frozen=True)
class ConfigIncompleteBranchesError(_ConfigPathsMixin, ThespiaeError):
    attributes: Collection[str] = field(metadata={'format': _('missing field names: {}')})


class _CircularReferenceError(ThespiaeError):
    pass
