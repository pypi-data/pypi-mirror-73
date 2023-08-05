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

from asyncio import gather, create_task, get_running_loop, run as aio_run, set_event_loop_policy, \
    DefaultEventLoopPolicy, WindowsSelectorEventLoopPolicy
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from io import SEEK_END
from os import rename, makedirs, rmdir, listdir, remove, removedirs
from os.path import exists, dirname
from re import fullmatch, ASCII
from shutil import copyfile, rmtree, unpack_archive
from subprocess import run as subprocess_run, CalledProcessError
import sys
from typing import TYPE_CHECKING
from winreg import OpenKeyEx, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, KEY_WOW64_32KEY, KEY_READ, KEY_WOW64_64KEY

from aiohttp import ClientSession, ClientError
from aiohttp.web import HTTPOk, HTTPPartialContent, HTTPRequestRangeNotSatisfiable

from .data import ContentRangeData
from .exception import DownloadError, HashError, UnsupportedResponseError

if TYPE_CHECKING:
    from typing import MutableMapping, Mapping, Sequence, List, Optional, BinaryIO
    from pathlib import Path

    from aiohttp import ClientResponse

    from .data import DownloadSpec
    from .protocol import Feedback

# TODO: remove for 4.x+ version of aiohttp (https://github.com/aio-libs/aiohttp/issues/4324) <AP>
if sys.platform == 'win32':
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())


def _test_key_present_view(root: int, path: str, key: str, view: int) -> bool:
    try:
        with OpenKeyEx(root, f'{path}\\{key}', 0, KEY_READ | view):
            return True
    except OSError as e:
        if e.winerror == 2:
            return False
        else:
            raise


def _test_key_present(root: int, path: str, key: str) -> bool:
    return _test_key_present_view(root, path, key, KEY_WOW64_64KEY) or \
           _test_key_present_view(root, path, key, KEY_WOW64_32KEY)


class InstallManager:

    @staticmethod
    def is_file_present(path: str) -> bool:
        return exists(path)

    @staticmethod
    def is_product_code_present(code: str) -> bool:
        # TODO: 32-bit installer compatibility <AP>
        return _test_key_present(HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', code) or \
               _test_key_present(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', code)

    @staticmethod
    def run_file(path: str, args: List[str]) -> None:
        subprocess_run([path] + (args if args else []), check=True, shell=True)

    def install_msi(self, package_path: str, args: List[str]) -> None:
        self.run_command('msiexec', ['/I', package_path] + (args if args else []))

    def uninstall_msi(self, product_code: str, args: List[str]) -> None:
        self.run_command('msiexec', ['/x', product_code] + (args if args else []))

    @staticmethod
    def run_command(command: str, args: List[str]) -> str:
        try:
            return subprocess_run([command] + (args if args else []), shell=True, capture_output=True, text=True,
                                  check=True).stdout
        except CalledProcessError as e:
            if e.returncode != 3010:
                raise

    @staticmethod
    def copy_file(src: str, path: Path, name: str):
        makedirs(path, exist_ok=True)
        copyfile(src, path / name)

    @staticmethod
    def _remove_directories(path: Sequence[Path]):
        # TODO: investigate options to raise exception if directory is in use <AP>
        for p in reversed(path):
            p_str = str(p)
            if not listdir(p_str):
                rmdir(p_str)

    @staticmethod
    def remove_directory(path: Path):
        rmtree(path)
        removedirs(path.parent)

    @staticmethod
    def remove_file(path: Path, name: str):
        remove(path / name)
        removedirs(path)

    @staticmethod
    def unpack_archive(archive_path: str, archive_format: str, directory_path: Path):
        makedirs(directory_path, exist_ok=True)
        unpack_archive(archive_path, directory_path, archive_format)


def _prepare_download(part_path: str, fos: MutableMapping[str, BinaryIO]) -> int:
    if part_path in fos:
        raise RuntimeError(f'{part_path} is already associated with another download')
    if exists(part_path):
        fo = open(part_path, 'r+b')
        fo.seek(0, SEEK_END)
        ln = fo.tell()
    else:
        makedirs(dirname(part_path), exist_ok=True)
        fo = open(part_path, 'w+b')
        ln = 0
    fos[part_path] = fo
    return ln


def _write_data(part_path: str, data: bytes, fos: Mapping[str, BinaryIO]) -> None:
    fo = fos[part_path]
    fo.write(data)


def _truncate_file(part_path: str, fos: Mapping[str, BinaryIO]) -> None:
    fo = fos[part_path]
    fo.seek(0)
    fo.truncate(0)


def _finalize_download(part_path: str, download_path: str, fos: MutableMapping[str, BinaryIO]) -> None:
    fo = fos.pop(part_path)
    fo.close()
    rename(part_path, download_path)


def _close_fos(fos) -> None:
    for fo in fos.values():
        fo.close()


