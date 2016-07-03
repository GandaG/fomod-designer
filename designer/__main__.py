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

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from .exceptions import excepthook
from .gui import IntroWindow, read_settings


def main():
    sys.excepthook = excepthook

    settings = read_settings()
    if settings["Appearance"]["style"]:
        QApplication.setStyle(settings["Appearance"]["style"])
    app = QApplication(sys.argv)
    if settings["Appearance"]["palette"]:
        app.setPalette(QPalette(QColor(settings["Appearance"]["palette"])))
    IntroWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
