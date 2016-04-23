#!/usr/bin/env python

# Copyright 2016 Daniel Nunes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .exceptions import BaseInstanceException


class _PropertyBase(object):
    def __init__(self, type_id, name, tag, values, editable=True):
        if type(self) is _PropertyBase:
            raise BaseInstanceException(self)

        self.type_id = type_id
        self.name = name
        self.tag = tag
        self.editable = editable

        self.value = ""
        self.values = values


class PropertyText(_PropertyBase):
    def __init__(self, name, tag, text="", editable=True):
        super().__init__(str, name, tag, (), editable)
        self.value = text

    def set_value(self, text):
        if self.editable:
            self.value = text


class PropertyCombo(_PropertyBase):
    def __init__(self, name, tag, values, editable=True):
        super().__init__(list, name, tag, values, editable)
        self.value = values[0]

    def set_value(self, value):
        if self.editable and value in self.values:
            self.value = value


class PropertyInt(_PropertyBase):
    def __init__(self, name, tag, min_value, max_value, default, editable=True):
        self.min = min_value
        self.max = max_value
        values = range(min_value, max_value + 1)

        super().__init__(int, name, tag, values, editable)
        self.value = default

    def set_value(self, value):
        if self.editable and value in self.values:
            self.value = value
