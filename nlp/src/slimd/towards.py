from slimd import argTypes
import awayFrom
import features
import math2d
import orngTree
import preposition
import to

class TowardsAxesFeatures(features.FeatureGroup):
    """
    Here an axes is created by approximating the figure as a line.
    """
    def __init__(self):
        features.FeatureGroup.__init__(self, {
                #"axesToLandmarkCentroid":"The distance between the extended axes of the linearized figure and the centroid of the landmark.",
                #"axesOrientation":"The orientation of the axes with respect to the landmark.",
                "axesIntersectLandmark":"Whether the extended axes intersect the landmark.",
                                              })
    def doCompute(self, drawer, landmark, figure, **args):
        landmarkCentroid = math2d.centroid(landmark)
        d_f = math2d.length(figure)/100
        steps = list(math2d.stepAlongLine(figure, d_f))
        slope, intercept, r_value, p_value, std_err = math2d.regression(steps[25:])
        axes = math2d.lineEquationToPoints(slope, intercept)

        axes = [math2d.closestPointOnSegmentLine(axes, figure[0]),
                   math2d.closestPointOnSegmentLine(axes, figure[-1])]

        #axes = [steps[5], steps[-1]]

        point = math2d.closestPointOnSegmentLine(axes, landmarkCentroid)
        bborigin, (width, height) = math2d.boundingBox(figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        if scale == 0:
            bborigin, (width, height) = math2d.boundingBox(landmark)
            scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        m = {}
        drawer.distanceFeature(m,
                               "axesToLandmarkCentroid",
                               "Point on Figure Line",
                               "Landmark Centroid",
                               point, landmarkCentroid, scale)
        
        segmentStartToLandmark = [axes[0], landmarkCentroid]
        m["axesOrientation"] = math2d.angleBetweenSegments(segmentStartToLandmark, 
                                                           axes)
        drawer.drawLine("axesOrientation", segmentStartToLandmark)
        drawer.drawLine("axesOrientation", axes)
        drawer.drawPoint("axesOrientation", point, "Point on Figure Line")

        try:
            slope, intersept = math2d.lineEquation(axes)
        except:
            print "axes", axes
            raise
        intersectPoints = math2d.intersectPolygonAnalytic(landmark, 
                                                          slope, intersept)
        for p in intersectPoints:
            drawer.drawPoint("axesIntersectLandmark", p, "")
        if len(intersectPoints) == 0:
            m["axesIntersectLandmark"] = 0
            drawer.drawPoint("axesIntersectLandmark", landmarkCentroid, 
                           "No intersect points.")
        else:
            m["axesIntersectLandmark"] = 1
        
        #intersectPoint = 
        #m["axesToLandmark"] = 
        return m

class Towards(preposition.Preposition):

    def __init__(self):
        preposition.Preposition.__init__(self, "towards", 
                                         [("obstacles", argTypes.Polygon, "*"),
                                          ("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [#along.LinearizingFeatures(),
                                             to.EndPointFeatures(),
                                             #to.DistToLandmarkFeatures(),
                                             #TowardsAxesFeatures(),
                                             awayFrom.DisplacementFeatures()
                                             ],
                                         ["distFigureEndToLandmark",
                                          "displacementFromLandmark",
                                          ]
                                          )
    

    def makeLearner(self):
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        return treeLearner
    
