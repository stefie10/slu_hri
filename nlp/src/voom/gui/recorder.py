from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime, timedelta
from environ_vars import TKLIB_HOME
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from qt_utils import CheckboxDrawer
from voom import agents, mpl_drawer, trainer_pacman
from voom.event_logic.primitives import IsMoving, IsVisible, IsClose, \
    MovingTowards
from voom.gui import recorder_ui, pathModel
from voom.gui.assignments import assignmentData
import agentModel
import basewindow
import cPickle
import capturers
import carmen_maptools
import engine
import landmarkSelector
import math
import math2d
import matplotlib
import numpy as na
import pylab as mpl
import tag_util
import timeline
import turtle

names = ["figure", "landmark", "landmark2", "a", "b", "c", "d", "e"]

def plot_map(gridmap):
    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size, cmap="carmen_cmap_white")
    mpl.draw()

class FullPathDrawer(CheckboxDrawer):
    def FullPathDrawer(self, wnd):
        self.wnd = wnd
    
    def doDraw(self, axes):

        plots = []
        
        for agent in self.wnd.situation.agents:
            X = []
            Y = []
            for t, (x, y, theta) in agent.data:
                X.append(x)
                Y.append(y)
            plots.extend(mpl.plot(X, Y))
            #self.wnd.mpl_draw()
        return plots

