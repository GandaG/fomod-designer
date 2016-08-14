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
from PyQt5.QtWidgets import QStackedWidget, QFileDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from . import cur_folder
from .io import node_factory
from .ui_templates import (wizard_files_01, wizard_files_item, wizard_depend_01, wizard_depend_depend,
                           wizard_depend_depend_depend, wizard_depend_depend_file, wizard_depend_depend_flag,
                           wizard_depend_depend_version, wizard_depend_file, wizard_depend_flag)


class _WizardBase(QStackedWidget):
    """
    The base class for wizards. Shouldn't be instantiated directly.
    """
    __metaclass__ = ABCMeta

    code_changed = pyqtSignal([object])
    cancelled = pyqtSignal()
    finished = pyqtSignal([object])

    def __init__(self, parent, element, code_signal, **kwargs):
        """
        :param parent: The parent widget.
        :param element: The element this wizard corresponds.
        :param main_window: The app's main window.
        """
        super().__init__(parent)
        if type(self) is _WizardBase:
            raise AssertionError(str(type(self)) + " is not meant to be instanced. A subclass should be used instead.")

        self.element = element
        self.parent = parent
        self.kwargs = kwargs
        self.code_changed.connect(code_signal.emit)
        self._setup_pages()

    @abstractmethod
    def _process_results(self, result):
        """
        Method called to process the results into a new element.

        :param result: The temporary element with all the info.
        """
        pass

    @abstractmethod
    def _setup_pages(self):
        """
        Method called during initialization to create all the pages necessary for each wizard.
        """
        pass


class WizardFiles(_WizardBase):
    """
    Wizard for the "files" tag.
    """
    def _process_results(self, result):
        self.finished.emit(result)

    def _setup_pages(self):
        def add_elem(element_, layout):
            """
            :param element_: The element to be copied
            :param layout: The layout into which to insert the newly copied element
            """
            child = node_factory(element_.tag, element_result)
            for key in element_.attrib:
                child.properties[key].set_value(element_.attrib[key])
            element_result.add_child(child)
            spacer = layout.takeAt(layout.count() - 1)
            item = self._create_field(child)
            layout.addWidget(item)
            layout.addSpacerItem(spacer)
            self.code_changed.emit(element_result)

        element_result = deepcopy(self.element)

        page = QWidget()
        page_ui = wizard_files_01.Ui_Form()
        page_ui.setupUi(page)

        file_list = [elem for elem in element_result if elem.tag == "file"]
        for element in file_list:
            element_result.remove_child(element)
            add_elem(element, page_ui.layout_file)

        folder_list = [elem for elem in element_result if elem.tag == "folder"]
        for element in folder_list:
            element_result.remove_child(element)
            add_elem(element, page_ui.layout_folder)

        # finish with connections
        page_ui.button_add_file.clicked.connect(
            lambda: add_elem(node_factory("file", element_result), page_ui.layout_file)
        )
        page_ui.button_add_folder.clicked.connect(
            lambda: add_elem(node_factory("folder", element_result), page_ui.layout_folder)
        )
        page_ui.finish_button.clicked.connect(lambda: self._process_results(element_result))
        page_ui.cancel_button.clicked.connect(self.cancelled.emit)

        self.addWidget(page)

    def _create_field(self, element):
        """
        :param element: the element newly copied
        :return: base QWidget, with the source and destination fields built
        """
        def button_clicked():
            open_dialog = QFileDialog()
            if element.tag == "file":
                file_path = open_dialog.getOpenFileName(self, "Select File:", self.kwargs["package_path"])
                if file_path[0]:
                    item_ui.edit_source.setText(relpath(file_path[0], self.kwargs["package_path"]))
            elif element.tag == "folder":
                folder_path = open_dialog.getExistingDirectory(self, "Select folder:", self.kwargs["package_path"])
                if folder_path:
                    item_ui.edit_source.setText(relpath(folder_path, self.kwargs["package_path"]))

        parent_element = element.getparent()

        item = QWidget()
        item_ui = wizard_files_item.Ui_base()
        item_ui.setupUi(item)

        # set initial values
        item_ui.edit_source.setText(element.properties["source"].value)
        item_ui.edit_dest.setText(element.properties["destination"].value)
        item_ui.button_delete.setIcon(QIcon(join(cur_folder, "resources/logos/logo_cross.png")))

        # connect the signals
        item_ui.edit_source.textChanged.connect(element.properties["source"].set_value)
        item_ui.edit_source.textChanged.connect(element.write_attribs)
        item_ui.edit_source.textChanged.connect(lambda: self.code_changed.emit(parent_element))
        item_ui.edit_dest.textChanged.connect(element.properties["destination"].set_value)
        item_ui.edit_dest.textChanged.connect(element.write_attribs)
        item_ui.edit_dest.textChanged.connect(lambda: self.code_changed.emit(parent_element))
        item_ui.button_source.clicked.connect(button_clicked)
        item_ui.button_delete.clicked.connect(item.deleteLater)
        item_ui.button_delete.clicked.connect(lambda _: parent_element.remove_child(element))
        item_ui.button_delete.clicked.connect(lambda: self.code_changed.emit(parent_element))

        return item


