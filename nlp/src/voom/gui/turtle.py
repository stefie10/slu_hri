from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math
import math2d
import random


class Turtle:
    name = "base class"
    def __init__(self, tagFile, skeleton):
        self.location = None
        self.agent = None
        self.tagFile = tagFile
        self.skeleton = skeleton
        self.lastTimestamp = 0  

    def setLocation(self, location):
        if location != None:
            x, y, theta = location
            self.location = location
        else:
            location = None
    

    def setAgent(self, agent):
        self.agent = agent
        self.setLocation(self.agent.location(self.agent.endTime))

    def update(self, timestamp):
        dt = (timestamp - self.lastTimestamp) / 1000.0
        x, y, theta = self.doUpdate(timestamp, dt)
        self.location  = x, y, theta
        if self.agent != None:
            self.agent.addObservation(timestamp, (x, y, theta))
            
        self.lastTimestamp = timestamp              

    def doUpdate(self, timestamp, dt):
        raise NotImplementedError(self)

    def startRecording(self):
        pass

    
        

class FreeTurtle(Turtle):
    """
    A turtle that can turn and move anywhere where there isn't an
    obstacle.  It is controlled with a set of active commands, and
    updates according to those commands.  It can be driven randomly or
    with a keyboard (in subclasses.)
    """

    COMMANDS=set(["Forward", "Left", "Right"])

    def __init__(self, tagFile, skeleton):
        Turtle.__init__(self, tagFile, skeleton)
        self.speed = 1.3 # average walking speed
        
        self.clear()


    def clear(self):
        self.cmdSet = set()

    def addCmd(self, cmd):
        assert cmd in self.COMMANDS
        self.cmdSet.add(cmd)

    def removeCmd(self, cmd):
        assert cmd in self.COMMANDS
        if cmd in self.cmdSet:
            self.cmdSet.remove(cmd)
        
    def doUpdate(self, timestamp, dt):
        try:
            x, y, theta = self.location
        except ValueError:
            print "location", self.location
            raise

        if "Left" in self.cmdSet:
            theta += 20
        if "Right" in self.cmdSet:
            theta -= 20
        if "Forward" in self.cmdSet:
            dx = math.cos(math.radians(theta)) * self.speed * dt
            dy = math.sin(math.radians(theta)) * self.speed * dt
            newx = x + dx
            newy = y + dy


            occupied = self.tagFile.map.location_occupied((newx, newy))
            #loc_st_spl, loc_st_i = self.skeleton.nearest_spline_location((x, y))
            if not occupied:
                x = newx
                y = newy

        self.lastTimestamp = timestamp

        return x, y, theta

    def startRecording(self):
        if self.agent != None:
            print "clearing", self
            self.agent.clear()
            print "location", self.location
            x, y, theta = self.location
            self.agent.addObservation(0, (x, y, theta))

class KeyboardTurtle(FreeTurtle):
    name = "keyboard"
    def __init__(self, tagFile, skeleton):
        FreeTurtle.__init__(self, tagFile, skeleton)

        self.keyToCmd = {Qt.Key_Up:"Forward",
                         Qt.Key_Left:"Left",
                         Qt.Key_Right:"Right"}
        
    def keyPressed(self, key):
        if key in self.keyToCmd:
            self.addCmd(self.keyToCmd[key])
        
    def keyReleased(self, key):
        if key in self.keyToCmd:
            self.removeCmd(self.keyToCmd[key])

class RandomTurtle(FreeTurtle):
    name = "random"

    def doUpdate(self, timestep, dt):
        self.clear()
        self.addCmd("Forward")
        turn = random.choice([None, "Left", "Right"])
        if turn != None:
            self.addCmd(turn)
        return FreeTurtle.doUpdate(self, timestep, dt)


class TargetTurtle(Turtle):
    """
    At each timestep, moves at the specified speed towards a target.
    """
    
    def __init__(self, tagFile, skeleton):
        Turtle.__init__(self, tagFile, skeleton)
        self.speed = 1.3
        
    def doUpdate(self, timestamp, dt):
        target = self.updateTarget(timestamp)
        
        if target == None:
            return self.location
        else:

            x, y, theta = self.location
        
            line = [(x, y), target]
        
            print "point on line", line, dt*self.speed, target
            
            distAlongLine =  dt * self.speed
            
            if distAlongLine > math2d.length(line):
                newx, newy = target
            else:
                newx, newy = math2d.pointOnLine(line, dt * self.speed)

            return newx, newy, math.degrees(math2d.direction((newx, newy), target))
                                        
    
class FollowTurtle(TargetTurtle):
    """
    Follows anyone that gets close to it. 
    """
    
    name = "follow"
    
    def updateTarget(self, timestamp):
        situation = self.agent.situation

        minDist = None
        minAgent = None
        hereX, hereY, hereTheta = self.agent.location(timestamp)
        for a in situation.agents:
            
            aX, aY, aTheta = a.location(timestamp)
            dist = math2d.dist((aX, aY),
                               (hereX, hereY))
            if (minDist == None or dist < minDist) and a != self.agent:
                minDist = dist
                minAgent = a

        print "agent", minDist, minAgent
        if minDist != None and minDist < 4:
            if minDist < 1:
                return None
            else:
                x, y, theta = minAgent.location(timestamp) 
                return x, y
        else:
            return None
        
        
        

class SplineTurtle(Turtle):
    name = "spline"
    def __init__(self, tagFile, skeleton):
        Turtle.__init__(self, tagFile, skeleton)
        self.speed = 1.3 # average walking speed
        self.iLastLocs = []
        self.graph, I = self.skeleton.get_graph()

    def doUpdate(self, timestamp, dt):
        x, y, theta = self.location
        loc_st_spl, loc_st_i = self.skeleton.nearest_spline_location((x, y))

        placesToGo = set(self.graph[loc_st_i].keys())

        for loc in self.iLastLocs:
            if loc in placesToGo:
                placesToGo.remove(loc)

        if len(placesToGo) == 0:
            nextPlace = loc_st_i
        else:
            nextPlace = random.choice(list(placesToGo))

        X,Y = self.skeleton.i_to_xy([nextPlace])
        newXY =  X[0], Y[0]


        X,Y = self.skeleton.i_to_xy([nextPlace])
        lastXY = X[0], Y[0]
        


        theta = math2d.angleBetweenLines([(0, 0), (1, 0)], 
                                         [lastXY, newXY])
        while len(self.iLastLocs) > 2:
            del self.iLastLocs[0]
        self.iLastLocs.append(loc_st_i)


        

        return newXY + (math.degrees(theta),)

        
class PlaybackTurtle(Turtle):
    name = "playback"
    def __init__(self, tagFile, skeleton):
        Turtle.__init__(self, tagFile, skeleton)
        
    def update(self, timestamp):
        self.location = self.agent.location(timestamp)
        return self.location
        

class StaticTurtle(FreeTurtle):
    """
    A turtle that never moves."
    """
    name = "static"
    def doUpdate(self, timestamp, dt):
        self.clear()
        return FreeTurtle.doUpdate(self, timestamp, dt)
    

