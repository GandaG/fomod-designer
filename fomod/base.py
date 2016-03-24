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
    def __init__(self, name, tag, allowed_instances, element,
                 allow_parent=True, default_text="", allow_text=False,
                 allowed_children=None, max_children=0, required_children=None,
                 properties=None, default_properties=None):
        if type(self) is ObjectBase:
            raise Exception("ObjectBase is not meant to be instanced. "
                            "You should be using a subclass instead.")

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

        if default_text:
            self.set_text(default_text)
        if default_properties:
            self.set_properties(default_properties)

    def add_child(self, child):
        if not child.allow_parent:
            raise Exception("Parent {} to {} is not allowed.".format(type(self),
                                                                     type(child)))

        if child.allowed_instances:
            instances = 0
            for item in self.children:
                if item is type(child):
                    instances += 1
            if instances >= child.allowed_instances:
                raise Exception("Trying to add more instances of {} than allowed.".format(child))

        if type(child) in self.allowed_children and self.max_children and len(self.children) < self.max_children:
            self.children.append(child)
            child.parent = self
        else:
            raise Exception("Can't add {} to parent {}".format(child, self))

    def remove_child(self, child):
        if self.required_children and type(child) in self.required_children:
            instances = 0
            for item in self.children:
                if type(item) in self.required_children:
                    instances += 1
            if instances < 2:
                raise Exception("Can't remove {} - required child.".format(child))

        if child in self.children:
            self.children.remove(child)
        else:
            raise Exception("Can't remove {} - it doesn't exists in parent's children list.".format(child))

    def set_text(self, text):
        if self.allow_text:
            self.text = text
            return True
        else:
            return False

    def set_properties(self, properties):
        for key in properties:
            if self.properties[key].editable and (properties[key] in self.properties[key].values or
                                                  isinstance(properties[key], str)):
                self.properties[key].value = properties[key]

    def find_object(self, attr, value):
        if getattr(self, attr) == value:
            return self
        else:
            for child in self.children:
                match = child.findObject(attr, value)
                if match:
                    return match


class PropertyBase(object):
    def __init__(self, name, tag, values, editable=True):
        if type(self) is PropertyBase:
            raise Exception("PropertyBase is not meant to be instanced. "
                            "You should be using a subclass instead.")

        self.name = name
        self.tag = tag
        self.editable = editable

        self.value = ""
        self.values = values
