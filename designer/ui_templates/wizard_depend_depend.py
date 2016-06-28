# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/templates/wizard_depend_depend.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550, 130)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_type = QtWidgets.QLabel(Form)
        self.label_type.setText("")
        self.label_type.setObjectName("label_type")
        self.horizontalLayout.addWidget(self.label_type)
        self.button_more = QtWidgets.QPushButton(Form)
        self.button_more.setObjectName("button_more")
        self.horizontalLayout.addWidget(self.button_more)
        self.button_less = QtWidgets.QPushButton(Form)
        self.button_less.setObjectName("button_less")
        self.horizontalLayout.addWidget(self.button_less)
        self.button_edit = QtWidgets.QPushButton(Form)
        self.button_edit.setObjectName("button_edit")
        self.horizontalLayout.addWidget(self.button_edit)
        self.button_delete = QtWidgets.QPushButton(Form)
        self.button_delete.setMaximumSize(QtCore.QSize(30, 16777215))
        self.button_delete.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../logos/logo_cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_delete.setIcon(icon)
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout.addWidget(self.button_delete)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setGeometry(QtCore.QRect(0, 0, 542, 81))
        self.scroll_widget.setObjectName("scroll_widget")
        self.layout_depend_depend = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.layout_depend_depend.setContentsMargins(0, 0, 0, 0)
        self.layout_depend_depend.setSpacing(6)
        self.layout_depend_depend.setObjectName("layout_depend_depend")
        spacerItem = QtWidgets.QSpacerItem(20, 265, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_depend_depend.addItem(spacerItem)
        self.scrollArea.setWidget(self.scroll_widget)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Type:"))
        self.button_more.setText(_translate("Form", "More..."))
        self.button_less.setText(_translate("Form", "Less..."))
        self.button_edit.setText(_translate("Form", "Edit"))

