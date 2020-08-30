#from Inference import *
from BinaryInference import *
from sys import argv
from copy import deepcopy
import sys
import cPickle
from pyTklib import *
from scipy import array, zeros, argmax
from pylab import *
from math import atan2, sqrt, log

class model1_qanswer:
    
    def __init__(self, flickr_cache, categories):
        self.flickr_cache = flickr_cache
        self.olist = categories
        
        self.query_object = "kitchen"
        self.visible_objects = ["refrigerator", "sink", "soap", 
                                "faucet", "mug", "cup", "plate"]

        self.tp = 0.9; self.tn = 0.9
        self.allowed_objects = []

    #this should jointly compute the likelihood of all the
    #   classes at this location.  Use the graphical model
    #   toolbox that I've created.
    def create_model(self, question="", qvalue=True):
        print "*******************************"
        print "creating model"
        for obj_name in self.olist:
            if(not obj_name in self.flickr_cache.tagnames):
                print self.flickr_cache.tagnames
                print "bad context name:"+obj_name
                sys.exit(0)

        myinf = BinaryInference(len(self.olist))
        
        hidden_nodes = []
        mynode = None
        #add the nodes
        for oname in self.olist:
            #real nodes
            mynode = BinaryNode(oname)
            myinf.addNode(mynode)  
            hidden_nodes.append(mynode)

        #add the factors
        for i in range(len(self.olist)):
            for j in range(i+1, len(self.olist)):
                v11 = self.flickr_cache.get_val_exp(self.olist[i],True,  self.olist[j], True)
                v22 = self.flickr_cache.get_val_exp(self.olist[i],False, self.olist[j], False)
                v21 = self.flickr_cache.get_val_exp(self.olist[i],False, self.olist[j], True)
                v12 = self.flickr_cache.get_val_exp(self.olist[i],True,  self.olist[j], False)
                
                CPD = [[v11, v12],
                       [v21, v22]]


                fac = BinaryFactor(self.olist[i]+"->"+self.olist[j], 
                                   [self.olist[i], self.olist[j]], CPD)

                if(self.olist[i] == 'kitchen' or self.olist[j] == 'kitchen'):
                    print self.olist[i], "-->", self.olist[j]
                    print CPD
                    myinf.addNode(fac)
                del fac, v11, v12, v21, v22, CPD

        #raw_input()
                
        allowed_obj_curr = deepcopy(self.allowed_objects)

        if(question != "" and not question in allowed_obj_curr):
            allowed_obj_curr.append(question)

        for elt in allowed_obj_curr:
            if(elt == question and qvalue == True):
                print "adding", elt, True
                ev_vo = [self.tp, (1.0-self.tp)]
                myev_fac = BinaryFactor(elt+"_ev", [elt], ev_vo)
                print ev_vo
                myinf.addNode(myev_fac)
            elif(elt == question and qvalue == False):
                print "adding", elt, False
                ev_ivo = [(1.0-self.tn), (self.tn)]
                myev_fac = BinaryFactor(elt+"_ev", [elt], ev_ivo)
                print ev_ivo
                myinf.addNode(myev_fac)
            elif(elt in self.visible_objects):
                print "adding", elt
                ev_vo = [self.tp, (1.0-self.tp)]
                myev_fac = BinaryFactor(elt+"_ev", [elt], ev_vo)
                myinf.addNode(myev_fac)
                print ev_vo
                del ev_vo, myev_fac
            else:
                print "adding", elt
                ev_ivo = [(1.0-self.tn), (self.tn)]
                myev_fac = BinaryFactor(elt+"_ev", [elt], ev_ivo)
                print ev_ivo
                myinf.addNode(myev_fac)
                del ev_ivo, myev_fac            


        #raw_input()
        #raw_input("model created")
        return myinf, hidden_nodes

    def add_allowed_object(self, name):
        if(not name in self.allowed_objects):
            self.allowed_objects.append(name)
        
    def delete_allowed_object(self, name):
        self.allowed_objects.remove(name)

    def perform_inference(self, question="", qval=True):
        probs = {}
        
        #compute the posterior
        inference, mynodes = self.create_model(question, qval)
        inference.run_belief_propagation()
        
        #print "************"
        for j in range(len(mynodes)):
            #print "appending to lmap for", mynodes[j].name
            myprob = inference.marginal(mynodes[j])
            probs[mynodes[j].name] = myprob[0]
            del myprob

        return probs

    def maximal_information_gain(self):
        
        Igain = []
        P_t = []
        P_f = []
        myolist = []

        #if(True):
        #    return self.olist, Igain, P_t, P_f

        probs_before = self.perform_inference()
        
        for elt in self.olist:
            if(elt == self.query_object):
                continue

            print self.allowed_objects
            probs_after_T = self.perform_inference(elt, True)
            probs_after_F = self.perform_inference(elt, False)
            
            #now we need to compute P(X)
            p_b = probs_before[self.query_object]
            p_aT = probs_after_T[self.query_object]
            p_aF = probs_after_F[self.query_object]
            
            print "question:", elt
            print "p_before", p_b
            print "p_after_T", p_aT
            print "p_after_F", p_aF
            HY = -1.0*(p_b*log(p_b) + (1.0-p_b)*log(1.0-p_b))
            HYX_T = -1.0*(p_aT*log(p_aT) + (1-p_aT)*log(1.0-p_aT))
            HYX_F = -1.0*(p_aF*log(p_aF) + (1-p_aF)*log(1.0-p_aF))
            
            
            print "entropy before:", HY
            print "entropy after T:", HYX_T
            print "entropy after F:", HYX_F
            
            I = HY - 0.5*HYX_T - 0.5*HYX_F
            Igain.append(I)
            P_t.append(p_aT)
            P_f.append(p_aF)
            myolist.append(elt)
            
            print "object:", self.query_object
            print "information gain", I
    
            raw_input()
        return myolist, Igain, P_t, P_f



def load_location_file(locations_filename):
    loc_file = open(locations_filename, 'r')

    locations = []
    for line in loc_file:
        locations.append(line.strip())
    return locations

def run_model1_qa(objects_filename, flickr_cache):
    
    #load a location file
    loc_info = load_location_file(objects_filename);
    
    #create a likelihood map
    l_map = model1_qanswer(flickr_cache, loc_info)

    olists, igains, p_ts, p_fs = [], [], [], []

    for k in range(5):
        olist, igain, p_t, p_f = l_map.maximal_information_gain()

        olists.append(olist);
        igains.append(igain)
        p_ts.append(p_t)
        p_fs.append(p_f)
        
        for i in range(len(igain)):
            print "obj:", olist[i], " I:", igain[i], " P(t):", p_t[i], " P(f):", p_f[i]

                     
        if(len(igain) == 0):
            j = -1
        else:
            j = argmax(igain)
        
        if(not j == -1):
            print "adding allowed object:", olist[j]
            l_map.add_allowed_object(olist[j])
            print "best=", olist[j]
    
    res = {}
    res['object_lists'] = olists
    res['information_gain'] = igains
    res['prob_true'] = p_ts
    res['prob_false'] = p_fs
    cPickle.dump(res, open('m1_qanswer.pck', 'w'))


if __name__=="__main__":
    if(len(argv) == 3):
        print "loading prior"
        run_model1_qa(argv[1], cPickle.load(open(argv[2], 'r')))

            
    else:
        print "usage:\n\t python run_model1.py loc_filename flickr_cache.pck"



