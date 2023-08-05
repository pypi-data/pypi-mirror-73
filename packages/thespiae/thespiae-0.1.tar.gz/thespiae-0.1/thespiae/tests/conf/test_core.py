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

from unittest import TestCase

from thespiae.conf.core import create_app_entry, get_app_config_from
from thespiae.conf.data import AppEntry, ConfigPath
from thespiae.conf.exception import AppDataMissingFieldError, \
    AppDataFieldValueTypeError, AppDataCircularReferenceError, ConfigElementTypeError, \
    ConfigDuplicatedEntryIdentityError, ConfigIncompleteBranchesError, ConfigExcessiveAttributeError, \
    ConfigRequiredAttributesNotFoundError
from .helper import load_yaml_from_test_dir, set_app_data_reader_data, AppDataReaderResetMixin
from .singleton import config_processor, app_data_reader


class AppEntryCreationTest(TestCase):

    def test_app_entry_creation(self):
        e = create_app_entry([{'name': 'example', 'version': '1.1'}], [])
        self.assertEqual(e.name, 'example')
        self.assertEqual(e.version, '1.1')

    def test_no_name(self):
        with self.assertRaises(AppDataMissingFieldError) as c:
            create_app_entry([{'version': '1.1'}], [ConfigPath('$[1]'), ConfigPath('$[1].versions[2]')])
        self.assertEqual(c.exception.field_name, 'name')
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[1]'), ConfigPath('$[1].versions[2]')])

    def test_int_instead_str(self):
        with self.assertRaises(AppDataFieldValueTypeError) as c:
            create_app_entry([{'name': 1}], [ConfigPath('$[2]')])
        self.assertEqual(c.exception.expected, str)
        self.assertEqual(c.exception.received, int)
        self.assertEqual(c.exception.field_name, 'name')
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[2]')])

    def test_int_list_instead_str_list(self):
        with self.assertRaises(AppDataFieldValueTypeError) as c:
            create_app_entry([{'name': 'example', 'version': '1.1', 'install_args': [1, 2, 3]}], [ConfigPath('$[3]')])
        self.assertEqual(c.exception.expected, str)
        self.assertEqual(c.exception.received, int)
        self.assertEqual(c.exception.field_name, 'install_args')
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[3]')])

    def test_str_instead_list(self):
        with self.assertRaises(AppDataFieldValueTypeError) as c:
            create_app_entry([{'name': 'example', 'version': '1.1', 'uninstall_args': 'abc'}],
                             [ConfigPath('$[9]'), ConfigPath('$[9].versions[5]')])
        self.assertEqual(c.exception.expected, list)
        self.assertEqual(c.exception.received, str)
        self.assertEqual(c.exception.field_name, 'uninstall_args')
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[9]'), ConfigPath('$[9].versions[5]')])

    def test_refinement(self):
        e = create_app_entry([{'name': 'example', 'version': '1.1'}, {'install_args': ['a', 'b', 'c']}], [])
        self.assertSequenceEqual(e.install_args, ['a', 'b', 'c'])

    def test_refinement2(self):
        e = create_app_entry([{'name': 'example', 'version': '1.1', 'install_args': ['a', 'b', 'c']},
                              {'install_args': ['a', 'b']}], [])
        self.assertSequenceEqual(e.install_args, ['a', 'b'])

    def test_refinement3(self):
        e = create_app_entry([{'name': 'example', 'version': '1.1', 'command': '$a', 'b': 'test'}, {'a': '$b'}], [])
        self.assertEqual(e.command, 'test')

    def test_refinement4(self):
        e = create_app_entry([{'name': 'example', 'version': '1.1', 'command': 'te${a}t'}, {'a': 's'}], [])
        self.assertEqual(e.command, 'test')

    def test_list_refinement(self):
        e = create_app_entry([{'name': 'example', 'version': '1.1', 'install_args': ['a${b}c', 'de$f']},
                              {'b': 0, 'f': 1}], [])
        self.assertSequenceEqual(e.install_args, ['a0c', 'de1'])

    def test_circular_reference(self):
        with self.assertRaises(AppDataCircularReferenceError) as c:
            create_app_entry([{'name': 'example', 'version': '1.1', 'command': '$command'}], [ConfigPath('$[1]')])
        self.assertEqual(c.exception.field_name, 'command')
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[1]')])

    def test_circular_reference2(self):
        with self.assertRaises(AppDataCircularReferenceError) as c:
            create_app_entry([{'name': 'example', 'version': '1.1', 'command': '$a', 'a': '$command'}],
                             [ConfigPath('$[1]')])
        self.assertEqual(c.exception.field_name, 'command')
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[1]')])

    def test_circular_reference3(self):
        with self.assertRaises(AppDataCircularReferenceError) as c:
            create_app_entry([{'name': 'example', 'version': '1.1', 'command': '$a'}, {'a': '$command'}],
                             [ConfigPath('$[1]'), ConfigPath('$[1].versions[2]')])
        self.assertEqual(c.exception.field_name, 'command')
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[1]'), ConfigPath('$[1].versions[2]')])

    def test_refinement_priority(self):
        e = create_app_entry([{'name': 'example', 'version': '1.1', 'command': '$a', 'a': 'test'}, {'a': 'test2'}], [])
        self.assertEqual(e.command, 'test2')


