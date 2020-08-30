import features

import math2d
import preposition
import to
import orngTree
import argTypes


class PastAxesFeatures(features.FeatureGroup):
    """

    \citet{talmy05} defines ``past'' as figure's path must be going
    perpendicular to a point $P$ ``at a proximal remove'' from the
    landmark.  The path of the figure must be perpendicular to a line
    going from the landmark to this point.  I define the axes for past
    as this line and the line formed by the figure.  $P$ is computed
    by finding the point on the landmark that is closest to the figure.
    """
    def __init__(self):
        features.FeatureGroup.__init__(self, {"angleFigureToPastAxes":"The angle between the linearized figure and the line perpendicular to the closest point on the landmark.",
                                              "pastAxesLength":"The length of the axes, normalized."
                                              })
    def doCompute(self, drawer, landmark, figure, **args):
        fPoints = list(math2d.stepAlongLine(figure, 
                                            math2d.length(figure)/100.0))
        gPoints = [math2d.closestPointOnPolygon(landmark, p) for p in fPoints]
        distances = math2d.squareDistances(fPoints, gPoints) 
        #[math2d.squaredist(f1, g1) for f1, g1 in zip(fPoints, gPoints)]


        i, dist = math2d.argMin(distances)

        fPoint = fPoints[i]
        gPoint = math2d.closestPointOnPolygon(landmark, fPoint)
        
        axes = [fPoint, gPoint]

        
        m = {}
        
        drawer.drawSegment("angleFigureToPastAxes", fPoint, gPoint)
        bborigin, (width, height) = math2d.boundingBox(figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        if scale == 0:
            bborigin, (width, height) = math2d.boundingBox(landmark)
            scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        if math2d.isDegenerate(axes):
            m['angleFigureToPastAxes'] = 0
        else:
            m['angleFigureToPastAxes'] = math2d.angleBetweenLines(axes,
                                                              [figure[0], figure[-1]])
        drawer.distanceFeature(m,
                               "pastAxesLength",
                               "Axes Start",
                               "Axes End",
                               axes[0], axes[1], scale)
        
                                                          
        return m
        
        

class Past(preposition.Preposition):
    """
    
    """
    def __init__(self):
        preposition.Preposition.__init__(self, "past", 
                                         [("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [#across.AxesFeatures(), 
#                                          along.LinearizingFeatures(),
                                          to.EndPointFeatures(),
                                          #along.EndPointFeatures(),
                                          #distanceFeatures.DistanceFeatures(),
                                          #coaxial_distance_features.CoaxialDistanceFeatures(along.computeBoundaryLine),
                                          PastAxesFeatures(),
                                          ],
                                         [#"distFigureEndToLandmarkCentroid",
                                          #"distFigureStartToLandmarkCentroid",
                                          "distFigureStartToLandmark",
                                          "distFigureEndToLandmark",
                                          "angleFigureToPastAxes",
                                          "pastAxesLength",
                                          ])

    
    def makeLearner(self):
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        return treeLearner
        #return orngEnsemble.RandomForestLearner()
    
