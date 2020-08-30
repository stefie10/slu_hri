# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/voom/gui/landmarkSelector.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.landmarkSelectorTable = QtGui.QTableView(self.centralwidget)
        self.landmarkSelectorTable.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.landmarkSelectorTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.landmarkSelectorTable.setSortingEnabled(True)
        self.landmarkSelectorTable.setObjectName(_fromUtf8("landmarkSelectorTable"))
        self.gridLayout.addWidget(self.landmarkSelectorTable, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.clearSelectionButton = QtGui.QPushButton(self.frame)
        self.clearSelectionButton.setObjectName(_fromUtf8("clearSelectionButton"))
        self.gridLayout_2.addWidget(self.clearSelectionButton, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.clearSelectionButton.setText(_translate("MainWindow", "Clear Selection", None))
        self.clearSelectionButton.setShortcut(_translate("MainWindow", "Ctrl+C", None))

