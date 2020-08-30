# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/stefie10/dev/slu-with-hri-2010/pytools/direction_understanding3/src/du/tagFileGui/annotator.ui'
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
        self.tagTable = QtGui.QTableView(self.centralwidget)
        self.tagTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tagTable.setSortingEnabled(True)
        self.tagTable.setObjectName(_fromUtf8("tagTable"))
        self.gridLayout.addWidget(self.tagTable, 1, 1, 2, 1)
        self.capturerList = QtGui.QListWidget(self.centralwidget)
        self.capturerList.setMaximumSize(QtCore.QSize(200, 16777215))
        self.capturerList.setObjectName(_fromUtf8("capturerList"))
        item = QtGui.QListWidgetItem()
        self.capturerList.addItem(item)
        item = QtGui.QListWidgetItem()
        self.capturerList.addItem(item)
        self.gridLayout.addWidget(self.capturerList, 1, 0, 1, 1)
        self.canvasFrame = QtGui.QFrame(self.centralwidget)
        self.canvasFrame.setMinimumSize(QtCore.QSize(0, 400))
        self.canvasFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.canvasFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.canvasFrame.setObjectName(_fromUtf8("canvasFrame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.canvasFrame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout.addWidget(self.canvasFrame, 0, 0, 1, 2)
        self.resetButton = QtGui.QPushButton(self.centralwidget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.gridLayout.addWidget(self.resetButton, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuActions = QtGui.QMenu(self.menubar)
        self.menuActions.setObjectName(_fromUtf8("menuActions"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionDeleteTags = QtGui.QAction(MainWindow)
        self.actionDeleteTags.setObjectName(_fromUtf8("actionDeleteTags"))
        self.menuFile.addAction(self.actionSave)
        self.menuActions.addAction(self.actionDeleteTags)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.capturerList.isSortingEnabled()
        self.capturerList.setSortingEnabled(False)
        item = self.capturerList.item(0)
        item.setText(QtGui.QApplication.translate("MainWindow", "Point", None, QtGui.QApplication.UnicodeUTF8))
        item = self.capturerList.item(1)
        item.setText(QtGui.QApplication.translate("MainWindow", "Polygon", None, QtGui.QApplication.UnicodeUTF8))
        self.capturerList.setSortingEnabled(__sortingEnabled)
        self.resetButton.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuActions.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteTags.setText(QtGui.QApplication.translate("MainWindow", "Delete Tags", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteTags.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))

