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
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget
from PyQt5.QtCore import pyqtSignal
from .exceptions import BaseInstanceException


class _PageBase(QWidget):
    __metaclass__ = ABCMeta

    def __init__(self, wizard):
        super().__init__(wizard)
        if type(self) is _PageBase:
            raise BaseInstanceException(self)

    @abstractmethod
    def __create_buttons(self):
        pass


class PageSimple(_PageBase):
    def __init__(self, wizard):
        super().__init__(wizard)

    def __create_buttons(self):
        return


class _PageComplex(_PageBase):
    def __init__(self, wizard):
        super().__init__(wizard)
        if type(self) is _PageComplex:
            raise BaseInstanceException(self)

        self.main_widget = QWidget(self)
        self.button_set = self.__create_buttons()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.addWidget(self.main_widget)
        self.main_layout.addWidget(self.button_set)

    @abstractmethod
    def __create_buttons(self):
        pass


class PageInitial(_PageComplex):
    def __init__(self, wizard):
        super().__init__(wizard)
        self.next_clicked = pyqtSignal()
        self.cancel_clicked = pyqtSignal()

    def __create_buttons(self):
        next_button = QPushButton(self)
        next_button.setText("Next")
        next_button.clicked.connect(self.next_clicked.emit())
        cancel_button = QPushButton(self)
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.cancel_clicked.emit())
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(next_button)
        layout.addWidget(cancel_button)
        return layout


class PageMiddle(_PageComplex):
    def __init__(self, wizard):
        super().__init__(wizard)
        self.next_clicked = pyqtSignal()
        self.previous_clicked = pyqtSignal()
        self.cancel_clicked = pyqtSignal()

    def __create_buttons(self):
        previous_button = QPushButton(self)
        previous_button.setText("Previous")
        previous_button.clicked.connect(self.previous_clicked.emit())
        next_button = QPushButton(self)
        next_button.setText("Next")
        next_button.clicked.connect(self.next_clicked.emit())
        cancel_button = QPushButton(self)
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.cancel_clicked.emit())
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(previous_button)
        layout.addWidget(next_button)
        layout.addWidget(cancel_button)
        return layout


class PageFinal(_PageComplex):
    def __init__(self, wizard):
        super().__init__(wizard)
        self.finish_clicked = pyqtSignal()
        self.previous_clicked = pyqtSignal()
        self.cancel_clicked = pyqtSignal()

    def __create_buttons(self):
        previous_button = QPushButton(self)
        previous_button.setText("Previous")
        previous_button.clicked.connect(self.previous_clicked.emit())
        finish_button = QPushButton(self)
        finish_button.setText("Finish")
        finish_button.clicked.connect(self.finish_clicked.emit())
        cancel_button = QPushButton(self)
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.cancel_clicked.emit())
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(previous_button)
        layout.addWidget(finish_button)
        layout.addWidget(cancel_button)
        return layout


class _WizardBase(QStackedWidget):
    __metaclass__ = ABCMeta

    def __init__(self, parent=None):
        super().__init__(parent)
        if type(self) is _WizardBase:
            raise BaseInstanceException(self)

        self.return_data = None
        self.pages = self.add_pages()

    @abstractmethod
    def process_results(self):
        pass

    @abstractmethod
    def add_pages(self):
        return []


class _WizardSimple(_WizardBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        if type(self) is _WizardSimple:
            raise BaseInstanceException(self)

    @abstractmethod
    def process_results(self):
        pass

    @abstractmethod
    def add_pages(self):
        return []


class _WizardComplex(_WizardBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        if type(self) is _WizardComplex:
            raise BaseInstanceException(self)

        self.initial_page = PageInitial(self)
        self.initial_page.next_clicked.connect(self.next_page)
        self.initial_page.cancel_clicked.connect(self.cancelled_wizard.emit())
        self.final_page = PageFinal(self)
        self.final_page.previous_clicked.connect(self.previous_page)
        self.final_page.finish_clicked.connect(self.finished_wizard.emit(self.process_results()))
        self.final_page.cancel_clicked.connect(self.cancelled_wizard.emit())

        self.cancelled_wizard = pyqtSignal()
        self.finished_wizard = pyqtSignal()

        for page in self.pages:
            page.previous_clicked.connect(self.previous_page)
            page.next_clicked.connect(self.next_page)
            page.cancel_clicked.connect(self.cancelled_wizard.emit())

        self.pages.insert(0, self.initial_page)
        self.pages.append(self.final_page)

    @abstractmethod
    def process_results(self):
        pass

    @abstractmethod
    def initial_page(self):
        return PageInitial(self)

    @abstractmethod
    def add_pages(self):
        return []

    @abstractmethod
    def final_page(self):
        return PageFinal(self)

    def next_page(self):
        self.setCurrentIndex(self.pages.index(self.sender()) + 1)

    def previous_page(self):
        self.setCurrentIndex(self.pages.index(self.sender()) - 1)
