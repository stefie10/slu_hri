# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/maphacking/pathAnnotatorWindow.ui'
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
        MainWindow.resize(800, 680)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mapFrame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapFrame.sizePolicy().hasHeightForWidth())
        self.mapFrame.setSizePolicy(sizePolicy)
        self.mapFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mapFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mapFrame.setObjectName(_fromUtf8("mapFrame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.mapFrame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout.addWidget(self.mapFrame)
        self.annotationTable = QtGui.QTableView(self.centralwidget)
        self.annotationTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.annotationTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.annotationTable.setObjectName(_fromUtf8("annotationTable"))
        self.verticalLayout.addWidget(self.annotationTable)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pathDescriptionLabel = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pathDescriptionLabel.setFont(font)
        self.pathDescriptionLabel.setObjectName(_fromUtf8("pathDescriptionLabel"))
        self.horizontalLayout.addWidget(self.pathDescriptionLabel)
        self.verticalLayout.addWidget(self.frame)
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
        self.actionNext = QtGui.QAction(MainWindow)
        self.actionNext.setObjectName(_fromUtf8("actionNext"))
        self.menuActions.addAction(self.actionNext)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pathDescriptionLabel.setText(_translate("MainWindow", "sentence", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuActions.setTitle(_translate("MainWindow", "Actions", None))
        self.actionNext.setText(_translate("MainWindow", "Next", None))
        self.actionNext.setShortcut(_translate("MainWindow", "N", None))