class AppDataCreationTest(TestCase):

    def test_app_list_processing(self):
        app_conf = get_app_config_from(load_yaml_from_test_dir('app_list'))
        self.assertEqual(len(app_conf.to_install), 5)
        self.assertEqual(len(app_conf.to_uninstall), 5)

    def test_app_list_processing2(self):
        with self.assertRaises(ConfigDuplicatedEntryIdentityError) as c:
            get_app_config_from(load_yaml_from_test_dir('app_list_duplicated_name_version'))
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[0]'), ConfigPath('$[0].versions[0]')])
        self.assertSequenceEqual(c.exception.another_paths, [ConfigPath('$[1]'), ConfigPath('$[1].versions[0]')])
        self.assertDictEqual(c.exception.identity_values, {'architecture': None, 'name': 'test', 'version': '1.0'})

    def test_app_list_processing3(self):
        ac = get_app_config_from(load_yaml_from_test_dir('app_list_no_versions'))
        self.assertSequenceEqual(ac.to_uninstall, [AppEntry(name='test2', version='1.0'),
                                                   AppEntry(name='test', version='1.0')])

    def test_config_structure(self):
        with self.assertRaises(ConfigElementTypeError) as c:
            get_app_config_from(load_yaml_from_test_dir('app_list_invalid_root'))
        self.assertEqual(c.exception.expected, list)
        self.assertEqual(c.exception.received, str)
        self.assertEqual(c.exception.config_path, ConfigPath('$'))

    def test_config_structure2(self):
        with self.assertRaises(ConfigElementTypeError) as c:
            get_app_config_from(load_yaml_from_test_dir('app_list_invalid_root_entry'))
        self.assertEqual(c.exception.expected, dict)
        self.assertEqual(c.exception.received, str)
        self.assertEqual(c.exception.config_path, ConfigPath('$[1]'))

    def test_config_structure3(self):
        with self.assertRaises(ConfigElementTypeError) as c:
            get_app_config_from(load_yaml_from_test_dir('app_list_invalid_versions'))
        self.assertEqual(c.exception.expected, list)
        self.assertEqual(c.exception.received, str)
        self.assertEqual(c.exception.config_path, ConfigPath('$[1].versions'))

    def test_config_structure4(self):
        with self.assertRaises(ConfigElementTypeError) as c:
            get_app_config_from(load_yaml_from_test_dir('app_list_invalid_version_entry'))
        self.assertEqual(c.exception.expected, dict)
        self.assertEqual(c.exception.received, str)
        self.assertEqual(c.exception.config_path, ConfigPath('$[1].versions[1]'))


