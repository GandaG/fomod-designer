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
from .props import PropertyCombo, PropertyInt, PropertyText


class NodeConfig(NodeBase):
    tag = "config"

    def _init(self):
        allowed_children = (NodeModName, NodeModImage, NodeModDepend, NodeInstallSteps, NodeReqFiles, NodeCondInstall)
        properties = {"{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation":
                      PropertyText("xsi", "http://qconsulting.ca/fo3/ModConfig5.0.xsd", False)}
        self.init("Config", type(self).tag, 1, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeModName(NodeBase):
    tag = "moduleName"

    def _init(self):
        properties = {"position": PropertyCombo("Position", ("Left", "Right", "RightOfImage")),
                      "colour": PropertyText("Colour", "000000")}
        self.init("Name", type(self).tag, 1, allow_text=True, properties=properties)
        super()._init()


class NodeModImage(NodeBase):
    tag = "moduleImage"

    def _init(self):
        properties = {"path": PropertyText("Path"), "showImage": PropertyCombo("Show Image", ("true", "false")),
                      "showFade": PropertyCombo("Show Fade", ("true", "false")),
                      "height": PropertyInt("Height", -1, 9999, -1)}
        self.init("Image", "moduleImage", 1, properties=properties)
        super()._init()


class NodeModDepend(NodeBase):
    tag = "moduleDependencies"

    def _init(self):
        allowed_children = (NodeDependFile, NodeDependFlag, NodeDependGame)
        properties = {"operator": PropertyCombo("Type", ["And", "Or"])}
        self.init("Mod Dependencies", type(self).tag, 1, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeReqFiles(NodeBase):
    tag = "requiredInstallFiles"

    def _init(self):
        allowed_children = (NodeFile, NodeFolder)
        self.init("Mod Requirements", type(self).tag, 0, allowed_children=allowed_children)
        super()._init()


class NodeInstallSteps(NodeBase):
    tag = "installSteps"

    def _init(self):
        allowed_children = (NodeInstallStep,)
        properties = {"order": PropertyCombo("Order", ["Ascending", "Descending", "Explicit"])}
        self.init("Installation Steps", type(self).tag, 1, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeCondInstall(NodeBase):
    tag = "conditionalFileInstalls"

    def _init(self):
        allowed_children = (NodePatterns,)
        self.init("Conditional Installation", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeDependFile(NodeBase):
    tag = "fileDependency"

    def _init(self):
        properties = {"file": PropertyText("File"),
                      "state": PropertyCombo("State", ("Active", "Inactive", "Missing"))}
        self.init("File Dependency", type(self).tag, 0, properties=properties)
        super()._init()


class NodeDependFlag(NodeBase):
    tag = "flagDependency"

    def _init(self):
        properties = {"flag": PropertyText("Flag"), "value": PropertyText("Value")}
        self.init("Flag Dependency", type(self).tag, 0, properties=properties)
        super()._init()


class NodeDependGame(NodeBase):
    tag = "gameDependency"

    def _init(self):
        properties = {"version": PropertyText("Version")}
        self.init("Game Dependency", "gameDependency", 1, properties=properties)
        super()._init()


class NodeFile(NodeBase):
    tag = "file"

    def _init(self):
        properties = {"source": PropertyText("Source"),
                      "destination": PropertyText("Destination"),
                      "priority": PropertyInt("Priority", 0, 99, 0),
                      "alwaysInstall": PropertyCombo("Always Install", ("true", "false")),
                      "installIfUsable": PropertyCombo("Install If Usable", ("true", "false"))}
        self.init("File", type(self).tag, 0, properties=properties)
        super()._init()


class NodeFolder(NodeBase):
    tag = "folder"

    def _init(self):
        properties = {"source": PropertyText("Source"),
                      "destination": PropertyText("Destination"),
                      "priority": PropertyInt("Priority", 0, 99, 0),
                      "alwaysInstall": PropertyCombo("Always Install", ("true", "false")),
                      "installIfUsable": PropertyCombo("Install If Usable", ("true", "false"))}
        self.init("Folder", type(self).tag, 0, properties=properties)
        super()._init()


class NodePatterns(NodeBase):
    tag = "patterns"

    def _init(self):
        allowed_children = (NodePattern,)
        self.init("Patterns", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodePattern(NodeBase):
    tag = "pattern"

    def _init(self):
        allowed_children = (NodeFiles, NodeDependencies)
        self.init("Pattern", type(self).tag, 0, allowed_children=allowed_children)
        super()._init()


class NodeFiles(NodeBase):
    tag = "files"

    def _init(self):
        allowed_children = (NodeFile, NodeFolder)
        self.init("Files", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeDependencies(NodeBase):
    tag = "dependencies"

    def _init(self):
        allowed_children = (NodeDependFile, NodeDependFlag, NodeDependGame, NodeDependencies)
        properties = {"operator": PropertyCombo("Type", ["And", "Or"])}
        self.init("Dependencies", type(self).tag, 1, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeInstallStep(NodeBase):
    tag = "installStep"

    def _init(self):
        allowed_children = (NodeVisible, NodeOptGroups)
        properties = {"name": PropertyText("Name")}
        self.init("Install Step", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeVisible(NodeBase):
    tag = "visible"

    def _init(self):
        allowed_children = (NodeDependFile, NodeDependFlag, NodeDependGame, NodeDependencies)
        self.init("Visibility", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeOptGroups(NodeBase):
    tag = "optionalFileGroups"

    def _init(self):
        allowed_children = (NodeGroup,)
        properties = {"order": PropertyCombo("Order", ["Ascending", "Descending", "Explicit"])}
        self.init("Option Group", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeGroup(NodeBase):
    tag = "group"

    def _init(self):
        allowed_children = (NodePlugins,)
        properties = {"name": PropertyText("Name"),
                      "type": PropertyCombo("Type", ["SelectAny", "SelectAtMostOne",
                                                     "SelectExactlyOne", "SelectAll", "SelectAtLeastOne"])}
        self.init("Group", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodePlugins(NodeBase):
    tag = "plugins"

    def _init(self):
        allowed_children = (NodePlugin,)
        properties = {"order": PropertyCombo("Order", ["Ascending", "Descending", "Explicit"])}
        self.init("Plugins", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodePlugin(NodeBase):
    tag = "plugin"

    def _init(self):
        allowed_children = (NodePluginDescription, NodeImage, NodeFiles, NodeConditionFlags, NodeTypeDesc)
        properties = {"name": PropertyText("Name")}
        self.init("Plugin", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodePluginDescription(NodeBase):
    tag = "description"

    def _init(self):
        self.init("Description", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeImage(NodeBase):
    tag = "image"

    def _init(self):
        properties = {"path": PropertyText("Path")}
        self.init("Image", type(self).tag, 1, properties=properties)
        super()._init()


class NodeConditionFlags(NodeBase):
    tag = "conditionFlags"

    def _init(self):
        allowed_children = (NodeFlag,)
        self.init("Flags", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeTypeDesc(NodeBase):
    tag = "typeDescriptor"

    def _init(self):
        allowed_children = (NodeDependencyType, NodeType)
        self.init("Type Descriptor", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()

    def can_add_child(self, child):
        if super().can_add_child(child):
            if len(self) < 1:
                return True
        return False


class NodeFlag(NodeBase):
    tag = "flag"

    def _init(self):
        properties = {"name": PropertyText("Name")}
        self.init("Flag", type(self).tag, 0, properties=properties, allow_text=True)
        super()._init()


class NodeDependencyType(NodeBase):
    tag = "dependencyType"

    def _init(self):
        allowed_children = (NodeInstallPatterns, NodeDefaultType)
        self.init("Dependency Type", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeDefaultType(NodeBase):
    tag = "defaultType"

    def _init(self):
        properties = {"name": PropertyCombo("Name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}
        self.init("Default Type", type(self).tag, 1, properties=properties)
        super()._init()


class NodeType(NodeBase):
    tag = "type"

    def _init(self):
        properties = {"name": PropertyCombo("Name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}
        self.init("Type", type(self).tag, 1, properties=properties)
        super()._init()


class NodeInstallPatterns(NodeBase):
    tag = "patterns"

    def _init(self):
        allowed_children = (NodeInstallPattern,)
        self.init("Patterns", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeInstallPattern(NodeBase):
    tag = "pattern"

    def _init(self):
        allowed_children = (NodeType, NodeDependencies)
        self.init("Pattern", type(self).tag, 0, allowed_children=allowed_children)
        super()._init()
