import nltk
import agreement
import orange
import orngTest
import orngEnsemble
import orngStat
import orangeUtils
from orangeGui import rocCurve, precisionRecallCurve
import annotation_reader
from environ_vars import TKLIB_HOME
import numpy as na
from  nltk.corpus import wordnet as wn
import matplotlib.pylab as mpl
from physical_objects import get_ancestors
import cPickle
import sys
from memoized import memoize


class WordnetKnnClassifier(orangeUtils.PythonClassifier):
    def __init__(self, training_table, learnweight):
        self.training_table = training_table
        
        self.training_synsets = []
        for t in self.training_table:        
            word = t["word"].value
            synsets = wn.synsets(word.replace(" ", "_"))
            self.training_synsets.append(synsets[0])
    def classify(self, ex):

        word = ex["word"].value
        synset_ex = wn.synsets(word.replace(" ", "_"))[0]
        similarities = [wn.lch_similarity(synset_ex, synset_t) 
                        for synset_t in self.training_synsets]
        cls_i = na.argmax(similarities)
        return self.training_table[cls_i]["class"]

def wordnet_glosses(training, testing):
    stopwords = set(nltk.corpus.stopwords.words())
    gloss_dist = training.gloss_map()
    used_words = [k for k in gloss_dist.keys() 
                  if not k in stopwords and gloss_dist[k] > 2]

    print "words", used_words
    
    attributes = [orange.EnumVariable(a, values=["True", "False"]) 
                  for a in used_words]
    print "got", len(used_words), "features"
    domain = orange.Domain(attributes, training.orange_class_var)


    results = []
    for annotation in [training, testing]:
        table = orange.ExampleTable(domain)
        results.append(table)
        for i, (word, label) in enumerate(annotation.data):
            ancestors = annotation.ancestors(i)
            ex = orange.Example(domain)
            ex["class"] = label
            ex["word"] = word
            for a_i, a in enumerate(attributes):
                word_i = used_words[a_i]
                if word_i in annotation.synset(i).definition:
                    ex[a.name] = "True"
                else:
                    ex[a.name] = "False"
            table.append(ex)

    training_table, testing_table = results
    return training_table, testing_table

def wordnet_meronyms(training, testing):

    ancestor_to_count = training.meronym_ancestor_map()

    all_ancestors = list(ancestor_to_count.keys())
    all_ancestors.sort(key=lambda a: ancestor_to_count[a], 
                       reverse=True)

    used_ancestors = all_ancestors
    print "name", used_ancestors[0].name
    attributes = [orange.EnumVariable(a.name, values=["True", "False"]) 
                  for a in used_ancestors]
    print "got", len(used_ancestors), "features"
    domain = orange.Domain(attributes, training.orange_class_var)

    
    results = []
    for annotation in [training, testing]:
        table = orange.ExampleTable(domain)
        results.append(table)
        for i, (word, label) in enumerate(annotation.data):
            ancestors = annotation.ancestors(i)
            ex = orange.Example(domain)
            ex["class"] = label
            for a_i, a in enumerate(attributes):
                ancestor_i = used_ancestors[a_i]
                if ancestor_i in ancestors:
                    ex[a.name] = "True"
                else:
                    ex[a.name] = "False"
            table.append(ex)

    training_table, testing_table = results
    return training_table, testing_table





def flickr_parents(training, testing):
    flickr = cPickle.load(open("%s/data/directions/breadbox/lmap.pck" % TKLIB_HOME))
    

    ancestor_to_count = training.ancestor_map()

    all_ancestors = list(ancestor_to_count.keys())
    all_ancestors.sort(key=lambda a: ancestor_to_count[a], 
                       reverse=True)

    used_ancestors = all_ancestors
    print "name", used_ancestors[0].name
    attributes = [orange.FloatVariable(a.name +"_flickr")
                  for a in used_ancestors]
    print "got", len(used_ancestors), "features"
    domain = orange.Domain(attributes, training.orange_class_var)

    
    results = []
    for annotation in [training, testing]:
        table = orange.ExampleTable(domain)
        results.append(table)
        for i, (word, label) in enumerate(annotation.data):
            ancestors = annotation.ancestors(i)
            ex = orange.Example(domain)
            ex["class"] = label
            ex["word"] = word
            for a_i, a in enumerate(attributes):
                ancestor_i = used_ancestors[a_i]
                tags = [l.name for l in ancestor_i.lemmas 
                        if flickr.sums[l.name] != 0]
                ex[a.name] = max([flickr.p_obj1_given_obj2(word, l) 
                                  for l in tags] + [0])

            table.append(ex)

    training_table, testing_table = results
    return training_table, testing_table
