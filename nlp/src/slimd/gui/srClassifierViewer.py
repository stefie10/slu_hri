from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from slimd.features import MatplotlibDrawer
from slimd.gui import srClassifierViewer_ui, geometry_model, engine_model, \
    feature_model
from voom.gui import capturers
import basewindow
import math2d
import matplotlib
import numpy as na
import pylab as mpl
import spatialRelationClassifier
matplotlib.use("Qt4Agg")









class MainWindow(QMainWindow, srClassifierViewer_ui.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)    
        self.initializeMatplotlib()
        self.plots = []
        self.geometryModel = geometry_model.Model(self.geometryTable)
        
        self.connect(self.actionClassify,
                     SIGNAL("triggered()"),
                     self.classify)

        
        self.engineModel = engine_model.Model(self.engineTable)
        self.engineModel.loadData(spatialRelationClassifier.engineMap)
        
        self.featureModel = feature_model.Model(self.featureTable)
        
        self.connect(self.featureTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectFeature)

        self.drawer = MatplotlibDrawer(self.figure)

    def draw(self):
        print "drawing"
        for r in self.plots:
            r.remove()
        self.plots = []
        colorMap = {"figure":"blue", "ground":"red"}
        for k, geometry in self.geometry.iteritems():
            if k == "ground":
                geometry = math2d.polygonToLine(geometry)
            X, Y = na.transpose(geometry)
            
            line, = self.axes.plot(X, Y, color=colorMap[k], linewidth=1.5)
            self.plots.append(line)
            
        selectedFeature = self.featureModel.selectedData()
        if selectedFeature != None:
            for drawCommand in selectedFeature.drawCommands:
                print drawCommand
                method = eval("self.drawer.%s" % drawCommand["name"])
                self.plots.extend(method(*drawCommand["args"]))
            
        mpl.draw()
            
    @property
    def engine(self):
        entry = self.engineModel.selectedData()
        return entry.engine
    
        
    def classify(self):
        print "geom", self.geometry
        cls, probabilities, example = self.engine.classify(**self.geometry)

        self.classificationLabel.setText(`cls`)
        self.featureModel.loadData(example)
        self.featureTable.selectRow(0)
        
        
    def loadData(self, sr, geometry):
        print "loading", geometry
        self.geometry = geometry
        self.geometryModel.loadData(geometry)
        self.draw()
        print
        
        
    def initializeMatplotlib(self):
        self.figure = mpl.figure()
        self.axes = mpl.gca()
        self.oldParent = self.figure.canvas.parent()
        self.figure.canvas.setParent(self)
        self.canvasFrame.layout().addWidget(self.figure.canvas)
        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
        self.addToolBar(self.toolbar)

    def initializeCapturePolygon(self):
        self.capturePolygon = capturers.PolygonCapturer()

        self.connect(self.captureAgentGeomButton,
                     SIGNAL("clicked()"),
                     self.captureAgentGeom)

        self.connect(self.clearAgentGeomButton,
                     SIGNAL("clicked()"),
                     self.capturePolygon.reset)

        self.connect(self.capturePolygon, SIGNAL("completedPolygon"),
                     self.completedPolygon)
    def initializeCapturePoint(self):
        self.capturePoint = capturers.PointOrientationCapturer()
        self.connect(self.placeAgentButton,
                     SIGNAL("clicked()"),
                     self.captureAgentLocation)

        self.connect(self.capturePoint, SIGNAL("completedPoint"),
                     self.completedPoint)
        
    def selectFeature(self):
        
        self.draw()

    
def main():
    
    app = basewindow.makeApp()

    wnd = MainWindow()
    wnd.setWindowTitle("Spatial Relation Classifier Viewer")
    wnd.show()
    #wnd.open("data/motion_verbs/follow/follow1.pck")
    app.exec_()


if __name__ == "__main__":
    main()
    