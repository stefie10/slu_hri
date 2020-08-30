from PyQt4.QtCore import *
from PyQt4.QtGui import *
from du.gui.modelBrowser import plot_map_for_model
from du.gui.resultsBrowser import pathOverlay_ui, sentenceResultsTableModel
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
import math2d
import matplotlib
import pylab as mpl
import random

matplotlib.use('Qt4Agg')




class MainWindow(QMainWindow, pathOverlay_ui.Ui_MainWindow):
    def __init__(self, m4du):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.m4du = m4du
        self.initializeMatplotlib()

        self.setWindowTitle("path overlay")
        plot_map_for_model(self.m4du)
        self.path_plots = []
        self.selected_vp_plots = []
        self.cached_results = None

        self.resultsModel = sentenceResultsTableModel.Model(self.resultsTable, 
                                                            self.m4du)
        
        self.connect(self.resultsTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectResult)

        self.connect(self.renderButton,
                     SIGNAL("clicked()"),
                     self.plotPaths)        
    def selectResult(self):
        for p in self.selected_vp_plots:
            p.remove()
        self.selectedDirectionLabel.setText("")
        self.selected_vp_plots = []
        first = True

        for idx in self.resultsTable.selectedIndexes():
            e = self.resultsModel.get(idx.row())
            if first:
                self.selectedDirectionLabel.setText(e.directions)
                first = False
            eloc_topo_st,  eloc_ang = self.m4du.viewpoints[e.iActualEloc].split("_")
            x, y = self.m4du.tmap_locs[float(eloc_topo_st)]
            p, = self.axes.plot([x], [y], "b+", markersize=15, 
                                markeredgewidth=4)

            self.selected_vp_plots.append(p)
        self.figure.canvas.draw()
    def initializeMatplotlib(self):
        self.figure = mpl.figure()
        self.oldParent = self.figure.canvas.parent()
        self.figure.canvas.setParent(self)
        self.canvasFrame.layout().addWidget(self.figure.canvas)
        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
        self.addToolBar(self.toolbar)

    @property
    def axes(self):
        return self.figure.gca()


    def draw_whole_path(self, path):
        path_plots = []
        for vp1_st, vp2_st in zip(path, path[1:]):

            print vp1_st
            sloc_topo_st, sloc_ang  = vp1_st.split("_")
            sloc = self.m4du.tmap_locs[float(sloc_topo_st)]

            eloc_topo_st,  eloc_ang = vp2_st.split("_")
            eloc = self.m4du.tmap_locs[float(eloc_topo_st)]




            X, Y = self.m4du.clusters.skel.compute_path(sloc, eloc)
            p3, = self.axes.plot(X, Y, '-', color="black")
            path_plots.append(p3)
        return path_plots
    def plotPaths(self, results=None):

        self.resultsModel.setEntries(results)
        if results == None:
            if self.cached_results != None:
                results = self.cached_results
            else:
                raise ValueError("Passed no results, and no cached results.")
        else:
            self.cached_results = results
        for p in self.path_plots:
            p.remove()
        self.path_plots = []

        true_eloc_i = results[0].iCorrectElocs[0]
        topo_st, ang = self.m4du.viewpoints[true_eloc_i].split("_")
        true_eloc = self.m4du.tmap_locs[float(topo_st)]

        radius = self.radiusBox.value()
        plot = matplotlib.patches.Ellipse(true_eloc, radius*2, radius*2, 
                                          facecolor='none',
                                          linewidth=5)
        self.axes.add_patch(plot)
        self.path_plots.append(plot)

        random.seed(3)
        total = 0.0
        num_within_radius = 0.0
        
        for e in results:
            for path in e.paths:
                eloc_topo_st,  eloc_ang = path[-1].split("_")
                x, y = self.m4du.tmap_locs[float(eloc_topo_st)]
                x += random.uniform(-1, 1)
                y += random.uniform(-1, 1)
                p, = self.axes.plot([x], [y], "r^", markersize=15)
                self.path_plots.append(p)
                if math2d.dist((x, y), true_eloc) < radius:
                    num_within_radius += 1
                total += 1

                sloc_topo_st,  sloc_ang = path[0].split("_")
                x, y = self.m4du.tmap_locs[float(sloc_topo_st)]
                p, = self.axes.plot([x], [y], "g^", markersize=15)
                self.path_plots.append(p)


        self.fractionWithinCircleLabel.setText("%.3f" % (num_within_radius/total))
        self.figure.canvas.draw()        
                
