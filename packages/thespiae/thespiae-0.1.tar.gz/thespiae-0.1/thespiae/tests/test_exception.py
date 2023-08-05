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

from dataclasses import dataclass, field
from typing import Sequence, Mapping
from unittest import TestCase

from thespiae.exception import generate___str__, META_FORMAT


class ExceptionFormattingTestCase(TestCase):

    def test_formatting(self):
        @generate___str__('test message')
        @dataclass(frozen=True)
        class TestError:
            pass

        te = TestError()
        self.assertEqual(str(te), 'test message')

    def test_formatting2(self):
        @generate___str__
        @dataclass(frozen=True)
        class TestError:
            field1: int = field(metadata={META_FORMAT: 'field #1: {}'})
            field2: int = field(metadata={META_FORMAT: 'field #2: {}'})

        te = TestError('a', 1)
        self.assertEqual(str(te), 'field #1: a, field #2: 1')

    def test_formatting3(self):
        @generate___str__('test message')
        @dataclass(frozen=True)
        class TestError:
            field1: int = field(metadata={META_FORMAT: 'field #1: {}'})
            field2: int = field(metadata={META_FORMAT: 'field #2: {}'})

        te = TestError('a', 1)
        self.assertEqual(str(te), 'test message; field #1: a, field #2: 1')

    def test_formatting4(self):
        @generate___str__('test message')
        @dataclass(frozen=True)
        class TestError:
            field1: str = field(metadata={META_FORMAT: 'field #1: {}'})
            field2: int = field(metadata={META_FORMAT: 'field #2: {}'})

        @generate___str__('test message 2')
        @dataclass(frozen=True)
        class TestError2(TestError):
            field3: Sequence[str] = field(metadata={META_FORMAT: 'field #3: {}'})
            field4: Mapping[str, int] = field(metadata={META_FORMAT: 'field #4: {}'})

        te = TestError2('a', 1, ['c', 'd'], {'e': 2})
        self.assertEqual(str(te), 'test message 2; field #1: a, field #2: 1, field #3: c, d, field #4: e:2')
