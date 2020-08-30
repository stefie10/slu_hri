import numpy as na
from routeDirectionCorpusReader import readSession, Annotation
from sentenceTokenizer import SentenceTokenizer
import math2d
import pylab as mpl
mpl.rcParams.update({'font.family':'serif',})

def annotationsInRange(annotations, targetRange):
    return [a for a in annotations if targetRange.contains(a.range)]

def matches(groundTruthAnnotation, testAnnotation, keys=Annotation.keys):
    for key in keys:
        testValue = testAnnotation.annotationMap[key]
        groundTruthValue = groundTruthAnnotation.annotationMap[key]
        #if not testValue.isNull() and testValue.range != groundTruthValue.range:
        if testValue.range != groundTruthValue.range:
            return False
    return True



def compareAnnotations(groundTruthSessions, testSessions, keys=Annotation.keys):
    sentenceTokenizer = SentenceTokenizer()
    
    numMatches = 0.0
    total = 0.0
    
    for groundTruthSession, testSession in zip(groundTruthSessions, 
                                               testSessions):
        for instructionIdx, instruction in enumerate(testSession.routeInstructions):
            for sentenceStandoff in sentenceTokenizer.tokenize(testSession.routeInstructions[instructionIdx]):
                testAnnotations = annotationsInRange(testSession.routeAnnotations[instructionIdx],
                                                     sentenceStandoff)
                groundTruthAnnotations = annotationsInRange(groundTruthSession.routeAnnotations[instructionIdx],
                                                            sentenceStandoff)
                
                for testAnnotation in testAnnotations:
                    degreesOfOverlap = [testAnnotation.degreeOfOverlap(x) for x in groundTruthAnnotations]
                    matchIdx, matchValue = math2d.argMax(degreesOfOverlap)
                    if (not(matchIdx is None) and 
                        matches(groundTruthAnnotations[matchIdx], testAnnotation, keys)):
                        numMatches += 1
                    total += 1
    return numMatches / total
                

def runNWay(sessionNames):
    for groundTruth in sessionNames:
        for test in sessionNames:
            fname = "data/Direction understanding subjects Floor 8 (Final).ods"
            groundTruthSessions = readSession(fname, groundTruth)
            testSessions = readSession(fname, test)
            score = compareAnnotations(groundTruthSessions, testSessions)
            print "score", groundTruth, test, score
                    

if __name__ == "__main__":
    runNWay(["dlaude"])
    runNWay(["stefie10", "dlaude", "crf_chunker"])
    fname = "data/Direction understanding subjects Floor 8 (Final).ods"
    groundTruthSessions = readSession(fname, "stefie10")
    testSessions = readSession(fname, "crf_chunker")
    score = compareAnnotations(groundTruthSessions, testSessions)
    print "score", score


    data = [compareAnnotations(groundTruthSessions, testSessions, [key]) for key in Annotation.keys]
    labels = list(Annotation.abbrvKeys)
    
    data.append(compareAnnotations(groundTruthSessions, testSessions, ["spatialRelation", "landmark"]))
    labels.append("SR and L")
    
    data.append(compareAnnotations(groundTruthSessions, testSessions))
    labels.append("All")


    mpl.ylabel("Fraction of Matched Annotations", fontsize=15)
    
    xlocations = na.array([x+0.5 for x in range(len(data))])
    mpl.bar(xlocations, data)

    mpl.xticks(xlocations + 0.5, labels, rotation=0)

    ax = mpl.axes()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(15)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(12)
    mpl.savefig("sdcExtractorPerformance.png")
    mpl.show()
