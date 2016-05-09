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

import os
from lxml import etree
from .utility import check_file
from .exceptions import MissingFileError, ParserError
from .base import info, config, base


class NodeLookup(etree.PythonElementClassLookup):
    def lookup(self, doc, element):
        if element.tag == "fomod":
            return info.NodeInfo
        elif element.tag == "Name":
            return info.NodeName
        elif element.tag == "Author":
            return info.NodeAuthor
        elif element.tag == "Version":
            return info.NodeVersion
        elif element.tag == "Id":
            return info.NodeID
        elif element.tag == "Website":
            return info.NodeWebsite
        elif element.tag == "Description":
            return info.NodeDescription
        elif element.tag == "Groups":
            return info.NodeGroup
        elif element.tag == "element":
            return info.NodeElement

        elif element.tag == "config":
            return config.NodeConfig
        elif element.tag == "moduleName":
            return config.NodeModName
        elif element.tag == "moduleImage":
            return config.NodeModImage
        elif element.tag == "moduleDependencies":
            return config.NodeModDepend
        elif element.tag == "requiredInstallFiles":
            return config.NodeReqFiles
        elif element.tag == "installSteps":
            return config.NodeInstallSteps
        elif element.tag == "conditionalFileInstalls":
            return config.NodeCondInstall
        elif element.tag == "fileDependency":
            return config.NodeDependFile
        elif element.tag == "flagDependency":
            return config.NodeDependFlag
        elif element.tag == "gameDependency":
            return config.NodeDependGame
        elif element.tag == "file":
            return config.NodeFile
        elif element.tag == "folder":
            return config.NodeFolder
        elif element.tag == "patterns":
            if element.getparent().tag == "dependencyType":
                return config.NodeInstallPatterns
            elif element.getparent().tag == "conditionalFileInstalls":
                return config.NodePatterns
        elif element.tag == "pattern":
            if element.getparent().getparent().tag == "conditionalFileInstalls":
                return config.NodePattern
            elif element.getparent().getparent().tag == "dependencyType":
                return config.NodeInstallPattern
        elif element.tag == "files":
            return config.NodeFiles
        elif element.tag == "dependencies":
            return config.NodeDependencies
        elif element.tag == "installStep":
            return config.NodeInstallStep
        elif element.tag == "visible":
            return config.NodeVisible
        elif element.tag == "optionalFileGroups":
            return config.NodeOptGroups
        elif element.tag == "group":
            return config.NodeGroup
        elif element.tag == "plugins":
            return config.NodePlugins
        elif element.tag == "plugin":
            return config.NodePlugin
        elif element.tag == "description":
            return config.NodePluginDescription
        elif element.tag == "image":
            return config.NodeImage
        elif element.tag == "conditionFlags":
            return config.NodeConditionFlags
        elif element.tag == "typeDescriptor":
            return config.NodeTypeDesc
        elif element.tag == "flag":
            return config.NodeFlag
        elif element.tag == "dependencyType":
            return config.NodeDependencyType
        elif element.tag == "defaultType":
            return config.NodeDefaultType
        elif element.tag == "type":
            return config.NodeType

        else:
            return base.NodeBase


def import_(package_path):
    try:
        fomod_folder = check_file(package_path, "fomod")
        fomod_folder_path = os.path.join(package_path, fomod_folder)

        info_file = check_file(fomod_folder_path, "Info.xml")
        config_file = check_file(fomod_folder_path, "ModuleConfig.xml")

        info_path = os.path.join(fomod_folder_path, info_file)
        config_path = os.path.join(fomod_folder_path, config_file)

        parser = etree.XMLParser(remove_comments=True, remove_pis=True, remove_blank_text=True)
        parser.set_element_class_lookup(NodeLookup())
        info_root = etree.parse(info_path, parser=parser).getroot()
        config_root = etree.parse(config_path, parser=parser).getroot()

        for root in (info_root, config_root):
            for element in root.iter():
                element.parse_attribs()

                for elem in element:
                    if _validate_child(elem):
                        element.model_item.appendRow(elem.model_item)

    except etree.ParseError as e:
        raise ParserError(str(e))
    except MissingFileError:
        return None, None

    return info_root, config_root


def new():
    from .base import info, config

    return info.NodeInfo(), config.NodeConfig()


def _validate_child(child):
    if type(child) in child.getparent().allowed_children:
        if child.allowed_instances:
            instances = 0
            for item in child.getparent():
                if type(item) == type(child):
                    instances += 1
            if instances <= child.allowed_instances:
                return True
        else:
            return True
    return False
