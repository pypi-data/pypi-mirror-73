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

from dataclasses import dataclass
from typing import TYPE_CHECKING

from thespiae.conf import AppEntry

if TYPE_CHECKING:
    from typing import Optional


@dataclass(frozen=True)
class DownloadSpec(AppEntry):
    url: str = None
    hash: str = None
    download_path: str = None
    part_path: str = None


@dataclass(frozen=True)
class ContentRangeData:
    start: Optional[int]
    end: Optional[int]
    total: Optional[int]
