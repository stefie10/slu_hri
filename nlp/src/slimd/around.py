import preposition
import past
import along
import orngTree
import argTypes
class Around(preposition.Preposition):
    """
    
    """
    def __init__(self):
        preposition.Preposition.__init__(self, "around", 
                                         [("obstacles", argTypes.Polygon, "*"),
                                          ("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [
                #to.StartPointFeatures(),
                #to.EndPointFeatures(),
                past.PastAxesFeatures(),
                #coaxial_distance_features.CoaxialDistanceFeatures(along.computeBoundaryLine),
                along.EndPointFeatures(),
                #along.LinearizingFeatures(),
                ],

                                         ["averageDistStartEndLandmarkBoundary",
                                          "distStartLandmarkBoundary",
                                          "figureStartToEnd"])
        
    def makeLearner(self):
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        return treeLearner
