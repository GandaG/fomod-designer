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


def check_fomod(package_path):
    existing_fomod = False
    fomod_folder = "fomod"

    for folder in os.listdir(package_path):
        if folder.upper() == "FOMOD":
            existing_fomod = True
            fomod_folder = folder

    return fomod_folder, existing_fomod


def check_file(fomod_path, ignore_errors=False):
    info_exists = False
    config_exists = False

    info_file = "info.xml"
    config_file = "moduleconfig.xml"

    for file in os.listdir(fomod_path):
        if file.upper() == "INFO.XML":
            info_exists = True
            info_file = file
        if file.upper() == "MODULECONFIG.XML":
            config_exists = True
            config_file = file

    if (not info_exists or not config_exists) and not ignore_errors:
        raise OSError

    return info_file, config_file
