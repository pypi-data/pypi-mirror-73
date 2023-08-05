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

from abc import ABC, abstractmethod
from dataclasses import asdict
from os.path import splitext
from pathlib import Path
from shutil import get_unpack_formats
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from .data import DownloadSpec
from .exception import InvalidOrMissingAppDataError, UnknownInstallTypeError, UnknownUninstallTypeError, \
    InterruptedFileOperationsError

if TYPE_CHECKING:
    from typing import Optional, Iterable, Tuple

    from thespiae.conf.data import AppData, AppEntry
    from .protocol import Feedback
    from .system import InstallManager, DownloadManager


def _create_download_spec(url: str, directory: str, app_entry: AppEntry, ext: str = None) -> DownloadSpec:
    name = app_entry.name
    if not name:
        raise InvalidOrMissingAppDataError(app_entry, 'name', name)
    parsed = urlparse(url)
    d_dir = Path(directory) / name
    d_name = name
    version = app_entry.version
    if version:
        d_dir /= version
        d_name += f'_{version}'
    architecture = app_entry.architecture
    if architecture:
        d_dir /= architecture
        d_name += f'_{architecture}'
    if not ext:
        _, ext = splitext(parsed.path)
    d_name += ext
    d_path = (d_dir / d_name).absolute()
    return DownloadSpec(**asdict(app_entry), url=url, hash=app_entry.file_hash, download_path=str(d_path),
                        part_path=str(d_path) + '.part')


class InstallTypeHandler(ABC):

    def __init__(self, install_manager: InstallManager):
        self._instm = install_manager

    @abstractmethod
    def create_download_spec(self, app_entry: AppEntry, download_dir_path: str) -> Optional[DownloadSpec]:
        pass

    @abstractmethod
    def is_applicable(self, app_entry: AppEntry) -> bool:
        pass

    @abstractmethod
    def install(self, app_entry: AppEntry, ds: DownloadSpec) -> None:
        pass


class UninstallTypeHandler(ABC):

    def __init__(self, install_manager: InstallManager):
        self._instm = install_manager

    @abstractmethod
    def is_applicable(self, app_entry: AppEntry) -> bool:
        pass

    @abstractmethod
    def is_installed(self, app_entry: AppEntry) -> bool:
        pass

    @abstractmethod
    def uninstall(self, app_entry: AppEntry) -> None:
        pass


class ExeInstallHandler(InstallTypeHandler):

    def create_download_spec(self, app_entry: AppEntry, download_dir_path: str) -> Optional[DownloadSpec]:
        return _create_download_spec(app_entry.installer_url, download_dir_path, app_entry)

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.installer_url)

    def install(self, app_entry: AppEntry, ds: DownloadSpec) -> None:
        self._instm.run_file(ds.download_path, app_entry.install_args)


class ExeUninstallHandler(UninstallTypeHandler):

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.uninstaller_path)

    def is_installed(self, app_entry: AppEntry) -> bool:
        return self._instm.is_file_present(app_entry.uninstaller_path)

    def uninstall(self, app_entry: AppEntry) -> None:
        self._instm.run_file(app_entry.uninstaller_path, app_entry.uninstall_args)


class MSIInstallHandler(InstallTypeHandler):

    def create_download_spec(self, app_entry: AppEntry, download_dir_path: str) -> Optional[DownloadSpec]:
        return _create_download_spec(app_entry.package_url, download_dir_path, app_entry)

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.package_url)

    def install(self, app_entry: AppEntry, ds: DownloadSpec) -> None:
        self._instm.install_msi(ds.download_path, app_entry.install_args)


class MSIUninstallHandler(UninstallTypeHandler):

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.product_code)

    def is_installed(self, app_entry: AppEntry) -> bool:
        return self._instm.is_product_code_present(app_entry.product_code)

    def uninstall(self, app_entry: AppEntry) -> None:
        self._instm.uninstall_msi(app_entry.product_code, app_entry.uninstall_args)


class CommandInstallHandler(InstallTypeHandler):

    def create_download_spec(self, app_entry: AppEntry, download_dir_path: str) -> Optional[DownloadSpec]:
        return None

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.command)

    def install(self, app_entry: AppEntry, ds: DownloadSpec) -> None:
        self._instm.run_command(app_entry.command, app_entry.install_args)


class CommandUninstallHandler(UninstallTypeHandler):

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.command and app_entry.list_args and app_entry.installed_list_entry)

    def is_installed(self, app_entry: AppEntry) -> bool:
        # TODO: may be affected by cmd encoding issues, might need improvements <AP>
        installed_list = self._instm.run_command(app_entry.command, app_entry.list_args)
        return app_entry.installed_list_entry in installed_list

    def uninstall(self, app_entry: AppEntry) -> None:
        self._instm.run_command(app_entry.command, app_entry.uninstall_args)


def _get_path(app_entry: AppEntry, attribute: str) -> Path:
    path = getattr(app_entry, attribute)
    if path:
        return Path(path).absolute()
    else:
        raise InvalidOrMissingAppDataError(app_entry, attribute, path)


