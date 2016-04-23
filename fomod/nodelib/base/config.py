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

from .base import _ObjectBase
from .props import PropertyCombo, PropertyInt, PropertyText


class ObjectConfig(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectModName, ObjectModDepend, ObjectInstallSteps,
                            ObjectReqFiles, ObjectCondInstall)

        properties = {"xsi": PropertyText("xsi",
                                          "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation",
                                          "http://qconsulting.ca/fo3/ModConfig5.0.xsd",
                                          False)}

        super().__init__("Config", "config", 1, element, False,
                         allowed_children=allowed_children,
                         properties=properties)


class ObjectModName(_ObjectBase):
    def __init__(self, element=None, text=""):
        super().__init__("Name", "moduleName", 0, element, allow_text=True, default_text=text)


class ObjectModDepend(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectDependFile, ObjectDependFlag)

        super().__init__("Mod Dependencies", "moduleDependencies", 1, element,
                         allowed_children=allowed_children)


class ObjectReqFiles(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectFile, ObjectFolder)

        super().__init__("Mod Requirements", "requiredInstallFiles", 1, element,
                         allowed_children=allowed_children)


class ObjectInstallSteps(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectInstallStep,)

        properties = {"order": PropertyText("Order", "order", "Explicit", False)}

        super().__init__("Installation Steps", "installSteps", 1, element,
                         allowed_children=allowed_children, properties=properties)


class ObjectCondInstall(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectPatterns,)

        super().__init__("Conditional Installation", "conditionalFileInstalls", 1, element,
                         allowed_children=allowed_children)


class ObjectDependFile(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"file": PropertyText("File", "file", ""),
                      "state": PropertyCombo("State", "state", ("Active", "Inactive", "Missing"))}

        super().__init__("File Dependency", "fileDependency", 0, element,
                         properties=properties, default_properties=default_properties)


class ObjectDependFlag(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"flag": PropertyText("Flag", "flag", ""),
                      "value": PropertyText("Value", "value", "")}

        super().__init__("Flag Dependency", "flagDependency", 0, element,
                         properties=properties, default_properties=default_properties)


class ObjectFile(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"source": PropertyText("Source", "source", ""),
                      "destination": PropertyText("Destination", "destination", ""),
                      "priority": PropertyInt("Priority", "priority", 0, 99, 0)}

        super().__init__("File", "file", 0, element,
                         properties=properties, default_properties=default_properties)


class ObjectFolder(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"source": PropertyText("Source", "source", ""),
                      "destination": PropertyText("Destination", "destination", ""),
                      "priority": PropertyInt("Priority", "priority", 0, 99, 0)}

        super().__init__("Folder", "folder", 0, element,
                         properties=properties, default_properties=default_properties)


class ObjectPatterns(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectPattern,)

        super().__init__("Patterns", "patterns", 0, element,
                         allowed_children=allowed_children)


class ObjectPattern(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectFiles, ObjectDependencies)

        super().__init__("Pattern", "pattern", 0, element,
                         allowed_children=allowed_children)


class ObjectFiles(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectFile, ObjectFolder)

        super().__init__("Files", "files", 0, element,
                         allowed_children=allowed_children)


class ObjectDependencies(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (ObjectDependFile, ObjectDependFlag, ObjectDependencies)

        properties = {"operator": PropertyCombo("Type", "operator", ["And", "Or"])}

        super().__init__("Dependencies", "dependencies", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class ObjectInstallStep(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (ObjectVisible, ObjectOptGroups)

        properties = {"name": PropertyText("Name", "name", "")}

        super().__init__("Install Step", "installStep", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class ObjectVisible(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectDependFile, ObjectDependFlag)

        super().__init__("Visibility", "visible", 1, element,
                         allowed_children=allowed_children)


class ObjectOptGroups(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (ObjectGroup,)

        properties = {"order": PropertyCombo("Order", "order", ["Ascending", "Descending", "Explicit"])}

        super().__init__("Option Group", "optionalFileGroups", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class ObjectGroup(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (ObjectPlugins,)

        properties = {"name": PropertyText("Name", "name", ""),
                      "type": PropertyCombo("Type", "type", ["SelectAny", "SelectAtMostOne",
                                                             "SelectExactlyOne", "SelectAll", "SelectAtLeastOne"])}

        super().__init__("Group", "group", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class ObjectPlugins(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (ObjectPlugin,)

        properties = {"order": PropertyCombo("Order", "order", ["Ascending", "Descending", "Explicit"])}

        super().__init__("Plugins", "plugins", 0, element,
                         allowed_children=allowed_children,
                         properties=properties, default_properties=default_properties)


class ObjectPlugin(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        allowed_children = (ObjectPluginDescription, ObjectImage, ObjectFiles,
                            ObjectConditionFlags, ObjectTypeDesc)

        required_children = (ObjectConditionFlags, ObjectFiles)

        properties = {"name": PropertyText("Name", "name", "")}

        super().__init__("Plugin", "plugin", 0, element,
                         allowed_children=allowed_children, properties=properties,
                         required_children=required_children, default_properties=default_properties)


class ObjectPluginDescription(_ObjectBase):
    def __init__(self, element=None, text=""):
        super().__init__("Description", "description", 0, element,
                         allow_text=True, default_text=text)


class ObjectImage(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"path": PropertyText("Path", "path", "")}

        super().__init__("Image", "image", 0, element,
                         properties=properties, default_properties=default_properties)


class ObjectConditionFlags(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectFlag,)

        super().__init__("Flags", "conditionFlags", 0, element,
                         allowed_children=allowed_children)


class ObjectTypeDesc(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectDependencyType, ObjectType)

        super().__init__("Type Descriptor", "typeDescriptor", 0, element,
                         allowed_children=allowed_children,
                         max_children=1)


class ObjectFlag(_ObjectBase):
    def __init__(self, element=None, default_properties=None, text=""):
        properties = {"name": PropertyText("Name", "name", "")}

        super().__init__("Flag", "flag", 0, element,
                         properties=properties, allow_text=True,
                         default_properties=default_properties, default_text=text)


class ObjectDependencyType(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectInstallPatterns, ObjectDefaultType)

        super().__init__("Dependency Type", "dependencyType", 0, element,
                         allowed_children=allowed_children)


class ObjectDefaultType(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"name": PropertyCombo("Name", "name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}

        super().__init__("Default Type", "defaultType", 0, element,
                         properties=properties, default_properties=default_properties)


class ObjectType(_ObjectBase):
    def __init__(self, element=None, default_properties=None):
        properties = {"name": PropertyCombo("Name", "name",
                                            ["Required", "Recommended", "Optional", "CouldBeUsable", "NotUsable"])}

        super().__init__("Type", "type", 0, element,
                         properties=properties, default_properties=default_properties)


class ObjectInstallPatterns(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectInstallPattern,)

        super().__init__("Patterns", "patterns", 0, element,
                         allowed_children=allowed_children)


class ObjectInstallPattern(_ObjectBase):
    def __init__(self, element=None):
        allowed_children = (ObjectType, ObjectDependencies)

        super().__init__("Pattern", "pattern", 0, element,
                         allowed_children=allowed_children)
