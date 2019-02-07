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

from pathlib import Path

import pyfomod
from PyQt5 import QtGui, QtWidgets, uic

from utils import RESOURCE_FOLDER, file_dialog
from widgets import ConditionsFile, ConditionsNested, ConditionsVersion, ConditionsFlag

METADATA_UI = uic.loadUiType(RESOURCE_FOLDER / "metadata.ui")


class Metadata(*METADATA_UI):
    def __init__(self, fomod: pyfomod.Root, package_path: Path):
        super().__init__()
        self.setupUi(self)

        self.fomod = fomod
        self.package_path = package_path

        self.edit_name.setText(self.fomod.name)
        self.edit_author.setText(self.fomod.author)
        self.edit_version.setText(self.fomod.version)
        self.edit_description.setText(self.fomod.description)
        self.edit_website.setText(self.fomod.website)
        self.edit_image.setText(self.fomod.image)
        self.update_image(self.fomod.image)

        self.edit_name.textChanged.connect(
            lambda text: self.fomod.__setattr__("name", text)
        )
        self.edit_author.textChanged.connect(
            lambda text: self.fomod.__setattr__("author", text)
        )
        self.edit_version.textChanged.connect(
            lambda text: self.fomod.__setattr__("version", text)
        )
        self.edit_description.textChanged.connect(
            lambda text: self.fomod.__setattr__("description", text)
        )
        self.edit_website.textChanged.connect(
            lambda text: self.fomod.__setattr__("website", text)
        )
        self.edit_image.textChanged.connect(
            lambda text: self.fomod.__setattr__("image", text)
        )
        self.edit_image.textChanged.connect(self.update_image)
        self.button_image.clicked.connect(self.image_path_dialog)

        for key, value in self.fomod.conditions.items():
            self.append_condition(
                self.tree_conditions.invisibleRootItem(),
                self.fomod.conditions,
                key,
                value,
            )

        self.combo_type.insertItems(0, [a.value for a in pyfomod.ConditionType])
        self.combo_type.setCurrentText(self.fomod.conditions.type.value)
        self.combo_type.currentIndexChanged[str].connect(
            lambda text: self.fomod.conditions.__setattr__(
                "type", pyfomod.ConditionType(text)
            )
        )

        self.button_delete_condition.clicked.connect(self.remove_condition)

    def update_image(self, path: str) -> None:
        image_path = self.package_path / path
        pixmap = QtGui.QPixmap(str(image_path))
        self.label_image.setPixmap(pixmap)

    def image_path_dialog(self) -> None:
        fname = file_dialog(
            self, "Select Image", self.edit_image.text(), str(self.package_path)
        )
        if fname is not None:
            self.edit_image.setText(str(fname))

    def append_condition(self, parent: QtWidgets.QTreeWidgetItem, conditions: pyfomod.Conditions, key, value) -> None:
        item = QtWidgets.QTreeWidgetItem()
        parent.addChild(item)
        if key is None:
            widget = ConditionsVersion(conditions, value)
        elif isinstance(key, pyfomod.Conditions):
            widget = ConditionsNested(conditions, key)
            for child_key, child_value in key.items():
                self.append_condition(item, key, child_key, child_value)
        elif isinstance(value, pyfomod.FileType):  # key is string
            widget = ConditionsFile(conditions, key, value, str(self.package_path))
        else:  # both are string
            widget = ConditionsFlag(conditions, key, value)
        self.tree_conditions.setItemWidget(item, 0, widget)

    def remove_condition(self) -> None:
        try:
            selected = self.tree_conditions.selectedItems()[0]
        except IndexError:
            return
        widget = self.tree_conditions.itemWidget(selected, 0)
        widget.remove()
        parent = selected.parent()
        if parent is None:
            index = self.tree_conditions.indexOfTopLevelItem(selected)
            self.tree_conditions.takeTopLevelItem(index)
        else:
            index = parent.indexOfChild(selected)
            parent.takeChild(index)
