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
    def __init__(self, element=None):
        allowed_children = (NodeModName, NodeModDepend, NodeInstallSteps,
                            NodeReqFiles, NodeCondInstall)

        properties = {"xsi": PropertyText("xsi",
                                          "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation",
                                          "http://qconsulting.ca/fo3/ModConfig5.0.xsd",
                                          False)}

        super().__init__("Config", "config", 1, element, False,
                         allowed_children=allowed_children,
                         properties=properties)


class NodeModName(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Name", "moduleName", 0, element, allow_text=True, default_text=text)


class NodeModDepend(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeDependFile, NodeDependFlag)

        super().__init__("Mod Dependencies", "moduleDependencies", 1, element,
                         allowed_children=allowed_children)


class NodeReqFiles(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeFile, NodeFolder)

        super().__init__("Mod Requirements", "requiredInstallFiles", 1, element,
                         allowed_children=allowed_children)


class NodeInstallSteps(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeInstallStep,)

        properties = {"order": PropertyText("Order", "order", "Explicit", False)}

        super().__init__("Installation Steps", "installSteps", 1, element,
                         allowed_children=allowed_children, properties=properties)


class NodeCondInstall(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodePatterns,)

        super().__init__("Conditional Installation", "conditionalFileInstalls", 1, element,
                         allowed_children=allowed_children)


class NodeDependFile(NodeBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"file": PropertyText("File", "file", ""),
                      "state": PropertyCombo("State", "state", ("Active", "Inactive", "Missing"))}

        super().__init__("File Dependency", "fileDependency", 0, element,
                         properties=properties, default_properties=default_properties)


class NodeDependFlag(NodeBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"flag": PropertyText("Flag", "flag", ""),
                      "value": PropertyText("Value", "value", "")}

        super().__init__("Flag Dependency", "flagDependency", 0, element,
                         properties=properties, default_properties=default_properties)


class NodeFile(NodeBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"source": PropertyText("Source", "source", ""),
                      "destination": PropertyText("Destination", "destination", ""),
                      "priority": PropertyInt("Priority", "priority", 0, 99, 0)}

        super().__init__("File", "file", 0, element,
                         properties=properties, default_properties=default_properties)


class NodeFolder(NodeBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"source": PropertyText("Source", "source", ""),
                      "destination": PropertyText("Destination", "destination", ""),
                      "priority": PropertyInt("Priority", "priority", 0, 99, 0)}

        super().__init__("Folder", "folder", 0, element,
                         properties=properties, default_properties=default_properties)


class NodePatterns(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodePattern,)

        super().__init__("Patterns", "patterns", 0, element,
                         allowed_children=allowed_children)


class NodePattern(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeFiles, NodeDependencies)

        super().__init__("Pattern", "pattern", 0, element,
                         allowed_children=allowed_children)


class NodeFiles(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeFile, NodeFolder)

        super().__init__("Files", "files", 0, element,
                         allowed_children=allowed_children)


class NodeDependencies(NodeBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (NodeDependFile, NodeDependFlag, NodeDependencies)

        properties = {"operator": PropertyCombo("Type", "operator", ["And", "Or"])}

        super().__init__("Dependencies", "dependencies", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class NodeInstallStep(NodeBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (NodeVisible, NodeOptGroups)

        properties = {"name": PropertyText("Name", "name", "")}

        super().__init__("Install Step", "installStep", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class NodeVisible(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeDependFile, NodeDependFlag)

        super().__init__("Visibility", "visible", 1, element,
                         allowed_children=allowed_children)


class NodeOptGroups(NodeBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (NodeGroup,)

        properties = {"order": PropertyCombo("Order", "order", ["Ascending", "Descending", "Explicit"])}

        super().__init__("Option Group", "optionalFileGroups", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class NodeGroup(NodeBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (NodePlugins,)

        properties = {"name": PropertyText("Name", "name", ""),
                      "type": PropertyCombo("Type", "type", ["SelectAny", "SelectAtMostOne",
                                                             "SelectExactlyOne", "SelectAll", "SelectAtLeastOne"])}

        super().__init__("Group", "group", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class NodePlugins(NodeBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (NodePlugin,)

        properties = {"order": PropertyCombo("Order", "order", ["Ascending", "Descending", "Explicit"])}

        super().__init__("Plugins", "plugins", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class NodePlugin(NodeBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (NodePluginDescription, NodeImage, NodeFiles,
                            NodeConditionFlags, NodeTypeDesc)

        required_children = (NodeConditionFlags, NodeFiles)

        properties = {"name": PropertyText("Name", "name", "")}

        super().__init__("Plugin", "plugin", 0, element,
                         allowed_children=allowed_children, properties=properties,
                         required_children=required_children, default_properties=default_properties)


class NodePluginDescription(NodeBase):
    def __init__(self, element=None, text=""):
        super().__init__("Description", "description", 0, element,
                         allow_text=True, default_text=text)


class NodeImage(NodeBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"path": PropertyText("Path", "path", "")}

        super().__init__("Image", "image", 0, element,
                         properties=properties, default_properties=default_properties)


class NodeConditionFlags(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeFlag,)

        super().__init__("Flags", "conditionFlags", 0, element,
                         allowed_children=allowed_children)


class NodeTypeDesc(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeDependencyType, NodeType)

        super().__init__("Type Descriptor", "typeDescriptor", 0, element,
                         allowed_children=allowed_children,
                         max_children=1)


class NodeFlag(NodeBase):
    def __init__(self, element=None, default_properties=None, text=""):
        properties = {"name": PropertyText("Name", "name", "")}

        super().__init__("Flag", "flag", 0, element,
                         properties=properties, allow_text=True,
                         default_properties=default_properties, default_text=text)


class NodeDependencyType(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeInstallPatterns, NodeDefaultType)

        super().__init__("Dependency Type", "dependencyType", 0, element,
                         allowed_children=allowed_children)


class NodeDefaultType(NodeBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"name": PropertyCombo("Name", "name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}

        super().__init__("Default Type", "defaultType", 0, element,
                         properties=properties, default_properties=default_properties)


class NodeType(NodeBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"name": PropertyCombo("Name", "name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}

        super().__init__("Type", "type", 0, element,
                         properties=properties, default_properties=default_properties)


class NodeInstallPatterns(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeInstallPattern,)

        super().__init__("Patterns", "patterns", 0, element,
                         allowed_children=allowed_children)


class NodeInstallPattern(NodeBase):
    def __init__(self, element=None):
        allowed_children = (NodeType, NodeDependencies)

        super().__init__("Pattern", "pattern", 0, element,
                         allowed_children=allowed_children)
