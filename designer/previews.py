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

from os.path import join, sep, normpath, isfile, isdir
from os import listdir
from queue import Queue
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QVBoxLayout, QRadioButton, QCheckBox, QHeaderView, QMenu, \
    QAction
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from lxml.etree import XML, tostring
from lxml.objectify import deannotate
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.html import XmlLexer
from . import cur_folder
from .io import sort_elements
from .ui_templates import preview_mo


class PreviewDispatcherThread(QThread):
    """
    Thread used to dispatch the element to each preview worker thread.

    :param queue: The main queue containing the elements to process.
    :param mo_signal: The signal to pass to the MO preview worker, updates the MO preview.
    :param nmm_signal: The signal to pass to the NMM preview worker, updates the NMM preview.
    :param code_signal: The signal to pass to the code preview worker, updates the code preview.
    """
    def __init__(self, queue, code_signal, **kwargs):
        super().__init__()
        self.queue = queue
        self.gui_queue = Queue()
        self.code_queue = Queue()

        self.code_thread = PreviewCodeWorker(self.code_queue, code_signal)
        self.code_thread.start()
        self.gui_thread = PreviewGuiWorker(self.gui_queue, **kwargs)
        self.gui_thread.start()

    def run(self):
        while True:
            # wait for next element
            element = self.queue.get()

            if element is not None:
                element.write_attribs()
                element.load_metadata()
                sort_elements(element)

            # dispatch to every queue
            self.gui_queue.put(element)
            self.code_queue.put(element)


class PreviewCodeWorker(QThread):
    """
    Takes a xml element, writes the code, highlights it with inline css and returns the html code.

    :param queue: The queue that receives the elements to be processed.
    :param return_signal: The signal used to send the return code through.
    :return: The highlighted element html code.
    """
    def __init__(self, queue, return_signal):
        super().__init__()
        self.queue = queue
        self.return_signal = return_signal

    def run(self):
        while True:
            # wait for next element
            element = self.queue.get()

            if element is None:
                self.return_signal.emit("")
                continue

            element = XML(tostring(element))

            # process the element
            deannotate(element, cleanup_namespaces=True)
            code = tostring(element, encoding="Unicode", pretty_print=True, xml_declaration=False)
            self.return_signal.emit(highlight(code, XmlLexer(), HtmlFormatter(
                noclasses=True, style="autumn", linenos="table"
            )))


