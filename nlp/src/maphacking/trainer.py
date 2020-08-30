from orangeGui import rocCurve
from orangeUtils import displayResults
#import pickle
import cPickle as pickle
import math2d
import numpy as na
import orange
import orngBayes
import orngTest
import orngStat
from slimd import preposition, down, across, towards, along, around, awayFrom, out, past, through, to, until
import pylab as mpl
import spatialRelationClassifier
from environ_vars import TKLIB_HOME
import sys
mpl.rcParams.update({'font.family':'serif',})
from slimd import orangePickle
        

def printClassProbs(classifier):
    nValues=len(classifier.classVar.values)
    frmtStr=' %10.3f'*nValues
    classes=" "*20+ ((' %10s'*nValues) % tuple([i[:10] for i in classifier.classVar.values]))
    print classes
    print "class probabilities "+(frmtStr % tuple(classifier.distribution))
    print


def createLandmarkPt(point, isDoor=False):
    if isDoor:
        return boundingBox(point, width=0.5)
    else:
        return boundingBox(point, width=0.1)

def boundingBox(point, width=0.1):
    point = na.array(point)
    return na.array([point+[-width, -width],
                     point+[-width, width],
                     point+[width, width],
                     point+[width, -width]]).tolist()


skipMap = {
    "to":["towards", "until"],
    "through":["across", "down"],
    "across":["through"],
    "along":["down"],
    "down":["along", "through", "out", "across"],
    "towards":["to", "until"],
    "until":["towards", "to"],
    "around":[]
}

def makeTable(data, engine, tagLayer, useFarAway=False):
    table = orange.ExampleTable(engine.domain())
    if engine.name() in skipMap:
        skipList = skipMap[engine.name()]
    else:
        skipList = []

    labeledCount = 0
    negativeCount = 0
    farAwayCount = 0
    for engineName, landmarkName, geometry in data:
        
        #geometry["landmark"] = createLandmarkPt(math2d.centroid(geometry["landmark"]))

        if not (engineName in skipList): # or True:

            try:
                geometry["landmark"] = geometry["ground"]
                ex = engine.makeExample(**geometry)
            except preposition.InsaneExample:
                continue
            except:
                print "dc", engineName
                print "dc", geometry
                print "dc", landmarkName
                raise
            if engineName == engine.name():
                if engineName == "down" and False:
                    print "doing down differently"
                    if landmarkName == "hallway":
                        cls = "True"
                        labeledCount += 1
                    else:
                        continue
                        #cls = "False"
                        #negativeCount -= 1
                else:
                    cls = "True"
                    labeledCount += 1
            else:
                cls = "False"
                negativeCount += 1
            ex['class'] = cls
            ex['sourceEngineName'] = engineName
            ex['engineName'] = engine.name()
            ex['landmarkName'] = landmarkName
            ex['farAway'] = False
            table.append(ex)
    if useFarAway and engine.name() != "through" and engine.name() != "down":
        for name, landmark in tagLayer:
            centroid1 = math2d.centroid(landmark)
            for engineName, landmarkName, geometry in data:
                if engineName == engine.name():
                    centroid2 = math2d.centroid(geometry["landmark"])
                    d1 = math2d.dist(centroid1, centroid2)
                    d2 = math2d.length(geometry["figure"])
                    if d1 > d2:
                        ex = engine.makeExample(figure=geometry["figure"],
                                                landmark=landmark)
                        ex['class'] = "False"
                        ex['landmarkName'] = landmarkName
                        ex['sourceEngineName'] = engineName
                        ex['engineName'] = engine.name()
                        ex['farAway'] = True
                        table.append(ex)
                        farAwayCount += 1
                        if farAwayCount >= 100:
                            break
    for ex in table:
        ex['drawMap'] = None
        #ex['geometry'] = None

    print "counts"
    print labeledCount, "labeled examples."
    print negativeCount, "negative examples."
    print farAwayCount, "far away examples."
        
    return table

class Trainer:
    def __init__(self):
        self.trainingData = []
        self.engineMap = spatialRelationClassifier.liveEngineMap
        self.annotationEngines = set()
        self.tagLayer = pickle.load(open("%s/nlp/data/floor3.examples/tagLayer.pck" % TKLIB_HOME))
        for session in ["%s/nlp/data/floor3.examples/part1.pck" % TKLIB_HOME, 
                        "%s/nlp/data/floor3.examples/part2.pck" % TKLIB_HOME,
                        "%s/nlp/data/floor3.examples/part3.pck" % TKLIB_HOME,
                        ]:
            stuff = pickle.load(open(session))
            self.trainingData.extend(stuff)
            for engine, landmarkName, data in stuff:
                self.annotationEngines.add(engine)



    def makeTable(self, engine, trainingData=None, useFarAway=True):
        if trainingData == None:
            trainingData = self.trainingData
        return makeTable(trainingData, engine,
                         self.tagLayer, useFarAway=useFarAway)
    def configureClassifier(self, engine):
        data = self.makeTable(engine)
        engine._classifier = orangePickle.PickleableClassifier(data, 
                                                               #orange.LogRegLearner)
                                                               orngBayes.BayesLearner)
        return data
        
