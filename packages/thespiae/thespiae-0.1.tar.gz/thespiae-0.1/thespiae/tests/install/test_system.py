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

from pathlib import Path
from subprocess import CalledProcessError
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest import TestCase
from unittest.mock import NonCallableMock, call, patch, DEFAULT
from winreg import HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, KEY_WOW64_32KEY, KEY_READ, KEY_WOW64_64KEY

import thespiae.install.system
from thespiae.install.data import DownloadSpec, ContentRangeData
from thespiae.install.exception import HashError, UnsupportedResponseError
from thespiae.install.protocol import Feedback
from thespiae.install.system import parse_content_range
from .helper import TestWebServer, copy_to, ExtraAssertMixin, assert_download_progress_for, create_archive
from .singleton import real_download_manager as download_manager, real_install_manager as install_manager


def setUpModule():
    global web_server
    web_server = TestWebServer()
    web_server.start()


def tearDownModule():
    web_server.stop()


class TestContentRangeParser(TestCase):

    def test_content_range_parsing(self):
        self.assertEqual(parse_content_range('bytes */123'), ContentRangeData(None, None, 123))

    def test_content_range_parsing2(self):
        self.assertEqual(parse_content_range('bytes */*'), ContentRangeData(None, None, None))

    def test_content_range_parsing3(self):
        self.assertEqual(parse_content_range('bytes 12-23/34'), ContentRangeData(12, 23, 34))

    def test_content_range_parsing4(self):
        self.assertIsNone(parse_content_range('bytes 12-23/'))

    def test_content_range_parsing5(self):
        self.assertIsNone(parse_content_range('/'))

    def test_content_range_parsing6(self):
        self.assertIsNone(parse_content_range(''))

    def test_content_range_parsing7(self):
        self.assertEqual(parse_content_range('bytes 12-23/*'), ContentRangeData(12, 23, None))

    def test_content_range_parsing8(self):
        self.assertIsNone(parse_content_range('bytes 12-/23'))

    def test_content_range_parsing9(self):
        self.assertIsNone(parse_content_range('bytes -12/23'))


