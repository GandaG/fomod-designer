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
from os.path import expanduser, normpath, basename, join, relpath, isdir
from threading import Thread
from queue import Queue
from webbrowser import open as web_open
from datetime import datetime
from configparser import ConfigParser
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import (QShortcut, QFileDialog, QColorDialog, QMessageBox, QLabel, QHBoxLayout, QCommandLinkButton,
                             QFormLayout, QLineEdit, QSpinBox, QComboBox, QWidget, QPushButton, QSizePolicy, QStatusBar)
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from requests import get, codes, ConnectionError, Timeout
from validator import validate_tree, check_warnings, ValidatorError
from . import cur_folder, __version__
from .io import import_, new, export, sort_elements, elem_factory
from .previews import PreviewDispatcherThread
from .props import PropertyFile, PropertyColour, PropertyFolder, PropertyCombo, PropertyInt, PropertyText
from .exceptions import DesignerError


intro_ui = loadUiType(join(cur_folder, "resources/templates/intro.ui"))
base_ui = loadUiType(join(cur_folder, "resources/templates/mainframe.ui"))
settings_ui = loadUiType(join(cur_folder, "resources/templates/settings.ui"))
about_ui = loadUiType(join(cur_folder, "resources/templates/about.ui"))


class IntroWindow(intro_ui[0], intro_ui[1]):
    """
    The class for the intro window. Subclassed from QDialog and created in Qt Designer.
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(join(cur_folder, "resources/window_icon.svg")))
        self.setWindowTitle("FOMOD Designer")
        self.version.setText("Version " + __version__)

        settings = read_settings()
        for key in sorted(settings["Recent Files"]):
            if settings["Recent Files"][key]:
                butto = QCommandLinkButton(basename(settings["Recent Files"][key]), settings["Recent Files"][key], self)
                butto.clicked.connect(lambda _, path=settings["Recent Files"][key]: self.open_path(path))
                self.scroll_layout.addWidget(butto)

        if not settings["General"]["show_intro"]:
            main_window = MainFrame()
            main_window.move(self.pos())
            main_window.show()
            self.close()
        else:
            self.show()

        self.new_button.clicked.connect(lambda: self.open_path(""))
        self.button_about.clicked.connect(lambda _, self_=self: MainFrame.about(self_))

    def open_path(self, path):
        """
        Method used to open a path in the main window - closes the intro window and show the main.

        :param path: The path to open.
        """
        config = ConfigParser()
        config.read_dict(read_settings())
        config["General"]["show_intro"] = str(not self.check_intro.isChecked()).lower()
        config["General"]["show_advanced"] = str(self.check_advanced.isChecked()).lower()
        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            config.write(configfile)

        main_window = MainFrame()
        main_window.move(self.pos())
        main_window.open(path)
        main_window.show()
        self.close()


class MainFrame(base_ui[0], base_ui[1]):
    """
    The class for the main window. Subclassed from QMainWindow and created in Qt Designer.
    """

    #: Signals the xml code has changed.
    xml_code_changed = pyqtSignal([object])

    #: Signals the mo preview is updated.
    update_mo_preview = pyqtSignal([QWidget])

    #: Signals the nmm preview is updated.
    update_nmm_preview = pyqtSignal([QWidget])

    #: Signals the code preview is updated.
    update_code_preview = pyqtSignal([str])

    #: Signals there is an update available.
    update_available = pyqtSignal()

    #: Signals the app is up-to-date.
    up_to_date = pyqtSignal()

    #: Signals a connection timed out.
    timeout = pyqtSignal()

    #: Signals there was an error with the internet connection.
    connection_error = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # setup the icons properly
        self.setWindowIcon(QIcon(join(cur_folder, "resources/window_icon.svg")))
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
        self.action_About.triggered.connect(lambda _, self_=self: self.about(self_))
        self.actionClear.triggered.connect(self.clear_recent_files)
        self.action_Object_Tree.toggled.connect(self.object_tree.setVisible)
        self.actionObject_Box.toggled.connect(self.object_box.setVisible)
        self.action_Property_Editor.toggled.connect(self.property_editor.setVisible)

        self.object_tree.visibilityChanged.connect(self.action_Object_Tree.setChecked)
        self.object_box.visibilityChanged.connect(self.actionObject_Box.setChecked)
        self.property_editor.visibilityChanged.connect(self.action_Property_Editor.setChecked)

        self.object_tree_view.clicked.connect(self.selected_object_tree)

        self.fomod_changed = False
        self.original_title = self.windowTitle()
        self.package_path = ""
        self.package_name = ""
        self.settings_dict = read_settings()
        self.info_root = None
        self.config_root = None
        self.current_object = None
        self.current_prop_list = []
        self.tree_model = QStandardItemModel()

        # start the preview threads
        self.preview_queue = Queue()
        self.xml_code_changed.connect(self.preview_queue.put)
        self.update_code_preview.connect(self.xml_code_browser.setHtml)
        self.preview_thread = PreviewDispatcherThread(self.preview_queue, self.update_mo_preview,
                                                      self.update_nmm_preview, self.update_code_preview)
        self.preview_thread.start()

        # manage the wizard button
        self.wizard_button.clicked.connect(self.run_wizard)
        self.wizard_button.hide()

        self.object_tree_view.setModel(self.tree_model)
        self.object_tree_view.header().hide()

        self.update_recent_files()
        self.check_updates()

    def check_updates(self):
        """
        Checks the version number on the remote repository (Github Releases)
        and compares it against the current version.

        If the remote version is higher, then the user is warned in the status bar and advised to get the new one.
        Otherwise, ignore.
        """

        def update_available_button():
            update_button = QPushButton("New Version Available!")
            update_button.setFlat(True)
            update_button.clicked.connect(lambda: web_open("https://github.com/GandaG/fomod-designer/releases/latest"))
            self.statusBar().addWidget(update_button)

        def check_remote():
            try:
                response = get("https://api.github.com/repos/GandaG/fomod-designer/releases", timeout=10)
                if response.status_code == codes.ok and response.json()[0]["tag_name"][1:] > __version__:
                    self.update_available.emit()
                else:
                    self.up_to_date.emit()
            except Timeout:
                self.timeout.emit()
            except ConnectionError:
                self.connection_error.emit()

        self.up_to_date.connect(lambda: self.setStatusBar(QStatusBar()))
        self.up_to_date.connect(lambda: self.statusBar().addWidget(QLabel("Everything is up-to-date.")))
        self.update_available.connect(lambda: self.setStatusBar(QStatusBar()))
        self.update_available.connect(update_available_button)
        self.timeout.connect(lambda: self.setStatusBar(QStatusBar()))
        self.timeout.connect(lambda: self.statusBar().addWidget(QLabel("Connection timed out.")))
        self.connection_error.connect(lambda: self.setStatusBar(QStatusBar()))
        self.connection_error.connect(lambda: self.statusBar().addWidget(QLabel("Could not connect to remote server, "
                                                                                "check your internet connection.")))

        self.statusBar().addWidget(QLabel("Checking for updates..."))

        Thread(target=check_remote).start()

    def open(self, path=""):
        """
        Open a new installer if one exists at path (if no path is given a dialog pops up asking the user to choose one)
        or create a new one.

        If enabled in the Settings the installer is also validated and checked for common errors.

        :param path: Optional. The path to open/create an installer at.
        """
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
                    if self.settings_dict["Load"]["validate"]:
                        validate_tree(config_root, join(cur_folder, "resources", "mod_schema.xsd"),
                                      self.settings_dict["Load"]["validate_ignore"])
                    if self.settings_dict["Load"]["warnings"]:
                        check_warnings(package_path, config_root, self.settings_dict["Save"]["warn_ignore"])
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
        except (DesignerError, ValidatorError) as p:
            generic_errorbox(p.title, str(p), p.detailed)
            return

    def save(self):
        """
        Saves the current installer at the current path.

        If enabled in the Settings the installer is also validated and checked for common errors.
        """
        try:
            if self.info_root is None and self.config_root is None:
                return
            elif self.fomod_changed:
                sort_elements(self.info_root, self.config_root)
                if self.settings_dict["Save"]["validate"]:
                    validate_tree(self.config_root, join(cur_folder, "resources", "mod_schema.xsd"),
                                  self.settings_dict["Save"]["validate_ignore"])
                if self.settings_dict["Save"]["warnings"]:
                    check_warnings(self.package_path, self.config_root, self.settings_dict["Save"]["warn_ignore"])
                export(self.info_root, self.config_root, self.package_path)
                self.fomod_modified(False)
        except ValidatorError as e:
            generic_errorbox(e.title, str(e))
            return

    def options(self):
        """
        Opens the Settings dialog.
        """
        config = SettingsDialog(self)
        config.exec_()
        self.settings_dict = read_settings()

    def refresh(self):
        """
        Refreshes all the previews if the refresh rate in Settings is high enough.
        """
        if self.settings_dict["General"]["code_refresh"] >= 1:
            self.xml_code_changed.emit(self.current_object)

    def delete(self):
        """
        Deletes the current node in the tree. No effect when using the Basic View.
        """
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

    @staticmethod
    def about(parent):
        """
        Opens the About dialog. This method is static to be able to be called from the Intro window.

        :param parent: The parent of the dialog.
        """
        about_dialog = About(parent)
        about_dialog.exec_()

    def clear_recent_files(self):
        """
        Clears the Recent Files gui menu and settings.
        """
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
        """
        Updates the Recent Files gui menu and settings. If called when opening an installer, pass that installer as
        add_new so it can be added to list or placed at the top.

        :param add_new: If a new installer is being opened, add it to the list or move it to the top.
        """
        def invalid_path(path_):
            """
            Called when a Recent Files path in invalid. Requests user decision on wether to delete the item or to leave
            it.

            :param path_: The invalid path.
            """
            msg_box = QMessageBox()
            msg_box.setWindowTitle("This path no longer exists.")
            msg_box.setText("Remove it from the Recent Files list?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            answer = msg_box.exec_()
            config_ = ConfigParser()
            config_.read_dict(read_settings())
            if answer == QMessageBox.Yes:
                for key in config_["Recent Files"]:
                    if config_["Recent Files"][key] == path_:
                        config_["Recent Files"][key] = ""
                        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile_:
                            config_.write(configfile_)
                        self.update_recent_files()
            elif answer == QMessageBox.No:
                pass

        file_list = []
        settings = read_settings()

        # Populate the file_list with the existing recent files
        for index in range(1, len(settings["Recent Files"])):
            if settings["Recent Files"]["file" + str(index)]:
                file_list.append(settings["Recent Files"]["file" + str(index)])

        # remove all duplicates there was an issue with duplicate after invalid path
        seen = set()
        seen_add = seen.add
        file_list = [x for x in file_list if not (x in seen or seen_add(x))]

        self.clear_recent_files()

        # check if the path is new or if it already exists - delete the last one or reorder respectively
        if add_new:
            if add_new in file_list:
                file_list.remove(add_new)
            elif len(file_list) == 5:
                file_list.pop()
            file_list.insert(0, add_new)

        # write the new list to the settings file
        config = ConfigParser()
        config.read_dict(settings)
        for path in file_list:
            config["Recent Files"]["file" + str(file_list.index(path) + 1)] = path
        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            config.write(configfile)

        # populate the gui menu with the new files list
        self.menu_Recent_Files.removeAction(self.actionClear)
        for path in file_list:
            action = self.menu_Recent_Files.addAction(path)
            action.triggered.connect(lambda x, path_=path: self.open(path_) if isdir(path_) else invalid_path(path_))
        self.menu_Recent_Files.addSeparator()
        self.menu_Recent_Files.addAction(self.actionClear)

    def selected_object_tree(self, index):
        """
        Called when the user selects a node in the Object Tree.

        Updates the current object, emits the preview update signal if Settings allows it,
        updates the possible children list, the properties list and wizard buttons.

        :param index: The selected node's index.
        """
        self.current_object = self.tree_model.itemFromIndex(index).xml_node
        self.object_tree_view.setCurrentIndex(index)
        if self.settings_dict["General"]["code_refresh"] >= 2:
            self.xml_code_changed.emit(self.current_object)

        self.update_box_list()
        self.update_props_list()
        self.update_wizard_button()

    def update_box_list(self):
        """
        Updates the possible children to add in Object Box.
        """
        spacer = self.layout_box.takeAt(self.layout_box.count() - 1)
        for index in reversed(range(self.layout_box.count())):
            widget = self.layout_box.takeAt(index).widget()
            if widget is not None:
                widget.deleteLater()

        for child in self.current_object.allowed_children:
            new_object = child()
            child_button = QPushButton(new_object.name)
            font_button = QFont()
            font_button.setPointSize(8)
            child_button.setFont(font_button)
            child_button.setMaximumSize(5000, 30)
            child_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            child_button.clicked.connect(lambda _, tag_=new_object.tag: self.selected_object_list(tag_))
            if not self.current_object.can_add_child(new_object):
                child_button.setEnabled(False)
            self.layout_box.addWidget(child_button)
        self.layout_box.addSpacerItem(spacer)

    def selected_object_list(self, tag):
        """
        Called when the user selects a possible child in the Object Box.

        Adds the child corresponding to the tag and updates the possible children list.

        :param tag: The tag of the child to add.
        """
        new_child = elem_factory(tag, self.current_object)
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

    def clear_prop_list(self):
        """
        Deletes all the properties from the Property Editor
        """
        self.current_prop_list.clear()
        for index in reversed(range(self.formLayout.count())):
            widget = self.formLayout.takeAt(index).widget()
            if widget is not None:
                widget.deleteLater()

    def update_props_list(self):
        """
        Updates the Property Editor's prop list. Deletes everything and
        then creates the list from the node's properties.
        """
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
        """
        Updates the wizard button, hides or shows it.
        """
        if self.current_object.wizard:
            self.wizard_button.show()
        else:
            self.wizard_button.hide()

    def run_wizard(self):
        """
        Called when the wizard button is clicked.

        Sets up the main window and runs the wizard.
        """
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

        kwargs = {"package_path": self.package_path}
        wizard = self.current_object.wizard(self, self.current_object, self.xml_code_changed, **kwargs)
        self.splitter.insertWidget(0, wizard)

        wizard.cancelled.connect(close)
        wizard.cancelled.connect(lambda: self.selected_object_tree(current_index))
        wizard.finished.connect(close)
        wizard.finished.connect(lambda: self.selected_object_tree(current_index))
        wizard.finished.connect(lambda: self.fomod_modified(True))

    def fomod_modified(self, changed):
        """
        Changes the modified state of the installer, according to the parameter.
        """
        if changed is False:
            self.fomod_changed = False
            self.setWindowTitle(self.package_name + " - " + self.original_title)
        else:
            self.fomod_changed = True
            self.setWindowTitle("*" + self.package_name + " - " + self.original_title)

    def check_fomod_state(self):
        """
        Checks whether the installer has unsaved changes.
        """
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
        """
        Override the Qt close event to account for unsaved changes.
        :param event:
        """
        answer = self.check_fomod_state()
        if answer == QMessageBox.Save:
            self.save()
        elif answer == QMessageBox.Discard:
            pass
        elif answer == QMessageBox.Cancel:
            event.ignore()


class SettingsDialog(settings_ui[0], settings_ui[1]):
    """
    The class for the settings window. Subclassed from QDialog and created in Qt Designer.
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.Dialog)

        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.check_valid_load.stateChanged.connect(self.update_valid_load)
        self.check_warn_load.stateChanged.connect(self.update_warn_load)
        self.check_valid_save.stateChanged.connect(self.update_valid_save)
        self.check_warn_save.stateChanged.connect(self.update_warn_save)

        config = read_settings()
        self.combo_code_refresh.setCurrentIndex(config["General"]["code_refresh"])
        self.check_intro.setChecked(config["General"]["show_intro"])
        self.check_advanced.setChecked(config["General"]["show_advanced"])
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
        config["General"]["show_intro"] = str(self.check_intro.isChecked()).lower()
        config["General"]["show_advanced"] = str(self.check_advanced.isChecked()).lower()
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
    """
    The class for the about window. Subclassed from QDialog and created in Qt Designer.
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.move(parent.window().frameGeometry().topLeft() + parent.window().rect().center() - self.rect().center())

        self.setWindowFlags(Qt.WindowTitleHint | Qt.Dialog)

        self.version.setText("Version: " + __version__)

        copyright_text = self.copyright.text()
        new_year = "2016-" + str(datetime.now().year) if datetime.now().year != 2016 else "2016"
        copyright_text = copyright_text.replace("2016", new_year)
        self.copyright.setText(copyright_text)

        self.button.clicked.connect(self.close)


def not_implemented():
    """
    A convenience function for something that has not yet been implemented.
    """
    generic_errorbox("Nope", "Sorry, this part hasn't been implemented yet!")


def generic_errorbox(title, text, detail=""):
    """
    A function that creates a generic errorbox with the logo_admin.png logo.

    :param title: A string containing the title of the errorbox.
    :param text: A string containing the text of the errorbox.
    :param detail: Optional. A string containing the detail text of the errorbox.
    """
    errorbox = QMessageBox()
    errorbox.setText(text)
    errorbox.setWindowTitle(title)
    errorbox.setDetailedText(detail)
    errorbox.setIconPixmap(QPixmap(join(cur_folder, "resources/logos/logo_admin.png")))
    errorbox.exec_()


def read_settings():
    """
    Reads the settings from the ~/.fomod/.designer file. If such a file does not exist it uses the default settings.
    The settings are processed to be ready to be used in Python code (p.e. "option=1" translates to True).

    :return: The processed settings.
    """
    default_settings = {"General": {"code_refresh": 3,
                                    "show_intro": True,
                                    "show_advanced": False},
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
    for section in default_settings:
        settings[section] = {}
        for key in default_settings[section]:
            if isinstance(default_settings[section][key], bool):
                settings[section][key] = config.getboolean(section, key)
            elif isinstance(default_settings[section][key], int):
                settings[section][key] = config.getint(section, key)
            elif isinstance(default_settings[section][key], float):
                settings[section][key] = config.getfloat(section, key)
            else:
                settings[section][key] = config.get(section, key)
    return settings
