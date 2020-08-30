import preposition
import coaxial_distance_features
import across
import along
import awayFrom
import orngTree
import argTypes
import math2d

class Out(preposition.Preposition):
    def __init__(self):
        preposition.Preposition.__init__(self, "out", 
                                         [("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [across.AxesFeatures(), 
                                          along.LinearizingFeatures(),
                                          coaxial_distance_features.CoaxialDistanceFeatures(math2d.computeBoundaryLine),
                                          awayFrom.DisplacementFeatures(),
                                          #visibilityFeatures.VisibilityFeatures()
                                          ],
                                         ["displacementFromLandmark",
                                          "figureCenterOfMassToLandmarkCentroid",
                                          "averageDistToAxes",
                                          ],
                                          )
        
    def makeLearner(self):
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        return treeLearner
    
