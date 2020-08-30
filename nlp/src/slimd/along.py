import numpy as na
import math2d
import math
import features
import coaxial_distance_features
import preposition
import orange, orngTree
import orangeUtils
import across
import argTypes


def findSubsetOfFigure(landmark, figure):
    bestScore = None
    bestPath = figure
    d_f = math2d.length(figure)/100
    for subpath in math2d.slideWindowAlongPath(figure, 
                                               d_f,
                                               fractionSize=0.6):
        totalDist = 0.0
        count = 0
        for f1 in [x for x in math2d.stepAlongLine(figure, d_f)]:
            g1 = math2d.closestPointOnLine(math2d.polygonToLine(landmark), f1)
            totalDist += math2d.dist(f1, g1)
            count += 1
        mean = totalDist / count
        if bestScore == None or mean <= bestScore:
            bestScore = mean
            bestPath = subpath
    clippedFigure = bestPath

class LinearizingFeatures(features.FeatureGroup):
    """
    Measures how well the figure can be represented as a line, and
    whether the two lines are parallel.
    """
    def __init__(self):
        features.FeatureGroup.__init__(self,
                                       {"angleBtwnLinearizedObjects":
                                        "The angular difference of the slope of a line fit to the figure and the landmark.",
                                        "stdErrOfRegression":"The standard error of a line fit to the points in the figure."
                                        #"averageParallel":"",
                                        })

    def doCompute(self, drawer, landmark, figure, **args):

        fminX = min([p[0] for p in figure])
        fmaxX = max([p[0] for p in figure])

        fM, fB = math2d.fitLine(figure)

        gM, gB = math2d.fitLine(landmark)

        slope, intercept, r_value, p_value, std_err = math2d.regression(figure)


        m = {}
        bborigin, (width, height) = math2d.boundingBox(figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        #scale = 960
        m["stdErrOfRegression"] = std_err / scale
        # different: 0.59
        # same coordiante system: 0.45

        
        # only angle, identicle? 0.31, 0.21

        
        if na.isnan(fM):
            fpoint = (0, 1)
        else:
            fpoint = (1, fM)
        if na.isnan(gM):
            gpoint = (0, 1)
        else:
            gpoint = (1, gM)
        m['angleBtwnLinearizedObjects'] = math2d.angleBetweenLines([(0, 0), fpoint],
                                                                   [(0, 0), gpoint])            
        
            
        drawer.drawLine("angleBtwnLinearizedObjects", [(fminX, fminX*fM + fB),
                                                        (fmaxX, fmaxX*fM + fB)])
        drawer.drawLine("stdErrOfRegression", [(fminX, fminX*fM + fB),
                                              (fmaxX, fmaxX*fM + fB)])

        #m['averageParallel'] = self.averageParallel(landmark, figure)

        return m

    def averageParallel(self, drawer, landmark, figure):
        total = 0.0
        count = 0.0
        d_f = math2d.length(figure)/100
        steps = list(math2d.stepAlongLine(figure, d_f))
        for f1, f2 in zip(steps, steps[1:]):
            g1 = math2d.closestPointOnLine(math2d.polygonToLine(landmark), f1)
            g2 = math2d.closestPointOnLine(math2d.polygonToLine(landmark), f2)
            drawer.drawLine('averageParallel', [f1,g1])
            try:
                angle = math2d.angleBetweenLines([f1, f2], [g1, g2])
            except math2d.VerticalSegmentError:
                continue
            total += angle
            count += 1
            
        if count == 0:
            return math.pi/4
        else:
            return total / count
                                                        

        
        

class EndPointFeatures(features.FeatureGroup):
    """
    These features capture properties of the beginning and end of the
    figure relative to the landmark object.
    """
    def __init__(self):
        features.FeatureGroup.__init__(self,
                                       {"distEndLandmarkBoundary":"The distance of the endpoint of the figure to the landmark.",
                                        "distStartLandmarkBoundary":"The distance of the start of the figure to the landmark.",
                                        "averageDistStartEndLandmarkBoundary":"The average of distEndLandmark and distStartLandmarkBoundary.",
                                        "figureStartToEnd":"The distance between the start of the figure and the end.",
#                                        "figureLength":"The length of the figure, relative to the size of the bounding box ."

})
    def doCompute(self, drawer, landmark, figure, **args):
        boundary = math2d.computeBoundaryLine(landmark, figure)
        map = {}
        bborigin, (width, height) = math2d.boundingBox(figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)

        if scale == 0:
            bborigin, (width, height) = math2d.boundingBox(landmark)
            scale = pow(pow(width, 2) + pow(height, 2), 0.5)

        drawer.distanceFeature(map,
                               "distStartLandmarkBoundary",
                               "Boundary",
                               "Figure Start",
                               math2d.closestPointOnLine(boundary, figure[0]),
                               figure[0], scale)
        drawer.distanceFeature(map,
                               "distEndLandmarkBoundary",
                               "Boundary",
                               "Figure End",
                               math2d.closestPointOnLine(boundary, figure[-1]),
                               figure[-1], scale)

        map['averageDistStartEndLandmarkBoundary'] = na.mean([map['distStartLandmarkBoundary'],
                                                              map['distEndLandmarkBoundary']])
        drawer.drawLine('averageDistStartEndLandmarkBoundary', figure[-1],
                      math2d.closestPointOnLine(boundary, figure[-1]))

        drawer.distanceFeature(map,
                               "figureStartToEnd",
                               "Start",
                               "End",
                               figure[0],
                               figure[-1],
                               scale)

        map['figureLength'] = math2d.length(figure) / scale
        drawer.drawPoint('figureLength', figure[0])
        drawer.drawPoint('figureLength', figure[-1])

        if math2d.length(figure) == 0:
            map['figureLengthByCrow'] = 0
        else:
            map['figureLengthByCrow'] = math2d.dist(figure[0], figure[-1]) / math2d.length(figure)
        return map
                                 

class Along(preposition.Preposition):
    """
    The axes for ``along'' is computed by taking a subset of the
    boundary of the landmark object.  The start of the axes is the point
    on the landmark closest to the start of the figure; the end of the
    axes is the point on the landmark closest to the end of the figure.
    The axes itself is the boundary of the landmark between these two
    points.
    """
    def __init__(self):
        preposition.Preposition.__init__(self, "along", 
                                         [("obstacles", argTypes.Polygon, "*"),
                                          ("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [coaxial_distance_features.CoaxialDistanceFeatures(math2d.computeBoundaryLine),
                                          EndPointFeatures(),
                                          LinearizingFeatures(),
                                          #past.AxesFeatures(),
                                          #visibilityFeatures.VisibilityFeatures()
                                          ],
                                         ["peakDistToAxes",
                                          "stdDevToAxes",
                                          "averageDistStartEndLandmarkBoundary",
                                          "angleBtwnLinearizedObjects"])
                                         
#                                          "stdErrOfRegression",
#                                          "standardDeviation",
#                                          "peakDistanceToAxes",
#                                          ])

    def makeLearner(self):
        #return orngEnsemble.RandomForestLearner()
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        treeLearner.stop = orange.TreeStopCriteria_common() 
        treeLearner.maxDepth=4
        return preposition.RejectInsaneExampleLearner(treeLearner)


        
class TargetDistance(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self, 
                                       {"centroidToTarget":"The distance between a target point and the centroid of the figure."})
    def doCompute(self, drawer, landmark, figure, **args):
        figureCom = math2d.centerOfMass(figure)
        landmarkCom = math2d.centerOfMass(landmark)
        bborigin, (width, height) = math2d.boundingBox(figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        #scale = 960
        map = {}
        self.distanceFeature(map,
                             "centroidToTarget",
                             "Figure Centroid",
                             "Landmark Centroid",
                             figureCom, landmarkCom, scale)
        return map
    
class RightSideOfIslandIntersectBoundingBox(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self,
                                       {'intersectBoundingBox':'Whether figure intersects a bounding box.  0 or 1'})
    def doCompute(self, drawer, landmark, figure, **args):
        (x0,y0), (width, height) = math2d.boundingBox(landmark)

        #point, dims = (x0 + width, y0), (width, height)
        #translatedBox = math2d.boxToPolygon(point, dims)
        translatedBox = math2d.boxToPolygon((x0,y0),(width, height))
        
        drawer.drawRect("intersectBoundingBox", 
                      translatedBox[0], translatedBox[2])
        if math2d.clip(figure, math2d.polygonToLine(translatedBox)) != []:
            return {"intersectBoundingBox":1}
        else:
            return {"intersectBoundingBox":0}
                                        

class AlongBaseline(preposition.Preposition):
    def __init__(self):
        preposition.Preposition.__init__(self, "alongBaselineLength", 
                                         [("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [across.LengthBaseline(),
                                          RightSideOfIslandIntersectBoundingBox(),
                                          TargetDistance()])

    def makeLearner(self):

        class IntersectClassifier(orangeUtils.PythonClassifier):
            def classify(self, ex):
                if ex['intersectBoundingBox'] == 1:
                    return "True"
                else:
                    return "False"
        def learner(*args):
            return IntersectClassifier()
        return learner
    
        #return ThresholdLearner("centroidToTarget", intersectBoundingBox)
                
