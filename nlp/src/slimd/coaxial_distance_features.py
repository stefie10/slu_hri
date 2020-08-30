import features
import math2d
import math
from preposition import InsaneExample
class CoaxialDistanceFeatures(features.FeatureGroup):
    """ These features measure how well the figure follows the axes.
    """
    def __init__(self, lineFunction):
        features.FeatureGroup.__init__(self, 
                                       {"averageDistToAxes":"The average distance between the figure and the axes." ,
                                        "peakDistToAxes":"The maximum distance between the figure and the axes it imposes, for the part of the figure that is inside the landmark.",
                                        "stdDevToAxes":"The standard deviation of the distance between the figure and the landmark.",
#                                        "whitenedAverageDistance":"The average distance with the mean subtracted."
                                        })
        self._lineFunction = lineFunction
    def doCompute(self, drawer, landmark, figure, **args):
        line = self._lineFunction(landmark, figure)
        for x in self.names():
            drawer.drawLine(x, line)
        if line == None:
            raise InsaneExample("Couldn't get line: %s %s" % (landmark,figure))
        else:
            steps = 100
            figure = math2d.trimLine(figure, line[0], line[-1])
            if len(figure) <= 1:
                print "degenerate figure", figure, landmark
                raise InsaneExample("Figure was too short: %s" % figure)
            d_f = math2d.length(figure) / float(steps)
            fpoints = [x for x in math2d.stepAlongLine(figure, d_f)]
            distances = [math2d.dist(f1, 
                                     math2d.closestPointOnLine(line, f1))
                         for f1 in fpoints]
            start, stop = math2d.smallestWindow(distances, 
                                                int(len(distances) * 0.75))


            distances = []
            maxDist = 0.0
            maxp1 = None
            maxp2 = None
            bborigin, (width, height) = math2d.boundingBox(figure)
            scaleFactor = pow(pow(width, 2) + pow(height, 2), 0.5)
            for f1 in fpoints[start:stop]:
                g1 = math2d.closestPointOnLine(line, f1)
                drawer.drawSegment("averageDistToAxes", f1, g1)
                drawer.drawSegment("stdDevToAxes", f1, g1)
                d = math2d.dist(f1, g1)
                distances.append(d / scaleFactor)
                if d > maxDist:
                    maxDist = d
                    maxp1 = f1
                    maxp2 = g1

            if len(distances) == 0:
                map = {}
                centroid = math2d.centroid(landmark)
                for x in self.names():
                    drawer.drawText(x, centroid, "Couldn't find axes.")
                    map[x] = -1
                return map

            mean = math2d.mean(distances)
            stdDev = math2d.stdDeviation(distances)

            whitenedMean = math2d.mean([x - mean for x in distances])
            drawer.drawSegment("peakDistToAxes", maxp1, maxp2)
            f1 = math2d.closestPointOnLine(figure, line[0])
            f2 = math2d.closestPointOnLine(figure, line[-1])

            distF1F2 = math2d.distBetweenPointsAlongLine(figure, f1, f2)
            if distF1F2 != 0:
                x = math.fabs(distF1F2 / math2d.length(line))
                relativeLength = min(x, 1.0/x)
                #relativeLength = 1.0/x
                #x = math2d.length(line) / math2d.length(figure) 
                #relativeLength = min(x, 1.0/x)
            else:
                relativeLength = -1

            drawer.drawPoint("relativeLength", f1)
            drawer.drawPoint("relativeLength", f2)
            drawer.drawLine("relativeLength", line)



            return {"averageDistToAxes":mean,
                    "whitenedAverageDist":whitenedMean,
                    "peakDistToAxes": maxDist / scaleFactor,
                    "stdDevToAxes":stdDev,
                    "relativeLength":relativeLength}


        
