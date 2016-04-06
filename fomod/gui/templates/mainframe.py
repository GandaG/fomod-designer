# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fomod/gui/templates/mainframe.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 563)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.preview_label = QtWidgets.QLabel(self.centralwidget)
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_label.setWordWrap(True)
        self.preview_label.setObjectName("preview_label")
        self.horizontalLayout_3.addWidget(self.preview_label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu_Tools = QtWidgets.QMenu(self.menubar)
        self.menu_Tools.setObjectName("menu_Tools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.property_editor = QtWidgets.QDockWidget(MainWindow)
        self.property_editor.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.property_editor.setObjectName("property_editor")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.formLayout = QtWidgets.QFormLayout(self.dockWidgetContents)
        self.formLayout.setObjectName("formLayout")
        self.property_editor.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.property_editor)
        self.object_tree = QtWidgets.QDockWidget(MainWindow)
        self.object_tree.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.object_tree.setObjectName("object_tree")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.object_tree_view = QtWidgets.QTreeView(self.dockWidgetContents_2)
        self.object_tree_view.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.object_tree_view.sizePolicy().hasHeightForWidth())
        self.object_tree_view.setSizePolicy(sizePolicy)
        self.object_tree_view.setMinimumSize(QtCore.QSize(151, 0))
        self.object_tree_view.setObjectName("object_tree_view")
        self.horizontalLayout.addWidget(self.object_tree_view)
        self.object_tree.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.object_tree)
        self.object_box = QtWidgets.QDockWidget(MainWindow)
        self.object_box.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.object_box.setObjectName("object_box")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.object_box_list = QtWidgets.QListView(self.dockWidgetContents_3)
        self.object_box_list.setObjectName("object_box_list")
        self.horizontalLayout_2.addWidget(self.object_box_list)
        self.object_box.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.object_box)
        self.action_Open = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../logos/1456477639_file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../logos/1456477689_disc-floopy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon1)
        self.action_Save.setObjectName("action_Save")
        self.actionO_ptions = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../logos/1456477700_configuration.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionO_ptions.setIcon(icon2)
        self.actionO_ptions.setObjectName("actionO_ptions")
        self.action_Refresh = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../logos/1456477730_refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Refresh.setIcon(icon3)
        self.action_Refresh.setObjectName("action_Refresh")
        self.action_Delete = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../logos/1456477717_error.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Delete.setIcon(icon4)
        self.action_Delete.setObjectName("action_Delete")
        self.action_About = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../logos/1457582962_notepad.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_About.setIcon(icon5)
        self.action_About.setObjectName("action_About")
        self.actionHe_lp = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../logos/1457582991_info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHe_lp.setIcon(icon6)
        self.actionHe_lp.setObjectName("actionHe_lp")
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionO_ptions)
        self.menu_Tools.addAction(self.action_Refresh)
        self.menu_Tools.addAction(self.action_Delete)
        self.menuHelp.addAction(self.action_About)
        self.menuHelp.addAction(self.actionHe_lp)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionO_ptions)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Refresh)
        self.toolBar.addAction(self.action_Delete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_About)
        self.toolBar.addAction(self.actionHe_lp)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FOMOD Designer"))
        self.preview_label.setText(_translate("MainWindow", "<html><head/><body><p>The preview is not ready yet!</p><p>Meanwhile, try to install your mod using NMM or MO to check if everything is ok.</p></body></html>"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menu_Tools.setTitle(_translate("MainWindow", "&Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.property_editor.setWindowTitle(_translate("MainWindow", "Property Editor"))
        self.object_tree.setWindowTitle(_translate("MainWindow", "Object Tree"))
        self.object_box.setWindowTitle(_translate("MainWindow", "Object Box"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.action_Open.setToolTip(_translate("MainWindow", "New/Open"))
        self.action_Open.setShortcut(_translate("MainWindow", "Ctrl+N, Ctrl+O"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionO_ptions.setText(_translate("MainWindow", "O&ptions"))
        self.actionO_ptions.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.action_Refresh.setText(_translate("MainWindow", "&Refresh"))
        self.action_Refresh.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.action_Delete.setText(_translate("MainWindow", "&Delete"))
        self.action_Delete.setShortcut(_translate("MainWindow", "Ctrl+D, Del"))
        self.action_About.setText(_translate("MainWindow", "&About"))
        self.action_About.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionHe_lp.setText(_translate("MainWindow", "He&lp"))
        self.actionHe_lp.setShortcut(_translate("MainWindow", "Ctrl+H"))

