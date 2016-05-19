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

from os import listdir, makedirs
from os.path import join
from lxml.etree import (PythonElementClassLookup, XMLParser, tostring, fromstring,
                        Element, SubElement, parse, ParseError, ElementTree, XML)
from lxml.objectify import deannotate
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.html import XmlLexer
from .exceptions import MissingFileError, ParserError, TagNotFound


class _NodeLookup(PythonElementClassLookup):
    def lookup(self, doc, element):
        from . import nodes

        if element.tag == "fomod":
            return nodes.NodeInfoRoot
        elif element.tag == "Name":
            return nodes.NodeInfoName
        elif element.tag == "Author":
            return nodes.NodeInfoAuthor
        elif element.tag == "Version":
            return nodes.NodeInfoVersion
        elif element.tag == "Id":
            return nodes.NodeInfoID
        elif element.tag == "Website":
            return nodes.NodeInfoWebsite
        elif element.tag == "Description":
            return nodes.NodeInfoDescription
        elif element.tag == "Groups":
            return nodes.NodeInfoGroup
        elif element.tag == "element":
            return nodes.NodeInfoElement

        elif element.tag == "config":
            return nodes.NodeConfigRoot
        elif element.tag == "moduleName":
            return nodes.NodeConfigModName
        elif element.tag == "moduleImage":
            return nodes.NodeConfigModImage
        elif element.tag == "moduleDependencies":
            return nodes.NodeConfigModDepend
        elif element.tag == "requiredInstallFiles":
            return nodes.NodeConfigReqFiles
        elif element.tag == "installSteps":
            return nodes.NodeConfigInstallSteps
        elif element.tag == "conditionalFileInstalls":
            return nodes.NodeConfigCondInstall
        elif element.tag == "fileDependency":
            return nodes.NodeConfigDependFile
        elif element.tag == "flagDependency":
            return nodes.NodeConfigDependFlag
        elif element.tag == "gameDependency":
            return nodes.NodeConfigDependGame
        elif element.tag == "file":
            return nodes.NodeConfigFile
        elif element.tag == "folder":
            return nodes.NodeConfigFolder
        elif element.tag == "patterns":
            if element.getparent().tag == "dependencyType":
                return nodes.NodeConfigInstallPatterns
            elif element.getparent().tag == "conditionalFileInstalls":
                return nodes.NodeConfigPatterns
        elif element.tag == "pattern":
            if element.getparent().getparent().tag == "conditionalFileInstalls":
                return nodes.NodeConfigPattern
            elif element.getparent().getparent().tag == "dependencyType":
                return nodes.NodeConfigInstallPattern
        elif element.tag == "files":
            return nodes.NodeConfigFiles
        elif element.tag == "dependencies":
            if element.getparent().tag == "dependencies":
                return nodes.NodeConfigNestedDependencies
            else:
                return nodes.NodeConfigDependencies
        elif element.tag == "installStep":
            return nodes.NodeConfigInstallStep
        elif element.tag == "visible":
            return nodes.NodeConfigVisible
        elif element.tag == "optionalFileGroups":
            return nodes.NodeConfigOptGroups
        elif element.tag == "group":
            return nodes.NodeConfigGroup
        elif element.tag == "plugins":
            return nodes.NodeConfigPlugins
        elif element.tag == "plugin":
            return nodes.NodeConfigPlugin
        elif element.tag == "description":
            return nodes.NodeConfigPluginDescription
        elif element.tag == "image":
            return nodes.NodeConfigImage
        elif element.tag == "conditionFlags":
            return nodes.NodeConfigConditionFlags
        elif element.tag == "typeDescriptor":
            return nodes.NodeConfigTypeDesc
        elif element.tag == "flag":
            return nodes.NodeConfigFlag
        elif element.tag == "dependencyType":
            return nodes.NodeConfigDependencyType
        elif element.tag == "defaultType":
            return nodes.NodeConfigDefaultType
        elif element.tag == "type":
            return nodes.NodeConfigType

        else:
            raise TagNotFound(element)


module_parser = XMLParser(remove_comments=True, remove_pis=True, remove_blank_text=True)
module_parser.set_element_class_lookup(_NodeLookup())


def _check_file(base_path, file_):
    base_file = file_
    try:
        for item in listdir(base_path):
            if item.casefold() == base_file.casefold():
                return item
        raise MissingFileError(base_file)
    except FileNotFoundError:
        raise MissingFileError(base_file)


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


def elem_factory(tag, parent):
    list_ = [parent]
    for elem in parent.iterancestors():
        list_.append(elem)

    list_ = list_[::-1]
    list_[0] = Element(list_[0].tag)
    for elem in list_[1:]:
        list_[list_.index(elem)] = SubElement(list_[list_.index(elem) - 1], elem.tag)
    SubElement(list_[len(list_) - 1], tag)

    root = fromstring(tostring(list_[0]), module_parser)
    parsed_list = []
    for elem in root.iterdescendants():
        parsed_list.append(elem)
    return parsed_list[len(parsed_list) - 1]


def import_(package_path):
    try:
        fomod_folder = _check_file(package_path, "fomod")
        fomod_folder_path = join(package_path, fomod_folder)

        info_file = _check_file(fomod_folder_path, "Info.xml")
        config_file = _check_file(fomod_folder_path, "ModuleConfig.xml")

        info_path = join(fomod_folder_path, info_file)
        config_path = join(fomod_folder_path, config_file)

        info_root = parse(info_path, parser=module_parser).getroot()
        config_root = parse(config_path, parser=module_parser).getroot()

        for root in (info_root, config_root):
            for element in root.iter():
                element.parse_attribs()

                for elem in element:
                    element.model_item.appendRow(elem.model_item)
                    if not _validate_child(elem):
                        element.remove_child(elem)

                element.write_attribs()

    except ParseError as e:
        raise ParserError(str(e))
    except MissingFileError:
        return None, None

    return info_root, config_root


def new():
    from . import nodes

    info_root = module_parser.makeelement(nodes.NodeInfoRoot.tag)
    config_root = module_parser.makeelement(nodes.NodeConfigRoot.tag)

    return info_root, config_root


def export(info_root, config_root, package_path):
    try:
        fomod_folder = _check_file(package_path, "fomod")
    except MissingFileError as e:
        makedirs(join(package_path, e.file))
        fomod_folder = join(package_path, e.file)

    fomod_folder_path = join(package_path, fomod_folder)

    try:
        info_file = _check_file(fomod_folder_path, "Info.xml")
    except MissingFileError as e:
        info_file = e.file

    try:
        config_file = _check_file(fomod_folder_path, "ModuleConfig.xml")
    except MissingFileError as e:
        config_file = e.file

    info_path = join(fomod_folder_path, info_file)
    config_path = join(fomod_folder_path, config_file)

    with open(info_path, "wb") as infofile:
        info_tree = ElementTree(info_root)
        info_tree.write(infofile, pretty_print=True)

    with open(config_path, "wb") as configfile:
        config_tree = ElementTree(config_root)
        config_tree.write(configfile, pretty_print=True)


def highlight_fragment(element):
    element.write_attribs()
    new_elem = XML(tostring(element))
    deannotate(new_elem, cleanup_namespaces=True)
    code = tostring(new_elem, encoding="Unicode", pretty_print=True, xml_declaration=False)
    return highlight(code, XmlLexer(), HtmlFormatter(noclasses=True, style="autumn"))


def sort_elements(info_root, config_root):
    for root in (info_root, config_root):
        for parent in root.xpath('//*[./*]'):
            parent[:] = sorted(parent, key=lambda x: x.sort_order)
