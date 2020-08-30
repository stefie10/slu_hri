from PyQt4.QtCore import *
from PyQt4.QtGui import *
import landmarkSelectorTableModel
import landmarkSelector_ui

class MainWindow(QMainWindow, landmarkSelector_ui.Ui_MainWindow):
    def __init__(self, tag_file):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.landmarkModel = landmarkSelectorTableModel.Model(self.landmarkSelectorTable, tag_file)

        self.setWindowTitle("Select Landmarks.")
        self.connect(self.clearSelectionButton,
                     SIGNAL("clicked()"),
                     self.clearSelection)
    def clearSelection(self):
        self.landmarkSelectorTable.clearSelection()

    def selectIndexes(self, indexes):
        self.landmarkModel
