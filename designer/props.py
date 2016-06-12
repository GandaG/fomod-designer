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
    """
    Base class for the properties. Shouldn't be used directly.
    """
    def __init__(self, name, values, editable=True):
        """
        :param name: The display name of the variable.
        :param values: The acceptable values tuple.
        :param editable: If the property is editable. If not, it will not be displayed.
        """
        if type(self) is _PropertyBase:
            raise BaseInstanceException(self)

        self.name = name
        self.editable = editable

        self.value = ""
        self.values = values

    def set_value(self, value):
        """
        Method used to set the property's value. Sub-classes should validate the value before setting it.

        :param value: The value to be validated and set.
        """
        if self.editable:
            self.value = value


class PropertyText(_PropertyBase):
    """
    A property that holds simple text.
    """
    def __init__(self, name, text="", editable=True):
        super().__init__(name, (), editable)
        self.value = text


class PropertyCombo(_PropertyBase):
    """
    A property that holds a combo list - only one value from this list should be selected.
    """
    def __init__(self, name, values, editable=True):
        super().__init__(name, values, editable)
        self.value = values[0]

    def set_value(self, value):
        if value in self.values:
            super().set_value(value)


class PropertyInt(_PropertyBase):
    """
    A property that holds an integer.
    """
    def __init__(self, name, min_value, max_value, default, editable=True):
        """
        :param name: The display name of the variable.
        :param min_value: The minimum integer value.
        :param max_value: The maximum integer value.
        :param default: The default value for the property.
        :param editable: If the property is editable. If not, it will not be displayed.
        """
        self.min = min_value
        self.max = max_value
        values = range(min_value, max_value + 1)

        super().__init__(name, values, editable)
        self.value = default

    def set_value(self, value):
        if value in self.values:
            super().set_value(value)


class PropertyFolder(_PropertyBase):
    """
    A property that holds the path to a folder.
    """
    def __init__(self, name, text="", editable=True):
        super().__init__(name, (), editable)
        self.value = text


class PropertyFile(_PropertyBase):
    """
    A property that holds the path to a file.
    """
    def __init__(self, name, text="", editable=True):
        super().__init__(name, (), editable)
        self.value = text


class PropertyColour(_PropertyBase):
    """
    A property that holds a colour hex value.
    """
    def __init__(self, name, text="", editable=True):
        super().__init__(name, (), editable)
        self.value = text
