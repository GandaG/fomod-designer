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
from io import BytesIO
from threading import Thread
from queue import Queue
from webbrowser import open as web_open
from datetime import datetime
from collections import deque
from json import JSONDecodeError
from jsonpickle import encode, decode, set_encoder_options
from lxml.etree import parse, tostring
from PyQt5.QtWidgets import (QFileDialog, QColorDialog, QMessageBox, QLabel, QHBoxLayout, QCommandLinkButton, QDialog,
                             QFormLayout, QLineEdit, QSpinBox, QComboBox, QWidget, QPushButton, QSizePolicy, QStatusBar,
                             QCompleter, QApplication, QMainWindow)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont, QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSignal, QStringListModel, QMimeData
from requests import get, codes, ConnectionError, Timeout
from validator import validate_tree, check_warnings, ValidatorError
from . import cur_folder, __version__
from .io import import_, new, export, sort_elements, elem_factory, copy_element
from .previews import PreviewDispatcherThread
from .props import PropertyFile, PropertyColour, PropertyFolder, PropertyCombo, PropertyInt, PropertyText, \
    PropertyFlagLabel, PropertyFlagValue
from .exceptions import DesignerError
from .ui_templates import window_intro, window_mainframe, window_about, window_settings


class IntroWindow(QMainWindow, window_intro.Ui_MainWindow):
    """
    The class for the intro window. Subclassed from QDialog and created in Qt Designer.
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(join(cur_folder, "resources/window_icon.svg")))
        self.setWindowTitle("FOMOD Designer")
        self.version.setText("Version " + __version__)

        self.settings_dict = read_settings()
        recent_files = self.settings_dict["Recent Files"]
        for path in recent_files:
            if not isdir(path):
                recent_files.remove(path)
                continue
            button = QCommandLinkButton(basename(path), path, self)
            button.setIcon(QIcon(join(cur_folder, "resources/logos/logo_enter.png")))
            button.clicked.connect(lambda _, path_=path: self.open_path(path_))
            self.scroll_layout.addWidget(button)

        if not self.settings_dict["General"]["show_intro"]:
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
        self.settings_dict["General"]["show_intro"] = not self.check_intro.isChecked()
        self.settings_dict["General"]["show_advanced"] = self.check_advanced.isChecked()
        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            set_encoder_options("json", indent=4)
            configfile.write(encode(self.settings_dict))

        main_window = MainFrame()
        main_window.move(self.pos())
        main_window.open(path)
        main_window.show()
        self.close()


class MainFrame(QMainWindow, window_mainframe.Ui_MainWindow):
    """
    The class for the main window. Subclassed from QMainWindow and created in Qt Designer.
    """

    class NodeMimeData(QMimeData):
        def __init__(self):
            super().__init__()
            self._node = None
            self._item = None
            self._original_item = None

        def has_node(self):
            if self._node is None:
                return False
            else:
                return True

        def node(self):
            return self._node

        def set_node(self, node):
            self._node = node

        def has_item(self):
            if self._item is None:
                return False
            else:
                return True

        def item(self):
            return self._item

        def set_item(self, item):
            self._item = item

        def original_item(self):
            return self._original_item

        def set_original_item(self, item):
            self._original_item = item

    class NodeStandardModel(QStandardItemModel):
        def mimeData(self, index_list):
            if not index_list:
                return 0

            mime_data = MainFrame.NodeMimeData()
            new_node = copy_element(self.itemFromIndex(index_list[0]).xml_node)
            mime_data.set_item(new_node.model_item)
            mime_data.set_node(new_node)
            mime_data.set_original_item(self.itemFromIndex(index_list[0]))
            return mime_data

        def canDropMimeData(self, mime_data, drop_action, row, col, parent_index):
            if self.itemFromIndex(parent_index) and mime_data.has_node() and mime_data.has_item() and drop_action == 2:
                if isinstance(self.itemFromIndex(parent_index).xml_node, type(mime_data.node().getparent())):
                    return True
                else:
                    return False
            else:
                return False

        def dropMimeData(self, mime_data, drop_action, row, col, parent_index):
            if not self.canDropMimeData(mime_data, drop_action, row, col, parent_index):
                return False

            parent = self.itemFromIndex(drop_action)
            xml_node = mime_data.node()
            parent.insertRow(row, xml_node.model_item)
            for row_index in range(0, parent.rowCount()):
                if parent.child(row_index) == mime_data.original_item():
                    continue
                parent.child(row_index).xml_node.user_sort_order = str(parent.child(row_index).row()).zfill(7)
                parent.child(row_index).xml_node.save_metadata()
            return True

        def supportedDragActions(self):
            return Qt.MoveAction

    #: Signals the xml code has changed.
    xml_code_changed = pyqtSignal([object])

    #: Signals the mo preview is updated.
    update_mo_preview = pyqtSignal([QWidget])

    #: Signals the nmm preview is updated.
    update_nmm_preview = pyqtSignal([QWidget])

    #: Signals the code preview is updated.
    update_code_preview = pyqtSignal([str])

    #: Signals there is an update available.
    update_check_update_available = pyqtSignal()

    #: Signals the app is up-to-date.
    update_check_up_to_date = pyqtSignal()

    #: Signals a connection timed out.
    update_check_timeout = pyqtSignal()

    #: Signals there was an error with the internet connection.
    update_check_connection_error = pyqtSignal()

    #: Signals a new node has been selected in the node tree.
    node_selected = pyqtSignal([object])

    #: Signals the previews need to be updated.
    update_previews = pyqtSignal([object])

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
        self.actionCopy.setIcon(QIcon(join(cur_folder, "resources/logos/logo_copy.png")))
        self.actionPaste.setIcon(QIcon(join(cur_folder, "resources/logos/logo_paste.png")))

        # manage node tree model
        self.node_tree_model = self.NodeStandardModel()
        self.node_tree_view.setModel(self.node_tree_model)
        self.node_tree_model.itemChanged.connect(lambda item: item.xml_node.save_metadata())
        self.node_tree_model.itemChanged.connect(lambda item: self.xml_code_changed.emit(item.xml_node))

        # setup any additional info left from designer
        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.actionO_ptions.triggered.connect(self.settings)
        self.action_Refresh.triggered.connect(self.refresh)
        self.action_Delete.triggered.connect(self.delete)
        self.actionHe_lp.triggered.connect(self.help)
        self.action_About.triggered.connect(lambda _, self_=self: self.about(self_))
        self.actionClear.triggered.connect(self.clear_recent_files)
        self.actionCopy.triggered.connect(
            lambda: self.copy_item_to_clipboard(
                self.node_tree_model.itemFromIndex(
                    self.node_tree_view.selectedIndexes()[0]
                ),
                self.node_tree_model
            )
            if self.node_tree_view.selectedIndexes() else None
        )
        self.actionPaste.triggered.connect(
            lambda: self.paste_item_from_clipboard(
                self.node_tree_model.itemFromIndex(
                    self.node_tree_view.selectedIndexes()[0]
                ),
                self.statusBar()
            )
            if self.node_tree_view.selectedIndexes() else None
        )

        self.action_Object_Tree.toggled.connect(self.node_tree.setVisible)
        self.actionObject_Box.toggled.connect(self.children_box.setVisible)
        self.action_Property_Editor.toggled.connect(self.property_editor.setVisible)

        self.node_tree.visibilityChanged.connect(self.action_Object_Tree.setChecked)
        self.children_box.visibilityChanged.connect(self.actionObject_Box.setChecked)
        self.property_editor.visibilityChanged.connect(self.action_Property_Editor.setChecked)

        self.node_tree_view.clicked.connect(self.node_selected.emit)
        self.node_tree_view.activated.connect(self.node_selected.emit)

        self.fomod_changed = False
        self.original_title = self.windowTitle()
        self.package_path = ""
        self.package_name = ""
        self.settings_dict = read_settings()
        self.info_root = None
        self.config_root = None
        self.current_node = None
        self.current_prop_list = []

        # start the preview threads
        self.preview_queue = Queue()
        self.update_previews.connect(self.preview_queue.put)
        self.update_code_preview.connect(self.xml_code_browser.setHtml)
        self.preview_thread = PreviewDispatcherThread(
            self.preview_queue,
            self.update_mo_preview,
            self.update_nmm_preview,
            self.update_code_preview
        )
        self.preview_thread.start()

        # manage the wizard button
        self.button_wizard.clicked.connect(self.run_wizard)

        # manage auto-completion
        self.flag_label_model = QStringListModel()
        self.flag_label_completer = QCompleter()
        self.flag_label_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.flag_label_completer.setModel(self.flag_label_model)
        self.flag_value_model = QStringListModel()
        self.flag_value_completer = QCompleter()
        self.flag_value_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.flag_value_completer.setModel(self.flag_value_model)

        # connect node selected signal
        self.node_selected.connect(
            lambda index: self.set_current_node(self.node_tree_model.itemFromIndex(index).xml_node)
        )
        self.node_selected.connect(lambda index: self.node_tree_view.setCurrentIndex(index))
        self.node_selected.connect(
            lambda: self.update_previews.emit(self.current_node)
            if self.settings_dict["General"]["code_refresh"] >= 2 else None
        )
        self.node_selected.connect(self.update_children_box)
        self.node_selected.connect(self.update_props_list)
        self.node_selected.connect(
            lambda: self.button_wizard.setEnabled(False)
            if self.current_node.wizard is None else self.button_wizard.setEnabled(True)
        )

        # manage code changed signal
        self.xml_code_changed.connect(lambda: self.fomod_modified(True))
        self.xml_code_changed.connect(self.update_previews.emit)

        self.update_recent_files()
        self.check_updates()

    def set_current_node(self, node_):
        self.current_node = node_

    @staticmethod
    def copy_item_to_clipboard(item, model):
        QApplication.clipboard().setMimeData(model.mimeData([model.indexFromItem(item)]))

    @staticmethod
    def paste_item_from_clipboard(parent_item, status_bar):
        new_node = copy_element(QApplication.clipboard().mimeData().node())
        if not parent_item.xml_node.can_add_child(new_node):
            status_bar.showMessage("This parent is not valid!")
        else:
            parent_item.xml_node.append(new_node)
            parent_item.appendRow(new_node.model_item)
            parent_item.sortChildren(0)

    @staticmethod
    def update_flag_label_completer(label_model, elem_root):
        label_list = []
        for elem in elem_root.iter():
            if elem.tag == "flag":
                value = elem.properties["name"].value
                if value not in label_list:
                    label_list.append(value)
        label_model.setStringList(label_list)

    @staticmethod
    def update_flag_value_completer(value_model, elem_root, label):
        value_list = []
        for elem in elem_root.iter():
            if elem.tag == "flag" and elem.text not in value_list and elem.properties["name"].value == label:
                value_list.append(elem.text)
        value_model.setStringList(value_list)

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
                    self.update_check_update_available.emit()
                else:
                    self.update_check_up_to_date.emit()
            except Timeout:
                self.update_check_timeout.emit()
            except ConnectionError:
                self.update_check_connection_error.emit()

        self.update_check_up_to_date.connect(lambda: self.setStatusBar(QStatusBar()))
        self.update_check_up_to_date.connect(lambda: self.statusBar().addWidget(QLabel("Everything is up-to-date.")))
        self.update_check_update_available.connect(lambda: self.setStatusBar(QStatusBar()))
        self.update_check_update_available.connect(update_available_button)
        self.update_check_timeout.connect(lambda: self.setStatusBar(QStatusBar()))
        self.update_check_timeout.connect(lambda: self.statusBar().addWidget(QLabel("Connection timed out.")))
        self.update_check_connection_error.connect(lambda: self.setStatusBar(QStatusBar()))
        self.update_check_connection_error.connect(
            lambda: self.statusBar().addWidget(QLabel(
                "Could not connect to remote server, check your internet connection."
            ))
        )

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
                        validate_tree(
                            parse(BytesIO(tostring(config_root, pretty_print=True))),
                            join(cur_folder, "resources", "mod_schema.xsd"),
                            self.settings_dict["Load"]["validate_ignore"]
                        )
                    if self.settings_dict["Load"]["warnings"]:
                        check_warnings(
                            package_path,
                            config_root,
                            self.settings_dict["Save"]["warn_ignore"]
                        )
                else:
                    info_root, config_root = new()

                self.package_path = package_path
                self.info_root, self.config_root = info_root, config_root

                self.node_tree_model.clear()

                self.node_tree_model.appendRow(self.info_root.model_item)
                self.node_tree_model.appendRow(self.config_root.model_item)

                self.package_name = basename(normpath(self.package_path))
                self.current_node = None
                self.xml_code_changed.emit(self.current_node)
                self.fomod_modified(False)
                self.update_recent_files(self.package_path)
                self.clear_prop_list()
                self.button_wizard.setEnabled(False)
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
                sort_elements(self.info_root)
                sort_elements(self.config_root)
                if self.settings_dict["Save"]["validate"]:
                    validate_tree(
                        parse(BytesIO(tostring(self.config_root, pretty_print=True))),
                        join(cur_folder, "resources", "mod_schema.xsd"),
                        self.settings_dict["Save"]["validate_ignore"]
                    )
                if self.settings_dict["Save"]["warnings"]:
                    check_warnings(
                        self.package_path,
                        self.config_root,
                        self.settings_dict["Save"]["warn_ignore"]
                    )
                export(self.info_root, self.config_root, self.package_path)
                self.fomod_modified(False)
        except ValidatorError as e:
            generic_errorbox(e.title, str(e))
            return

    def settings(self):
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
            self.update_previews.emit(self.current_node)

    def delete(self):
        """
        Deletes the current node in the tree. No effect when using the Basic View.
        """
        try:
            if self.current_node is not None:
                object_to_delete = self.current_node
                new_index = self.node_tree_model.indexFromItem(self.current_node.getparent().model_item)
                object_to_delete.getparent().remove_child(object_to_delete)
                self.fomod_modified(True)
                self.node_selected.emit(new_index)
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
        self.settings_dict["Recent Files"].clear()
        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            set_encoder_options("json", indent=4)
            configfile.write(encode(self.settings_dict))

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
        file_list = deque(self.settings_dict["Recent Files"], maxlen=5)
        self.clear_recent_files()

        # check for invalid paths and remove them
        for path in file_list:
            if not isdir(path):
                file_list.remove(path)

        # check if the path is new or if it already exists - delete the last one or reorder respectively
        if add_new:
            if add_new in file_list:
                file_list.remove(add_new)
            file_list.appendleft(add_new)

        # write the new list to the settings file
        self.settings_dict["Recent Files"] = file_list
        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            set_encoder_options("json", indent=4)
            configfile.write(encode(self.settings_dict))

        # populate the gui menu with the new files list
        self.menu_Recent_Files.removeAction(self.actionClear)
        for path in self.settings_dict["Recent Files"]:
            action = self.menu_Recent_Files.addAction(path)
            action.triggered.connect(lambda _, path_=path: self.open(path_))
        self.menu_Recent_Files.addSeparator()
        self.menu_Recent_Files.addAction(self.actionClear)

    def update_children_box(self):
        """
        Updates the possible children to add in Object Box.
        """
        spacer = self.layout_box.takeAt(self.layout_box.count() - 1)
        for index in reversed(range(self.layout_box.count())):
            widget = self.layout_box.takeAt(index).widget()
            if widget is not None:
                widget.deleteLater()

        for child in self.current_node.allowed_children:
            new_object = child()
            child_button = QPushButton(new_object.name)
            font_button = QFont()
            font_button.setPointSize(8)
            child_button.setFont(font_button)
            child_button.setMaximumSize(5000, 30)
            child_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            child_button.setStatusTip("A possible child node.")
            child_button.clicked.connect(lambda _, tag_=new_object.tag: self.child_selected(tag_))
            if not self.current_node.can_add_child(new_object):
                child_button.setEnabled(False)
            if child in self.current_node.required_children:
                child_button.setStyleSheet("background-color: " + QColor("#ba4d0e").name())#FFD9D9
                child_button.setStatusTip("A red button indicates that at least one of this node is required.")
            if child in self.current_node.either_children_group:
                child_button.setStyleSheet("background-color: " + QColor("#ffaa7f").name())
                child_button.setStatusTip("An orange button indicates that only one of these buttons must be used.")
            if child in self.current_node.at_least_one_children_group:
                child_button.setStyleSheet("background-color: " + QColor("#d0d02e").name())#FFFFD9
                child_button.setStatusTip(
                    "A yellow button indicates that from all the yellow buttons, at least one is required."
                )
            self.layout_box.addWidget(child_button)
        self.layout_box.addSpacerItem(spacer)

    def child_selected(self, tag):
        """
        Called when the user selects a possible child in the Object Box.

        Adds the child corresponding to the tag and updates the possible children list.

        :param tag: The tag of the child to add.
        """
        new_child = elem_factory(tag, self.current_node)
        defaults_dict = self.settings_dict["Defaults"]
        if tag in defaults_dict and defaults_dict[tag].enabled():
            new_child.properties[defaults_dict[tag].key()].set_value(defaults_dict[tag].value())
        self.current_node.add_child(new_child)
        self.node_tree_model.sort(0)

        # expand the parent
        current_index = self.node_tree_model.indexFromItem(self.current_node.model_item)
        self.node_tree_view.expand(current_index)

        # select the new item
        self.node_tree_view.setCurrentIndex(self.node_tree_model.indexFromItem(new_child.model_item))
        self.node_selected.emit(self.node_tree_model.indexFromItem(new_child.model_item))

        # reload the object box
        self.update_children_box()

    def clear_prop_list(self):
        """
        Deletes all the properties from the Property Editor
        """
        self.current_prop_list.clear()
        for index in reversed(range(self.layout_prop_editor.count())):
            widget = self.layout_prop_editor.takeAt(index).widget()
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
        props = self.current_node.properties

        for key in props:
            if not props[key].editable:
                continue

            label = QLabel(self.dockWidgetContents)
            label.setObjectName("label_" + str(prop_index))
            label.setText(props[key].name)
            self.layout_prop_editor.setWidget(prop_index, QFormLayout.LabelRole, label)

            if type(props[key]) is PropertyText:
                prop_list.append(QLineEdit(self.dockWidgetContents))
                prop_list[prop_index].setText(props[key].value)
                prop_list[prop_index].textEdited[str].connect(props[key].set_value)
                prop_list[prop_index].textEdited[str].connect(self.current_node.write_attribs)
                prop_list[prop_index].textEdited[str].connect(self.current_node.update_item_name)
                prop_list[prop_index].textEdited[str].connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )

            if type(props[key]) is PropertyFlagLabel:
                prop_list.append(QLineEdit(self.dockWidgetContents))
                self.update_flag_label_completer(self.flag_label_model, self.config_root)
                self.flag_label_completer.activated[str].connect(prop_list[prop_index].setText)
                prop_list[prop_index].setCompleter(self.flag_label_completer)
                prop_list[prop_index].textChanged[str].connect(
                    lambda text: self.update_flag_value_completer(self.flag_value_model, self.config_root, text)
                )
                prop_list[prop_index].setText(props[key].value)
                prop_list[prop_index].textChanged[str].connect(props[key].set_value)
                prop_list[prop_index].textChanged[str].connect(self.current_node.write_attribs)
                prop_list[prop_index].textChanged[str].connect(self.current_node.update_item_name)
                prop_list[prop_index].textChanged[str].connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )

            if type(props[key]) is PropertyFlagValue:
                prop_list.append(QLineEdit(self.dockWidgetContents))
                prop_list[prop_index].setCompleter(self.flag_value_completer)
                self.flag_value_completer.activated[str].connect(prop_list[prop_index].setText)
                prop_list[prop_index].setText(props[key].value)
                prop_list[prop_index].textChanged[str].connect(props[key].set_value)
                prop_list[prop_index].textChanged[str].connect(self.current_node.write_attribs)
                prop_list[prop_index].textChanged[str].connect(self.current_node.update_item_name)
                prop_list[prop_index].textChanged[str].connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )

            elif type(props[key]) is PropertyInt:
                prop_list.append(QSpinBox(self.dockWidgetContents))
                prop_list[prop_index].setValue(int(props[key].value))
                prop_list[prop_index].setMinimum(props[key].min)
                prop_list[prop_index].setMaximum(props[key].max)
                prop_list[prop_index].valueChanged.connect(props[key].set_value)
                prop_list[prop_index].valueChanged.connect(self.current_node.write_attribs)
                prop_list[prop_index].valueChanged.connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )

            elif type(props[key]) is PropertyCombo:
                prop_list.append(QComboBox(self.dockWidgetContents))
                prop_list[prop_index].insertItems(0, props[key].values)
                prop_list[prop_index].setCurrentIndex(props[key].values.index(props[key].value))
                prop_list[prop_index].activated[str].connect(props[key].set_value)
                prop_list[prop_index].activated[str].connect(self.current_node.write_attribs)
                prop_list[prop_index].activated[str].connect(self.current_node.update_item_name)
                prop_list[prop_index].activated[str].connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )

            elif type(props[key]) is PropertyFile:
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
                line_edit.textChanged[str].connect(self.current_node.write_attribs)
                line_edit.textChanged[str].connect(self.current_node.update_item_name)
                line_edit.textChanged[str].connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )
                path_button.clicked.connect(button_clicked)

            elif type(props[key]) is PropertyFolder:
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
                line_edit.textChanged.connect(self.current_node.write_attribs)
                line_edit.textChanged.connect(self.current_node.update_item_name)
                line_edit.textChanged.connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )
                path_button.clicked.connect(button_clicked)

            elif type(props[key]) is PropertyColour:
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
                line_edit.textChanged.connect(self.current_node.write_attribs)
                line_edit.textChanged.connect(
                    lambda: self.xml_code_changed.emit(self.current_node)
                    if self.settings_dict["General"]["code_refresh"] >= 3 else None
                )
                path_button.clicked.connect(button_clicked)

            self.layout_prop_editor.setWidget(prop_index, QFormLayout.FieldRole, prop_list[prop_index])
            prop_list[prop_index].setObjectName(str(prop_index))
            prop_index += 1

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

        current_index = self.node_tree_model.indexFromItem(self.current_node.model_item)
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
        wizard = self.current_node.wizard(self, self.current_node, self.xml_code_changed, **kwargs)
        self.splitter.insertWidget(0, wizard)

        wizard.cancelled.connect(close)
        wizard.cancelled.connect(lambda: self.node_selected.emit(current_index))
        wizard.finished.connect(close)
        wizard.finished.connect(lambda: self.node_selected.emit(current_index))

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


class SettingsDialog(QDialog, window_settings.Ui_Dialog):
    """
    The class for the settings window. Subclassed from QDialog and created in Qt Designer.
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.Dialog)

        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.close)

        self.check_valid_load.stateChanged.connect(self.check_valid_load_ignore.setEnabled)
        self.check_warn_load.stateChanged.connect(self.check_warn_load_ignore.setEnabled)
        self.check_valid_save.stateChanged.connect(self.check_valid_save_ignore.setEnabled)
        self.check_warn_save.stateChanged.connect(self.check_warn_save_ignore.setEnabled)

        self.check_installSteps.stateChanged.connect(self.combo_installSteps.setEnabled)
        self.check_optionalFileGroups.stateChanged.connect(self.combo_optionalFileGroups.setEnabled)
        self.check_type.stateChanged.connect(self.combo_type.setEnabled)
        self.check_defaultType.stateChanged.connect(self.combo_defaultType.setEnabled)

        self.settings_dict = read_settings()
        self.combo_code_refresh.setCurrentIndex(self.settings_dict["General"]["code_refresh"])
        self.check_intro.setChecked(self.settings_dict["General"]["show_intro"])
        self.check_advanced.setChecked(self.settings_dict["General"]["show_advanced"])

        self.check_valid_load.setChecked(self.settings_dict["Load"]["validate"])
        self.check_valid_load_ignore.setChecked(self.settings_dict["Load"]["validate_ignore"])
        self.check_warn_load.setChecked(self.settings_dict["Load"]["warnings"])
        self.check_warn_load_ignore.setChecked(self.settings_dict["Load"]["warn_ignore"])

        self.check_valid_save.setChecked(self.settings_dict["Save"]["validate"])
        self.check_valid_save_ignore.setChecked(self.settings_dict["Save"]["validate_ignore"])
        self.check_warn_save.setChecked(self.settings_dict["Save"]["warnings"])
        self.check_warn_save_ignore.setChecked(self.settings_dict["Save"]["warn_ignore"])

        self.check_installSteps.setChecked(self.settings_dict["Defaults"]["installSteps"].enabled())
        self.combo_installSteps.setEnabled(self.settings_dict["Defaults"]["installSteps"].enabled())
        self.combo_installSteps.setCurrentText(self.settings_dict["Defaults"]["installSteps"].value())
        self.check_optionalFileGroups.setChecked(self.settings_dict["Defaults"]["optionalFileGroups"].enabled())
        self.combo_optionalFileGroups.setEnabled(self.settings_dict["Defaults"]["optionalFileGroups"].enabled())
        self.combo_optionalFileGroups.setCurrentText(self.settings_dict["Defaults"]["optionalFileGroups"].value())
        self.check_type.setChecked(self.settings_dict["Defaults"]["type"].enabled())
        self.combo_type.setEnabled(self.settings_dict["Defaults"]["type"].enabled())
        self.combo_type.setCurrentText(self.settings_dict["Defaults"]["type"].value())
        self.check_defaultType.setChecked(self.settings_dict["Defaults"]["defaultType"].enabled())
        self.combo_defaultType.setEnabled(self.settings_dict["Defaults"]["defaultType"].enabled())
        self.combo_defaultType.setCurrentText(self.settings_dict["Defaults"]["defaultType"].value())

    def accepted(self):
        self.settings_dict["General"]["code_refresh"] = self.combo_code_refresh.currentIndex()
        self.settings_dict["General"]["show_intro"] = self.check_intro.isChecked()
        self.settings_dict["General"]["show_advanced"] = self.check_advanced.isChecked()

        self.settings_dict["Load"]["validate"] = self.check_valid_load.isChecked()
        self.settings_dict["Load"]["validate_ignore"] = self.check_valid_load_ignore.isChecked()
        self.settings_dict["Load"]["warnings"] = self.check_warn_load.isChecked()
        self.settings_dict["Load"]["warn_ignore"] = self.check_warn_load_ignore.isChecked()

        self.settings_dict["Save"]["validate"] = self.check_valid_save.isChecked()
        self.settings_dict["Save"]["validate_ignore"] = self.check_valid_save_ignore.isChecked()
        self.settings_dict["Save"]["warnings"] = self.check_warn_save.isChecked()
        self.settings_dict["Save"]["warn_ignore"] = self.check_warn_save_ignore.isChecked()

        self.settings_dict["Defaults"]["installSteps"].set_enabled(self.check_installSteps.isChecked())
        self.settings_dict["Defaults"]["installSteps"].set_value(self.combo_installSteps.currentText())

        self.settings_dict["Defaults"]["optionalFileGroups"].set_enabled(self.check_optionalFileGroups.isChecked())
        self.settings_dict["Defaults"]["optionalFileGroups"].set_value(self.combo_optionalFileGroups.currentText()
                                                                       )
        self.settings_dict["Defaults"]["type"].set_enabled(self.check_type.isChecked())
        self.settings_dict["Defaults"]["type"].set_value(self.combo_type.currentText())

        self.settings_dict["Defaults"]["defaultType"].set_enabled(self.check_defaultType.isChecked())
        self.settings_dict["Defaults"]["defaultType"].set_value(self.combo_defaultType.currentText())

        makedirs(join(expanduser("~"), ".fomod"), exist_ok=True)
        with open(join(expanduser("~"), ".fomod", ".designer"), "w") as configfile:
            set_encoder_options("json", indent=4)
            configfile.write(encode(self.settings_dict))

        self.close()


