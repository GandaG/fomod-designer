# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/templates/wizard_dependtype_pattern.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(345, 31)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.combo_type = QtWidgets.QComboBox(Form)
        self.combo_type.setObjectName("combo_type")
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.horizontalLayout.addWidget(self.combo_type)
        self.button_depend = QtWidgets.QPushButton(Form)
        self.button_depend.setObjectName("button_depend")
        self.horizontalLayout.addWidget(self.button_depend)
        self.button_delete = QtWidgets.QPushButton(Form)
        self.button_delete.setMaximumSize(QtCore.QSize(30, 16777215))
        self.button_delete.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../logos/logo_cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_delete.setIcon(icon)
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout.addWidget(self.button_delete)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Type:"))
        self.combo_type.setItemText(0, _translate("Form", "Required"))
        self.combo_type.setItemText(1, _translate("Form", "Optional"))
        self.combo_type.setItemText(2, _translate("Form", "Recommended"))
        self.button_depend.setText(_translate("Form", "Manage Dependencies"))

