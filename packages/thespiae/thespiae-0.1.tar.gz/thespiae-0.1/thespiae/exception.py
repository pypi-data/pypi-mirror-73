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

from dataclasses import fields
from functools import singledispatch, partial
from typing import List, Mapping, Set

META_FORMAT = 'format'


@singledispatch
def generate___str__(message: str):
    return partial(_generate___str__, message=message)


def _format_helper(obj) -> str:
    if isinstance(obj, Mapping):
        return ', '.join((f'{_format_helper(key)}:{_format_helper(value)}' for key, value in obj.items()))
    elif isinstance(obj, (List, Set)):
        return ', '.join((f'{_format_helper(item)}' for item in obj))
    else:
        return obj


@generate___str__.register
def _generate___str__(cls: type, message: str = None):
    if '__str__' in cls.__dict__:
        raise TypeError(f'{cls.__name__} explicitly defines __str__')

    def __str__(self):
        nonlocal message
        if message:
            es = [message]
        else:
            es = []
        fs = []
        for field in fields(cls):
            fmt = field.metadata.get(META_FORMAT, None)
            if fmt:
                val = getattr(self, field.name, None)
                if val is not None:
                    fs.append(fmt.format(_format_helper(val)))
        if fs:
            es.append(', '.join(fs))
        return '; '.join(es)

    setattr(cls, '__str__', __str__)
    return cls


class ThespiaeError(Exception):
    pass
