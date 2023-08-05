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

from thespiae.conf.exception import AppEntryMixin
from thespiae.exception import ThespiaeError, generate___str__

t = translation('thespiae', fallback=True)
_ = t.gettext


class PathEntryError(ThespiaeError):
    pass


class PathError(ThespiaeError):
    pass


class InconsistentUserPathEntryDataError(ThespiaeError):
    pass


class InconsistentActualPathEntryDataError(ThespiaeError):
    pass


@generate___str__(_('Invalid value of system PATH'))
@dataclass(frozen=True)
class InvalidSystemPathError(ThespiaeError):
    pass


@generate___str__(_('Invalid value of user PATH'))
@dataclass(frozen=True)
class InvalidUserPathError(ThespiaeError):
    pass


@generate___str__
@dataclass(frozen=True)
class _InconsistentDataExtensionMixin:
    data: str = field(metadata={'format': _('raw string {}')})
    extended_data: str = field(metadata={'format': _('extended string {}')})


@generate___str__(_('Number of user path entries is not preserved with regard to extension'))
@dataclass(frozen=True)
class InconsistentUserPathExtensionError(_InconsistentDataExtensionMixin, ThespiaeError):
    pass


@generate___str__(_('Invalid path entry'))
@dataclass(frozen=True)
class InvalidPathEntryError(AppEntryMixin, ThespiaeError):
    entry: str = field(metadata={'format': _('path element string {}')})


@generate___str__(_('Path element is not consistent with regard to extension'))
@dataclass(frozen=True)
class InconsistentPathEntryExtensionError(_InconsistentDataExtensionMixin, AppEntryMixin, ThespiaeError):
    pass