class ConfigProcessorTest(AppDataReaderResetMixin, TestCase):

    def test_config_processing(self):
        set_app_data_reader_data('app_list')
        data = config_processor.process_config('config.yml')
        app_data_reader.read.assert_called_once_with('config.yml')
        to_install = [AppEntry(name='example1', installer_url='http://example1.com/test_1.1.exe', file_hash='1234',
                               uninstaller_path='C:\\Program Files\\Example1\\1.1\\uninstall.exe',
                               install_args=['/SILENT', '/DIR=C:\\Program Files\\Example1\\1.1'],
                               path_entries=['C:\\Program Files\\Example1\\1.1\\bin',
                                             'C:\\Program Files\\Example1\\1.1\\bin2'], version='1.1', keep=True),
                      AppEntry(name='example2', package_url='http://example.com/example2_0.1b.msi', file_hash='5678',
                               product_code='pc1234', install_args=['/q', 'INSTALLDIR=C:\\Program Files\\Example2'],
                               path_entries=['C:\\Program Files\\Example2'], version='0.1b',
                               keep=True),
                      AppEntry(name='example3', command='manager', install_args=['install', 'example3:1.1'],
                               uninstall_args=['uninstall', 'example3:1.1'],
                               path_entries=['C:\\apps\\example3\\1.1\\bin'], list_args=['list'],
                               installed_list_entry='example3:1.1', version='1.1', keep=True),
                      AppEntry(name='example4', architecture='x86_64', file_directory=r'C:\temp\example4',
                               file_url='http://example.com/x86_64/file.exe', file_name='example4.exe',
                               file_hash='456', keep=True),
                      AppEntry(name='example5', architecture='x86_64', unpack_directory=r'C:\temp\example5\0.6',
                               archive_url='http://example.com/x86_64/file-0.6.zip', archive_format='zip',
                               file_hash='123', keep=True, version='0.6')]
        to_uninstall = [AppEntry(name='example1', installer_url='http://example1.com/test_1.0.exe', file_hash='1235',
                                 uninstaller_path='C:\\Program Files\\Example1\\1.0\\uninstall.exe',
                                 install_args=['/SILENT', '/DIR=C:\\Program Files\\Example1\\1.0'],
                                 path_entries=['C:\\Program Files\\Example1\\1.0\\bin',
                                               'C:\\Program Files\\Example1\\1.0\\bin2'], version='1.0'),
                        AppEntry(name='example3', command='manager', install_args=['install', 'example3_final:1.0'],
                                 uninstall_args=['uninstall', 'example3_final:1.0'],
                                 path_entries=['C:\\apps\\example3\\1.0\\bin'], list_args=['list'],
                                 installed_list_entry='example3_final:1.0', version='1.0'),
                        AppEntry(name='example2', package_url='http://example.com/example2_0.1a.msi', file_hash='3579',
                                 product_code='pc1235', install_args=['/q', 'INSTALLDIR=C:\\Program Files\\Ex2'],
                                 uninstall_args=['/q'], path_entries=['C:\\Program Files\\Ex2'], version='0.1a'),
                        AppEntry(name='example4', architecture='x86', file_directory=r'C:\temp\example4',
                                 file_url='http://example.com/x86/file.exe', file_name='example4.exe',
                                 file_hash='123'),
                        AppEntry(name='example5', architecture='x86_64',
                                 unpack_directory=r'C:\temp\example5\0.5',
                                 archive_url='http://example.com/x86_64/file-0.5.zip', archive_format='zip',
                                 file_hash='456', version='0.5')]
        self.assertSequenceEqual(data.to_install, to_install)
        self.assertSequenceEqual(data.to_uninstall, to_uninstall)

    def test_config_processing2(self):
        set_app_data_reader_data('app_entry_name_only')
        data = config_processor.process_config('config.yml')
        self.assertEqual(len(data.to_install), 0)
        self.assertEqual(len(data.to_uninstall), 1)
        self.assertEqual(data.to_uninstall[0].name, 'example1')
        self.assertEqual(data.to_uninstall[0].file_hash, '123')


class NewConfigProcessorTest(TestCase):

    def test_config_data_processing(self):
        data = load_yaml_from_test_dir('advanced_config_structure')
        items = get_app_config_from(data)
        to_install = [AppEntry(name='test', version='0.3', architecture='x86_64', keep=True, file_hash='5'),
                      AppEntry(name='test', version='0.2', architecture='x86_64', keep=True, file_hash='6'),
                      AppEntry(name='test2', version='0.3', architecture='x86_64', keep=True, file_hash='5'),
                      AppEntry(name='test2', version='0.1', architecture='x86', keep=True, file_hash='7')]
        to_uninstall = [AppEntry(name='test', version='999.1', architecture='x86_128', file_hash='4'),
                        AppEntry(name='test', version='0.1', architecture='x86', file_hash='7'),
                        AppEntry(name='test2', version='999.1', architecture='x86_128', file_hash='4'),
                        AppEntry(name='test2', version='0.2', architecture='x86_64', file_hash='6')]
        self.assertSequenceEqual(items.to_install, to_install)
        self.assertSequenceEqual(items.to_uninstall, to_uninstall)

    def test_no_name(self):
        with self.assertRaises(ConfigRequiredAttributesNotFoundError) as c:
            get_app_config_from(load_yaml_from_test_dir('advanced_config_no_name'))
        self.assertEqual(c.exception.config_path, ConfigPath('$[1]'))
        self.assertSetEqual(c.exception.attributes, {'name'})

    def test_excessive_attribute(self):
        with self.assertRaises(ConfigExcessiveAttributeError) as c:
            get_app_config_from(load_yaml_from_test_dir('advanced_config_excessive_attribute.yml'))
        self.assertEqual(c.exception.config_path, ConfigPath('$[0].versions[0].versions'))

    def test_excessive_attribute2(self):
        with self.assertRaises(ConfigExcessiveAttributeError) as c:
            get_app_config_from(load_yaml_from_test_dir('advanced_config_excessive_attribute2.yml'))
        self.assertEqual(c.exception.config_path, ConfigPath('$[0].architectures[0].version'))

    def test_excessive_attribute3(self):
        with self.assertRaises(ConfigExcessiveAttributeError) as c:
            get_app_config_from(load_yaml_from_test_dir('advanced_config_excessive_attribute3.yml'))
        self.assertEqual(c.exception.config_path, ConfigPath('$[0].versions'))

    def test_incomplete_branches(self):
        with self.assertRaises(ConfigIncompleteBranchesError) as c:
            get_app_config_from(load_yaml_from_test_dir('advanced_config_incomplete_branches.yml'))
        self.assertSequenceEqual(c.exception.config_paths, [ConfigPath('$[0].architectures[0]')])
        self.assertSetEqual(c.exception.attributes, {'version'})
