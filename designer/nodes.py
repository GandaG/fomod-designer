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

from os import sep
from PyQt5.QtGui import QStandardItem
from lxml import etree
from .wizards import WizardFiles
from .props import PropertyCombo, PropertyInt, PropertyText, PropertyFile, PropertyFolder, PropertyColour
from .exceptions import BaseInstanceException


class _NodeBase(etree.ElementBase):
    """
    The base class for all nodes. Should never be instantiated directly.
    """
    def _init(self):
        if type(self) is _NodeBase:
            raise BaseInstanceException(self)
        super()._init()

    def init(self, name, tag, allowed_instances, sort_order=0, allow_text=False, allowed_children=None, properties=None,
             wizard=None):

        if not properties:
            properties = {}
        if not allowed_children:
            allowed_children = ()

        self.name = name
        self.tag = tag
        self.sort_order = sort_order
        self.properties = properties
        self.allowed_children = allowed_children
        self.allow_text = allow_text
        self.allowed_instances = allowed_instances
        self.wizard = wizard

        self.model_item = NodeStandardItem(self)
        self.model_item.setText(self.name)
        self.model_item.setEditable(False)

    def can_add_child(self, child):
        """
        Checks if the given child can be added to this node.

        :param child: The child to check.
        :return: True if possible, False if not.
        """
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
        """
        Adds the given child to this node. Includes a check with can_add_child at the start.

        :param child: The child to add.
        """
        if self.can_add_child(child):
            self.append(child)
            self.model_item.appendRow(child.model_item)
            child.write_attribs()

    def remove_child(self, child):
        """
        Removes the given child from this node.

        :param child: The child to remove.
        """
        if child in self:
            self.model_item.takeRow(child.model_item.row())
            self.remove(child)

    def parse_attribs(self):
        """
        Reads the values from the BaseElement's attrib dictionary into the node's properties.
        """
        for key in self.properties:
            if key not in self.attrib.keys():
                continue
            self.properties[key].set_value(self.attrib[key])
        self.update_item_name()

    def write_attribs(self):
        """
        Writes the values from the node's properties into the BaseElement's attrib dictionary.
        """
        self.attrib.clear()
        for key in self.properties:
            self.set(key, str(self.properties[key].value))

    def update_item_name(self):
        """
        Updates this node's item's display name.

        If the node contains a property called "name" then it uses its value for the display.
        If it contains a property called "source" then it expects a path and uses the last part of the path.
        """
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
        """
        Method used to set the node's text, if allowed.

        :param text: The text to set.
        """
        if self.allow_text:
            self.text = text


class NodeStandardItem(QStandardItem):
    """A Standard Item but with an added reference to a xml node."""
    def __init__(self, node):
        self.xml_node = node
        super().__init__()


class NodeInfoRoot(_NodeBase):
    """
    A node for the tag fomod
    """
    tag = "fomod"

    def _init(self):
        allowed_children = (NodeInfoName, NodeInfoAuthor, NodeInfoDescription,
                            NodeInfoID, NodeInfoGroup, NodeInfoVersion, NodeInfoWebsite)
        self.init("Info", type(self).tag, 1, allow_text=False, allowed_children=allowed_children)
        super()._init()


