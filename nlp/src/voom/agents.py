from affineMatrix import AffineMatrix
from bisect import bisect
from math import radians
from math2d import interpolate
from pyTklib import tklib_normalize_theta
import cPickle
import glob
import math2d


import numpy as na


def read_directory(dirname):
    """
    read a directory of situations and return it 
    """
    return [load(fname) for fname in glob.glob("%s/*.pck" % dirname)]


def make_simple_situation():
    agents = [Agent("figure", [(0, (0, 0, 45)), (500, (1, 1, 45)), 
                               (1000, (2, 2))]),
              Agent("landmark", [(0, (1, 9, 0)), (500, (4, 7, 0)), (1000, (5, 6, 0))]),
              ]
    s = Situation(agents, [])
    return s

def empty_situation():
    return Situation([])

def save(situation, fname):
    outfile = open(fname, "w")
    cPickle.dump(situation, outfile, 2)
    outfile.close()

def load(fname):
#    import agents #@UnusedImport
    situation = cPickle.load(open(fname, "r"))
    situation.fname = fname
    return situation


class ControlledAgent:
    def __init__(self, tagFile, skeleton, agent, turtleClass):
        self.tagFile = tagFile
        self.skeleton = skeleton
        self.agent = agent

        self.setTurtle(turtleClass(self.tagFile, self.skeleton))

    def setTurtleClass(self, turtleClass):
        self.setTurtle(turtleClass(self.tagFile, self.skeleton))

    def setTurtle(self, turtle):
        self.turtle = turtle
        self.turtle.setAgent(self.agent)
        self.turtleClass = turtle.__class__
        
    def setLocation(self, loc):
        x, y, theta = loc
        self.agent.clear()
        self.agent.addObservation(0, loc)
        self.turtle.setLocation(loc)
    def asPrimitives(self):
        return {"turtleClass":str(self.turtleClass),
                "agentName":self.agent.name}
    
    @staticmethod
    def fromPrimitives(tagFile, skeleton, situation, p):
        import voom.gui.turtle #@UnusedImport
        return ControlledAgent(tagFile, skeleton, situation.agent(p["agentName"]), 
                                                                  eval(p["turtleClass"]))


class Situation:
    
    @staticmethod
    def copy(situation):
        return Situation([Agent.copy(a) for a in situation.agents],
                         situation.tagFile, situation.skeletonFile)
    def __init__(self, agents, tagFile, skeletonFile):
        self.tagFile = tagFile
        self.skeletonFile = skeletonFile
        self.agents = agents
        for a in self.agents:
            a.situation = self
            
        self.nameToAgent = dict([(a.name, a) for a in self.agents])
            
            
    def subset(self, start, end):
        newagents = [a.subset(start, end) for a in self.agents]
        return Situation(newagents, self.tagFile, self.skeletonFile)
            
    def isVisible(self, location1, location2):
        """
        Return whether location1 is visible from location2
        """
        return self.tagFile.is_visible(location1, location2, 20)
        
    def shortestPath(self, location1, location2):
        """
        Return the shortest path between location1 and location2, avoiding
        obstacles.
        """
        X, Y = self.skeletonFile.compute_path(location1, location2)
        return [(x, y) for x, y in zip(X, Y)]
        

    def agent(self, name):
        return self.nameToAgent[name] 

    def addAgent(self, agent):
        self.agents.append(agent)
        agent.situation = self
        self.nameToAgent = dict([(a.name, a) for a in self.agents])

    def removeAgent(self, agent):
        self.agents.remove(agent)

    @property
    def startTime(self):
        return min([a.startTime for a in self.agents])

    @property
    def endTime(self):
        return max([a.endTime for a in self.agents])

    @property
    def length(self):
        return max([time for time, agent in self.events])        

    @property
    def events(self):
        events = []
        for agent in self.agents:
            for time, position in agent.data:
                events.append((time, agent))
        return events
    
    
    def locations1(self, dt):
        #locs = [list(agent.locations1(dt,
        #                             startTime=self.startTime, 
        #                             endTime=self.endTime)) for agent in self.agents]
        locs = [list(agent.locations1(dt, startTime=0)) for agent in self.agents]
        
            
        for locList in zip(*locs):
            r = {}
            offset = None
            for a, (t, loc) in zip(self.agents, locList):
                r[a.name] = loc
                if offset == None:
                    offset = t
                else:
                    assert offset == t, (offset, t)
            yield offset, r
            
    def asPrimitives(self):
        return {"agents": [a.asPrimitives() for a in self.agents]}
    
    @staticmethod
    def fromPrimitives(p, tagFile, skeletonFile):
        return Situation([Agent.fromPrimitives(a) for a in p["agents"]],
                         tagFile, skeletonFile)
        
