# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/stefie10/dev/slu-with-hri-2010/pytools/direction_understanding3/src/du/gui/modelBrowser.ui'
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
        MainWindow.resize(1335, 1309)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.matplotlibFrame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matplotlibFrame.sizePolicy().hasHeightForWidth())
        self.matplotlibFrame.setSizePolicy(sizePolicy)
        self.matplotlibFrame.setMinimumSize(QtCore.QSize(700, 500))
        self.matplotlibFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.matplotlibFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.matplotlibFrame.setObjectName(_fromUtf8("matplotlibFrame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.matplotlibFrame)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2.addWidget(self.matplotlibFrame, 1, 2, 1, 1)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame_3 = QtGui.QFrame(self.frame_2)
        self.frame_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout.addWidget(self.frame_3, 4, 0, 1, 1)
        self.slocTable = QtGui.QTableView(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slocTable.sizePolicy().hasHeightForWidth())
        self.slocTable.setSizePolicy(sizePolicy)
        self.slocTable.setMaximumSize(QtCore.QSize(150, 16777215))
        self.slocTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.slocTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.slocTable.setSortingEnabled(True)
        self.slocTable.setObjectName(_fromUtf8("slocTable"))
        self.gridLayout.addWidget(self.slocTable, 4, 3, 1, 1)
        self.elocTable = QtGui.QTableView(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elocTable.sizePolicy().hasHeightForWidth())
        self.elocTable.setSizePolicy(sizePolicy)
        self.elocTable.setMaximumSize(QtCore.QSize(150, 16777215))
        self.elocTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.elocTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.elocTable.setSortingEnabled(True)
        self.elocTable.setObjectName(_fromUtf8("elocTable"))
        self.gridLayout.addWidget(self.elocTable, 4, 4, 1, 1)
        self.landmarkTable = QtGui.QTableView(self.frame_2)
        self.landmarkTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.landmarkTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.landmarkTable.setSortingEnabled(True)
        self.landmarkTable.setObjectName(_fromUtf8("landmarkTable"))
        self.gridLayout.addWidget(self.landmarkTable, 4, 6, 1, 1)
        self.slocTransitionsBox = QtGui.QCheckBox(self.frame_2)
        self.slocTransitionsBox.setObjectName(_fromUtf8("slocTransitionsBox"))
        self.gridLayout.addWidget(self.slocTransitionsBox, 0, 3, 1, 1)
        self.jointViewpointTable = QtGui.QTableView(self.frame_2)
        self.jointViewpointTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.jointViewpointTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.jointViewpointTable.setSortingEnabled(True)
        self.jointViewpointTable.setObjectName(_fromUtf8("jointViewpointTable"))
        self.gridLayout.addWidget(self.jointViewpointTable, 4, 5, 1, 1)
        self.filterBySlocBox = QtGui.QCheckBox(self.frame_2)
        self.filterBySlocBox.setObjectName(_fromUtf8("filterBySlocBox"))
        self.gridLayout.addWidget(self.filterBySlocBox, 0, 5, 1, 1)
        self.filterByElocBox = QtGui.QCheckBox(self.frame_2)
        self.filterByElocBox.setObjectName(_fromUtf8("filterByElocBox"))
        self.gridLayout.addWidget(self.filterByElocBox, 1, 5, 1, 1)
        self.startingSlocTable = QtGui.QTableView(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startingSlocTable.sizePolicy().hasHeightForWidth())
        self.startingSlocTable.setSizePolicy(sizePolicy)
        self.startingSlocTable.setMaximumSize(QtCore.QSize(150, 16777215))
        self.startingSlocTable.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.startingSlocTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.startingSlocTable.setSortingEnabled(True)
        self.startingSlocTable.setObjectName(_fromUtf8("startingSlocTable"))
        self.gridLayout.addWidget(self.startingSlocTable, 4, 1, 1, 1)
        self.slocObservationProbabilityCheckBox = QtGui.QCheckBox(self.frame_2)
        self.slocObservationProbabilityCheckBox.setObjectName(_fromUtf8("slocObservationProbabilityCheckBox"))
        self.gridLayout.addWidget(self.slocObservationProbabilityCheckBox, 1, 3, 1, 1)
        self.slocVerbProbabilityCheckBox = QtGui.QCheckBox(self.frame_2)
        self.slocVerbProbabilityCheckBox.setObjectName(_fromUtf8("slocVerbProbabilityCheckBox"))
        self.gridLayout.addWidget(self.slocVerbProbabilityCheckBox, 2, 3, 1, 1)
        self.sdcTable = QtGui.QTableView(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sdcTable.sizePolicy().hasHeightForWidth())
        self.sdcTable.setSizePolicy(sizePolicy)
        self.sdcTable.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.sdcTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.sdcTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.sdcTable.setObjectName(_fromUtf8("sdcTable"))
        self.gridLayout.addWidget(self.sdcTable, 4, 2, 1, 1)
        self.landmarkProbsCheckBox = QtGui.QCheckBox(self.frame_2)
        self.landmarkProbsCheckBox.setObjectName(_fromUtf8("landmarkProbsCheckBox"))
        self.gridLayout.addWidget(self.landmarkProbsCheckBox, 3, 3, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 2, 0, 1, 3)
        self.frame_4 = QtGui.QFrame(self.centralwidget)
        self.frame_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_4)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.directionsTextEdit = QtGui.QPlainTextEdit(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directionsTextEdit.sizePolicy().hasHeightForWidth())
        self.directionsTextEdit.setSizePolicy(sizePolicy)
        self.directionsTextEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.directionsTextEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.directionsTextEdit.setFont(font)
        self.directionsTextEdit.setObjectName(_fromUtf8("directionsTextEdit"))
        self.verticalLayout.addWidget(self.directionsTextEdit)
        self.submitButton = QtGui.QPushButton(self.frame_4)
        self.submitButton.setObjectName(_fromUtf8("submitButton"))
        self.verticalLayout.addWidget(self.submitButton)
        self.viewSrClassifierButton = QtGui.QPushButton(self.frame_4)
        self.viewSrClassifierButton.setObjectName(_fromUtf8("viewSrClassifierButton"))
        self.verticalLayout.addWidget(self.viewSrClassifierButton)
        self.jointVpToSlocElocButton = QtGui.QPushButton(self.frame_4)
        self.jointVpToSlocElocButton.setObjectName(_fromUtf8("jointVpToSlocElocButton"))
        self.verticalLayout.addWidget(self.jointVpToSlocElocButton)
        self.zoomToMagicSpotButton = QtGui.QPushButton(self.frame_4)
        self.zoomToMagicSpotButton.setObjectName(_fromUtf8("zoomToMagicSpotButton"))
        self.verticalLayout.addWidget(self.zoomToMagicSpotButton)
        self.picturesForViewpointButton = QtGui.QPushButton(self.frame_4)
        self.picturesForViewpointButton.setObjectName(_fromUtf8("picturesForViewpointButton"))
        self.verticalLayout.addWidget(self.picturesForViewpointButton)
        self.useSpatialRelationsBox = QtGui.QCheckBox(self.frame_4)
        self.useSpatialRelationsBox.setChecked(True)
        self.useSpatialRelationsBox.setObjectName(_fromUtf8("useSpatialRelationsBox"))
        self.verticalLayout.addWidget(self.useSpatialRelationsBox)
        self.useWizardOfOzSdcsCheckBox = QtGui.QCheckBox(self.frame_4)
        self.useWizardOfOzSdcsCheckBox.setObjectName(_fromUtf8("useWizardOfOzSdcsCheckBox"))
        self.verticalLayout.addWidget(self.useWizardOfOzSdcsCheckBox)
        self.showLandmarksCheckBox = QtGui.QCheckBox(self.frame_4)
        self.showLandmarksCheckBox.setChecked(True)
        self.showLandmarksCheckBox.setObjectName(_fromUtf8("showLandmarksCheckBox"))
        self.verticalLayout.addWidget(self.showLandmarksCheckBox)
        self.showTopologyBox = QtGui.QCheckBox(self.frame_4)
        self.showTopologyBox.setObjectName(_fromUtf8("showTopologyBox"))
        self.verticalLayout.addWidget(self.showTopologyBox)
        self.gridLayout_2.addWidget(self.frame_4, 1, 0, 1, 1)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2.addWidget(self.frame, 4, 0, 1, 1)
        self.frame_5 = QtGui.QFrame(self.centralwidget)
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_5)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.observationProbabilityLabel = QtGui.QLabel(self.frame_5)
        self.observationProbabilityLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.observationProbabilityLabel.setObjectName(_fromUtf8("observationProbabilityLabel"))
        self.gridLayout_4.addWidget(self.observationProbabilityLabel, 0, 0, 1, 1)
        self.srProbabilityLabel = QtGui.QLabel(self.frame_5)
        self.srProbabilityLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.srProbabilityLabel.setObjectName(_fromUtf8("srProbabilityLabel"))
        self.gridLayout_4.addWidget(self.srProbabilityLabel, 1, 0, 1, 1)
        self.tMatLabel = QtGui.QLabel(self.frame_5)
        self.tMatLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.tMatLabel.setObjectName(_fromUtf8("tMatLabel"))
        self.gridLayout_4.addWidget(self.tMatLabel, 2, 0, 1, 1)
        self.p_prev_label = QtGui.QLabel(self.frame_5)
        self.p_prev_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.p_prev_label.setObjectName(_fromUtf8("p_prev_label"))
        self.gridLayout_4.addWidget(self.p_prev_label, 3, 0, 1, 1)
        self.overallscore_label = QtGui.QLabel(self.frame_5)
        self.overallscore_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.overallscore_label.setObjectName(_fromUtf8("overallscore_label"))
        self.gridLayout_4.addWidget(self.overallscore_label, 4, 0, 1, 1)
        self.pathLabel = QtGui.QLabel(self.frame_5)
        self.pathLabel.setWordWrap(True)
        self.pathLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.pathLabel.setObjectName(_fromUtf8("pathLabel"))
        self.gridLayout_4.addWidget(self.pathLabel, 0, 1, 1, 1)
        self.visibleObjectFromLandmarkLabel = QtGui.QLabel(self.frame_5)
        self.visibleObjectFromLandmarkLabel.setObjectName(_fromUtf8("visibleObjectFromLandmarkLabel"))
        self.gridLayout_4.addWidget(self.visibleObjectFromLandmarkLabel, 1, 1, 1, 1)
        self.visibleObjectsFromSlocLabel = QtGui.QLabel(self.frame_5)
        self.visibleObjectsFromSlocLabel.setObjectName(_fromUtf8("visibleObjectsFromSlocLabel"))
        self.gridLayout_4.addWidget(self.visibleObjectsFromSlocLabel, 2, 1, 1, 1)
        self.visibleObjectsFromOrientedSlocLabel = QtGui.QLabel(self.frame_5)
        self.visibleObjectsFromOrientedSlocLabel.setObjectName(_fromUtf8("visibleObjectsFromOrientedSlocLabel"))
        self.gridLayout_4.addWidget(self.visibleObjectsFromOrientedSlocLabel, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_5, 4, 1, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1335, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionSaveLimits = QtGui.QAction(MainWindow)
        self.actionSaveLimits.setObjectName(_fromUtf8("actionSaveLimits"))
        self.actionRestoreLimits = QtGui.QAction(MainWindow)
        self.actionRestoreLimits.setObjectName(_fromUtf8("actionRestoreLimits"))
        self.actionSelectSpatialRelations = QtGui.QAction(MainWindow)
        self.actionSelectSpatialRelations.setObjectName(_fromUtf8("actionSelectSpatialRelations"))
        self.actionClear = QtGui.QAction(MainWindow)
        self.actionClear.setObjectName(_fromUtf8("actionClear"))
        self.menuEdit.addAction(self.actionPreferences)
        self.menuEdit.addAction(self.actionSelectSpatialRelations)
        self.menuEdit.addAction(self.actionSaveLimits)
        self.menuEdit.addAction(self.actionRestoreLimits)
        self.menuEdit.addAction(self.actionClear)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Model Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.slocTransitionsBox.setText(QtGui.QApplication.translate("MainWindow", "Show Transitions", None, QtGui.QApplication.UnicodeUTF8))
        self.filterBySlocBox.setText(QtGui.QApplication.translate("MainWindow", "Filter by sloc", None, QtGui.QApplication.UnicodeUTF8))
        self.filterByElocBox.setText(QtGui.QApplication.translate("MainWindow", "Filter by eloc", None, QtGui.QApplication.UnicodeUTF8))
        self.slocObservationProbabilityCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Show p_obs", None, QtGui.QApplication.UnicodeUTF8))
        self.slocVerbProbabilityCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Show p_verb", None, QtGui.QApplication.UnicodeUTF8))
        self.landmarkProbsCheckBox.setText(QtGui.QApplication.translate("MainWindow", "display ldmk probs", None, QtGui.QApplication.UnicodeUTF8))
        self.directionsTextEdit.setPlainText(QtGui.QApplication.translate("MainWindow", "Go to the elevators.", None, QtGui.QApplication.UnicodeUTF8))
        self.submitButton.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.viewSrClassifierButton.setText(QtGui.QApplication.translate("MainWindow", "View SR Classifier", None, QtGui.QApplication.UnicodeUTF8))
        self.jointVpToSlocElocButton.setText(QtGui.QApplication.translate("MainWindow", "Joint VP to sloc,eloc", None, QtGui.QApplication.UnicodeUTF8))
        self.jointVpToSlocElocButton.setShortcut(QtGui.QApplication.translate("MainWindow", "J", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomToMagicSpotButton.setText(QtGui.QApplication.translate("MainWindow", "Zoom to Magic Spot", None, QtGui.QApplication.UnicodeUTF8))
        self.zoomToMagicSpotButton.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.picturesForViewpointButton.setText(QtGui.QApplication.translate("MainWindow", "Pictures for VP", None, QtGui.QApplication.UnicodeUTF8))
        self.useSpatialRelationsBox.setText(QtGui.QApplication.translate("MainWindow", "use spatial relations", None, QtGui.QApplication.UnicodeUTF8))
        self.useWizardOfOzSdcsCheckBox.setText(QtGui.QApplication.translate("MainWindow", "use wizard of oz sdcs", None, QtGui.QApplication.UnicodeUTF8))
        self.showLandmarksCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Show Landmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.showTopologyBox.setText(QtGui.QApplication.translate("MainWindow", "Show topology", None, QtGui.QApplication.UnicodeUTF8))
        self.observationProbabilityLabel.setText(QtGui.QApplication.translate("MainWindow", "Observation:", None, QtGui.QApplication.UnicodeUTF8))
        self.srProbabilityLabel.setText(QtGui.QApplication.translate("MainWindow", "SR:", None, QtGui.QApplication.UnicodeUTF8))
        self.tMatLabel.setText(QtGui.QApplication.translate("MainWindow", "Transistion:", None, QtGui.QApplication.UnicodeUTF8))
        self.p_prev_label.setText(QtGui.QApplication.translate("MainWindow", "P_prev", None, QtGui.QApplication.UnicodeUTF8))
        self.overallscore_label.setText(QtGui.QApplication.translate("MainWindow", "Overall Score", None, QtGui.QApplication.UnicodeUTF8))
        self.pathLabel.setText(QtGui.QApplication.translate("MainWindow", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.visibleObjectFromLandmarkLabel.setText(QtGui.QApplication.translate("MainWindow", "Visible objects:", None, QtGui.QApplication.UnicodeUTF8))
        self.visibleObjectsFromSlocLabel.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.visibleObjectsFromOrientedSlocLabel.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Select Landmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveLimits.setText(QtGui.QApplication.translate("MainWindow", "Save Limits", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveLimits.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRestoreLimits.setText(QtGui.QApplication.translate("MainWindow", "Restore Limits", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRestoreLimits.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectSpatialRelations.setText(QtGui.QApplication.translate("MainWindow", "Select Spatial Relations", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