class About(QDialog, window_about.Ui_Dialog):
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
    class DefaultsSettings(object):
        def __init__(self, key, default_enabled, default_value):
            self.__enabled = default_enabled
            self.__property_key = key
            self.__property_value = default_value

        def set_enabled(self, enabled):
            self.__enabled = enabled

        def set_value(self, value):
            self.__property_value = value

        def enabled(self):
            return self.__enabled

        def value(self):
            return self.__property_value

        def key(self):
            return self.__property_key

    def deep_merge(a, b, path=None):
        """merges b into a"""
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    deep_merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                elif isinstance(b[key], type(a[key])):
                    a[key] = b[key]
                elif not isinstance(b[key], type(a[key])):
                    pass  # user has messed with conf files
                else:
                    raise Exception('Conflict at {}'.format('.'.join(path + [str(key)])))
            else:
                a[key] = b[key]
        return a

    default_settings = {
        "General": {
            "code_refresh": 3,
            "show_intro": True,
            "show_advanced": False
        },
        "Defaults": {
            "installSteps": DefaultsSettings("order", True, "Explicit"),
            "optionalFileGroups": DefaultsSettings("order", True, "Explicit"),
            "type": DefaultsSettings("name", True, "Optional"),
            "defaultType": DefaultsSettings("name", True, "Optional"),
        },
        "Load": {
            "validate": True,
            "validate_ignore": False,
            "warnings": True,
            "warn_ignore": True
        },
        "Save": {
            "validate": True,
            "validate_ignore": False,
            "warnings": True,
            "warn_ignore": True
        },
        "Recent Files": deque(maxlen=5)
    }

    try:
        with open(join(expanduser("~"), ".fomod", ".designer"), "r") as configfile:
            settings_dict = decode(configfile.read())
        deep_merge(default_settings, settings_dict)
        return default_settings
    except (FileNotFoundError, JSONDecodeError):
        return default_settings
