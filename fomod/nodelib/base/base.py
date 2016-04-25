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

from PyQt5.QtGui import QStandardItem
from os import sep
from .exceptions import (BaseInstanceException, WrongParentException, RemoveRequiredChildException,
                         RemoveChildException, TextNotAllowedException)


class ObjectBase(object):
    def __init__(self, name, tag, allowed_instances, element,
                 allow_parent=True, default_text="", allow_text=False,
                 allowed_children=None, max_children=0, required_children=None,
                 properties=None, default_properties=None):
        if type(self) is ObjectBase:
            raise BaseInstanceException(self)

        if not properties:
            properties = {}
        if not default_properties:
            default_properties = {}
        if not allowed_children:
            allowed_children = ()
        if not required_children:
            required_children = ()

        self.name = name
        self.tag = tag
        self.children = []
        self.properties = properties
        self.allowed_children = allowed_children
        self.max_children = max_children
        self.required_children = required_children
        self.allow_text = allow_text
        self.text = ""
        self.element = element
        self.allow_parent = allow_parent
        self.parent = None
        self.allowed_instances = allowed_instances

        self.model_item = NodeStandardItem(self)
        self.model_item.setText(self.name)
        self.model_item.setEditable(False)

        if default_text:
            self.set_text(default_text)
        if default_properties:
            self.set_properties(default_properties)

    def can_add_child(self, child):
        if not child.allow_parent:
            raise WrongParentException(child, self)

        if child.allowed_instances:
            instances = 0
            for item in self.children:
                if type(item) == type(child):
                    instances += 1
            if instances >= child.allowed_instances:
                return False

        if type(child) in self.allowed_children and \
                (not self.max_children or len(self.children) < self.max_children):
            return True
        return False

    def add_child(self, child):
        if self.can_add_child(child):
            self.children.append(child)
            child.parent = self
            self.model_item.appendRow(child.model_item)
            return True
        return False

    def check_required_children(self, child):
        if self.required_children and type(child) in self.required_children:
            instances = 0
            for item in self.children:
                if type(item) in self.required_children:
                    instances += 1
            if instances < 2:
                return False
        return True

    def remove_child(self, child):
        try:
            self.check_required_children(child)
        except RemoveRequiredChildException:
            raise
        else:
            if child in self.children:
                self.children.remove(child)
            else:
                raise RemoveChildException(child, self)

            if child.model_item.row() == -1:
                raise RemoveChildException(child, self)
            else:
                self.model_item.takeRow(child.model_item.row())

    def set_text(self, text):
        if self.allow_text:
            self.text = text
        else:
            raise TextNotAllowedException(self)

    def set_properties(self, properties):
        for key in properties:
            if self.properties[key].editable and (properties[key] in self.properties[key].values or
                                                  isinstance(properties[key], str)):
                self.properties[key].value = properties[key]

    def set_item_name(self, name):
        if not name:
            self.model_item.setText(self.name)
        elif "name" in self.properties:
            self.model_item.setText(name)
        elif "source" in self.properties:
            split_name = name.split(sep)
            self.model_item.setText(split_name[len(split_name) - 1])

    def iter(self):
        result = [self]

        for child in self.children:
            result.extend(child.iter())

        return result


class NodeStandardItem(QStandardItem):
    """A Standard Item but with an added reference to a xml node."""
    def __init__(self, node):
        self.xml_node = node
        super().__init__()
