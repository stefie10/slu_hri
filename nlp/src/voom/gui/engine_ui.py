# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/voom/gui/engine.ui'
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
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.classLabel = QtGui.QLabel(self.centralwidget)
        self.classLabel.setObjectName(_fromUtf8("classLabel"))
        self.gridLayout.addWidget(self.classLabel, 1, 1, 1, 1)
        self.featureTable = QtGui.QTableView(self.centralwidget)
        self.featureTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.featureTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.featureTable.setObjectName(_fromUtf8("featureTable"))
        self.gridLayout.addWidget(self.featureTable, 0, 5, 1, 1)
        self.engineTable = QtGui.QTableView(self.centralwidget)
        self.engineTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.engineTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.engineTable.setObjectName(_fromUtf8("engineTable"))
        self.gridLayout.addWidget(self.engineTable, 0, 0, 1, 5)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.pTrueLabel = QtGui.QLabel(self.centralwidget)
        self.pTrueLabel.setObjectName(_fromUtf8("pTrueLabel"))
        self.gridLayout.addWidget(self.pTrueLabel, 1, 3, 1, 1)
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
        self.label.setText(_translate("MainWindow", "Class:", None))
        self.classLabel.setText(_translate("MainWindow", "TextLabel", None))
        self.label_2.setText(_translate("MainWindow", "p_true:", None))
        self.pTrueLabel.setText(_translate("MainWindow", "TextLabel", None))

