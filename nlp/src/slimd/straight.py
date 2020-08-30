from slimd import argTypes
import orngTree
import orngBayes
import os
import preposition
import turn


                                       
class Straight(preposition.Preposition):
    def __init__(self):
                preposition.Preposition.__init__(self, "straight",
                                                 [("figure", argTypes.LineString, 1)],
                                                 [turn.LineFeatures(),
                                                  turn.TurnFeatures(),
                                                  ],
                                                 ["figureLengthByCrow"]
                                                 )

    def makeData(self):
        return turn.makeData(self, 
                             ["%s/testdata/straight_examples" % 
                              os.environ["SLIMD_HOME"]],
                             ["%s/testdata/turn_right_examples" % 
                              os.environ["SLIMD_HOME"],
                              "%s/testdata/turn_left_examples" % 
                              os.environ["SLIMD_HOME"]])

        #return turn.makeData(self, 
        #                     ["%s/testdata/straight_examples" % 
        #                      os.environ["SLIMD_HOME"]],
        #                     [])
                             
        

    def makeLearner(self):
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        bayesLearner = orngBayes.BayesLearner()
        return bayesLearner                                                 

