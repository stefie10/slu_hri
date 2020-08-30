from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math
from gsl_utilities import tklib_get_distance
import numpy as na
from preposition import InsaneExample
from scipy import optimize
from slimd import argTypes
import coaxial_distance_features
import features
import math2d
import orange
import orngTree
import preposition


#import pylab
#import plot2d

"""
Computes the axes based on where the figure enters and leaves the
landmark.

Raises value error if the figure doesn't enter the landmark.
"""

def computeAxes1(landmarkGeom, figureGeom):
    if math2d.length(figureGeom) == 0:
        raise InsaneExample("Degenertie figure.")
    landmarkAsLine = math2d.polygonToLine(landmarkGeom)
    l = math2d.length(landmarkAsLine)
    resolution = 100
    fLength = math2d.length(figureGeom)
    def score(xArr):
        axis = [math2d.pointOnLine(landmarkAsLine, xArr[0] % l),
                math2d.pointOnLine(landmarkAsLine, xArr[1] % l)]
        score = 0.0
        for p1, p2 in zip(math2d.stepAlongLine(figureGeom, fLength/resolution),
                          math2d.stepAlongLine(axis, math2d.length(axis)/resolution)):
            score += math2d.squaredist(p1, p2)

        return score
    #plot2d.plotLine(landmarkGeom, "r+-")
    #plot2d.plotLine(figureGeom, "r+-")
    guessMajor, guessMinor = computeAxes2(landmarkGeom, figureGeom)
    if guessMinor == None:
        return None, None
    

    guess = [math2d.distAlongLine(landmarkAsLine, 
                                  guessMinor[0]),
             math2d.distAlongLine(landmarkAsLine,
                                  guessMinor[1])]
    #xopt = optimize.fmin(score, guess)
    
    xopt, retval = optimize.anneal(score, guess)
    #pylab.show()
    #print "opt", xopt
    p1 = math2d.pointOnLine(landmarkAsLine, xopt[0] % l)
    p2 = math2d.pointOnLine(landmarkAsLine, xopt[1] % l)
    minor = [p1, p2]
    major = math2d.perpendicular(minor)
    return major, minor

    
#@memoize.memoize
def computeAxes2(landmarkGeom, figureGeom):
    if math2d.length(figureGeom) == 0:
            raise InsaneExample("Degenerate figure.")

    # three algorithms
    # 1.  connect endpoints and extend
    # 2.  fit line with regression
    # 3.  get a line with my fancy optimization (minimize area and distance)
    
    #intersectPoints = math2d.intersectLines(math2d.polygonToLine(landmarkGeom),
    #                                        figureGeom)

    #m, b = math2d.fitLine(figureGeom)
    #intersectPoints = math2d.intersectPolygonAnalytic(landmarkGeom, m, b)


    endPointSegment = [figureGeom[0], figureGeom[-1]]
    if not math2d.isVertical(endPointSegment) and not math2d.isDegenerate(endPointSegment):
        m, b = math2d.lineEquation(endPointSegment)
        intersectPoints = math2d.intersectPolygonAnalytic(landmarkGeom, m, b)
    else:
        gYs = [p[1] for p in landmarkGeom]
        mungedFigAxis = [(figureGeom[0][0], min(gYs) - 1), 
                         (figureGeom[0][0], max(gYs) + 1)]
        intersectPoints = math2d.intersectLines(math2d.polygonToLine(landmarkGeom),
                                                mungedFigAxis)

    #m, b = math2d.fitLine(figureGeom)
    #intersectPoints = math2d.intersectPolygonAnalytic(landmarkGeom, m, b)
    
    if len(intersectPoints) == 0:
        if math2d.isInteriorPoint(landmarkGeom, figureGeom[0]):
            
            minor = [math2d.closestPointOnPolygon(landmarkGeom, figureGeom[0]),
                     math2d.closestPointOnPolygon(landmarkGeom, figureGeom[-1])]
        else:
            return None, None
    elif (len(intersectPoints) == 1 or 
          (intersectPoints[0] == intersectPoints[1])):
        if math2d.isInteriorPoint(landmarkGeom, figureGeom[0]):
            minorStart = math2d.closestPointOnPolygon(landmarkGeom, figureGeom[0])
        else:
            minorStart =  intersectPoints[0]

        minorEnd = math2d.closestPointOnPolygon(landmarkGeom, figureGeom[-1])
        minor = [minorStart, minorEnd]
    else:
        # ignoring figure after first two intersect points
        minor = [intersectPoints[0], intersectPoints[1]]

        D = tklib_get_distance(na.transpose(intersectPoints), [0,0]);

        i_st = na.argmin(D);
        i_end = na.argmax(D);
        
        minor = [intersectPoints[i_st], intersectPoints[i_end]]


    try:
        major = math2d.perpendicular(minor)
        intersectPoint = math2d.intersectSegment(major, minor)
    except:
        print "minor", minor
        print "figure", figureGeom
        raise
    
    if intersectPoint == None:
        #    if math2d.sorta_eq(math2d.length(figureGeom), 0):
        # degenerate case - start and end at the same point. 
        # can happen for zero length tracks. 
        # But other tracks too - still happens when you test zero length.
        raise InsaneExample("No axes" + `[major, minor, intersectPoint]`)
    else:
        return major, minor


