import matplotlib
matplotlib.use("Qt4Agg")

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from slimd.gui import sr_session_model, srSessionViewer_ui, srClassifierViewer
import basewindow
import cPickle
    

    

class MainWindow(QMainWindow, srSessionViewer_ui.Ui_MainWindow):
    def __init__(self, data):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.sessionModel = sr_session_model.Model(self.sessionTable)
        self.sessionModel.loadData(data)
        
        self.connect(self.sessionTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectExample)

        
        self.classifierViewer = srClassifierViewer.MainWindow()
        self.classifierViewer.show()
        
        self.sessionTable.selectRow(0)
    def selectExample(self):
        sr, landmark, geometry = self.sessionModel.selectedData()
        self.classifierViewer.loadData(sr, geometry)
        
def main():
    app = basewindow.makeApp()
    data = []
    for session in ["data/floor3.examples/part1.pck", 
                    "data/floor3.examples/part2.pck",
                    "data/floor3.examples/part3.pck",
                    ]:
        stuff = cPickle.load(open(session))
        data.extend(stuff)
        
        
    wnd = MainWindow(data)
    wnd.show()
    app.exec_()

if __name__ == "__main__":
    main()
    