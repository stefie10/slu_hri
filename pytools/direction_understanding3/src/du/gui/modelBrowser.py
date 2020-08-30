import matplotlib_qt
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QMainWindow, QItemSelectionModel, QItemSelection

import tag_util
from du import dir_util
from du.srel_utils import createFigure
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from matplotlib.transforms import offset_copy
from qt_utils import CheckboxDrawer
from pyTklib import tklib_du_lp_obs
import basewindow
import cPickle
import landmarkSelector
import landmarkTableModel
import landmark_icon_cache
import math
import modelBrowser_ui
import numpy as na
import pylab as mpl
import sdcTableModel
import spatialRelationsSelector
import viewpointAndObservationProbabilityTableModel
import viewpointTableModel







def plot_map(gridmap):
    from carmen_maptools import plot_tklib_log_gridmap
    plot_tklib_log_gridmap(gridmap, cmap="carmen_cmap_gray")
    mpl.draw()

def plot_map_for_model(mymodel):
    plot_map(mymodel.clusters.get_map())


class ObservationDrawer(CheckboxDrawer):
    
    def p_link(self, entry):
        return entry.p_obs * entry.p_verb
    
    def doDraw(self, axes):

        plots = []
        if self.wnd.slocTable.currentIndex().row() != -1:
            sloc = self.wnd.slocModel.selectedData()
            x, y = sloc.loc

            entries = [e for e in self.wnd.jointViewpointModel._data if e.iSloc == sloc.vp_i]

            sum = na.sum([self.p_link(e) for e in entries])

            for e in entries:
                p_link = (self.p_link(e) / sum)
                if p_link != 0:
                    X = [e.sloc[0], e.eloc[0]]
                    Y = [e.sloc[1], e.eloc[1]]

                    X, Y = self.wnd.m4du.clusters.skel.compute_path(e.sloc, e.eloc)
                    
                    p3, = axes.plot(X, Y, '-', color="black", linewidth=1 + 5 * p_link)
                    #p3, = axes.plot(X, Y, color="black", linewidth=1 + 5 * p_link)
                    plots.append(p3)
            self.wnd.mpl_draw()
        return plots

class VerbDrawer(ObservationDrawer):
    def p_link(self, entry):
        return entry.p_verb
    

    

class ViewpointLandmarkDrawer(CheckboxDrawer):
    def doDraw(self, axes):
        plots = []

        markers = [entry.o_mat_prob for entry in self.wnd.slocModel._data]
        sum = na.sum(markers)
        markers = [m/sum for m in markers]
        markers = [-7*math.log(m) for m in markers]
        
        maxval = na.max(markers)
        markers = [maxval - m for m in markers]
        
        
        for entry, markersize in zip(self.wnd.slocModel._data, markers):
            print "drawing", entry.o_mat_prob
            x, y = entry.loc

            p, = axes.plot([x], [y], "g^", markersize=7 + markersize, markerfacecolor="#90ee90")
            plots.append(p)
        self.wnd.mpl_draw()
        return plots


class TopoDrawer(CheckboxDrawer):
    def doDraw(self, axes):
        plots = []
        m4du = self.wnd.m4du
        for topo_i, topo_key in enumerate(m4du.tmap_keys):
            x_s, y_s = m4du.tmap_locs[topo_key]
            plots.extend(axes.plot((x_s,), (y_s,), '+', markersize=10,
                                        markerfacecolor="white", markeredgecolor="black"))
        
            for topo_key in m4du.tmap[topo_key]:
                x_e, y_e = m4du.tmap_locs[topo_key]
                #plots.extend(axes.plot((x_s, x_e), (y_s, y_e), 'b-'))
        self.wnd.mpl_draw()                
        return plots
        
