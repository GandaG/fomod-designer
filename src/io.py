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

from os import listdir, makedirs, rename
from os.path import join
from lxml.etree import (PythonElementClassLookup, XMLParser, tostring, fromstring, CommentBase, Comment,
                        Element, SubElement, parse, ParseError, ElementTree, CustomElementClassLookup)
from .exceptions import MissingFileError, ParserError

module_parser = XMLParser(remove_pis=True, remove_blank_text=True)


class _CommentLookup(CustomElementClassLookup):
    def lookup(self, elem_type, doc, namespace, name):
        from .nodes import NodeComment

        if elem_type == "comment":
            return NodeComment
        else:
            return None


class _NodeClassLookup(PythonElementClassLookup):
    """
    Class that handles the custom lookup for the element factories.
    """
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
            if element.getparent().tag == "dependencies" or \
                    element.getparent().tag == "moduleDependencies" or \
                    element.getparent().tag == "visible":
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
            raise AssertionError("Tag {} at line {} could not be matched.".format(element.tag, element.sourceline))


module_parser.set_element_class_lookup(_CommentLookup(_NodeClassLookup()))


def _check_file(base_path, file_):
    """
    Function used to search case-insensitively for a file/folder is a given path.

    :param base_path: The path to search for the file/folder in.
    :param file_: The file/folder to search for.
    :return: The file if found, raises an exception if not.
    """
    base_file = file_
    try:
        for item in listdir(base_path):
            if item.casefold() == base_file.casefold():
                return item
        raise MissingFileError(base_file)
    except FileNotFoundError:
        raise MissingFileError(base_file)


def _validate_child(child):
    """
    Function used during installer import to check if each element's children is valid.

    :param child: The child to check.
    :return: True if valid, False if not.
    """
    if type(child) in child.getparent().allowed_children or child.tag is Comment:
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


def node_factory(tag, parent=None):
    """
    Function meant as a replacement for the default element factory.

    Creates a tree up to the root, re-parses that tree and returns an element corresponding to the tag given.
    This is necessary due to the way the _NodeLookup class works when checking for tags
    (it requires parents and grandparents).

    :param tag: The tag to create an element from.
    :param parent: The parent of the future element.
    :return: The created element with the tag *tag*.
    """
    if tag is Comment:
        from .nodes import NodeComment
        return NodeComment()
    elif parent is not None:
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
    else:
        return module_parser.makeelement(tag)


def copy_node(node, parent=None):
    if parent is None:
        parent = node.getparent()
    result = node_factory(node.tag, parent)
    result.text = node.text
    for key in node.keys():
        result.set(key, node.get(key))
    result.parse_attribs()
    for child in node:
        if child.tag is Comment:
            result.append(CommentBase(child.text))
        else:
            new_child = copy_node(child)
            result.add_child(new_child)
    result.load_metadata()
    return result


def import_(package_path):
    """
    Function used to import an existing installer from *package_path*.

    Raises ``ParserError`` if the lxml parser could not read a file.

    :param package_path: The package where the installer is.
    :return: The root elements of each installer file. A tuple of None, None if any file is missing.
    """
    try:
        fomod_folder = _check_file(package_path, "fomod")
        fomod_folder_path = join(package_path, fomod_folder)

        info_file = _check_file(fomod_folder_path, "Info.xml")
        config_file = _check_file(fomod_folder_path, "ModuleConfig.xml")

        info_path = join(fomod_folder_path, info_file)
        config_path = join(fomod_folder_path, config_file)
        rename(info_path, info_path)
        rename(config_path, config_path)  # check if another app is using these files

        info_root = parse(info_path, parser=module_parser).getroot()
        config_root = parse(config_path, parser=module_parser).getroot()

        for root in (info_root, config_root):
            root.sort()
            root.model_item.sortChildren(0)
            for element in root.iter():
                element.parse_attribs()

                for elem in element:
                    element.model_item.appendRow(elem.model_item)
                    if not _validate_child(elem):
                        element.remove_child(elem)

                element.write_attribs()
                element.load_metadata()

    except ParseError as e:
        raise ParserError(str(e))
    except MissingFileError:
        return None, None
    except OSError:
        raise AssertionError("Files are being used by another process. Please shut them down before opening.")

    return info_root, config_root


def new():
    """
    Creates and returns new root nodes for each element.
    """
    from . import nodes

    info_root = module_parser.makeelement(nodes.NodeInfoRoot.tag)
    config_root = module_parser.makeelement(nodes.NodeConfigRoot.tag)

    return info_root, config_root


def export(info_root, config_root, package_path):
    """
    Exports the root elements and saves them to installer files.

    :param info_root: The root element of the info.xml file.
    :param config_root: The root element of the moduleconfig.xml file.
    :param package_path: The path to save the files to.
    """
    hidden_nodes_pairs = []
    for root in (info_root, config_root):
        for node in root:
            if node.hidden_children:
                for hidden_node in node.hidden_children:
                    hidden_nodes_pairs.append((node, hidden_node, node.index(hidden_node)))
                    node.remove(hidden_node)

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

    for pair in hidden_nodes_pairs:
        pair[0].insert(pair[2], pair[1])
