from os.path import dirname
import math
import numpy as na


class LdaModel:
    """
    We have the overall topic model trained on flickr.
    And also the query model trained on all the possible queries we might see.
    """
    def __init__(self, model_fname):
        self.model = GibbsLdaRun(model_fname)

    def p_topic_given_objects(self, objects):
        r = na.ones(self.model.num_topics)
        
        for obj in objects:
            r = r * self.p_topic_given_obj(obj)
        r = r / na.sum(r)
        return r
    
    def p_objects_given_obs(self, objects, observations):
        p_topic = [self.p_topic_given_obj(o) for o in observations]
        
        p_topic = na.prod(p_topic, axis=0)
            
        p_objects = [self.model.phi[:, self.model.wordToIdx[o]] for o in objects]
        p_objects = na.prod(p_objects, axis=0)
        return na.sum(p_topic * p_objects)
    
    def p_objects_given_obj(self, objects, obj2):
        p_topic_given_obj2 = self.p_topic_given_obj(obj2)
        
        p_objects_given_topic = na.ones(self.model.num_topics)
        
        for o in objects:
            wordId = self.model.wordToIdx[o]
            p_o_given_obj = self.model.phi[:, wordId]
            p_objects_given_topic = p_objects_given_topic * p_o_given_obj
            
        return na.sum(p_objects_given_topic * p_topic_given_obj2)
        
    def p_topic_given_obj(self, obj):
        wordId = self.model.wordToIdx[obj]
        p_obj_given_topic = self.model.phi[:, wordId]
        
        denom = na.sum(p_obj_given_topic)
        
        return p_obj_given_topic / denom
        
        
        
    def p_obj1_given_obj2_joint_marginalize(self, obj1, obj2):
        p_topics = self.p_topic_given_obj(obj1) * self.p_topic_given_obj(obj2)
        word1Id = self.model.wordToIdx[obj1]    
        return na.sum(p_topics  * self.model.phi[:, word1Id])        
                
    def p_obj1_given_obj2_joint_argmax(self, obj1, obj2):
        p_topics = self.p_topic_given_obj(obj1) * self.p_topic_given_obj(obj2)
        
        topic = na.argmax(p_topics)
        
        print 'topic', topic
        word1Id = self.model.wordToIdx[obj1]    
        return self.model.phi[topic, word1Id]

                
    def p_obj1_given_obj2_argmax(self, obj1, obj2):
        p_topic_given_obj2 = self.p_topic_given_obj(obj2)
        
        topic = na.argmax(p_topic_given_obj2)
        print "topic", topic
        word1Id = self.model.wordToIdx[obj1]    
        p_obj1_given_topic = self.model.phi[topic, word1Id]
        return p_obj1_given_topic 
        
    def p_obj1_given_objects_marginalize_topics(self, obj1, objects):
        p_topics = self.p_topic_given_objects(objects)
        total = na.sum(p_topics)
        assert math.fabs(total - 1.0) < 0.00000000001, total
        
        word1Id = self.model.wordToIdx[obj1]
   
        p_obj1_given_topic = self.model.phi[:, word1Id]    
        
        return na.sum(p_obj1_given_topic * p_topics)
        
    
    def p_obj1_given_obj2_marginalize_topics(self, obj1, obj2):
        p_topic_given_obj2 = self.p_topic_given_obj(obj2)
        
        total = na.sum(p_topic_given_obj2)
        assert math.fabs(total - 1.0) < 0.00000000001, total
        
        word1Id = self.model.wordToIdx[obj1]
   
        p_obj1_given_topic = self.model.phi[:, word1Id]    
        
        return na.sum(p_obj1_given_topic * p_topic_given_obj2)

    def p_obj1_given_obj2_posterior(self, obj1, obj2):
        word1Id = self.model.wordToIdx[obj1]
        docId = self.queries.documentToIdx[frozenset([obj2])]
        
        p_topic_given_doc = self.queries.theta[docId]
        return na.sum(p_topic_given_doc * self.model.phi[:, word1Id])
        
                
    def p_obj1_obj2(self, obj1, obj2):
        word1Id = self.model.wordToIdx[obj1]
        word2Id = self.model.wordToIdx[obj2]

        return na.sum(self.model.phi[:, word1Id] * self.model.phi[:, word2Id])
    
    def logLiklihood(self):
        print "docs", len(self.model.documents)
        print "theta", len(self.model.theta)
        lp = 0
        for i, d in enumerate(self.model.documents):
            lp_doc = 0
            for word in d:
                wordId = self.model.wordToIdx[word]
                p_word = self.model.phi[:, wordId] * self.model.theta[i]
                lp_word = na.log(na.sum(p_word))
                lp_doc += lp_word
            lp += lp_doc
            #if i % 1000 == 0:
            #    print "document", i, lp
        return lp
        
         
    
    
