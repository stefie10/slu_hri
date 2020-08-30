from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math2d
import matplotlib
import numpy as na
from time import time

class MatplotlibDrawer:
    def __init__(self, figure):
        self.figure = figure
        self.axes = figure.gca()
    
    def drawText(self, p, text):
        x, y  = self.mtp(p)
        self.p.drawText(x, y, text)
    def drawDistance(self, p1, p2, p1Desc, p2Desc):
        plots = []
        plots.extend(self.drawPoint(p1))
        plots.extend(self.drawPoint(p2))
        plots.extend(self.drawSegment(p1, p2))
        
        plots.append(self.axes.text(p1[0], p1[1], p1Desc))
        plots.append(self.axes.text(p2[0], p2[1], p2Desc))

        return plots
    def drawPoint(self, pMap, label="", color="00FFFF", radius=3):
        plots = []
        w = matplotlib.patches.Wedge(pMap, radius, 
                                     0, 360,
                                     facecolor=color,
                                     animated=True)
        self.axes.add_artist(w)
        plots.append(w)
        
        
        plots.append(self.axes.text(pMap[0], pMap[1], label))
        return plots

        
    def drawPointForReal(self, x, y, color):
        oldPen = self.p.pen()
        self.p.setPen(color)
        self.p.drawPoint(x,y)
        self.p.setPen(oldPen)

    def drawLine(self, line):
        plots = []
        for p1, p2 in zip(line, line[1:]):
            plots.extend(self.drawSegment(p1, p2))
        return plots
        
    def drawSegment(self, p1Map, p2Map):
        plots = []
        line = [p1Map, p2Map]
        X, Y = na.transpose(line)
        plots.extend(self.axes.plot(X, Y))
        return plots

    def drawAxes(self, axes):
        self.pushPen(Qt.green)
        major, minor = axes
        self.drawSegment(major[0], major[1])
        self.drawSegment(minor[0], minor[1])
        self.popPen()

    def drawArrow(self, line, narrowness=4, length=5):
        self.drawLine(line)

        p1 = self.mtp(line[0])
        p2 = self.mtp(line[-1])
        pixSeg = [p1, p2]

        startP = math2d.pointOnSegment(pixSeg, math2d.dist(p1, p2) - length)
        segment = math2d.perpendicular(pixSeg, startP)
        sa1 = [startP, segment[0]]
        sa2 = [startP, segment[-1]]
        
        a1 = math2d.pointOnSegment(sa1, narrowness)
        a2 = math2d.pointOnSegment(sa2, narrowness)
        a3 = p2

        self.p.drawLine(a1[0], a1[1], a3[0], a3[1])
        self.p.drawLine(a2[0], a2[1], a3[0], a3[1])
        
    def drawRect(self, pLowerLeft, pUpperRight, color=Qt.green):
        x1, y1 = self.mtp(pLowerLeft)
        x2, y2 = self.mtp(pUpperRight)
        self.pushPen(color)
        self.p.drawRect(x1, y1, (x2 - x1), (y2 - y1))
        self.popPen()

    def fillRect(self, pLowerLeft, pUpperRight, color):
        x1, y1 = self.mtp(pLowerLeft)
        x2, y2 = self.mtp(pUpperRight)
        self.p.fillRect(x1, y1, (x2 - x1), (y2 - y1), color)
        self.pushPen(color)
        self.p.drawRect(x1, y1, x2 - x1, y2 - y1)
        self.popPen()



def makeDrawMethod(name):
    def drawMethod(self, key, *args):
        assert isinstance(key, str)
        self.drawMap.setdefault(key, [])
        self.drawMap[key].append({"name":name, "args":args})
    return drawMethod


class Drawer:
    def __init__(self):
        self.drawMap = {}

    def distanceFeature(self, valueMap, key, p1Desc, p2Desc, start, end, scale):
        valueMap[key] = math2d.dist(start, end) / float(scale)
        self.drawDistance(key, start, end, p1Desc, p2Desc)

        
    for k, v in MatplotlibDrawer.__dict__.iteritems():
        if k.startswith("draw"):
            exec("%s = makeDrawMethod(\'%s\')" % (k, k))

class EmptyDrawer:
    def __init__(self):
        self.drawMap = {}
    def noop(self, *args, **margs):
        pass
    def distanceFeature(self, valueMap, key, p1Desc, p2Desc, start, end, scale):
        valueMap[key] = math2d.dist(start, end) / float(scale)
        self.drawDistance(key, start, end, p1Desc, p2Desc)
    
    
    def __getattr__(self, name):
        return self.noop

class FeatureGroup:
    def __init__(self, names):
        assert isinstance(names, dict), names
        self._names = names
        self.lastValues = None
    def names(self):
        return self._names.keys()
    def description(self, name):
        return self._names[name]
    """
    Returns a map of features with values.  Keys are in names. 
    """
    def compute(self, **args):
        drawer = EmptyDrawer()
        try:
            map = self.doCompute(drawer, **args)
        except Exception, e:
            e.args = (self, e.args)
            raise
        if map != None:
            # if you bailed, don't require that you drew everything. 
            #for name in self.names():
                #assert map.has_key(name), (map, name, self)
                #assert drawer.drawMap.has_key(name), (drawer.drawMap, name, "Did you draw this feature?", self)
            pass
        else:
            map = {}
            for x in self.names():
                map[x] = -1
        drawer.lastValues = map
        self.lastValues = map
        return self.lastValues, drawer

    """
    The method that clients actually override. 
    """
    def doCompute(self, **args):
        pass



class FeatureCollection:
    def __init__(self, groups):
        self._groups = groups
        self._map = {}
        for group in self._groups:
            for x in group.names():
                self._map[x] = group

    @property
    def groups(self):
        return self._groups

    def compute(self, **args):
        result, drawMap = self.computeAndVisualize(**args)
        return result

    def computeAndVisualize(self, **args):
        result = {}
        drawMap = {}
        for feature in self._groups:
            vMap, drawer = feature.compute(**args)
            result.update(vMap)
            drawMap.update(drawer.drawMap)
        return result, drawMap

    def computeWithTime(self, **args):
        result, result_times = self.computeAndVisualizeWithTime(**args)
        return result, result_times

    def computeAndVisualizeWithTime(self, **args):
        result_names = []
        result_vals = []
        result_times = []
        for feature in self._groups:
            t1 = time()
            vMap, drawer = feature.compute(**args)
            result_names.extend(vMap.keys())
            result_vals.extend(vMap.values())
            t2 = time()
            num_elts = len(vMap.keys())*1.0
            result_times.extend(list(na.zeros(len(vMap.keys()))+((t2-t1)/num_elts)))

        return zip(result_names, result_vals), result_times

    def names(self):
        for feature in self._groups:
            for name in feature.names():
                yield name


    def description(self, name):
        return self._map[name].description(name)
    def visualize(self, name):
        try:
            group = self._map[name]
            return group.visualize(name)
        except KeyError:
            print "self", self
            raise
                          
        
