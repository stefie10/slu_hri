from PyQt4.QtCore import *
from qgis.core import *
import capturetool
import qgis_utils
import math2d
from PyQt4.QtGui import *
import basewindow
import yaml
import rubberBand
import pathAnnotationTableModel
import preposition
import pathAnnotatorWindow_ui
import tag_util
from muri import tkloader
import layers
import editorwindow
import spatialRelationClassifier
import os



class MainWindow(basewindow.BaseWindow, pathAnnotatorWindow_ui.Ui_MainWindow):
    def __init__(self, directory, engineMap=spatialRelationClassifier.engineMap):
        basewindow.BaseWindow.__init__(self, "Path Annotator")
        self.mapFrame.layout().addWidget(self.widget)
        self.directory = directory
        self.engineMap = engineMap
        self.figureLayer = None
        
        print "table", self.annotationTable
        self.model = pathAnnotationTableModel.Model(self.annotationTable, 
                                                    directory, self.engineMap)

        self.tagLayer = layers.openLayer(self.directory + "/tags", "tags", "ogr")
        layers.enableTextLabels(self.tagLayer, "name", size=18)
        self.addStaticLayer(self.tagLayer)
        self.editorWindow = editorwindow.makeWindow()
        self.editorWindow.engineMap = self.engineMap
        self.connect(self.actionNext, SIGNAL("triggered()"), self.next)

        self.connect(self.annotationTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectAnnotation)
        self.rubberBand = rubberBand.RubberBand(self.canvas, isPolygon=True)



        self.captureTool = capturetool.CaptureMapToolNoLayer(self.canvas,
                                                             QGis.WKBLineString,
                                                             self.tagLayer)
        self.editorToolbar = self.addToolBar("Editor Tools")
        self.addEditorTool(self.captureTool, "mActionCaptureLine.png", 
                           "Capture tool.")

        self.connect(self.captureTool,
                     SIGNAL("newFeature()"), 
                     self.newFigure)
        self.canvas.setMapTool(self.captureTool)
        self.annotationTable.selectRow(0)

    def setFigureLayer(self, layer):
        if not (self.figureLayer is None):
            self.deleteStaticLayer(self.figureLayer)
        self.figureLayer = layer
        self.addStaticLayer(self.figureLayer)
    def next(self):
        rowIdx = self.annotationTable.currentIndex().row()
        self.annotationTable.selectRow(rowIdx + 1)

    def selectAnnotation(self):
        dc = self.model.selectedData()
        self.editorWindow.setPreposition(dc.engine.name())
        #self.editorWindow.newGeometry(**dc.geometry)
        self.rubberBand.clear()

        minCorner, widthAndHeight = math2d.boundingBox(dc.ground)
        
        center = math2d.centroid(dc.ground)
        self.canvas.setExtent(qgis_utils.qgsRectFromCenterWidthHeight(center, (15, 15)))
        self.rubberBand.setPoints(dc.ground)        
        self.canvas.refresh()
        self.pathDescriptionLabel.setText("%s the %s" % (dc.engine.name(), dc.groundName))
        self.setFigureLayer(dc.figureLayer)
        
    def setFigure(self, geometry):
        self.figureLayer.startEditing()
        layers.clear(self.figureLayer)
        layers.addLineFeature(self.figureLayer, geometry)
        self.figureLayer.commitChanges()
        
    def newFigure(self):
        self.setFigure(self.captureTool.geometry)
        self.captureTool.reset()
        self.next()


def main():
    app = basewindow.makeApp()

    #nd = MainWindow("scratch.assignment/")
    wnd = MainWindow("data/floor3.examples/annotations.part3/")
    wnd.show()
    retval = app.exec_()


if __name__=="__main__":
    main()