class MainWindow(QMainWindow, recorder_ui.Ui_MainWindow):
    def __init__(self, tagFile, skeleton):
        QMainWindow.__init__(self)
        self.setupUi(self)    
        self.initializeMatplotlib()
        self.setWindowTitle("Recorder")

        self.tagFile = tagFile
        self.skeleton = skeleton

        self.oldLimits = None
        self.inDraw = False
        #self.drawMap()
        #self.landmark_plots = plotLandmarks(self.figure, self.tagFile, useText=False)
        fname = "%s/data/directions/direction_floor_3/direction_floor_3_image.png" % TKLIB_HOME
        fname = "%s/data/directions/stata3_aaai/stata3_aaai.png" % TKLIB_HOME
        bg = mpl.imread(fname)

        gridMap = self.tagFile.map
        mpl.imshow(na.flipud(na.asarray(bg)), origin=1, extent=[0, gridMap.x_size, 0, gridMap.y_size])
        
        themap = gridMap.to_probability_map_carmen()
        
        carmen_maptools.plot_map(themap, gridMap.x_size, gridMap.y_size, cmap="carmen_cmap_white",
                                 curraxis=self.axes)
        mpl.draw()
                
        #return na.flipud(na.asarray(img))
        #mpl.imshow(bg)
        
        self.isRecording = False

        self.fname = ""

        classifiers = trainer_pacman.versionOne().values()
        #classifiers = [Classifier(meet.Engine(), None),
        #               Classifier(follow.Engine(), None)
        #               ]
        self.engineWindow = engine.MainWindow(classifiers)
        self.engineWindow.show()

        self.landmarkSelectorWindow = landmarkSelector.MainWindow(self.tagFile)
        #self.landmarkSelectorWindow.show()



        #self.axes.axis([60, 90, 30, 45])
        #self.axes.set_aspect(1./self.axes.get_data_ratio())
        assignmentEntry = assignmentData.VerbAssignmentEntry("avoid", "Avoid the kitchen.",
                                                            self.tagFile, self.skeleton) 
        self.agentModel = agentModel.Model(self.agentTable, 
                                           assignmentEntry,
                                           self.tagFile, self.skeleton)
        
        self.fullPathDrawer = FullPathDrawer(self, self.showFullPathBox)
        
        self.pathModel = pathModel.Model(self.pathTable)
        
        print "constructing timeline"
        self.timeline = timeline.Widget(self)
        
        print "adding timeline"
        self.timelineFrame.layout().addWidget(self.timeline)


        self.connect(self.agentTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectAgent)

        
        self.connect(self.playButton,
                     SIGNAL("clicked()"),
                     self.play)
        
        self.connect(self.clearButton,
                     SIGNAL("clicked()"),
                     self.clear)
        self.connect(self.stopButton,
                     SIGNAL("clicked()"),
                     self.stop)



        self.connect(self.recordButton,
                     SIGNAL("clicked()"),
                     self.record)

        self.connect(self.actionClassify,
                     SIGNAL("triggered()"),
                     self.classify)

        self.connect(self.timeline,
                     SIGNAL("eventClicked"),
                     self.movePlayhead)

        self.connect(self.newAgentButton,
                     SIGNAL("clicked()"),
                     self.newAgent)

        self.connect(self.removeAgentButton,
                     SIGNAL("clicked()"),
                     self.removeAgent)

        self.connect(self.actionNew,
                     SIGNAL("triggered()"),
                     self.new)
        self.connect(self.actionSave,
                     SIGNAL("triggered()"),
                     self.save)        

        self.connect(self.actionDisplayPrimitives,
                     SIGNAL("triggered()"),
                     self.displayPrimitives)        
        

        self.initializeCapturePolygon()
        self.initializeCapturePoint()
        self.capturers = [self.capturePolygon, self.capturePoint]

        self.featureDrawer = mpl_drawer.Drawer(self.figure)
        self.playTimer = QTimer(self)
        self.playTimer.setInterval(100)
        
        
        self.figure.canvas.mpl_connect('draw_event', self.updateAssignmentGeom)

        
        self.connect(self.playTimer,
                     SIGNAL("timeout()"),
                     self.draw)
        self.anim_plots = []

        self.background = None
        self.startTime = None
        self.new()

    def updateAssignmentGeom(self, event):
        newLimits = self.axes.axis()
        if newLimits != self.oldLimits:
            self.background = None
            QTimer.singleShot(0, self.draw)        

        if newLimits != self.assignmentEntry.axisLimits:
            self.assignmentEntry.setAxisLimits(self.axes.axis())


        
        self.oldLimits = newLimits        
        
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
        
    @property
    def classifier(self):
        return self.engineWindow.classifier
    
    @property
    def situation(self):
        return self.assignmentEntry.situation
        
    def classify(self):
        print "classifying"
        cls = self.classifier.classify(self.situation)
        print "classifier", self.classifier
        print "recorder cls", cls
        print "recorder has data", self.classifier.has_data
        
        self.featureDrawer.setDrawMap(self.classifier.drawMap)
        self.engineWindow.update()
        self.draw()

    def stop(self):
        self.playTimer.stop()
        self.releaseKeyboard()
        self.isRecording = False
        self.startTime = None

    def movePlayhead(self, time):
        self.playhead = time
        self.draw(self.playhead)

    def play(self):
        self.startTime = datetime.now()
        self.playTimer.start()
        
        
    def clear(self):
        for a in self.situation.agents:
            a.reset()
        self.agentModel.reset()
        self.draw()

    def record(self):
        self.startTime = datetime.now()
        self.isRecording = True

        self.grabKeyboard()
        self.playTimer.start()
        


        for e in self.agentModel.entries:
            if e.agent.location == None:
                continue
            print "recording", e.turtle
            e.turtle.startRecording()
            if hasattr(e.turtle, "keyPressed"):
                self.connect(self,
                             SIGNAL("keyPressed"),
                             e.turtle.keyPressed)

            if hasattr(e.turtle, "keyReleased"):
                self.connect(self,
                             SIGNAL("keyReleased"),
                             e.turtle.keyReleased)

    
    def recenter(self, location):
        x, y = location

        xstart, xend, ystart, yend = self.axes.axis()
        bbox = [(xstart, ystart), (xend, ystart), (xend, yend),
                (xstart, yend)]
        width = xend - xstart
        height = yend - ystart
        print 'axis', self.axes.axis()
        if not math2d.isInteriorPoint(bbox, (x, y)):
            print "invoking recentering"
            xstart = x - width/2
            xend = x + width/2
            ystart = y - height/2
            yend = y + height/2
            self.axes.axis([xstart, xend, ystart, yend])
            self.background = None
            return True
        else:
            return False

        
    def keyPressEvent(self, event):
        self.emit(SIGNAL("keyPressed"), event.key())

    def keyReleaseEvent(self, event):
        self.emit(SIGNAL("keyReleased"), event.key())

        
    def drawOnEvent(self, event):
        print "redrawing because", event
        self.draw()
        
    def cacheBackground(self):
        self.background = self.figure.canvas.copy_from_bbox(self.axes.bbox)
    
    def mpl_draw(self):
        self.background = None
        self.draw()
    def draw(self, offset=None):
        if self.inDraw:
            """
            mpl.draw() invokes the qt event loop, which could invoke draw again
            during recording or playback via the qtimer.  If that happens, we 
            want to ignore it.
            """
            return
        self.inDraw = True
        
        if offset == None:
            if self.startTime != None:
                offset = datetime.now()  - self.startTime
            else:
                offset = self.timeline.playhead
        
        print "offset", offset
        self.timeLabel.setText(str(offset))
        if isinstance(offset, timedelta):
            offset = (offset.days * 24 * 60 * 60*1000  + offset.seconds*1000 + 
                        offset.microseconds / 1000)
        
        if False:
            entry = self.agentModel.selectedData()
            if entry != None:
                location = entry.agent.location(offset)
                print 'location', location
                if location != None:
                    x, y, theta = location
                    print 'recentering'
                    self.recenter((x, y))
        
        try:

            for p in self.anim_plots:
                try:
                    p.remove()
                except NotImplementedError:
                    pass
            self.anim_plots = []
        
            if self.background == None:
                #import cProfile
                #cProfile.run('mpl.draw', 'draw.prof')
                mpl.draw()
                self.cacheBackground()


            self.figure.canvas.restore_region(self.background)






            self.timeline.setPlayhead(offset)


            for entry in self.agentModel.entries:
                t = entry.turtle

                if self.isRecording:
                    t.update(offset)
                location = entry.agent.location(offset)
                if location != None:
                    x, y, theta = location
                    assert x != None and y != None, (x, y, theta, offset)

                    if isinstance(t, turtle.StaticTurtle):
                        print "Drawing static"
                        X, Y = math2d.points_to_xy(entry.agent.geometryAsLine(offset))

                        plot, = self.axes.plot(X, Y, 'ro-', animated=True, 
                                               scalex=False, scaley=False)
                                                
                    else:
                        if isinstance(t, turtle.KeyboardTurtle):
                            facecolor="y"
                            if self.isRecording:
                                self.recenter((x, y))
                        else:
                            facecolor="k"   
                            
                        
                        plot = matplotlib.patches.Wedge((x, y), 0.3, 
                                                        theta + 45, theta - 45,
                                                        facecolor=facecolor,
                                                        animated=True)
                    self.anim_plots.append(plot)
                    self.axes.add_artist(plot)
                    self.axes.draw_artist(plot)

            if self.classifier != None and self.classifier.has_data:
                self.featureDrawer.actuallyDraw(self.engineWindow.feature, offset)
            #mpl.draw()
            self.figure.canvas.blit(self.axes.bbox)
        finally:
            self.inDraw = False
        
    def initializeMatplotlib(self):
        self.figure = mpl.figure()
        self.axes = mpl.gca()
        self.oldParent = self.figure.canvas.parent()
        self.figure.canvas.setParent(self)
        self.canvasFrame.layout().addWidget(self.figure.canvas)
        self.toolbar = NavigationToolbar2QT(self.figure.canvas, self)
        self.addToolBar(self.toolbar)

    def newAgent(self):
        name = names[len(self.situation.agents)]
        newAgent = agents.Agent(name, [])
        print "adding agent", name
        self.agentModel.situation.addAgent(newAgent)
        self.agentModel.reset()

    def removeAgent(self):
        self.situation.removeAgent(self.agentModel.selectedData())
        self.agentModel.reset()
        
        
    def new(self):
        self.recordAssignment(assignmentData.VerbAssignmentEntry("avoid", "Avoid the kitchen.",
                                                                 self.tagFile, self.skeleton))

    def save(self):
        fname = QFileDialog.getSaveFileName(self, "Save File", self.fname)
        if fname != "":
            self.fname = fname
            self.assignmentEntry.save(fname)

    def selectAgent(self):
        self.pathModel.loadData(self.agentModel.selectedData().agent)
            
    def drawMap(self):
        gridmap = self.tagFile.map 
        carmen_maptools.plot_map(self.tagFile.carmen_map, 
                                 gridmap.x_size, gridmap.y_size, 
                                 cmap="carmen_cmap_white",
                                 curraxis=self.axes)
    def drawSkeleton(self):
        graph, I = self.skeleton.get_graph()
        X, Y = self.skeleton.i_to_xy(graph.keys())
        mpl.scatter(X, Y)
        
        
        X, Y = self.skeleton.get_junction_points()
        mpl.scatter(X, Y, marker="o", s=60, color="r")

    def recordAssignment(self, assignmentEntry):
        self.assignmentEntry = assignmentEntry
        self.commandLabel.setText(assignmentEntry.command)
        self.timeline.setSituation(self.situation)
        self.agentModel.setAssignmentEntry(assignmentEntry)
        self.agentTable.selectRow(0)
        
        self.axes.axis(assignmentEntry.axisLimits)
        self.timeline.setPlayhead(0)
        self.background = None
        
        try:
            self.engineWindow.selectByName(assignmentEntry.verb)
        except:
            print "warning, couldn't select engine for", assignmentEntry.verb
            pass
        
        QTimer.singleShot(0, self.draw)
        
    
        

    def captureAgentGeom(self):
        for c in self.capturers:
            c.deactivate()
        print "activating polygon"
        self.capturePolygon.activate(self.figure)

    def captureAgentLocation(self):
        for c in self.capturers:
            c.deactivate()
        self.capturePoint.activate(self.figure)


    def completedPolygon(self, polygon):
        print "completed polygon", polygon

        entry = self.agentModel.selectedData()
        if entry != None:
            entry.agent.setGeometry(polygon)
            theta = 0
            entry.setLocation(math2d.centroid(polygon) + (theta,))
            self.draw()
        self.capturePolygon.deactivate()
            
    def completedPoint(self, point):
        print "got", point
        point1, point2 = point
        entry = self.agentModel.selectedData()
        if entry != None:
            theta = math.degrees(math2d.direction(point1, point2))
            entry.setLocation(point1 + (theta,))
            self.draw()
        self.capturePoint.deactivate()
        
    def displayPrimitives(self):
        
        primitives = [IsMoving("figure"), 
                      IsMoving("landmark"),
                      IsVisible("figure", "landmark"),
                      IsClose("figure", "landmark"),
                      MovingTowards("figure", "landmark"),
                      MovingTowards("landmark", "figure"),
                      ]
        
        for p in primitives:    
            results = p.findEvents(self.situation)
            self.timeline.setEvents(`p`, results)


def loadTagFile(gtruth_tag_fn, map_fn):
    tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
    tagFile.get_map()
    tagFile.get_tag_names()
    return tagFile

def main():
    from sys import argv

    app = basewindow.makeApp()
    map_fn = argv[1]
    gtruth_tag_fn = argv[2]
    skeleton_fn = argv[3]
    
    tagFile = loadTagFile(argv[2], argv[1])
    skeleton = cPickle.load(open(skeleton_fn, 'r'))

    wnd = MainWindow(tagFile, skeleton)
    wnd.setWindowTitle("Spatial Motion Verbs Pacman")
    wnd.show()
    #wnd.open("data/motion_verbs/follow/follow1.pck")
    app.exec_()


if __name__ == "__main__":
    main()
