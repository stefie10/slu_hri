from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math2d

import matplotlib
import pylab as mpl

    
class Drawer:
    def __init__(self, figure):
        self.drawMap = None
        self.figure = figure

        self.plotted_objects = []
        
    @property
    def axes(self):
        return self.figure.gca()

    def pixels(self, dist):
        """
        Convert a distance in pixels to distance in the figure using
        the current data coordinates.
        """
        p1 = self.axes.transData.inverted().transform((0, 0))
        p2 = self.axes.transData.inverted().transform((0, dist))
        
        return math2d.dist(p1, p2)


    def setDrawMap(self, drawMap):
        self.drawMap = drawMap
        

    def drawPoint(self, pt, label):
        pt = matplotlib.patches.Circle(pt, radius=self.pixels(5),
                                  facecolor="green")
        x, y = pt
        mpl.text(x + self.pixels(5), y, label)
        
    def drawDistance(self, sloc, eloc):

        line = matplotlib.lines.Line2D([sloc[0], eloc[0]], [sloc[-1], eloc[-1]],
                                       marker=None)
        s_patch = matplotlib.patches.Circle(sloc, radius=self.pixels(5), 
                                            facecolor="green")
        e_patch = matplotlib.patches.Circle(eloc, radius=self.pixels(5), 
                                            facecolor="red")
        
        return [line, s_patch, e_patch]

    def actuallyDraw(self, feature, offset):
        for o in self.plotted_objects:
            o.remove()

        self.plotted_objects = []
        print "feature", feature
        if feature in self.drawMap:
            flog = self.drawMap[feature]

            flog.sort(key=lambda x: x['time'])


            for m in flog:
                if m['time'] >= offset:
                    method = eval("self.%s" % m['name'])
                    artists = method(*m['args'])
                    self.plotted_objects.extend(artists)
                    break

            for o in self.plotted_objects:
                print "o", o, o.__class__
                self.figure.gca().add_artist(o)
