from glob import glob
import cPickle
from scipy import mod
from scipy import ones
from copy import deepcopy
import orange
import orngTest, orngBayes, orngTree, orngSVM, orngEnsemble
from scipy import array, transpose


def get_train_test_documents_esp(directory, dataset_type="esp", 
                                 max_entries=500000, known_objects=set([]), start_image=0):
    if(dataset_type == "flickr"):
        myfiles = glob(directory+'FlickrNotes/*/*_tags.txt')
    elif(dataset_type=="esp"):
        myfiles = glob(directory+'labels/*.desc')
    
    print "taking images:", start_image, " to ", start_image+max_entries
    myfiles = myfiles[start_image:start_image+max_entries]
    
    prior_cache = {}
    word_to_document_hash={}

    print "parsing files"
    D = []
    docs_index = 0
    for i, file in enumerate(myfiles):
        if(mod(i, 1000) == 0):
            print i, 'of', len(myfiles)

        #if(i > max_entries):
        #    break

        objs = []
        ofile = open(file, 'r')
        
        
        words = []
        w_in_set = False
        for line in ofile:
            word = line.strip().lower()
            if(word in known_objects or len(known_objects) == 0):
                w_in_set = True
            words.append(word)
        if(not w_in_set):
            continue
        
        for word in words:            
            obj = word
            if(obj != ''):
                objs.append(obj)
            if(not prior_cache.has_key(obj)):
                prior_cache[obj] = {}

            if(not word_to_document_hash.has_key(obj)):
                word_to_document_hash[obj] = [docs_index]
            else:
                word_to_document_hash[obj].append(docs_index)

        docs_index+=1
        D.append(objs)
        
    print "adding objects for ", len(D), "files"
    for i, objs in enumerate(D):
        if(mod(i, 1000) == 0):
            print i, "of", len(D)
        
        for obj1 in objs:
            for obj2 in objs:
                if(obj1 != obj2):
                    if(prior_cache[obj1].has_key(obj2)):
                        prior_cache[obj1][obj2] += 1
                    else:
                        prior_cache[obj1][obj2] = 1

                    if(prior_cache[obj2].has_key(obj1)):
                        prior_cache[obj2][obj1] += 1
                    else:
                        prior_cache[obj2][obj1] = 1

    return D, prior_cache, word_to_document_hash



