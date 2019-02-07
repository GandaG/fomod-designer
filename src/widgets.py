#!/usr/bin/env python

# Copyright 2019 Daniel Nunes
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

import pyfomod
from PyQt5 import uic

from utils import RESOURCE_FOLDER

CONDITIONS_FILE_UI = uic.loadUiType(RESOURCE_FOLDER / "conditions_file.ui")
CONDITIONS_FLAG_UI = uic.loadUiType(RESOURCE_FOLDER / "conditions_flag.ui")
CONDITIONS_VERSION_UI = uic.loadUiType(RESOURCE_FOLDER / "conditions_version.ui")
CONDITIONS_NESTED_UI = uic.loadUiType(RESOURCE_FOLDER / "conditions_nested.ui")


class ConditionsFile(*CONDITIONS_FILE_UI):
    def __init__(
        self,
        conditions: pyfomod.Conditions,
        key: str,
        value: pyfomod.FileType,
        package_path: str,
    ):
        super().__init__()
        self.setupUi(self)

        self.conditions = conditions
        self.current_text = key
        self.package_path = package_path

        self.edit_file.setText(self.current_text)
        self.edit_file.textChanged.connect(self.update_file)

        self.combo_type.insertItems(0, [a.value for a in pyfomod.FileType])
        if value is not None:
            self.combo_type.setCurrentText(value.value)
        self.combo_type.currentIndexChanged[str].connect(
            lambda text: self.conditions.update(
                {self.current_text: pyfomod.FileType(text)}
            )
        )

    def update_file(self, text: str) -> None:
        del self.conditions[self.current_text]
        self.conditions[text] = self.combo_type.currentText()
        self.current_text = text

    def remove(self):
        del self.conditions[self.current_text]


class ConditionsFlag(*CONDITIONS_FLAG_UI):
    def __init__(self, conditions: pyfomod.Conditions, name: str, value: str):
        super().__init__()
        self.setupUi(self)

        self.conditions = conditions
        self.current_name = name

        self.edit_name.setText(name)
        self.edit_name.textChanged.connect(self.update_name)

        self.edit_value.setText(value)
        self.edit_value.textChanged.connect(
            lambda text: self.conditions.update({self.edit_name.text(): text})
        )

    def update_name(self, name: str) -> None:
        del self.conditions[self.current_name]
        self.conditions[name] = self.edit_value.text()
        self.current_name = name

    def remove(self):
        del self.conditions[self.current_name]


class ConditionsVersion(*CONDITIONS_VERSION_UI):
    def __init__(self, conditions: pyfomod.Conditions, value: str):
        super().__init__()
        self.setupUi(self)

        self.conditions = conditions

        self.edit_version.setText(value)
        self.edit_version.textChanged.connect(
            lambda text: self.conditions.update({None: text})
        )

    def remove(self):
        del self.conditions[None]


class ConditionsNested(*CONDITIONS_NESTED_UI):
    def __init__(self, parent_conditions: pyfomod.Conditions, conditions: pyfomod.Conditions):
        super().__init__()
        self.setupUi(self)

        self.conditions = parent_conditions
        self.self_conditions = conditions

        self.combo_type.insertItems(0, [a.value for a in pyfomod.ConditionType])
        self.combo_type.setCurrentText(self.self_conditions.type.value)
        self.combo_type.currentIndexChanged[str].connect(
            lambda text: self.self_conditions.__setattr__(
                "type", pyfomod.ConditionType(text)
            )
        )

    def remove(self):
        del self.conditions[self.self_conditions]