class TestInstallManager(ExtraAssertMixin, TestCase):

    def test_file_copy_and_removal(self):
        with TemporaryDirectory() as temp_path:
            with NamedTemporaryFile(dir=temp_path, delete=False) as temp_file:
                temp_file.close()
                tp = Path(temp_path) / 'test'
                path = tp / 'test2'
                temp_file_path = Path(temp_file.name)
                copied_file_path = path / temp_file_path.name
                install_manager.copy_file(str(temp_file.name), path, temp_file_path.name)
                self.assertTrue(copied_file_path.exists())
                install_manager.remove_file(path, temp_file_path.name)
                self.assertFalse(copied_file_path.exists())
                self.assertFalse(tp.exists())
                self.assertFalse(path.exists())

    def test_archive_unpacking_and_removal(self):
        with TemporaryDirectory() as temp_path:
            base_path = Path(temp_path) / 'test_archive'
            unpack_path = base_path.parent / 'unpack_dir' / 'unpack_dir2'
            archive_path = create_archive(base_path, 'bztar')
            install_manager.unpack_archive(archive_path, 'bztar', unpack_path)
            self.assertTrue(unpack_path.exists())
            self.assertTrue(unpack_path / 'test.txt')
            self.assertTrue(unpack_path / 'test2.txt')
            self.assertTrue(unpack_path / 'test4.txt')
            install_manager.remove_directory(unpack_path)
            self.assertFalse(unpack_path.parent.exists())

    def test_file_presence(self):
        with NamedTemporaryFile() as file:
            self.assertTrue(install_manager.is_file_present(file.name))
            file.close()
            self.assertFalse(install_manager.is_file_present(file.name))

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_running_file(self, subprocess_run):
        install_manager.run_file('test_path.exe', ['arg1', 'arg2'])
        subprocess_run.assert_called_once_with(['test_path.exe', 'arg1', 'arg2'], check=True, shell=True)

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_running_file2(self, subprocess_run):
        install_manager.run_file('test_path.exe', None)
        subprocess_run.assert_called_once_with(['test_path.exe'], check=True, shell=True)

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_installing_msi(self, subprocess_run):
        install_manager.install_msi('test_package.msi', ['arg1', 'arg2'])
        subprocess_run.assert_called_once_with(['msiexec', '/I', 'test_package.msi', 'arg1', 'arg2'],
                                               capture_output=True, check=True, shell=True, text=True)

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_installing_msi2(self, subprocess_run):
        install_manager.install_msi('test_package.msi', None)
        subprocess_run.assert_called_once_with(['msiexec', '/I', 'test_package.msi'],
                                               capture_output=True, check=True, shell=True, text=True)

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_running_command(self, subprocess_run):
        install_manager.run_command('test_command', ['arg1', 'arg2'])
        subprocess_run.assert_called_once_with(['test_command', 'arg1', 'arg2'],
                                               capture_output=True, check=True, shell=True, text=True)

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_running_command2(self, subprocess_run):
        install_manager.run_command('test_command', None)
        subprocess_run.assert_called_once_with(['test_command'],
                                               capture_output=True, check=True, shell=True, text=True)

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_running_command_issue(self, subprocess_run):
        subprocess_run.side_effect = CalledProcessError(-1, ['test_command', 'arg1', 'arg2'])
        with self.assertRaises(CalledProcessError):
            install_manager.run_command('test_command', ['arg1', 'arg2'])
        subprocess_run.assert_called_once_with(['test_command', 'arg1', 'arg2'],
                                               capture_output=True, check=True, shell=True, text=True)

    @patch.multiple(thespiae.install.system, subprocess_run=DEFAULT)
    def test_running_command_no_restart(self, subprocess_run):
        subprocess_run.side_effect = CalledProcessError(3010, ['test_command', 'arg1', 'arg2'])
        install_manager.run_command('test_command', ['arg1', 'arg2'])
        subprocess_run.assert_called_once_with(['test_command', 'arg1', 'arg2'],
                                               capture_output=True, check=True, shell=True, text=True)

    @patch.multiple(thespiae.install.system, OpenKeyEx=DEFAULT)
    def test_product_code_presence(self, OpenKeyEx):
        err = OSError()
        err.winerror = 2
        OpenKeyEx.side_effect = err
        self.assertFalse(install_manager.is_product_code_present('{123}'))
        self.assert_called_exactly_with_no_order(OpenKeyEx,
                                                 call(HKEY_LOCAL_MACHINE,
                                                      r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{123}', 0,
                                                      KEY_READ | KEY_WOW64_32KEY),
                                                 call(HKEY_LOCAL_MACHINE,
                                                      r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{123}', 0,
                                                      KEY_READ | KEY_WOW64_64KEY),
                                                 call(HKEY_CURRENT_USER,
                                                      r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{123}', 0,
                                                      KEY_READ | KEY_WOW64_32KEY),
                                                 call(HKEY_CURRENT_USER,
                                                      r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{123}', 0,
                                                      KEY_READ | KEY_WOW64_64KEY))

    @patch.multiple(thespiae.install.system, OpenKeyEx=DEFAULT)
    def test_product_code_presence2(self, OpenKeyEx):
        self.assertTrue(install_manager.is_product_code_present('{123}'))


