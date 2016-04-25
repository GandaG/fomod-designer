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

from .base import NodeBase


class NodeInfo(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeName, NodeAuthor, NodeDescription,
                            NodeID, NodeGroup, NodeVersion, NodeWebsite)

        super().__init__("Info", "fomod", 1, element, False,
                         allowed_children=allowed_children)


class NodeName(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Name", "Name", 1, element, allow_text=True, default_text=text)


class NodeAuthor(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Author", "Author", 1, element, allow_text=True, default_text=text)


class NodeVersion(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Version", "Version", 1, element, allow_text=True, default_text=text)


class NodeID(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("ID", "Id", 1, element, allow_text=True, default_text=text)


class NodeWebsite(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Website", "Website", 1, element, allow_text=True, default_text=text)


class NodeDescription(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Description", "Description", 1, element, allow_text=True, default_text=text)


class NodeGroup(NodeBase):
    def __init__(self, element=None):
        allowed_child = (NodeElement,)

        super().__init__("Group", "Groups", 1, element,
                         allowed_children=allowed_child)


class NodeElement(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Element", "element", 0, element, allow_text=True, default_text=text)
