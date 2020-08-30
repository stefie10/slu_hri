import orange, orngTest, orngStat
import orangeUtils
from numpy import arange
from orangeUtils import fScore

def returnNone(ex):
    return None

"""
Classifies with a single threshold of a single feature.
"""

class ThresholdClassifier(orangeUtils.PythonClassifier):
    def __init__(self, attributeName, threshold, order, 
                 classifyFunction=returnNone):
        self.attributeName = attributeName
        self.threshold = threshold
        self.order = order
        self.classifyFunction = classifyFunction
    def classify(self, ex):
        value = self.classifyFunction(ex)
        if value == None:
            if ex[self.attributeName] <= self.threshold:
                value = self.order[0]
            else:
                value = self.order[1]
        return value

    def __str__(self):
        return "ThresholdClassifier('%s', %f, %s)" % (self.attributeName,
                                                      self.threshold,
                                                      self.order)
    def __repr__(self):
        return str(self)

class ThresholdLearner(orange.Learner):
    def __init__(self, attributeName, classifyFunction=returnNone):
        self.attributeName = attributeName
        self.classifyFunction = classifyFunction
    def __call__(self, examples, weightID=0):
        maxValue = max([x[self.attributeName] for x in examples])
        minValue = min([x[self.attributeName] for x in examples])
        steps = 10
        bestAccuracy = 0
        bestThreshold = None
        values = ["True", "False"] #examples.domain.classVar.values
        assert len(values) == 2
        reversedValues = [x for x in reversed(values)]

        classifiers = []
        for threshold in arange(minValue, maxValue, 
                                (maxValue - minValue) / steps):
            classifiers.append(ThresholdClassifier(self.attributeName,
                                                   threshold,
                                                   values,
                                                   self.classifyFunction))
            classifiers.append(ThresholdClassifier(self.attributeName,
                                                   threshold,
                                                   reversedValues,
                                                   self.classifyFunction))




        maxFScore = 0
        bestClassifier = None
        for x in classifiers:
            results = orngTest.testOnData([x], examples)
            fscore = [fScore(cm) for cm in orngStat.confusionMatrices(results, classIndex=0)][0]
            if maxFScore <= fscore:
                maxFScore = fscore
                bestClassifier = x
        return bestClassifier