class TestDownloadManager(ExtraAssertMixin, TestCase):

    def test_spec_filtering(self):
        with TemporaryDirectory() as temp_path:
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'),
                              hash='bddace389020162bfc3cec0d82042a8eeebc73cb0fdcf9b50bde03a476329d66',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'), hash=None, download_path=str(p2),
                               part_path=str(p2) + '.part', name='a', version='2')
            copy_to('test.txt', str(p))
            self.assertSequenceEqual(download_manager.filter_present([sp, sp2]), [sp2])

    def test_spec_filtering2(self):
        with TemporaryDirectory() as temp_path:
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'),
                              hash='bddace389020162bfc3cec0d82042a8eeebc73cb0fdcf9b50bde03a476329d66',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'), hash=None, download_path=str(p2),
                               part_path=str(p2) + '.part', name='a', version='2')
            copy_to('test.txt', str(p), 5)
            with self.assertRaises(HashError) as c:
                download_manager.filter_present([sp, sp2])
            self.assertEqual(c.exception.download_spec, sp)
            self.assertEqual(c.exception.actual_hash,
                             '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5')

    def test_no_check_downloading_feedback(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'), hash=None, download_path=str(p),
                              part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'), hash=None, download_path=str(p2),
                               part_path=str(p2) + '.part', name='a', version='2')
            download_manager.download([sp, sp2], fb)
            self.assertTrue(p.exists())
            self.assertTrue(p2.exists())
            fb.report_download_started.assert_called_once()
            self.assert_called_exactly_with_no_order(fb.report_entry_download_initiated, call(sp), call(sp2))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_started, call(sp, 0, 18),
                                                     call(sp2, 0, 18))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_finished, call(sp), call(sp2))
            assert_download_progress_for(fb, {sp, sp2})
            fb.report_download_finished.assert_called_once()

    def test_hash_check_downloading(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'),
                              hash='bddace389020162bfc3cec0d82042a8eeebc73cb0fdcf9b50bde03a476329d66',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'),
                               hash='a132b1e5a4bd5a4f201e2b3fffdefaf7a9864dcae43c1963eeab7c13661ae6be',
                               download_path=str(p2), part_path=str(p2) + '.part', name='b', version='2')
            download_manager.download([sp, sp2], fb)
            self.assertTrue(p.exists())
            self.assertTrue(p2.exists())
            fb.report_download_started.assert_called_once()
            self.assert_called_exactly_with_no_order(fb.report_entry_download_initiated, call(sp), call(sp2))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_started, call(sp, 0, 18),
                                                     call(sp2, 0, 18))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_finished, call(sp), call(sp2))
            assert_download_progress_for(fb, {sp, sp2})
            fb.report_download_finished.assert_called_once()

    def test_hash_check_downloading2(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'),
                              hash='bddace389020162bfc3cec0d82042a8eeebc73cb0fdcf9b50bde03a476329d66',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'), hash='123', download_path=str(p2),
                               part_path=str(p2) + '.path', name='b', version='2')
            with self.assertRaises(HashError) as c:
                download_manager.download([sp, sp2], fb)
            self.assertEqual(c.exception.download_spec, sp2)
            self.assertEqual(c.exception.actual_hash,
                             'a132b1e5a4bd5a4f201e2b3fffdefaf7a9864dcae43c1963eeab7c13661ae6be')
            fb.report_download_started.assert_called_once()
            self.assert_called_exactly_with_no_order(fb.report_entry_download_initiated, call(sp), call(sp2))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_started, call(sp, 0, 18),
                                                     call(sp2, 0, 18))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_finished, call(sp), call(sp2))
            assert_download_progress_for(fb, {sp, sp2})
            fb.report_download_finished.assert_not_called()

    def test_not_found_downloading(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test3.txt'
            p2 = Path(temp_path) / 'test' / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test3.txt'), hash=None, download_path=str(p),
                              part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'),
                               hash='a132b1e5a4bd5a4f201e2b3fffdefaf7a9864dcae43c1963eeab7c13661ae6be',
                               download_path=str(p2), part_path=str(p2) + '.part', name='b', version='2')
            with self.assertRaises(UnsupportedResponseError) as c:
                download_manager.download([sp, sp2], fb)
            self.assertEqual(c.exception.download_spec, sp)
            self.assertEqual(c.exception.status, 404)
            self.assertIsNotNone(c.exception.headers)
            fb.report_download_started.assert_called_once()
            self.assert_called_exactly_with_no_order(fb.report_entry_download_initiated, call(sp), call(sp2))
            fb.report_download_finished.assert_not_called()

    def test_partial_downloading(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'),
                              hash='bddace389020162bfc3cec0d82042a8eeebc73cb0fdcf9b50bde03a476329d66',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'),
                               hash='a132b1e5a4bd5a4f201e2b3fffdefaf7a9864dcae43c1963eeab7c13661ae6be',
                               download_path=str(p2), part_path=str(p2) + '.part', name='b', version='2')
            copy_to('test2.txt', str(p2) + '.part', 12)
            download_manager.download([sp, sp2], fb)
            self.assertTrue(p.exists())
            self.assertTrue(p2.exists())
            self.assertCountEqual(web_server.get_request_data(),
                                  [('/static/test.txt', None), ('/static/test2.txt', 'bytes=12-')])
            fb.report_download_started.assert_called_once()
            self.assert_called_exactly_with_no_order(fb.report_entry_download_initiated, call(sp), call(sp2))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_started, call(sp, 0, 18),
                                                     call(sp2, 12, 18))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_finished, call(sp), call(sp2))
            assert_download_progress_for(fb, {sp, sp2})
            fb.report_download_finished.assert_called_once()

    def test_partial_downloading2(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'),
                              hash='bddace389020162bfc3cec0d82042a8eeebc73cb0fdcf9b50bde03a476329d66',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'),
                               file_hash='a132b1e5a4bd5a4f201e2b3fffdefaf7a9864dcae43c1963eeab7c13661ae6be',
                               download_path=str(p2), part_path=str(p2) + '.part', name='b', version='2')
            copy_to('test2.txt', str(p2) + '.part')
            download_manager.download([sp, sp2], fb)
            self.assertTrue(p.exists())
            self.assertTrue(p2.exists())
            self.assertCountEqual(web_server.get_request_data(),
                                  [('/static/test.txt', None), ('/static/test2.txt', 'bytes=18-')])
            fb.report_download_started.assert_called_once()
            self.assert_called_exactly_with_no_order(fb.report_entry_download_initiated, call(sp), call(sp2))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_started, call(sp, 0, 18),
                                                     call(sp2, 18, 18))
            self.assert_called_exactly_with_no_order(fb.report_entry_download_finished, call(sp), call(sp2))
            assert_download_progress_for(fb, {sp})
            fb.report_download_finished.assert_called_once()

    def test_partial_downloading3(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test4.txt'
            copy_to('test2.txt', str(p) + '.part', 10)
            sp = DownloadSpec(url=web_server.create_url_for('dynamic/test4.txt'),
                              hash='771c8bf33bbaea2ebc52d77cbd010185bc7ec53a0a44860cf8d3e352cebc4462',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            download_manager.download([sp], fb)
            self.assertTrue(p.exists())
            self.assertCountEqual(web_server.get_request_data(), [('/dynamic/test4.txt', 'bytes=10-')])
            fb.report_download_started.assert_called_once()
            fb.report_entry_download_initiated.assert_called_once_with(sp)
            fb.report_entry_download_started.assert_called_once_with(sp, 0, 56)
            fb.report_entry_download_finished.assert_called_once_with(sp)
            assert_download_progress_for(fb, {sp})
            fb.report_download_finished.assert_called_once()

    def test_partial_downloading4(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test5.txt'
            sp = DownloadSpec(url=web_server.create_url_for('dynamic/test5.txt'), hash=None, download_path=str(p),
                              part_path=str(p) + '.part', name='a', version='1')
            copy_to('test2.txt', str(p) + '.part', 10)
            with self.assertRaises(UnsupportedResponseError) as c:
                download_manager.download([sp], fb)
            self.assertEqual(c.exception.download_spec, sp, fb)
            self.assertEqual(c.exception.status, 416)
            self.assertIsNotNone(c.exception.headers)
            self.assertCountEqual(web_server.get_request_data(), [('/dynamic/test5.txt', 'bytes=10-')])
            fb.report_download_started.assert_called_once()
            fb.report_entry_download_initiated.assert_called_once_with(sp)
            fb.report_download_finished.assert_not_called()

    def test_partial_downloading5(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test6.txt'
            sp = DownloadSpec(url=web_server.create_url_for('dynamic/test6.txt'), hash=None, download_path=str(p),
                              part_path=str(p) + '.part', name='a', version='1')
            copy_to('test2.txt', str(p) + '.part', 10)
            with self.assertRaises(UnsupportedResponseError) as c:
                download_manager.download([sp], fb)
            self.assertEqual(c.exception.download_spec, sp, fb)
            self.assertEqual(c.exception.status, 416)
            self.assertIsNotNone(c.exception.headers)
            self.assertCountEqual(web_server.get_request_data(), [('/dynamic/test6.txt', 'bytes=10-')])
            fb.report_download_started.assert_called_once()
            fb.report_entry_download_initiated.assert_called_once_with(sp)
            fb.report_download_finished.assert_not_called()

    def test_skiping_downloaded_files(self):
        web_server.reset_request_data()
        with TemporaryDirectory() as temp_path:
            fb = NonCallableMock(spec_set=Feedback)
            p = Path(temp_path) / 'test.txt'
            p2 = Path(temp_path) / 'test2.txt'
            sp = DownloadSpec(url=web_server.create_url_for('static/test.txt'),
                              hash='bddace389020162bfc3cec0d82042a8eeebc73cb0fdcf9b50bde03a476329d66',
                              download_path=str(p), part_path=str(p) + '.part', name='a', version='1')
            sp2 = DownloadSpec(url=web_server.create_url_for('static/test2.txt'),
                               hash='a132b1e5a4bd5a4f201e2b3fffdefaf7a9864dcae43c1963eeab7c13661ae6be',
                               download_path=str(p2), part_path=str(p2) + '.part', name='b', version='2')
            copy_to('test2.txt', str(p2))
            download_manager.download(download_manager.filter_present([sp, sp2]), fb)
            self.assertTrue(p.exists())
            self.assertTrue(p2.exists())
            self.assertCountEqual(web_server.get_request_data(), [('/static/test.txt', None)])
            fb.report_download_started.assert_called_once()
            fb.report_entry_download_initiated.assert_called_once_with(sp)
            fb.report_entry_download_started.assert_called_once_with(sp, 0, 18)
            fb.report_entry_download_finished.assert_called_once_with(sp)
            assert_download_progress_for(fb, {sp})
            fb.report_download_finished.assert_called_once()
