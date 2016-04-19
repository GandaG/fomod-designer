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


class InstanceException(Exception):
    def __init__(self, instance):
        self.title = "Instance Error"
        self.message = "Offending instance type: " + type(instance)
        self.detailed = ""
        Exception.__init__(self, self.message)


class BaseInstanceException(InstanceException):
    def __init__(self, base):
        self.title = "Instance Error"
        self.message = "{} is not meant to be instanced. You should be using a subclass instead.".format(type(base))
        self.detailed = ""
        Exception.__init__(self, self.message)


class InstanceCreationException(InstanceException):
    def __init__(self, instance):
        self.title = "Instance Error"
        self.message = "Trying to create more instances of {} than allowed.".format(type(instance))
        self.detailed = ""
        Exception.__init__(self, self.message)


class WrongParentException(Exception):
    def __init__(self, instance, parent):
        self.title = "Parent Error"
        self.message = "{} has the wrong kind of parent - {}.".format(type(instance), type(parent))
        self.detailed = ""
        Exception.__init__(self, self.message)


class ChildException(Exception):
    def __init__(self, child):
        self.title = "Child Error"
        self.message = "Offending child type: " + type(child)
        self.detailed = ""
        Exception.__init__(self, self.message)


class AddChildException(ChildException):
    def __init__(self, child, parent):
        self.title = "Child Error"
        self.message = "Can't add child {} to parent {}.".format(type(child), type(parent))
        self.detailed = ""
        Exception.__init__(self, self.message)


class RemoveChildException(ChildException):
    def __init__(self, child, parent):
        self.title = "Child Error"
        self.message = "Can't remove child {} from parent {}.".format(type(child), type(parent))
        self.detailed = ""
        Exception.__init__(self, self.message)


class RemoveRequiredChildException(ChildException):
    def __init__(self, child, parent):
        self.title = "Child Error"
        self.message = "Can't remove {} - required child to {}.".format(type(child), type(parent))
        self.detailed = ""
        Exception.__init__(self, self.message)


class TextNotAllowedException(Exception):
    def __init__(self, instance):
        self.title = "Text Error"
        self.message = "Text not allowed in {} {}".format(type(instance), instance)
        self.detailed = ""
        Exception.__init__(self, self.message)


class FactoryTagNotFound(Exception):
    def __init__(self, tag):
        self.title = "Factory Error"
        self.message = "Factory couldn't find a class to match {}".format(tag)
        self.detailed = ""
        Exception.__init__(self, self.message)
