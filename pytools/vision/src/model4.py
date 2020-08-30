#from Inference import *
from BinaryInference import *
from sys import argv
import sys
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
from math import log
from datatypes_lmap import *


class likelihood_map_model4(likelihood_map):

    def get_spatial_factors(self, ind1_fp, obj_names):
        mymap = self.mylogfile.get_map()
        loc1 = self.mylogfile.path_pts_unique[:,ind1_fp]
        ind1 = mymap.to_index(loc1)        
        ind1_neighbors = [[ind1[0]+1, ind1[1]+1], 
                          [ind1[0]+1, ind1[1]-1], 
                          [ind1[0]-1, ind1[1]+1], 
                          [ind1[0]-1, ind1[1]-1], 
                          [ind1[0], ind1[1]+1],
                          [ind1[0], ind1[1]-1], 
                          [ind1[0]+1, ind1[1]],
                          [ind1[0]-1, ind1[1]]]
        #loc1_NN_indexes = kNN_index(loc1, self.mylogfile.path_pts_unique, 9);
        loc1_NN_indexes = self.mylogfile.path_pts_unique_nn[ind1_fp]        

        myfactors = []
        for ind2_fp in loc1_NN_indexes:
            loc2 = self.mylogfile.path_pts_unique[:,ind2_fp]
            ind2 = mymap.to_index(loc2)
            
            if(ind2 in ind1_neighbors and ind2_fp > ind1_fp):
                overlap = self.mylogfile.compute_overlap(loc1, loc2)

                if(overlap < 0.5):
                    overlap = 0.5
                elif(overlap == 1.0):
                    overlap=0.99

                CPD = [[overlap, 1.0-overlap], 
                       [1.0-overlap, overlap]]
                for obj_name in obj_names:
                    #add a factor node
                    #fac = Factor(obj_name+":"+str(int(ind1_fp))+":"+str(int(ind2_fp)), 
                    #             "discrete", [obj_name+":"+str(int(ind1_fp)), 
                    #                          obj_name+":"+str(int(ind2_fp))], CPD)
                    fac = BinaryFactor(obj_name+":"+str(int(ind1_fp))+":"+str(int(ind2_fp)), 
                                       [obj_name+":"+str(int(ind1_fp)), 
                                        obj_name+":"+str(int(ind2_fp))], CPD)
                    myfactors.append(fac)

                '''print "name:", obj_name
                print "ind1:", ind1, " to ind2:", ind2
                print CPD
                print "name: ", obj_name+":"+str(int(ind1_fp))+":"+str(int(ind2_fp))
                raw_input()'''
                    
        return myfactors


    def get_context_factors(self, k, obj_names):

        factors = []
        #print "adding CPDs"
        #add the factors
        for i in range(len(obj_names)):
            for j in range(i+1, len(obj_names)):
                v11 = self.flickr_cache.get_val_exp(obj_names[i], True,  
                                                  obj_names[j], True)
                v22 = self.flickr_cache.get_val_exp(obj_names[i], False, 
                                                  obj_names[j], False)
                v21 = self.flickr_cache.get_val_exp(obj_names[i], False, 
                                                  obj_names[j], True)
                v12 = self.flickr_cache.get_val_exp(obj_names[i], True,  
                                                  obj_names[j], False)
                
                CPD = [[v11, v12],
                       [v21, v22]]
                
                
                fac = BinaryFactor(obj_names[i]+"->"+obj_names[j]+":"+str(int(k)), 
                                   [obj_names[i]+":"+str(int(k)), 
                                    obj_names[j]+":"+str(int(k))], CPD)
                factors.append(fac)

                #print "obj1:", obj_names[i], " -> obj2:", obj_names[j]
                #print CPD
                #raw_input()

        return factors


    def get_detection_factors(self, k, query_object):
        nodes = []
        factors = []

        CPD = [[self.mylogfile.class_tp, 1.0-self.mylogfile.class_tp],
               [1.0-self.mylogfile.class_tn, self.mylogfile.class_tn]]


        #add the factors
        winnum = 0
        curr_detections = self.mylogfile.detections[k]

        #if there aren't any detections, then use the tn rate of the classifier 
        #                and observe no detections
        if(len(curr_detections) == 0):
            fac1 = BinaryFactor(query_object+"_ev_nodetect:"+str(int(k)),
                                [query_object+":"+str(int(k))], 
                                [1.0-self.mylogfile.class_tn, self.mylogfile.class_tn])
            return [], [fac1]

        #if there are detections, then use the tp rate of the classifier here
        for elt in curr_detections:
            #create a window node
            mynode = BinaryNode(query_object+"_window("+str(winnum)+"):"+str(int(k)))

            #create a factor from the window node to the whether or not the object exists
            fac1 = BinaryFactor(query_object+"_fac_window("+str(winnum)+"):"+str(int(k)),
                               [query_object+":"+str(int(k)), 
                                query_object+"_window("+str(winnum)+"):"+str(int(k))], CPD)
            
            #print "CPD:", CPD

            #now add in the detection likelihood according to Pablo's approach
            fac2 = BinaryFactor(query_object+"_ev_window("+str(winnum)+"):"+str(int(k)),
                                [query_object+"_window("+str(winnum)+"):"+str(int(k))], 
                                [elt['prob_fin'], 1.0-elt['prob_fin']])

            #print "ev:", [elt['prob_fin'], 1.0-elt['prob_fin']]
            
            nodes.append(mynode)
            factors.append(fac1)
            factors.append(fac2)
            winnum+=1
            
            #raw_input()

        return nodes, factors
                
    def get_observation_factors(self, query_object, vpolygons):
        #print "adding observations"
        m = 0
        myfacs = []
        
        for vpolys in vpolygons:
            visible_objects = []
            for elt in vpolys:
                if(elt.tag in self.known_classes 
                   and not elt.tag in visible_objects
                   and not elt.tag == query_object):
                    #print "adding pos for ", elt.tag
                    ev_vo = [self.mylogfile.tp, 1.0-self.mylogfile.tp]
                    myev_fac = BinaryFactor(elt.tag+"_ev:"+str(int(m)), 
                                            [elt.tag+":"+str(int(m))], ev_vo)
                    myfacs.append(myev_fac)
                    visible_objects.append(elt.tag)
        
            #add observations for those things not seen
            for elt in self.known_classes:

                if(not elt in visible_objects and not elt == query_object):
                    #print "adding neg for ", elt
                    ev_ivo = [1.0-self.mylogfile.tn, self.mylogfile.tn]
                    myev_fac = BinaryFactor(elt+"_ev:"+str(int(m)), 
                                            [elt+":"+str(int(m))], ev_ivo)
                    myfacs.append(myev_fac)

            m+=1

        return myfacs


    def perform_inference(self):
        #if there are none
        if(self.my_inference == None):
            return
        obj_names = self.object_names
        for elt in self.known_classes:
            if(not elt in obj_names):
                obj_names.append(elt)

        for obj_name in obj_names:
            self.likelihood_map[obj_name] = []

        #observed = {}
        print "running bp"
        self.my_inference.run_belief_propagation()
        
        print "appending marginals"
        for mykey in self.hidden_nodes.keys():
            for j in range(len(self.hidden_nodes[mykey])):
                print "performing inference for ", mykey, " at loc ", j

                probs = self.my_inference.marginal(self.hidden_nodes[mykey][j])             

                try:
                    self.likelihood_map[mykey].append(probs[0])
                except(KeyError):
                    self.likelihood_map[mykey] = []
                    self.likelihood_map[mykey].append(probs[0])
                

    def create_model(self):
        query_object = self.mylogfile.det_type 

        if(len(self.mylogfile.path_pts_unique) == 0):
            return

        #when we iterate through them
        obj_names = self.object_names

        #append all of the objects 
        for elt in self.known_classes:
            if(not elt in obj_names):
                obj_names.append(elt)
        
        #then remove the one that we're able to detect
        #obj_names.remove(self.mylogfile.det_type)

        #now compute the model
        vpolygons = self.mylogfile.visible_objects

        print "computing posterior"
        self.my_inference, self.hidden_nodes = self.create_model_rec(query_object, 
                                                                     obj_names, 
                                                                     vpolygons)

    #this should jointly compute the likelihood of all the
    #   classes at this location.  Use the graphical model
    #   toolbox that I've created.
    def create_model_rec(self, query_object, obj_names, vpolygons):
        
        print "obj_names", obj_names
        print "self.known_classes", self.known_classes

        for obj_name in obj_names:
            if(not obj_name in self.flickr_cache.tagnames):
                print self.flickr_cache.tagnames
                print "bad context name:"+obj_name
                sys.exit(0)

        print "creating inference and adding nodes"
        self.my_inference = BinaryInference(self.num_bp_iterations)
        
        self.hidden_nodes = {}
        mynode = None
        
        self.hidden_nodes[query_object] = []
        #add nodes for the query object
        for i in range(len(self.mylogfile.path_pts_unique[0])):
            #real nodes
            mynode = BinaryNode(query_object+":"+str(int(i)))
            
            self.my_inference.addNode(mynode)
            self.hidden_nodes[query_object].append(mynode)

        #add the nodes
        for oname in obj_names:

            if(oname == query_object):
                continue
            
            print "creating ", oname, " nodes"
            self.hidden_nodes[oname] = []
            for i in range(len(self.mylogfile.path_pts_unique[0])):
                #real nodes
                mynode = BinaryNode(oname+":"+str(int(i)))

                self.my_inference.addNode(mynode)
                self.hidden_nodes[oname].append(mynode)
                

        print "adding spatial and contexutal factors"
        #add the location-based and then spatial factors
        for k in range(len(self.mylogfile.path_pts_unique[0])):
            print k, " of ", len(self.mylogfile.path_pts_unique[0])
            
            print "getting spatial factors"
            my_spatial_facs = self.get_spatial_factors(k, obj_names)
            
            print "getting context factors"
            my_context_facs = self.get_context_factors(k, obj_names)
            
            print "adding factors"
            for elt in my_spatial_facs:
                self.my_inference.addNode(elt)
            for elt in my_context_facs:
                self.my_inference.addNode(elt)


        #add in the actual detections from the classifier outputs
        for k in range(len(self.mylogfile.path_pts_unique[0])):
            my_det_nodes, my_det_facs = self.get_detection_factors(k, query_object)
            
            for elt in my_det_nodes:
                self.my_inference.addNode(elt)
            for elt in my_det_facs:
                self.my_inference.addNode(elt)

        print "adding observations"
        #add the observations
        #    vpolygons is meant to be indexed by location in free_pts
        my_observation_facs = self.get_observation_factors(query_object, vpolygons)
        for elt in my_observation_facs:
            self.my_inference.addNode(elt)




        
                
        return self.my_inference, self.hidden_nodes
    