def pickleClassifiers():
    print "entering pickle"
    trainer = Trainer()
    classifierMap = {}
    for i, (key, engine) in enumerate(trainer.engineMap.iteritems()):
        print "doing", engine.name()
        #if engine.name() != "towards":
        #    continue

        if engine.name() in trainer.annotationEngines:
            trainer.configureClassifier(engine)
        else:
            print "warning,No " + `engine.name()` + " in " + `trainer.annotationEngines`

        classifierMap[key] = engine       
    outfile = open("data/engines.floor3.stefie10.pck", "wb")
    pickle.dump(classifierMap, outfile, protocol=0)
    outfile.close()
        
def load(files):
    trainingData = []
    annotationEngines = set()
    
    tagLayer = pickle.load(open("%s/nlp/data/floor3.examples/tagLayer.pck" % TKLIB_HOME))
    
    
    for session in files:
        stuff = pickle.load(open(session))
        for engineName, landmarkName, data in stuff:
            annotationEngines.add(engineName)
        trainingData.extend(data)
    return trainingData, annotationEngines, tagLayer

def ablateFeatures():
    ablateFeaturesForCls(across.Across)
    ablateFeaturesForCls(along.Along)
    ablateFeaturesForCls(around.Around)
    ablateFeaturesForCls(awayFrom.AwayFrom)
    ablateFeaturesForCls(down.Down)
    ablateFeaturesForCls(out.Out)
    ablateFeaturesForCls(past.Past)
    ablateFeaturesForCls(through.Through)
    ablateFeaturesForCls(to.To)
    ablateFeaturesForCls(towards.Towards)
    ablateFeaturesForCls(until.Until)
    mpl.show()



def ablateFeaturesForCls(engineCls):
    mpl.figure()
    trainer = Trainer()
    engine = engineCls()
    trainer.configureClassifier(engine)
    markers = ['.', ',','v','^','<','>','1','2','3','4','s','p','*','h','H',]
    colors = ["b", "g", "r", "c","m", "y"]
    
    sub_engines = []
    for i, name in enumerate(sorted(engine.masterList)):
        sub_engine = engineCls()
        sub_engine.setFeatureList([name])
        sub_engines.append((name, sub_engine))

    markers = markers[0:len(sub_engines)]
    colors = colors[0:len(sub_engines)]
    sub_engines.append(("all", engineCls()))
    markers.append("o")
    colors.append("k")



    for i, (name, sub_engine) in enumerate(sub_engines):
        table = trainer.configureClassifier(sub_engine)
        cv_indices = orange.MakeRandomIndices2(table, p0=0.75)

        training = table.select(cv_indices, 0, negate=True)
        testing = table.select(cv_indices, 0, negate=False)

        #classifier = orange.LogRegLearner(training)
        classifier = orngBayes.BayesLearner(training)
        results = orngTest.testOnData([classifier], testing)
        displayResults(results)

        line = rocCurve(results, "", stepSize=0.001,
                        marker=markers[i % len(markers)],
                        plotArgs=dict(linewidth=5, markersize=10,
                                      color=colors[i % len(colors)]),)


        line[0].set_label(name)

    mpl.title(engine.name(), size=30)
    mpl.xlabel("FP", fontsize=30)
    mpl.ylabel("TP", fontsize=30)
    mpl.xticks([0,1], fontsize=17)
    mpl.yticks([0,1], fontsize=17)
    mpl.subplots_adjust(bottom=0.14, top=0.91)
    mpl.legend(loc="lower right", prop=dict(size=17))
    mpl.savefig("roc.ablate.%s.png" % engine.name())



