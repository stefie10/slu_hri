from BinaryInference import *
from Inference import *
from sys import argv
import sys
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
from math import log
from datatypes_lmap import *


class likelihood_map_model2(likelihood_map):
    
    def perform_inference(self):
        
        self.inference_cache = {}
        self.known_classes.sort()
        
        obj_names = self.object_names
        
        for obj_name in obj_names:
            self.likelihood_map[obj_name] = []
        
        #if there are none
        if(len(self.mylogfile.path_pts_unique) == 0):
            return

        #when we iterate through them
        for i in range(len(self.mylogfile.path_pts_unique[0])):
            vobjs = self.mylogfile.visible_objects[i]

            myvobjs = []
            for elt in vobjs:
                if(elt.tag in self.known_classes 
                   and not (elt.tag in myvobjs)):
                    myvobjs.append(elt.tag)
            myvobjs.sort()

            
            inference = None; mynodes = None;
            #if we've seen these observations, then just get the inference
            print myvobjs
            try: 
                inference, mynodes = self.inference_cache[str(myvobjs)]
            except(KeyError):
                #compute the posterior
                inference, mynodes = self.create_model(obj_names, vobjs)
                inference.run_belief_propagation()
                self.inference_cache[str(myvobjs)] = [inference, mynodes]
            
            
            print "************"
            for j in range(len(mynodes)):
                print "appending to lmap for", mynodes[j].name
                probs = inference.marginal(mynodes[j])
                self.likelihood_map[mynodes[j].name].append(probs[0])
                del probs 

            print "i=", i,  " of ", len(self.mylogfile.path_pts_unique[0]), " grid cells"
            del inference, mynodes, vobjs
            

    #this should jointly compute the likelihood of all the
    #   classes at this location.  Use the graphical model
    #   toolbox that I've created.
    def create_model(self, obj_names, vpolygons):
        
        for obj_name in obj_names:
            if(not obj_name in self.flickr_cache.tagnames):
                print self.flickr_cache.tagnames
                print "bad context name:"+obj_name
                sys.exit(0)

        myinf = BinaryInference(50)
        #myinf = Inference("BP", 50)
        
        hidden_nodes = []
        mynode = None
        #add the nodes
        for oname in obj_names:
            #real nodes
            mynode = BinaryNode(oname)
            #mynode = Node(oname, "discrete", [0,1])
            myinf.addNode(mynode)  
            hidden_nodes.append(mynode)

        #add the factors
        for i in range(len(obj_names)):
            for j in range(i+1, len(obj_names)):
            
                #print "obj_names[j]", obj_names[j]

                #try:
                v11 = self.flickr_cache.get_val_exp(obj_names[i],True,  obj_names[j], True)
                v22 = self.flickr_cache.get_val_exp(obj_names[i],False, obj_names[j], False)
                v21 = self.flickr_cache.get_val_exp(obj_names[i],False, obj_names[j], True)
                v12 = self.flickr_cache.get_val_exp(obj_names[i],True,  obj_names[j], False)
                #except(KeyError):
                #    continue
                
                CPD = [[v11, v12],
                       [v21, v22]]


                #print "CPD "+obj_names[i] + " -> " + obj_names[j]              
                #print CPD 

                fac = BinaryFactor(obj_names[i]+"->"+obj_names[j], 
                                   [obj_names[i], obj_names[j]], CPD)

                #fac = Factor(obj_names[i]+"->"+obj_names[j], "discrete",
                #             [obj_names[i], obj_names[j]], CPD)
                myinf.addNode(fac)
                del fac, v11, v12, v21, v22, CPD

            #raw_input()

        #print "adding observations"
        #add the observations
        visible_objects = []
        for elt in vpolygons:
            if(elt.tag in self.known_classes and not elt.tag in visible_objects):
                print "adding observation of ", elt.tag
                ev_vo = [self.mylogfile.tp, (1.0-self.mylogfile.tp)]
                myev_fac = BinaryFactor(elt.tag+"_ev", [elt.tag], ev_vo)
                #myev_fac = Factor(elt.tag+"_ev", "discrete", [elt.tag], ev_vo)
                myinf.addNode(myev_fac)
                visible_objects.append(elt.tag)

                del ev_vo, myev_fac
        
        #print "adding observations 2"
        #add observations for those things not seen
        invisible_objects = []
        for elt in obj_names:
            if(not elt in visible_objects and elt in self.known_classes 
               and not elt in invisible_objects):
                print "adding inobservation of ", elt
                ev_ivo = [(1.0-self.mylogfile.tn), (self.mylogfile.tn)]
                myev_fac = BinaryFactor(elt+"_ev", [elt], ev_ivo)
                #myev_fac = Factor(elt+"_ev", "discrete", [elt], ev_ivo)
                myinf.addNode(myev_fac)
                invisible_objects.append(elt)
                
                del ev_ivo, myev_fac

        del visible_objects, invisible_objects

        return myinf, hidden_nodes
