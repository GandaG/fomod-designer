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
from .io import elem_factory, copy_element
from .exceptions import BaseInstanceException
from .ui_templates import (wizard_files_01, wizard_files_item, wizard_depend_01, wizard_depend_depend,
                           wizard_depend_depend_depend, wizard_depend_depend_file, wizard_depend_depend_flag,
                           wizard_depend_depend_version, wizard_depend_file, wizard_depend_flag, wizard_dependtype_01,
                           wizard_dependtype_pattern, wizard_plugin_01, wizard_plugin_flag)


class _WizardBase(QStackedWidget):
    """
    The base class for wizards. Shouldn't be instantiated directly.
    """
    __metaclass__ = ABCMeta

    code_changed = pyqtSignal([object])
    cancelled = pyqtSignal()
    finished = pyqtSignal([object])

    def __init__(self, parent_widget, element, code_signal, **kwargs):
        """
        :param parent_widget: The parent widget.
        :param element: The element this wizard corresponds.
        :param main_window: The app's main window.
        """
        super().__init__(parent_widget)
        if type(self) is _WizardBase:
            raise BaseInstanceException(self)

        self.element = element
        self.parent_widget = parent_widget
        self.kwargs = kwargs
        self.code_changed.connect(code_signal.emit)
        self._setup_pages()

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
    def _setup_pages(self):
        def add_elem(element_, layout):
            """
            :param element_: The element to be copied
            :param layout: The layout into which to insert the newly copied element
            """
            child = elem_factory(element_.tag, element_result)
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

        file_list = element_result.findall("file")
        for element in file_list:
            element_result.remove_child(element)
            add_elem(element, page_ui.layout_file)

        folder_list = element_result.findall("folder")
        for element in folder_list:
            element_result.remove_child(element)
            add_elem(element, page_ui.layout_folder)

        # finish with connections
        page_ui.button_add_file.clicked.connect(
            lambda: add_elem(elem_factory("file", element_result), page_ui.layout_file)
        )
        page_ui.button_add_folder.clicked.connect(
            lambda: add_elem(elem_factory("folder", element_result), page_ui.layout_folder)
        )
        page_ui.finish_button.clicked.connect(lambda: self.finished.emit(element_result))
        page_ui.cancel_button.clicked.connect(self.cancelled.emit)

        self.code_changed.emit(element_result)
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
    def _setup_pages(self):
        """
        NodeConfigVisible and NodeConfigRoot are used as simple placeholders for the factory. They serve no purpose
        other than giving the factory a parent to help parsing.
        """
        element_result = copy_element(self.element)
        self.code_changed.emit(element_result)

        page = QWidget()
        page_ui = wizard_depend_01.Ui_Form()
        page_ui.setupUi(page)

        page_ui.typeComboBox.setCurrentText(element_result.get("operator"))

        for element in element_result.findall("fileDependency"):
            self.add_elem(element_result, page_ui.layout_file, element_=element)

        for element in element_result.findall("flagDependency"):
            self.add_elem(element_result, page_ui.layout_flag, element_=element)

        for element in element_result.findall("dependencies"):
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

        page_ui.finish_button.clicked.connect(lambda: self.finished.emit(element_result))
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
            child = elem_factory(tag, NodeConfigVisible())
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
        elem = element.find("gameDependency")

        if elem is not None:
            if not value:
                element.remove_child(elem)
            else:
                elem.properties["version"].set_value(value)
                elem.write_attribs()
        else:
            if value:
                elem = elem_factory("gameDependency", element)
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

        for element_ in element.findall("fileDependency"):
            file_ui.label_file.setText(element_.properties["file"].value)
            file_ui.label_type.setText(element_.properties["state"].value)
            item_ui.layout_depend_depend.addWidget(file)

        for element_ in element.findall("flagDependency"):
            flag_ui.label_flag.setText(element_.properties["flag"].value)
            flag_ui.label_value.setText(element_.properties["value"].value)
            item_ui.layout_depend_depend.addWidget(flag)

        sub_dependencies_sum = len(element.findall("dependencies"))
        if sub_dependencies_sum:
            depend_ui.label_number.setText(str(sub_dependencies_sum))
            if sub_dependencies_sum > 1:
                depend_ui.label_depend.setText("Sub-Dependencies")
                item_ui.layout_depend_depend.addWidget(depend)

        for element_ in element.findall("gameDependency"):
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

        [self.add_elem(main_elem, depend_layout, element_=elem) for elem in main_elem.findall("dependencies")]


