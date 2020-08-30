# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/chunkerAnnotator/sdcAnnotator.ui'
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
        MainWindow.resize(1028, 700)
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
        self.instructionEdit = QtGui.QTextEdit(self.frame)
        self.instructionEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.instructionEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.instructionEdit.setObjectName(_fromUtf8("instructionEdit"))
        self.verticalLayout.addWidget(self.instructionEdit)
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.figureButton = QtGui.QPushButton(self.frame_2)
        self.figureButton.setObjectName(_fromUtf8("figureButton"))
        self.horizontalLayout_2.addWidget(self.figureButton)
        self.figureLabel = QtGui.QLabel(self.frame_2)
        self.figureLabel.setText(_fromUtf8(""))
        self.figureLabel.setObjectName(_fromUtf8("figureLabel"))
        self.horizontalLayout_2.addWidget(self.figureLabel)
        self.verbButton = QtGui.QPushButton(self.frame_2)
        self.verbButton.setObjectName(_fromUtf8("verbButton"))
        self.horizontalLayout_2.addWidget(self.verbButton)
        self.verbLabel = QtGui.QLabel(self.frame_2)
        self.verbLabel.setText(_fromUtf8(""))
        self.verbLabel.setObjectName(_fromUtf8("verbLabel"))
        self.horizontalLayout_2.addWidget(self.verbLabel)
        self.spatialRelationButton = QtGui.QPushButton(self.frame_2)
        self.spatialRelationButton.setObjectName(_fromUtf8("spatialRelationButton"))
        self.horizontalLayout_2.addWidget(self.spatialRelationButton)
        self.spatialRelationLabel = QtGui.QLabel(self.frame_2)
        self.spatialRelationLabel.setText(_fromUtf8(""))
        self.spatialRelationLabel.setObjectName(_fromUtf8("spatialRelationLabel"))
        self.horizontalLayout_2.addWidget(self.spatialRelationLabel)
        self.landmarkButton = QtGui.QPushButton(self.frame_2)
        self.landmarkButton.setObjectName(_fromUtf8("landmarkButton"))
        self.horizontalLayout_2.addWidget(self.landmarkButton)
        self.landmarkLabel = QtGui.QLabel(self.frame_2)
        self.landmarkLabel.setText(_fromUtf8(""))
        self.landmarkLabel.setObjectName(_fromUtf8("landmarkLabel"))
        self.horizontalLayout_2.addWidget(self.landmarkLabel)
        self.landmark2Button = QtGui.QPushButton(self.frame_2)
        self.landmark2Button.setObjectName(_fromUtf8("landmark2Button"))
        self.horizontalLayout_2.addWidget(self.landmark2Button)
        self.landmark2Label = QtGui.QLabel(self.frame_2)
        self.landmark2Label.setText(_fromUtf8(""))
        self.landmark2Label.setObjectName(_fromUtf8("landmark2Label"))
        self.horizontalLayout_2.addWidget(self.landmark2Label)
        self.verticalLayout.addWidget(self.frame_2)
        self.annotationTable = QtGui.QTableView(self.frame)
        self.annotationTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.annotationTable.setObjectName(_fromUtf8("annotationTable"))
        self.verticalLayout.addWidget(self.annotationTable)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1028, 25))
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
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.figureButton.setText(_translate("MainWindow", "Figure:", None))
        self.figureButton.setShortcut(_translate("MainWindow", "F", None))
        self.verbButton.setText(_translate("MainWindow", "Verb:", None))
        self.verbButton.setShortcut(_translate("MainWindow", "V", None))
        self.spatialRelationButton.setText(_translate("MainWindow", "Spatial Relation:", None))
        self.spatialRelationButton.setShortcut(_translate("MainWindow", "S", None))
        self.landmarkButton.setText(_translate("MainWindow", "Landmark:", None))
        self.landmarkButton.setShortcut(_translate("MainWindow", "L", None))
        self.landmark2Button.setText(_translate("MainWindow", "Landmark2:", None))
        self.landmark2Button.setShortcut(_translate("MainWindow", "2", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+X, Ctrl+S", None))
        self.actionExportAsDotty.setText(_translate("MainWindow", "Export as dotty", None))

