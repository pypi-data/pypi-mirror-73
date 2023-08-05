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

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Sequence

    from thespiae.conf import AppEntry
    from .data import DownloadSpec


class Feedback(Protocol):

    @abstractmethod
    def report_checking_software(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def confirm_operations(self, to_download: Sequence[DownloadSpec], to_uninstall: Sequence[AppEntry],
                           to_install: Sequence[AppEntry]) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_software_set_no_changes(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_download_started(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_download_initiated(self, spec: DownloadSpec) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_download_started(self, spec: DownloadSpec, current_size: int, total_size: int = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_download_progress(self, spec: DownloadSpec, batch_size: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_download_finished(self, spec: DownloadSpec) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_download_finished(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_removal_started(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_removal_started(self, entry: AppEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_removal_finished(self, entry: AppEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_removal_finished(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_installation_started(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_installation_started(self, entry: AppEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_entry_installation_finished(self, entry: AppEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    def report_installation_finished(self) -> None:
        raise NotImplementedError
