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

from . import info, config
from .exceptions import FactoryTagNotFound


def from_element(element):
    if element.tag == "fomod" and not element.getparent():
        return info.ObjectInfo(element)
    elif element.tag == "Name":
        return info.ObjectName(element, element.text)
    elif element.tag == "Author":
        return info.ObjectAuthor(element, element.text)
    elif element.tag == "Version":
        return info.ObjectVersion(element, element.text)
    elif element.tag == "Id":
        return info.ObjectID(element, element.text)
    elif element.tag == "Website":
        return info.ObjectWebsite(element, element.text)
    elif element.tag == "Description":
        return info.ObjectDescription(element, element.text)
    elif element.tag == "Groups":
        return info.ObjectGroup(element)
    elif element.tag == "element":
        return info.ObjectElement(element, element.text)

    elif element.tag == "config" and not element.getparent():
        return config.ObjectConfig(element)
    elif element.tag == "moduleName":
        return config.ObjectModName(element, element.text)
    elif element.tag == "moduleDependencies":
        return config.ObjectModDepend(element)
    elif element.tag == "requiredInstallFiles":
        return config.ObjectReqFiles(element)
    elif element.tag == "installSteps":
        return config.ObjectInstallSteps(element)
    elif element.tag == "conditionalFileInstalls":
        return config.ObjectCondInstall(element)
    elif element.tag == "fileDependency":
        return config.ObjectDependFile(element, dict(element.attrib))
    elif element.tag == "flagDependency":
        return config.ObjectDependFlag(element, dict(element.attrib))
    elif element.tag == "file":
        return config.ObjectFile(element, dict(element.attrib))
    elif element.tag == "folder":
        return config.ObjectFolder(element, dict(element.attrib))
    elif element.tag == "patterns":
        if element.getparent().tag == "dependencyType":
            return config.ObjectInstallPatterns(element)
        elif element.getparent().tag == "conditionalFileInstalls":
            return config.ObjectPatterns(element)
    elif element.tag == "pattern":
        if element.getparent().getparent().tag == "conditionalFileInstalls":
            return config.ObjectPattern(element)
        elif element.getparent().getparent().tag == "dependencyType":
            return config.ObjectInstallPattern(element)
    elif element.tag == "files":
        return config.ObjectFiles(element)
    elif element.tag == "dependencies":
        return config.ObjectDependencies(element, dict(element.attrib))
    elif element.tag == "installStep":
        return config.ObjectInstallStep(element, dict(element.attrib))
    elif element.tag == "visible":
        return config.ObjectVisible(element)
    elif element.tag == "optionalFileGroups":
        return config.ObjectOptGroups(element, dict(element.attrib))
    elif element.tag == "group":
        return config.ObjectGroup(element, dict(element.attrib))
    elif element.tag == "plugins":
        return config.ObjectPlugins(element, dict(element.attrib))
    elif element.tag == "plugin":
        return config.ObjectPlugin(element, dict(element.attrib))
    elif element.tag == "description":
        return config.ObjectPluginDescription(element, element.text)
    elif element.tag == "image":
        return config.ObjectImage(element, dict(element.attrib))
    elif element.tag == "conditionFlags":
        return config.ObjectConditionFlags(element)
    elif element.tag == "typeDescriptor":
        return config.ObjectTypeDesc(element)
    elif element.tag == "flag":
        return config.ObjectFlag(element, dict(element.attrib), element.text)
    elif element.tag == "dependencyType":
        return config.ObjectDependencyType(element)
    elif element.tag == "defaultType":
        return config.ObjectDefaultType(element, dict(element.attrib))
    elif element.tag == "type":
        return config.ObjectType(element, dict(element.attrib))

    raise FactoryTagNotFound(element.tag)