class GibbsLdaRun:
    def __init__(self, model_fname, wordmap_fname=None, document_fname=None):
        self.model_fname = model_fname
        if wordmap_fname == None:
            self.wordmap_fname = dirname(self.model_fname) + "/wordmap.txt"
        else:
            self.wordmap_fname= wordmap_fname
            
        if document_fname == None:
            self.document_fname = dirname(self.model_fname) + "/flickrLda.dat"

        self._idxToWord = None
        self._wordToIdx = None
        
        self._documents = None
        self._documentToIdx = None
        
        self._num_topics = None
        
    @property
    def num_topics(self):
        if self._num_topics != None:
            self.loadDocuments()
            self._num_topics = len(self.phi)
        return self._num_topics
    
        
    @property
    def documents(self):
        if self._documents == None:
            self.loadDocuments()
        return self._documents

    @property
    def documentToIdx(self):
        if self._documentToIdx == None:
            self.loadDocuments()
        return self._documentToIdx
    
    
    def loadDocuments(self):
        file = open(self.document_fname, "r")
        numdocs = int(file.readline())
        documents = []
        for docline in file:
            doc = set([x.strip() for x in docline.split()])
            documents.append(doc)
        self._documents = documents            
        self._documentToIdx = dict([(frozenset(d), i) for i, d in enumerate(self._documents)])
        

    @property
    def idxToWord(self):
        if self._idxToWord == None:
            self.initializeWordmap()
        return self._idxToWord
    
    @property    
    def wordToIdx(self):
        if self._wordToIdx == None:
            self.initializeWordmap()
        return self._wordToIdx

    
        
    @property
    def phi(self):
        self.phi = self.loadPhi(self.model_fname  + ".phi")
        return self.phi
        
        
    @property
    def theta(self):
        self.theta = self.loadTheta(self.model_fname + ".theta")
        return self.theta
    
    def loadTheta(self, theta_fname):
        file = open(theta_fname, "r")
        theta = []
        for docLine in file:
            thetaLine =[float(x) for x in docLine.split()]
            theta.append(thetaLine)
        return na.array(theta)
    
    
       
       
    def initializeWordmap(self):
        self._idxToWord = self.loadWordmap(self.wordmap_fname)
        self._wordToIdx = dict((word, idx) for idx, word in enumerate(self.idxToWord))
        
    def loadWordmap(self, wordmap_fname=None):
        file = open(wordmap_fname, "r")
        size = int(file.readline())
        wordmap = [None for x in range(size)]
        
        for i, line in enumerate(file):
            word, idx = line.split()
            idx = int(idx)
            wordmap[idx]  = word
        
        for i, w in enumerate(wordmap):
            assert w != None, i    
        return wordmap
    
    def loadPhi(self, phi_fname):
        file = open(phi_fname, "r")
        
        phi = []
        for topicLine in file:
            topicProbs = [float(s) for s in topicLine.split()]
            phi.append(topicProbs)
            
        return na.array(phi)
    
