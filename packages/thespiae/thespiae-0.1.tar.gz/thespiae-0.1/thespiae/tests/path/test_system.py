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


from ctypes.wintypes import HWND, UINT
from unittest import TestCase
from unittest.mock import patch, DEFAULT
from winreg import HKEY_CURRENT_USER, KEY_SET_VALUE, REG_EXPAND_SZ, HKEY_LOCAL_MACHINE

import thespiae.path.system as ts
from .singleton import real_path_manager as path_manager


class PathManagerTestCase(TestCase):

    @patch.multiple(ts, OpenKeyEx=DEFAULT, QueryValueEx=DEFAULT, CloseKey=DEFAULT)
    def test_getting_system_path(self, OpenKeyEx, QueryValueEx, CloseKey):
        QueryValueEx.return_value = 'test_system_path', None
        self.assertEqual(path_manager.get_system_path(), 'test_system_path')
        OpenKeyEx.assert_called_once_with(HKEY_LOCAL_MACHINE,
                                          r'System\CurrentControlSet\Control\Session Manager\Environment')
        QueryValueEx.assert_called_once_with(OpenKeyEx.return_value, 'Path')
        CloseKey.assert_called_once_with(OpenKeyEx.return_value)

    @patch.multiple(ts, OpenKeyEx=DEFAULT, QueryValueEx=DEFAULT, CloseKey=DEFAULT)
    def test_getting_user_path(self, OpenKeyEx, QueryValueEx, CloseKey):
        QueryValueEx.return_value = 'test_user_path', None
        self.assertEqual(path_manager.get_user_path(), 'test_user_path')
        OpenKeyEx.assert_called_once_with(HKEY_CURRENT_USER, 'Environment')
        QueryValueEx.assert_called_once_with(OpenKeyEx.return_value, 'Path')
        CloseKey.assert_called_once_with(OpenKeyEx.return_value)

    @patch.multiple(ts, ExpandEnvironmentStrings=DEFAULT)
    def test_extending_path_data(self, ExpandEnvironmentStrings):
        ExpandEnvironmentStrings.return_value = 'extended_test_data'
        self.assertEqual(path_manager.extend_path_data('test_data'), 'extended_test_data')
        ExpandEnvironmentStrings.assert_called_once_with('test_data')

    @patch.multiple(ts, OpenKeyEx=DEFAULT, CloseKey=DEFAULT, SetValueEx=DEFAULT)
    def test_setting_user_path(self, OpenKeyEx, CloseKey, SetValueEx):
        path_manager.set_user_path('test_user_path')
        OpenKeyEx.assert_called_once_with(HKEY_CURRENT_USER, 'Environment', access=KEY_SET_VALUE)
        SetValueEx.assert_called_once_with(OpenKeyEx.return_value, 'Path', 0, REG_EXPAND_SZ, 'test_user_path')
        CloseKey.assert_called_once_with(OpenKeyEx.return_value)

    @patch.multiple(ts, WinDLL=DEFAULT)
    def test_notifying_path_changes(self, WinDLL):
        path_manager.notify_path_change()
        WinDLL.assert_called_once_with('user32', use_last_error=True)
        args = WinDLL.return_value.SendMessageTimeoutW.call_args
        hwnd, msg, wParam, lParam, fuFlags, uTimeout, lpdwResult = args[0]
        self.assertEqual(hwnd.value, HWND(0xffff).value)
        self.assertEqual(msg.value, UINT(0x001A).value)
        self.assertIsNone(wParam)
        self.assertEqual(lParam.value, 'Environment')
        self.assertEqual(fuFlags.value, UINT(0x0002 & 0x0008).value)
        self.assertEqual(uTimeout.value, UINT(1000).value)
        self.assertIsNone(lpdwResult)

    @patch.multiple(ts, WinDLL=DEFAULT)
    def test_notifying_path_changes2(self, WinDLL):
        WinDLL.return_value.SendMessageTimeoutW.return_value = 0
        with self.assertRaises(OSError):
            path_manager.notify_path_change()
