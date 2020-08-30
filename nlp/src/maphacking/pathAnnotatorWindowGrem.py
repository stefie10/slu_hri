from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pathAnnotatorWindow
import login_ui
import basewindow
from makeAssignment import makeAssignment
import os
import spatialRelationClassifier

class AssignmentTableModel(QAbstractTableModel):
    def __init__(self, view, directories):
        QAbstractTableModel.__init__(self)
        self._data = directories
        self.view = view
        view.setModel(self)
    def columnCount(self, parent):
        return 1
    def rowCount(self, parent):
        return len(self._data)
    def get(self, idx):
        return self._data[idx.row()]
    def selectedData(self):
        return self.get(self.view.currentIndex())
    def data(self, idx, role=Qt.DisplayRole):
        dc = self.get(idx)
        
        col = idx.column()
        if role != Qt.DisplayRole:
            return QVariant()            
        
        if col == 0:
            return QVariant(dc)
        else:
            raise ValueError("Unexpected idx: " + `idx`)
        

class Dialog(QDialog, login_ui.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.model = AssignmentTableModel(self.assignmentTable, 
                                          ["part1", "part2", "part3"])
        self.assignmentTable.selectRow(0)

    @property
    def username(self):
        return str(self.userNameEdit.text())

    @property
    def assignmentDirectory(self):
        return self.model.selectedData()


def main():
    app = basewindow.makeApp()
    dialog = Dialog()
    username = ""
    while username == "":
        if dialog.exec_() == QDialog.Accepted:
            username = dialog.username

    
    assignment = dialog.assignmentDirectory

    
    fullDirectory = "gremclass/%s" % (username)
    assignmentDirectory = "%s/%s" % (fullDirectory, assignment)
    if not os.path.exists(assignmentDirectory):
        if not os.path.exists(fullDirectory):
            os.makedirs(fullDirectory)
        makeAssignment(assignmentDirectory,
                       "../data/directions/direction_floor_3/log4_s3.tag", 
                       "../data/directions/direction_floor_3/log4_s3.cmf",
                       spatialRelationClassifier.engineMap)
    
    wnd = pathAnnotatorWindow.MainWindow(assignmentDirectory)

                   
    wnd.show()
    retval = app.exec_()

if __name__=="__main__":
    main()
