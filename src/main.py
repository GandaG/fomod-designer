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

import sys
from pathlib import Path

import pyfomod
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from metadata import Metadata
from utils import RESOURCE_FOLDER, excepthook

MAINWINDOW_UI = uic.loadUiType(RESOURCE_FOLDER / "mainwindow.ui")


class MainWindow(*MAINWINDOW_UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.package_path = None
        self.fomod = None
        self.current_widget = None
        self.metadata = None

        self.widget_index.setEnabled(False)

        self.button_metadata.clicked.connect(self.open_metadata)

        self.widget_page_order.setStyleSheet("background-color:red;")
        self.widget_page_order.hide()

        self.page_model = QtGui.QStandardItemModel()
        self.list_pages.setModel(self.page_model)
        self.button_add.clicked.connect(self.new_page)
        self.button_delete.clicked.connect(self.remove_page)

    def open_metadata(self) -> None:
        if self.metadata is None:
            self.metadata = Metadata(self.fomod, self.package_path)
        if self.current_widget is None:
            self.widget_work.layout().addWidget(self.metadata)
        else:
            self.layout_central.replaceWidget(self.current_widget, self.metadata)
        self.current_widget = self.metadata

    def new_page(self) -> None:
        page = pyfomod.Page()
        self.fomod.pages.append(page)
        self.add_page(page)

    def add_page(self, page: pyfomod.Page) -> None:
        item = QtGui.QStandardItem(page.name)
        item.page = page
        self.page_model.appendRow(item)

    def remove_page(self) -> None:
        try:
            index = self.list_pages.selectedIndexes()[0]
        except IndexError:
            return
        item = self.page_model.item(index.row(), index.column())
        page = item.page
        self.fomod.pages.remove(page)
        self.page_model.removeRow(index.row())

    def load(self, path: str) -> None:
        try:
            self.fomod = pyfomod.parse(path)
        except FileNotFoundError:
            pass  # XXX fixme
        self.package_path = Path(path)

        if self.fomod.pages.order is not pyfomod.Order.EXPLICIT:
            self.widget_page_order.show()

        self.page_model.clear()
        for page in self.fomod.pages:
            self.add_page(page)

        self.widget_index.setEnabled(True)


def main() -> int:
    sys.excepthook = excepthook
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.load(str(Path("../pyfomod/tests/package_test").resolve()))
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
