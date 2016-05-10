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
                             "validate_ignore": False,
                             "warnings": True,
                             "warn_ignore": True},
                    "Save": {"validate": True,
                             "validate_ignore": False,
                             "warnings": True,
                             "warn_ignore": True}}


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
        self.check_valid_load.stateChanged.connect(self.update_valid_load)
        self.check_warn_load.stateChanged.connect(self.update_warn_load)
        self.check_valid_save.stateChanged.connect(self.update_valid_save)
        self.check_warn_save.stateChanged.connect(self.update_warn_save)

        config = read_settings()
        self.check_valid_load.setChecked(config["Load"]["validate"])
        self.check_valid_load_ignore.setChecked(config["Load"]["validate_ignore"])
        self.check_warn_load.setChecked(config["Load"]["warnings"])
        self.check_warn_load_ignore.setChecked(config["Load"]["warn_ignore"])
        self.check_valid_save.setChecked(config["Save"]["validate"])
        self.check_valid_save_ignore.setChecked(config["Save"]["validate_ignore"])
        self.check_warn_save.setChecked(config["Save"]["warnings"])
        self.check_warn_save_ignore.setChecked(config["Save"]["warn_ignore"])

        self.check_valid_load.stateChanged.emit(self.check_valid_load.isChecked())
        self.check_warn_load.stateChanged.emit(self.check_warn_load.isChecked())
        self.check_valid_save.stateChanged.emit(self.check_valid_save.isChecked())
        self.check_warn_save.stateChanged.emit(self.check_warn_save.isChecked())

    def accepted(self):
        config = ConfigParser()
        config.read_dict(default_settings)
        config["Load"]["validate"] = str(self.check_valid_load.isChecked()).lower()
        config["Load"]["validate_ignore"] = str(self.check_valid_load_ignore.isChecked()).lower()
        config["Load"]["warnings"] = str(self.check_warn_load.isChecked()).lower()
        config["Load"]["warn_ignore"] = str(self.check_warn_load_ignore.isChecked()).lower()
        config["Save"]["validate"] = str(self.check_valid_save.isChecked()).lower()
        config["Save"]["validate_ignore"] = str(self.check_valid_save_ignore.isChecked()).lower()
        config["Save"]["warnings"] = str(self.check_warn_save.isChecked()).lower()
        config["Save"]["warn_ignore"] = str(self.check_warn_save_ignore.isChecked()).lower()

        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            config.write(configfile)

        self.close()

    def rejected(self):
        self.close()

    def update_valid_load(self, new_state):
        if not new_state:
            self.check_valid_load_ignore.setEnabled(False)
        else:
            self.check_valid_load_ignore.setEnabled(True)

    def update_warn_load(self, new_state):
        if not new_state:
            self.check_warn_load_ignore.setEnabled(False)
        else:
            self.check_warn_load_ignore.setEnabled(True)

    def update_valid_save(self, new_state):
        if not new_state:
            self.check_valid_save_ignore.setEnabled(False)
        else:
            self.check_valid_save_ignore.setEnabled(True)

    def update_warn_save(self, new_state):
        if not new_state:
            self.check_warn_save_ignore.setEnabled(False)
        else:
            self.check_warn_save_ignore.setEnabled(True)
