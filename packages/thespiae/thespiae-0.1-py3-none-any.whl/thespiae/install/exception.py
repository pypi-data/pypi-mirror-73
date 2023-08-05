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

from thespiae.conf.exception import AppEntryMixin
from thespiae.exception import ThespiaeError, generate___str__

if TYPE_CHECKING:
    from multidict import CIMultiDictProxy

    from .data import DownloadSpec

t = translation('thespiae', fallback=True)
_ = t.gettext


@generate___str__
@dataclass(frozen=True)
class _DownloadSpecMixin:
    download_spec: DownloadSpec = field(metadata={'format': _('entry for: {0.ref}')})


@generate___str__(_('Invalid or missing configuration data'))
@dataclass(frozen=True)
class InvalidOrMissingAppDataError(AppEntryMixin, ThespiaeError):
    key: str = field(metadata={'format': _('configuration key: {}')})
    value: object = field(metadata={'format': _('current key value: {}')})


@generate___str__(_('Unrecognized application installation type'))
@dataclass(frozen=True)
class UnknownInstallTypeError(AppEntryMixin, ThespiaeError):
    pass


@generate___str__(_('Unrecognized application removal type'))
@dataclass(frozen=True)
class UnknownUninstallTypeError(AppEntryMixin, ThespiaeError):
    pass


@generate___str__(_('Download error'))
@dataclass(frozen=True)
class DownloadError(_DownloadSpecMixin, ThespiaeError):
    pass


@generate___str__(_('File hash does not match the specified one'))
@dataclass(frozen=True)
class HashError(_DownloadSpecMixin, ThespiaeError):
    actual_hash: str = field(metadata={'format': _('actual hash: {}')})


@generate___str__(_('Remote server returned unsupported response'))
@dataclass(frozen=True)
class UnsupportedResponseError(_DownloadSpecMixin, ThespiaeError):
    status: int = field(metadata={'format': _('response status {}')})
    headers: CIMultiDictProxy = field(metadata={'format': _('response headers {}')})


@generate___str__(_('Filesystem operations have been interrupted, please resolve remaining inconsistencies manually \
                     before running the application again'))
@dataclass(frozen=True)
class InterruptedFileOperationsError(AppEntryMixin, ThespiaeError):
    root_directory: str = field(metadata={'format': _('directory: {}')})
