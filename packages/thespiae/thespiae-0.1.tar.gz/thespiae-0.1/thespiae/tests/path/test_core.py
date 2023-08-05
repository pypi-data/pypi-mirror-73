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

from collections import namedtuple
from unittest import TestCase
from unittest.mock import NonCallableMock

from thespiae.conf import AppData
from thespiae.conf.core import create_app_entry
from thespiae.path.core import get_path_entries, get_single_path_entry, construct_new_user_path
from thespiae.path.exception import PathEntryError, PathError, InconsistentUserPathExtensionError, \
    InconsistentPathEntryExtensionError, InconsistentUserPathEntryDataError, InconsistentActualPathEntryDataError, \
    InvalidPathEntryError, InvalidSystemPathError, InvalidUserPathError
from thespiae.path.protocol import Feedback
from .helper import complex_string, PathManagerMockResetMixin, set_path_manager_data
from .singleton import path_processor, path_manager


class PathConstructorTest(TestCase):

    def test_getting_path_entries(self):
        empty = ('', ([], []))
        strings = ('   "" ;"  " ', (['""', '"  "'], ['', '  ']))
        cx = (complex_string, (['"a bc"', 'def', "'g", "h'"], ['a bc', 'def', "'g", "h'"]))
        for path_string, (expected_raw_entries, expected_entries) in [empty, strings, cx]:
            with self.subTest(path_string=path_string, expected_raw_entries=expected_raw_entries,
                              expected_entries=expected_entries):
                self.assertSequenceEqual(get_path_entries(path_string, True), expected_raw_entries)
                self.assertSequenceEqual(get_path_entries(path_string, False), expected_entries)

    def test_getting_path_entries2(self):
        with self.assertRaises(PathError):
            get_path_entries('";', True)

    def test_getting_path_entries3(self):
        with self.assertRaises(PathError):
            get_path_entries('abc;d"e', True)

    def test_gettings_single_path_entry(self):
        self.assertEqual(get_single_path_entry('"abc"', True), '"abc"')
        self.assertEqual(get_single_path_entry('"abc"', False), 'abc')

    def test_gettings_single_path_entry2(self):
        with self.assertRaises(PathEntryError):
            get_single_path_entry('abc;d', True)

    def test_constructing_new_user_path(self):
        dataset = namedtuple('dataset', ['system_path_entries', 'raw_user_path_entries', 'user_path_entries',
                                         'raw_actual_entries', 'actual_entries', 'obsolete_entries'])
        input_data = [dataset(system_path_entries=['C:\\bin'], raw_user_path_entries=[], user_path_entries=[],
                              raw_actual_entries=['"D:\\bi;n"'], actual_entries=['D:\\bi;n'], obsolete_entries=[]),
                      dataset(system_path_entries=['C:\\bin'], raw_user_path_entries=['D:\\bin'],
                              user_path_entries=['D:\\bin'], raw_actual_entries=['D:\\bin'], actual_entries=['D:\\bin'],
                              obsolete_entries=[]),
                      dataset(system_path_entries=['C:\\bin'], raw_user_path_entries=['"D:\\bin"'],
                              user_path_entries=['D:\\bin'], raw_actual_entries=['E:\\bin'], actual_entries=['E:\\bin'],
                              obsolete_entries=[]),
                      dataset(system_path_entries=['C:\\bin'], raw_user_path_entries=['"D:\\bin"'],
                              user_path_entries=['D:\\bin'], raw_actual_entries=['E:\\bin'], actual_entries=['E:\\bin'],
                              obsolete_entries=['D:\\bin']),
                      dataset(system_path_entries=['C:\\bin'], raw_user_path_entries=['"D:\\bin"'],
                              user_path_entries=['D:\\bin'], raw_actual_entries=['E:\\bin'], actual_entries=['E:\\bin'],
                              obsolete_entries=['C:\\bin'])]
        expected_output = ['"D:\\bi;n"', 'D:\\bin', '"D:\\bin";E:\\bin', 'E:\\bin', '"D:\\bin";E:\\bin']
        for inputs, output in zip(input_data, expected_output):
            with self.subTest(**inputs._asdict(), expected=output):
                self.assertEqual(construct_new_user_path(**inputs._asdict()), output)

    def test_constructing_new_user_path2(self):
        with self.assertRaises(InconsistentUserPathEntryDataError):
            construct_new_user_path([], ['C:\\bin'], [], [], [], [])

    def test_constructing_new_user_path3(self):
        with self.assertRaises(InconsistentActualPathEntryDataError):
            construct_new_user_path([], [], [], ['C:\\bin'], [], [])


