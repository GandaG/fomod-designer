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

from PyQt5 import QtWidgets
from .templates import intro as template
from .. import __version__


class IntroWindow(QtWidgets.QMainWindow, template.Ui_MainWindow):
    def __init__(self):
        super(IntroWindow, self).__init__()
        self.setupUi(self)

        self.version.setText("Version %s" % __version__)

        self.new_button.clicked.connect(self.new)
        self.open_button.clicked.connect(self.open)

    def new(self):
        from . import generic
        generic.not_implemented()

    def open(self):
        from . import generic
        generic.not_implemented()


def main():
    window = IntroWindow()
    window.exec_()


# For testing and debugging.
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = IntroWindow()
    window.show()
    sys.exit(app.exec_())
