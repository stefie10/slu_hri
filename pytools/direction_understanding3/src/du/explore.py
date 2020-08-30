from pyTklib import kNN_index
from scipy import transpose, zeros, argmax
from copy import deepcopy
from scipy import radians
#from math import radians


class explore:
    def __init__(self, dg_model):
        self.dg_model = dg_model
      
        self.tmap = dg_model.tmap
        self.tmap_keys = dg_model.tmap_keys
        self.tmap_locs = dg_model.tmap_locs
        self.num_viewpoints = dg_model.num_viewpoints

        get_viewpoint_orientations = self.dg_model.get_viewpoint_orientations 
        
    def infer_path_incremental(self):
        ret_vals = self.dg_model.infer_path(self.sdcs, self.sloc, self.orient)
        self.dg_model.set_topo_map(self.tmap_orig)
        
        return ret_vals

    def initialize(self, sloc, orient_rad):
        self.tmap_orig = deepcopy(self.dg_model.tmap)
        
        self.allowed_topologies = []
        self.visited_frontiers = []

        #append the starting topology
        i, = kNN_index(sloc, transpose(self.dg_model.tmap_locs.values()), 1)
        mytopo_i = self.dg_model.tmap_locs.keys()[int(i)]
        self.allowed_topologies.append(mytopo_i)
        self.allowed_topologies.extend(list(self.tmap_orig[mytopo_i]))
        self.visited_frontiers.append(mytopo_i)
        self.sdcs = []

        #self.orient = radians(orient_deg)
        self.orient = orient_rad
        self.sloc = sloc
        
    def add_sdc(self, sdc):
        self.sdcs.append(sdc)

        #create the correct topological map
        tmap_new = self.tmap_mask(self.tmap_orig, self.allowed_topologies)
            
        #set the topological map in the model
        self.dg_model.set_topo_map(tmap_new)            

        #give the current number of sdcs
        curr_sdcs = self.sdcs

        self.dg_model.initialize_transition_matrices()

        #infer the best destinations
        dest, prob, sdcs_u, probs = self.dg_model.infer_destination(self.sdcs, 
                                                                    self.sloc, 
                                                                    self.orient)

        dest, prob, afront = self.get_best_frontier(self.dg_model, 
                                                    tmap_new, probs, 
                                                    self.visited_frontiers)
        
        mydest = float(dest[0].split("_")[0])
        mydest_orient = radians(float(dest[0].split("_")[1]))

        #print "mydest", mydest
        #print "allowed_topo:", self.allowed_topologies

        if(not mydest in tmap_new.keys()):
            print "probability", prob
            print tmap_new
            raise KeyError("Bad key value")

        self.visited_frontiers.append(mydest)
        self.allowed_topologies.extend(self.tmap_orig[mydest])
        
        #self.tmap_locs[i]
        allowed_locs = [self.dg_model.tmap_locs[mykey] 
                        for mykey in self.allowed_topologies]

        allowed_front = [self.dg_model.tmap_locs[mykey] 
                         for mykey in afront]
        
        #put the orientation together with the destination
        fin_dest = self.dg_model.tmap_locs[mydest].tolist()
        fin_dest.append(mydest_orient)
        return fin_dest, allowed_locs, allowed_front
    

    def tmap_mask(self, tmap, mask):
        tmap_new = {}
        
        #iterate through the from keys and check feasibility
        for key_from in tmap.keys():
            if key_from in mask:
                #iterate through the to keys and check feasibility
                for key_to in tmap[key_from]:
                    if(key_to == key_from):
                        tmap_new[key_from] = []                        
                    elif(key_to in mask):
                        try:
                            tmap_new[key_from].append(key_to)
                        except(KeyError):
                            tmap_new[key_from] = [key_to]

            else:
                tmap_new[key_from] = []

        return tmap_new

    def get_best_frontier(self, dg_model, tmap, probs, visited_topos):
        
        #topo_sing = self.get_singly_connected_topologies(tmap)
        topo_sing = tmap.keys()
        
        orients = dg_model.get_viewpoint_orientations(dg_model.num_viewpoints)
        mymask = zeros(len(dg_model.viewpoints))*1.0

        allowed_frontiers = []
        for topo in topo_sing:
            if(topo in visited_topos):
                continue

            allowed_frontiers.append(topo)
            
            for orient in orients:
                #print "topo:", topo
                #print "adding option for:",str(topo) + "_"+ str(orient), " -->prob:", probs[i]
                i = dg_model.vpt_to_num[str(topo)+"_"+str(orient)]
                mymask[i] = 1.0 
        
        
        new_probs = probs*mymask

        print "old max prob", max(probs)
        print "new max prob:", max(new_probs)
        return [dg_model.viewpoints[argmax(new_probs)]], new_probs[argmax(new_probs)], allowed_frontiers


'''    #def infer_path(self, sdcs, loc, sorient_rad=None):
    def infer_path(self, sdcs, sloc, orient):

        tmap_orig = deepcopy(self.dg_model.tmap)

        allowed_topologies = []
        visited_frontiers = []

        #append the starting topology
        i, = kNN_index(sloc, transpose(self.dg_model.tmap_locs.values()), 1)
        mytopo_i = self.dg_model.tmap_locs.keys()[int(i)]
        allowed_topologies.append(mytopo_i)
        allowed_topologies.extend(list(tmap_orig[mytopo_i]))
        visited_frontiers.append(mytopo_i)
        
        for i in range(len(sdcs)):
            #create the correct topological map
            tmap_new = self.tmap_mask(tmap_orig, allowed_topologies)
            
            #set the topological map in the model
            self.dg_model.set_topo_map(tmap_new)            
            
            #give the current number of sdcs
            curr_sdcs = sdcs[0:i+1]
            
            self.dg_model.initialize_transition_matrices()
            
            #infer the best destinations
            dest, prob, sdcs_u, probs = self.dg_model.infer_destination(sdcs, sloc, orient)
            dest, prob = self.get_best_frontier(self.dg_model, tmap_new, probs, visited_frontiers)
            
            mydest = float(dest[0].split("_")[0])
            
            print "mydest", mydest
            print "allowed_topo:", allowed_topologies
            
            if(not mydest in tmap_new.keys()):
                print "probability", prob
                print tmap_new
                raise KeyError("Bad key value")

            visited_frontiers.append(mydest)
            allowed_topologies.extend(tmap_orig[mydest])
            
        ret_vals = self.dg_model.infer_path(sdcs, sloc, orient)
        self.dg_model.set_topo_map(tmap_orig)
        
        return ret_vals'''
