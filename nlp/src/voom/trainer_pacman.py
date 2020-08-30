'''
Created on Dec 22, 2009

@author: stefie10
'''
from environ_vars import TKLIB_HOME
from orangeGui import rocCurve
from orangeUtils import displayResults
from orngBayes import BayesLearner
from orngEnsemble import RandomForestLearner
from voom import verb_classifier
from voom.gui.assignments.assignmentData import Assignment
from voom.verbs import bring, follow, meet, avoid
import cPickle
import cProfile
import carmen_map_skeletonizer
import itertools
import matplotlib
import orange
import orangeGui
import orangeUtils
import orngTest
import pylab as mpl
import tag_util
import time

def versionOne():
    return cPickle.load(open("%s/nlp/data/engines.verbs.floor3.stefie10.pck" % TKLIB_HOME, "r"))
    
def saveClassifiers():
    import psyco
    map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
    cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
    gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
    
    assignment_fns = ["%s/nlp/data/aaai_2010_smv/stefie10/assignment1.1.yaml" % TKLIB_HOME,
                      "%s/nlp/data/aaai_2010_smv/stefie10/assignment1.2.yaml" % TKLIB_HOME,
                      "%s/nlp/data/aaai_2010_smv/stefie10/assignment2.1.yaml" % TKLIB_HOME,
                      "%s/nlp/data/aaai_2010_smv/tkollar/assignment3.1.yaml" % TKLIB_HOME,
                      ]

    tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
    tagFile.get_map()
    tagFile.get_tag_names()
    
    #print cluster_fn
    #raw_input()
    skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)
    assignments = [Assignment.load(fn, tagFile, skeleton)for  fn in assignment_fns]
    #classifiers = makeClassifiers(assignment)
    result = []
    def run():
        classifiers = makeClassifiers(assignments)
        result.append(classifiers)
        

    start = time.time()
    cProfile.runctx("run()", globals(), locals(), "profile.out")
    end = time.time()
    print "took", (end - start)/60., "minutes"
    classifiers = result[0]    
    fname = "%s/nlp/data/engines.verbs.floor3.stefie10.pck" % TKLIB_HOME
    cPickle.dump(classifiers, open(fname, "w"))
    print "wrote", fname
    
    #testingAssignment = Assignment.load("%s/nlp/data/aaai_2010_smv/stefie10/assignment1.1.yaml" % TKLIB_HOME, tagFile, skeleton)
    #testingAssignment = Assignment.load("%s/nlp/data/aaai_2010_smv/tkollar/assignment3.1.yaml" % TKLIB_HOME, tagFile, skeleton)
    testingAssignment = Assignment.load("%s/nlp/data/aaai_2010_smv/stefie10/assignment4.1.yaml" % TKLIB_HOME, tagFile, skeleton)    
    
    for name, c in classifiers.iteritems():
        engine = c.engine
        testing = makeTable(engine, [testingAssignment])
        results = orngTest.testOnData([c.classifier], testing)
        mpl.figure()
        line, = orangeGui.rocCurve(results, engine.name, stepSize=0.001, marker="x", plotArgs=dict(color="k"))
        
        mpl.title(engine.name.capitalize(), fontsize=30)
        mpl.xlabel("TP")
        mpl.ylabel("FP")
        mpl.xticks([0, 1], fontsize=20)
        mpl.yticks([0, 1], fontsize=20)
        line.set_label(engine.name.upper())
        mpl.savefig("roc.%s.png" % engine.name)
        orangeUtils.displayResults(results)
    #mpl.legend(loc="lower right")
    #mpl.title("Classifiers for Verbs")
    mpl.show()



def makeTable(engine, assignments):
    negativeMap = {"bring":["avoid", "meet","follow"],
                   "follow":["bring", "meet", "avoid"],
                   "meet":["follow", "avoid"],
                   "avoid":["bring", "follow", "meet"],
                   "go":["wander"],
                   "wander":["bring", "follow", "avoid"],
                   }
    out = orange.ExampleTable(engine.domain)
    for assignment in assignments:
        negativeVerbs = negativeMap[engine.name]
        table = makeTableFromEntries(engine, assignment.entriesForVerb(engine.name),
                                     itertools.chain(*[assignment.entriesForVerb(v) for v in negativeVerbs]))
        out.extend(table)
    return out
     
def makeTableFromEntries(engine, positiveEntries, negativeEntries):
    table = orange.ExampleTable(engine.domain)
    print "engine", engine.name
    for entry in positiveEntries:
        try:
            ex = engine.makeExample(entry.situation)
            ex["verbclass"] = "True"
            ex["description"] = entry.verb
            ex["entry"] = entry
            table.append(ex)
        except:
            print "was doing", entry.command
            raise   
    for entry in negativeEntries:
        try:
            ex = engine.makeExample(entry.situation)
            ex["verbclass"] = "False"
            ex["description"] = entry.verb
            ex["entry"] = entry
            table.append(ex)
        except:
            print "was doing", entry.command
            raise
        
    return table


def makeClassifiers(assignments):    
    engineMap = dict((x.name, x) for x in 
                     [bring.Engine(), 
                      follow.Engine(), 
                      meet.Engine(), 
                      avoid.Engine(), 
                      #wander.Engine(), 
                      #go.Engine()
                    ])    
    classifiers =  {}
    for engine in engineMap.values():
        verb = engine.name
        if verb != "follow":
            #continue
            pass
        table = orange.ExampleTable(engine.domain)
        for a in assignments:
            try:
                table.extend(makeTable(engine, [a]))
                table.extend(makeSubsetExamples(engine, table))
            except:
                print "exception on", a.fname
                raise
        #classifiers[engine.name] = verb_classifier.Classifier(engine, RandomForestLearner(table))
        classifiers[engine.name] = verb_classifier.Classifier(engine, BayesLearner(table))
    return classifiers