def smallRocCurve():

    trainer = Trainer()


    keys = None
    keys = None
    #keys = ["towards"]
    for i, key in enumerate(trainer.annotationEngines):
        if keys != None and not key in keys:
            continue
            
        print "*****************************************************"
        print key
        engine = trainer.engineMap[key]
        mpl.figure(figsize=(8,8))
        print "training"
        table = trainer.makeTable(engine)
        cv_indices = orange.MakeRandomIndices2(table, p0=0.75)

        training = table.select(cv_indices, 0, negate=True)
        testing = table.select(cv_indices, 0, negate=False)        


        classifier = orangePickle.PickleableClassifier(training, 
                                                       orngBayes.BayesLearner)
                                                       #orange.LogRegLearner)
        results = orngTest.testOnData([classifier], testing)

        displayResults(results)    

        line = rocCurve(results, "", stepSize=0.001, marker=".",
                        plotArgs=dict(linewidth=5))

        line[0].set_label(engine.name())
        mpl.xlabel("FP", fontsize=25)
        mpl.ylabel("TP", fontsize=25)
        mpl.xticks([0,1], fontsize=20)
        mpl.yticks([0,1], fontsize=20)
        ax = mpl.gca()
        ax.set_aspect(1./ax.get_data_ratio())
        mpl.title(engine.name().capitalize(), fontsize=30)
        #mpl.legend(loc='lower right', prop=FontProperties(size=25))
        mpl.savefig("roc.%s.png" % engine.name())

    mpl.show()


def make_example_nway(geometry, trainer, domain):
    ex = orange.Example(domain)
    geometry["landmark"] = geometry["ground"]
    examples = [trainer.engineMap[key].makeExample(expectInsane=True,
                                                   **geometry)
                     for key in trainer.annotationEngines 
                if not len(geometry["figure"]) == 0]
    for engine_ex in examples:
        for attr in engine_ex.domain:
            ex[attr.name] = engine_ex[attr.name]
    return ex
def nway():
    engine_to_examples = {}

    trainer = Trainer()
    classes = set()
    for i, key in enumerate(trainer.annotationEngines):
        engine = trainer.engineMap[key]
        table = trainer.makeTable(engine)

        for ex in table:
            if ex["farAway"].value:
                cls = "null"
            else:
                cls = ex["sourceEngineName"].value
            geometry = ex["geometry"].value
            engine_to_examples.setdefault(cls, [])


            classes.add(cls)
        
            examples = [trainer.engineMap[key].makeExample(expectInsane=True,
                                                           **geometry
                                                             ) 
                        for key in trainer.annotationEngines if not len(geometry["figure"]) == 0]

            engine_to_examples[cls].append(examples)
           
        if i >= 1:
            #break
            pass
    variables = []
    for ex in examples:
        for attr in ex.domain:
            if attr.name == "class":
                continue
            new_attr = orange.FloatVariable(attr.name)
            variables.append(new_attr)
    domain = orange.Domain(variables, 
                           orange.EnumVariable("class", 
                                               values=list(classes)))
    table = orange.ExampleTable(domain)
    for engine_name, example_lists in engine_to_examples.iteritems():
        for example_list in example_lists:
            ex = orange.Example(domain)
            for engine_ex in example_list:
                for attr in engine_ex.domain:
                    ex[attr.name] = engine_ex[attr.name]
            ex["class"] = engine_name
            table.append(ex)
    print "domain", domain
    

    cv_indices = orange.MakeRandomIndices2(table, p0=0.75)

    training = table.select(cv_indices, 0, negate=True)
    testing = table.select(cv_indices, 0, negate=False)
    #classifier = orngBayes.BayesLearner(training)

    classifier = orangePickle.PickleableClassifier(training,
                                                   orngBayes.BayesLearner)
    

    results = orngTest.testOnData([classifier], testing)
    print orngStat.CA(results)
    cm = orngStat.confusionMatrices(results)[0]
    classes = list(domain.classVar.values)
    print "           ", " ".join([c.rjust(12) for c in classes + ["", ""]])
    for className, classConfusions in zip(classes, cm): 
        #format = ("%s" + ("\t%i" * len(classes)))
        values = (className, ) + tuple(classConfusions) 
        print " ".join([str(c).rjust(12) for c in values])
        #print  format % values

    for name in classes:
        classIndex = classes.index(name)
        mpl.figure()
        rocCurve(results, "", classIndex, stepSize=0.001, 
                 plotArgs=dict(linewidth=5, markersize=10))
        mpl.title(name, size=30)
        mpl.xlabel("FP", fontsize=30)
        mpl.ylabel("TP", fontsize=30)
        mpl.xticks([0,1], fontsize=17)
        mpl.yticks([0,1], fontsize=17)
    fname = "nway.pck"
    print "saving", fname
    with open(fname, "w") as f:
        pickle.dump(classifier, f, protocol=2)
    mpl.show()
    

if __name__ == "__main__":
    from sys import argv
    command = argv[1]
    if command == "pickle":
        pickleClassifiers()
    elif command == "plot":
        #unifiedRocCurve()
        smallRocCurve()
    elif command == "ablate":
        ablateFeatures()
    elif command == "nway":
        nway()
    else:        
        raise ValueError("Bad command:" + `sys.argv`)
    #smallRocCurve()
    
