from PyQt4.QtCore import *
from PyQt4.QtGui import *
import landmarkSelector_ui
import landmarkSelectorTableModel 

class MainWindow(QMainWindow, landmarkSelector_ui.Ui_MainWindow):
    def __init__(self, m4du):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.landmarkModel = landmarkSelectorTableModel.Model(self.landmarkSelectorTable,
                                                              m4du)

        self.setWindowTitle("Select Landmarks.")
        self.connect(self.clearSelectionButton,
                     SIGNAL("clicked()"),
                     self.clearSelection)
    def clearSelection(self):
        self.landmarkSelectorTable.clearSelection()

    def selectIndexes(self, indexes):
        self.landmarkModel
