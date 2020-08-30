# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/slimd/gui/srClassifierViewer.ui'
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
        MainWindow.resize(855, 761)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.canvasFrame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvasFrame.sizePolicy().hasHeightForWidth())
        self.canvasFrame.setSizePolicy(sizePolicy)
        self.canvasFrame.setMinimumSize(QtCore.QSize(640, 480))
        self.canvasFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.canvasFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.canvasFrame.setObjectName(_fromUtf8("canvasFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.canvasFrame)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.canvasFrame, 0, 1, 3, 1)
        self.geometryTable = QtGui.QTableView(self.centralwidget)
        self.geometryTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.geometryTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.geometryTable.setObjectName(_fromUtf8("geometryTable"))
        self.gridLayout.addWidget(self.geometryTable, 0, 0, 1, 1)
        self.featureTable = QtGui.QTableView(self.centralwidget)
        self.featureTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.featureTable.setObjectName(_fromUtf8("featureTable"))
        self.gridLayout.addWidget(self.featureTable, 1, 0, 1, 1)
        self.engineTable = QtGui.QTableView(self.centralwidget)
        self.engineTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.engineTable.setObjectName(_fromUtf8("engineTable"))
        self.gridLayout.addWidget(self.engineTable, 2, 0, 1, 1)
        self.classificationLabel = QtGui.QLabel(self.centralwidget)
        self.classificationLabel.setWordWrap(True)
        self.classificationLabel.setObjectName(_fromUtf8("classificationLabel"))
        self.gridLayout.addWidget(self.classificationLabel, 3, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuActions = QtGui.QMenu(self.menubar)
        self.menuActions.setObjectName(_fromUtf8("menuActions"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionClassify = QtGui.QAction(MainWindow)
        self.actionClassify.setObjectName(_fromUtf8("actionClassify"))
        self.menuActions.addAction(self.actionClassify)
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.classificationLabel.setText(_translate("MainWindow", "TextLabel", None))
        self.menuActions.setTitle(_translate("MainWindow", "Actions", None))
        self.actionClassify.setText(_translate("MainWindow", "Classify", None))
        self.actionClassify.setShortcut(_translate("MainWindow", "Ctrl+C", None))