def parse_content_range(val: str) -> Optional[ContentRangeData]:
    mo = fullmatch(r'bytes (?:\*|(?P<start>\d+)-(?P<end>\d+))/(?:\*|(?P<total>\d+))', val, ASCII)
    if mo:
        start, end, total = mo.group('start', 'end', 'total')
        return ContentRangeData(int(start) if start else None, int(end) if end else None,
                                int(total) if total else None)
    else:
        return None


class DownloadManager:

    def __init__(self):
        self._ex = ThreadPoolExecutor(max_workers=1)
        self._cs = 1000 * 1000

    def _get_hash(self, path) -> str:
        h = sha256()
        cs = self._cs
        with open(path, 'rb') as fo:
            data = fo.read(cs)
            while len(data) > 0:
                h.update(data)
                data = fo.read(cs)
        return h.hexdigest()

    async def _fetch_and_write(self, resp: ClientResponse, spec: DownloadSpec, fos: MutableMapping[str, BinaryIO],
                               fb: Feedback) -> None:
        loop = get_running_loop()
        cs = self._cs
        ex = self._ex
        path = spec.part_path
        while True:
            data = await resp.content.read(cs)
            if data:
                await loop.run_in_executor(ex, _write_data, path, data, fos)
                fb.report_entry_download_progress(spec, len(data))
            else:
                await loop.run_in_executor(ex, _finalize_download, path, spec.download_path, fos)
                fb.report_entry_download_finished(spec)
                break

    async def _download_file(self, session: ClientSession, spec: DownloadSpec, fos: MutableMapping[str, BinaryIO],
                             fb: Feedback) -> None:
        loop = get_running_loop()
        fb.report_entry_download_initiated(spec)
        try:
            ln = await loop.run_in_executor(self._ex, _prepare_download, spec.part_path, fos)
            headers = {}
            if ln:
                headers['Range'] = f'bytes={ln}-'
            async with session.get(spec.url, headers=headers) as resp:
                loop = get_running_loop()
                if resp.status == HTTPOk.status_code:
                    if ln:
                        await loop.run_in_executor(self._ex, _truncate_file, spec.part_path, fos)
                        ln = 0
                    fb.report_entry_download_started(spec, ln, resp.content_length)
                    await self._fetch_and_write(resp, spec, fos, fb)
                elif resp.status == HTTPPartialContent.status_code:
                    fb.report_entry_download_started(spec, ln,
                                                     resp.content_length + ln if resp.content_length else None)
                    await self._fetch_and_write(resp, spec, fos, fb)
                elif resp.status == HTTPRequestRangeNotSatisfiable.status_code:
                    crd = resp.headers.get('Content-Range')
                    if crd:
                        parsed_crd = parse_content_range(crd)
                        if parsed_crd and parsed_crd.total == ln:
                            await loop.run_in_executor(self._ex, _finalize_download, spec.part_path,
                                                       spec.download_path, fos)
                            fb.report_entry_download_started(spec, ln, ln)
                            fb.report_entry_download_finished(spec)
                        else:
                            raise UnsupportedResponseError(spec, resp.status, resp.headers)
                    else:
                        raise UnsupportedResponseError(spec, resp.status, resp.headers)
                else:
                    raise UnsupportedResponseError(spec, resp.status, resp.headers)
        except (OSError, ClientError) as e:
            raise DownloadError(spec) from e

    async def _download(self, specs: Sequence[DownloadSpec], fb: Feedback) -> None:
        async with ClientSession() as session:
            fos = {}
            tasks = [create_task(self._download_file(session, s, fos, fb)) for s in specs]
            try:
                await gather(*tasks)
            finally:
                to_wait_for = []
                for task in tasks:
                    if not task.done():
                        task.cancel()
                        to_wait_for.append(task)
                await gather(*to_wait_for, return_exceptions=True)
                loop = get_running_loop()
                try:
                    await loop.run_in_executor(self._ex, _close_fos, fos)
                except OSError:
                    # TODO: logging <AP>
                    pass

    def _ensure_hash(self, spec: DownloadSpec) -> None:
        if spec.hash:
            actual = self._get_hash(spec.download_path)
            if actual != spec.hash:
                raise HashError(spec, actual)

    def filter_present(self, specs: Sequence[DownloadSpec]) -> List[DownloadSpec]:
        a = []
        for spec in specs:
            if exists(spec.download_path):
                self._ensure_hash(spec)
            else:
                a.append(spec)
        return a

    def download(self, specs: Sequence[DownloadSpec], fb: Feedback) -> None:
        async def _helper(std):
            download_task = create_task(self._download(std, fb))
            await download_task

        if specs:
            fb.report_download_started()
            aio_run(_helper(specs))
        for s in specs:
            self._ensure_hash(s)
        fb.report_download_finished()
