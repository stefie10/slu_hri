from eventLogic.allenRelations import iMeets, meets
from eventLogic.expressions import AndR, Not, overlaps, Tense, cooccur
from eventLogic.interval import OP
from eventLogic.model import ModelEntry
from eventLogic.spanningInterval import SpanningInterval, Interval, CL, \
    SpanningIntervalSet
import eventLogic.expressions
import math
import math2d




class Primitive(eventLogic.expressions.Primitive):
    def __init__(self, *args):
        eventLogic.expressions.Primitive.__init__(self, *args)
        self.name = str(self)

    def findEvents(self, situation):
        featureValues = []
        times = []
        for t in range(situation.startTime, situation.endTime, 100):
            if self.compute(situation, t):
                featureValues.append(True)
            else:
                featureValues.append(False)
                
            times.append(t)
                
        windowSize = 5
        
        result = []
        for i, (r, t) in enumerate(zip(featureValues, times)):
            start = max(0, i - windowSize/2)
            end = min(len(featureValues) - 1, i + windowSize/2 + 1)
            window = featureValues[start:end]
            tcount = len([x for x in window if x])
            fcount = len([x for x in window if not x])
            if tcount > fcount:
                result.append(t)
            
        return result
    

    def findRanges(self, situation):
        result = []
        
        turnedOn = False
        start = None
        end = None
        
        for t in range(situation.startTime, situation.endTime, 100):
            if self.compute(situation, t):
                if not turnedOn:
                    start = t
                    turnedOn = True
            else:
                if turnedOn:
                    end = t
                    turnedOn = False
                    result.append((start, end))
                    start = None
                    end = None
                    
        if turnedOn:
            result.append((start, t))
        return result
    
    def findSpanningIntervals(self, situation):
        result = []
        for start, end in self.findRanges(situation):
            result.append(SpanningInterval(CL, Interval(CL, start, end, CL),
                                           Interval(CL, start, end, CL), OP))
        return SpanningIntervalSet(result)
    def modelEntries(self, situation):
        spanningIntervals = self.findSpanningIntervals(situation)
        entries = [ModelEntry(self, si) for si in spanningIntervals]
        return entries
        

class Inverted(Primitive):
    def __init__(self, primitive):
        self.primitive = primitive
        Primitive.__init__(self)

        
    def compute(self, situation, offset):
        return not self.primitive.compute(situation, offset)
    def __repr__(self):
        return "Inverted(%s)" % (repr(self.primitive))
    def __eq__(self, obj):
        return obj.__class__ == Inverted and obj.primitive == self.primitive


class IsVisible(Primitive):
    def __init__(self, a1, a2):
        Primitive.__init__(self, a1, a2)
        self.a1 = a1
        self.a2 = a2
        
    def compute(self, situation, offset):
        a1 = situation.agent(self.a1)
        a2 = situation.agent(self.a2)
        
                
        fx, fy, ftheta = a1.location(offset)
        lx, ly, ltheta = a2.location(offset)
        result = situation.isVisible((fx, fy), (lx, ly))
        return result
            
            
            
class IsMoving(Primitive):
    def __init__(self, a1):
        Primitive.__init__(self, a1)
        self.a1 = a1
        
    def compute(self, situation, offset):
        a1 = situation.agent(self.a1)
        
        dt = 100
        
        x1, y1, theta1 = a1.location(offset)
        x2, y2, theta2 = a1.location(offset + dt)
        
        
        if math2d.dist((x1, y1), (x2, y2)) != 0:
            return True
        else:
            return False
        
                            
class IsClose(Primitive):
    def __init__(self, a1, a2):
        Primitive.__init__(self, a1, a2)
        self.a1 = a1
        self.a2 = a2
        
    def compute(self, situation, offset):
        a1 = situation.agent(self.a1)
        a2 = situation.agent(self.a2)
        
        x1, y1, theta1 = a1.location(offset)
        x2, y2, theta2 = a2.location(offset)

        #if math2d.length(situation.shortestPath((x1, y1), (x2, y2))) < 10:
        if math2d.dist((x1, y1), (x2, y2)) < 5:
            return True
        else:
            return False
        
class IsContained(Primitive):
    def __init__(self, figure, landmark):
        Primitive.__init__(self, figure, landmark)
        self.figure = figure
        self.landmark = landmark
        
    def compute(self, situation, offset):
        a1 = situation.agent(self.figure)
        
        a2 = situation.agent(self.landmark)
        
        geom = a2.geometry(offset)
        
        if math2d.isInteriorPoint(a1.location(offset)):
            return True
        else:
            return False
        
class MovingTowards(Primitive):
    def __init__(self, figure, landmark):
        Primitive.__init__(self, figure, landmark)
        self.figure = figure
        self.landmark = landmark
        
    def compute(self, situation, offset):
        a1 = situation.agent(self.figure)
        x1, y1, t1 = a1.location(offset)
        
        a2 = situation.agent(self.landmark)
        x2, y2, t2 = a2.location(offset)
        
        dx1, dy1, dt1 = a1.derivative(offset)
        
        directionOfMovement = math2d.normalizeAngleMinusPiToPi(math2d.angle((dx1, dy1)))
        directionOfLandmark = math2d.normalizeAngleMinusPiToPi(math2d.direction((x1, y1), (x2, y2)))
        
        
        
        dtheta = directionOfLandmark - directionOfMovement
        dtheta = math.fabs(math2d.normalizeAngleMinusPiToPi(dtheta))
        if dtheta < math.pi/4 and (dx1 != 0 or dy1 != 0):
            return True
        else:
            return False
        
        

def approachWithoutInverted(figure, landmark):
    return cooccur(Not(overlaps(IsClose(figure, landmark))),
                   Tense([iMeets], IsClose(figure, landmark)))

def approach(figure, landmark):
    return AndR(Inverted(IsClose(figure, landmark)),
                [meets],
                IsClose(figure, landmark))

def following(figure, landmark):
    return cooccur(MovingTowards(figure, landmark),
                   IsClose(figure, landmark)
                   )
    return cooccur(IsClose(figure, landmark),
                   IsMoving(figure),
                   IsMoving(landmark),
                   IsVisible(figure, landmark),
                   MovingTowards(figure, landmark),
                   )
                   
