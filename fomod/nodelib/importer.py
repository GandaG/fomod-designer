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
from .base.factory import from_element
from .utility import check_file
from .exceptions import MissingFileError, ParserError


def import_(package_path):
    try:
        fomod_folder = check_file(package_path, "fomod")
        fomod_folder_path = os.path.join(package_path, fomod_folder)

        info_file = check_file(fomod_folder_path, "Info.xml")
        config_file = check_file(fomod_folder_path, "ModuleConfig.xml")

        info_path = os.path.join(fomod_folder_path, info_file)
        config_path = os.path.join(fomod_folder_path, config_file)

        info_tree = etree.parse(info_path)
        config_tree = etree.parse(config_path)

    except etree.ParseError as e:
        raise ParserError(str(e))
    except MissingFileError:
        return new()

    info_root = from_element(info_tree.getroot())
    config_root = from_element(config_tree.getroot())

    for element in info_tree.getroot().iter():
        if element is info_tree.getroot() or element.tag is etree.Comment:
            continue
        parsed_element = from_element(element)

        for node in info_root.iter():
            if node.element is element.getparent():
                node.add_child(parsed_element)

    for element in config_tree.getroot().iter():
        if element is config_tree.getroot() or element.tag is etree.Comment:
            continue
        parsed_element = from_element(element)

        for node in config_root.iter():
            if node.element is element.getparent():
                node.add_child(parsed_element)

    return info_root, config_root


def new():
    from .base import info, config

    return info.ObjectInfo(), config.ObjectConfig()