class PreviewGuiWorker(QThread):
    class InstallStepData(object):
        def __init__(self, name):
            self.name = name
            self.group_list = []

        def set_group_list(self, group_list):
            self.group_list = group_list

        def sort_ascending(self):
            self.group_list = sorted(self.group_list, key=lambda x: x.name)

        def sort_descending(self):
            self.group_list = sorted(self.group_list, reverse=True, key=lambda x: x.name)

    class GroupData(object):
        def __init__(self, name, group_type):
            self.name = name
            self.type = group_type
            self.plugin_list = []

        def set_plugin_list(self, plugin_list):
            self.plugin_list = plugin_list

        def sort_ascending(self):
            self.plugin_list = sorted(self.plugin_list, key=lambda x: x.name)

        def sort_descending(self):
            self.plugin_list = sorted(self.plugin_list, reverse=True, key=lambda x: x.name)

    class PluginData(object):
        def __init__(self, name, description, image_path, file_list, folder_list, flag_list, plugin_type):
            self.name = name
            self.description = description
            self.image_path = image_path
            self.file_list = file_list
            self.folder_list = folder_list
            self.flag_list = flag_list
            self.type = plugin_type

    class FileData(object):
        def __init__(self, abs_source, rel_source, destination, priority, always_install, install_usable):
            self.abs_source = abs_source
            self.rel_source = rel_source
            self.destination = destination
            self.priority = priority
            self.always_install = always_install
            self.install_usable = install_usable

    class FolderData(FileData):
        pass

    class FlagData(object):
        def __init__(self, label, value):
            self.label = label
            self.value = value

    def __init__(self, queue, **kwargs):
        super().__init__()
        self.queue = queue
        self.kwargs = kwargs

    def run(self):
        while True:
            # wait for next element
            element = self.queue.get()

            if element is None:
                self.kwargs["gui_worker"].invalid_node_signal.emit()
                continue
            elif element.tag == "installStep":
                pass
            elif [elem for elem in element.iterancestors() if elem.tag == "installStep"]:
                element = [elem for elem in element.iterancestors() if elem.tag == "installStep"][0]
            elif not [elem for elem in self.kwargs["config_root"]().iter() if elem.tag == "installStep"]:
                self.kwargs["gui_worker"].missing_node_signal.emit()
                continue
            else:
                self.kwargs["gui_worker"].invalid_node_signal.emit()
                continue

            self.kwargs["gui_worker"].clear_tab_signal.emit()
            self.kwargs["gui_worker"].clear_ui_signal.emit()
            info_name = self.kwargs["info_root"]().find("Name").text \
                if self.kwargs["info_root"]().find("Name") is not None else ""
            info_author = self.kwargs["info_root"]().find("Author").text \
                if self.kwargs["info_root"]().find("Author") is not None else ""
            info_version = self.kwargs["info_root"]().find("Version").text \
                if self.kwargs["info_root"]().find("Version") is not None else ""
            info_website = self.kwargs["info_root"]().find("Website").text \
                if self.kwargs["info_root"]().find("Website") is not None else ""
            self.kwargs["gui_worker"].set_labels_signal.emit(info_name, info_author, info_version, info_website)

            step_data = self.InstallStepData(element.get("name"))
            opt_group_elem = element.find("optionalFileGroups")
            if opt_group_elem is not None:
                group_data_list = []

                for group_elem in opt_group_elem.findall("group"):
                    group_data = self.GroupData(group_elem.get("name"), group_elem.get("type"))

                    plugins_elem = group_elem.find("plugins")
                    if plugins_elem is not None:
                        plugin_data_list = []

                        for plugin_elem in plugins_elem.findall("plugin"):
                            name_ = plugin_elem.get("name")
                            description_ = plugin_elem.find("description").text \
                                if plugin_elem.find("description") is not None else ""
                            image_ = plugin_elem.find("image").get("path") \
                                if plugin_elem.find("image") is not None else ""
                            if image_:
                                # normalize path, for some reason normpath wasn't working
                                image_ = join(self.kwargs["package_path"](), image_).replace("\\", "/")
                                image_ = image_.replace("/", sep)

                            file_data_list = []
                            for file_elem in plugin_elem.findall("files/file"):
                                file_data_list.append(
                                    self.FileData(
                                        normpath(join(
                                            self.kwargs["package_path"](),
                                            file_elem.get("source").replace("\\", "/")
                                        )),
                                        file_elem.get("source"),
                                        normpath(file_elem.get("destination").replace("\\", "/")),
                                        file_elem.get("priority"),
                                        file_elem.get("alwaysInstall"),
                                        file_elem.get("installIfUsable")
                                    )
                                )

                            folder_data_list = []
                            for folder_elem in plugin_elem.findall("files/folder"):
                                folder_data_list.append(
                                    self.FolderData(
                                        normpath(join(
                                            self.kwargs["package_path"](),
                                            folder_elem.get("source").replace("\\", "/")
                                        )),
                                        folder_elem.get("source"),
                                        normpath(folder_elem.get("destination").replace("\\", "/")),
                                        folder_elem.get("priority"),
                                        folder_elem.get("alwaysInstall"),
                                        folder_elem.get("installIfUsable")
                                    )
                                )

                            flag_data_list = []
                            for flag_elem in plugin_elem.findall("conditionFlags/flag"):
                                flag_data_list.append(
                                    self.FlagData(
                                        flag_elem.get("name"),
                                        flag_elem.text
                                    )
                                )

                            type_elem = plugin_elem.find("typeDescriptor/type")
                            default_type_elem = plugin_elem.find("typeDescriptor/dependencyType/defaultType")
                            if type_elem is not None:
                                type_ = type_elem.get("name")
                            elif default_type_elem is not None:
                                type_ = default_type_elem.get("name")
                            else:
                                type_ = "Required"

                            plugin_data_list.append(
                                self.PluginData(
                                    name_,
                                    description_,
                                    image_,
                                    file_data_list,
                                    folder_data_list,
                                    flag_data_list,
                                    type_
                                )
                            )

                        group_data.set_plugin_list(plugin_data_list)
                        if plugins_elem.get("order") == "Ascending":
                            group_data.sort_ascending()
                        elif plugins_elem.get("order") == "Descending":
                            group_data.sort_descending()

                    group_data_list.append(group_data)

                step_data.set_group_list(group_data_list)
                if opt_group_elem.get("order") == "Ascending":
                    step_data.sort_ascending()
                elif opt_group_elem.get("order") == "Descending":
                    step_data.sort_descending()

            self.kwargs["gui_worker"].create_page_signal.emit(step_data)


