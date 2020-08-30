# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/stefie10/dev/slu-with-hri-2010/pytools/direction_understanding3/src/du/gui/resultsBrowser/resultsBrowser.ui'
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
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.resultsTable = QtGui.QTableView(self.centralwidget)
        self.resultsTable.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.resultsTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.resultsTable.setSortingEnabled(True)
        self.resultsTable.setObjectName(_fromUtf8("resultsTable"))
        self.resultsTable.verticalHeader().setVisible(False)
        self.resultsTable.verticalHeader().setCascadingSectionResizes(False)
        self.gridLayout.addWidget(self.resultsTable, 0, 0, 1, 1)
        self.sentenceResultsTable = QtGui.QTableView(self.centralwidget)
        self.sentenceResultsTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.sentenceResultsTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.sentenceResultsTable.setObjectName(_fromUtf8("sentenceResultsTable"))
        self.gridLayout.addWidget(self.sentenceResultsTable, 0, 1, 1, 1)
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