class PathProcessorTest(PathManagerMockResetMixin, TestCase):

    def test_processing_path_changes(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_path_manager_data('C:\\bin', '"D:\\%TEST_VAR2%n";E:\\bin', {'TEST_VAR': 'i;n', 'TEST_VAR2': 'b;i'})
        app_data = AppData([create_app_entry([{'name': 'a', 'version': '1',
                                               'path_entries': ['"E:\\bin"', '"F:\\b%TEST_VAR%"'], 'keep': True}], []),
                            create_app_entry([{'name': 'b', 'version': '2',
                                               'path_entries': ['"D:\\%TEST_VAR2%n"']}], [])])
        path_processor.process_path_changes(app_data, fb)
        fb.report_path_analysis.assert_called_once()
        fb.confirm_user_path_update.assert_called_once_with('"D:\\%TEST_VAR2%n";E:\\bin', 'E:\\bin;"F:\\b%TEST_VAR%"')
        path_manager.set_user_path.assert_called_once_with('E:\\bin;"F:\\b%TEST_VAR%"')
        path_manager.notify_path_change.assert_called_once()
        fb.report_user_path_updated.assert_called_once()
        fb.report_user_path_no_changes.assert_not_called()

    def test_processing_path_changes2(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_path_manager_data('"C:\\b;in', 'D:\\bi%TEST_VAR%:\\bin', {'TEST_VAR': 'n;E'})
        app_data = AppData([create_app_entry([{'name': 'a', 'version': '1',
                                               'path_entries': ['F:\\bin'], 'keep': True}], []),
                            create_app_entry([{'name': 'b', 'version': '2'}], [])])
        with self.assertRaises(InvalidSystemPathError):
            path_processor.process_path_changes(app_data, fb)
        fb.report_path_analysis.assert_called_once()
        fb.confirm_user_path_update.assert_not_called()
        path_manager.set_user_path.assert_not_called()
        path_manager.notify_path_change.assert_not_called()
        fb.report_user_path_updated.assert_not_called()
        fb.report_user_path_no_changes.assert_not_called()

    def test_processing_path_changes3(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_path_manager_data('C:\\bin', 'D:\\bi%TEST_VAR%:\\b"in', {'TEST_VAR': 'n;E'})
        app_data = AppData([create_app_entry([{'name': 'a', 'version': '1',
                                               'path_entries': ['F:\\bin'], 'keep': True}], []),
                            create_app_entry([{'name': 'b', 'version': '2'}], [])])
        with self.assertRaises(InvalidUserPathError):
            path_processor.process_path_changes(app_data, fb)
        fb.report_path_analysis.assert_called_once()
        fb.confirm_user_path_update.assert_not_called()
        fb.report_path_analysis.assert_called_once()
        path_manager.set_user_path.assert_not_called()
        path_manager.notify_path_change.assert_not_called()
        fb.report_user_path_updated.assert_not_called()
        fb.report_user_path_no_changes.assert_not_called()

    def test_processing_path_changes4(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_path_manager_data('C:\\bin', 'D:\\bi%TEST_VAR%:\\bin', {'TEST_VAR': 'n;E'})
        app_data = AppData([create_app_entry([{'name': 'a', 'version': '1',
                                               'path_entries': ['F:\\bin'], 'keep': True}], []),
                            create_app_entry([{'name': 'b', 'version': '2'}], [])])
        with self.assertRaises(InconsistentUserPathExtensionError) as c:
            path_processor.process_path_changes(app_data, fb)
        fb.report_path_analysis.assert_called_once()
        fb.confirm_user_path_update.assert_not_called()
        path_manager.set_user_path.assert_not_called()
        path_manager.notify_path_change.assert_not_called()
        fb.report_user_path_updated.assert_not_called()
        fb.report_user_path_no_changes.assert_not_called()
        self.assertEqual(c.exception.data, 'D:\\bi%TEST_VAR%:\\bin')
        self.assertEqual(c.exception.extended_data, 'D:\\bin;E:\\bin')

    def test_processing_path_changes5(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_path_manager_data('C:\\bin', 'D:\\bin;E:\\bin', {'TEST_VAR': 'i;n'})
        app_data = AppData([create_app_entry([{'name': 'a', 'version': '1',
                                               'path_entries': ['F:\\b%TEST_VAR%'], 'keep': True}], []),
                            create_app_entry([{'name': 'b', 'version': '2'}], [])])
        with self.assertRaises(InconsistentPathEntryExtensionError) as c:
            path_processor.process_path_changes(app_data, fb)
        fb.report_path_analysis.assert_called_once()
        fb.confirm_user_path_update.assert_not_called()
        path_manager.set_user_path.assert_not_called()
        path_manager.notify_path_change.assert_not_called()
        fb.report_user_path_updated.assert_not_called()
        fb.report_user_path_no_changes.assert_not_called()
        self.assertEqual(c.exception.data, 'F:\\b%TEST_VAR%')
        self.assertEqual(c.exception.extended_data, 'F:\\bi;n')

    def test_processing_path_changes6(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_path_manager_data('C:\\bin', 'D:\\bin;E:\\bin', {})
        app_data = AppData([create_app_entry([{'name': 'a', 'version': '1',
                                               'path_entries': ['F:\\bi;n'], 'keep': True}], []),
                            create_app_entry([{'name': 'b', 'version': '2'}], [])])
        with self.assertRaises(InvalidPathEntryError) as c:
            path_processor.process_path_changes(app_data, fb)
        fb.report_path_analysis.assert_called_once()
        fb.confirm_user_path_update.assert_not_called()
        self.assertEqual(c.exception.entry, 'F:\\bi;n')
        self.assertEqual(c.exception.app_entry, create_app_entry([{'name': 'a', 'version': '1',
                                                                   'path_entries': ['F:\\bi;n'], 'keep': True}], []))
        fb.report_user_path_updated.assert_not_called()
        fb.report_user_path_no_changes.assert_not_called()
        path_manager.set_user_path.assert_not_called()
        path_manager.notify_path_change.assert_not_called()

    def test_processing_path_changes7(self):
        fb = NonCallableMock(spec_set=Feedback)
        set_path_manager_data('C:\\bin', '"D:\\%TEST_VAR2%n";E:\\bin', {'TEST_VAR': 'i;n', 'TEST_VAR2': 'b;i'})
        app_data = AppData([create_app_entry([{'name': 'a', 'version': '1', 'path_entries': [], 'keep': True}], []),
                            create_app_entry([{'name': 'b', 'version': '2', 'path_entries': []}], [])])
        path_processor.process_path_changes(app_data, fb)
        fb.report_path_analysis.assert_called_once()
        fb.confirm_user_path_update.assert_not_called()
        path_manager.set_user_path.assert_not_called()
        path_manager.notify_path_change.assert_not_called()
        fb.report_user_path_updated.assert_not_called()
        fb.report_user_path_no_changes.assert_called_once()