class _FileOperations:

    def __init__(self, app_entry: AppEntry, path: Path):
        self.app_entry = app_entry
        self.path = path

    def __enter__(self) -> Path:
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise InterruptedFileOperationsError(self.app_entry, str(self.path)) from exc_val


class FileInstallHandler(InstallTypeHandler):

    def create_download_spec(self, app_entry: AppEntry, download_dir_path: str) -> Optional[DownloadSpec]:
        return _create_download_spec(app_entry.file_url, download_dir_path, app_entry)

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.file_url) and bool(app_entry.file_name) and bool(app_entry.file_directory)

    def install(self, app_entry: AppEntry, ds: DownloadSpec) -> None:
        with _FileOperations(app_entry, _get_path(app_entry, 'file_directory')) as path:
            self._instm.copy_file(ds.download_path, path, app_entry.file_name)


class FileUninstallHandler(UninstallTypeHandler):

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.file_directory) and bool(app_entry.file_name)

    def is_installed(self, app_entry: AppEntry) -> bool:
        return self._instm.is_file_present(str(_get_path(app_entry, 'file_directory') / app_entry.file_name))

    def uninstall(self, app_entry: AppEntry) -> None:
        with _FileOperations(app_entry, _get_path(app_entry, 'file_directory')) as path:
            self._instm.remove_file(path, app_entry.file_name)


_format_extension = {f_name: f_ext[0] for f_name, f_ext, _ in get_unpack_formats()}


class ArchiveInstallHandler(InstallTypeHandler):

    def create_download_spec(self, app_entry: AppEntry, download_dir_path: str) -> Optional[DownloadSpec]:
        return _create_download_spec(app_entry.archive_url, download_dir_path, app_entry,
                                     _format_extension[app_entry.archive_format])

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.archive_url and app_entry.archive_format and app_entry.unpack_directory)

    def install(self, app_entry: AppEntry, ds: DownloadSpec) -> None:
        with _FileOperations(app_entry, _get_path(app_entry, 'unpack_directory')) as path:
            self._instm.unpack_archive(ds.download_path, app_entry.archive_format, path)


class ArchiveUninstallHandler(UninstallTypeHandler):

    def is_applicable(self, app_entry: AppEntry) -> bool:
        return bool(app_entry.unpack_directory)

    def is_installed(self, app_entry: AppEntry) -> bool:
        return self._instm.is_file_present(str(_get_path(app_entry, 'unpack_directory')))

    def uninstall(self, app_entry: AppEntry) -> None:
        with _FileOperations(app_entry, _get_path(app_entry, 'unpack_directory')) as path:
            self._instm.remove_directory(path)


class SoftwareProcessor:

    def __init__(self, download_manager: DownloadManager, install_type_handlers: Iterable[InstallTypeHandler],
                 uninstall_type_handlers: Iterable[UninstallTypeHandler]):
        self._dm = download_manager
        self._hs = install_type_handlers
        self._uhs = uninstall_type_handlers

    def _get_handlers(self, app_entry: AppEntry) -> Tuple[InstallTypeHandler, UninstallTypeHandler]:
        for h in self._hs:
            if h.is_applicable(app_entry):
                ih = h
                break
        else:
            raise UnknownInstallTypeError(app_entry)
        for h in self._uhs:
            if h.is_applicable(app_entry):
                uh = h
                break
        else:
            raise UnknownUninstallTypeError(app_entry)
        return ih, uh

    def process(self, download_dir_path: str, config: AppData, fb: Feedback) -> None:
        to_install = []
        to_install_entries = []
        to_uninstall = []
        to_uninstall_entries = []
        specs = []
        fb.report_checking_software()
        for entry in config.to_install:
            install_handler, uninstall_handler = self._get_handlers(entry)
            if not uninstall_handler.is_installed(entry):
                ds = install_handler.create_download_spec(entry, download_dir_path)
                if ds:
                    specs.append(ds)
                to_install.append((entry, install_handler, ds))
                to_install_entries.append(entry)
        for entry in config.to_uninstall:
            install_handler, uninstall_handler = self._get_handlers(entry)
            if uninstall_handler.is_installed(entry):
                to_uninstall.append((entry, uninstall_handler))
                to_uninstall_entries.append(entry)
        specs = self._dm.filter_present(specs)
        if specs or to_install_entries or to_uninstall_entries:
            fb.confirm_operations(specs, to_uninstall_entries, to_install_entries)
            if specs:
                self._dm.download(specs, fb)
            if to_uninstall:
                fb.report_removal_started()
                for entry, handler in to_uninstall:
                    fb.report_entry_removal_started(entry)
                    handler.uninstall(entry)
                    fb.report_entry_removal_finished(entry)
                fb.report_removal_finished()
            if to_install:
                fb.report_installation_started()
                for entry, handler, ds in to_install:
                    fb.report_entry_installation_started(entry)
                    handler.install(entry, ds)
                    fb.report_entry_installation_finished(entry)
                fb.report_installation_finished()
        else:
            fb.report_software_set_no_changes()