computeAxes = computeAxes2

def lineFunction(landmark, figure):
    major, minor = computeAxes(landmark, figure)
    return minor


class EigenAxes(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self, {"eigenAxesRatio":"The ratio between the eigenvectors of the covariance matrix of the landmark when represented as an occupancy grid.", 
                                              "angleEigenImposed":"The angle between the major eigen axis and the major axis the figure imposes on the landmark."})
    def doCompute(self, drawer, landmark, figure, **args):
        major, minor  = computeAxes(landmark, figure)

        if (major, minor) == (None, None):
            centroid = math2d.centroid(landmark)
            for x in self.names():
                drawer.drawText(x, centroid, "Couldn't find axes.")
            return None
        else:
            eMajor, eMinor = math2d.eigenAxes(landmark)
            drawer.drawAxes("eigenAxesRatio", (eMajor, eMinor))
            drawer.drawLine("eigenAxesRatio", eMajor)
            drawer.drawLine("eigenAxesRatio", eMinor)

            drawer.drawLine("angleEigenImposed", eMajor)
            drawer.drawLine("angleEigenImposed", major)


            ratio = math2d.length(eMinor) / math2d.length(eMajor)  
            ratio = max(ratio, 1.0/ratio)
            try:
                angleEigenImposed = math2d.angleBetweenLines(major, eMajor)
            except ZeroDivisionError:
                angleEigenImposed = -1

                
            return {"eigenAxesRatio":ratio,
                    "angleEigenImposed":angleEigenImposed}
