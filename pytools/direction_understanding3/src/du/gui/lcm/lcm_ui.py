# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/stefie10/dev/slu-with-hri-2010/pytools/direction_understanding3/src/du/gui/lcm/lcm.ui'
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
        MainWindow.resize(699, 420)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.commandText = QtGui.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.commandText.setFont(font)
        self.commandText.setObjectName(_fromUtf8("commandText"))
        self.gridLayout.addWidget(self.commandText, 0, 0, 7, 1)
        self.sendPathButton = QtGui.QPushButton(self.centralwidget)
        self.sendPathButton.setObjectName(_fromUtf8("sendPathButton"))
        self.gridLayout.addWidget(self.sendPathButton, 0, 1, 1, 1)
        self.confirmPathButton = QtGui.QPushButton(self.centralwidget)
        self.confirmPathButton.setObjectName(_fromUtf8("confirmPathButton"))
        self.gridLayout.addWidget(self.confirmPathButton, 1, 1, 1, 1)
        self.useRobotYawBox = QtGui.QCheckBox(self.centralwidget)
        self.useRobotYawBox.setChecked(True)
        self.useRobotYawBox.setObjectName(_fromUtf8("useRobotYawBox"))
        self.gridLayout.addWidget(self.useRobotYawBox, 5, 1, 1, 1)
        self.clearPathButton = QtGui.QPushButton(self.centralwidget)
        self.clearPathButton.setObjectName(_fromUtf8("clearPathButton"))
        self.gridLayout.addWidget(self.clearPathButton, 3, 1, 1, 1)
        self.sendAndExecutePathButton = QtGui.QPushButton(self.centralwidget)
        self.sendAndExecutePathButton.setObjectName(_fromUtf8("sendAndExecutePathButton"))
        self.gridLayout.addWidget(self.sendAndExecutePathButton, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 699, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Command Window", None, QtGui.QApplication.UnicodeUTF8))
        self.commandText.setPlainText(QtGui.QApplication.translate("MainWindow", "Face the windows.", None, QtGui.QApplication.UnicodeUTF8))
        self.sendPathButton.setText(QtGui.QApplication.translate("MainWindow", "Send Path", None, QtGui.QApplication.UnicodeUTF8))
        self.sendPathButton.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.confirmPathButton.setText(QtGui.QApplication.translate("MainWindow", "Execute Path", None, QtGui.QApplication.UnicodeUTF8))
        self.confirmPathButton.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.useRobotYawBox.setText(QtGui.QApplication.translate("MainWindow", "Use Robot Yaw", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPathButton.setText(QtGui.QApplication.translate("MainWindow", "Kill Path", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPathButton.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+K", None, QtGui.QApplication.UnicodeUTF8))
        self.sendAndExecutePathButton.setText(QtGui.QApplication.translate("MainWindow", "Send and Execute", None, QtGui.QApplication.UnicodeUTF8))