def makeSubsetExamples(engine, table):
            
    if engine.isLiquid:
        verbclass = "True"
    else:
        verbclass = "False"

    print "making subset, **************"
    outputTable = orange.ExampleTable(table.domain)
    for ex in table:
        if ex["verbclass"] == "True" and engine.isLiquid:
            assert engine == ex["engine"].value
            thisentry =  ex["entry"].value
            situation = ex["situation"].value
            #for windowSize in [10*1000, 5*1000, 2*1000]:
            for windowSize in [10*1000, 5*1000]:
                for t in range (situation.startTime,
                                situation.endTime - windowSize, windowSize/3):
                    newSituation = situation.subset(t, t + windowSize)
                    newex = engine.makeExample(newSituation)
                    newex["verbclass"] = verbclass
                    newex["entry"] = thisentry
                    outputTable.append(newex)
    return outputTable

def testFeatureSubsets(engine, training, testing):
    lines = []

    def doRun(title, newDomain, learner, training, testing, marker):
        newTraining = orangeUtils.convertTable(training, newDomain)
        newTesting = orangeUtils.convertTable(testing, newDomain)

        classifier = learner(newTraining)
        results = orngTest.testOnData([classifier], testing, storeClassifiers=1)
        
        print "title", title
        displayResults(results)    
        line, = rocCurve(results, title, stepSize=0.001, marker=marker)
        line.set_label(title)
        lines.append(line)

        return results
    
    learner = RandomForestLearner()
    domain = engine.domain
    doRun("All Features", domain, learner, training, testing, marker='p')
    
    attributes = [x for x in domain.attributes
                  if x.name in ("IsClose('figure','landmark')","averageDifferenceInAngle",
                                "stdDevOfDistance")]
    attributeSubsets = [[x] for x in attributes]
    for i, x in enumerate(attributes):
        for y in attributes[i:]:
            if x != y:
                attributeSubsets.append([x, y])
                #pass
    for i, attributes in enumerate(attributeSubsets):
        #mpl.figure()
        newDomain = orange.Domain(attributes, domain.classVar)
        newDomain.addmetas(domain.getmetas())

        idx = i % len(matplotlib.lines.Line2D.filled_markers)
        title = ",".join([x.name for x in attributes])
        doRun(title, newDomain, learner, training, testing, 
              marker=matplotlib.lines.Line2D.filled_markers[idx])


    mpl.legend(loc="lower right")
    


def main():
    from sys import argv
        
    map_fn = argv[1]
    gtruth_tag_fn = argv[2]
    cluster_fn = argv[3]
    assignment_fns = argv[4:]
    tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
    tagFile.get_map()
    tagFile.get_tag_names()
    
    
    skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)

    assignments = [Assignment.load(assignment_fn, tagFile, skeleton) for assignment_fn 
                   in assignment_fns]
    
    engineMap = dict((x.name, x) for x in
                     [bring.Engine(), 
                      follow.Engine(), 
                      meet.Engine(), 
                      avoid.Engine(), 
                      #wander.Engine(), 
                      #go.Engine(),
                      ])
    
    
    for engine in engineMap.values():
        verb = engine.name
        if verb != "follow" and False:
            continue
        

        def run():
            return makeTable(engine, assignments)
        #cProfile.runctx("run()", globals(), locals(), "profile.out")
        #return
        table = run()
        print "verb", verb, len(table)  
    
        cv_indices = orange.MakeRandomIndicesCV(table, 2)
        humanLabeledTraining = table.select(cv_indices, 0)
        training = orange.ExampleTable(humanLabeledTraining.domain)
        training.extend(humanLabeledTraining)
        generatedTraining = makeSubsetExamples(engine, humanLabeledTraining)
        training.extend(generatedTraining)
        
        print "Using", len(generatedTraining), "subset examples"
        
        testing = table.select(cv_indices, 1)
        
        #testFeatureSubsets(engine, training, testing)
        
        #classifier  = orngBayes.BayesLearner(training)
        classifier  = RandomForestLearner(training)
        results = orngTest.testOnData([classifier], testing)
        print "results", results
        tuples = list(zip(testing, results.results))
        tuples.sort(key=lambda x: x[0]["description"])
        for e, r in tuples:
#            print e["description"], e["hasApproach"], e["hasFollow"],
            if r.actualClass == r.classes[0]:
                print "correct", e["description"], e["entry"].value.id 
            else:
                print "incorrect", e["description"], e["entry"].value.id 

        mpl.figure(figsize=(6,6))
        mpl.subplots_adjust(bottom=0.13)
        line, = orangeGui.rocCurve(results, engine.name, stepSize=0.001,
                                   plotArgs={"color":"black"})

        orangeUtils.displayResults(results)
        mpl.xlabel("FP", fontsize=32)
        mpl.ylabel("TP", fontsize=32)
        mpl.xticks((0, 1), fontsize=20)
        mpl.yticks((0, 1), fontsize=20)
        line.set_label(engine.name)
        mpl.title(engine.name.capitalize(), fontsize=32)
        mpl.savefig("roc_%s.png" % engine.name)
        mpl.savefig("roc_%s.ps" % engine.name)
    mpl.show()
    
    
if __name__ == "__main__":
    main()
