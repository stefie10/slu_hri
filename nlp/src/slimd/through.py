from slimd import argTypes
import across
import coaxial_distance_features
import math2d
import orange
import orngTree
import preposition

class Through(preposition.Preposition):
    """
    Features for ``towards'' are borrowed from ``across.''
    """
    def __init__(self):
        preposition.Preposition.__init__(self, "through", 
                                         [("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [across.AxesFeatures(), 
                                          coaxial_distance_features.CoaxialDistanceFeatures(across.lineFunction),
                                          ],
                                         ['distAlongLandmarkBtwnAxes',
                                          'figureCenterOfMassToLandmarkCentroid',
                                          'ratioFigureToAxes' ]
                                         )
    def makeLearner(self):
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        treeLearner.stop = orange.TreeStopCriteria_common() 
        treeLearner.maxDepth=5
        return preposition.RejectInsaneExampleLearner(treeLearner)



    def makeExample(self, landmark, figure, expectInsane=True, **args):
        try:
            return preposition.Preposition.makeExample(self, landmark=landmark, 
                                                       figure=math2d.clip(figure, 
                                                                          landmark),
                                                       expectInsane=expectInsane)
        except Exception, e:
            e.classifierArgs = args
            raise
