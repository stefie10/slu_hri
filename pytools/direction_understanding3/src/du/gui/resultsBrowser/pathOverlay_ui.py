# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/stefie10/dev/slu-with-hri-2010/pytools/direction_understanding3/src/du/gui/resultsBrowser/pathOverlay.ui'
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
        MainWindow.resize(1059, 1241)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.canvasFrame = QtGui.QFrame(self.centralwidget)
        self.canvasFrame.setMinimumSize(QtCore.QSize(0, 200))
        self.canvasFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.canvasFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.canvasFrame.setObjectName(_fromUtf8("canvasFrame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.canvasFrame)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout.addWidget(self.canvasFrame)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.renderButton = QtGui.QPushButton(self.frame)
        self.renderButton.setObjectName(_fromUtf8("renderButton"))
        self.gridLayout.addWidget(self.renderButton, 0, 2, 1, 1)
        self.radiusBox = QtGui.QSpinBox(self.frame)
        self.radiusBox.setProperty("value", 10)
        self.radiusBox.setObjectName(_fromUtf8("radiusBox"))
        self.gridLayout.addWidget(self.radiusBox, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.fractionWithinCircleLabel = QtGui.QLabel(self.frame)
        self.fractionWithinCircleLabel.setObjectName(_fromUtf8("fractionWithinCircleLabel"))
        self.gridLayout.addWidget(self.fractionWithinCircleLabel, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.selectedDirectionLabel = QtGui.QLabel(self.centralwidget)
        self.selectedDirectionLabel.setMinimumSize(QtCore.QSize(0, 200))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.selectedDirectionLabel.setFont(font)
        self.selectedDirectionLabel.setText(_fromUtf8(""))
        self.selectedDirectionLabel.setWordWrap(True)
        self.selectedDirectionLabel.setObjectName(_fromUtf8("selectedDirectionLabel"))
        self.verticalLayout.addWidget(self.selectedDirectionLabel)
        self.resultsTable = QtGui.QTableView(self.centralwidget)
        self.resultsTable.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.resultsTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.resultsTable.setObjectName(_fromUtf8("resultsTable"))
        self.verticalLayout.addWidget(self.resultsTable)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1059, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.renderButton.setText(QtGui.QApplication.translate("MainWindow", "Render", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Circle Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Fraction within circle:", None, QtGui.QApplication.UnicodeUTF8))
        self.fractionWithinCircleLabel.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

