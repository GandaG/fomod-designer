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
from lxml import etree
from os import sep
from .exceptions import BaseInstanceException


class NodeBase(etree.ElementBase):
    def _init(self):
        if type(self) is NodeBase:
            raise BaseInstanceException(self)
        super()._init()

    def init(self, name, tag, allowed_instances, allow_text=False, allowed_children=None, properties=None):

        if not properties:
            properties = {}
        if not allowed_children:
            allowed_children = ()

        self.name = name
        self.tag = tag
        self.properties = properties
        self.allowed_children = allowed_children
        self.allow_text = allow_text
        self.allowed_instances = allowed_instances

        self.model_item = NodeStandardItem(self)
        self.model_item.setText(self.name)
        self.model_item.setEditable(False)

        self.write_attribs()

    def can_add_child(self, child):
        if child.allowed_instances:
            instances = 0
            for item in self:
                if type(item) == type(child):
                    instances += 1
            if instances >= child.allowed_instances:
                return False
        if type(child) in self.allowed_children:
            return True
        return False

    def add_child(self, child):
        if self.can_add_child(child):
            self.append(child)
            self.model_item.appendRow(child.model_item)

    def remove_child(self, child):
        if child in self:
            self.model_item.takeRow(child.model_item.row())
            self.remove(child)

    def parse_attribs(self):
        for key in self.properties:
            if key not in self.attrib.keys():
                continue
            self.properties[key].set_value(self.attrib[key])
        self.update_item_name()

    def write_attribs(self):
        self.attrib.clear()
        for key in self.properties:
            self.set(key, str(self.properties[key].value))

    def update_item_name(self):
        if "name" in self.properties:
            if not self.properties["name"].value:
                self.model_item.setText(self.name)
                return
            self.model_item.setText(self.properties["name"].value)
        elif "source" in self.properties:
            if not self.properties["source"].value:
                self.model_item.setText(self.name)
                return
            split_name = self.properties["source"].value.split(sep)
            self.model_item.setText(split_name[len(split_name) - 1])
        else:
            self.model_item.setText(self.name)

    def set_text(self, text):
        if self.allow_text:
            self.text = text


class NodeStandardItem(QStandardItem):
    """A Standard Item but with an added reference to a xml node."""
    def __init__(self, node):
        self.xml_node = node
        super().__init__()
