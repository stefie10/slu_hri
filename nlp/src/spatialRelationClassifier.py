import traceback
from slimd import across
from slimd import along
from slimd import turn
from slimd import straight
from slimd import through
from slimd import past
from slimd import around
from slimd import to
from slimd import out
from slimd import towards
from slimd import down
from slimd import awayFrom
from slimd import until
import cPickle as pickle
import chunker
from slimd.preposition import orangeToBoolean
import os


def pointToSmallPolygon(point, width=0.1):
    """
    Converts a point to a small square with width
    """
    offset = width * 0.5
    x, y = point
    return [(x - offset, y - offset),
            (x - offset, y + offset),
            (x + offset, y + offset),
            (x + offset, y - offset),]


def printClassProbs(classifier):
    nValues=len(classifier.classVar.values)
    frmtStr=' %10.3f'*nValues
    classes=" "*20+ ((' %10s'*nValues) % tuple([i[:10] for i in classifier.classVar.values]))
    print classes
    print "class probabilities "+(frmtStr % tuple(classifier.distribution))
    print


def isPolygon(arg):
    try:
        for p in arg:
            x, y = p

        return True
    except:
        #traceback.print_exc()
        return False

    
def ensurePolygon(arg):
    if isPolygon(arg):
        return arg
    else:
        return pointToSmallPolygon(arg, width=0.001)
    


def loadEngineMap():
    print 'loading engine map'
    return pickle.load(open("%s/nlp/data/engines.floor3.stefie10.pck" % os.environ["TKLIB_HOME"], "rb"))


try:
    engineMap = loadEngineMap()
    #engineMap = None
except:
    traceback.print_exc()
    print "ignoring engine map load error"
    engineMap = None



liveEngineMap = {"across":across.Across(),
                 "along":along.Along(),
                 "through":through.Through(),
                 "past":past.Past(),
                 "around":around.Around(),
                 "to":to.To(),
                 "out":out.Out(),
                 "towards":towards.Towards(),
                 "down":down.Down(),
                 "away from":awayFrom.AwayFrom(),
                 "until":until.Until(),
                 "turnRight":turn.TurnRight(),
                 "turnLeft":turn.TurnLeft(),
                 "straight":straight.Straight(),
                 }

#liveEngineMap = dict((name, CEngine(engine))
#                     for name, engine in liveEngineMap.iteritems())






class SpatialRelationClassifier:
    def __init__(self):
        print "engine map", engineMap
        self.set_engine_map(engineMap)
        



        
    
    @property
    def engineMap(self):
        return self._engineMap

    def set_engine_map(self, newMap):
        print "calling setter", newMap
        print "classifier in set engine map"
        self._engineMap = newMap

        if "straight" in self._engineMap:
            del self._engineMap["straight"]

        if "turnRight" in self._engineMap:            
            del self._engineMap["turnRight"]

        if "turnLeft" in self._engineMap:            
            del self._engineMap["turnLeft"]



        self.tokenToEngine = dict(self.engineMap)
        self.tokenToEngine["toward"] = self.engineMap["towards"]
        self.tokenToEngine["thru"] = self.engineMap["through"]
        self.tokenToEngine["under"] = self.engineMap["through"]
        self.tokenToEngine["away"] = self.engineMap["away from"]
        self.tokenToEngine["from"] = self.engineMap["away from"]
        self.tokenToEngine["out"] = self.engineMap["away from"]
        self.tokenToEngine["onto"] = self.engineMap["to"]
        self.tokenToEngine["into"] = self.engineMap["to"]
        self.tokenToEngine["down"] = self.engineMap["past"] # no polygons...
        self.engineNames = sorted(self.engineMap.keys())
        self._engineToIdx = dict([(x, i) for i, x in enumerate(self.engineNames)])

    def sdcToClassifier(self, sdc):
        """
        Finds the classifier for an sdc. 
        """
        vIndexes, vTokens = chunker.tokenize(sdc.verb.text)
        srIndexes, srTokens = chunker.tokenize(sdc.spatialRelation.text)
        vTokens = [x.lower() for x in vTokens]
        srTokens = [x.lower() for x in srTokens]
        

        if "pass" in vTokens and "past" in self.tokenToEngine:
            return self.tokenToEngine["past"]
        else:
            for sp, engine in self.tokenToEngine.iteritems():
                if sp in srTokens:
                    if sp == "to" and sdc.spatialRelation.text.lower() != "to" and len(sdc.spatialRelation.text.split()) > 2:
                        # if they say "with your back to" or "to the left of", don't use "to."
                        continue
                    else:
                        return self.tokenToEngine[sp]


        if "stop" in vTokens:
            if not sdc.landmark.isNull() and "until" in self.tokenToEngine:
                return self.tokenToEngine["until"]

#        if "exit" in vTokens or "leave" in vTokens:
#            if not sdc.landmark.isNull():
#                return self.tokenToEngine["out"]

        return None


    def engineToIdx(self, engineName):
        return self._engineToIdx[engineName]

    def classifySpatialRelation(self, annotation, landmark, figure):
        """
        Classifies a spatial relation given a path.
        returns True/False, confidence

        Right now, confidence is the weight for the returned class
        from naive bayes, right now. 0 <= confidence <= 1. 
        """
        
        classifier = self.sdcToClassifier(annotation)
        if classifier is None:
            raise NoClassifierError(annotation)
        return self.doClassify(classifier, landmark, figure)

    def classify(self, spatialRelation, landmark, figure):
        return self.doClassify(self.sdcToClassifier_text(spatialRelation), landmark, figure)
    
    
    def doClassify(self, classifier, landmark, figure):
        try:

            cls, probabilities, ex = classifier.classify(figure=figure,
                                                         landmark=landmark)

        except:
            print "landmark", landmark
            print "figure", figure
            raise
        if probabilities is None:
            if cls == "True":
                score = 1
            elif cls == "False":
                score = 0
            else:
                raise ValueError("Unexpected class:" + `cls`)
        else:
            score = probabilities[cls]
        boolCls = orangeToBoolean(cls)
        if boolCls:
            return classifier, orangeToBoolean(cls), score
        else:
            return classifier, orangeToBoolean(cls), 1-score

    def classifySpatialRelation_text(self, mytext, landmark, figure):
        """
        Classifies a spatial relation given a path.
        returns True/False, confidence

        Right now, confidence is the weight for the returned class
        from naive bayes, right now. 0 <= confidence <= 1. 
        """
        
        classifier = self.sdcToClassifier_text(mytext)
        if classifier is None:
            raise NoClassifierError(None)
        return self.doClassify(classifier, landmark, figure)


    
    def sdcToClassifier_keyword(self, sdc):
        """
        The original algorithm to get sds for classifiers, using
        string containment.
        """
        for srname, engine in self.engineMap.iteritems():
            if(srname in sdc["spatialRelation"].text):
                return engine
        return None


    def sdcToClassifier_text(self, mytext):
        #srIndexes, srTokens = chunker.tokenize(mytext)
        #srTokens = [x.lower() for x in srTokens]

        if "pass" in mytext:
            return self.engineMap["past"]
        else:
            for sp, engine in self.engineMap.iteritems():
                if sp in mytext:
                    return self.engineMap[sp]
        return None





class NoClassifierError(Exception):
    def __init__(self, annotation):
        Exception.__init__(self, "Can't find classifier for: %s" % annotation.text, annotation)
        self.annotation = annotation