class WizardDependType(_WizardBase):
    def _setup_pages(self):
        element_result = copy_element(self.element)

        default_type_elem = element_result.find("defaultType")
        if default_type_elem is None:
            default_type_elem = elem_factory("defaultType", element_result)
            element_result.add_child(default_type_elem)

        patterns_elem = element_result.find("patterns")
        if patterns_elem is None:
            patterns_elem = elem_factory("patterns", element_result)
            element_result.add_child(patterns_elem)

        page = QWidget()
        page_ui = wizard_dependtype_01.Ui_Form()
        page_ui.setupUi(page)

        pattern_list = patterns_elem.findall("pattern")
        for element in pattern_list:
            element_result.remove_child(element)
            self.add_elem(element_result, page_ui.layout_pattern, element_=element)

        page_ui.typeComboBox.setCurrentText(default_type_elem.properties["name"].value)

        # finish with connections
        page_ui.typeComboBox.currentTextChanged.connect(default_type_elem.properties["name"].set_value)
        page_ui.typeComboBox.currentTextChanged.connect(default_type_elem.write_attribs)
        page_ui.typeComboBox.currentTextChanged.connect(lambda: self.code_changed.emit(element_result))

        page_ui.button_pattern.clicked.connect(
            lambda: self.add_elem(patterns_elem, page_ui.layout_pattern, tag="pattern"))
        page_ui.button_pattern.clicked.connect(lambda: self.code_changed.emit(element_result))

        page_ui.finish_button.clicked.connect(lambda: self.finished.emit(element_result))
        page_ui.cancel_button.clicked.connect(self.cancelled.emit)

        self.code_changed.emit(element_result)
        self.addWidget(page)

    def add_elem(self, parent_elem, layout, tag="", element_=None):
        """
        :param parent_elem: The parent element - the element the wizard is being applied on.
        :param tag: The tag of the element to be created
        :param element_: The element to be used
        :param layout: The layout into which to insert the newly copied element
        """
        if element_ is None and tag:
            child = elem_factory(tag, parent_elem)
            parent_elem.add_child(child)
        else:
            if element_ is None:
                return
            child = element_
        spacer = layout.takeAt(layout.count() - 1)
        item = self._create_field(child)
        layout.addWidget(item)
        layout.addSpacerItem(spacer)
        self.code_changed.emit(parent_elem)

    def _create_field(self, element):
        """
        :param element: the element newly copied
        :return: base QWidget, with the source and destination fields built
        """
        parent_element = element.getparent()

        type_elem = element.find("type")
        if type_elem is None:
            type_elem = elem_factory("type", element)
            element.add_child(type_elem)

        depend_elem = element.find("dependencies")
        if depend_elem is None:
            depend_elem = elem_factory("dependencies", element)
            element.add_child(depend_elem)

        item = QWidget()
        item_ui = wizard_dependtype_pattern.Ui_Form()
        item_ui.setupUi(item)

        # set initial values
        item_ui.combo_type.setCurrentText(type_elem.properties["name"].value)
        item_ui.button_delete.setIcon(QIcon(join(cur_folder, "resources/logos/logo_cross.png")))

        # connect the signals
        item_ui.combo_type.currentTextChanged.connect(type_elem.properties["name"].set_value)
        item_ui.combo_type.currentTextChanged.connect(type_elem.write_attribs)
        item_ui.combo_type.currentTextChanged.connect(lambda: self.code_changed.emit(parent_element.getparent()))

        item_ui.button_depend.clicked.connect(
            lambda _, element_=depend_elem: self._nested_wizard(element_, item_ui.button_depend))

        item_ui.button_delete.clicked.connect(item.deleteLater)
        item_ui.button_delete.clicked.connect(lambda: parent_element.remove_child(element))
        item_ui.button_delete.clicked.connect(lambda: self.code_changed.emit(parent_element.getparent()))

        return item

    def _nested_wizard(self, element, depend_button):
        def update_depend_button(parent_element, depend_button_):
            depend_elem = parent_element.find("dependencies")
            depend_button_.clicked.disconnect()
            depend_button_.clicked.connect(
                lambda _, element_=depend_elem: self._nested_wizard(element_, depend_button_)
            )

        nested_wiz = WizardDepend(self, element, self.code_changed, **self.kwargs)
        self.addWidget(nested_wiz)
        self.setCurrentWidget(nested_wiz)

        nested_wiz.cancelled.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.cancelled.connect(
            lambda parent=element.getparent().getparent().getparent(): self.code_changed.emit(parent)
        )

        nested_wiz.finished.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.finished.connect(
            lambda parent=element.getparent().getparent().getparent(): self.code_changed.emit(parent)
        )
        nested_wiz.finished.connect(lambda parent=element.getparent(): update_depend_button(parent, depend_button))


