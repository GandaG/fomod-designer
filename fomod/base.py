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


class ObjectBase(object):
    def __init__(self, name, tag, allowed_instances,
                 parent, allow_parent=True,
                 default_text="", allow_text=False,
                 default_children=None, allowed_children=None,
                 max_children=0, required_children=None,
                 properties=None):
        if type(self) is ObjectBase:
            raise Exception("ObjectBase is not meant to be instanced. "
                            "You should be using a subclass instead.")

        if not properties:
            properties = {}
        if not default_children:
            default_children = []
        if not allowed_children:
            allowed_children = ()
        if not required_children:
            required_children = ()

        self.name = name
        self.tag = tag
        self.children = []
        self.properties = properties

        if allow_parent or not parent:
            self.parent = parent
        else:
            raise Exception("Parent {} to {} is not allowed.".format(type(parent),
                                                                     self.name))

        if parent and allowed_instances:
            instances = 0
            for child in self.parent.children:
                if child is type(self):
                    instances += 1
            if instances >= allowed_instances:
                raise Exception("Trying to create more instances than allowed.")

        self.allowed_children = allowed_children
        self.max_children = max_children
        self.required_children = required_children
        for child in default_children:
            self.add_child(child(self))

        self.allow_text = allow_text
        if allow_text:
            self._text = default_text

    def add_child(self, child):
        if type(child) in self.allowed_children and self.max_children and len(self.children) < self.max_children:
            self.children.append(child)
            return True
        else:
            return False

    def remove_child(self, child):
        instances = 0
        for item in self.children:
            if type(item) in self.required_children:
                instances += 1

        if child in self.children and instances >= 2:
            self.children.remove(child)
            return True
        else:
            return False

    def can_delete(self):
        if not self.parent or self in self.parent.default_children:
            return False
        else:
            return True

    def set_text(self, text):
        if self.allow_text:
            self._text = text
            return True
        else:
            return False


class PropertyBase(object):
    def __init__(self, name, tag, editable=True):
        self.name = name
        self.tag = tag
        self.editable = editable

        self.value = ""
