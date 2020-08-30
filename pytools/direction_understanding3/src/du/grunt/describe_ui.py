# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/stefie10/dev/slu-with-hri-2010/pytools/direction_understanding3/src/du/grunt/describe.ui'
#
# Created: Tue May 28 10:24:35 2013
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
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mapFrame = QtGui.QFrame(self.centralwidget)
        self.mapFrame.setMinimumSize(QtCore.QSize(0, 200))
        self.mapFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mapFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mapFrame.setObjectName(_fromUtf8("mapFrame"))
        self.gridLayout.addWidget(self.mapFrame, 0, 0, 1, 2)
        self.srResultTable = QtGui.QTableView(self.centralwidget)
        self.srResultTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.srResultTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.srResultTable.setSortingEnabled(True)
        self.srResultTable.setObjectName(_fromUtf8("srResultTable"))
        self.gridLayout.addWidget(self.srResultTable, 1, 1, 1, 1)
        self.verbResultTable = QtGui.QTableView(self.centralwidget)
        self.verbResultTable.setObjectName(_fromUtf8("verbResultTable"))
        self.gridLayout.addWidget(self.verbResultTable, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuActions = QtGui.QMenu(self.menubar)
        self.menuActions.setObjectName(_fromUtf8("menuActions"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionGenerate = QtGui.QAction(MainWindow)
        self.actionGenerate.setObjectName(_fromUtf8("actionGenerate"))
        self.actionNew_Situation = QtGui.QAction(MainWindow)
        self.actionNew_Situation.setObjectName(_fromUtf8("actionNew_Situation"))
        self.menuActions.addAction(self.actionGenerate)
        self.menuActions.addAction(self.actionNew_Situation)
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuActions.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate.setText(QtGui.QApplication.translate("MainWindow", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate.setShortcut(QtGui.QApplication.translate("MainWindow", "G", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Situation.setText(QtGui.QApplication.translate("MainWindow", "New Situation", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Situation.setShortcut(QtGui.QApplication.translate("MainWindow", "N", None, QtGui.QApplication.UnicodeUTF8))

