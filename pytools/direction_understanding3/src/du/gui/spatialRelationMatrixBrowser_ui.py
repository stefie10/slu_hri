# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/stefie10/dev/slu-with-hri-2010/pytools/direction_understanding3/src/du/gui/spatialRelationMatrixBrowser.ui'
#
# Created: Tue May 28 10:24:36 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.matplotlibFrame = QtGui.QFrame(self.centralwidget)
        self.matplotlibFrame.setMinimumSize(QtCore.QSize(0, 200))
        self.matplotlibFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.matplotlibFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.matplotlibFrame.setObjectName(_fromUtf8("matplotlibFrame"))
        self.gridLayout = QtGui.QGridLayout(self.matplotlibFrame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout.addWidget(self.matplotlibFrame)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.engineMapListView = QtGui.QListView(self.frame)
        self.engineMapListView.setObjectName(_fromUtf8("engineMapListView"))
        self.horizontalLayout.addWidget(self.engineMapListView)
        self.verticalLayout.addWidget(self.frame)
        self.matrixBrowserTable = QtGui.QTableView(self.centralwidget)
        self.matrixBrowserTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.matrixBrowserTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.matrixBrowserTable.setSortingEnabled(True)
        self.matrixBrowserTable.setObjectName(_fromUtf8("matrixBrowserTable"))
        self.verticalLayout.addWidget(self.matrixBrowserTable)
        self.nwayVsBinaryTable = QtGui.QTableView(self.centralwidget)
        self.nwayVsBinaryTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.nwayVsBinaryTable.setSortingEnabled(True)
        self.nwayVsBinaryTable.setObjectName(_fromUtf8("nwayVsBinaryTable"))
        self.verticalLayout.addWidget(self.nwayVsBinaryTable)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Spatial Relation", None, QtGui.QApplication.UnicodeUTF8))

