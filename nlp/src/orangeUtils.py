import math2d
import orngStat
import numpy as na
import orange
import orngTest
def accuracy(cm):
    return float(cm.TP + cm.FP) / (cm.TP + cm.FP + cm.FN + cm.TN)
def fScore(cm):
    try:
        return orngStat.F1(cm)
    except ZeroDivisionError:
        return 0 


def crossValidateWithSeparateTrainingAndTesting(training, testing, 
                                                learner,
                                                folds=10):
    assert len(training) == len(testing)
    indices = orange.MakeRandomIndicesCV(training, folds=folds)
    cm = orngStat.ConfusionMatrix()
    for i in range(folds):
        trainingFold = training.select(indices, i, negate=1)
        testingFold = testing.select(indices, i)
        results = orngTest.learnAndTestOnTestData([learner], trainingFold, 
                                                  testingFold)
        fCm = orngStat.confusionMatrices(results, classIndex = 0)[0]
        cm.TP += fCm.TP
        cm.FP += fCm.FP
        cm.FN += fCm.FN
        cm.TN += fCm.TN
    return cm
class PythonClassifier(orange.Classifier):
    def __init__(self):
        orange.Classifier.__init__(self)
    def classify(self, ex):
        raise NotImplementedError()
    def __call__(self, ex, what = orange.Classifier.GetValue):
        value = self.classify(ex)
        result = orange.Value(ex.domain.classVar, str(value))
        probs = orange.DiscDistribution(ex.domain.classVar)
        probs[value] = 1.0
        if what == orange.Classifier.GetValue:
            return result
        elif what == orange.Classifier.GetProbabilities:
            return probs
        elif what == orange.Classifier.GetBoth:
            return result, probs
        else:
            raise ValueError("Bad what argument: %s" % `what`)


def displayResults(results):
    for accuracy, cm in zip(orngStat.CA(results),
                            orngStat.confusionMatrices(results, classIndex=0)):
        
        print "accuracy", accuracy
        print " TP: %i, FP: %i, FN: %s, TN: %i" % (cm.TP, cm.FP, cm.FN, cm.TN)
        print "precision", orngStat.precision(cm)
        print "recall", orngStat.recall(cm)
        print "f1", fScore(cm)
        print

class ThresholdProbabilityLearner(orange.Learner):
    def __init__(self, positiveValue, negativeValue,
                 inputLearner=None, inputClassifier=None):
        self.positiveValue = positiveValue
        self.negativeValue = negativeValue

        if inputLearner != None:
            self.learner = inputLearner
            self.classifier = None
        elif inputClassifier != None:
            self.classifier = inputClassifier
        else:
            raise ValueError("Must pass exactly one of inputLearner and inputClassifier.")
        
    def __call__(self, examples, weightID=0):
        if self.classifier is None:
            classifier = self.learner(examples, weightID=weightID)
        else:
            classifier = self.classifier


        for f in examples.domain.classVar.values:
            print "f", f, f.__class__
        classIndex = examples.domain.classVar.values.index(self.positiveValue)
        results = orngTest.testOnData([classifier], examples)
        thresholds = list(na.arange(0, 1.1, 0.01))

        matrices = [orngStat.confusionMatrices(results, 
                                                classIndex=classIndex,
                                                cutoff=threshold)[0]
                    for threshold in thresholds]
        fscores = map(fScore, matrices)
        i, score = math2d.argMax(fscores)
        threshold = thresholds[i]
        print "fscores", fscores
        print "threshold", threshold
        print "score", score
        return ThresholdProbabilityClassifier(self.classifier, threshold,
                                              self.positiveValue, 
                                              self.negativeValue)
    
    
        

class ThresholdProbabilityClassifier(PythonClassifier):
    def __init__(self, classifier, threshold, 
                 positiveValue, negativeValue):
        self.positiveValue = positiveValue
        self.negativeValue = negativeValue
        self.classifier = classifier
        self.threshold = threshold
    def classify(self, ex, what=orange.Classifier.GetValue):
        value = self.classifier(ex, orange.Classifier.GetProbabilities)
        if value[self.positiveValue] > self.threshold:
            return self.positiveValue
        else:
            return self.negativeValue



def convertTable(table, newDomain):
    newTable = orange.ExampleTable(newDomain)
    for ex in table:
        newex = orange.Example(newDomain,
                               [ex[key] for key in newDomain])
        for var in newDomain.getmetas().values():
            newex[var.name] = ex[var.name]
        newTable.append(newex)
    return newTable


def confusion_matrix_to_string(domain, cm):
    classes = domain.classVar.values 
    colwidth = 9
    out = " " * (colwidth + colwidth/2)
    for c in classes:
        out += c.ljust(colwidth)
    out += "\n"
    for className, classConfusions in zip(classes, cm): 
        out += className.ljust(colwidth)
        for confusion in classConfusions:
            out += str(confusion).rjust(colwidth)
        out += "\n"
    return out

