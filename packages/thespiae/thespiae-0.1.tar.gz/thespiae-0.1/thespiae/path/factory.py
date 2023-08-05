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

import sys
from typing import TYPE_CHECKING

from antlr4 import BailErrorStrategy
from antlr4.error.ErrorListener import ConsoleErrorListener

from .envparse.EnvParser import EnvParser as _EnvParser

if TYPE_CHECKING:
    from typing import TextIO

    from antlr4 import TokenStream


class EnvParser(_EnvParser):

    def __init__(self, input_stream: TokenStream, output: TextIO = sys.stdout, build_parse_trees=True):
        super().__init__(input_stream, output)
        self.removeErrorListener(ConsoleErrorListener.INSTANCE)
        self._errHandler = BailErrorStrategy()
        self.buildParseTrees = build_parse_trees
