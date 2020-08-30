from annotations import containingAnnotations
from chunker import tokenize
from environ_vars import *
from os import system
from routeDirectionCorpusReader import Annotation, readSession, TextStandoff
from sentenceTokenizer import SentenceTokenizer
import annotations
import chunker
import numpy as na

def hasAllNullValues(standoffMap):
    for key, standoff in standoffMap.iteritems():
        if not standoff.isNull() and key != "None":
            return False
    return True

def sh(cmd):
    print cmd
    system(cmd)

class ConfusionMatrix:
    def __init__(self, labels):
        self.labels = labels
        self.matrix = na.zeros((len(self.labels), len(self.labels)), int)
        self.keysToIndex = dict([(key, idx) for idx, key in enumerate(labels)])
    def increment(self, key1, key2):
        self.matrix[self.keysToIndex[key1], self.keysToIndex[key2]] += 1

    def __str__(self):

        maxWidth = max([len(x) for x in self.labels])
        width = maxWidth + 1
        string = "      "
        string += string.ljust(width)

        for label in self.labels:
            string +=  label.ljust(width) + " "
        string += "\n"
        
        for i, label in enumerate(self.labels):
            string += label.rjust(width)
            for j, label in enumerate(self.labels):
                string += ("%d" % self.matrix[i,j]).rjust(width) + " "
            string += "\n"
        return string
    def accuracy(self):
        correct = 0.0
        total = 0.0
        for i, label in enumerate(self.labels):
            for j, label in enumerate(self.labels):
                total += self.matrix[i,j]
                if i == j:
                    correct += self.matrix[i,j]

        return correct / total

                    

class CrfChunker:
    def __init__(self, modelFile):
        self.tagger = chunker.makeTagger()
        self.sentenceTokenizer = SentenceTokenizer()
        self.modelFile = modelFile
    def writeTrainingSession(self, session, instructionIdx, out):
        instruction = session.routeInstructions[instructionIdx]
        annotations = session.routeAnnotations[instructionIdx]

        self.writeTrainingForText(instruction, annotations, out)
    
    
    def writeTrainingForText(self, text, annotations, out):
        for sentenceStandoff in self.sentenceTokenizer.tokenize(text):
            indexes, tokens = tokenize(sentenceStandoff.text)    
            tags = self.tagger.tag(tokens)

            for startIndex, (word, posTag) in zip(indexes, tags):
                startIndex = startIndex + sentenceStandoff.start
                wordRange = startIndex, startIndex + len(word)
                annotation, key = containingAnnotations(annotations, wordRange)
                if not (annotation is None):
                    chunk = key
                else:
                    chunk = "None"
                out.write("\t".join([word, posTag, chunk]) + "\n")
            out.write("\n")

    
        
        
    def writeTraining(self, sessions, outFileName):
        out = open(outFileName, "w")
        for session in sessions:
            for instructionIdx in range(len(session.routeInstructions)):
                #if session.subject == "Subject 17" and instructionIdx == 2:
                self.writeTrainingSession(session, instructionIdx, out)
                out.write("\n")
        out.close()
    def runTraining(self, templateFile, trainingFile, outputFile):
        sh(TKLIB_HOME + "/nlp/3rdParty/crf++/CRF++-0.53/crf_learn %s %s %s" %
           (templateFile, trainingFile, outputFile))

    def runTesting(self, modelFile, testingFile, outputFile):
        sh(TKLIB_HOME+ "/nlp/3rdParty/crf++/CRF++-0.53/crf_test -m %s %s > %s" %
           (modelFile, testingFile, outputFile))

    def confusionMatrix(self, outputFile):
        cmKeys = Annotation.keys + ["None"]

        cm = ConfusionMatrix(cmKeys)
        baselineCm = ConfusionMatrix(cmKeys)
        for line in open(outputFile, "r"):
            tokens = line.split()
            if len(tokens) == 0:
                continue
            else:
                token = tokens[0]
                features = tokens[1:-3]
                trueLabel = tokens[-2]
                systemLabel = tokens[-1]

                #token, pos, trueLabel, systemLabel = tokens
                cm.increment(trueLabel, systemLabel)
                baselineCm.increment(trueLabel, "landmark")
        return cm, baselineCm
    def chunk(self, string):
        import CRFPP
        tagger = CRFPP.Tagger("-m " + self.modelFile)
        indexes, tokens = tokenize(string)
        tags = self.tagger.tag(tokens)
        tagger.clear()


        for word, posTag in tags:
            tagger.add(str("%s %s" % (word, posTag)))
        tagger.parse()
        for i, (index, token) in enumerate(zip(indexes, tokens)):
            label = tagger.y2(i)
            #print index, token, label
        labels = [tagger.y2(i) for i in range(len(tokens))]
        return indexes, tokens, labels
            

def trainingAndTestingSplit():
    fname = TKLIB_HOME+"/nlp/data/Direction understanding subjects Floor 8 (Final).ods"

    sessions = readSession(fname, 'stefie10')
    splitPoint = len(sessions) / 2
    training = sessions[0:splitPoint]
    testing = sessions[splitPoint:]
    return training, testing