class TransitionDrawer(CheckboxDrawer):
    def doDraw(self, axes):
        plots = []
        if self.wnd.slocTable.currentIndex().row() != -1:

            sdcIdx = self.wnd.sdcTable.currentIndex().row()

            ua = self.wnd.m4du.mygm.update_args[sdcIdx]


            sloc = self.wnd.slocModel.selectedData()
            x, y = sloc.loc

            x_orig = [x]
            y_orig = [y]
            X_plt = []
            Y_plt = []
            X = []
            Y = []

            T_mat = ua["T_curr"]
            if T_mat != None and len(T_mat) != 0 and len(T_mat[0]) != 0:
                for j in range(len(self.wnd.m4du.viewpoints)):
                    topoend, orient_end = self.wnd.m4du.viewpoints[j].split("_")
                    orient_end = float(orient_end)
                    t_val = T_mat[j][sloc.vp_i]
                    if t_val > 0:
                        x, y = [[self.wnd.m4du.tmap_locs[float(topoend)][0]],
                                [self.wnd.m4du.tmap_locs[float(topoend)][1]]]
                        X_plt.extend([x, x_orig])
                        Y_plt.extend([y, y_orig])
                        X.append(x)
                        Y.append(y)
                        p3, = axes.plot(X_plt, Y_plt, color="black", linewidth=5*t_val)
                        plots.append(p3)
            self.wnd.mpl_draw()
        return plots

        