class cooccurrence:
    def __init__(self, esp_dirname, known_objects, dataset_type="esp", max_entries=500000):

        self.esp_dirname = esp_dirname
        self.documents, self.cooccurrence_mat, self.w_to_doc = get_train_test_documents_esp(esp_dirname, dataset_type, 
                                                                                            max_entries, known_objects)
        
        self.known_objects = known_objects
        
        print "get subset"
        self.documents_redux_I = self.get_keyword_subset_I()
        
        print len(self.documents)
        print len(self.documents)


        self.domain = None
        self.classifiers = {}
        
    def get_keyword_subset_I(self):
        docs_redux = set([])
        for i, elt in enumerate(self.known_objects):
            try:
                docs_redux = docs_redux.union(set(self.w_to_doc[elt]))
            except(KeyError):
                pass
        
        return list(docs_redux)
    
    def train(self, keyword, learner="svm"):
        training_docs, test_docs, train_label, test_label = self.get_training_test_sets(keyword, 0.8)
        
        if(len(train_label) == 0):
            return None

        F_train = []
        print "--------------TRAIN:", keyword , "-------------------"
        for i, doc_i in enumerate(training_docs):
            #print self.documents[i]
            myfeatures = self.get_features(keyword, self.documents[doc_i])
            if(not '1' in myfeatures):
                continue
            
            
            myfeatures.append(str(int(train_label[i])))
            F_train.append(myfeatures)
            
        if(len(F_train) == 0):
            return None
        
        #create the attributes and domain
        table = orange.ExampleTable(self.get_domain())
        
        #define the rest of the table by addign elements to it
        for i in range(len(F_train)):
            #print self.known_objects
            #print "i=", i
            #print "ftrain[i]", zip(self.known_objects, F_train[i]), 
            #print " label[i]", train_label[i]
            #F_train[i].append(str(int(train_label[i])))
            table.append(F_train[i])
            
            
        #perform the learning

        if(learner == "bayes"):
            print "running bayes"
            classifier = orngBayes.BayesLearner(table)
            #classifier = orngBayes.BayesLearner(table, m=2)
        elif(learner == "tree"):
            print "running tree"
            classifier = orngTree.TreeLearner(table)
        elif(learner == "svm"):
            #can't load the svmlearner
            print "running svm"
            classifier = orngSVM.SVMLearner(table, svm_type=orange.SVMLearner.Nu_SVC, 
                                            nu=0.3, probability=True)
        elif(learner == "boosting"):
            #problem here too
            #this is meant to be adaboost
            classifier = orngTree.BoostedLearner(table) 
        elif(learner == "randomforest"):
            #problem here too 
            classifier = orngEnsemble.RandomForestLearner(table, 
                                                          trees=50, name="forest")

        else:
            print "unknown learner"
            raise
        
        return classifier
    

    def get_domain(self):
        if(self.domain != None):
            return self.domain
        
        values = ["0", "1"]
        mynames = self.known_objects
        attributes = [orange.EnumVariable(mynames[i], values = values)
                      for i in range(len(mynames))]
        classattr = orange.EnumVariable("classname", values = ["-1", "0", "1"])
        self.domain = orange.Domain(attributes + [classattr])
        
        return self.domain


    def predict(self, query_word, document, learner="svm"):
        if(not self.classifiers.has_key(query_word)):
            classifier = self.train(query_word, learner=learner)
            self.classifiers[query_word] = classifier
        
        if(self.classifiers[query_word] == None):
            return None

        f = self.get_features(query_word, document)
        if(not "1" in f):
            return None
        
        f.append("1")

        ex = orange.Example(self.get_domain(), f)

        #orngBayes.printModel(self.classifiers[query_word])
        results = self.classifiers[query_word](ex, orange.GetBoth)

        return results

    
    def get_training_test_sets(self, keyword, train_percentage):
        if(not self.w_to_doc.has_key(keyword)):
            return [],[],[],[]
        
        docs_rel = self.w_to_doc[keyword]
        
        docs_irrel = deepcopy(self.documents_redux_I)

        #print docs_irrel
        
        for i in docs_rel:
            #print "i", i
            try:
                docs_irrel.remove(i)
            except(ValueError):
                pass
        
        
        #add the relevant documents
        training = docs_rel[0:int(train_percentage*len(docs_rel))]
        test = docs_rel[int(train_percentage*len(docs_rel)):]

        #create the labels
        training_labels = list(ones(len(training)))
        test_labels = list(ones(len(test)))
        training_labels.extend(-1*ones(len(docs_irrel[0:len(training)])))
        test_labels.extend(-1*ones(len(docs_irrel[0:len(test)])))
        
        #append the rest of the data
        training.extend(docs_irrel[0:len(training)])
        test.extend(docs_irrel[0:len(test)])
        
        return training, test, training_labels, test_labels


    def get_features(self, query_word, document):
        F = []
        
        for elt in self.known_objects:
            if(query_word == elt):
                F.append(str(0))
            elif(elt in document):
                try:
                    num_elts = self.cooccurrence_mat[query_word][elt]
                    #F.append(num_elts)
                    if(num_elts > 0):
                        F.append(str(1))

                except(KeyError):
                    F.append(str(0))
            else:
                F.append(str(0))

        return F

        

        

        


#results = orngTest.testOnData([self.classifiers[query_word]], table)
#print dir(results.results[0])
#print results.results[0].actualClass
#print results.results[0].probabilities
#print results.results[0].classes[0]
        
