
from voom import verb_classifier
from voom.agents import Agent
from voom.event_logic.features import AverageOfPrimitives
from voom.features import FeatureGroup, InsaneExample
from voom.verb_classifier import Signature
import math
import math2d
import scipy

class MovingTowards(FeatureGroup):
    def __init__(self):
        FeatureGroup.__init__(self, {"averageDifferenceInAngle":"Difference in movement direction from movement towards landmark"})
        
    def doCompute(self, drawer, situation):
        
        figure = situation.agent("figure")
        landmark = situation.agent("landmark")
        
        sum = 0.0
        count = 0
        for t in range(situation.startTime, situation.endTime, 100):
            x1, y1, t1 = figure.location(t)
            x2, y2, t2 = landmark.location(t)

            dx1, dy1, dt1 = figure.derivative(t)
        
            directionOfMovement = math2d.angle((dx1, dy1))
        
            directionOfLandmark = math2d.direction((x1, y1), (x2, y2))
        
            sum += math2d.normalizeAngleMinusPiToPi(math.fabs(directionOfLandmark - directionOfMovement))
            count += 1
            
        if count == 0:
            return {"averageDifferenceInAngle":math.pi}
        else:
            return {"averageDifferenceInAngle":sum/count}


class Visibility(FeatureGroup):
    def __init__(self):
        FeatureGroup.__init__(self, {"averageVisibility":"Proportion of time figure is visible from ground."})
    
    def doCompute(self, drawer, situation):
        figure = situation.agent("figure")
        landmark = situation.agent("landmark")

        visCount = 0.0
        total = 0.0
        for t in range(situation.startTime, situation.endTime, 100):
            fx, fy, ftheta = figure.location(t)
            lx, ly, ltheta = landmark.location(t)
            
            if situation.isVisible((fx, fy), (lx, ly)):
                visCount +=1
                drawer.drawDistance("averageVisibility", t, (fx, fy), (lx, ly))
            else:
                drawer.drawPoint("averageVisibility", (fx, fy), "")
                drawer.drawPoint("averageVisibility", (lx, ly), "")
            total += 1
        if total == 0:
            raise InsaneExample("Expected non-null figure")
        return {"averageVisibility":visCount/total}
            
            


class AverageDistance(FeatureGroup):
    def __init__(self):
        FeatureGroup.__init__(self, {"averageDistance":"The average distance between the figure and landmark.",
                                     "stdDevOfDistance":"The variance of the distance.",
                                     #"averageDistanceAtEnd":"Average distance in last 10%",
                                     #"averageDistanceAtStart":"Average distance in fist 10%",
                                     })
        

    def doCompute(self, drawer, situation):
        distances = []
        
        figure = situation.agent("figure")
        landmark = situation.agent("landmark")
        points = [(x, y) for x, y, theta in figure.positions + landmark.positions]
        (minX, minY), (scaleX, scaleY)  = math2d.boundingBox(points)
        
        scale = math.pow(scaleX**2 + scaleY**2, 0.5)
        
        for t in range(situation.startTime, situation.endTime, 100):
            fx, fy, ftheta = figure.location(t)
            lx, ly, ltheta = landmark.location(t)
            floc = fx, fy
            lloc = lx, ly
            distances.append(math2d.dist(floc, lloc))
            drawer.drawDistance("averageDistance", t, floc, lloc)
            drawer.drawDistance("stdDevOfDistance", t, floc, lloc)
            
        if len(distances) == 0:
            raise InsaneExample("Bad figure: " + `figure`)
        if scale == 0:
            scale = 0.000001
        return {"averageDistance":scipy.mean(distances) / scale,
                "stdDevOfDistance":scipy.std(distances) / scale
                }
        
            
            
                                     


class Engine(verb_classifier.Engine):
    def __init__(self):
        verb_classifier.Engine.__init__(self, "follow", Signature(figure=Agent,
                                                  landmark=Agent),
                                        [#AverageDistance(), 
                                         #Visibility(),
                                         #Approach(),
                                         AverageOfPrimitives(),
                                         #MovingTowards(),
                                         ],
                                         isLiquid=True)

        
                        
