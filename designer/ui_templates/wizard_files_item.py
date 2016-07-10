# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/templates/wizard_files_item.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_base(object):
    def setupUi(self, base):
        base.setObjectName("base")
        base.resize(396, 24)
        self.layout_main = QtWidgets.QHBoxLayout(base)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setObjectName("layout_main")
        self.label_source = QtWidgets.QLabel(base)
        self.label_source.setObjectName("label_source")
        self.layout_main.addWidget(self.label_source)
        self.edit_source = QtWidgets.QLineEdit(base)
        self.edit_source.setObjectName("edit_source")
        self.layout_main.addWidget(self.edit_source)
        self.button_source = QtWidgets.QPushButton(base)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_source.sizePolicy().hasHeightForWidth())
        self.button_source.setSizePolicy(sizePolicy)
        self.button_source.setMaximumSize(QtCore.QSize(50, 16777215))
        self.button_source.setObjectName("button_source")
        self.layout_main.addWidget(self.button_source)
        self.label_dest = QtWidgets.QLabel(base)
        self.label_dest.setObjectName("label_dest")
        self.layout_main.addWidget(self.label_dest)
        self.edit_dest = QtWidgets.QLineEdit(base)
        self.edit_dest.setObjectName("edit_dest")
        self.layout_main.addWidget(self.edit_dest)
        self.button_delete = QtWidgets.QPushButton(base)
        self.button_delete.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../logos/logo_cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_delete.setIcon(icon)
        self.button_delete.setObjectName("button_delete")
        self.layout_main.addWidget(self.button_delete)

        self.retranslateUi(base)
        QtCore.QMetaObject.connectSlotsByName(base)

    def retranslateUi(self, base):
        _translate = QtCore.QCoreApplication.translate
        base.setWindowTitle(_translate("base", "Form"))
        self.label_source.setText(_translate("base", "Source:"))
        self.button_source.setText(_translate("base", "..."))
        self.label_dest.setText(_translate("base", "Destination:"))