def trainingAndTestingFloor1():
    training = readSession(TKLIB_HOME+"/nlp/data/Direction understanding subjects Floor 1 (Final).ods", 'stefie10')
    testing = readSession(TKLIB_HOME+"/nlp/data/Direction understanding subjects Floor 8 (Final).ods", 'stefie10')
    return training, testing

def trainingAndTesting():
    return trainingAndTestingFloor1()

"""
Trains the CRF model for tagging text, and saves it.
"""
def trainModel():
    training, testing = trainingAndTesting()

    trainingFile = "training.txt"
    testingFile = "testing.txt"

    modelFile = TKLIB_HOME+"/nlp/data/out.model"

    outputFile = "out.txt"
    chunker = CrfChunker(modelFile)
    chunker.writeTraining(training, trainingFile)
    chunker.writeTraining(testing, testingFile)

    chunker.runTraining(TKLIB_HOME+"/nlp/etc/crf++/test.template",
                        trainingFile, modelFile)

    chunker.runTesting(modelFile, testingFile, outputFile)

    cm, baselineCm = chunker.confusionMatrix(outputFile)
    print "system"
    print cm
    print "accuracy", cm.accuracy()
    print

    print "baseline (always pick landmark)"
    print baselineCm
    print "accuracy", baselineCm.accuracy()

    print
    print


class RecursiveSdcExtractor:
    def __init__(self, extractor):
        self.extractor = extractor
    def chunk(self, txt):
        sdcs = []
        first = True
        for t in txt.split(" to "):
            if not first:
                t = "to " + t
            sdcs.extend(self.extractor.chunk(t))
            first = False
        return sdcs

class SdcExtractor:
    def __init__(self, modelFile=TKLIB_HOME+ "/nlp/data/out.model"):
        self.sentenceTokenizer = SentenceTokenizer()
        self.chunker = CrfChunker(modelFile)
        
    def chunk(self, instructionTxt):
        try:
            return self.doChunk(instructionTxt)
        except:
            print instructionTxt
            print instructionTxt.__class__
            raise
    def doChunk(self, instructionTxt):
        """
        The method takes a string and returns a list of Annotations,
        which I should rename to SpatialDescriptionClause.  Each
        Annotation contains a figure, a ground, a spatial relation,
        and a verb.  It uses standoff tags internally so you know
        exactly what part of the input string is part of each field.
        """

        annotations = []
        for sentenceStandoff in self.sentenceTokenizer.tokenize(instructionTxt):
            indexes, tokens, labels = self.chunker.chunk(sentenceStandoff.text)
            def nullMap():
                return dict([(key, TextStandoff(instructionTxt, (0, 0)))
                             for key in Annotation.keys])

            offset = sentenceStandoff.start
            annotation = nullMap()
            currentField = None
            currentStandoff = TextStandoff(instructionTxt, (0, 0))
            #print
            #print
            for index, token, label in zip(indexes, tokens, labels):
                if currentField != label:
                    if not currentStandoff.isNull():
                        annotation[currentField] = currentStandoff

                    if label == "None" or not annotation[label].isNull():
                        #print "adding annotation."
                        #for key in Annotation.keys:
                        #    print key, annotation[key].text

                        if not hasAllNullValues(annotation):
                            annotations.append(Annotation(**annotation))
                            annotation = nullMap()

                    currentStandoff = TextStandoff(instructionTxt, (index + offset, index + len(token) + offset))
                    currentField = label
                else:
                    currentStandoff.range = (currentStandoff.start, index + len(token) + offset)


            if not currentStandoff.isNull():
                annotation[currentField] = currentStandoff
            # only add if there are non-null fields.
            if not hasAllNullValues(annotation):
                annotations.append(Annotation(**annotation))
        return annotations


"""
Uses an existing model to chunk instructions and save them to xml.
"""
def chunkInstructions():
    training, testing = trainingAndTesting()
    fname = "data/Direction understanding subjects Floor 8 (Final).ods"
    sessions = readSession(fname, 'stefie10')
#    splitPoint = len(sessions) / 2
#    outputSessions = readSession(fname, 'crf_chunker')[splitPoint:]
    outputSessions = readSession(fname, 'crf_chunker')


    trainingFile = "training.txt"
    testingFile = "testing.txt"
    modelFile = "out.model"
    outputFile = "out.txt"


    chunker = CrfChunker()
    chunker.writeTraining(testing, testingFile)

    outputFile = "floor1.out.txt"
    chunker.runTesting(modelFile, testingFile, outputFile)

    cm, baselineCm = chunker.confusionMatrix(outputFile)

    print "system"
    print cm
    print "accuracy", cm.accuracy()
    print

    print "baseline (always pick landmark)"
    print baselineCm
    print "accuracy", baselineCm.accuracy()
    
    iChunker = SpatialDescriptionClauseExtractor()


    for session in outputSessions:
        session.clearAnnotations()
        for instructionIdx, instruction in enumerate(session.routeInstructions):
            annotations = iChunker.chunk(session.routeInstructions[instructionIdx])
            for a in annotations:
                print "a", a, a.__class__
                session.addAnnotation(instructionIdx, a)
        session.saveAnnotations()

            


def main():
    trainModel()
    #chunkInstructions()

if __name__ == "__main__":
    main()
