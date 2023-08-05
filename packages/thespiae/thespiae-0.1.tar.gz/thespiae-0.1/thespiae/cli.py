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

import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from gettext import translation
from os import linesep
from typing import TYPE_CHECKING

from tqdm import tqdm

from .exception import ThespiaeError
from .install.protocol import Feedback as InstallFeedback
from .path.protocol import Feedback as PathFeedback

if TYPE_CHECKING:
    from typing import Sequence, MutableMapping
    from .conf import AppEntry, AppEntryRef
    from .install import DownloadSpec

t = translation('thespiae', fallback=True)
_ = t.gettext


def _info(o) -> None:
    print(o, file=sys.stdout)


def _error(o) -> None:
    print(o, file=sys.stderr)


def _confirm(prompt: str) -> None:
    # TODO: implement through tty <AP>
    resp = input(prompt + ' [y/N]:')
    if 'y' != resp:
        raise _NotConfirmedError


def _position_after_bars(bar_count: int) -> None:
    if bar_count > 0:
        sys.stdout.write('\r')
        sys.stdout.write('\x1b[{}B'.format(bar_count - 1))
        sys.stdout.flush()


class _NotConfirmedError(Exception):
    pass


class CLIFeedback(InstallFeedback, PathFeedback):

    def report_checking_software(self):
        _info(_('Checking software'))

    def __init__(self):
        self._download_name_max_len = 0
        self._download_bars: MutableMapping[AppEntryRef, tqdm] = {}
        self._uninstall_count_total = 0
        self._install_count_total = 0
        self._uninstall_count = 0
        self._install_count = 0

    def confirm_operations(self, to_download: Sequence[DownloadSpec], to_uninstall: Sequence[AppEntry],
                           to_install: Sequence[AppEntry]):
        # TODO: multi-line indent <AP>
        if to_download:
            self._download_bars = {}
            self._download_name_max_len = max((len(str(spec.ref)) for spec in to_download))
            _info(_('Download distribution for'))
            _info('\t' + ' '.join(str(e.ref) for e in to_download))
        if to_uninstall:
            self._uninstall_count_total = len(to_uninstall)
            self._uninstall_count = 0
            _info(_('To uninstall'))
            _info('\t' + ' '.join(str(e.ref) for e in to_uninstall))
        if to_install:
            self._install_count_total = len(to_install)
            self._install_count = 0
            _info(_('To install'))
            _info('\t' + ' '.join(str(e.ref) for e in to_install))
        _confirm(_('Continue?'))

    def report_software_set_no_changes(self):
        _info(_('Installed software matches requirements, no changes needed'))

    def report_download_started(self):
        _info(_('Downloading'))

    def report_entry_download_initiated(self, spec: DownloadSpec):
        self._download_bars[spec.ref] = tqdm(desc=str(spec.ref).rjust(self._download_name_max_len), unit='B',
                                             unit_scale=True, miniters=1000 * 1000, ascii=True)

    def report_entry_download_started(self, spec: DownloadSpec, current_size: int, total_size: int = None):
        bar = self._download_bars[spec.ref]
        if total_size:
            bar.total = total_size
        bar.n = current_size
        bar.refresh()

    def report_entry_download_progress(self, spec: DownloadSpec, batch_size: int):
        bar = self._download_bars[spec.ref]
        bar.update(batch_size)

    def report_entry_download_finished(self, spec: DownloadSpec):
        pass

    def report_download_finished(self):
        self._finalize_download()

    def report_removal_started(self):
        _info(_('Uninstalling software'))

    def report_entry_removal_started(self, entry: AppEntry):
        self._uninstall_count += 1
        _info(_('[{0}/{1}] uninstalling {2}').format(self._uninstall_count, self._uninstall_count_total, entry.ref))

    def report_entry_removal_finished(self, entry: AppEntry):
        _info(_('{} uninstalled').format(entry.ref))

    def report_removal_finished(self):
        pass

    def report_installation_started(self):
        _info(_('Installing software'))

    def report_entry_installation_started(self, entry: AppEntry):
        self._install_count += 1
        _info(_('[{0}/{1}] installing {2}').format(self._install_count, self._install_count_total, entry.ref))

    def report_entry_installation_finished(self, entry: AppEntry):
        _info(_('{} installed').format(entry.ref))

    def report_installation_finished(self):
        pass

    def report_path_analysis(self):
        _info(_('Checking user PATH'))

    def confirm_user_path_update(self, before: str, after):
        # TODO: multi-line indent <AP>
        _info(_('Current user PATH'))
        _info('\t' + before)
        _info(_('Updated user PATH'))
        _info('\t' + after)
        _confirm(_('Continue?'))

    def report_user_path_no_changes(self):
        _info(_('No changes to user PATH are needed'))

    def report_user_path_updated(self):
        _info(_('User PATH updated'))

    def finalize(self):
        self._finalize_download()

    def _finalize_download(self):
        bars = list(self._download_bars.values())
        for bar in bars:
            bar.refresh()
        for bar in reversed(bars):
            bar.close()
        _position_after_bars(len(bars))


@dataclass(frozen=True)
class CLIParams:
    config_file: str
    data_dir: str


class CLI:

    def __init__(self, app_name: str):
        parser = ArgumentParser(app_name)
        parser.add_argument('config_file', metavar=_('CONFIG_FILE'), help=_('YAML file to read configuration from'))
        parser.add_argument('data_dir', metavar=_('DATA_DIR'),
                            help=_('directory to download to and install software from'))
        ns = parser.parse_args()
        self._params = CLIParams(ns.config_file, ns.data_dir)
        self._feedback = CLIFeedback()

    @property
    def params(self) -> CLIParams:
        return self._params

    @property
    def feedback(self) -> CLIFeedback:
        return self._feedback

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.feedback.finalize()
            if issubclass(exc_type, ThespiaeError):
                _error(str(exc_val))
                if exc_val.__cause__:
                    _error(_('because of'))
                    _error(str(exc_val.__cause__))
                return True
            elif issubclass(exc_type, _NotConfirmedError) or issubclass(exc_type, KeyboardInterrupt):
                _error(linesep + _('Action cancelled by the user'))
                return True
