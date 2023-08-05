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

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from antlr4.error.Errors import ParseCancellationException

from thespiae.path.envparse.EnvLexer import EnvLexer
from thespiae.path.envparse.EnvParserListener import EnvParserListener
from thespiae.path.factory import EnvParser
from .helper import complex_string


class _TestParserListener(EnvParserListener):

    def __init__(self):
        self._entries = []

    def enterEntry(self, ctx: EnvParser.EntryContext):
        self._entries.append(ctx.getText())

    @property
    def entries(self):
        return self._entries


def _get_token_stream(token_string: str) -> CommonTokenStream:
    lexer = EnvLexer(InputStream(token_string))
    return CommonTokenStream(lexer)


def _get_parser(token_string: str) -> EnvParser:
    return EnvParser(_get_token_stream(token_string))


class EnvLexerTest(TestCase):

    def test_string_tokenization(self):
        empty = ('', [])
        cx = (complex_string, ['"a bc"', ';', 'def', ';', "'g", ';', "h'", ';'])
        for string, tokens in [empty, cx]:
            with self.subTest(token_string=string, expected_tokens=tokens):
                stream = _get_token_stream(string)
                stream.fill()
                ts = stream.getTokens(0, len(tokens) + 1)
                self.assertSequenceEqual([t.text for t in ts], tokens)


class EnvParserTest(TestCase):

    def test_string_parsing(self):
        empty = ('', [])
        cx = (complex_string, ['"a bc"', 'def', '\'g', 'h\''])
        for string, entries in [empty, cx]:
            with self.subTest(string=string, expected_entries=entries):
                parser = _get_parser(string)
                listener = _TestParserListener()
                walker = ParseTreeWalker()
                walker.walk(listener, parser.path())
                self.assertSequenceEqual(listener.entries, entries)

    def test_path_entry_validation(self):
        self.assertEqual('abc', _get_parser('abc').single_entry().getChild(0).getText())
        with self.assertRaises(ParseCancellationException):
            _get_parser('de;f').single_entry()
