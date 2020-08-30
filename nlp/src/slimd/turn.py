from PyQt4.QtCore import *
from PyQt4.QtGui import *
from preposition import Preposition, InsaneExample
from slimd import argTypes
import features
import math
import math2d
import numpy as na
import orange
import orngBayes
import orngTree
import os
import preposition

def makeData(engine, positiveDirectories, negativeDirectories):
    table = orange.ExampleTable(engine.domain())

    positiveCnt = 0
    for d in positiveDirectories:
        for fname in preposition.readDirectory(d):
            ex = engine.loadFile(fname)
            table.append(ex)
            positiveCnt += 1
    print "added", positiveCnt, "labeled examples."

    negativeCnt = 0
    for d in negativeDirectories:
        for fname in preposition.readDirectory(d):
            ex = engine.loadFile(fname)
            # only use positive examples from the other set.
            if ex['class'] == 'True':
                ex['class'] = 'False'
                table.append(ex)
                negativeCnt += 1
    print "added", negativeCnt, "negative examples."
    return table



class TurnFeatures(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self,
                                       {"deltaHeading":"The difference between the start heading and end heading of the figure.",
                                        "absDeltaHeading":"The absolute difference in heading,  measuring the degree of turn but not the direction.",
                                        "deltaStartHeadingToEnd":"The absolute difference in heading,  measuring the degree of turn but not the direction.",
                                       })
        
    def doCompute(self, drawer, figure, **args):
        if len(figure) == 0:
            raise InsaneExample("Figure has length 0." + `figure`)
        out = {}
        resolution = 100
        fps = math2d.stepAlongLine(figure, 
                                   math2d.length(figure)/resolution)

        size = 10
        startOfFigure = fps[:size]
        endOfFigure = fps[-size:]



        m1, b1 = math2d.fitLine(startOfFigure)
        m2, b2 = math2d.fitLine(endOfFigure)
        if na.isnan(m1):
            s1 = [startOfFigure[0], startOfFigure[-1]]
            assert math2d.isVertical(s1), s1
        else:
            s1 = [(startOfFigure[0][0], startOfFigure[0][0]*m1+b1),
                  (startOfFigure[-1][0], startOfFigure[-1][0]*m1+b1)]
        
        if na.isnan(m2):
            s2 = [endOfFigure[0], endOfFigure[-1]]
            assert math2d.isVertical(s2)
        else:
            s2 = [(endOfFigure[0][0], endOfFigure[0][0]*m2+b2),
                  (endOfFigure[-1][0], endOfFigure[-1][0]*m2+b2)]
                  
        for k in ["deltaHeading", "absDeltaHeading", "deltaStartHeadingToEnd"]:
            drawer.drawLine(k, s1)
            drawer.drawPoint(k, s1[0], "", Qt.green, 30)
            drawer.drawPoint(k, s1[-1], "", Qt.red, 30)

            drawer.drawLine(k, s2)
            drawer.drawPoint(k, s2[0], "", Qt.green, 30)
            drawer.drawPoint(k, s2[-1], "", Qt.red, 30)

        k = "deltaStartHeadingToEnd"
        drawer.drawLine(k, [figure[0], figure[-1]])
        drawer.drawLine(k, s1)
        drawer.drawPoint(k, s1[0], "", Qt.green, 30)
        drawer.drawPoint(k, s1[-1], "", Qt.red, 30)

        out["deltaStartHeadingToEnd"] = math2d.deltaHeading(s1, [figure[0],
                                                                 figure[-1]])

        out["deltaHeading"] = math2d.deltaHeading(s1, s2)
        out["absDeltaHeading"] = math.fabs(out["deltaHeading"])

        for k, v in out.iteritems():
            out[k] = math.degrees(v)
        return out
        
        

class LineFeatures(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self,
                                       {"stdErrOfRegression":"The standard error of a line fit to the points in the figure.",
                                        "figureLengthByCrow":"The ratio between the start and end points of the figure and the length.  Copied from an across feature.",

                                        })

    def doCompute(self, drawer, figure, **args):
        m = {}
        bborigin, (width, height) = math2d.boundingBox(figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)

        resolution = 100
        fps = math2d.stepAlongLine(figure, 
                                   math2d.length(figure)/resolution)
        
        slope, intercept, r_value, p_value, std_err = math2d.regression(fps)
        m["stdErrOfRegression"] = std_err / scale
        

        minX = min([p[0] for p in figure])
        maxX = max([p[0] for p in figure])
        drawer.drawLine("stdErrOfRegression", [(minX, minX*slope + intercept),
                                               (maxX, maxX*slope + intercept)])

        m['figureLengthByCrow'] = math2d.ratioLengthByCrow(figure)
        drawer.drawDistance("figureLengthByCrow", figure[0], figure[-1], "Start", "End")
        
        return m
        
                                       
class Turn(Preposition):
    def __init__(self, name):
        Preposition.__init__(self, name,
                             [("figure", argTypes.LineString, 1),
                              ],
                             [#LineFeatures(),
                              TurnFeatures(),
                              ],
                             #["deltaHeading", deltaSta])
                             )

    def makeLearner(self):
        treeLearner = orngTree.TreeLearner(storeExamples=True)
        bayesLearner = orngBayes.BayesLearner()
        return bayesLearner
    

class TurnRight(Turn):
    def __init__(self):
        Turn.__init__(self, "turnRight")

    def makeData(self):
        return makeData(self, 
                        ["%s/testdata/turn_right_examples" % 
                         os.environ["SLIMD_HOME"]],
                        ["%s/testdata/turn_left_examples" % 
                         os.environ["SLIMD_HOME"],
                         "%s/testdata/straight_examples" % 
                         os.environ["SLIMD_HOME"]])

class TurnLeft(Turn):
    def __init__(self):
        Turn.__init__(self, "turnLeft")

    def makeData(self):
        return makeData(self, 
                        ["%s/testdata/turn_left_examples" % 
                         os.environ["SLIMD_HOME"]],
                        ["%s/testdata/turn_right_examples" % 
                         os.environ["SLIMD_HOME"],
                         "%s/testdata/straight_examples" % 
                         os.environ["SLIMD_HOME"]])
    

        

        
                                                 
