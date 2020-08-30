import matplotlib
matplotlib.use("Qt4Agg")
from tag_util import tag_file
from environ_vars import TKLIB_HOME
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
import basewindow
import pylab as mpl
from carmen_maptools import plot_tklib_log_gridmap, carmen_cmap_gray
from du.tagFileGui import annotator_ui, tagModel, capturers
import tag_util
from qt_utils import convertVariant
import scipy as na

class MainWindow(QMainWindow, annotator_ui.Ui_MainWindow):
    def __init__(self, tag_fname, map_fname):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tag_fname = tag_fname
        self.tag_file = tag_file(self.tag_fname, map_fname)

        self.initializeMatplotlib()

        plot_tklib_log_gridmap(self.tag_file.get_map(), cmap="carmen_cmap_white",
                               set_rc=True)

        self.plots = []
        self.figure.canvas.mpl_connect('draw_event', self.updateLimits)
        self.tagModel = tagModel.Model(self.tagTable)
        self.tagModel.load(self.tag_file)

        self.connect(self.tagTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectTag)

        self.connect(self.capturerList.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.changeCapturer)


        self.capturePolygon = capturers.PolygonCapturer()
        self.capturePoint = capturers.PointCapturer()
        
        self.connect(self.capturePolygon, SIGNAL("completedPolygon"),
                     self.completedPolygon)

        self.connect(self.capturePoint, SIGNAL("completedPoint"),
                     self.completedPoint)        

        self.connect(self.actionSave,
                     SIGNAL("triggered()"),
                     self.save)        


        self.connect(self.actionDeleteTags,
                     SIGNAL("triggered()"),
                     self.deleteTags)   
                
        self.capturers = [self.capturePoint,
                          self.capturePolygon,
                          ]


        self.timer = QTimer()
        self.timer.setSingleShot(True)
        def init():
            self.capturerList.setCurrentRow(0)
        self.connect(self.timer, SIGNAL("timeout()"), init)
        self.timer.start(10)

    def save(self):
        tag_util.save_polygons(self.tagModel.getPoints(),
                               self.tagModel.getPolygons(),
                               self.tag_fname)
    def updateLimits(self, event):
        self.limits = self.axes.axis()


    def deleteTags(self):
        self.tagModel.delete(self.tagModel.selectedEntries())

    def selectTag(self):
        self.draw()

    def changeCapturer(self):
        self.capturer = self.capturers[self.capturerList.currentIndex().row()]

        for c in self.capturers:
            c.deactivate()

        self.capturer.activate(self.figure)


    def askForTag(self):
        tag = str(QInputDialog.getText(self, "Tag", "Type a tag")[0])
        return tag
    def completedPolygon(self, polygon):
        print "completed polygon", na.transpose(polygon)

        tag = self.askForTag()

        outp = tag_util.polygon()
        outp.X, outp.Y = na.transpose([self.tag_file.get_map().to_index(p)
                                       for p in polygon])
        outp.tag = tag
        self.tagModel.add(outp)
            
    def completedPoint(self, point):
        print "got", point
        tag = self.askForTag()

        outp = tag_util.point()
        outp.x, outp.y = self.tag_file.get_map().to_index(point)
        outp.tag = tag
        
        self.tagModel.add(outp)        
        
    def draw(self):
        for p in self.plots:
            try:
                p.remove()
            except NotImplementedError:
                pass

        self.plots = []

        self.drawTags(self.plots)
        self.axes.axis(self.limits)
        self.figure.canvas.draw()

    def drawTags(self, plots):
        print "drawing"
        for o in self.tagModel.selectedEntries():
            X, Y = o.geometry
            plot = self.axes.plot(X, Y, 'ro-')  

            lst = []
            for x, y in zip(X, Y):
                lst.append((x, y))
            print "plotting"
            print lst
            
            plots.extend(plot)        

        
            
    def initializeMatplotlib(self):
        self.figure = mpl.figure()
        self.axes = mpl.gca()
        self.oldParent = self.figure.canvas.parent()
        self.figure.canvas.setParent(self)
        self.canvasFrame.layout().addWidget(self.figure.canvas)
        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
        self.addToolBar(self.toolbar)

        
    
def main():
    from sys import argv
    
    app = basewindow.makeApp()

    map_fname = argv[1]
    tag_fname = argv[2]

    #tag_fname = "%s/data/directions/direction_hsp/tags/objects.tag" % TKLIB_HOME
    #map_fname = "%s/data/directions/direction_hsp/hsp.cmf" % TKLIB_HOME
    
    wnd = MainWindow(tag_fname, map_fname)
    wnd.setWindowTitle("Track Browser")
    wnd.show()
    app.exec_()


if __name__ == "__main__":
    main()
