import matplotlib_qt
from PyQt4.QtCore import SIGNAL, Qt, QAbstractListModel
from PyQt4.QtGui import QMainWindow
import basewindow
import cPickle
import matrixBrowserModel
import nwayVsBinaryModel
import spatialRelationMatrixBrowser_ui
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
import pylab as mpl
from numpy import transpose as tp
from itertools import chain

class EngineModel(QAbstractListModel):
    def __init__(self, engineMap, view):
        QAbstractListModel.__init__(self)
        self.view = view
        self.view.setModel(self)
        self.engineMap = engineMap
        self.engines = list(sorted(self.engineMap.keys()))
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.engines[index.row()]
        else:
            return None
    def rowCount(self, idx):
        return len(self.engines)
    def selectedData(self):
        data = []
        for idx in self.view.selectionModel().selectedRows():
            data.append(self.engines[idx.row()])
        return data[0]

class MainWindow(QMainWindow, spatialRelationMatrixBrowser_ui.Ui_MainWindow):

    def mpl_draw(self):
        self.restoreLimits()
        self.figure.canvas.draw()
    def updateLimits(self, mplEvent):
        self.saveLimits()
    def saveLimits(self):
        self.limits = self.axes.axis()
    def restoreLimits(self):
        if self.limits != None:
            self.axes.axis(self.limits)

    def __init__(self, m4du):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.figure = mpl.figure()
        self.axes = self.figure.gca()
        self.axes.set_aspect("equal")
        self.oldParent = self.figure.canvas.parent()
        self.figure.canvas.setParent(self)
        self.matplotlibFrame.layout().addWidget(self.figure.canvas)
        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
        self.addToolBar(self.toolbar)
        self.limits = [-20, 30, 10, 51]
        self.restoreLimits()
        self.figure.canvas.mpl_connect('draw_event', self.updateLimits)

        self.m4du = m4du


        self.engineModel = EngineModel(self.m4du.sr_class.engineMap, 
                                       self.engineMapListView)

        self.matrixModel = matrixBrowserModel.Model(self.matrixBrowserTable, 
                                                    self.m4du)

        self.nwayVsBinaryModel = nwayVsBinaryModel.Model(self.nwayVsBinaryTable)
        
        self.connect(self.engineMapListView.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectEngine)

        self.connect(self.matrixBrowserTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectScore)

        
        self.connect(self.nwayVsBinaryTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.draw)


        
        #self.engineModel.selectByName("past")

    def selectEngine(self):
        engine = self.engineModel.selectedData()
        self.matrixModel.selectEngine(engine)
        print "selected", engine, engine.__class__
        engineData = self.matrixModel.currentEngineData()
        entries = []
        for i in chain(range(0, 10), range(130579, 130579+10),
                       range(106095, 106095 + 10)):
            engine, idxTuple, score = engineData.get(i)
            print "metadata..."
            metadata = self.m4du.metadataForMatrixKey(idxTuple)
            print "done"
            geometry = metadata.args
            if geometry["figure"] == None:
                continue

            e = nwayVsBinaryModel.Entry(i, engine.name(), score, geometry)

            entries.append(e)
        print "setting data"
        self.nwayVsBinaryModel.setData(entries)

    def selectScore(self):
        print "selected score"
        engine, idxTuple, score = self.matrixModel.selectedData()
        print "idxTuple", idxTuple, score
        metadata = self.m4du.metadataForMatrixKey(idxTuple)
        print "args", metadata.args
        #self.editorWindow.setPreposition(metadata.engine.name())        
        #self.editorWindow.newGeometry(**metadata.args)

    def draw(self):
        print "drawing"
        self.axes.clear()
        entry = self.nwayVsBinaryModel.selectedEntry()
        print "plotting", entry.nway_score
        g = entry.geometry
        X, Y = tp(g["figure"])
        self.axes.plot(X, Y, color="blue")

        X, Y = tp(g["landmark"] + [g["landmark"][0]])
        self.axes.plot(X, Y, color="red")

        self.figure.canvas.draw()


        

def main(argv):
    import time
    start = time.time()
    m4du = cPickle.load(open(argv[1], 'r'))
    m4du.initialize()
    end = time.time()
    print "took %.2f seconds" % (end - start)
    app = basewindow.makeApp()
    wnd = MainWindow(m4du)
    wnd.show()
    retval = app.exec_()


if __name__=="__main__":
    import sys
    main(sys.argv)

