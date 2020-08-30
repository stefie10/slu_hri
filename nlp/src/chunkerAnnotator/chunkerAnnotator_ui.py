# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/chunkerAnnotator/chunkerAnnotator.ui'
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
        MainWindow.resize(497, 677)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout.addWidget(self.frame)
        self.instructionTable = QtGui.QTableView(self.centralwidget)
        self.instructionTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.instructionTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.instructionTable.setObjectName(_fromUtf8("instructionTable"))
        self.instructionTable.horizontalHeader().setVisible(False)
        self.instructionTable.horizontalHeader().setStretchLastSection(True)
        self.instructionTable.verticalHeader().setVisible(False)
        self.instructionTable.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.instructionTable)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 497, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionExportAsDotty = QtGui.QAction(MainWindow)
        self.actionExportAsDotty.setObjectName(_fromUtf8("actionExportAsDotty"))
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+X, Ctrl+S", None))
        self.actionExportAsDotty.setText(_translate("MainWindow", "Export as dotty", None))

