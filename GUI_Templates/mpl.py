# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mpl.ui'
#
# Created: Mon Nov 24 15:07:00 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(512, 384)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(512, 384))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_6 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.mpl = MplWidget(self.centralwidget)
        self.mpl.setObjectName(_fromUtf8("mpl"))
        self.gridLayout_6.addWidget(self.mpl, 0, 0, 1, 1)
        self.Button_Grid = QtGui.QGridLayout()
        self.Button_Grid.setObjectName(_fromUtf8("Button_Grid"))
        self.pushButton_clear = QtGui.QPushButton(self.centralwidget)
        self.pushButton_clear.setObjectName(_fromUtf8("pushButton_clear"))
        self.Button_Grid.addWidget(self.pushButton_clear, 0, 2, 1, 1)
        self.toolbar_grid = QtGui.QGridLayout()
        self.toolbar_grid.setObjectName(_fromUtf8("toolbar_grid"))
        self.Button_Grid.addLayout(self.toolbar_grid, 0, 0, 1, 1)
        self.pushButton_plot = QtGui.QPushButton(self.centralwidget)
        self.pushButton_plot.setObjectName(_fromUtf8("pushButton_plot"))
        self.Button_Grid.addWidget(self.pushButton_plot, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Button_Grid.addItem(spacerItem, 0, 4, 1, 1)
        self.Button_Layout = QtGui.QHBoxLayout()
        self.Button_Layout.setObjectName(_fromUtf8("Button_Layout"))
        self.Button_Grid.addLayout(self.Button_Layout, 0, 3, 1, 1)
        self.gridLayout_6.addLayout(self.Button_Grid, 1, 0, 1, 1)
        self.Options_Grid = QtGui.QGridLayout()
        self.Options_Grid.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.Options_Grid.setObjectName(_fromUtf8("Options_Grid"))
        self.Grid_horizontal_Layout_1 = QtGui.QHBoxLayout()
        self.Grid_horizontal_Layout_1.setObjectName(_fromUtf8("Grid_horizontal_Layout_1"))
        self.Options_Grid.addLayout(self.Grid_horizontal_Layout_1, 1, 0, 1, 1)
        self.Grid_horizontal_Layout_2 = QtGui.QHBoxLayout()
        self.Grid_horizontal_Layout_2.setObjectName(_fromUtf8("Grid_horizontal_Layout_2"))
        self.Options_Grid.addLayout(self.Grid_horizontal_Layout_2, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.Options_Grid, 2, 0, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 512, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_About = QtGui.QMenu(self.menubar)
        self.menu_About.setObjectName(_fromUtf8("menu_About"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Save_Data = QtGui.QAction(MainWindow)
        self.action_Save_Data.setObjectName(_fromUtf8("action_Save_Data"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.menubar.addAction(self.menu_About.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_clear.setText(_translate("MainWindow", "Clear", None))
        self.pushButton_plot.setText(_translate("MainWindow", "Plot", None))
        self.menu_About.setTitle(_translate("MainWindow", "&About", None))
        self.action_Save_Data.setText(_translate("MainWindow", "&Save Data", None))
        self.action_Quit.setText(_translate("MainWindow", "&Quit", None))

from mplwidget import MplWidget
