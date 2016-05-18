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

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from os.path import join, relpath
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QLayout,
                             QStackedWidget, QLineEdit, QLabel, QFormLayout, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from . import cur_folder
from .io import elem_factory
from .exceptions import BaseInstanceException


class _WizardBase(QStackedWidget):
    __metaclass__ = ABCMeta

    cancelled = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, parent, element, main_window):
        super().__init__(parent)
        if type(self) is _WizardBase:
            raise BaseInstanceException(self)

        self.return_data = None
        self.element = element
        self.parent = parent
        self.main_window = main_window
        self.pages = self._add_pages()
        for page in self.pages:
            self.addWidget(page)

    @abstractmethod
    def _process_results(self, result):
        pass

    @abstractmethod
    def _add_pages(self):
        return []


class WizardFiles(_WizardBase):
    def _process_results(self, result):
        self.element.getparent().replace(self.element, result)
        item_parent = self.element.model_item.parent()
        row = self.element.model_item.row()
        item_parent.removeRow(row)
        item_parent.insertRow(row, result.model_item)
        self.finished.emit()

    def _add_pages(self):
        def add_elem(element_, layout):
            """
            :param element_: The element to be copied
            :param layout: The layout into which to insert the newly copied element
            """
            child = elem_factory(element_.tag, element_result)
            for key in element_.properties:
                child.properties[key].set_value(element_.properties[key].value)
            element_result.add_child(child)
            spacer = layout.takeAt(layout.count() - 1)
            layout.addWidget(self._create_field(child, page))
            layout.addSpacerItem(spacer)

        element_result = deepcopy(self.element)

        page = loadUi(join(cur_folder, "resources/templates/wizard_files_01.ui"))

        file_list = [elem for elem in element_result if elem.tag == "file"]
        for element in file_list:
            add_elem(element, page.layout_file)
            element_result.remove_child(element)

        folder_list = [elem for elem in element_result if elem.tag == "folder"]
        for element in folder_list:
            add_elem(element, page.layout_folder)
            element_result.remove_child(element)

        # finish with connections
        page.button_add_file.clicked.connect(lambda: add_elem(elem_factory("file", element_result), page.layout_file))
        page.button_add_folder.clicked.connect(
            lambda: add_elem(elem_factory("folder", element_result), page.layout_folder))
        page.finish_button.clicked.connect(lambda: self._process_results(element_result))
        page.cancel_button.clicked.connect(self.cancelled.emit)

        return [page]

    def _create_field(self, element, parent):
        """
        :param element: the element newly copied
        :param parent: the parent widget (the QWidgets inside the scroll areas)
        :return: base QWidget, with the source and destination fields built
        """
        def button_clicked():
            open_dialog = QFileDialog()
            if element.tag == "file":
                file_path = open_dialog.getOpenFileName(self, "Select File:", self.main_window.package_path)
                if file_path[0]:
                    edit_source.setText(relpath(file_path[0], self.main_window.package_path))
            elif element.tag == "folder":
                folder_path = open_dialog.getExistingDirectory(self, "Select folder:", self.main_window.package_path)
                if folder_path:
                    edit_source.setText(relpath(folder_path, self.main_window.package_path))

        # main widget
        base = QWidget(parent)
        layout_main = QHBoxLayout(base)
        layout_main.setContentsMargins(0, 0, 0, 0)

        # the entire source form, label + (edit + button)
        layout_source = QHBoxLayout()
        layout_source.setContentsMargins(0, 0, 0, 0)
        label_source = QLabel("Source:", base)

        # the source box (edit + button)
        base_source = QWidget(base)
        layout_source_field = QHBoxLayout(base_source)
        layout_source_field.setContentsMargins(0, 0, 0, 0)
        edit_source = QLineEdit(element.get("source"), base_source)
        button_source = QPushButton("...", base_source)
        layout_source_field.addWidget(edit_source)
        layout_source_field.addWidget(button_source)

        # finish the source form
        layout_source.addWidget(label_source)
        layout_source.addWidget(base_source)

        # the entire destination form, label + (edit + button)
        layout_dest = QHBoxLayout()
        layout_dest.setContentsMargins(0, 0, 0, 0)
        label_dest = QLabel("Destination:", base)
        edit_dest = QLineEdit(element.get("destination"), base)
        layout_dest.addWidget(label_dest)
        layout_dest.addWidget(edit_dest)

        # the delete self button
        button_delete = QPushButton(QIcon(join(cur_folder, "resources/logos/logo_cross.png")), "", base)
        button_delete.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button_delete.setMaximumSize(30, 30)

        # finish the main widget
        layout_main.addLayout(layout_source)
        layout_main.addLayout(layout_dest)
        layout_main.addWidget(button_delete)

        # connect the signals
        edit_source.textChanged.connect(element.properties["source"].set_value)
        edit_source.textChanged.connect(element.write_attribs)
        edit_dest.textChanged.connect(element.properties["destination"].set_value)
        edit_dest.textChanged.connect(element.write_attribs)
        button_source.clicked.connect(button_clicked)
        button_delete.clicked.connect(base.deleteLater)
        button_delete.clicked.connect(lambda x: element.getparent().remove_child(element))

        return base
