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

from dataclasses import replace
from pathlib import Path
from unittest import TestCase
from unittest.mock import call, NonCallableMock

from thespiae.conf import AppData, AppEntry
from thespiae.conf.core import get_app_config_from
from thespiae.install.exception import InvalidOrMissingAppDataError, InterruptedFileOperationsError, \
    UnknownInstallTypeError, UnknownUninstallTypeError
from thespiae.install.protocol import Feedback
from .helper import set_install_manager_data, InstallManagerMockResetMixin, DownloadManagerMockResetMixin, \
    ExtraAssertMixin, set_download_manager_data
from .singleton import exe_install_handler, msi_install_handler, command_install_handler, install_manager, \
    software_processor, download_manager, exe_uninstall_handler, msi_uninstall_handler, command_uninstall_handler, \
    file_install_handler, file_uninstall_handler, archive_install_handler, archive_uninstall_handler
from ..conf.helper import load_yaml_from_test_dir

_exe_entry1 = AppEntry(name='test', installer_url='http://example.com/123.exe', file_hash='4567', version='890',
                       uninstaller_path='123.exe', install_args=['a'], uninstall_args=['b'])


class ExeInstallHandlerTest(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(exe_install_handler.is_applicable(_exe_entry1))

    def test_applicability2(self):
        self.assertFalse(exe_install_handler.is_applicable(replace(_exe_entry1, installer_url=None)))

    def test_creating_download_spec(self):
        spec = exe_install_handler.create_download_spec(_exe_entry1, 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/123.exe')
        self.assertEqual(spec.download_path, 'C:\\test\\890\\test_890.exe')
        self.assertEqual(spec.hash, '4567')
        self.assertEqual(spec.name, 'test')
        self.assertEqual(spec.version, '890')

    def test_creating_download_spec2(self):
        e = replace(_exe_entry1, name='')
        with self.assertRaises(InvalidOrMissingAppDataError) as c:
            exe_install_handler.create_download_spec(e, 'C:\\')
        self.assertEqual(c.exception.app_entry, e)
        self.assertEqual(c.exception.key, 'name')
        self.assertEqual(c.exception.value, '')

    def test_creating_download_spec3(self):
        spec = exe_install_handler.create_download_spec(replace(_exe_entry1, version=None), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/123.exe')
        self.assertEqual(spec.download_path, 'C:\\test\\test.exe')
        self.assertEqual(spec.hash, '4567')
        self.assertEqual(spec.name, 'test')

    def test_creating_download_spec4(self):
        spec = exe_install_handler.create_download_spec(replace(_exe_entry1, architecture='x86_64'), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/123.exe')
        self.assertEqual(spec.download_path, 'C:\\test\\890\\x86_64\\test_890_x86_64.exe')
        self.assertEqual(spec.hash, '4567')
        self.assertEqual(spec.name, 'test')
        self.assertEqual(spec.version, '890')
        self.assertEqual(spec.architecture, 'x86_64')

    def test_installing(self):
        ds = exe_install_handler.create_download_spec(_exe_entry1, 'C:\\')
        exe_install_handler.install(_exe_entry1, ds)
        install_manager.run_file.assert_called_once_with('C:\\test\\890\\test_890.exe', ['a'])


class ExeUninstallHandlerTest(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(exe_uninstall_handler.is_applicable(_exe_entry1))

    def test_applicability2(self):
        self.assertFalse(exe_uninstall_handler.is_applicable(replace(_exe_entry1, uninstaller_path=None)))

    def test_is_installed_checking(self):
        set_install_manager_data(True, None, None)
        self.assertTrue(exe_uninstall_handler.is_installed(_exe_entry1))
        install_manager.is_file_present.assert_called_once_with('123.exe')

    def test_uninstalling(self):
        exe_uninstall_handler.uninstall(_exe_entry1)
        install_manager.run_file.assert_called_once_with('123.exe', ['b'])


_msi_entry1 = AppEntry(name='test', version='890', package_url='http://example.com/123.msi', product_code='123',
                       file_hash='4567', install_args=['a'], uninstall_args=['b'])


class MSIInstallHandlerTest(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(msi_install_handler.is_applicable(_msi_entry1))

    def test_applicability2(self):
        self.assertFalse(msi_install_handler.is_applicable(replace(_msi_entry1, package_url=None)))

    def test_creating_download_spec(self):
        spec = msi_install_handler.create_download_spec(_msi_entry1, 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/123.msi')
        self.assertEqual(spec.download_path, 'C:\\test\\890\\test_890.msi')
        self.assertEqual(spec.hash, '4567')
        self.assertEqual(spec.name, 'test')
        self.assertEqual(spec.version, '890')

    def test_creating_download_spec2(self):
        e = replace(_msi_entry1, name='')
        with self.assertRaises(InvalidOrMissingAppDataError) as c:
            msi_install_handler.create_download_spec(e, 'C:\\')
        self.assertEqual(c.exception.app_entry, e)
        self.assertEqual(c.exception.key, 'name')
        self.assertEqual(c.exception.value, '')

    def test_creating_download_spec3(self):
        spec = msi_install_handler.create_download_spec(replace(_msi_entry1, version=None), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/123.msi')
        self.assertEqual(spec.download_path, 'C:\\test\\test.msi')
        self.assertEqual(spec.hash, '4567')
        self.assertEqual(spec.name, 'test')

    def test_creating_download_spec4(self):
        spec = msi_install_handler.create_download_spec(replace(_msi_entry1, architecture='x86_64'), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/123.msi')
        self.assertEqual(spec.download_path, 'C:\\test\\890\\x86_64\\test_890_x86_64.msi')
        self.assertEqual(spec.hash, '4567')
        self.assertEqual(spec.name, 'test')
        self.assertEqual(spec.version, '890')
        self.assertEqual(spec.architecture, 'x86_64')

    def test_installing(self):
        msi_install_handler.install(_msi_entry1, msi_install_handler.create_download_spec(_msi_entry1, 'C:\\'))
        install_manager.install_msi.assert_called_once_with('C:\\test\\890\\test_890.msi', ['a'])


class MSIUninstallHandlerTest(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(msi_uninstall_handler.is_applicable(_msi_entry1))

    def test_applicability2(self):
        self.assertFalse(msi_uninstall_handler.is_applicable(replace(_msi_entry1, product_code=None)))

    def test_is_installed_checking(self):
        set_install_manager_data(None, True, None)
        self.assertTrue(msi_uninstall_handler.is_installed(_msi_entry1))
        install_manager.is_product_code_present.assert_called_once_with('123')

    def test_uninstalling(self):
        msi_uninstall_handler.uninstall(_msi_entry1)
        install_manager.uninstall_msi.assert_called_once_with('123', ['b'])


_command_entry1 = AppEntry(name='test', version='456', command='testc', install_args=['a'], list_args=['b'],
                           installed_list_entry='123:456', uninstall_args=['c'])


class CommandInstallHandlerTest(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(command_install_handler.is_applicable(_command_entry1))

    def test_applicability2(self):
        self.assertFalse(command_install_handler.is_applicable(replace(_msi_entry1, command=None)))

    def test_creating_download_spec(self):
        self.assertIsNone(command_install_handler.create_download_spec(_msi_entry1, 'C:\\'))

    def test_installing(self):
        command_install_handler.install(_command_entry1, None)
        install_manager.run_command.assert_called_once_with('testc', ['a'])


class CommandUninstallHandlerTest(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(command_uninstall_handler.is_applicable(_command_entry1))

    def test_applicability2(self):
        self.assertFalse(command_uninstall_handler.is_applicable(replace(_command_entry1, list_args=None)))

    def test_applicability3(self):
        self.assertFalse(command_uninstall_handler.is_applicable(replace(_command_entry1, installed_list_entry=None)))

    def test_is_installed_checking(self):
        set_install_manager_data(None, None, 'a:b\r\n123:456\r\nc:d\r\n')
        self.assertTrue(command_uninstall_handler.is_installed(_command_entry1))
        install_manager.run_command.assert_called_once_with('testc', ['b'])

    def test_uninstalling(self):
        command_uninstall_handler.uninstall(_command_entry1)
        install_manager.run_command.assert_called_once_with('testc', ['c'])


_file_entry1 = AppEntry(name='123', version='456', file_url='http://example.com/1.txt',
                        file_directory=r'C:\test\test2', file_name='test.txt', file_hash='789')


class FileInstallTestCase(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(file_install_handler.is_applicable(_file_entry1))

    def test_applicability2(self):
        self.assertFalse(file_install_handler.is_applicable(replace(_file_entry1, file_url=None)))

    def test_applicability3(self):
        self.assertFalse(file_install_handler.is_applicable(replace(_file_entry1, file_directory=None)))

    def test_applicability4(self):
        self.assertFalse(file_install_handler.is_applicable(replace(_file_entry1, file_name=None)))

    def test_creating_download_spec(self):
        spec = file_install_handler.create_download_spec(_file_entry1, 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/1.txt')
        self.assertEqual(spec.download_path, 'C:\\123\\456\\123_456.txt')
        self.assertEqual(spec.part_path, 'C:\\123\\456\\123_456.txt.part')
        self.assertEqual(spec.hash, '789')
        self.assertEqual(spec.name, '123')
        self.assertEqual(spec.version, '456')

    def test_creating_download_spec2(self):
        spec = file_install_handler.create_download_spec(replace(_file_entry1, version=None), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/1.txt')
        self.assertEqual(spec.download_path, 'C:\\123\\123.txt')
        self.assertEqual(spec.part_path, 'C:\\123\\123.txt.part')
        self.assertEqual(spec.hash, '789')
        self.assertEqual(spec.name, '123')

    def test_creating_download_spec3(self):
        spec = file_install_handler.create_download_spec(replace(_file_entry1, architecture='x86_64'), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/1.txt')
        self.assertEqual(spec.download_path, 'C:\\123\\456\\x86_64\\123_456_x86_64.txt')
        self.assertEqual(spec.part_path, 'C:\\123\\456\\x86_64\\123_456_x86_64.txt.part')
        self.assertEqual(spec.hash, '789')
        self.assertEqual(spec.name, '123')
        self.assertEqual(spec.version, '456')

    def test_installing(self):
        file_install_handler.install(_file_entry1, file_install_handler.create_download_spec(_file_entry1, 'C:\\'))
        install_manager.copy_file.assert_called_once_with('C:\\123\\456\\123_456.txt', Path('C:/test/test2'),
                                                          'test.txt')

    def test_installing2(self):
        e = replace(_file_entry1, file_directory=[])
        with self.assertRaises(InvalidOrMissingAppDataError) as c:
            file_install_handler.install(e, file_install_handler.create_download_spec(e, 'C:\\'))
        self.assertEqual(c.exception.app_entry, e)
        self.assertEqual(c.exception.key, 'file_directory')
        self.assertEqual(c.exception.value, [])

    def test_installing4(self):
        install_manager.copy_file.side_effect = OSError
        with self.assertRaises(InterruptedFileOperationsError) as c:
            file_install_handler.install(_file_entry1, file_install_handler.create_download_spec(_file_entry1, 'C:\\'))
        self.assertEqual(c.exception.app_entry, _file_entry1)
        self.assertEqual(c.exception.root_directory, r'C:\test\test2')


class FileUninstallTestCase(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(file_uninstall_handler.is_applicable(_file_entry1))

    def test_applicability2(self):
        self.assertFalse(file_uninstall_handler.is_applicable(replace(_file_entry1, file_directory=None)))

    def test_applicability3(self):
        self.assertFalse(file_uninstall_handler.is_applicable(replace(_file_entry1, file_name=None)))

    def test_is_installed(self):
        file_uninstall_handler.is_installed(_file_entry1)
        install_manager.is_file_present.assert_called_once_with('C:\\test\\test2\\test.txt')

    def test_uninstalling(self):
        file_uninstall_handler.uninstall(_file_entry1)
        install_manager.remove_file.assert_called_once_with(Path('C:/test/test2'), 'test.txt')

    def test_uninstalling2(self):
        e = replace(_file_entry1, file_directory=[])
        with self.assertRaises(InvalidOrMissingAppDataError) as c:
            file_uninstall_handler.uninstall(e)
        self.assertEqual(c.exception.app_entry, e)
        self.assertEqual(c.exception.key, 'file_directory')
        self.assertEqual(c.exception.value, [])

    def test_uninstalling4(self):
        install_manager.remove_file.side_effect = OSError
        with self.assertRaises(InterruptedFileOperationsError) as c:
            file_uninstall_handler.uninstall(_file_entry1)
        self.assertEqual(c.exception.app_entry, _file_entry1)
        self.assertEqual(c.exception.root_directory, r'C:\test\test2')


_archive_entry1 = AppEntry(name='123', version='456', archive_url='http://example.com/1.file',
                           unpack_directory=r'C:\test\test2', archive_format='zip', file_hash='789')


class ArchiveInstallHandlerTestCase(TestCase):

    def test_applicability(self):
        self.assertTrue(archive_install_handler.is_applicable(_archive_entry1))

    def test_applicability2(self):
        self.assertFalse(archive_install_handler.is_applicable(replace(_archive_entry1, archive_url=None)))

    def test_applicability3(self):
        self.assertFalse(archive_install_handler.is_applicable(replace(_archive_entry1, archive_url=None)))

    def test_applicability4(self):
        self.assertFalse(archive_install_handler.is_applicable(replace(_archive_entry1, archive_format=None)))

    def test_creating_download_spec(self):
        spec = archive_install_handler.create_download_spec(_archive_entry1, 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/1.file')
        self.assertEqual(spec.download_path, 'C:\\123\\456\\123_456.zip')
        self.assertEqual(spec.part_path, 'C:\\123\\456\\123_456.zip.part')
        self.assertEqual(spec.hash, '789')
        self.assertEqual(spec.name, '123')
        self.assertEqual(spec.version, '456')

    def test_creating_download_spec2(self):
        spec = archive_install_handler.create_download_spec(replace(_archive_entry1, version=None), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/1.file')
        self.assertEqual(spec.download_path, 'C:\\123\\123.zip')
        self.assertEqual(spec.part_path, 'C:\\123\\123.zip.part')
        self.assertEqual(spec.hash, '789')
        self.assertEqual(spec.name, '123')

    def test_creating_download_spec3(self):
        spec = archive_install_handler.create_download_spec(replace(_archive_entry1, architecture='x86_64'), 'C:\\')
        self.assertEqual(spec.url, 'http://example.com/1.file')
        self.assertEqual(spec.download_path, 'C:\\123\\456\\x86_64\\123_456_x86_64.zip')
        self.assertEqual(spec.part_path, 'C:\\123\\456\\x86_64\\123_456_x86_64.zip.part')
        self.assertEqual(spec.hash, '789')
        self.assertEqual(spec.name, '123')
        self.assertEqual(spec.version, '456')

    def test_installing(self):
        archive_install_handler.install(_archive_entry1, archive_install_handler.create_download_spec(_archive_entry1,
                                                                                                      'C:\\'))
        install_manager.unpack_archive.assert_called_once_with(r'C:\123\456\123_456.zip', 'zip',
                                                               Path('C:/test/test2'))

    def test_installing2(self):
        e = replace(_archive_entry1, unpack_directory=None)
        with self.assertRaises(InvalidOrMissingAppDataError) as c:
            archive_install_handler.install(e, archive_install_handler.create_download_spec(e, 'C:\\'))
        self.assertEqual(c.exception.app_entry, e)
        self.assertEqual(c.exception.key, 'unpack_directory')
        self.assertEqual(c.exception.value, None)

    def test_installing4(self):
        install_manager.unpack_archive.side_effect = OSError
        with self.assertRaises(InterruptedFileOperationsError) as c:
            archive_install_handler.install(_archive_entry1,
                                            archive_install_handler.create_download_spec(_archive_entry1, 'C:\\'))
        self.assertEqual(c.exception.app_entry, _archive_entry1)
        self.assertEqual(c.exception.root_directory, r'C:\test\test2')


class ArchiveUninstallTestCase(InstallManagerMockResetMixin, TestCase):

    def test_applicability(self):
        self.assertTrue(archive_uninstall_handler.is_applicable(_archive_entry1))

    def test_applicability2(self):
        self.assertFalse(archive_uninstall_handler.is_applicable(replace(_archive_entry1, unpack_directory=None)))

    def test_applicability3(self):
        self.assertTrue(archive_uninstall_handler.is_applicable(replace(_archive_entry1, archive_format=None)))

    def test_is_installed(self):
        archive_uninstall_handler.is_installed(_archive_entry1)
        install_manager.is_file_present.assert_called_once_with(r'C:\test\test2')

    def test_uninstalling(self):
        archive_uninstall_handler.uninstall(_archive_entry1)
        install_manager.remove_directory.assert_called_once_with(Path('C:/test/test2'))

    def test_uninstalling2(self):
        e = replace(_archive_entry1, unpack_directory=None)
        with self.assertRaises(InvalidOrMissingAppDataError) as c:
            archive_uninstall_handler.uninstall(e)
        self.assertEqual(c.exception.app_entry, e)
        self.assertEqual(c.exception.key, 'unpack_directory')
        self.assertEqual(c.exception.value, None)

    def test_uninstalling4(self):
        install_manager.remove_directory.side_effect = OSError
        with self.assertRaises(InterruptedFileOperationsError) as c:
            archive_uninstall_handler.uninstall(_archive_entry1)
        self.assertEqual(c.exception.app_entry, _archive_entry1)
        self.assertEqual(c.exception.root_directory, r'C:\test\test2')


class SoftwareProcessorTestCase(InstallManagerMockResetMixin, DownloadManagerMockResetMixin, ExtraAssertMixin,
                                TestCase):

    def test_processing(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_install_manager_data(False, False, '')
        set_download_manager_data({'C:\\temp\\example2\\0.1b\\example2_0.1b.msi'})
        data = get_app_config_from(load_yaml_from_test_dir('app_list'))
        software_processor.process('C:\\temp', data, fb)
        specs = [exe_install_handler.create_download_spec(data.to_install[0], 'C:\\temp'),
                 msi_install_handler.create_download_spec(data.to_install[1], 'C:\\temp'),
                 file_install_handler.create_download_spec(data.to_install[3], 'C:\\temp'),
                 archive_install_handler.create_download_spec(data.to_install[4], 'C:\\temp')]
        download_manager.filter_present.assert_called_once_with(specs)
        download_manager.download.assert_called_once_with(specs[:1] + specs[2:], fb)
        fb.report_checking_software.assert_called_once()
        install_manager.uninstall_msi.assert_not_called()
        install_manager.copy_file.assert_called_once_with('C:\\temp\\example4\\x86_64\\example4_x86_64.exe',
                                                          Path('C:/temp/example4'), 'example4.exe')
        install_manager.unpack_archive.assert_called_once_with(r'C:\temp\example5\0.6\x86_64\example5_0.6_x86_64.zip',
                                                               'zip', Path('C:/temp/example5/0.6'))
        self.assert_called_exactly_with_no_order(install_manager.run_file,
                                                 call('C:\\temp\\example1\\1.1\\example1_1.1.exe',
                                                      ['/SILENT', '/DIR=C:\\Program Files\\Example1\\1.1']))
        self.assert_called_exactly_with_no_order(install_manager.run_command,
                                                 call('manager', ['list']), call('manager', ['list']),
                                                 call('manager', ['install', 'example3:1.1']))
        self.assert_called_exactly_with_no_order(install_manager.install_msi,
                                                 call('C:\\temp\\example2\\0.1b\\example2_0.1b.msi',
                                                      ['/q', 'INSTALLDIR=C:\\Program Files\\Example2']))
        fb.confirm_operations.assert_called_once_with(specs[:1] + specs[2:], [], list(data.to_install))
        fb.report_removal_started.assert_not_called()
        fb.report_removal_finished.assert_not_called()
        fb.report_installation_started.assert_called_once()
        fb.report_installation_finished.assert_called_once()
        self.assert_called_exactly_with_no_order(fb.report_entry_installation_started,
                                                 *(call(item) for item in data.to_install))
        self.assert_called_exactly_with_no_order(fb.report_entry_installation_finished,
                                                 *(call(item) for item in data.to_install))
        fb.report_entry_removal_started.assert_not_called()
        fb.report_entry_removal_finished.assert_not_called()

    def test_processing2(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_install_manager_data(True, True, 'example3_final:1.0\r\nexample3:1.1')
        set_download_manager_data(set())
        data = get_app_config_from(load_yaml_from_test_dir('app_list'))
        software_processor.process('C:\\temp', data, fb)
        fb.report_checking_software.assert_called_once()
        download_manager.filter_present.assert_called_once_with([])
        download_manager.download.assert_not_called()
        install_manager.install_msi.assert_not_called()
        install_manager.remove_file.assert_called_once_with(Path('C:/temp/example4'), 'example4.exe')
        install_manager.remove_directory.assert_called_once_with(Path('C:/temp/example5/0.5'))
        self.assert_called_exactly_with_no_order(install_manager.run_file,
                                                 call('C:\\Program Files\\Example1\\1.0\\uninstall.exe', None))
        self.assert_called_exactly_with_no_order(install_manager.run_command,
                                                 call('manager', ['list']), call('manager', ['list']),
                                                 call('manager', ['uninstall', 'example3_final:1.0']))
        self.assert_called_exactly_with_no_order(install_manager.uninstall_msi, call('pc1235', ['/q']))
        fb.confirm_operations.assert_called_once_with([], list(data.to_uninstall), [])
        fb.report_installation_started.assert_not_called()
        fb.report_installation_finished.assert_not_called()
        fb.report_removal_started.assert_called_once()
        fb.report_removal_finished.assert_called_once()
        self.assert_called_exactly_with_no_order(fb.report_entry_removal_started,
                                                 *(call(item) for item in data.to_uninstall))
        self.assert_called_exactly_with_no_order(fb.report_entry_removal_finished,
                                                 *(call(item) for item in data.to_uninstall))
        fb.report_entry_installation_started.assert_not_called()
        fb.report_entry_installation_finished.assert_not_called()

    def test_processing3(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_download_manager_data(set())
        data = AppData([])
        software_processor.process('C:\\temp', data, fb)
        fb.report_checking_software.assert_called_once()
        download_manager.download.assert_not_called()
        install_manager.install_msi.assert_not_called()
        install_manager.run_file.assert_not_called()
        install_manager.run_command.assert_not_called()
        install_manager.uninstall_msi.assert_not_called()
        install_manager.unpack_archive.assert_not_called()
        install_manager.remove_directory.assert_not_called()
        install_manager.copy_file.assert_not_called()
        install_manager.remove_file.assert_not_called()
        fb.confirm_operations.assert_not_called()
        fb.report_installation_started.assert_not_called()
        fb.report_installation_finished.assert_not_called()
        fb.report_removal_started.assert_not_called()
        fb.report_removal_finished.assert_not_called()
        fb.report_entry_removal_started.assert_not_called()
        fb.report_entry_removal_finished.assert_not_called()
        fb.report_entry_installation_started.assert_not_called()
        fb.report_entry_installation_finished.assert_not_called()
        fb.report_software_set_no_changes.assert_called_once()

    def test_processing4(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_download_manager_data(set())
        data = AppData([AppEntry(name='test', installer_url='http://example.com/file.exe')])
        with self.assertRaises(UnknownUninstallTypeError) as c:
            software_processor.process('C:\\temp', data, fb)
        self.assertEqual(c.exception.app_entry, data.to_uninstall[0])

    def test_processing5(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_download_manager_data(set())
        data = AppData([AppEntry(name='test', uninstaller_path='C:\\uninst.exe', keep=True)])
        with self.assertRaises(UnknownInstallTypeError) as c:
            software_processor.process('C:\\temp', data, fb)
        self.assertEqual(c.exception.app_entry, data.to_install[0])
