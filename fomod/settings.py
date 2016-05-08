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

from PyQt5 import QtCore, uic
from configparser import ConfigParser
from os import makedirs
from os.path import join, expanduser
from . import cur_folder

settings_ui = uic.loadUiType(join(cur_folder, "resources/templates/settings.ui"))
default_settings = {"Load": {"validate": True,
                             "warnings": True},
                    "Save": {"validate": True,
                             "warnings": True}}


def read_settings():
    config = ConfigParser()
    config.read_dict(default_settings)
    config.read(join(expanduser("~"), ".fomod", ".designer"))

    settings = {}
    for section in config:
        settings[section] = {}
        for key in config[section]:
            if isinstance(default_settings[section][key], bool):
                settings[section][key] = config.getboolean(section, key)
            elif isinstance(default_settings[section][key], int):
                settings[section][key] = config.getint(section, key)
            elif isinstance(default_settings[section][key], float):
                settings[section][key] = config.getfloat(section, key)
            else:
                settings[section][key] = config.get(section, key)
    return settings


class SettingsDialog(settings_ui[0], settings_ui[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)

        config = read_settings()
        self.check_valid_load.setChecked(config["Load"]["validate"])
        self.check_warn_load.setChecked(config["Load"]["warnings"])
        self.check_valid_save.setChecked(config["Save"]["validate"])
        self.check_warn_save.setChecked(config["Save"]["warnings"])

    def accepted(self):
        config = ConfigParser()
        config.read_dict(default_settings)
        config["Load"]["validate"] = str(self.check_valid_load.isChecked()).lower()
        config["Load"]["warnings"] = str(self.check_warn_load.isChecked()).lower()
        config["Save"]["validate"] = str(self.check_valid_save.isChecked()).lower()
        config["Save"]["warnings"] = str(self.check_warn_save.isChecked()).lower()

        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            config.write(configfile)

        self.close()

    def rejected(self):
        self.close()
