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
    tag = "fomod"

    def _init(self):
        allowed_children = (NodeName, NodeAuthor, NodeDescription, NodeID, NodeGroup, NodeVersion, NodeWebsite)
        self.init("Info", type(self).tag, 1, allow_text=False, allowed_children=allowed_children)
        super()._init()


class NodeName(NodeBase):
    tag = "Name"

    def _init(self):
        self.init("Name", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeAuthor(NodeBase):
    tag = "Author"

    def _init(self):
        self.init("Author", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeVersion(NodeBase):
    tag = "Version"

    def _init(self):
        self.init("Version", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeID(NodeBase):
    tag = "Id"

    def _init(self):
        self.init("ID", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeWebsite(NodeBase):
    tag = "Website"

    def _init(self):
        self.init("Website", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeDescription(NodeBase):
    tag = "Description"

    def _init(self):
        self.init("Description", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeGroup(NodeBase):
    tag = "Groups"

    def _init(self):
        allowed_child = (NodeElement,)
        self.init("Group", type(self).tag, 1, allowed_children=allowed_child)
        super()._init()


class NodeElement(NodeBase):
    tag = "element"

    def _init(self):
        self.init("Element", type(self).tag, 0, allow_text=True)
        super()._init()
