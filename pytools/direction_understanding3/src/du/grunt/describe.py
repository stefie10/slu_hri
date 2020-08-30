import spatialRelationClassifier
import basewindow
import describe_ui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import classifierResultTableModel as crtm



class MainWindow(QMainWindow, describe_ui.Ui_MainWindow):
    def __init__(self, verbEngineMap, srEngineMap):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Path Describer")
        layout = QVBoxLayout(self.mapFrame)
        self.srEngineMap = srEngineMap
        self.verbEngineMap = verbEngineMap

        self.engine = self.srEngineMap["to"]


        self.srResultModel = crtm.Model(self.srResultTable, self.srEngineMap)
        self.verbResultModel = crtm.Model(self.verbResultTable, 
                                          self.verbEngineMap)
        

        self.connect(self.actionGenerate, SIGNAL("triggered()"), 
                     self.generate)        

    
    def geometry(self):
        geometries = {}
        for key in self.engine.signature():
            if key in self.editableLayers:
                layer = self.editableLayers[key]['layer']
                type = self.engine.type(key)
                geometries[key] = self.engine.geomFromLayer(key, layer)

        return geometries
                            

    def generate(self, geometry=None):
        if geometry == None:
            geometry = self.geometry()
        self.srResultModel.setGeometry(geometry)
        #self.verbResultModel.setGeometry(geometry)
        return None, self.srResultModel.get(0)
        



            

                    

def main():
    app = basewindow.makeApp()
    
    srEngineMap = dict([(key, spatialRelationClassifier.engineMap[key]) 
                      for key in ["across", "through", "past", "around", 
                                  "to", "out", "towards", "away from", 
                                  "until"]])

    verbEngineMap = dict([(key, spatialRelationClassifier.engineMap[key]) 
                      for key in ["turnLeft", "turnRight", "straight"]])
    wnd = MainWindow(verbEngineMap, srEngineMap)
    wnd.show()
    retval = app.exec_()


if __name__ == "__main__":
    main()

    
