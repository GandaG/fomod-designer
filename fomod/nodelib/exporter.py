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
from .exceptions import MissingFileError


def export(info_root, config_root, package_path):
    try:
        fomod_folder = check_file(package_path, "fomod")
    except MissingFileError as e:
        os.makedirs(os.path.join(package_path, e.file))
        fomod_folder = os.path.join(package_path, e.file)

    fomod_folder_path = os.path.join(package_path, fomod_folder)

    try:
        info_file = check_file(fomod_folder_path, "Info.xml")
    except MissingFileError as e:
        info_file = e.file

    try:
        config_file = check_file(fomod_folder_path, "ModuleConfig.xml")
    except MissingFileError as e:
        config_file = e.file

    info_path = os.path.join(fomod_folder_path, info_file)
    config_path = os.path.join(fomod_folder_path, config_file)

    info_element = None
    config_element = None

    for node in info_root.iter():
        element = etree.Element(node.tag)
        node.element = element

        if node.allow_text:
            element.text = node.text

        if node.parent is None:
            info_element = element
            continue

        node.parent.element.append(element)

    for node in config_root.iter():
        element = etree.Element(node.tag)
        node.element = element

        if node.allow_text:
            element.text = node.text

        for key in node.properties:
            element.set(node.properties[key].tag, str(node.properties[key].value))

        if node.required_children:
            for child in node.iter():
                if type(child) in node.required_children:
                    node.check_required_children(child)

        if node.parent is None:
            config_element = element
            continue

        node.parent.element.append(element)

    with open(info_path, "wb") as info:
        info_tree = etree.ElementTree(info_element)
        info_tree.write(info, pretty_print=True)

    with open(config_path, "wb") as config:
        config_tree = etree.ElementTree(config_element)
        config_tree.write(config, pretty_print=True)
