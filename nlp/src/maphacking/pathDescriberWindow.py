from PyQt4.QtCore import *
from PyQt4.QtGui import *
from descriptionTableModel import DescriptionCandidate
from muri import tkloader, pathDescriber
from qgis.core import *
import basewindow
import capturetool
import descriptionTableModel
import editorwindow
import layers
import math2d
import named_region
import os
import pathDescriberWindow_ui
import qgis_utils
import qt_utils
import rubberBand
import spatialRelationClassifier
import sys

class MainWindow(basewindow.BaseWindow, pathDescriberWindow_ui.Ui_MainWindow):
    def __init__(self, tagLayer, candidates):
        basewindow.BaseWindow.__init__(self, "HSP Spatial Queries")
        self.tagLayer = tagLayer
        layers.makeUniqueValueRenderer(self.tagLayer, "id")
        layers.enableTextLabels(self.tagLayer, "name", size=10)
        self.addStaticLayer(self.tagLayer)

        self.rubberBand = rubberBand.RubberBand(self.canvas, isPolygon=True)

        self.model = descriptionTableModel.Model(self.descriptionTable, 
                                                 candidates)

        self.descriptionTable.verticalHeader().hide()
        self.descriptionTable.horizontalHeader().hide()
        self.connect(self.descriptionTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectDescriptionCandidate)


        self.mapFrame.layout().addWidget(self.widget)
        editorToolbar = self.addToolBar("Editor Tools")
        self.toolCapture = capturetool.CaptureMapTool(self.canvas)
        actionCapture = self.baritem(QgsApplication.defaultThemePath() + \
                                         "/mActionCaptureLine.png", 
                                     "Draw paths.", self.capture,editorToolbar) 
        self.connect(self.toolCapture, SIGNAL("newFeature()"), 
                     self.newPath)
        self.pathLayers = []
        self.pathLayer = None
        
        self.editorWindow = editorwindow.makeWindow()
        self.editorWindow.engineMap = spatialRelationClassifier.engineMap

        self.canvas.setMapTool(self.toolCapture)
        self.zoomFull()
        self.connect(self.canvas, SIGNAL("xyCoordinates(QgsPoint &)"),
                     self.updateMousePosition)
        self.canvas.setExtent(QgsRect(109, 364, 335, 504))
        #color = layers.randomColor()
        color = QColor(0, 255, 255)
        #layers.formatLayer(self.tagLayer, color)
    def selectDescriptionCandidate(self, idx):
        dc = self.model.selectedData()
        feature = tkloader.featureForPolygon(self.tagLayer, dc.landmark)
        self.tagLayer.setSelectedFeatures([feature.id()])
        
        print "selected", dc, feature.id()
        print "selectedFeatures", self.tagLayer.selectedFeatureCount()
        print "features"
        self.editorWindow.setPreposition(dc.engine.name())
        self.editorWindow.newGeometry(**dc.geometry)
        for f in self.tagLayer.selectedFeatures():
            print "f", f, f.id()
            print "name", qt_utils.convertVariant(layers.attribute(self.tagLayer, f, 'name'))
        self.rubberBand.clear()
        self.rubberBand.setPoints(dc.landmark.vertices)
        self.generateInstructions(dc.path)
            
    def updateMousePosition(self, point):
        x, y = point
        self.coordinateLabel.setText("%.3f, %.3f" % (x, y))
    def newPath(self):
        self.generateInstructions(self.toolCapture.geometry)
    def newPathLayer(self, path):
        if self.pathLayer != None:
            self.pathLayers.append(self.pathLayer)
        self.pathLayer = layers.openOrEmpty("/tmp/%s/boundboxlayerand" % (os.getpid()), QGis.WKBLineString, [("id", "Integer")], "Paths")
        self.pathLayer.startEditing()

        layers.addNewFeature(self.pathLayer, path)
        layers.commit(self.pathLayer)
        self.toolCapture.setLayer(self.pathLayer)
        self.addStaticLayer(self.pathLayer)
        

    def generateInstructions(self, path):
        self.newPathLayer(path)
        print path[0]
        print "generating?"
        (minX, minY), (width, height) = math2d.boundingBox(path)
        rect = qgis_utils.qgsRectFromWidthHeight(*math2d.boundingBox(path))
        self.tagLayer.select(rect, False)

        self.descriptionLabel.setText("test")
        return
        for x in self.tagLayer.selectedFeatures():
            nr = named_region.TkNamedRegion(self.tagLayer, x)
            print "name", nr.name()
            print "x", nr.points
            preposition = pathDescriber.describe(nr.points, path)
            if preposition != None:
                self.descriptionLabel.setText("go %s the %s" % 
                                              (preposition, nr.name()))
                break
            
            
        

def makeWindow(polygons, figures):  
    """
    Display the window, showing all prepositions for all the
    landmarks, with all the figures.
    """
    #wnd = MainWindow(loadTagLayer("3rdParty/muri/tkdata/log4_s3.tag"))

    candidates = []
    for landmark in polygons:
        if not math2d.sorta_eq(math2d.signedArea(landmark.vertices), 0):
            for engine in spatialRelationClassifier.engineMap.values():
                for figure in figures:
                    candidates.append(DescriptionCandidate(engine, landmark, 
                                                           figure))

    wnd = MainWindow(tkloader.loadTagLayer(polygons), candidates)
    return wnd
def main(argv):
    app = basewindow.makeApp()
    wnd = makeWindow()
    wnd.show()
    retval = app.exec_()
    return QgsApplication.exitQgis()

if __name__ == "__main__":
    try:
        retval = main(sys.argv)
        sys.exit(retval)
    except:
        raise


