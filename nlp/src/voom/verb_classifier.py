
from features import FeatureCollection, InsaneExample
import math
import orange


class Signature:
    def __init__(self, **args):
        for argname, argtype in args.iteritems():
            assert isinstance(argname, str)
            self.args = args
    def iteritems(self):
        return self.args.iteritems()

class Classifier:
    def __init__(self, engine, classifier):
        self.engine = engine
        self.classifier = classifier
        self.clear()

    def clear(self):
        """
        Clear the saved state.
        """
        self.ex = None
        self.features = None
        self.drawMap = None
        self.cls = None
        self.probabilities = None
        self.has_data = False
        
    def classify(self, situation):
        self.ex, self.features, self.drawMap = self.engine.makeExampleFull(situation)
        
        if self.classifier != None:
            #print "ex", self.ex 
            self.cls, probs = self.classifier(self.ex, orange.GetBoth)
            if isinstance(probs, dict):
                self.pTrue = probs["True"]
                self.pFalse = probs["False"]
            else:
                self.pTrue = probs[0]
                self.pFalse = probs[1]
                
        
            if math.isnan(self.pTrue) or math.isnan(self.pFalse):
                if self.cls == "True":
                    self.pTrue = 1
                    self.pFalse = 0
                elif self.cls == "False":
                    self.pTrue = 0
                    self.pFalse = 1
        
        
            self.has_data = True        
            if self.cls.value == "True":
                return True
            else:
                return False
        else:
            return None

        
class Engine:
    def __init__(self, name, signature, feature_groups, isLiquid=False):
        self.name = name
        self.signature = signature
        self.features = FeatureCollection(feature_groups)
        self.domain = self.makeDomain()
        self.isLiquid = isLiquid

    def makeDomain(self):
        attributes = [orange.FloatVariable(n) for n in self.features.names] 

        attributes.append(orange.EnumVariable("isInsane", 
                                              values=["True", "False"]))
        domain = orange.Domain(attributes,
                               # orange broke when there were two enume variables
                               # with the same name but different values. 
                               # the one in spatial relations land is called
                               # "class" with three values ("bad tracking"). 
                               # it was something to do with pickling and unpickling
                               # and importing - anyway I fixed it by renaming the
                               # class attribute. -- stefie10, 1/13/2009
                               orange.EnumVariable("verbclass", 
                                                   values=["True", "False"]))


        
        domain.addmeta(orange.newmetaid(), orange.PythonVariable("drawMap"))
        domain.addmeta(orange.newmetaid(), orange.PythonVariable("entry"))
        domain.addmeta(orange.newmetaid(), orange.PythonVariable("situation"))
        domain.addmeta(orange.newmetaid(), orange.PythonVariable("engine"))
        domain.addmeta(orange.newmetaid(), orange.PythonVariable("description"))
        domain.addmeta(orange.newmetaid(), orange.PythonVariable("exceptions"))
        return domain

    def makeExample(self, situation):
        ex, features, drawMap = self.makeExampleFull(situation)
        return ex

    def makeExampleFull(self, situation):

        try:
            features, drawMap, exceptions = self.features.computeAndVisualize(situation)
            features['drawMap'] = drawMap
            features['situation'] = situation
            if len(exceptions) != 0:
                features['isInsane'] = "True"
            else:
                features['isInsane'] = "False"
            lst = []
            for attr in self.domain:
                if attr.name == "verbclass":
                    lst.append("")
                else:
                    if attr.name in features:
                        featureValue = features[attr.name]
                        #print "feature", attr.name, featureValue
                        if featureValue == None:
                            raise InsaneExample("Feature " + attr.name + " was None.")
                        if not isinstance(featureValue, str):
                            if math.isnan(featureValue):
                                raise InsaneExample("Feature " + attr.name + " was not a number.")
                            if math.isinf(featureValue):
                                raise InsaneExample("Feature " + attr.name + " was inf.") 
                        lst.append(featureValue)
                    else:
                        lst.append("")
            ex = orange.Example(self.domain, lst)
            ex['drawMap'] = drawMap
            ex['exceptions'] = exceptions
            ex['situation'] = situation
            ex['engine'] = self
        except InsaneExample, e:
            print "situation", situation
            print "situation as primitives", situation.asPrimitives()
            raise

        return ex, features, drawMap

    