class MainWindow(QMainWindow, modelBrowser_ui.Ui_MainWindow):
    def mpl_draw(self):
        self.restoreLimits()
        self.figure.canvas.draw()



    def __init__(self, m4du, corpus_fname=None, addFigureToMainWindow=True):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.m4du = m4du
        self.m4du.save_update_args = True
        self.corpus_fname = corpus_fname
        

        self.extractor = dir_util.direction_parser_sdc()

        self.landmarkSelector = landmarkSelector.MainWindow(self.m4du)
        self.spatialRelationsSelector = spatialRelationsSelector.MainWindow(self.m4du)

        self.connect(self.landmarkSelector.landmarkSelectorTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectLandmarks)

        self.connect(self.submitButton,
                     SIGNAL("clicked()"),
                     self.followDirections)

        self.connect(self.zoomToMagicSpotButton,
                     SIGNAL("clicked()"),
                     self.load_ranges)

        self.connect(self.actionPreferences,
                     SIGNAL("triggered()"),
                     self.showPreferences)

        self.connect(self.actionClear,
                     SIGNAL("triggered()"),
                     self.clearDrawings)


        self.connect(self.actionSelectSpatialRelations,
                     SIGNAL("triggered()"),
                     self.showSpatialRelationsSelector)

        self.connect(self.actionSaveLimits,
                     SIGNAL("triggered()"),
                     self.saveLimits)

        self.connect(self.actionRestoreLimits,
                     SIGNAL("triggered()"),
                     self.restoreLimits)

        self.connect(self.jointVpToSlocElocButton,
                     SIGNAL("clicked()"),
                     self.jointVpToSlocEloc)

        self.connect(self.viewSrClassifierButton,
                     SIGNAL("clicked()"),
                     self.viewSrClassifier)
        
        self.figure = mpl.figure()
        self.axes = self.figure.gca()

        if addFigureToMainWindow:
            self.oldParent = self.figure.canvas.parent()
            self.figure.canvas.setParent(self)
            self.matplotlibFrame.layout().addWidget(self.figure.canvas)
        self.limits = None            
            
        self.figure.canvas.mpl_connect('draw_event', self.updateLimits)
        print "m4du", m4du, hasattr(self.m4du, "boundingBox")


        
         
        plot_map_for_model(self.m4du)
        
        self.pathPlot, = self.figure.gca().plot([], [], '--', linewidth=4, 
                                                color="black")    
        self.startPlot, = self.figure.gca().plot([], [], 'go-')    
        self.endPlot, = self.figure.gca().plot([], [], 'ro-')    
        self.selectedLandmarkPlot = None
        self.selectedElocPlots = []
        self.selectedSlocPlots = []
        self.selectedStartingSlocPlots = []
        self.correctElocPlots = []

        self.landmarkPlots = []
        self.plotLandmarks()


        self.transitionPlotDrawer = TransitionDrawer(self, self.slocTransitionsBox)
        self.observationPlotDrawer = ObservationDrawer(self, self.slocObservationProbabilityCheckBox)
        self.verbPlotDrawer = VerbDrawer(self, self.slocVerbProbabilityCheckBox)

        self.viewpointLandmarkPlotDrawer = ViewpointLandmarkDrawer(self, self.landmarkProbsCheckBox)
        
        self.topoDrawer = TopoDrawer(self, self.showTopologyBox)


        self.connect(self.filterBySlocBox, SIGNAL("stateChanged(int)"),
                     self.updateFilters)
        self.connect(self.filterByElocBox, SIGNAL("stateChanged(int)"),
                     self.updateFilters)
        
        self.connect(self.useSpatialRelationsBox, SIGNAL("stateChanged(int)"),
                     self.toggleSpatialRelations)
        self.connect(self.showLandmarksCheckBox, SIGNAL("stateChanged(int)"),
                     self.toggleLandmarks)

        self.connect(self.useWizardOfOzSdcsCheckBox, SIGNAL("stateChanged(int)"),
                     self.toggleSdcExtractor)
        #self.useWizardOfOzSdcsCheckBox.setCheckState(Qt.Checked)



        self.showLandmarksCheckBox.setCheckState(Qt.Unchecked)


        
        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
        self.addToolBar(self.toolbar)

        self.sdcModel = sdcTableModel.Model(self.m4du, self.sdcTable)
        self.landmarkModel = landmarkTableModel.Model(self.landmarkTable, 
                                                      self.m4du)

        #self.editorWindow = editorwindow.makeWindow()
        #self.editorWindow.engineMap = self.m4du.sr_class.engineMap
        #self.editorWindow.show()

        self.startingSlocModel = viewpointTableModel.Model(self.startingSlocTable, self.m4du, "starting sloc")
        self.jointViewpointModel = viewpointAndObservationProbabilityTableModel.Model(self.jointViewpointTable,
                                                                                      self.m4du)
        


        self.slocModel = viewpointTableModel.Model(self.slocTable, self.m4du, "sloc")
        self.elocModel = viewpointTableModel.Model(self.elocTable, self.m4du, "eloc")

        self.connect(self.jointViewpointTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectJointViewpoint)

        self.connect(self.sdcTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectSdc)

        self.connect(self.landmarkTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectLandmark)

        self.connect(self.slocTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectSloc)

        self.connect(self.startingSlocTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectStartingSloc)

        self.connect(self.elocTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectEloc)
        self.startingSlocTable.selectRow(133)
        
        if hasattr(self.m4du, "boundingBox") and self.m4du.boundingBox != None:
            X, Y = na.transpose(self.m4du.boundingBox)
            self.limits = min(X), max(X), min(Y), max(Y)
            self.mpl_draw()
    def clearDrawings(self):
        self.startPlot.set_data([], [])
        self.endPlot.set_data([], [])
        self.pathPlot.set_data([], [])
        for p in self.selectedElocPlots:
            p.remove()

        for p in self.selectedSlocPlots:
            p.remove()
        self.selectedSlocPlots = []

        for p in self.correctElocPlots:
            p.remove()
        self.correctElocPlots = []


        self.selectedElocPlots = []        
        self.mpl_draw()
    def showPreferences(self):
        self.landmarkSelector.show()

    def showSpatialRelationsSelector(self):
        self.spatialRelationsSelector.show()

    def updateFilters(self, state=None):
        if state != Qt.PartiallyChecked:
            if self.filterBySlocBox.checkState() == Qt.Checked:
                slocEntry = self.slocModel.selectedData()
                iSloc = slocEntry.vp_i
            else:
                iSloc = None

            if self.filterByElocBox.checkState() == Qt.Checked:
                elocEntry = self.elocModel.selectedData()
                iEloc = elocEntry.vp_i
            else:
                iEloc = None
            self.jointViewpointModel.setFilter(iSloc=iSloc, iEloc=iEloc)

    def updateProbabilityLabels(self):
        if (hasattr(self.m4du.mygm, "update_args") and 
            self.sdcTable.currentIndex().row() != -1 and
            self.slocTable.currentIndex().row() != -1 and 
            self.elocTable.currentIndex().row() != -1):


            sloc = self.slocModel.selectedData()
            eloc = self.elocModel.selectedData()

            sdc_i = self.sdcTable.currentIndex().row()
            e = self.sdcModel.selectedData()
            sdc = e.sdc

            ua = self.m4du.mygm.update_args[sdc_i]

            if "P_prev" in ua and sdc_i != 0:
                previous_sdc = self.sdcModel.get(sdc_i - 1)
                if previous_sdc.v1 == None or previous_sdc.v2 == None:
                    self.p_prev_label.setText("P_prev: Unknown viewpoints.")
                else:
                    P_prev = ua["P_prev"]
                    p_prev = P_prev[previous_sdc.v1, previous_sdc.v2]
                    equals_zero = (p_prev == 0)
                    if equals_zero:
                        zero_str = "=="
                    else:
                        zero_str = "!="
                    self.p_prev_label.setText("P_prev: %e, p_prev%s0" %  (p_prev, zero_str))
            else:
                self.p_prev_label.setText("Unknown")


            p_obs = na.exp(tklib_du_lp_obs(sloc.vp_i, 
                                    eloc.vp_i, 
                                    ua["vp_index_to_topo_index"],
                                    na.log(ua["T_curr"]),
                                    na.log(ua["D_curr"]),
                                    na.log(ua["SR_curr"]),
                                    na.log(ua["L_curr"]),
                                    na.log(ua["O_curr"]),
                                    ua["num_topologies"]))
            self.observationProbabilityLabel.setText("Observation: %.10f" % p_obs)
            p_trans = self.m4du.mygm.T_seq[sdc_i][eloc.vp_i][sloc.vp_i]
            self.tMatLabel.setText("Transition: %.10f" % p_trans)



            if self.landmarkTable.currentIndex().row() != -1 and sdc["sr"] != None:
                e = self.landmarkModel.selectedData()

                matrixKey = (self.m4du.sr_class.engineToIdx(sdc["sr"]),
                             sloc.topo_i, 
                             eloc.topo_i,
                             e.i)
                sr_prob = self.m4du.srel_mat[matrixKey]
                #assert e.sr_prob == sr_prob
                
                self.srProbabilityLabel.setText("SR: %.10f" % sr_prob)
            else:
                self.srProbabilityLabel.setText("SR: Unknown")            

        else:
            self.observationProbabilityLabel.setText("Observation: Unknown")

            self.tMatLabel.setText("Transition: Unknown")

            

    def toggleSpatialRelations(self, state):
        if state == Qt.Checked:
            self.m4du.use_spatial_relations = True
        elif state == Qt.Unchecked:
            self.m4du.use_spatial_relations = False
        elif state == Qt.PartiallyChecked:
            pass
        else:
            raise ValueError("Unepxected state: " + `state`)
        


    def toggleSdcExtractor(self, state):
        if state == Qt.Checked:
            self.extractor = dir_util.direction_parser_wizard_of_oz(self.corpus_fname, "stefie10")
        elif state == Qt.Unchecked:
            self.extractor = dir_util.direction_parser_sdc()
        elif state == Qt.PartiallyChecked:
            pass
        else:
            raise ValueError("Unepxected state: " + `state`)
        

    def selectLandmarks(self, start, end):
        self.toggleLandmarks()
        
    def toggleLandmarks(self, newState=None):
        state = self.showLandmarksCheckBox.checkState()
        if newState != None:
            state = newState
        if state == Qt.Checked:
            self.showLandmarks()
        elif state == Qt.Unchecked:
            self.hideLandmarks()
        elif state == Qt.PartiallyChecked:
            pass
        else:
            raise ValueError("Unepxected state: " + `state`)

        self.mpl_draw()

    def selectSdc(self):
        e = self.sdcModel.selectedData()
        sdc = e.sdc
        self.transitionPlotDrawer.updateState()
        self.updateProbabilityLabels()
        i = self.sdcTable.currentIndex().row()
        ua = self.m4du.mygm.update_args[i]

        self.landmarkModel.setData(self.m4du,
                                   `sdc["landmarks"]`, ua["L_curr"], 
                                   ua["SR_curr"], ua["num_topologies"],
                                   e.v1, e.v2)


        self.slocModel.setData(ua["O_curr"])
        self.elocModel.setData(ua["O_curr"])
        if e.v1 != None:
            self.slocTable.selectRow(e.v1)
        if e.v2 != None:
            self.elocTable.selectRow(e.v2)

        P_prev = None
        P_curr = None
        
        if "P_prev" in ua:
            P_prev = ua["P_prev"]
        if "P_curr"in ua:
            P_curr = ua["P_curr"]



        self.jointViewpointModel.load(ua["O_curr"], ua["T_curr"], 
                                      ua["D_curr"], ua["SR_curr"],
                                      ua["L_curr"], self.m4du.mygm.topo_i_to_location_mask,
                                      P_prev, P_curr)


    def viewSrClassifier(self):
        e = self.sdcModel.selectedData()
        self.editorWindow.setPreposition(e.sdc["sr"])
        print "distributions", self.editorWindow.engine._classifier.distribution
        print "geometry", self.geometry()
        self.editorWindow.newGeometry(**self.geometry())
        

    def geometry(self):
        sloc = self.slocModel.selectedData()
        eloc = self.elocModel.selectedData()
        e = self.landmarkModel.selectedData()
        print "calling createGround"
        return {
            "figure":createFigure(self.m4du.clusters, sloc.loc, eloc.loc),
            "ground":self.m4du.createGround(e.i)
            }


        
    def selectSrIdx(self):
        pass

    def draw_vp(self, loc, angle, format, plotargs):
        x, y = loc
        arrow_length = 2
        # e1, = self.figure.gca().plot([x, x + arrow_length*math.cos(math.radians(angle - 45))],
