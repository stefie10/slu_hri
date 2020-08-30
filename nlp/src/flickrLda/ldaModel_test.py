from flickrLda.ldaModel import LdaModel, GibbsLdaRun
from nltk.stem.porter import PorterStemmer
import numpy as na
import unittest

class TestCase(unittest.TestCase):

    def testLoad(self):
        
        model = GibbsLdaRun("data/flickrLda.keywords/model-final")
        
        self.assertEqual(model.phi.shape, (100, len(model.idxToWord)))
        
        idx = 21
        word = model.idxToWord[idx]
        self.assertEqual(model.wordToIdx[word], idx)
        self.assertEqual(model.idxToWord[idx], word)
    
        
    def testLdaLoad(self):
        model = LdaModel("data/flickrLda.keywords/model-final")
        
        lmtzr = PorterStemmer()

        
        def testProb(obj1, obj2):
            
            
            
            #print
            label = "p(%s | %s)" % (obj1, obj2)
            label = label.rjust(60) 
            #print label
            
            #if isinstance(obj1, str):
                #p = model.p_objects_given_obj([obj1], obj2)
                #p = model.p_obj1_given_obj2_marginalize_topics(obj1, obj2)
                #p = model.p_obj1_obj2(obj1, obj2)
                #p = model.p_obj1_given_obj2_posterior(obj1, obj2)
                #p = model.p_obj1_given_obj2_argmax(obj1, obj2)
                #p = model.p_obj1_given_obj2_joint_argmax(obj1, obj2)
                #p = model.p_obj1_given_obj2_joint_marginalize(obj1, obj2)
            #else:
                #   p = model.p_objects_given_obj(obj1, obj2)
                #p = None
                
            if isinstance(obj1, str):
                obj1 = [obj1]
            if isinstance(obj2, str):
                obj2 = [obj2]
            
            obj1 = [lmtzr.stem(t) for t in obj1]
            obj2 = [lmtzr.stem(t) for t in obj2]
                
            #p = model.p_objects_given_obs(obj1, obj2)
            p = model.p_obj1_given_objects_marginalize_topics(obj1[0], obj2)            
            #p = model.p_obj1_given_obj2_marginalize_topics(obj1[0], obj2[0])            
            
                
            print label, p
            return p
        
        testProb("kitchen", "door")
        testProb("kitchen", "window")
        testProb("kitchen", "urinal")        
        testProb("kitchen", "microwave")        
        testProb("kitchen", "refrigerator")
        print        
            
        testProb("view", "door")
        testProb("view", "window")
        testProb("view", "urinal")
        testProb("view", "chair")
        print
        testProb("nice", "door")
        testProb("nice", "window")
        testProb("nice", "urinal")
        testProb("nice", "chair")
        print
        testProb(["nice", "view"], "door")
        testProb(["nice", "view"], "window")
        testProb(["nice", "view"], "urinal")
        
        testProb(["nice", "view"], ["window", "door", "elevator"])
        
        testProb(["coffee"], ["microwave", "refrigerator"])
        #testProb(["coffeemaker"], ["microwave", "refrigerator"])
        testProb(["kitchen"], ["microwave", "refrigerator"])
        testProb(["kitchen"], ["microwave", "refrigerator", "stapler"])
        testProb(["kitchenette"], ["microwave", "refrigerator"])
            
        testProb(["atrium"], ["elevator", "stapler"])
        testProb(["lounge"], ["sofa", "elevator"])
        testProb(["lounge"], ["sofa", "chair"])

        
        print
        testProb("bathroom", "door")
        testProb("bathroom", "window")
        testProb("bathroom", "urinal")
        testProb("bathroom", ["urinal", "sink", "faucet"])
        testProb("bathroom", ["sink"])
        
        urinalId = model.model.wordToIdx["urinal"]
        print "topic", na.argmax(model.model.phi[:, urinalId])

        
        #self.fail()
