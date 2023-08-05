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

from ctypes import WinDLL, c_wchar_p, WinError
from ctypes.wintypes import HWND, UINT
from winreg import OpenKeyEx, QueryValueEx, CloseKey, ExpandEnvironmentStrings, SetValueEx, HKEY_CURRENT_USER, \
    KEY_SET_VALUE, REG_EXPAND_SZ, HKEY_LOCAL_MACHINE


class PathManager:
    notify_timeout = 1000

    @staticmethod
    def get_system_path() -> str:
        key = OpenKeyEx(HKEY_LOCAL_MACHINE, r'System\CurrentControlSet\Control\Session Manager\Environment')
        try:
            path, _ = QueryValueEx(key, 'Path')
        finally:
            CloseKey(key)
        return path

    @staticmethod
    def get_user_path() -> str:
        key = OpenKeyEx(HKEY_CURRENT_USER, 'Environment')
        try:
            path, _ = QueryValueEx(key, 'Path')
        finally:
            CloseKey(key)
        return path

    @staticmethod
    def extend_path_data(path_entry: str) -> str:
        return ExpandEnvironmentStrings(path_entry)

    @staticmethod
    def set_user_path(path: str) -> None:
        key = OpenKeyEx(HKEY_CURRENT_USER, 'Environment', access=KEY_SET_VALUE)
        try:
            SetValueEx(key, 'Path', 0, REG_EXPAND_SZ, path)
        finally:
            CloseKey(key)

    @staticmethod
    def notify_path_change() -> None:
        send_message_timeout_w = WinDLL('user32', use_last_error=True).SendMessageTimeoutW
        handle = HWND(0xffff)
        message = UINT(0x001A)
        l_param = c_wchar_p('Environment')
        flags = UINT(0x0002 & 0x0008)
        timeout = UINT(__class__.notify_timeout)
        result = send_message_timeout_w(handle, message, None, l_param, flags, timeout, None)
        if result == 0:
            raise WinError()
