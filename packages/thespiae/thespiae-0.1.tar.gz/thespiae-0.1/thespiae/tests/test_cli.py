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

import builtins
import sys
from unittest import TestCase
from unittest.mock import patch, DEFAULT, NonCallableMagicMock, call, ANY

import thespiae.cli
from thespiae.conf import AppEntry
from thespiae.exception import ThespiaeError
from thespiae.install import DownloadSpec


@patch.object(sys, 'argv', new=['script_path', 'config_file_path', 'data_dir_path'])
@patch.multiple(thespiae.cli, _error=DEFAULT, _position_after_bars=DEFAULT)
class CLITestCase(TestCase):

    def test_param_parsing(self, _error, _position_after_bars):
        ui = thespiae.cli.CLI('thespiae')
        self.assertEqual(ui.params.config_file, 'config_file_path')
        self.assertEqual(ui.params.data_dir, 'data_dir_path')
        _error.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_keyboard_interrupt(self, _error, _position_after_bars):
        with thespiae.cli.CLI('thespiae'):
            raise KeyboardInterrupt
        _error.assert_called()
        _position_after_bars.assert_called_once()

    def test_no_confirm_interrupt(self, _error, _position_after_bars):
        with thespiae.cli.CLI('thespiae'):
            raise thespiae.cli._NotConfirmedError
        _error.assert_called()
        _position_after_bars.assert_called_once()

    def test_application_error(self, _error, _position_after_bars):
        class TestError(ThespiaeError):

            def __str__(self):
                return '123'

        with thespiae.cli.CLI('thespiae'):
            raise TestError
        _error.assert_called_once_with('123')
        _position_after_bars.assert_called_once()


@patch.object(sys, 'argv', new=['script_path', 'config_file_path', 'data_dir_path'])
@patch.multiple(thespiae.cli, _error=DEFAULT, _info=DEFAULT, _confirm=DEFAULT, tqdm=DEFAULT,
                _position_after_bars=DEFAULT)