class WizardDepend(_WizardBase):
    """
    Wizard for the "dependencies" tag.
    """
    def _process_results(self, result):
        self.finished.emit(result)

    def _setup_pages(self):
        """
        NodeConfigVisible and NodeConfigRoot are used as simple placeholders for the factory. They serve no purpose
        other than giving the factory a parent to help parsing.
        """
        from .nodes import NodeConfigVisible, NodeConfigRoot

        def copy_depend(element_):
            if element_.getparent().tag == "dependencies" or \
                    element_.getparent().tag == "moduleDependencies" or \
                    element_.getparent().tag == "visible":
                result = node_factory(element_.tag, NodeConfigVisible())
            elif element_.tag == "moduleDependencies":
                result = node_factory(element_.tag, NodeConfigVisible())
            elif element_.tag == "visible":
                result = node_factory(element_.tag, NodeConfigVisible())
            else:
                result = node_factory(element_.tag, NodeConfigRoot())

            element_.write_attribs()
            for key in element_.keys():
                result.set(key, element_.get(key))
            result.parse_attribs()

            for child in element_:
                if child.tag == "dependencies":
                    result.add_child(copy_depend(child))
                    continue
                new_child = deepcopy(child)
                for key in child.keys():
                    new_child.set(key, child.get(key))
                new_child.parse_attribs()
                result.add_child(new_child)

            return result

        element_result = copy_depend(self.element)
        self.code_changed.emit(element_result)

        page = QWidget()
        page_ui = wizard_depend_01.Ui_Form()
        page_ui.setupUi(page)

        page_ui.typeComboBox.setCurrentText(element_result.get("operator"))

        for element in [elem for elem in element_result if elem.tag == "fileDependency"]:
            self.add_elem(element_result, page_ui.layout_file, element_=element)

        for element in [elem for elem in element_result if elem.tag == "flagDependency"]:
            self.add_elem(element_result, page_ui.layout_flag, element_=element)

        for element in [elem for elem in element_result if elem.tag == "dependencies"]:
            self.add_elem(element_result, page_ui.layout_depend, element_=element)

        for elem in element_result:
            if elem.tag == "gameDependency":
                page_ui.gameVersionLineEdit.setText(elem.get("version"))

        # finish with connections
        page_ui.typeComboBox.currentTextChanged.connect(element_result.properties["operator"].set_value)
        page_ui.typeComboBox.currentTextChanged.connect(element_result.write_attribs)
        page_ui.typeComboBox.currentTextChanged.connect(lambda: self.code_changed.emit(element_result))

        page_ui.gameVersionLineEdit.textChanged.connect(
            lambda value, element_=element_result: self._update_version(value, element_))

        page_ui.button_file.clicked.connect(
            lambda: self.add_elem(element_result, page_ui.layout_file, tag="fileDependency"))

        page_ui.button_flag.clicked.connect(
            lambda: self.add_elem(element_result, page_ui.layout_flag, tag="flagDependency"))

        page_ui.button_sub.clicked.connect(
            lambda: self.add_elem(element_result, page_ui.layout_depend, tag="dependencies"))

        page_ui.finish_button.clicked.connect(lambda: self._process_results(element_result))
        page_ui.cancel_button.clicked.connect(self.cancelled.emit)

        self.addWidget(page)

    def add_elem(self, parent_elem, layout, tag="", element_=None):
        """
        :param parent_elem: The parent element - the element the wizard is being applied on.
        :param tag: The tag of the element to be created
        :param element_: The element to be used
        :param layout: The layout into which to insert the newly copied element
        """
        from .nodes import NodeConfigVisible

        if element_ is None and tag:
            child = node_factory(tag, NodeConfigVisible())
            parent_elem.add_child(child)
        else:
            if element_ is None:
                return
            child = element_
            tag = child.tag
        spacer = layout.takeAt(layout.count() - 1)
        item = None
        if tag == "fileDependency":
            item = self._create_file(child)
        elif tag == "flagDependency":
            item = self._create_flag(child)
        elif tag == "dependencies":
            item = self._create_depend(child, layout)
        layout.addWidget(item)
        layout.addSpacerItem(spacer)
        self.code_changed.emit(parent_elem)

    def _update_version(self, value, element):
        elem = None
        for ele in element:
            if ele.tag == "gameDependency":
                elem = ele

        if elem is not None:
            if not value:
                element.remove_child(elem)
            else:
                elem.properties["version"].set_value(value)
                elem.write_attribs()
        else:
            if value:
                elem = node_factory("gameDependency", element)
                element.add_child(elem)
                elem.properties["version"].set_value(value)
                elem.write_attribs()

        self.code_changed.emit(element)

    def _create_file(self, element):
        parent_element = element.getparent()

        item = QWidget()
        item_ui = wizard_depend_file.Ui_Form()
        item_ui.setupUi(item)

        # set initial values
        item_ui.edit_file.setText(element.properties["file"].value)
        item_ui.combo_type.setCurrentText(element.properties["state"].value)
        item_ui.button_delete.setIcon(QIcon(join(cur_folder, "resources/logos/logo_cross.png")))

        # connect the signals
        item_ui.edit_file.textChanged.connect(element.properties["file"].set_value)
        item_ui.edit_file.textChanged.connect(element.write_attribs)
        item_ui.edit_file.textChanged.connect(lambda: self.code_changed.emit(parent_element))

        item_ui.combo_type.currentTextChanged.connect(element.properties["state"].set_value)
        item_ui.combo_type.currentTextChanged.connect(element.write_attribs)
        item_ui.combo_type.currentTextChanged.connect(lambda: self.code_changed.emit(parent_element))

        item_ui.button_delete.clicked.connect(item.deleteLater)
        item_ui.button_delete.clicked.connect(lambda _: parent_element.remove_child(element))
        item_ui.button_delete.clicked.connect(lambda: self.code_changed.emit(parent_element))

        return item

    def _create_flag(self, element):
        parent_element = element.getparent()

        item = QWidget()
        item_ui = wizard_depend_flag.Ui_Form()
        item_ui.setupUi(item)

        # set initial values
        item_ui.edit_flag.setText(element.properties["flag"].value)
        item_ui.edit_value.setText(element.properties["value"].value)
        item_ui.button_delete.setIcon(QIcon(join(cur_folder, "resources/logos/logo_cross.png")))

        # connect the signals
        item_ui.edit_flag.textChanged.connect(element.properties["flag"].set_value)
        item_ui.edit_flag.textChanged.connect(element.write_attribs)
        item_ui.edit_flag.textChanged.connect(lambda: self.code_changed.emit(parent_element))

        item_ui.edit_value.textChanged.connect(element.properties["value"].set_value)
        item_ui.edit_value.textChanged.connect(element.write_attribs)
        item_ui.edit_value.textChanged.connect(lambda: self.code_changed.emit(parent_element))

        item_ui.button_delete.clicked.connect(item.deleteLater)
        item_ui.button_delete.clicked.connect(lambda _: parent_element.remove_child(element))
        item_ui.button_delete.clicked.connect(lambda: self.code_changed.emit(parent_element))

        return item

    def _create_depend(self, element, depend_layout):
        parent_element = element.getparent()

        item = QWidget()
        item_ui = wizard_depend_depend.Ui_Form()
        item_ui.setupUi(item)

        file = QWidget()
        file_ui = wizard_depend_depend_file.Ui_Form()
        file_ui.setupUi(file)

        flag = QWidget()
        flag_ui = wizard_depend_depend_flag.Ui_Form()
        flag_ui.setupUi(flag)

        version = QWidget()
        version_ui = wizard_depend_depend_version.Ui_Form()
        version_ui.setupUi(version)

        depend = QWidget()
        depend_ui = wizard_depend_depend_depend.Ui_Form()
        depend_ui.setupUi(depend)

        item_ui.label_type.setText(element.properties["operator"].value)
        item_ui.button_less.hide()
        item_ui.line.hide()
        item_ui.scrollArea.hide()
        item_ui.button_delete.setIcon(QIcon(join(cur_folder, "resources/logos/logo_cross.png")))

        spacer = item_ui.layout_depend_depend.takeAt(item_ui.layout_depend_depend.count() - 1)

        for element_ in [elem for elem in element if elem.tag == "fileDependency"]:
            file_ui.label_file.setText(element_.properties["file"].value)
            file_ui.label_type.setText(element_.properties["state"].value)
            item_ui.layout_depend_depend.addWidget(file)

        for element_ in [elem for elem in element if elem.tag == "flagDependency"]:
            flag_ui.label_flag.setText(element_.properties["flag"].value)
            flag_ui.label_value.setText(element_.properties["value"].value)
            item_ui.layout_depend_depend.addWidget(flag)

        sub_dependencies_sum = sum(1 for elem in element if elem.tag == "dependencies")
        if sub_dependencies_sum:
            depend_ui.label_number.setText(str(sub_dependencies_sum))
            if sub_dependencies_sum > 1:
                depend_ui.label_depend.setText("Sub-Dependencies")
                item_ui.layout_depend_depend.addWidget(depend)

        for element_ in [elem for elem in element if elem.tag == "gameDependency"]:
            version_ui.label_version.setText(element_.get("version"))
            item_ui.layout_depend_depend.addWidget(version)

        item_ui.layout_depend_depend.addSpacerItem(spacer)

        item_ui.button_more.clicked.connect(lambda: item_ui.button_more.hide())
        item_ui.button_more.clicked.connect(lambda: item_ui.button_less.show())
        item_ui.button_more.clicked.connect(lambda: item_ui.line.show())
        item_ui.button_more.clicked.connect(lambda: item_ui.scrollArea.show())

        item_ui.button_less.clicked.connect(lambda: item_ui.button_less.hide())
        item_ui.button_less.clicked.connect(lambda: item_ui.button_more.show())
        item_ui.button_less.clicked.connect(lambda: item_ui.line.hide())
        item_ui.button_less.clicked.connect(lambda: item_ui.scrollArea.hide())

        item_ui.button_edit.clicked.connect(lambda _, element__=element: self._nested_wizard(element__, depend_layout))

        item_ui.button_delete.clicked.connect(item.deleteLater)
        item_ui.button_delete.clicked.connect(lambda _: parent_element.remove_child(element))
        item_ui.button_delete.clicked.connect(lambda: self.code_changed.emit(parent_element))

        return item

    def _nested_wizard(self, element, depend_layout):
        nested_wiz = WizardDepend(self, element, self.code_changed, **self.kwargs)
        self.addWidget(nested_wiz)
        self.setCurrentWidget(nested_wiz)

        nested_wiz.cancelled.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.cancelled.connect(lambda parent=element.getparent(): self.code_changed.emit(parent))

        nested_wiz.finished.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.finished.connect(lambda parent=element.getparent(): self._update_depends(parent, depend_layout))
        nested_wiz.finished.connect(lambda parent=element.getparent(): self.code_changed.emit(parent))

    def _update_depends(self, main_elem, depend_layout):
        for index in reversed(range(depend_layout.count())):
            if depend_layout.itemAt(index).widget():
                widget = depend_layout.takeAt(index).widget()
                if widget is not None:
                    widget.deleteLater()

        [self.add_elem(main_elem, depend_layout, element_=elem) for elem in main_elem if elem.tag == "dependencies"]
