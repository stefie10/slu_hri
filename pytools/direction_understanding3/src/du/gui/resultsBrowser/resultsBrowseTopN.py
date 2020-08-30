import matplotlib
matplotlib.use("Qt4Agg")
from tag_util import tag_file
import sqlite3
from environ_vars import TKLIB_HOME
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
import trackBrowser_ui
import basewindow
import pointModel
import trackModel
import read_tracks
import squintPlayer.player
import squintReader
import pylab as mpl
import traceback
from carmen_maptools import plot_tklib_log_gridmap

class MainWindow(QMainWindow, trackBrowser_ui.Ui_MainWindow):
    def __init__(self, tag_fname, map_fname):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.tag_file = tag_file(tag_fname, map_fname)

        self.initializeMatplotlib()

        plot_tklib_log_gridmap(self.tag_file.get_map())


        self.playerWindow = squintPlayer.player.Window()
        self.playerWindow.show()


        self.pointModel = pointModel.Model(self.pointTable)
        

        self.trackModel = trackModel.Model(self.trackTable)


        self.connect(self.trackTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectTrack)
        self.limits = [0, 0, 100, 100]
        self.plots = []
        self.figure.canvas.mpl_connect('draw_event', self.updateLimits)

#    def load(self, tracks):
#        self.trackModel.load(tracks)

#    def updateLimits(self, event):
#        self.limits = self.axes.axis()
#        

#    @property
#    def player(self):
#        return self.playerWindow.player

#    def draw(self):
#        for p in self.plots:
#            try:
#                p.remove()
#            except NotImplementedError:
#                pass

#        self.plots = []
#        track = self.trackModel.selectedData()
#        X, Y = track.points_XY
#        self.plots.extend(self.axes.plot(X, Y))
#        self.figure.canvas.draw()        

#        
#    def selectTrack(self):
#        track = self.trackModel.selectedData()
#        self.pointModel.load(track)

#        print track.merged_track_id
#        print track.tracklet_id
#        
#        self.draw()

#        
#        try:
#            self.player.gotoDatetime(track.start_time, track.end_time,
#                                     channel=track.points[0].channel_id)
#        #except squintReader.SquintError:
#        except:
#            print "ignoring squint error"
#            traceback.print_exc()
#            
#    def initializeMatplotlib(self):
#        self.figure = mpl.figure()
#        self.axes = mpl.gca()
#        self.oldParent = self.figure.canvas.parent()
#        self.figure.canvas.setParent(self)
#        self.canvasFrame.layout().addWidget(self.figure.canvas)
#        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
#        self.addToolBar(self.toolbar)

        
    
def main():
    from sys import argv
    
    app = basewindow.makeApp()

    track_fname = "%s/pytools/video_retrieval/3rdParty/cogmac_slimd2/slimd2/data/worldtracks_2c_hsp_01-01-07_combined.db" % TKLIB_HOME

    tag_fname = "%s/data/directions/direction_hsp/tags/objects.tag" % TKLIB_HOME
    map_fname = "%s/data/directions/direction_hsp/hsp.cmf" % TKLIB_HOME
    
    wnd = MainWindow(tag_fname, map_fname)
    wnd.setWindowTitle("Track Browser")

    tracks = read_tracks.readTracks(track_fname)
    wnd.load(tracks)

    wnd.show()
    app.exec_()


if __name__ == "__main__":
    main()
