# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/templates/wizard_depend_depend_depend.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(345, 30)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_number = QtWidgets.QLabel(Form)
        self.label_number.setText("")
        self.label_number.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_number.setObjectName("label_number")
        self.horizontalLayout.addWidget(self.label_number)
        self.label_depend = QtWidgets.QLabel(Form)
        self.label_depend.setObjectName("label_depend")
        self.horizontalLayout.addWidget(self.label_depend)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_depend.setText(_translate("Form", "Sub-Dependency"))

