from slimd import argTypes
import features
import math2d
import orange
import orngTree
import os
import preposition
import to
import numpy as na

class DisplacementFeatures(features.FeatureGroup):
    """
    This feature measures the net distance traveled by the figure
    towards the landmark.  It is illustrated in
    Figure~\\ref{fig:displacement}.
    """
    def __init__(self):
        features.FeatureGroup.__init__(self,
                                       {"displacementFromLandmark":    "This feature measures the net distance traveled by the figure towards the landmark.  It is illusrated in Figure~\\ref{fig:displacement}."})
    def doCompute(self, drawer, landmark, figure, **args):
        out = {}
        bborigin, (width, height) = math2d.boundingBox(na.append(landmark,
                                                                 figure, 0))
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        landmarkCentroid = math2d.centroid(landmark)

        dFigureStartToLandmark = math2d.dist(landmarkCentroid, figure[0])
        dFigureEndToLandmark = math2d.dist(landmarkCentroid, figure[-1])
        drawer.drawLine("displacementFromLandmark", 
                        [landmarkCentroid, figure[0]])

        drawer.drawLine("displacementFromLandmark", 
                        [landmarkCentroid, figure[-1]])



        out["displacementFromLandmark"] = (dFigureEndToLandmark - dFigureStartToLandmark)/scale
        return out

class AwayFrom(preposition.Preposition):
    """
    As in ``walk away from the door.''
    """
    def __init__(self):
        preposition.Preposition.__init__(self, "away from", 
                                         [#("obstacles", QGis.WKBPolygon, "*"),
                                          ("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [DisplacementFeatures(),
                                          to.EndPointFeatures(),
                                          ],
                                         ["distFigureEndToLandmark",
                                          "distFigureStartToLandmark",
                                          "displacementFromLandmark",
                                          ]
                                         )


    def makeLearner(self):
        #return orngEnsemble.RandomForestLearner()
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        treeLearner.stop = orange.TreeStopCriteria_common() 
        treeLearner.maxDepth=4
        return preposition.RejectInsaneExampleLearner(treeLearner)        

    def dataFiles(self):
        return preposition.readDirectory("%s/testdata/awayFrom_examples" % os.environ["SLIMD_HOME"])