class PreviewMoGui(QWidget, preview_mo.Ui_Form):
    clear_tab_signal = pyqtSignal()
    clear_ui_signal = pyqtSignal()
    invalid_node_signal = pyqtSignal()
    missing_node_signal = pyqtSignal()
    set_labels_signal = pyqtSignal([str, str, str, str])
    create_page_signal = pyqtSignal([object])

    class ScaledLabel(QLabel):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.original_pixmap = None
            self.setMinimumSize(320, 200)

        def set_scalable_pixmap(self, pixmap):
            self.original_pixmap = pixmap
            self.setPixmap(self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio))

        def resizeEvent(self, event):
            if self.pixmap() and self.original_pixmap:
                self.setPixmap(self.original_pixmap.scaled(event.size(), Qt.KeepAspectRatio))

    class PreviewItem(QStandardItem):
        def set_priority(self, value):
            self.priority = value

    def __init__(self, mo_preview_layout):
        super().__init__()
        self.mo_preview_layout = mo_preview_layout
        self.setupUi(self)
        self.mo_preview_layout.addWidget(self)
        self.label_image = self.ScaledLabel(self)
        self.splitter_label.addWidget(self.label_image)
        self.hide()

        self.button_preview_more.setIcon(QIcon(join(cur_folder, "resources/logos/logo_more.png")))
        self.button_preview_less.setIcon(QIcon(join(cur_folder, "resources/logos/logo_less.png")))
        self.button_preview_more.clicked.connect(self.button_preview_more.hide)
        self.button_preview_more.clicked.connect(self.button_preview_less.show)
        self.button_preview_more.clicked.connect(self.widget_preview.show)
        self.button_preview_less.clicked.connect(self.button_preview_less.hide)
        self.button_preview_less.clicked.connect(self.button_preview_more.show)
        self.button_preview_less.clicked.connect(self.widget_preview.hide)
        self.button_preview_more.clicked.emit()
        self.button_results_more.setIcon(QIcon(join(cur_folder, "resources/logos/logo_more.png")))
        self.button_results_less.setIcon(QIcon(join(cur_folder, "resources/logos/logo_less.png")))
        self.button_results_more.clicked.connect(self.button_results_more.hide)
        self.button_results_more.clicked.connect(self.button_results_less.show)
        self.button_results_more.clicked.connect(self.widget_results.show)
        self.button_results_less.clicked.connect(self.button_results_less.hide)
        self.button_results_less.clicked.connect(self.button_results_more.show)
        self.button_results_less.clicked.connect(self.widget_results.hide)
        self.button_results_less.clicked.emit()

        self.model_files = QStandardItemModel()
        self.tree_results.expanded.connect(
            lambda: self.tree_results.header().resizeSections(QHeaderView.Stretch)
        )
        self.tree_results.collapsed.connect(
            lambda: self.tree_results.header().resizeSections(QHeaderView.Stretch)
        )
        self.tree_results.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_results.customContextMenuRequested.connect(self.on_custom_context_menu)
        self.model_flags = QStandardItemModel()
        self.list_flags.expanded.connect(
            lambda: self.list_flags.header().resizeSections(QHeaderView.Stretch)
        )
        self.list_flags.collapsed.connect(
            lambda: self.list_flags.header().resizeSections(QHeaderView.Stretch)
        )
        self.reset_models()

        self.label_invalid = QLabel(
            "Select an Installation Step node or one of its children to preview its installer page."
        )
        self.label_invalid.setAlignment(Qt.AlignCenter)
        self.mo_preview_layout.addWidget(self.label_invalid)
        self.label_invalid.hide()

        self.label_missing = QLabel(
            "In order to preview an installer page, create an Installation Step node."
        )
        self.label_missing.setAlignment(Qt.AlignCenter)
        self.mo_preview_layout.addWidget(self.label_missing)
        self.label_missing.hide()

        self.clear_tab_signal.connect(self.clear_tab)
        self.clear_ui_signal.connect(self.clear_ui)
        self.invalid_node_signal.connect(self.invalid_node)
        self.missing_node_signal.connect(self.missing_node)
        self.set_labels_signal.connect(self.set_labels)
        self.create_page_signal.connect(self.create_page)

    def on_custom_context_menu(self, position):
        node_tree_context_menu = QMenu(self.tree_results)

        action_expand = QAction(QIcon(join(cur_folder, "resources/logos/logo_expand.png")), "Expand All", self)
        action_collapse = QAction(QIcon(join(cur_folder, "resources/logos/logo_collapse.png")), "Collapse All", self)

        action_expand.triggered.connect(self.tree_results.expandAll)
        action_collapse.triggered.connect(self.tree_results.collapseAll)

        node_tree_context_menu.addActions([action_expand, action_collapse])

        node_tree_context_menu.move(self.tree_results.mapToGlobal(position))
        node_tree_context_menu.exec_()

    def eventFilter(self, object_, event):
        if event.type() == QEvent.HoverEnter:
            self.label_description.setText(object_.property("description"))
            self.label_image.set_scalable_pixmap(QPixmap(object_.property("image_path")))

        return QWidget().eventFilter(object_, event)

    def clear_ui(self):
        self.label_name.clear()
        self.label_author.clear()
        self.label_version.clear()
        self.label_website.clear()
        self.label_description.clear()
        self.label_image.clear()
        [widget.deleteLater() for widget in [
            self.layout_widget.itemAt(index).widget() for index in range(self.layout_widget.count())
            if self.layout_widget.itemAt(index).widget()
            ]]
        self.reset_models()

    def reset_models(self):
        self.model_files.clear()
        self.model_files.setHorizontalHeaderLabels(["Files Preview", "Source", "Plugin"])
        self.model_files_root = QStandardItem(QIcon(join(cur_folder, "resources/logos/logo_folder.png")), "<root>")
        self.model_files.appendRow(self.model_files_root)
        self.tree_results.setModel(self.model_files)
        self.model_flags.clear()
        self.model_flags.setHorizontalHeaderLabels(["Flag Label", "Flag Value", "Plugin"])
        self.list_flags.setModel(self.model_flags)

    def clear_tab(self):
        for index in reversed(range(self.mo_preview_layout.count())):
            widget = self.mo_preview_layout.itemAt(index).widget()
            if widget is not None:
                widget.hide()

    def invalid_node(self):
        self.clear_tab()
        self.label_invalid.show()

    def missing_node(self):
        self.clear_tab()
        self.label_missing.show()

    def set_labels(self, name, author, version, website):
        self.label_name.setText(name)
        self.label_author.setText(author)
        self.label_version.setText(version)
        self.label_website.setText("<a href = {}>link</a>".format(website))

    # this is pretty horrendous, need to come up with a better way of doing this.
    def create_page(self, page_data):
        group_step = QGroupBox(page_data.name)
        layout_step = QVBoxLayout()
        group_step.setLayout(layout_step)

        check_first_radio = True
        for group in page_data.group_list:
            group_group = QGroupBox(group.name)
            layout_group = QVBoxLayout()
            group_group.setLayout(layout_group)

            for plugin in group.plugin_list:
                if group.type in ["SelectAny", "SelectAll", "SelectAtLeastOne"]:
                    button_plugin = QCheckBox(plugin.name, self)

                    if group.type == "SelectAll":
                        button_plugin.setChecked(True)
                        button_plugin.setEnabled(False)
                    elif group.type == "SelectAtLeastOne":
                        button_plugin.toggled.connect(
                            lambda checked, button=button_plugin: button.setChecked(True)
                            if not checked and not [
                                button for button in [
                                    layout_group.itemAt(index).widget() for index in range(layout_group.count())
                                    if layout_group.itemAt(index).widget()
                                ] if button.isChecked()
                            ]
                            else None
                        )

                elif group.type in ["SelectExactlyOne", "SelectAtMostOne"]:
                    button_plugin = QRadioButton(plugin.name, self)
                    if check_first_radio and not button_plugin.isChecked():
                        button_plugin.animateClick(0)
                        check_first_radio = False

                button_plugin.setProperty("description", plugin.description)
                button_plugin.setProperty("image_path", plugin.image_path)
                button_plugin.setProperty("file_list", plugin.file_list)
                button_plugin.setProperty("folder_list", plugin.folder_list)
                button_plugin.setProperty("flag_list", plugin.flag_list)
                button_plugin.setProperty("type", plugin.type)
                button_plugin.setAttribute(Qt.WA_Hover)

                if plugin.type == "Required":
                    button_plugin.setEnabled(False)
                elif plugin.type == "Recommended":
                    button_plugin.animateClick(0) if not button_plugin.isChecked() else None
                elif plugin.type == "NotUsable":
                    button_plugin.setChecked(False)
                    button_plugin.setEnabled(False)

                button_plugin.toggled.connect(self.reset_models)
                button_plugin.toggled.connect(self.update_installed_files)
                button_plugin.toggled.connect(self.update_set_flags)

                button_plugin.installEventFilter(self)
                button_plugin.setObjectName("preview_button")
                layout_group.addWidget(button_plugin)

            if group.type == "SelectAtMostOne":
                button_none = QRadioButton("None")
                layout_group.addWidget(button_none)

            layout_step.addWidget(group_group)

        self.layout_widget.addWidget(group_step)
        self.reset_models()
        self.update_installed_files()
        self.update_set_flags()
        self.show()

    def update_installed_files(self):
        def recurse_add_items(folder, parent):
            for boop in listdir(folder):  # I was very tired
                if isdir(join(folder, boop)):
                    folder_item = None
                    existing_folder_ = self.model_files.findItems(boop, Qt.MatchRecursive)
                    if existing_folder_:
                        for boopity in existing_folder_:
                            if boopity.parent() is parent:
                                folder_item = boopity
                                break
                    if not folder_item:
                        folder_item = self.PreviewItem(
                            QIcon(join(cur_folder, "resources/logos/logo_folder.png")),
                            boop
                        )
                        folder_item.set_priority(folder_.priority)
                        parent.appendRow([folder_item, QStandardItem(rel_source), QStandardItem(button.text())])
                    recurse_add_items(join(folder, boop), folder_item)

                elif isfile(join(folder, boop)):
                    file_item_ = None
                    existing_file_ = self.model_files.findItems(boop, Qt.MatchRecursive)
                    if existing_file_:
                        for boopity in existing_file_:
                            if boopity.parent() is parent:
                                if folder_.priority < boopity.priority:
                                    file_item_ = boopity
                                    break
                                else:
                                    parent.removeRow(boopity.row())
                                    break
                    if not file_item_:
                        file_item_ = self.PreviewItem(
                            QIcon(join(cur_folder, "resources/logos/logo_file.png")),
                            boop
                        )
                        file_item_.set_priority(folder_.priority)
                        parent.appendRow([file_item_, QStandardItem(rel_source), QStandardItem(button.text())])

        for button in self.findChildren((QCheckBox, QRadioButton), "preview_button"):
            for folder_ in button.property("folder_list"):
                if (button.isChecked() and button.property("type") != "NotUsable" or
                        folder_.always_install or
                        folder_.install_usable and button.property("type") != "NotUsable" or
                        button.property("type") == "Required"):
                    destination = folder_.destination
                    abs_source = folder_.abs_source
                    rel_source = folder_.rel_source
                    parent_item = self.model_files_root

                    destination_split = destination.split("/")
                    if destination_split[0] == ".":
                        destination_split = destination_split[1:]
                    for dest_folder in destination_split:
                        existing_folder_list = self.model_files.findItems(dest_folder, Qt.MatchRecursive)
                        if existing_folder_list:
                            for existing_folder in existing_folder_list:
                                if existing_folder.parent() is parent_item:
                                    parent_item = existing_folder
                                    break
                            continue
                        item_ = self.PreviewItem(
                            QIcon(join(cur_folder, "resources/logos/logo_folder.png")),
                            dest_folder
                        )
                        item_.set_priority(folder_.priority)
                        parent_item.appendRow([item_, QStandardItem(), QStandardItem(button.text())])
                        parent_item = item_

                    if isdir(abs_source):
                        recurse_add_items(abs_source, parent_item)

            for file_ in button.property("file_list"):
                if (button.isChecked() and button.property("type") != "NotUsable" or
                        file_.always_install or
                        file_.install_usable and button.property("type") != "NotUsable" or
                        button.property("type") == "Required"):
                    destination = file_.destination
                    abs_source = file_.abs_source
                    rel_source = file_.rel_source
                    parent_item = self.model_files_root

                    destination_split = destination.split("/")
                    if destination_split[0] == ".":
                        destination_split = destination_split[1:]
                    for dest_folder in destination_split:
                        existing_folder_list = self.model_files.findItems(dest_folder, Qt.MatchRecursive)
                        if existing_folder_list:
                            for existing_folder in existing_folder_list:
                                if existing_folder.parent() is parent_item:
                                    parent_item = existing_folder
                                    break
                            continue
                        item_ = self.PreviewItem(
                            QIcon(join(cur_folder, "resources/logos/logo_folder.png")),
                            dest_folder
                        )
                        item_.set_priority(file_.priority)
                        parent_item.appendRow([item_, QStandardItem(), QStandardItem(button.text())])
                        parent_item = item_

                    source_file = abs_source.split("/")[len(abs_source.split("/")) - 1]
                    file_item = None
                    existing_file_list = self.model_files.findItems(source_file, Qt.MatchRecursive)
                    if existing_file_list:
                        for existing_file in existing_file_list:
                            if existing_file.parent() is parent_item:
                                if file_.priority < existing_file.priority:
                                    file_item = existing_file
                                    break
                                else:
                                    parent_item.removeRow(existing_file.row())
                                    break
                    if not file_item:
                        file_item = self.PreviewItem(
                            QIcon(join(cur_folder, "resources/logos/logo_file.png")),
                            source_file
                        )
                        file_item.set_priority(file_.priority)
                        parent_item.appendRow([file_item, QStandardItem(rel_source), QStandardItem(button.text())])

        self.tree_results.header().resizeSections(QHeaderView.Stretch)

    def update_set_flags(self):
        for button in self.findChildren((QCheckBox, QRadioButton), "preview_button"):
            if button.isChecked():
                for flag in button.property("flag_list"):
                    flag_label = QStandardItem(flag.label)
                    flag_value = QStandardItem(flag.value)
                    flag_plugin = QStandardItem(button.text())
                    existing_flag = self.model_flags.findItems(flag.label)
                    if existing_flag:
                        previous_flag_row = existing_flag[0].row()
                        self.model_flags.removeRow(previous_flag_row)
                        self.model_flags.insertRow(previous_flag_row, [flag_label, flag_value, flag_plugin])
                    else:
                        self.model_flags.appendRow([flag_label, flag_value, flag_plugin])

        self.list_flags.header().resizeSections(QHeaderView.Stretch)
