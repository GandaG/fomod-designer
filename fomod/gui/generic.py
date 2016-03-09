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

from PyQt5 import QtWidgets, QtGui, QtCore
import templates.notimplemented as template


class NotImplementedDialog(QtWidgets.QDialog, template.Ui_Dialog):
    def __init__(self):
        super(NotImplementedDialog, self).__init__()
        self.setupUi(self)

        if __name__ == "__main__":
            self.label_2.setPixmap(QtGui.QPixmap("fomod/gui/logos/1456477754_user-admin.png"))
        else:
            self.label_2.setPixmap(QtGui.QPixmap("logos/1456477754_user-admin.png"))

        self.pushButton.clicked.connect(self.ok)

    def ok(self):
        self.hide()

        if __name__ == "__main__":
            QtCore.QCoreApplication.instance().quit()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = NotImplementedDialog()
    window.show()
    sys.exit(app.exec_())


# For testing and debugging.
if __name__ == "__main__":
    main()
