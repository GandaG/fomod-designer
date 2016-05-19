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

from os import makedirs
from os.path import expanduser, normpath, basename, join, relpath
from datetime import datetime
from configparser import ConfigParser
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import (QShortcut, QFileDialog, QColorDialog, QMessageBox, QLabel, QHBoxLayout,
                             QFormLayout, QLineEdit, QSpinBox, QComboBox, QWidget, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from validator import validate_tree, check_warnings, ValidatorError, ValidationError, WarningError
from . import cur_folder, __version__
from .io import import_, new, export, sort_elements, elem_factory, highlight_fragment
from .props import PropertyFile, PropertyColour, PropertyFolder, PropertyCombo, PropertyInt, PropertyText
from .exceptions import GenericError


base_ui = loadUiType(join(cur_folder, "resources/templates/mainframe.ui"))
settings_ui = loadUiType(join(cur_folder, "resources/templates/settings.ui"))
about_ui = loadUiType(join(cur_folder, "resources/templates/about.ui"))


class MainFrame(base_ui[0], base_ui[1]):
    xml_code_changed = pyqtSignal([object])

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # setup the icons properly
        self.setWindowIcon(QIcon(join(cur_folder, "resources/window_icon.jpg")))
        self.action_Open.setIcon(QIcon(join(cur_folder, "resources/logos/logo_open_file.png")))
        self.action_Save.setIcon(QIcon(join(cur_folder, "resources/logos/logo_floppy_disk.png")))
        self.actionO_ptions.setIcon(QIcon(join(cur_folder, "resources/logos/logo_gear.png")))
        self.action_Refresh.setIcon(QIcon(join(cur_folder, "resources/logos/logo_refresh.png")))
        self.action_Delete.setIcon(QIcon(join(cur_folder, "resources/logos/logo_cross.png")))
        self.action_About.setIcon(QIcon(join(cur_folder, "resources/logos/logo_notepad.png")))
        self.actionHe_lp.setIcon(QIcon(join(cur_folder, "resources/logos/logo_info.png")))

        # setup any additional info left from designer
        self.delete_sec_shortcut = QShortcut(self)
        self.delete_sec_shortcut.setKey(Qt.Key_Delete)

        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.actionO_ptions.triggered.connect(self.options)
        self.action_Refresh.triggered.connect(self.refresh)
        self.action_Delete.triggered.connect(self.delete)
        self.delete_sec_shortcut.activated.connect(self.delete)
        self.actionHe_lp.triggered.connect(self.help)
        self.action_About.triggered.connect(self.about)
        self.actionClear.triggered.connect(self.clear_recent_files)
        self.action_Object_Tree.toggled.connect(self.toggle_tree)
        self.actionObject_Box.toggled.connect(self.toggle_list)
        self.action_Property_Editor.toggled.connect(self.toggle_editor)

        self.object_tree_view.clicked.connect(self.selected_object_tree)
        self.object_box_list.activated.connect(self.selected_object_list)

        self.wizard_button.clicked.connect(self.run_wizard)
        self.xml_code_changed.connect(self.update_gen_code)

        self.fomod_changed = False
        self.original_title = self.windowTitle()
        self.package_path = ""
        self.package_name = ""
        self.settings_dict = read_settings()
        self.info_root = None
        self.config_root = None
        self.current_object = None
        self.current_prop_list = []
        self.current_children_list = []
        self.tree_model = QStandardItemModel()
        self.list_model = QStandardItemModel()

        self.wizard_button.hide()

        self.object_tree_view.setModel(self.tree_model)
        self.object_tree_view.header().hide()
        self.object_box_list.setModel(self.list_model)

        self.update_recent_files()

    def open(self, path=""):
        try:
            answer = self.check_fomod_state()
            if answer == QMessageBox.Save:
                self.save()
            elif answer == QMessageBox.Cancel:
                return
            else:
                pass

            if not path:
                open_dialog = QFileDialog()
                package_path = open_dialog.getExistingDirectory(self, "Select package root directory:", expanduser("~"))
            else:
                package_path = path

            if package_path:
                info_root, config_root = import_(normpath(package_path))
                if info_root is not None and config_root is not None:
                    try:
                        if self.settings_dict["Load"]["validate"]:
                            validate_tree(config_root, join(cur_folder, "resources", "mod_schema.xsd"))
                    except ValidationError as e:
                        generic_errorbox(e.title, str(e))
                        if not self.settings_dict["Load"]["validate_ignore"]:
                            return
                    try:
                        if self.settings_dict["Load"]["warnings"]:
                            check_warnings(package_path, config_root)
                    except WarningError as e:
                        generic_errorbox(e.title, str(e))
                        if not self.settings_dict["Load"]["warn_ignore"]:
                            return
                else:
                    info_root, config_root = new()

                self.package_path = package_path
                self.info_root, self.config_root = info_root, config_root

                self.tree_model.clear()

                self.tree_model.appendRow(self.info_root.model_item)
                self.tree_model.appendRow(self.config_root.model_item)

                self.package_name = basename(normpath(self.package_path))
                self.fomod_modified(False)
                self.current_object = None
                self.xml_code_changed.emit(self.current_object)
                self.update_recent_files(self.package_path)
                self.clear_prop_list()
        except (GenericError, ValidatorError) as p:
            generic_errorbox(p.title, str(p), p.detailed)
            return

    def save(self):
        try:
            if not self.info_root and not self.config_root:
                return
            elif self.fomod_changed:
                sort_elements(self.info_root, self.config_root)
                try:
                    if self.settings_dict["Save"]["validate"]:
                        validate_tree(self.config_root, join(cur_folder, "resources", "mod_schema.xsd"))
                except ValidationError as e:
                    generic_errorbox(e.title, str(e))
                    if not self.settings_dict["Save"]["validate_ignore"]:
                        return
                try:
                    if self.settings_dict["Save"]["warnings"]:
                        check_warnings(self.package_path, self.config_root)
                except WarningError as e:
                    generic_errorbox(e.title, str(e))
                    if not self.settings_dict["Save"]["warn_ignore"]:
                        return
                export(self.info_root, self.config_root, self.package_path)
                self.fomod_modified(False)
        except ValidatorError as e:
            generic_errorbox(e.title, str(e))
            return

    def options(self):
        config = SettingsDialog()
        config.exec_()
        self.settings_dict = read_settings()

    def refresh(self):
        if self.settings_dict["General"]["code_refresh"] >= 1:
            self.xml_code_changed.emit(self.current_object)

    def delete(self):
        try:
            if self.current_object is not None:
                object_to_delete = self.current_object
                new_index = self.tree_model.indexFromItem(self.current_object.getparent().model_item)
                object_to_delete.getparent().remove_child(object_to_delete)
                self.fomod_modified(True)
                self.selected_object_tree(new_index)
        except AttributeError:
            generic_errorbox("You can't do that...", "You can't delete root objects!")

    @staticmethod
    def help():
        not_implemented()

    def about(self):
        # noinspection PyTypeChecker
        about_dialog = About(self)
        about_dialog.exec_()

    def toggle_tree(self, visible):
        if visible:
            self.object_tree.show()
        else:
            self.object_tree.hide()

    def toggle_list(self, visible):
        if visible:
            self.object_box.show()
        else:
            self.object_box.hide()

    def toggle_editor(self, visible):
        if visible:
            self.property_editor.show()
        else:
            self.property_editor.hide()

    def clear_recent_files(self):
        config = ConfigParser()
        config.read_dict(read_settings())
        for key in config["Recent Files"]:
            config["Recent Files"][key] = ""
        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            config.write(configfile)

        for child in self.menu_Recent_Files.actions():
            if child is not self.actionClear:
                self.menu_Recent_Files.removeAction(child)
                del child

    def update_recent_files(self, add_new=None):
        def open_path(instance, package):
            def open_():
                instance.open(package)
            return open_

        file_list = []
        settings = read_settings()
        for index in range(1, 5):
            if settings["Recent Files"]["file" + str(index)]:
                file_list.append(settings["Recent Files"]["file" + str(index)])
        self.clear_recent_files()

        if add_new:
            if add_new in file_list:
                file_list.remove(add_new)
            elif len(file_list) == 5:
                file_list.pop()
            file_list.insert(0, add_new)

        config = ConfigParser()
        config.read_dict(settings)
        for path in file_list:
            config["Recent Files"]["file" + str(file_list.index(path) + 1)] = path
        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            config.write(configfile)

        self.menu_Recent_Files.removeAction(self.actionClear)
        for path in file_list:
            action = self.menu_Recent_Files.addAction(path)
            action.triggered.connect(open_path(self, path))
        self.menu_Recent_Files.addSeparator()
        self.menu_Recent_Files.addAction(self.actionClear)

    def selected_object_tree(self, index):
        self.current_object = self.tree_model.itemFromIndex(index).xml_node
        self.object_tree_view.setCurrentIndex(index)
        if self.settings_dict["General"]["code_refresh"] >= 2:
            self.xml_code_changed.emit(self.current_object)

        self.update_box_list()
        self.update_props_list()
        self.update_wizard_button()

    def update_box_list(self):
        self.list_model.clear()
        self.current_children_list.clear()

        for child in self.current_object.allowed_children:
            new_object = child()
            if self.current_object.can_add_child(new_object):
                self.list_model.appendRow(new_object.model_item)
                self.current_children_list.append(new_object)

    def clear_prop_list(self):
        self.current_prop_list.clear()
        for index in reversed(range(self.formLayout.count())):
            widget = self.formLayout.takeAt(index).widget()
            if widget is not None:
                widget.deleteLater()

    def update_props_list(self):
        self.clear_prop_list()

        prop_index = 0
        prop_list = self.current_prop_list
        props = self.current_object.properties

        if self.current_object.allow_text:
            text_label = QLabel(self.dockWidgetContents)
            text_label.setObjectName("text_label")
            text_label.setText("Text")
            self.formLayout.setWidget(prop_index, QFormLayout.LabelRole, text_label)
            prop_list.append(QLineEdit(self.dockWidgetContents))
            prop_list[prop_index].setObjectName(str(prop_index))
            prop_list[prop_index].setText(self.current_object.text)
            prop_list[prop_index].textEdited[str].connect(self.current_object.set_text)
            prop_list[prop_index].textEdited[str].connect(self.current_object.write_attribs)
            prop_list[prop_index].textEdited[str].connect(self.fomod_modified)
            prop_list[prop_index].textEdited[str].connect(lambda: self.xml_code_changed.emit(self.current_object)
                                                          if self.settings_dict["General"]["code_refresh"] >= 3
                                                          else None)
            self.formLayout.setWidget(prop_index, QFormLayout.FieldRole,
                                      prop_list[prop_index])

            prop_index += 1

        for key in props:
            if not props[key].editable:
                continue

            label = QLabel(self.dockWidgetContents)
            label.setObjectName("label_" + str(prop_index))
            label.setText(props[key].name)
            self.formLayout.setWidget(prop_index, QFormLayout.LabelRole, label)

            if isinstance(props[key], PropertyText):
                prop_list.append(QLineEdit(self.dockWidgetContents))
                prop_list[prop_index].setText(props[key].value)
                prop_list[prop_index].textEdited[str].connect(props[key].set_value)
                prop_list[prop_index].textEdited[str].connect(self.current_object.write_attribs)
                prop_list[prop_index].textEdited[str].connect(self.current_object.update_item_name)
                prop_list[prop_index].textEdited[str].connect(self.fomod_modified)
                prop_list[prop_index].textEdited[str].connect(lambda: self.xml_code_changed.emit(self.current_object)
                                                              if self.settings_dict["General"]["code_refresh"] >= 3
                                                              else None)

            elif isinstance(props[key], PropertyInt):
                prop_list.append(QSpinBox(self.dockWidgetContents))
                prop_list[prop_index].setValue(int(props[key].value))
                prop_list[prop_index].setMinimum(props[key].min)
                prop_list[prop_index].setMaximum(props[key].max)
                prop_list[prop_index].valueChanged.connect(props[key].set_value)
                prop_list[prop_index].valueChanged.connect(self.current_object.write_attribs)
                prop_list[prop_index].valueChanged.connect(self.fomod_modified)
                prop_list[prop_index].valueChanged.connect(lambda: self.xml_code_changed.emit(self.current_object)
                                                           if self.settings_dict["General"]["code_refresh"] >= 3
                                                           else None)

            elif isinstance(props[key], PropertyCombo):
                prop_list.append(QComboBox(self.dockWidgetContents))
                prop_list[prop_index].insertItems(0, props[key].values)
                prop_list[prop_index].setCurrentIndex(props[key].values.index(props[key].value))
                prop_list[prop_index].activated[str].connect(props[key].set_value)
                prop_list[prop_index].activated[str].connect(self.current_object.write_attribs)
                prop_list[prop_index].activated[str].connect(self.current_object.update_item_name)
                prop_list[prop_index].activated[str].connect(self.fomod_modified)
                prop_list[prop_index].activated[str].connect(lambda: self.xml_code_changed.emit(self.current_object)
                                                             if self.settings_dict["General"]["code_refresh"] >= 3
                                                             else None)

            elif isinstance(props[key], PropertyFile):
                def button_clicked():
                    open_dialog = QFileDialog()
                    file_path = open_dialog.getOpenFileName(self, "Select File:", self.package_path)
                    if file_path[0]:
                        line_edit.setText(relpath(file_path[0], self.package_path))

                prop_list.append(QWidget(self.dockWidgetContents))
                layout = QHBoxLayout(prop_list[prop_index])
                line_edit = QLineEdit(prop_list[prop_index])
                path_button = QPushButton(prop_list[prop_index])
                path_button.setText("...")
                layout.addWidget(line_edit)
                layout.addWidget(path_button)
                layout.setContentsMargins(0, 0, 0, 0)
                line_edit.setText(props[key].value)
                line_edit.textChanged.connect(props[key].set_value)
                line_edit.textChanged[str].connect(self.current_object.write_attribs)
                line_edit.textChanged[str].connect(self.current_object.update_item_name)
                line_edit.textChanged[str].connect(self.fomod_modified)
                line_edit.textChanged[str].connect(lambda: self.xml_code_changed.emit(self.current_object)
                                                   if self.settings_dict["General"]["code_refresh"] >= 3 else None)
                path_button.clicked.connect(button_clicked)

            elif isinstance(props[key], PropertyFolder):
                def button_clicked():
                    open_dialog = QFileDialog()
                    folder_path = open_dialog.getExistingDirectory(self, "Select folder:", self.package_path)
                    if folder_path:
                        line_edit.setText(relpath(folder_path, self.package_path))

                prop_list.append(QWidget(self.dockWidgetContents))
                layout = QHBoxLayout(prop_list[prop_index])
                line_edit = QLineEdit(prop_list[prop_index])
                path_button = QPushButton(prop_list[prop_index])
                path_button.setText("...")
                layout.addWidget(line_edit)
                layout.addWidget(path_button)
                layout.setContentsMargins(0, 0, 0, 0)
                line_edit.setText(props[key].value)
                line_edit.textChanged.connect(props[key].set_value)
                line_edit.textChanged.connect(self.current_object.write_attribs)
                line_edit.textChanged.connect(self.current_object.update_item_name)
                line_edit.textChanged.connect(self.fomod_modified)
                line_edit.textChanged.connect(lambda: self.xml_code_changed.emit(self.current_object)
                                              if self.settings_dict["General"]["code_refresh"] >= 3 else None)
                path_button.clicked.connect(button_clicked)

            elif isinstance(props[key], PropertyColour):
                def button_clicked():
                    init_colour = QColor("#" + props[key].value)
                    colour_dialog = QColorDialog()
                    colour = colour_dialog.getColor(init_colour, self, "Choose Colour:")
                    if colour.isValid():
                        line_edit.setText(colour.name()[1:])

                def update_button_colour(text):
                    colour = QColor("#" + text)
                    if colour.isValid() and len(text) == 6:
                        path_button.setStyleSheet("background-color: " + colour.name())
                        path_button.setIcon(QIcon())
                    else:
                        path_button.setStyleSheet("background-color: #ffffff")
                        icon = QIcon()
                        icon.addPixmap(QPixmap(join(cur_folder, "resources/logos/logo_danger.png")),
                                       QIcon.Normal, QIcon.Off)
                        path_button.setIcon(icon)

                prop_list.append(QWidget(self.dockWidgetContents))
                layout = QHBoxLayout(prop_list[prop_index])
                line_edit = QLineEdit(prop_list[prop_index])
                line_edit.setMaxLength(6)
                path_button = QPushButton(prop_list[prop_index])
                layout.addWidget(line_edit)
                layout.addWidget(path_button)
                layout.setContentsMargins(0, 0, 0, 0)
                line_edit.setText(props[key].value)
                update_button_colour(line_edit.text())
                line_edit.textChanged.connect(props[key].set_value)
                line_edit.textChanged.connect(update_button_colour)
                line_edit.textChanged.connect(self.current_object.write_attribs)
                line_edit.textChanged.connect(self.fomod_modified)
                line_edit.textChanged.connect(lambda: self.xml_code_changed.emit(self.current_object)
                                              if self.settings_dict["General"]["code_refresh"] >= 3 else None)
                path_button.clicked.connect(button_clicked)

            self.formLayout.setWidget(prop_index, QFormLayout.FieldRole, prop_list[prop_index])
            prop_list[prop_index].setObjectName(str(prop_index))
            prop_index += 1

    def update_wizard_button(self):
        if self.current_object.wizard:
            self.wizard_button.show()
        else:
            self.wizard_button.hide()

    def run_wizard(self):
        def close():
            wizard.deleteLater()
            self.action_Object_Tree.toggled.emit(enabled_tree)
            self.actionObject_Box.toggled.emit(enabled_box)
            self.action_Property_Editor.toggled.emit(enabled_list)
            self.menu_File.setEnabled(True)
            self.menu_Tools.setEnabled(True)
            self.menu_View.setEnabled(True)

        current_index = self.tree_model.indexFromItem(self.current_object.model_item)
        enabled_tree = self.action_Object_Tree.isChecked()
        enabled_box = self.actionObject_Box.isChecked()
        enabled_list = self.action_Property_Editor.isChecked()
        self.action_Object_Tree.toggled.emit(False)
        self.actionObject_Box.toggled.emit(False)
        self.action_Property_Editor.toggled.emit(False)
        self.menu_File.setEnabled(False)
        self.menu_Tools.setEnabled(False)
        self.menu_View.setEnabled(False)

        wizard = self.current_object.wizard(self, self.current_object, self)
        self.splitter.insertWidget(0, wizard)

        wizard.cancelled.connect(close)
        wizard.finished.connect(close)
        wizard.finished.connect(lambda: self.selected_object_tree(current_index))
        wizard.finished.connect(lambda: self.fomod_modified(True))

    def selected_object_list(self, index):
        item = self.list_model.itemFromIndex(index)

        new_child = elem_factory(item.xml_node.tag, self.current_object)
        self.current_object.add_child(new_child)

        # expand the parent
        current_index = self.tree_model.indexFromItem(self.current_object.model_item)
        self.object_tree_view.expand(current_index)

        # select the new item
        self.object_tree_view.setCurrentIndex(self.tree_model.indexFromItem(new_child.model_item))
        self.selected_object_tree(self.tree_model.indexFromItem(new_child.model_item))

        # reload the object box
        self.update_box_list()

        # set the installer as changed
        self.fomod_modified(True)

    def update_gen_code(self, element):
        if element is not None:
            self.xml_code_browser.setHtml(highlight_fragment(element))
        else:
            self.xml_code_browser.setText("")

    def fomod_modified(self, changed):
        if changed is False:
            self.fomod_changed = False
            self.setWindowTitle(self.package_name + " - " + self.original_title)
        else:
            self.fomod_changed = True
            self.setWindowTitle("*" + self.package_name + " - " + self.original_title)

    def check_fomod_state(self):
        if self.fomod_changed:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("The installer has been modified.")
            msg_box.setText("Do you want to save your changes?")
            msg_box.setStandardButtons(QMessageBox.Save |
                                       QMessageBox.Discard |
                                       QMessageBox.Cancel)
            msg_box.setDefaultButton(QMessageBox.Save)
            return msg_box.exec_()
        else:
            return

    def closeEvent(self, event):
            answer = self.check_fomod_state()
            if answer == QMessageBox.Save:
                self.save()
            elif answer == QMessageBox.Discard:
                pass
            elif answer == QMessageBox.Cancel:
                event.ignore()


class SettingsDialog(settings_ui[0], settings_ui[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.check_valid_load.stateChanged.connect(self.update_valid_load)
        self.check_warn_load.stateChanged.connect(self.update_warn_load)
        self.check_valid_save.stateChanged.connect(self.update_valid_save)
        self.check_warn_save.stateChanged.connect(self.update_warn_save)

        config = read_settings()
        self.combo_code_refresh.setCurrentIndex(config["General"]["code_refresh"])
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
        config.read_dict(read_settings())
        config["General"]["code_refresh"] = str(self.combo_code_refresh.currentIndex())
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


class About(about_ui[0], about_ui[1]):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)

        self.move(parent.window().frameGeometry().topLeft() + parent.window().rect().center() - self.rect().center())

        self.setWindowFlags(Qt.WindowTitleHint)

        self.version.setText("Version: " + __version__)

        copyright_text = self.copyright.text()
        new_year = "2016-" + str(datetime.now().year) if datetime.now().year != 2016 else "2016"
        copyright_text = copyright_text.replace("2016", new_year)
        self.copyright.setText(copyright_text)

        self.button.clicked.connect(self.close)


def not_implemented():
    generic_errorbox("Nope", "Sorry, this part hasn't been implemented yet!")


def generic_errorbox(title, text, detail=""):
    errorbox = QMessageBox()
    errorbox.setText(text)
    errorbox.setWindowTitle(title)
    errorbox.setDetailedText(detail)
    errorbox.setIconPixmap(QPixmap(join(cur_folder, "resources/logos/logo_admin.png")))
    errorbox.exec_()


def read_settings():
    default_settings = {"General": {"code_refresh": 3},
                        "Load": {"validate": True,
                                 "validate_ignore": False,
                                 "warnings": True,
                                 "warn_ignore": True},
                        "Save": {"validate": True,
                                 "validate_ignore": False,
                                 "warnings": True,
                                 "warn_ignore": True},
                        "Recent Files": {"file1": "",
                                         "file2": "",
                                         "file3": "",
                                         "file4": "",
                                         "file5": ""}}
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
