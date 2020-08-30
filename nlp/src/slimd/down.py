from slimd import along
import across
import argTypes
import coaxial_distance_features
import orange
import orngTree
import os
import preposition
import to
import math2d
class Down(preposition.Preposition):
    """
    As in ``down the hall'' or ``down the road.''
    """
    def __init__(self):
        preposition.Preposition.__init__(self, "down", 
                                         [#("obstacles", QGis.WKBPolygon, "*"),
                                          ("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [#coaxial_distance_features.CoaxialDistanceFeatures(along.computeBoundaryLine),
                                             coaxial_distance_features.CoaxialDistanceFeatures(math2d.computeBoundaryLine),
                                             across.AxesFeatures(),
                                             along.EndPointFeatures(),
                                             to.BoundingBoxFeatures(),
                                             across.EigenAxes(),
                                             #along.LinearizingFeatures(),
                                             #visibilityFeatures.VisibilityFeatures()
                                          ]
                                         ,
                                         ["figureCenterOfMassToAxesOrigin",
                                          "stdDevToAxes",
                                          "distAlongLandmarkBtwnAxes",
                                          "eigenAxesRatio",
                                          ]
                                         )


    def makeLearner(self):
        #return orngEnsemble.RandomForestLearner()
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        treeLearner.stop = orange.TreeStopCriteria_common() 
        treeLearner.maxDepth=4
        return preposition.RejectInsaneExampleLearner(treeLearner)        

    def dataFiles(self):
        return preposition.readDirectory("%s/testdata/down_examples" % os.environ["SLIMD_HOME"])
