from routeDirectionCorpusReader import readSession
from chunker import makeTagger, tokenize

class ConfusionMatrix:
    def __init__(self):
        self.TP = 0.0
        self.FP = 0.0
        self.TN = 0.0
        self.FN = 0.0
    @property
    def numberOfExamples(self):
        return self.TP + self.FP + self.TN + self.FN
    @property
    def accuracy(self):
        if self.numberOfExamples == 0:
            return 0.0
        else:
            return float(self.TP + self.FP) / (self.TP + self.FP + self.FN + self.TN)
    @property
    def precision(self):
        if self.numberOfExamples == 0:
            return 0.0
        else:
            return float(self.TP) / (self.TP + self.FP)
    @property
    def recall(self):
        if self.numberOfExamples == 0:
            return 0.0
        else:
            return float(self.TP) / (self.TP + self.FN)
    @property
    def f1(self):
        return 2.0 * self.precision * self.recall / (self.precision + self.recall)

def findMatch(testAnnotation, groundTruthAnnotations, matchFunction):
    for i, groundTruthAnnotation in enumerate(groundTruthAnnotations):
        if matchFunction(testAnnotation, groundTruthAnnotation):
            return i, groundTruthAnnotation
    return None, None
def ppMatch(x, y):
    return ((x.spatialRelation.range == y.spatialRelation.range) and
            (x.landmark.range == y.landmark.range))
def npMatch(x, y):
    return x.landmark.range == y.landmark.range

def score(groundTruthSessions, testSessions):
    tagger = makeTagger()
    cm = ConfusionMatrix()

    for groundTruth in groundTruthSessions:
        testSession = testSessions[groundTruth]
        for instructionIdx, instruction in enumerate(groundTruth.routeInstructions):
            groundTruthAnnotations = groundTruth.routeAnnotations[instructionIdx]

            indexes, tokens = tokenize(instruction)
            print "tokens", tokens
            tags = tagger.tag(tokens)
            print " ".join(["%s/%s" % (word, tag) 
                            for word, tag in tags])

            matchedIndexes = [False for g in groundTruthAnnotations]
            if len(groundTruthAnnotations) != 0:
                print "considering", groundTruth.key, "instruction", instructionIdx
                for testAnnotation in testSession.routeAnnotations[instructionIdx]:

                    idx, groundTruthMatch = findMatch(testAnnotation, 
                                                      groundTruthAnnotations,
                                                      npMatch)

                    
                    if groundTruthMatch is None:
                        print "fp", testAnnotation
                        cm.FP += 1
                    else:
                        print "tp", testAnnotation
                        print "\tmatched", groundTruthMatch
                        cm.TP += 1
                        matchedIndexes[idx] = True
                for i, hasMatch in enumerate(matchedIndexes):
                    if not hasMatch:
                        cm.FN += 1
                        print "fn", groundTruthAnnotations[i]
                    #else:
                    # what to do with true negatives
                        
    print "precision", cm.precision
    print "recall", cm.recall
    print "f1", cm.f1
                            
                    
                

if __name__ == "__main__":
    fname = "data/Direction understanding subjects Floor 1 (Final).ods"
    #fname = "data/Direction understanding subjects Floor 1.ods"
    groundTruthSessions = readSession(fname, "stefie10")
    testSessions = readSession(fname, "regexp_chunker")
    score(groundTruthSessions, testSessions)
    

    