#                       [y, y + arrow_length*math.sin(math.radians(angle - 45))],
#                       "-", color="black")
#         e2,  = self.figure.gca().plot([x, x + arrow_length*math.cos(math.radians(angle + 45))],
#                        [y, y + arrow_length*math.sin(math.radians(angle + 45))],
#                       "-", color="black")
        e1 = self.figure.gca().arrow(x, y,
                                     arrow_length*math.cos(math.radians(angle)),
                                     arrow_length*math.sin(math.radians(angle)),
                                     width=1, facecolor="white")
        

        p, = self.figure.gca().plot([x], [y], format, **plotargs)

        return p, e1
        

    def selectJointViewpoint(self):
        pass
        #entry = self.jointViewpointModel.selectedData()
        #self.slocTable.selectRow(entry.iSloc)
        #self.elocTable.selectRow(entry.iEloc)

    def jointVpToSlocEloc(self):
        entry = self.jointViewpointModel.selectedData()
        self.slocTable.selectRow(entry.iSloc)
        self.elocTable.selectRow(entry.iEloc)

    def setExpectedElocs(self, iCorrectEloc, iActualEloc):
        correctEloc = viewpointTableModel.Entry(self.m4du, iCorrectEloc)

        for p in self.correctElocPlots:
            p.remove()
        self.correctElocPlots = []
        x, y = correctEloc.loc
        p, = self.figure.gca().plot([x], [y], 'ro', markersize=10)
        self.correctElocPlots.append(p)

        if iActualEloc != None:
            actualEloc = viewpointTableModel.Entry(self.m4du, iActualEloc)
            e = self.draw_vp(actualEloc.loc, 
                             actualEloc.angle,
                             "r*", dict(markersize=10))
            self.correctElocPlots.extend(e)
        self.mpl_draw()

    def selectStartingSloc(self):
        for p in self.selectedStartingSlocPlots:
            p.remove()

        self.selectedStartingSlocPlots = []

        sloc = self.startingSlocModel.selectedData()

        artists = self.draw_vp(sloc.loc, sloc.angle, 'go', dict(markersize=10))
        [self.selectedStartingSlocPlots.append(p) for p in artists]
        self.mpl_draw()



    def selectSloc(self):
        for p in self.selectedSlocPlots:
            p.remove()
        self.selectedSlocPlots = []

        sloc = self.slocModel.selectedData()
        p = self.draw_vp(sloc.loc, sloc.angle, 
                         'go', dict())
        self.selectedSlocPlots.extend(p)

        self.mpl_draw()
        self.landmarkModel.selectSloc(sloc.vp_i)
        self.updateProbabilityLabels()
        self.updateFilters()
        self.transitionPlotDrawer.updateState()


        vtags = self.m4du.topo_key_to_vtags[sloc.topo_key]

        self.visibleObjectsFromSlocLabel.setText("Sloc Visible: " + `vtags`)

        vtags = self.m4du.vp_i_to_vtags[sloc.vp_i]

        self.visibleObjectsFromOrientedSlocLabel.setText("Oriented Sloc Visible: " + `vtags`)
        

    def selectEloc(self):
        for p in self.selectedElocPlots:
            p.remove()
        self.selectedElocPlots = []

        eloc = self.elocModel.selectedData()
        
        p = self.draw_vp(eloc.loc, eloc.angle, 'ro', 
                         dict())

        self.selectedElocPlots.extend(p)
        self.mpl_draw()
        self.landmarkModel.selectEloc(eloc.vp_i)
        self.updateProbabilityLabels()




    def selectLandmark(self):
        print "selecting landmark"
        if not (self.selectedLandmarkPlot is None):
            self.selectedLandmarkPlot.remove()

            
        e = self.landmarkModel.selectedData()
        x, y = e.location
        self.selectedLandmarkPlot, = self.figure.gca().plot([x], [y], 'yo')

        print "drawing"
        self.mpl_draw()

        print "getting vtags"
        vtags, itags_t = self.m4du.obj_to_visibility[e.i]

        self.visibleObjectFromLandmarkLabel.setText("Visible: " + `vtags`)
        #self.visibleLandmarkLabel.setText("Invisible: " `itags_t`)


            
    def showLandmarks(self):
        self.hideLandmarks()
        indices = self.landmarkSelector.landmarkModel.selectedIndexes()
        for idx in indices:
            for x in self.landmarkPlots[idx]:
                x.set_visible(True)

    def hideLandmarks(self):
        for plots in self.landmarkPlots:
            for p in plots:
                p.set_visible(False)

        #self.landmarkPlots = []
    def plotLandmarks(self):
        #self.removeLandmarks()
        transOffset = offset_copy(self.figure.gca().transData, fig=self.figure,
                                  x=0.02, y=-0.17, units='inches')
        map = self.m4du.clusters.get_map()

        for obj in self.m4du.obj_geometries:
            x, y = obj.centroid()
            x, y = map.to_xy((x, y))

            icon = landmark_icon_cache.getIcon(obj.tag)
            if icon != None:
                width, height, channels = icon.shape
                draw_width = 1.5
                draw_height = draw_width*width/height
                lower_left_x = x - draw_width / 2.0
                lower_left_y = y - draw_height / 2.0
                
                img = self.figure.gca().imshow(icon, origin="lower",
                                 extent=(lower_left_x, lower_left_x + draw_width, 
                                         lower_left_y, lower_left_y + draw_height))
                self.landmarkPlots.append((img,))
            else:
                plots = []
                if isinstance(obj, tag_util.polygon) and False:
                    print "***", obj.tag
                    X, Y = na.transpose([map.to_xy((z, w))
                                         for z, w in zip(obj.X, obj.Y)])
                    print "plotting", X, Y                    
                    plots.extend(self.axes.plot(X, Y, "k-"))

                    plots.extend(self.axes.plot([X[0], X[-1]] ,
                                                [Y[0], Y[-1]], "k"))

                    plots.extend(self.axes.plot((x,), (y,), 'ro'))
                else:
                    plots.extend(self.axes.plot((x,), (y,), 'ko'))

                    
                text = obj.tag
                print "text", text, text.__class__
                if text == "landing":
                    text = "LZ"
                elif text == "charlie":
                    text = "CC"
                elif text == "triangle":
                    text = "TR"
                elif text == "flagpole":
                    text = "FP"
                text = " " + text
                plots.append(self.axes.text(x, y, text,
                                            transform=transOffset,
                                            size=16))
                
                self.landmarkPlots.append(plots)


    def followDirections(self):
        sentence = self.directionsTextEdit.toPlainText()
        sentence = str(sentence)
        self.runSentence(sentence)

    def runSentence(self, sentence, iSloc = None, call_callback=True):
        print "running", sentence
        #sentence = sentence.lower()
        #sentence = sentence.replace('camp', 'the camp') # camp charlie doesn't always parse. 
        #sentence = sentence.replace("to the", ", to the")
        #if sentence[-1] != ".":
        #    sentence = sentence + "."
        self.directionsTextEdit.document().setPlainText(sentence)
        sdcs = self.extractor.extract_SDCs(sentence)
        print "mysdcs:", sdcs
        #raw_input()
        
        if iSloc != None:
            if isinstance(iSloc, int):
                iSlocs = [iSloc]
            else:
                iSlocs = iSloc


            self.startingSlocTable.selectionModel().clear()
            for iSloc in iSlocs:
                self.startingSlocTable.selectionModel().select(self.startingSlocModel.index(iSloc, 0),
                                                               QItemSelectionModel.Rows | QItemSelectionModel.SelectCurrent)

            self.selectStartingSloc()
                
                
            #self.startingSlocTable.selectRow(iSloc)
            slocs = [x for x in self.startingSlocModel._data if x.vp_i in iSlocs]
        else:
            slocs = self.startingSlocModel.selectedEntries()
        print "slocs", [x.vp_i for x in slocs]
        assert (na.array([e.loc for e in slocs]) == slocs[0].loc).all()
        orients = [math.radians(e.angle) for e in slocs]

        infer_path = self.m4du.infer_path
        results = []

        #cProfile.runctx("self.m4du.infer_path(sdcs, sloc.loc, math.radians(sloc.angle))", globals(), locals(), "out.prof")
        #if "stop" in sentence:
        #    return []
        path, lprob, sdc_utilized = self.m4du.infer_path(sdcs,
                                                         vp_slocs_i=[x.vp_i for x in slocs])
        
        print "path", path
        def callback():
            if lprob == 0.0:
                zero = True
            else:
                zero = False
            self.overallscore_label.setText("Overall Score: %e" % lprob +
                                            " isZero: " + `zero`)
            path_str = ["%d %s" % (self.m4du.vpt_to_num[p], p) for p in path]
            self.pathLabel.setText(`path_str`)
            self.plot(path)
            print "sdc_utilized:", sdc_utilized
            self.sdcModel.setData(sdc_utilized, path)
            self.sdcTable.selectRow(0)
            self.mpl_draw()
        
        self.callback = callback
        if call_callback:
            self.callback()
        return path

    def draw_viewpoint_paths(self):
        paths = set()
        for vp1_i, vp1 in enumerate(self.m4du.viewpoints):
            topo_start, topo_start_ang = vp1.split("_")
            topo_start = float(topo_start)

            for vp2_i, vp2 in enumerate(self.m4du.viewpoints):
                topo_end, topo_end_ang = vp2.split("_")
                topo_end = float(topo_end)

                if (topo_end in self.m4du.tmap[topo_start] or
                    topo_start in self.m4du.tmap[topo_end]):
                    paths.add((topo_start, topo_end))


        for topo_st, topo_end in paths:
            loc1 = self.m4du.tmap_locs[float(topo_st)]
            loc2 = self.m4du.tmap_locs[float(topo_end)]
            print "loc", loc1
            X, Y = self.m4du.clusters.skel.compute_path(loc1, loc2)
            self.figure.gca().plot(X, Y, ':', linewidth=1, color="black")

        self.figure.gca().xticks([])
        self.figure.gca().yticks([])
            
    def plot(self, path):
        X = []
        Y = []

        if len(path) != 0:
            if isinstance(path[0], int):
                path = [self.m4du.viewpoints[p] for p in path]
            path1 = [key.split("_")  for  key in path]
            
            path_X = []
            path_Y = []
            first = True
            for (topo1, orient1) in path1:
                loc1 = self.m4du.tmap_locs[float(topo1)]
                print loc1

            for (topo1, orient1), (topo2, orient2) in zip(path1, path1[1:]):
                loc1 = self.m4du.tmap_locs[float(topo1)]

                loc2 = self.m4du.tmap_locs[float(topo2)]
                if first:
                    path_X.append(loc1[0])
                    path_Y.append(loc1[1])
                    first = False

                X, Y = self.m4du.clusters.skel.compute_path(loc1, loc2)
                path_X.extend(X)
                path_Y.extend(Y)

            self.pathPlot.set_data(path_X, path_Y)

            if len(X) >  1:
                self.startPlot.set_data([path_X[0], path_Y[0]])
                self.endPlot.set_data([path_X[-1], path_Y[-1]])
                self.slocTable.selectRow(self.m4du.vpt_to_num[path[0]])
                self.elocTable.selectRow(self.m4du.vpt_to_num[path[-1]])

    def loadResult(self, result):
        self.directionsTextEdit.setPlainText(result.sentence)
        self.startingSlocTable.selectRow(result.iCorrectSloc)
        self.setExpectedElocs(result.iCorrectElocs[0], result.iActualEloc)

        
    def load_ranges(self):
        #self.load_ranges_left_right()
        self.load_ranges_ex()

    def load_ranges_left_right(self):
        self.figure.gca().xlim(40, 80)
        self.figure.gca().ylim(2, 14)
        self.figure.gca().draw()
    def load_ranges_trans(self):
        self.figure.gca().xlim(14, 28)
        self.figure.gca().ylim(20, 35)
        self.figure.gca().draw()

    def load_ranges_ex(self):
        self.figure.gca().set_xlim(15, 62)
        self.figure.gca().set_ylim(15, 35)
        self.showLandmarksCheckBox.setCheckState(Qt.Checked)
        #self.matplotlibFrame.layout().removeWidget(self.figure.canvas)    
        #self.figure.canvas.setParent(self.oldParent)
        #self.figure.set_size_inches(6, 6)
        landmarks = [6, 7, 8, 16, 20, 21, 24, 25, 26, 29, 
                     167, 168, 52, 53, 54, 55, 101, 102, 105, 106, 36, 38, 41, 44, 71]

        self.landmarkSelector.landmarkModel.selectIndexes(landmarks)
        self.figure.gca().draw() # call this to get mpl in its own window

    def updateLimits(self, mplEvent):
        self.saveLimits()
    def saveLimits(self):
        self.limits = self.axes.axis()
    def restoreLimits(self):
        if self.limits != None:
            self.axes.axis(self.limits)

    
def main(argv):

    model_fname = argv[1]
    corpus_fname = argv[2]

    m4du = dir_util.load(argv[1])

    print "tags"


    app = basewindow.makeApp()
    wnd = MainWindow(m4du, corpus_fname, addFigureToMainWindow=True)
    wnd.setWindowTitle(model_fname)
    wnd.show()

    #wnd.followDirections()
    #wnd.load_ranges()
    #wnd.draw_viewpoint_paths()
    #self.figure.gca().show()
    #wnd.plot([4, 12])

    
    app.exec_()

        
if __name__=="__main__":
    import sys
    main(sys.argv)

