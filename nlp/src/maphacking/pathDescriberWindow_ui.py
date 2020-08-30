# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/maphacking/pathDescriberWindow.ui'
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
        MainWindow.resize(792, 566)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.mapFrame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapFrame.sizePolicy().hasHeightForWidth())
        self.mapFrame.setSizePolicy(sizePolicy)
        self.mapFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mapFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mapFrame.setObjectName(_fromUtf8("mapFrame"))
        self.hboxlayout = QtGui.QHBoxLayout(self.mapFrame)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.vboxlayout.addWidget(self.mapFrame)
        self.descriptionTable = QtGui.QTableView(self.centralwidget)
        self.descriptionTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.descriptionTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.descriptionTable.setObjectName(_fromUtf8("descriptionTable"))
        self.vboxlayout.addWidget(self.descriptionTable)
        self.frame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.frame)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.descriptionLabel = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.descriptionLabel.setFont(font)
        self.descriptionLabel.setText(_fromUtf8(""))
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.vboxlayout1.addWidget(self.descriptionLabel)
        self.coordinateLabel = QtGui.QLabel(self.frame)
        self.coordinateLabel.setObjectName(_fromUtf8("coordinateLabel"))
        self.vboxlayout1.addWidget(self.coordinateLabel)
        self.vboxlayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 792, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.coordinateLabel.setText(_translate("MainWindow", "coordinates", None))

