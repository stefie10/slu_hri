from PyQt4.QtCore import *
from PyQt4.QtGui import *
import engine_model
import engine_ui
import feature_model




class MainWindow(QMainWindow, engine_ui.Ui_MainWindow):
    def __init__(self, classifiers):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Features")
        self.engineModel = engine_model.Model(self.engineTable, classifiers)
        
        self.featureModel = feature_model.Model(self.featureTable)
        
        self.connect(self.engineTable.selectionModel(),
                     SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.selectEngine)

        self.connect(self.featureTable.selectionModel(),
                     SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.selectFeature)


        self.engineTable.selectRow(0)

    @property
    def classifier(self):
        if self.engineModel.rowCount() != 0:
            return self.engineModel.selectedData()
        else:
            return None
    
    @property
    def feature(self):
        return self.featureModel.selectedData()
        
    def selectByName(self, name):
        self.engineTable.selectRow(self.engineModel.idxForName(name))
    def selectEngine(self):
        print "selecting feature"
        self.featureModel.setClassifier(self.classifier)
        self.updateLabels()
        self.emit(SIGNAL("selectedEngine"), (self.classifier,))

    def selectFeature(self):
        self.emit(SIGNAL("selectedFeature"), (self.featureModel.selectedData()))

        
    def updateLabels(self):
        print "updating labels", self.classifier.has_data
        if self.classifier.has_data:
            
            self.classLabel.setText(str(self.classifier.cls))
            self.pTrueLabel.setText("%e" % self.classifier.pTrue)
    def update(self):
        print "classifier", self.classifier
        self.featureModel.reset()
        self.updateLabels()
        

        
                                
