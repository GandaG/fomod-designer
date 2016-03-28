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


class WrongParentException(Exception):
    def __init__(self, instance, parent):
        print("{} has the wrong kind of parent - {}.".format(type(instance), type(parent)))


class BaseInstanceException(Exception):
    def __init__(self, base):
        print("{} is not meant to be instanced. You should be using a subclass instead.".format(type(base)))


class InstanceCreationException(Exception):
    def __init__(self, instance):
        print("Trying to create more instances of {} than allowed.".format(type(instance)))


class AddChildException(Exception):
    def __init__(self, child, parent):
        print("Can't add child {} to parent {}.".format(type(child), type(parent)))


class RemoveChildException(Exception):
    def __init__(self, child, parent):
        print("Can't remove child {} from parent {}.".format(type(child), type(parent)))


class RemoveRequiredChildException(Exception):
    def __init__(self, child, parent):
        print("Can't remove {} - required child to {}.".format(type(child), type(parent)))


class TextNotAllowedException(Exception):
    def __init__(self, instance):
        print("Text not allowed in {} {}".format(type(instance), instance))


class FactoryTagNotFound(Exception):
    def __init__(self, tag):
        print("Factory couldn't find a class to match {}".format(tag))