def build_table(methods, training, testing):
    training_tabs = []
    testing_tabs = []
    #for method in [wordnet_parents, flickr_parents]:
    #[wordnet_parents]:
    
    for method in methods:
        training_tab, testing_tab = method(training, testing)
        training_tabs.append(training_tab)
        testing_tabs.append(testing_tab) 

    print 'args', training_tabs
    training_table = orange.ExampleTable(*training_tabs)
    testing_table = orange.ExampleTable(*testing_tabs)

    return training_table, testing_table

def histogram(annotations):
    width = 0.7
    ylocations = na.arange(len(annotations.labels)) + 0.5
    labels = [l for l in annotations.labels]
    data = [annotations.label_to_count[l] for l in labels]
    rects = mpl.barh(ylocations, data, height=width, align='center')
    mpl.yticks(ylocations, labels)
    mpl.show()

def check_annotations(fname):
    annotations = annotation_reader.from_file(fname)

class WordnetParentsEngine():
    def __init__(self, training):
        self.training = training
        self.ancestor_to_count = training.ancestor_map()


        self.all_ancestors = list(self.ancestor_to_count.keys())
        self.all_ancestors.sort(key=lambda a: self.ancestor_to_count[a], 
                                reverse=True)

        self.used_ancestors = self.all_ancestors
        print "name", self.used_ancestors[0].name
        self.attributes = [orange.EnumVariable(a.name, 
                                               values=["True", "False"]) 
                           for a in self.used_ancestors]
        #self.attributes = [orange.FloatVariable(a.name)
        #                   for a in self.used_ancestors]
        print "got", len(self.used_ancestors), "features"
        self.domain = orange.Domain(self.attributes, training.orange_class_var)
        self.domain.addmeta(orange.newmetaid(), orange.StringVariable("word"))
        table = self.makeTable(self.training)
        self.classifier = orngEnsemble.RandomForestLearner()(table)



    def makeTable(self, annotations):
        table = orange.ExampleTable(self.domain)
        for i, (word, label) in enumerate(annotations.data):
            ex = self.makeExample(word)
            ex["class"] = label
            table.append(ex)
        return table

    @memoize
    def makeExample(self, word):
        ancestors = self.training.ancestors(word)
        ex = orange.Example(self.domain)

        ex["word"] = word
        
        for a_i, a in enumerate(self.attributes):
            ancestor_i = self.used_ancestors[a_i]
            #ex[a.name] = wn.path_similarity(self.training.synset(word), 
            #                                ancestor_i)
            if ancestor_i in ancestors:
                ex[a.name] = "True"
            else:
                ex[a.name] = "False"
        return ex

    def classify(self, word):
        ex = self.makeExample(word)
        result = self.classifier(ex)
        return result.value

def main():
    print "loading"
    annotations = annotation_reader.from_file("%s/data/directions/breadbox/nouns_stefie10.txt" % TKLIB_HOME)
    annotator2 = annotation_reader.from_file("%s/data/directions/breadbox/nouns_dlaude.partial.txt" % TKLIB_HOME)
    #histogram(annotations)
    print "table"
    table = annotations.as_orange_table()
    cv_indices = orange.MakeRandomIndices2(table, p0=0.5)
    print "indices", set(cv_indices)
    print "splitting"
    training, testing = annotation_reader.split(annotations, cv_indices)
    print "features"

    engine = WordnetParentsEngine(training)
    training_table = engine.makeTable(training)
    testing_table = engine.makeTable(testing)
    
    #training_table, testing_table = wordnet_parents(training, testing)
    #training_table, testing_table = wordnet_glosses(training, testing)
    #training_table, testing_table = flickr_parents(training, testing)

    print len(training_table), "training examples"
    print len(testing_table), "testing examples"

    #training_table = annotation_reader.to_big_small(training_table)
    #testing_table = annotation_reader.to_big_small(testing_table)


    #information_gain = orange.MeasureAttribute_info()
    #for x in training_table.domain.attributes:
    #    print "x", information_gain(x, training_table)
    

    learners = [orange.MajorityLearner(),
                orngEnsemble.RandomForestLearner(),
                WordnetKnnClassifier,
                agreement.WizardOfOzLearner(annotator2.as_orange_table())
                ]
    results = orngTest.learnAndTestOnTestData(learners, 
                                              training_table, testing_table)
    for accuracy, cm in zip(orngStat.CA(results),
                            orngStat.confusionMatrices(results)):
        print orangeUtils.confusion_matrix_to_string(table.domain, cm)
        print "accuracy: %.2f%%" % (accuracy*100)


    
if __name__ == "__main__":
    main()    
    
    
