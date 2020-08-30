import os
import to
import preposition
import orngTree
import argTypes

class Until(preposition.Preposition):
    def __init__(self):
        preposition.Preposition.__init__(self, "until", 
                                         [("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [to.EndPointFeatures(),
                                          #StartPointFeatures(),
                                          to.DistToLandmarkFeatures(),
                                          #towards.AxesFeatures(), # don't help, in icmi land.
                                          to.BoundingBoxFeatures(),
                                          #visibilityFeatures.VisibilityFeatures(),
                                          ],
                                         ["distFigureEndToLandmark",
#                                          "minimumDistanceToLandmark",
                                          "startPointsInLandmarkBoundingBox"
                                          ]

                                         )
        
    def dataFiles(self):
        return preposition.readDirectory("%s/testdata/until_examples" % os.environ["SLIMD_HOME"])
    def makeLearner(self):
        return orngTree.TreeLearner()
        
    
