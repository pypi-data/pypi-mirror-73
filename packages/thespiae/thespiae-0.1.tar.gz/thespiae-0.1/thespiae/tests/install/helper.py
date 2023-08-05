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

from asyncio import new_event_loop, set_event_loop, run_coroutine_threadsafe, all_tasks, gather
from functools import partial
from io import SEEK_END
from pathlib import Path
from shutil import make_archive
from threading import Thread, Event
from typing import TYPE_CHECKING
from urllib.parse import urlunsplit

from aiohttp.test_utils import unused_port
from aiohttp.web import Application, AppRunner, TCPSite, middleware, StreamResponse, Response, \
    HTTPRequestRangeNotSatisfiable

from .singleton import install_manager, download_manager

if TYPE_CHECKING:
    from typing import List, Set
    from unittest import TestCase

    from thespiae.install.data import DownloadSpec
    from thespiae.install.protocol import Feedback


class InstallManagerMockResetMixin:

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        install_manager.reset_mock(return_value=True, side_effect=True)
        install_manager.is_file_present.reset_mock(return_value=True, side_effect=True)
        install_manager.is_product_code_present.reset_mock(return_value=True, side_effect=True)
        install_manager.run_command.reset_mock(return_value=True, side_effect=True)
        install_manager.copy_file.reset_mock(return_value=True, side_effect=True)
        install_manager.remove_file.reset_mock(return_value=True, side_effect=True)
        install_manager.unpack_archive.reset_mock(return_value=True, side_effect=True)
        install_manager.remove_directory.reset_mock(return_value=True, side_effect=True)


class DownloadManagerMockResetMixin:

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        download_manager.reset_mock(return_value=True, side_effect=True)
        download_manager.filter_present.reset_mock(return_value=True, side_effect=True)


def set_install_manager_data(is_file_present: bool = None, is_product_code_present: bool = None,
                             run_command: str = None):
    install_manager.is_file_present.return_value = is_file_present
    install_manager.is_product_code_present.return_value = is_product_code_present
    install_manager.run_command.return_value = run_command


def set_download_manager_data(present_paths: Set[str]):
    download_manager.filter_present.side_effect = lambda l: [i for i in l if i.download_path not in present_paths]


class ExtraAssertMixin:

    def assert_called_exactly_with_no_order(self: TestCase, mock, *calls):
        self.assertEqual(mock.call_count, len(calls))
        mock.assert_has_calls(calls, any_order=True)


def assert_download_progress_for(mock: Feedback, expected: Set[DownloadSpec]):
    encountered = set()
    for ci in mock.report_entry_download_progress.call_args_list:
        ((sp, _), _) = ci
        encountered.add(sp)
    if expected != encountered:
        raise AssertionError('No progress for {}'.format(expected))


def _get_test_middleware(log: List):
    @middleware
    async def test_middleware(request, handler):
        log.append((request.raw_path, request.headers.get('Range')))
        return await handler(request)

    return test_middleware


class _TestWebServerCore:

    def __init__(self, host: str, port: int, calls: List, runner: AppRunner, site: TCPSite):
        self.host = host
        self.port = port
        self.calls = calls
        self.runner = runner
        self.site = site

    async def stop(self) -> None:
        await self.runner.cleanup()


_dir_path = Path(__file__).parent / 'test_files'
_chunk = 16


def create_archive(archive_path: Path, archive_format: str):
    return make_archive(archive_path, archive_format, _dir_path)


async def _handle_test4(request):
    resp = StreamResponse()
    with open(_dir_path / 'test4.txt', 'rb') as fo:
        fo.seek(0, SEEK_END)
        resp.content_length = fo.tell()
        fo.seek(0)
        await resp.prepare(request)
        for data in iter(partial(fo.read, _chunk), b''):
            await resp.write(data)
    await resp.write_eof()
    return resp


async def _handle_test5(_):
    return Response(status=HTTPRequestRangeNotSatisfiable.status_code)


async def _handle_test6(_):
    resp = Response(status=HTTPRequestRangeNotSatisfiable.status_code)
    resp.headers['Content-Range'] = 'meters 1-2/3'
    return resp


async def _create_test_web_server_core() -> _TestWebServerCore:
    calls = []
    app = Application(middlewares=[_get_test_middleware(calls)])
    app.router.add_static('/static/', _dir_path)
    app.router.add_get('/dynamic/test4.txt', _handle_test4)
    app.router.add_get('/dynamic/test5.txt', _handle_test5)
    app.router.add_get('/dynamic/test6.txt', _handle_test6)
    runner = AppRunner(app)
    await runner.setup()
    host = 'localhost'
    port = unused_port()
    site = TCPSite(runner, host, port)
    await site.start()
    return _TestWebServerCore(host, port, calls, runner, site)


class TestWebServer:

    def __init__(self):
        self.loop = None
        self.core = None

        def helper():
            loop = new_event_loop()
            set_event_loop(loop)
            self.loop = loop
            self.core = loop.run_until_complete(_create_test_web_server_core())
            self.started.set()
            self.loop.run_forever()
            tasks = all_tasks(self.loop)
            loop.run_until_complete(gather(*tasks, return_exceptions=True))
            loop.run_until_complete(loop.shutdown_asyncgens())
            self.loop.close()
            set_event_loop(None)

        self.started = Event()
        self.thread = Thread(target=helper)

    def start(self):
        self.thread.start()
        self.started.wait()

    def stop(self):
        async def helper():
            await self.core.stop()
            self.loop.stop()

        run_coroutine_threadsafe(helper(), self.loop)
        self.thread.join()

    def create_url_for(self, file_name: str) -> str:
        return urlunsplit(('http', f'{self.core.host}:{self.core.port}', file_name, '', ''))

    def reset_request_data(self):
        self.core.calls.clear()

    def get_request_data(self):
        return list(self.core.calls)


def copy_to(test_file: str, dst: str, n_bytes: int = None):
    with open(Path(__file__).parent / 'test_files' / test_file, 'rb') as sfo:
        with open(dst, 'wb') as dfo:
            if n_bytes:
                full_reads = n_bytes // _chunk
                partial_read = n_bytes % _chunk
                for _ in range(full_reads):
                    data = sfo.read(_chunk)
                    if data:
                        dfo.write(data)
                    else:
                        break
                else:
                    data = sfo.read(partial_read)
                    dfo.write(data)
            else:
                for data in iter(partial(sfo.read, _chunk), b''):
                    dfo.write(data)