class CLIFeedbackTestCase(TestCase):

    def test_report_checking_software(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_checking_software()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_confirm_operations(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.confirm_operations([DownloadSpec(name='test')], [AppEntry(name='test2')],
                                           [AppEntry(name='test3')])
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_called_once()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_software_set_no_changes(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_software_set_no_changes()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_download_started(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_download_started()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_entry_download_initiated(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.confirm_operations([DownloadSpec(name='test')], [AppEntry(name='test2')],
                                           [AppEntry(name='test3')])
            ui.feedback.report_entry_download_initiated(DownloadSpec(name='test'))
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_called()
        tqdm.assert_called_once()
        _position_after_bars.assert_not_called()

    def test_report_entry_download_started(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.confirm_operations([DownloadSpec(name='test')], [AppEntry(name='test2')],
                                           [AppEntry(name='test3')])
            ui.feedback.report_entry_download_initiated(DownloadSpec(name='test'))
            ui.feedback.report_entry_download_started(DownloadSpec(name='test'), 5, 15)
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_called_once()
        tqdm.assert_called_once()
        self.assertEqual(tqdm.return_value.total, 15)
        self.assertEqual(tqdm.return_value.n, 5)
        tqdm.return_value.refresh.assert_called_once()
        _position_after_bars.assert_not_called()

    def test_report_entry_download_progress(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.confirm_operations([DownloadSpec(name='test')], [AppEntry(name='test2')],
                                           [AppEntry(name='test3')])
            ui.feedback.report_entry_download_initiated(DownloadSpec(name='test'))
            ui.feedback.report_entry_download_progress(DownloadSpec(name='test'), 10)
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_called_once()
        tqdm.assert_called_once()
        tqdm.return_value.update.assert_called_once_with(10)
        _position_after_bars.assert_not_called()

    def test_report_entry_download_finished(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_entry_download_finished(DownloadSpec(name='test'))
        _info.assert_not_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_download_finished(self, _error, _info, _confirm, tqdm, _position_after_bars):
        items = [NonCallableMagicMock(), NonCallableMagicMock()]
        tqdm.side_effect = items
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.confirm_operations([DownloadSpec(name='test'), DownloadSpec(name='test2')], [], [])
            ui.feedback.report_entry_download_initiated(DownloadSpec(name='test'))
            ui.feedback.report_entry_download_initiated(DownloadSpec(name='test2'))
            ui.feedback.report_entry_download_started(DownloadSpec(name='test'), 5)
            ui.feedback.report_entry_download_started(DownloadSpec(name='test2'), 10)
            ui.feedback.report_entry_download_progress(DownloadSpec(name='test'), 5)
            ui.feedback.report_entry_download_progress(DownloadSpec(name='test2'), 10)
            ui.feedback.report_download_finished()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_called()
        self.assertEqual(tqdm.call_count, 2)
        _position_after_bars.assert_called_once_with(2)
        self.assertSequenceEqual(items[0].method_calls, [call.refresh(), call.update(5), call.refresh(), call.close()])
        self.assertSequenceEqual(items[1].method_calls, [call.refresh(), call.update(10), call.refresh(), call.close()])

    def test_report_removal_started(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_removal_started()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_entry_removal_started(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_entry_removal_started(AppEntry(name='test2'))
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_entry_removal_finished(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_entry_removal_finished(AppEntry(name='test2'))
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_removal_finished(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_removal_finished()
        _info.assert_not_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_installation_started(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_installation_started()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_entry_installation_started(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_entry_installation_started(AppEntry(name='test2'))
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_entry_installation_finished(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_entry_installation_finished(AppEntry(name='test2'))
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_installation_finished(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_installation_finished()
        _info.assert_not_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_path_analysis(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_path_analysis()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_confirm_user_path_update(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.confirm_user_path_update('before', 'after')
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_called_once()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_user_path_no_changes(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_user_path_no_changes()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()

    def test_report_user_path_updated(self, _error, _info, _confirm, tqdm, _position_after_bars):
        with thespiae.cli.CLI('thespiae') as ui:
            ui.feedback.report_user_path_updated()
        _info.assert_called()
        _error.assert_not_called()
        _confirm.assert_not_called()
        tqdm.assert_not_called()
        _position_after_bars.assert_not_called()


@patch.multiple(builtins, print=DEFAULT, input=DEFAULT)
class InternalCLITestCase(TestCase):

    def test_displaying_info(self, print, input):
        thespiae.cli._info('test_data')
        print.assert_called_once_with('test_data', file=ANY)
        input.assert_not_called()

    def test_displaying_error(self, print, input):
        thespiae.cli._error('test_data')
        print.assert_called_once_with('test_data', file=ANY)
        input.assert_not_called()

    def test_asking_confirmation(self, print, input):
        input.return_value = 'y'
        thespiae.cli._confirm('test_data')
        input.assert_called_once()
        print.assert_not_called()

    @patch.multiple(sys, stdout=DEFAULT)
    def test_moving_cursor(self, stdout, print, input):
        thespiae.cli._position_after_bars(5)
        self.assertSequenceEqual(stdout.mock_calls, [call.write('\r'), call.write('\x1b[4B'), call.flush()])
        print.assert_not_called()
        input.assert_not_called()

    @patch.multiple(sys, stdout=DEFAULT)
    def test_moving_cursor2(self, stdout, print, input):
        thespiae.cli._position_after_bars(0)
        self.assertSequenceEqual(stdout.mock_calls, [])
        print.assert_not_called()
        input.assert_not_called()

    def test_asking_confirmation2(self, print, input):
        input.return_value = ''
        with self.assertRaises(thespiae.cli._NotConfirmedError):
            thespiae.cli._confirm('test_data')
        input.assert_called_once()
        print.assert_not_called()