class AxesFeatures(features.FeatureGroup):
    """ These features measure how well the axes imposed on the landmark
    object fit it.
    """
    def __init__(self):
        features.FeatureGroup.__init__(self, {"centroidToAxesOrigin":"The distance between the centroid of the landmark and the origin of the axes the figure imposes on the landmark.",
                                              "figureCenterOfMassToAxesOrigin":"The distance between the center of mass of points in the figure and the axes origin.",
                                              "figureCenterOfMassToLandmarkCentroid":"The distance between the center of mass of the figure and the centroid of the landmark.",
                                              "axesToLandmarkSum":"The distance between the start of the axes and the landmark object.  Intereseting when figure starts or ends inside.",
                                              "axesToFigureSum":"The total distance between axes start to figure start, plus axes end to figure end.",
                                              "figureLengthByCrow":"The ratio between the start and end points of the figure and the length.",
                                              "distAlongLandmarkBtwnAxes":"The distance along the landmark between the start and end of the minor axis.",
                                              "ratioFigureToAxes":"The ratio between the distance between the start and end points of the figure and the axes.",
                                              })
    def doCompute(self, drawer, landmark, figure, **args):
        major, minor = computeAxes(landmark, figure)

        if (major, minor) == (None, None):
            centroid = math2d.centroid(landmark)
            for x in self.names():
                drawer.drawText(x, centroid, "Couldn't find axes.")
            return None
        else:
            map = {}
            origin = math2d.intersectSegment(major, minor)

            centroid = math2d.centroid(landmark)
            bborigin, (width, height) = math2d.boundingBox(landmark + figure)
            scale = pow(pow(width, 2) + pow(height, 2), 0.5)
            drawer.distanceFeature(map, 
                                   "centroidToAxesOrigin", 
                                   "Centroid",
                                   "Axes Origin",
                                   centroid, origin, scale)
            drawer.drawAxes("centroidToAxesOrigin", (major, minor))


            sampledFig = [x for x in 
                          math2d.stepAlongLine(figure, 
                                               math2d.length(figure)/100)]
            figureCentroid = math2d.centerOfMass(sampledFig)
            drawer.distanceFeature(map, 
                                   "figureCenterOfMassToAxesOrigin", 
                                   "Figure Center of Mass",
                                   "Axes Origin",
                                   figureCentroid,
                                   origin,
                                   scale)
            drawer.drawAxes("figureCenterOfMassToAxesOrigin", (major, minor))



            drawer.distanceFeature(map, 
                                   "figureCenterOfMassToLandmarkCentroid", 
                                   "Figure Center of Mass",
                                   "Centroid",
                                   figureCentroid,
                                   centroid, 
                                   scale)
            
            drawer.distanceFeature(map,
                                   "axesStartToLandmark",
                                   "Landmark",
                                   "Start of minor axis",
                                   math2d.closestPointOnPolygon(landmark, minor[0]), 
                                   minor[0], scale)
            drawer.drawAxes("axesStartToLandmark", (major, minor))

            drawer.distanceFeature(map,
                                   "axesEndToLandmark",
                                   "Landmark",
                                   "End of minor axis",
                                   math2d.closestPointOnPolygon(landmark, minor[-1]), 
                                   minor[-1], scale)

            drawer.drawAxes("axesEndToLandmark", (major, minor))
            
            map['axesToLandmarkSum'] = map['axesEndToLandmark'] + map['axesStartToLandmark']
            drawer.drawAxes("axesToLandmarkSum", (major, minor))
            
            map['figureLengthByCrow'] = math2d.ratioLengthByCrow(figure)
            drawer.drawDistance("figureLengthByCrow", figure[0], figure[-1], "Start", "End")
            

            m1 = minor[0]
            f1 = figure[0]
            m2 = minor[-1]
            f2 = figure[-1]
            d1 = math2d.dist(m1, f1) + math2d.dist(m2, f2)
            d2 = math2d.dist(m1, f2) + math2d.dist(m2, f1)
            if (math.fabs(d1 - d2) > math2d.threshold and
                d1 > d2):
                f1 = figure[-1]
                f2 = figure[0]

            drawer.distanceFeature(map,
                                   "axesStartToFigureStart",
                                   "Axes Start",
                                   "Figure start",
                                   m1, f1, scale)

            
            drawer.distanceFeature(map,
                                   "axesEndToFigureEnd",
                                   "Axes End",
                                   "Figure End",
                                   m2, f2, scale)
            
            map['axesToFigureSum'] = map['axesEndToFigureEnd'] + map['axesStartToFigureStart']
            drawer.drawDistance('axesToFigureSum', m2, f2, 'Axes End', 'Figure End')
            # from Rao at Winston's group meeting 12-9-2008
            map['distAlongLandmarkBtwnAxes'] = \
                math2d.distBetweenPointsAlongPolygon(landmark, 
                                                     minor[0], minor[-1]) / math2d.perimeter(landmark)
            drawer.drawAxes("distAlongLandmarkBtwnAxes", (major, minor))
            drawer.drawPoint("distAlongLandmarkBtwnAxes", figure[0], "", Qt.green, 30)
            drawer.drawPoint("distAlongLandmarkBtwnAxes", figure[-1], "", Qt.red, 30)
            
            map['ratioFigureToAxes'] = \
                math2d.dist(figure[0], figure[-1]) / math2d.length(minor)
            drawer.drawAxes("ratioFigureToAxes", (major, minor))



            drawer.drawDistance("ratioFigureToAxes", figure[0], figure[-1], 
                              "Figure Start", "Figure End")
            drawer.drawDistance("ratioFigureToAxes", minor[0], minor[-1],
                              "Minor Start", "Minor End")


            map['ratioLengthFigureToAxes'] = \
                math2d.length(figure) / math2d.length(minor)
            drawer.drawAxes("ratioLengthFigureToAxes", (major, minor))



            return map


