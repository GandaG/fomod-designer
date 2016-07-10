# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/templates/tutorial_advanced.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1115, 659)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.button_exit = QtWidgets.QPushButton(Dialog)
        self.button_exit.setGeometry(QtCore.QRect(270, 640, 581, 21))
        self.button_exit.setObjectName("button_exit")
        self.frame_node = QtWidgets.QFrame(Dialog)
        self.frame_node.setGeometry(QtCore.QRect(20, 210, 241, 121))
        self.frame_node.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_node.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_node.setObjectName("frame_node")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_node)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_node)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.frame_preview = QtWidgets.QFrame(Dialog)
        self.frame_preview.setGeometry(QtCore.QRect(270, 230, 551, 111))
        self.frame_preview.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_preview.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_preview.setObjectName("frame_preview")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_preview)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame_preview)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.frame_prop = QtWidgets.QFrame(Dialog)
        self.frame_prop.setGeometry(QtCore.QRect(850, 10, 241, 271))
        self.frame_prop.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_prop.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_prop.setObjectName("frame_prop")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_prop)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame_prop)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.frame_child = QtWidgets.QFrame(Dialog)
        self.frame_child.setGeometry(QtCore.QRect(850, 320, 241, 271))
        self.frame_child.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_child.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_child.setObjectName("frame_child")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_child)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.frame_child)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.button_exit.setText(_translate("Dialog", "Continue"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">This is the Node Tree.</span></p><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">Here you\'ll find the nodes that make up your installer.</span></p><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">You can navigate the tree with the little arrows on the left side of each node.</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">These are the Preview Tabs.</span></p><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">Here you can preview what your installer looks like and what the XML code will be once you save.</span></p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">This is the Property Editor.</span></p><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">Here you can edit the individual properties each node has.</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">This is the Children Box.</span></p><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">Here you can view which children nodes are available to the currently selected node and add them if possible.</span></p><p align=\"center\"><span style=\" font-size:14pt; color:#0c10da;\">You can only have one of some children while others are available infinitely.</span></p></body></html>"))