class NodeInfoName(_NodeBase):
    """
    A node for the tag Name
    """
    tag = "Name"

    def _init(self):
        self.init("Name", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeInfoAuthor(_NodeBase):
    """
    A node for the tag Author
    """
    tag = "Author"

    def _init(self):
        self.init("Author", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeInfoVersion(_NodeBase):
    """
    A node for the tag Version
    """
    tag = "Version"

    def _init(self):
        self.init("Version", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeInfoID(_NodeBase):
    """
    A node for the tag Id
    """
    tag = "Id"

    def _init(self):
        self.init("ID", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeInfoWebsite(_NodeBase):
    """
    A node for the tag Website
    """
    tag = "Website"

    def _init(self):
        self.init("Website", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeInfoDescription(_NodeBase):
    """
    A node for the tag Description
    """
    tag = "Description"

    def _init(self):
        self.init("Description", type(self).tag, 1, allow_text=True)
        super()._init()


class NodeInfoGroup(_NodeBase):
    """
    A node for the tag Groups
    """
    tag = "Groups"

    def _init(self):
        allowed_child = (NodeInfoElement,)
        self.init("Categories Group", type(self).tag, 1, allowed_children=allowed_child)
        super()._init()


class NodeInfoElement(_NodeBase):
    """
    A node for the tag element
    """
    tag = "element"

    def _init(self):
        self.init("Category", type(self).tag, 0, allow_text=True)
        super()._init()


class NodeConfigRoot(_NodeBase):
    """
    A node for the tag config
    """
    tag = "config"

    def _init(self):
        allowed_children = (NodeConfigModName, NodeConfigModImage, NodeConfigModDepend,
                            NodeConfigInstallSteps, NodeConfigReqFiles, NodeConfigCondInstall)
        properties = {"{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation":
                      PropertyText("xsi", "http://qconsulting.ca/fo3/ModConfig5.0.xsd", False)}
        self.init("Config", type(self).tag, 1, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeConfigModName(_NodeBase):
    """
    A node for the tag moduleName
    """
    tag = "moduleName"

    def _init(self):
        properties = {"position": PropertyCombo("Position", ("Left", "Right", "RightOfImage")),
                      "colour": PropertyColour("Colour", "000000")}
        self.init("Name", type(self).tag, 1, allow_text=True, properties=properties, sort_order=1)
        super()._init()


class NodeConfigModImage(_NodeBase):
    """
    A node for the tag moduleImage
    """
    tag = "moduleImage"

    def _init(self):
        properties = {"path": PropertyFile("Path"), "showImage": PropertyCombo("Show Image", ("true", "false")),
                      "showFade": PropertyCombo("Show Fade", ("true", "false")),
                      "height": PropertyInt("Height", -1, 9999, -1)}
        self.init("Image", "moduleImage", 1, properties=properties, sort_order=2)
        super()._init()


class NodeConfigModDepend(_NodeBase):
    """
    A node for the tag moduleDependencies
    """
    tag = "moduleDependencies"

    def _init(self):
        allowed_children = (NodeConfigDependFile, NodeConfigDependFlag, NodeConfigDependGame)
        properties = {"operator": PropertyCombo("Type", ["And", "Or"])}
        self.init("Mod Dependencies", type(self).tag, 1, allowed_children=allowed_children,
                  properties=properties, sort_order=3)
        super()._init()


class NodeConfigReqFiles(_NodeBase):
    """
    A node for the tag requiredInstallFiles
    """
    tag = "requiredInstallFiles"

    def _init(self):
        allowed_children = (NodeConfigFile, NodeConfigFolder)
        self.init("Mod Requirements", type(self).tag, 1, allowed_children=allowed_children,
                  sort_order=4, wizard=WizardFiles)
        super()._init()


class NodeConfigInstallSteps(_NodeBase):
    """
    A node for the tag installSteps
    """
    tag = "installSteps"

    def _init(self):
        allowed_children = (NodeConfigInstallStep,)
        properties = {"order": PropertyCombo("Order", ["Ascending", "Descending", "Explicit"])}
        self.init("Installation Steps", type(self).tag, 1, allowed_children=allowed_children,
                  properties=properties, sort_order=5)
        super()._init()


class NodeConfigCondInstall(_NodeBase):
    """
    A node for the tag conditionalFileInstalls
    """
    tag = "conditionalFileInstalls"

    def _init(self):
        allowed_children = (NodeConfigPatterns,)
        self.init("Conditional Installation", type(self).tag, 1, allowed_children=allowed_children, sort_order=6)
        super()._init()


class NodeConfigDependFile(_NodeBase):
    """
    A node for the tag fileDependency
    """
    tag = "fileDependency"

    def _init(self):
        properties = {"file": PropertyText("File"),
                      "state": PropertyCombo("State", ("Active", "Inactive", "Missing"))}
        self.init("File Dependency", type(self).tag, 0, properties=properties)
        super()._init()


class NodeConfigDependFlag(_NodeBase):
    """
    A node for the tag flagDependency
    """
    tag = "flagDependency"

    def _init(self):
        properties = {"flag": PropertyText("Flag"), "value": PropertyText("Value")}
        self.init("Flag Dependency", type(self).tag, 0, properties=properties)
        super()._init()


class NodeConfigDependGame(_NodeBase):
    """
    A node for the tag gameDependency
    """
    tag = "gameDependency"

    def _init(self):
        properties = {"version": PropertyText("Version")}
        self.init("Game Dependency", "gameDependency", 1, properties=properties)
        super()._init()


class NodeConfigFile(_NodeBase):
    """
    A node for the tag file
    """
    tag = "file"

    def _init(self):
        properties = {"source": PropertyFile("Source"),
                      "destination": PropertyText("Destination"),
                      "priority": PropertyInt("Priority", 0, 99, 0),
                      "alwaysInstall": PropertyCombo("Always Install", ("false", "true")),
                      "installIfUsable": PropertyCombo("Install If Usable", ("false", "true"))}
        self.init("File", type(self).tag, 0, properties=properties)
        super()._init()


class NodeConfigFolder(_NodeBase):
    """
    A node for the tag folder
    """
    tag = "folder"

    def _init(self):
        properties = {"source": PropertyFolder("Source"),
                      "destination": PropertyText("Destination"),
                      "priority": PropertyInt("Priority", 0, 99, 0),
                      "alwaysInstall": PropertyCombo("Always Install", ("false", "true")),
                      "installIfUsable": PropertyCombo("Install If Usable", ("false", "true"))}
        self.init("Folder", type(self).tag, 0, properties=properties)
        super()._init()


class NodeConfigPatterns(_NodeBase):
    """
    A node for the tag patterns
    """
    tag = "patterns"

    def _init(self):
        allowed_children = (NodeConfigPattern,)
        self.init("Patterns", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeConfigPattern(_NodeBase):
    """
    A node for the tag pattern
    """
    tag = "pattern"

    def _init(self):
        allowed_children = (NodeConfigFiles, NodeConfigDependencies)
        self.init("Pattern", type(self).tag, 0, allowed_children=allowed_children)
        super()._init()


class NodeConfigFiles(_NodeBase):
    """
    A node for the tag files
    """
    tag = "files"

    def _init(self):
        allowed_children = (NodeConfigFile, NodeConfigFolder)
        self.init("Files", type(self).tag, 1, allowed_children=allowed_children, sort_order=3, wizard=WizardFiles)
        super()._init()


class NodeConfigDependencies(_NodeBase):
    """
    A node for the tag dependencies
    """
    tag = "dependencies"

    def _init(self):
        allowed_children = (NodeConfigDependFile, NodeConfigDependFlag,
                            NodeConfigDependGame, NodeConfigNestedDependencies)
        properties = {"operator": PropertyCombo("Type", ["And", "Or"])}
        self.init("Dependencies", type(self).tag, 1, allowed_children=allowed_children,
                  properties=properties, sort_order=1)
        super()._init()


class NodeConfigNestedDependencies(_NodeBase):
    """
    A node for the tag dependencies (this one refers to the all the dependencies that have a dependencies as a parent).
    """
    tag = "dependencies"

    def _init(self):
        allowed_children = (NodeConfigDependFile, NodeConfigDependFlag,
                            NodeConfigDependGame, NodeConfigNestedDependencies)
        properties = {"operator": PropertyCombo("Type", ["And", "Or"])}
        self.init("Dependencies", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeConfigInstallStep(_NodeBase):
    """
    A node for the tag installStep
    """
    tag = "installStep"

    def _init(self):
        allowed_children = (NodeConfigVisible, NodeConfigOptGroups)
        properties = {"name": PropertyText("Name")}
        self.init("Install Step", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeConfigVisible(_NodeBase):
    """
    A node for the tag visible
    """
    tag = "visible"

    def _init(self):
        allowed_children = (NodeConfigDependFile, NodeConfigDependFlag, NodeConfigDependGame, NodeConfigDependencies)
        self.init("Visibility", type(self).tag, 1, allowed_children=allowed_children, sort_order=1)
        super()._init()


class NodeConfigOptGroups(_NodeBase):
    """
    A node for the tag optionalFileGroups
    """
    tag = "optionalFileGroups"

    def _init(self):
        allowed_children = (NodeConfigGroup,)
        properties = {"order": PropertyCombo("Order", ["Ascending", "Descending", "Explicit"])}
        self.init("Option Group", type(self).tag, 0, allowed_children=allowed_children,
                  properties=properties, sort_order=2)
        super()._init()


class NodeConfigGroup(_NodeBase):
    """
    A node for the tag group
    """
    tag = "group"

    def _init(self):
        allowed_children = (NodeConfigPlugins,)
        properties = {"name": PropertyText("Name"),
                      "type": PropertyCombo("Type", ["SelectAny", "SelectAtMostOne",
                                                     "SelectExactlyOne", "SelectAll", "SelectAtLeastOne"])}
        self.init("Group", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeConfigPlugins(_NodeBase):
    """
    A node for the tag plugins
    """
    tag = "plugins"

    def _init(self):
        allowed_children = (NodeConfigPlugin,)
        properties = {"order": PropertyCombo("Order", ["Ascending", "Descending", "Explicit"])}
        self.init("Plugins", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeConfigPlugin(_NodeBase):
    """
    A node for the tag plugin
    """
    tag = "plugin"

    def _init(self):
        allowed_children = (NodeConfigPluginDescription, NodeConfigImage, NodeConfigFiles,
                            NodeConfigConditionFlags, NodeConfigTypeDesc)
        properties = {"name": PropertyText("Name")}
        self.init("Plugin", type(self).tag, 0, allowed_children=allowed_children, properties=properties)
        super()._init()


class NodeConfigPluginDescription(_NodeBase):
    """
    A node for the tag description
    """
    tag = "description"

    def _init(self):
        self.init("Description", type(self).tag, 1, allow_text=True, sort_order=1)
        super()._init()


class NodeConfigImage(_NodeBase):
    """
    A node for the tag image
    """
    tag = "image"

    def _init(self):
        properties = {"path": PropertyFile("Path")}
        self.init("Image", type(self).tag, 1, properties=properties, sort_order=2)
        super()._init()


class NodeConfigConditionFlags(_NodeBase):
    """
    A node for the tag conditionFlags
    """
    tag = "conditionFlags"

    def _init(self):
        allowed_children = (NodeConfigFlag,)
        self.init("Flags", type(self).tag, 1, allowed_children=allowed_children, sort_order=3)
        super()._init()


class NodeConfigTypeDesc(_NodeBase):
    """
    A node for the tag typeDescriptor
    """
    tag = "typeDescriptor"

    def _init(self):
        allowed_children = (NodeConfigDependencyType, NodeConfigType)
        self.init("Type Descriptor", type(self).tag, 1, allowed_children=allowed_children, sort_order=4)
        super()._init()

    def can_add_child(self, child):
        if super().can_add_child(child):
            if len(self) < 1:
                return True
        return False


class NodeConfigFlag(_NodeBase):
    """
    A node for the tag flag
    """
    tag = "flag"

    def _init(self):
        properties = {"name": PropertyText("Name")}
        self.init("Flag", type(self).tag, 0, properties=properties, allow_text=True)
        super()._init()


class NodeConfigDependencyType(_NodeBase):
    """
    A node for the tag dependencyType
    """
    tag = "dependencyType"

    def _init(self):
        allowed_children = (NodeConfigInstallPatterns, NodeConfigDefaultType)
        self.init("Dependency Type", type(self).tag, 1, allowed_children=allowed_children)
        super()._init()


class NodeConfigDefaultType(_NodeBase):
    """
    A node for the tag defaultType
    """
    tag = "defaultType"

    def _init(self):
        properties = {"name": PropertyCombo("Name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}
        self.init("Default Type", type(self).tag, 1, properties=properties, sort_order=1)
        super()._init()


class NodeConfigType(_NodeBase):
    """
    A node for the tag type
    """
    tag = "type"

    def _init(self):
        properties = {"name": PropertyCombo("Name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}
        self.init("Type", type(self).tag, 1, properties=properties, sort_order=2)
        super()._init()


class NodeConfigInstallPatterns(_NodeBase):
    """
    A node for the tag patterns
    """
    tag = "patterns"

    def _init(self):
        allowed_children = (NodeConfigInstallPattern,)
        self.init("Patterns", type(self).tag, 1, allowed_children=allowed_children, sort_order=2)
        super()._init()


class NodeConfigInstallPattern(_NodeBase):
    """
    A node for the tag pattern
    """
    tag = "pattern"

    def _init(self):
        allowed_children = (NodeConfigType, NodeConfigDependencies)
        self.init("Pattern", type(self).tag, 0, allowed_children=allowed_children)
        super()._init()
