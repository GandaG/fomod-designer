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

from PyQt5 import QtWidgets, QtGui
from .templates import mainframe as template


class MainFrame(QtWidgets.QMainWindow, template.Ui_MainWindow):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.setupUi(self)

        icon_open = QtGui.QIcon()
        icon_open.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477639_file.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon_open)

        icon_save = QtGui.QIcon()
        icon_save.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477689_disc-floopy.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon_save)

        icon_options = QtGui.QIcon()
        icon_options.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477700_configuration.png"),
                               QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionO_ptions.setIcon(icon_options)

        icon_refresh = QtGui.QIcon()
        icon_refresh.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477730_refresh.png"),
                               QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Refresh.setIcon(icon_refresh)

        icon_delete = QtGui.QIcon()
        icon_delete.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477717_error.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Delete.setIcon(icon_delete)

        icon_about = QtGui.QIcon()
        icon_about.addPixmap(QtGui.QPixmap("fomod/gui/logos/1457582962_notepad.png"),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_About.setIcon(icon_about)

        icon_help = QtGui.QIcon()
        icon_help.addPixmap(QtGui.QPixmap("fomod/gui/logos/1457582991_info.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHe_lp.setIcon(icon_help)

        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.actionO_ptions.triggered.connect(self.options)
        self.action_Refresh.triggered.connect(self.refresh)
        self.action_Delete.triggered.connect(self.delete)
        self.actionHe_lp.triggered.connect(self.help)
        self.action_About.triggered.connect(self.about)

        self.object_tree_view.activated.connect(self.selected_object_tree)
        self.object_box_list.activated.connect(self.selected_object_list)

        self.original_title = self.windowTitle()
        self.package_path = ""
        self.info_root = None
        self.config_root = None
        self.current_item = None
        self.current_object = None
        self.current_children_list = []
        self.tree_model = QtGui.QStandardItemModel()
        self.list_model = QtGui.QStandardItemModel()

        self.object_tree_view.setModel(self.tree_model)
        self.object_tree_view.header().hide()
        self.object_box_list.setModel(self.list_model)

    def open(self):
        from os.path import expanduser, normpath, basename
        from ..parser import parse

        open_dialog = QtWidgets.QFileDialog()
        self.package_path = open_dialog.getExistingDirectory(self, "Select package root directory:", expanduser("~"))

        if self.package_path:
            self.info_root, self.config_root = parse(normpath(self.package_path))

            self.tree_model.appendRow(self.info_root.model_item)
            self.tree_model.appendRow(self.config_root.model_item)

            title = basename(normpath(self.package_path)) + " - " + self.original_title
            self.setWindowTitle(title)

    def save(self):
        from ..serializer import serialize

        if self.info_root and self.config_root:
            serialize(self.info_root, self.config_root, self.package_path)

    def options(self):
        from . import generic
        generic.main()

    def refresh(self):
        from . import generic
        generic.main()

    def delete(self):
        try:
            if self.current_object:
                object_to_delete = self.current_object
                object_to_delete.parent.remove_child(object_to_delete)

                new_index = self.tree_model.indexFromItem(self.current_object.parent.model_item)
                self.selected_object_tree(new_index)
            else:
                errorbox = QtWidgets.QMessageBox()
                errorbox.setText("You can't delete nothing... Try to select something before deleting.")
                errorbox.setWindowTitle("What are trying to do? o.O")
                errorbox.setIconPixmap(QtGui.QPixmap("fomod/gui/logos/1456477754_user-admin.png"))
                errorbox.exec_()
        except AttributeError:
            errorbox = QtWidgets.QMessageBox()
            errorbox.setText("You can't delete root objects!")
            errorbox.setWindowTitle("You can't do that...")
            errorbox.setIconPixmap(QtGui.QPixmap("fomod/gui/logos/1456477754_user-admin.png"))
            errorbox.exec_()

    def help(self):
        from . import generic
        generic.main()

    def about(self):
        from . import generic
        generic.main()

    def selected_object_tree(self, index):
        from ..exceptions import InstanceCreationException, AddChildException

        def check_item(self, node, item):
            if node.model_item is item:
                self.current_item = item
                self.current_object = node

                for child in node.allowed_children:
                    new_item = child()
                    try:
                        node.can_add_child(new_item)
                    except (InstanceCreationException, AddChildException):
                        continue

                    self.list_model.appendRow(new_item.model_item)
                    self.current_children_list.append(new_item)
                return True

            return False

        self.list_model.clear()
        self.current_children_list.clear()

        item = self.tree_model.itemFromIndex(index)
        for node in self.info_root.iter():
            if check_item(self, node, item):
                return

        for node in self.config_root.iter():
            if check_item(self, node, item):
                return

    def selected_object_list(self, index):
        item = self.list_model.itemFromIndex(index)

        for child in self.current_children_list:
            if child.model_item is item:
                new_child = type(child)()
                self.current_object.add_child(new_child)

                # reload the object box and expand the item
                current_index = self.tree_model.indexFromItem(self.current_item)
                self.selected_object_tree(current_index)
                self.object_tree_view.expand(current_index)


def main():
    window = MainFrame()
    window.exec_()


# For testing and debugging.
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainFrame()
    window.show()
    sys.exit(app.exec_())