class Agent:
    
    @staticmethod
    def copy(agent):
        return Agent(agent.name, agent.data, geometry=agent.geometry(0))
    """
    A history of an agent's positions in the world. 
    """

    def __init__(self, name, positions, geometry=[(0, 0), (0.5, 0), (0.5, 0.5),
                                                  (0, 0.5)]):

        """
        Positions are a  list of tuples of (t, (x, y theta))
        [(t1, (x1, y1, theta1)), (t2, (x2, y2, theta2))]
        
        """
        self._geometry = tuple(geometry)
        self.data = [(time, position) for time, position in positions]
        self.data.sort(key=lambda x: x[0])
        self.name = name
        self.validate()
        self.isEditing = False
        
        self.updateData()
        
    def subset(self, startTime, endTime):
        newData = [(t, pose) for t, pose in self.data if startTime <= t <= endTime]
        
        if len(newData) == 0:
            newData = [(startTime, self.location(startTime))]
        
        return Agent(self.name, newData, self.geometry(0))
        
    def startEditing(self):
        self.isEditing = True
        
    def stopEditing(self):
        self.isEditing = False
        
        
    def asPrimitives(self):
        keys = ["_geometry", "data", "name"]
        return dict([(k, self.__dict__[k]) for k in keys])
    
    @staticmethod
    def fromPrimitives(p):
        return Agent(p["name"], p["data"], p["_geometry"])

    def setGeometry(self, polygon):
        self._geometry = polygon


    def geometryAsLine(self, offset):
        return math2d.polygonToLine(self.geometry(offset))
    
    def geometry(self, offset):
        loc = self.location(offset)
        if loc != None:
            x, y, theta = loc 
            cx, cy = math2d.centroid(self._geometry)
            trans = AffineMatrix()
            trans.translate(x - cx, y - cy)
            trans.rotate(theta)
        else:
            trans = AffineMatrix()
        return [trans.transformPt(p) for p in self._geometry]
            

        
    @property
    def startPose(self):
        if len(self.data) == 0:
            return None
        else:
            time, pose = self.data[0]
            return pose
        
    @property
    def endPose(self):
        if len(self.data) == 0:
            return None
        else:
            time, pose = self.data[-1]
            return pose        
        
    
    def distance_traveled(self):
        return math2d.length(self.positions)
    
    def asPath(self, interval=100, endTime=None):

        if(endTime == None):
            endTime = self.endTime
        
        path = []
        for t in range(self.startTime, endTime, interval):
            fx, fy, ftheta = self.location(t)
            path.append((fx, fy))
        return path

    def asPoses(self, interval=100, endTime=None):
        if(endTime == None):
            endTime = self.endTime
        
        path = []
        for t in range(self.startTime, endTime, interval):
            fx, fy, ftheta = self.location(t)
            path.append((fx, fy, ftheta))
        return path

    def asPosesRadians(self, interval=100, endTime=None):
        if(endTime == None):
            endTime = self.endTime
        path = []
        for t in range(self.startTime, endTime + 1, interval):
            fx, fy, ftheta = self.location(t)
            path.append((fx, fy, tklib_normalize_theta(radians(ftheta))))
        
        return path
    
    
    def derivative(self, offset, dt=500):
        here = self.location(offset)
        
        gx, gy, gt = self.location(offset + dt)
        
        sx, sy, st = self.location(offset - dt)

        return gx - sx, gy - sy, gt - st
    
    def locations1(self, dt=100, endTime=None, startTime=None):
        if startTime == None:
            offset=self.startTime
        else:
            offset=startTime
        
        for (time1, position1), (time2, position2) in zip(self.data, 
                                                          self.data[1:]):
            while time1 <= offset <= time2:
                yield offset, interpolate(time1, position1, time2, position2, offset)
                offset += dt
                
        if endTime != None:
            while offset < endTime:
                yield offset, self.data[-1][1]
                offset += dt
    
    def location(self, offset):
        try:
            return self._locationCache[offset]
        except KeyError:
            loc = self.doLocation(offset)
            self._locationCache[offset] = loc
            return loc
        
    def doLocation(self, offset):
        
        
        if len(self.data) == 0:
            return None
        


        
        idx = bisect(self.times, offset)
        if idx == 0:
            return self.data[0][1]
        elif idx == len(self.times):
            return self.data[-1][1]
        else:
            time1, position1 = self.data[idx - 1]
            time2, position2 = self.data[idx]
            return interpolate(time1, position1, time2, position2, offset)



    def addObservation(self, time, location):
        x, y, theta = location

        newEntry = (time, location)
        if self.endTime == time:
            self.data[-1] = newEntry
        else:
            self.data.append(newEntry)


        self.data.sort(key=lambda x: x[0])
        
        self.updateData()
                
        
        self.validate()
        
    

    def updateData(self):
        def startTime(self):
            if len(self.data) == 0:
                return None
            else:   
                time, position = self.data[0]
                return time
        self.startTime = startTime(self)
        def endTime(self):
            if len(self.data) == 0:
                return None
            else:
                time, position = self.data[-1]
                return time
        self.endTime = endTime(self)

        self.positions = [position for time, position in self.data]
        self.times = na.array([time for time, position in self.data])
        self._locationCache = {}
        



    
    
    def validate(self):

        for t, pos in self.data:
            x, y, theta = pos
            
        
        for i, ((time1, position1), (time2, position2)) in enumerate(zip(self.data,
                                                                         self.data[1:])):
            if time1 == time2:
                raise ValueError("Times shouldn't be equal." + `time1` + " " + `time2` + " pos1: " + `position1` + " pos2: " + `position2` + " idx: " + `i` + " data: " + `self.data`)
        
        
    def clear(self):
        """
        Completely empty out the data. 
        """
        self.data = []
        self.updateData()
        
    def reset(self):
        """
        Empty all but the initial point
        """
        self.data = self.data[0:1]


def situationForVerb(verb, tagFile, skeleton):
    from voom import verbs
    try:
        engine = verbs.verbMap[verb]
    except KeyError:
        print "engines: ", verbs.verbMap
        print ("No engine for verb: "  + verb + " map: " +
               `verbs.verbMap`)
        engine = verbs.verbMap['follow']
    agents = []
    for argname, argtype in engine.signature.iteritems():
        agents.append(Agent(argname, []))
    return Situation(agents, tagFile, skeleton)