class LengthBaseline(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self, {"normalizedPathLength":"The normalzized length of the path."})
    def doCompute(self, drawer, landmark, figure, **args):
        bborigin, (width, height) = math2d.boundingBox(landmark + figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        map = {'normalizedPathLength':math2d.length(figure) / scale}
        drawer.drawPoint("normalizedPathLength", figure[0], "Figure Start")
        drawer.drawPoint("normalizedPathLength", figure[-1], "Figure End")
        return map


class Across(preposition.Preposition):
    """ An important underlying concept inherent in the meaning of
many spatial prepositions is the idea of coordinate axes.  ``Across''
has been defined as a spatial relation that takes a linear figure and
planar landmark, and requires the figure to be perpendicular to the
major axis of the landmark~\citep{talmy05,landau93}.  However this
definition does not specify how to find the major axis of the
landmark. In many contexts, there is no single set of axes: for example,
there are many paths across a square room. The system solves this
problem by finding the unique axes that the figure imposes on the
landmark, and then quantifying how well those axes match the landmark.
These axes are computed by finding the line that connects the first
and last point in the figure, and extending this line until it
intersects the landmark.  This computation is illustrated in
Figure~\\ref{fig:schematic}.  The origin of the axes is the midpoint
of this line segment, and the endpoints are the two points where the
axes intersect the landmark.  Once the axes are known, the system
computes features that capture how well the figure follows the axes,
and how well the axes fit the landmark.
"""
    def __init__(self):

        preposition.Preposition.__init__(self, "across", 
                                         [("landmark", argTypes.Polygon, 1),
                                          ("figure", argTypes.LineString, 1)],
                                         [AxesFeatures(), 
                                          coaxial_distance_features.CoaxialDistanceFeatures(lineFunction),
                                          ],
                                         #['ratioFigureToAxes', 'distAlongLandmarkBtwnAxes']
                                         ['distAlongLandmarkBtwnAxes', 'figureCenterOfMassToLandmarkCentroid', 'ratioFigureToAxes' ]
                                         )
        
    def makeExample(self, landmark, figure, expectInsane=True, **args):
        try:
            return preposition.Preposition.makeExample(self, landmark=landmark, 
                                                       figure=math2d.clip(figure, 
                                                                          landmark),
                                                       expectInsane=expectInsane)
        except Exception, e:
            e.classifierArgs = args
            raise
    def dataFiles(self):
        files = []
        for dir in ["testdata/across_examples", 
#                    "testdata/across_examples.r18460.trackRater/",
                    ]:
            for i, x in enumerate(preposition.readDirectory(dir)):
                files.append(x)
                if i > 10:
                    break
        return files
    
    def makeLearner(self):
        # for icmi
        #from orangeUtils import ThresholdProbabilityLearner
        #import orngBayes
        #learner = orngBayes.BayesLearner()
        #learner.adjustThreshold = True
        #return learner

        #return orngEnsemble.RandomForestLearner(data)
        #return orngTree.TreeLearner(data)
        #return treefss.TreeFSS(N=7)(data)
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        treeLearner.stop = orange.TreeStopCriteria_common() 
        #treeLearner.stop.minExamples = 1
        treeLearner.maxDepth=5
        #treeLearner.stop.maxMajority = 0.8
        #return treeLearner
        return preposition.RejectInsaneExampleLearner(treeLearner)
        #return orngFSS.FilteredLearner(orngTree.TreeLearner(),
        #                               filter=orngFSS.FilterBestNAtts(n=5),
        #                               )


        
