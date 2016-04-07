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
from ..factory import from_element


def parse(package_path):
    fomod_folder, fomod_exists = check_fomod(package_path)
    fomod_folder_path = os.path.join(package_path, fomod_folder)

    if not fomod_exists:
        return new(fomod_folder_path)

    info_path = os.path.join(fomod_folder_path, "info.xml")
    config_path = os.path.join(fomod_folder_path, "ModuleConfig.xml")

    info_tree = etree.parse(info_path)
    config_tree = etree.parse(config_path)

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


def new(fomod_folder_path):
    from .. import info, config

    return info.ObjectInfo(), config.ObjectConfig()


def check_fomod(package_path):
    existing_fomod = False
    fomod_folder = "fomod"

    for folder in os.listdir(package_path):
        if folder.upper() == "FOMOD":
            existing_fomod = True
            fomod_folder = folder

    return fomod_folder, existing_fomod