class WizardPlugin(_WizardBase):
    def _setup_pages(self):
        def button_clicked(line_edit):
            open_dialog = QFileDialog()
            file_path = open_dialog.getOpenFileName(self, "Select File:", self.kwargs["package_path"])
            if file_path[0]:
                line_edit.setText(relpath(file_path[0], self.kwargs["package_path"]))

        def create_type_depend(type_descriptor_elem_):
            for elem in type_descriptor_elem_:
                type_descriptor_elem_.remove_child(elem)
            type_depend_elem_ = elem_factory("dependencyType", type_descriptor_elem_)
            type_depend_elem_.add_child(elem_factory("patterns", type_depend_elem_))
            type_depend_elem_.add_child(elem_factory("defaultType", type_depend_elem_))
            type_descriptor_elem_.add_child(type_depend_elem_)
            try:
                page_ui.button_depend.clicked.disconnect()
            except TypeError:
                pass
            page_ui.button_depend.clicked.connect(
                lambda _, element_=type_depend_elem_: self._nested_type_depend(element_, page_ui.button_depend)
            )

        def create_type(type_descriptor_elem_):
            for elem in type_descriptor_elem_:
                type_descriptor_elem_.remove_child(elem)
            type_elem_ = elem_factory("type", type_descriptor_elem_)
            type_descriptor_elem_.add_child(type_elem_)
            page_ui.combo_type.currentTextChanged.disconnect()
            page_ui.combo_type.currentTextChanged.connect(type_elem_.properties["name"].set_value)
            page_ui.combo_type.currentTextChanged.connect(type_elem_.write_attribs)
            page_ui.combo_type.currentTextChanged.connect(lambda: self.code_changed.emit(element_result))
            page_ui.combo_type.setCurrentText("Required")
            page_ui.combo_type.setCurrentText("Optional")

        element_result = copy_element(self.element)

        description_elem = element_result.find("description")
        if description_elem is None:
            description_elem = elem_factory("description", element_result)
            element_result.add_child(description_elem)

        image_elem = element_result.find("image")
        if image_elem is None:
            image_elem = elem_factory("image", element_result)
            element_result.add_child(image_elem)

        files_elem = element_result.find("files")
        if files_elem is None:
            files_elem = elem_factory("files", element_result)
            element_result.add_child(files_elem)

        condition_flags_elem = element_result.find("conditionFlags")
        if condition_flags_elem is None:
            condition_flags_elem = elem_factory("conditionFlags", element_result)
            element_result.add_child(condition_flags_elem)

        type_descriptor_elem = element_result.find("typeDescriptor")
        if type_descriptor_elem is None:
            type_descriptor_elem = elem_factory("typeDescriptor", element_result)
            element_result.add_child(type_descriptor_elem)

        page = QWidget()
        page_ui = wizard_plugin_01.Ui_Form()
        page_ui.setupUi(page)

        flag_list = condition_flags_elem.findall("flag")
        for element in flag_list:
            element_result.remove_child(element)
            self.add_elem(element_result, page_ui.layout_flag, element_=element)

        page_ui.nameLineEdit.setText(element_result.properties["name"].value)
        page_ui.descriptionLineEdit.setText(description_elem.text)
        page_ui.edit_image.setText(image_elem.properties["path"].value)

        type_elem = type_descriptor_elem.find("type")
        type_depend_elem = type_descriptor_elem.find("dependencyType")
        if type_depend_elem is not None:
            page_ui.radio_depend.setChecked(True)
            page_ui.button_depend.setEnabled(True)
            page_ui.combo_type.setEnabled(False)
            page_ui.button_depend.clicked.connect(
                lambda _, element_=type_depend_elem: self._nested_type_depend(element_, page_ui.button_depend)
            )
        elif type_elem is not None:
            page_ui.combo_type.setCurrentText(type_elem.properties["name"].value)
            page_ui.combo_type.currentTextChanged.connect(type_elem.properties["name"].set_value)
            page_ui.combo_type.currentTextChanged.connect(type_elem.write_attribs)
            page_ui.combo_type.currentTextChanged.connect(lambda: self.code_changed.emit(element_result))
        else:
            type_elem = elem_factory("type", type_descriptor_elem)
            type_descriptor_elem.add_child(type_elem)
            page_ui.combo_type.currentTextChanged.connect(type_elem.properties["name"].set_value)
            page_ui.combo_type.currentTextChanged.connect(type_elem.write_attribs)
            page_ui.combo_type.currentTextChanged.connect(lambda: self.code_changed.emit(element_result))
            page_ui.combo_type.setCurrentText("Optional")

        # finish with connections
        page_ui.nameLineEdit.textChanged.connect(element_result.properties["name"].set_value)
        page_ui.nameLineEdit.textChanged.connect(element_result.write_attribs)
        page_ui.nameLineEdit.textChanged.connect(lambda: self.code_changed.emit(element_result))

        page_ui.descriptionLineEdit.textChanged.connect(description_elem.set_text)
        page_ui.descriptionLineEdit.textChanged.connect(description_elem.write_attribs)
        page_ui.descriptionLineEdit.textChanged.connect(lambda: self.code_changed.emit(element_result))

        page_ui.edit_image.textChanged.connect(image_elem.properties["path"].set_value)
        page_ui.edit_image.textChanged.connect(image_elem.write_attribs)
        page_ui.edit_image.textChanged.connect(lambda: self.code_changed.emit(element_result))
        page_ui.button_image.clicked.connect(lambda: button_clicked(page_ui.edit_image))

        page_ui.button_files.clicked.connect(
            lambda _, element_=files_elem: self._nested_files(element_, page_ui.button_files)
        )

        page_ui.button_flag.clicked.connect(
            lambda: self.add_elem(condition_flags_elem, page_ui.layout_flag, tag="flag")
        )
        page_ui.button_flag.clicked.connect(lambda: self.code_changed.emit(element_result))

        page_ui.radio_type.toggled.connect(page_ui.combo_type.setEnabled)
        page_ui.radio_type.clicked.connect(lambda: create_type(type_descriptor_elem))
        page_ui.radio_type.clicked.connect(lambda: self.code_changed.emit(element_result))

        page_ui.radio_depend.toggled.connect(page_ui.button_depend.setEnabled)
        page_ui.radio_depend.clicked.connect(lambda: create_type_depend(type_descriptor_elem))
        page_ui.radio_depend.clicked.connect(lambda: self.code_changed.emit(element_result))

        page_ui.finish_button.clicked.connect(lambda: self.finished.emit(element_result))
        page_ui.cancel_button.clicked.connect(self.cancelled.emit)

        self.code_changed.emit(element_result)
        self.addWidget(page)

    def add_elem(self, parent_elem, layout, tag="", element_=None):
        """
        :param parent_elem: The parent element - the element the wizard is being applied on.
        :param tag: The tag of the element to be created
        :param element_: The element to be used
        :param layout: The layout into which to insert the newly copied element
        """
        if element_ is None and tag:
            child = elem_factory(tag, parent_elem)
            parent_elem.add_child(child)
        else:
            if element_ is None:
                return
            child = element_
        spacer = layout.takeAt(layout.count() - 1)
        item = self._create_field(child)
        layout.addWidget(item)
        layout.addSpacerItem(spacer)
        self.code_changed.emit(parent_elem)

    def _create_field(self, element):
        """
        :param element: the element newly copied
        :return: base QWidget, with the source and destination fields built
        """
        parent_element = element.getparent()

        item = QWidget()
        item_ui = wizard_plugin_flag.Ui_Form()
        item_ui.setupUi(item)

        # set initial values
        item_ui.edit_flag.setText(element.properties["name"].value)
        item_ui.edit_value.setText(element.text)
        item_ui.button_delete.setIcon(QIcon(join(cur_folder, "resources/logos/logo_cross.png")))

        # connect the signals
        item_ui.edit_flag.textChanged.connect(element.properties["name"].set_value)
        item_ui.edit_flag.textChanged.connect(element.write_attribs)
        item_ui.edit_flag.textChanged.connect(lambda: self.code_changed.emit(parent_element.getparent()))

        item_ui.edit_value.textChanged.connect(element.set_text)
        item_ui.edit_value.textChanged.connect(element.write_attribs)
        item_ui.edit_value.textChanged.connect(lambda: self.code_changed.emit(parent_element.getparent()))

        item_ui.button_delete.clicked.connect(item.deleteLater)
        item_ui.button_delete.clicked.connect(lambda: parent_element.remove_child(element))
        item_ui.button_delete.clicked.connect(lambda: self.code_changed.emit(parent_element.getparent()))

        return item

    def _nested_type_depend(self, element, depend_button):
        def update_depend_button(new_element, parent_element, depend_button_):
            depend_elem = parent_element.find("dependencyType")
            parent_element.replace(depend_elem, new_element)
            item_parent = parent_element.model_item
            row = depend_elem.model_item.row()
            item_parent.removeRow(row)
            item_parent.insertRow(row, new_element.model_item)
            self.code_changed.emit(parent_element.getparent())

            depend_button_.clicked.disconnect()
            depend_button_.clicked.connect(
                lambda _, element_=new_element: self._nested_type_depend(element_, depend_button_)
            )

        nested_wiz = WizardDependType(self, element, self.code_changed, **self.kwargs)
        self.addWidget(nested_wiz)
        self.setCurrentWidget(nested_wiz)

        nested_wiz.cancelled.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.cancelled.connect(
            lambda parent=element.getparent().getparent(): self.code_changed.emit(parent)
        )

        nested_wiz.finished.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.finished.connect(
            lambda new_elem, parent=element.getparent(): update_depend_button(new_elem, parent, depend_button)
        )

    def _nested_files(self, element, file_button):
        def update_files_button(new_element, parent_element, files_button_):
            files_elem = parent_element.find("files")
            parent_element.replace(files_elem, new_element)
            item_parent = parent_element.model_item
            row = files_elem.model_item.row()
            item_parent.removeRow(row)
            item_parent.insertRow(row, new_element.model_item)
            self.code_changed.emit(parent_element)

            files_button_.clicked.disconnect()
            files_button_.clicked.connect(
                lambda _, element_=new_element: self._nested_files(element_, files_button_)
            )

        nested_wiz = WizardFiles(self, element, self.code_changed, **self.kwargs)
        self.addWidget(nested_wiz)
        self.setCurrentWidget(nested_wiz)

        nested_wiz.cancelled.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.cancelled.connect(
            lambda parent=element.getparent(): self.code_changed.emit(parent)
        )

        nested_wiz.finished.connect(lambda: nested_wiz.deleteLater())
        nested_wiz.finished.connect(
            lambda new_elem, parent=element.getparent(): update_files_button(new_elem, parent, file_button)
        )
