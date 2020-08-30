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


class likelihood_map_model6(likelihood_map):

    def get_spatial_factors(self, ind1_fp, obj_names, orientation, fov):
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
        loc1_NN_indexes = self.mylogfile.path_pts_unique_nn[ind1_fp]        

        myfactors = []
        for ind2_fp in loc1_NN_indexes:
            loc2 = self.mylogfile.path_pts_unique[:,ind2_fp]
            ind2 = mymap.to_index(loc2)
            
            if(ind2 in ind1_neighbors and ind2_fp > ind1_fp):

                overlap = self.mylogfile.compute_overlap_orient(loc1, loc2, orientation, fov)

                #testoverlap = self.mylogfile.compute_overlap(loc1, loc2)
                #print "overlap old:", testoverlap
                #print "overlap new:", overlap
                #raw_input()
                
                if(overlap < 0.5):
                    overlap = 0.5
                elif(overlap == 1.0):
                    overlap=0.99

                CPD = [[overlap, 1.0-overlap], 
                       [1.0-overlap, overlap]]
                for obj_name in obj_names:
                    #add a factor node
                    fac = BinaryFactor(obj_name+":"+str(int(ind1_fp))+":"+str(int(ind2_fp)), 
                                       [obj_name+":"+str(int(ind1_fp)), 
                                        obj_name+":"+str(int(ind2_fp))], CPD)
                    myfactors.append(fac)

        return myfactors


    def get_context_factors(self, k, obj_names):
        mypt = self.mylogfile.path_pts_unique[:,k]
        factors = []
        
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

        return factors
                
    def get_observation_factors(self, det_classes, vpolygons, det_configs):
        print "adding observations"
        m = 0
        myfacs = []
        
        for vpolys in vpolygons:
            visible_objects = []
            for elt in vpolys:
                if(elt.tag in det_classes
                   and not elt.tag in visible_objects):
                    #print "adding observation of ", elt.tag
                    ev_vo = [det_configs[elt.tag]["tp"], 1.0-det_configs[elt.tag]["tp"]]

                    myev_fac = BinaryFactor(elt.tag+"_ev:"+str(int(m)), 
                                            [elt.tag+":"+str(int(m))], ev_vo)
                    myfacs.append(myev_fac)
                    visible_objects.append(elt.tag)
        
            #add observations for those things not seen
            for elt in det_classes:
                if(not elt in visible_objects):
                    ev_ivo = [1.0-det_configs[elt]["tn"], det_configs[elt]["tn"]]
                    myev_fac = BinaryFactor(elt+"_ev:"+str(int(m)), 
                                            [elt+":"+str(int(m))], ev_ivo)
                    myfacs.append(myev_fac)
            
            m+=1

        return myfacs


    def perform_inference(self):
        
        self.likelihood_map0 = self.perform_inference_orient(0)
        self.likelihood_map90 = self.perform_inference_orient(pi/2.0)
        self.likelihood_map180 = self.perform_inference_orient(pi)
        self.likelihood_map270 = self.perform_inference_orient((3*pi)/2.0)

    def perform_inference_orient(self, orient):
        if(orient == 0):
            my_inference = self.my_inference0
            hidden_nodes = self.hidden_nodes0
        elif(orient == pi/2.0):
            my_inference = self.my_inference90
            hidden_nodes = self.hidden_nodes90
        elif(orient == pi):
            my_inference = self.my_inference180
            hidden_nodes = self.hidden_nodes180
        elif(orient == (3*pi)/2.0):
            my_inference = self.my_inference270
            hidden_nodes = self.hidden_nodes270

        #if there are none

        if(my_inference == None):
            return
        obj_names = self.object_names
        for elt in self.known_classes:
            if(not elt in obj_names):
                obj_names.append(elt)

        likelihood_map = {}
        for obj_name in obj_names:
            likelihood_map[obj_name] = []

        print "running bp"
        my_inference.run_belief_propagation()
        
        print "appending marginals"
        for mykey in hidden_nodes.keys():
            for j in range(len(hidden_nodes[mykey])):
                print "performing inference for ", mykey, " at loc ", j
                
                probs = my_inference.marginal(hidden_nodes[mykey][j])             

                try:
                    likelihood_map[mykey].append(probs[0])
                except(KeyError):
                    likelihood_map[mykey] = []
                    likelihood_map[mykey].append(probs[0])

        return likelihood_map
                

    def create_model(self, pdetect_files):
        if(len(self.mylogfile.path_pts_unique) == 0):
            return
        
        configs = {}
        for myfile in pdetect_files:
            myhash, myhash_joint, config = load_pclassfile(myfile)
            configs[config["name"]] = config

        print "computing posterior"
        self.my_inference0, self.hidden_nodes0=self.create_model_rec(configs, 
                                                                     self.mylogfile.vobjs0, 
                                                                     0)
        self.my_inference90, self.hidden_nodes90=self.create_model_rec(configs, 
                                                                       self.mylogfile.vobjs90, 
                                                                       pi/2.0)
        self.my_inference180, self.hidden_nodes180=self.create_model_rec(configs, 
                                                                         self.mylogfile.vobjs180, 
                                                                         pi)
        self.my_inference270, self.hidden_nodes270=self.create_model_rec(configs, 
                                                                         self.mylogfile.vobjs270, 
                                                                         (3.0*pi)/2.0)
        

    #this should jointly compute the likelihood of all the
    #   classes at this location.  Use the graphical model
    #   toolbox that I've created.
    def create_model_rec(self, det_configs, vpolygons, orientation):

        det_names = []
        for name in det_configs.keys():
            det_names.append(name)
            if(not name in self.flickr_cache.tagnames):
                print self.flickr_cache.tagnames
                print "bad context name:"+name
                sys.exit(0)

        print "creating inference and adding nodes"
        self.my_inference = BinaryInference(self.num_bp_iterations)
        self.hidden_nodes = {}
        mynode = None
        
        #add the nodes
        for oname in det_configs.keys():
            print "creating ", oname, " nodes"
            self.hidden_nodes[oname] = []
            for i in range(len(self.mylogfile.path_pts_unique[0])):
                #real nodes
                mynode = BinaryNode(oname+":"+str(int(i)))
                
                self.my_inference.addNode(mynode)
                self.hidden_nodes[oname].append(mynode)
        
        print "adding observations"
        #add the observations
        #    vpolygons is meant to be indexed by location in free_pts
        my_observation_facs = self.get_observation_factors(det_names, vpolygons, det_configs)
        for elt in my_observation_facs:
            self.my_inference.addNode(elt)

        print "adding spatial and contexutal factors"
        #add the location-based and then spatial factors
        for k in range(len(self.mylogfile.path_pts_unique[0])):
            print k, " of ", len(self.mylogfile.path_pts_unique[0])
            
            print "getting spatial factors"
            my_spatial_facs = self.get_spatial_factors(k, det_names, 
                                                       orientation, pi/2.0)
            
            print "getting context factors"
            my_context_facs = self.get_context_factors(k, det_names)
            
            print "adding factors"
            for elt in my_spatial_facs:
                self.my_inference.addNode(elt)
            for elt in my_context_facs:
                self.my_inference.addNode(elt)
        
        #perform the inference
        #print "performing inference"
        #observed = {}
        #for i in hidden_nodes:
        #    self.my_inference.infType = "BP"
        #    probs1 = self.my_inference.marginal([i], observed)

        print "done"
        return self.my_inference, self.hidden_nodes
    
