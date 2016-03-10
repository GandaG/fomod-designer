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
import templates.mainframe as template


class MainFrame(QtWidgets.QMainWindow, template.Ui_MainWindow):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477402_add.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_New.setIcon(icon)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477639_file.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon1)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477689_disc-floopy.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon2)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477799_disc-cd.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_AS.setIcon(icon3)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477700_configuration.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionO_ptions.setIcon(icon4)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477730_refresh.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Refresh.setIcon(icon5)

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("fomod/gui/logos/1456477717_error.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Delete.setIcon(icon6)

        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("fomod/gui/logos/1457582962_notepad.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_About.setIcon(icon7)

        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("fomod/gui/logos/1457582991_info.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHe_lp.setIcon(icon8)

        self.action_New.triggered.connect(self.new)
        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.actionSave_AS.triggered.connect(self.save_as)
        self.actionO_ptions.triggered.connect(self.options)
        self.action_Refresh.triggered.connect(self.refresh)
        self.action_Delete.triggered.connect(self.delete)
        self.actionHe_lp.triggered.connect(self.help)
        self.action_About.triggered.connect(self.about)

    def new(self):
        import generic
        generic.main()

    def open(self):
        import generic
        generic.main()

    def save(self):
        import generic
        generic.main()

    def save_as(self):
        import generic
        generic.main()

    def options(self):
        import generic
        generic.main()

    def refresh(self):
        import generic
        generic.main()

    def delete(self):
        import generic
        generic.main()

    def help(self):
        import generic
        generic.main()

    def about(self):
        import generic
        generic.main()


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
