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
        return info.NodeInfo(element)
    elif element.tag == "Name":
        return info.NodeName(element, element.text)
    elif element.tag == "Author":
        return info.NodeAuthor(element, element.text)
    elif element.tag == "Version":
        return info.NodeVersion(element, element.text)
    elif element.tag == "Id":
        return info.NodeID(element, element.text)
    elif element.tag == "Website":
        return info.NodeWebsite(element, element.text)
    elif element.tag == "Description":
        return info.NodeDescription(element, element.text)
    elif element.tag == "Groups":
        return info.NodeGroup(element)
    elif element.tag == "element":
        return info.NodeElement(element, element.text)

    elif element.tag == "config" and not element.getparent():
        return config.NodeConfig(element)
    elif element.tag == "moduleName":
        return config.NodeModName(element, element.text)
    elif element.tag == "moduleDependencies":
        return config.NodeModDepend(element)
    elif element.tag == "requiredInstallFiles":
        return config.NodeReqFiles(element)
    elif element.tag == "installSteps":
        return config.NodeInstallSteps(element)
    elif element.tag == "conditionalFileInstalls":
        return config.NodeCondInstall(element)
    elif element.tag == "fileDependency":
        return config.NodeDependFile(element, dict(element.attrib))
    elif element.tag == "flagDependency":
        return config.NodeDependFlag(element, dict(element.attrib))
    elif element.tag == "file":
        return config.NodeFile(element, dict(element.attrib))
    elif element.tag == "folder":
        return config.NodeFolder(element, dict(element.attrib))
    elif element.tag == "patterns":
        if element.getparent().tag == "dependencyType":
            return config.NodeInstallPatterns(element)
        elif element.getparent().tag == "conditionalFileInstalls":
            return config.NodePatterns(element)
    elif element.tag == "pattern":
        if element.getparent().getparent().tag == "conditionalFileInstalls":
            return config.NodePattern(element)
        elif element.getparent().getparent().tag == "dependencyType":
            return config.NodeInstallPattern(element)
    elif element.tag == "files":
        return config.NodeFiles(element)
    elif element.tag == "dependencies":
        return config.NodeDependencies(element, dict(element.attrib))
    elif element.tag == "installStep":
        return config.NodeInstallStep(element, dict(element.attrib))
    elif element.tag == "visible":
        return config.NodeVisible(element)
    elif element.tag == "optionalFileGroups":
        return config.NodeOptGroups(element, dict(element.attrib))
    elif element.tag == "group":
        return config.NodeGroup(element, dict(element.attrib))
    elif element.tag == "plugins":
        return config.NodePlugins(element, dict(element.attrib))
    elif element.tag == "plugin":
        return config.NodePlugin(element, dict(element.attrib))
    elif element.tag == "description":
        return config.NodePluginDescription(element, element.text)
    elif element.tag == "image":
        return config.NodeImage(element, dict(element.attrib))
    elif element.tag == "conditionFlags":
        return config.NodeConditionFlags(element)
    elif element.tag == "typeDescriptor":
        return config.NodeTypeDesc(element)
    elif element.tag == "flag":
        return config.NodeFlag(element, dict(element.attrib), element.text)
    elif element.tag == "dependencyType":
        return config.NodeDependencyType(element)
    elif element.tag == "defaultType":
        return config.NodeDefaultType(element, dict(element.attrib))
    elif element.tag == "type":
        return config.NodeType(element, dict(element.attrib))

    raise FactoryTagNotFound(element.tag)
