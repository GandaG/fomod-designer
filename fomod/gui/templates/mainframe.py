# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates/mainframe.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 563)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 2, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setMinimumSize(QtCore.QSize(151, 0))
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setRowCount(13)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(5)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(25)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tableWidget, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu_Tools = QtWidgets.QMenu(self.menubar)
        self.menu_Tools.setObjectName("menu_Tools")
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
        self.action_New = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../fomod/gui/logos/1456477402_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_New.setIcon(icon)
        self.action_New.setObjectName("action_New")
        self.action_Open = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../fomod/gui/logos/1456477639_file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon1)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../fomod/gui/logos/1456477689_disc-floopy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon2)
        self.action_Save.setObjectName("action_Save")
        self.actionSave_AS = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../fomod/gui/logos/1456477799_disc-cd.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_AS.setIcon(icon3)
        self.actionSave_AS.setObjectName("actionSave_AS")
        self.actionO_ptions = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../fomod/gui/logos/1456477700_configuration.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionO_ptions.setIcon(icon4)
        self.actionO_ptions.setObjectName("actionO_ptions")
        self.action_Refresh = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../fomod/gui/logos/1456477730_refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Refresh.setIcon(icon5)
        self.action_Refresh.setObjectName("action_Refresh")
        self.action_Delete = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../fomod/gui/logos/1456477717_error.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Delete.setIcon(icon6)
        self.action_Delete.setObjectName("action_Delete")
        self.menuFile.addAction(self.action_New)
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addAction(self.actionSave_AS)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionO_ptions)
        self.menu_Tools.addAction(self.action_Refresh)
        self.menu_Tools.addAction(self.action_Delete)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.toolBar.addAction(self.action_New)
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addAction(self.actionSave_AS)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionO_ptions)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Refresh)
        self.toolBar.addAction(self.action_Delete)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Object Tree"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Designer"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "XML"))
        self.label.setText(_translate("MainWindow", "Property Editor"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menu_Tools.setTitle(_translate("MainWindow", "&Tools"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_New.setText(_translate("MainWindow", "&New"))
        self.action_New.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.action_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_AS.setText(_translate("MainWindow", "Sa&ve As..."))
        self.actionSave_AS.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionO_ptions.setText(_translate("MainWindow", "O&ptions"))
        self.actionO_ptions.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.action_Refresh.setText(_translate("MainWindow", "&Refresh"))
        self.action_Refresh.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.action_Delete.setText(_translate("MainWindow", "&Delete"))
        self.action_Delete.setShortcut(_translate("MainWindow", "Ctrl+D"))

