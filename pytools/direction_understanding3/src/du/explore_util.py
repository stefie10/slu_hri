from copy import deepcopy
import copy as cpcp
from du.dir_util import direction_parser_wizard_of_oz, direction_parser_sdc
from du.eval_util import get_region_to_topo_hash_containment, \
    get_topological_paths_hash, get_output_filename, string_edit_distance
from du.eval_util import get_orientations_each, get_orientations_all, get_orientations_annotated
from du.srel_utils import ProcessPool
from numpy import argmax, copy, zeros, radians, transpose
from numpy import *
from pyTklib import kNN_index
from routeDirectionCorpusReader import readSession
from tag_util import tag_file
import cPickle
import os
import time


def infer_explore(dg_model, sdcs, sloc, orient, num_explorations, heuristic_name, params_num):
    dg_model_cp = cpcp.copy(dg_model)
    tmap_orig = deepcopy(dg_model_cp.tmap)
    dg_model_cp.tmap = tmap_orig

    allowed_topologies = []
    visited_frontiers = []
    visited_viewpoints = []

    heuristic_map = {"step":heuristic_step, "stairs":heuristic_stairs, "lifted_stairs":heuristic_lifted_stairs, "slope_offset_delay":heuristic_SOD, "frontier":heuristic_frontier}
    heuristic = heuristic_map[heuristic_name]
    
    #append the starting topology
    i, = kNN_index(sloc, transpose(dg_model_cp.tmap_locs.values()), 1)
    mytopo_i = dg_model_cp.tmap_locs.keys()[int(i)]
#    print "initial topology: ",mytopo_i  
    allowed_topologies.append(mytopo_i)
    allowed_topologies.extend(list(tmap_orig[mytopo_i]))
#    print "allowed topologies: ",allowed_topologies 
    visited_frontiers.append(mytopo_i)

    SOD_default = (0.5,1,1)


    num_sdcs = len(sdcs)
    
    hpar = h_param()
    hpar.num_sdcs = num_sdcs
    
    if params_num in [None, ""]:
        params_num = SOD_default

    
    hpar.SOD = params_num
    slope = params_num[0]
    offset = params_num[1]
    delay = params_num[2]
    
    if heuristic_name=="slope_offset_delay":
        num_explorations = int((num_sdcs-offset+0.0)/slope + delay)
        
    if heuristic_name=="frontier":
        hpar.curr_num_sdcs = 1
        num_explorations = 2
    
    #print "starting topologies", allowed_topologies
    print "Number of SDCs: ",len(sdcs)
#    for i in range(2*len(sdcs)):
    
    lst_of_i = range(num_explorations)

    for i in lst_of_i:
        hpar.i = i    
        #create the correct topological map
        tmap_new = tmap_mask(tmap_orig, allowed_topologies)
        #print "new topological map", tmap_new            
        
        #set the topological map in the model
        dg_model_cp.tmap = tmap_new         
        
        #give the current number of sdcs
#        curr_sdcs = sdcs[0:min(i/2+1,len(sdcs))]
        curr_sdcs = sdcs[0:heuristic(hpar)]
        #print "USING ",len(curr_sdcs)," SDCS"

        dg_model_cp.initialize_transition_matrices()
        #print "topological map is: ", dg_model_cp.tmap
        #infer the best destinations

        dest_0, prob_log, sdcs_u, probs_log = dg_model_cp.infer_destination(curr_sdcs, sloc, orient)
        dest, prob_log = get_best_frontier(dg_model_cp, tmap_new, probs_log, visited_frontiers)
        #print "best frontier:",dest,prob_log
        
        if heuristic_name=="frontier":
            if dest_0 != dest and prob_log!=log(0):
                pass
            else:
                hpar.curr_num_sdcs += 1
            if hpar.curr_num_sdcs < num_sdcs:
                lst_of_i.append(lst_of_i[-1]+1)
                lst_of_i.append(lst_of_i[-1]+1)
                

        if prob_log!= log(0):
            mydest = float(dest[0].split("_")[0])
            
            if(not mydest in tmap_new.keys()):
                print "probability", prob_log
                print tmap_new
                raise KeyError("Bad key value")

            visited_frontiers.append(mydest)
#            print "visited topology ",mydest 
            visited_viewpoints.append(dest[0])
            allowed_topologies.extend(tmap_orig[mydest])
            
            
                    
#        print "allowed topologies: ",allowed_topologies 
    
    tmap_new = tmap_mask(tmap_orig, allowed_topologies) 
    #print "final topological map", tmap_new            
    dg_model_cp.tmap = tmap_new
    dg_model_cp.initialize_transition_matrices()
    ret_vals = dg_model_cp.infer_path(sdcs, sloc, orient)
    path, probs, sdcs_eval = ret_vals
    if path in [None, []]:
        print "infer_path() failed!"
        new_path=visited_viewpoints
    else:
        new_path = [path[0]]
        new_path.extend(visited_viewpoints)
        new_path.append(path[-1])
    ret_vals = (new_path , probs, sdcs_eval)
    
#    dg_model_cp.set_topo_map(tmap_orig)
    dg_model_cp.tmap = tmap_orig
    
    print "returning: ",ret_vals, visited_viewpoints
    
    return ret_vals, visited_viewpoints

# parameters for the heuristic
class h_param:
    def __init__(self):
        self.i = None
        self.num_sdcs = None
        self.SOD = None
        self.curr_num_sdcs = None

##### All these heuristics take as an argument instance of h_param #######
def heuristic_step(h):
    return h.num_sdcs

def heuristic_stairs(h):
    if h.i+1>h.num_sdcs:
        return h.num_sdcs
    else:
        return h.i+1
        
def heuristic_lifted_stairs(h):
    if h.i>h.num_sdcs:
        return h.num_sdcs
    else:
        return (h.i + h.num_sdcs)/2 
      
# SOD= slope,offset,delay  
def heuristic_SOD(h):
    slope = h.SOD[0]
    offset = h.SOD[1]
    num_curr_sdcs = int(offset + (h.i+0.0)*slope)
    num_curr_sdcs = min(num_curr_sdcs,h.num_sdcs)
    return num_curr_sdcs
    
def heuristic_frontier(h):
    return min(h.curr_num_sdcs,h.num_sdcs)


def tmap_mask(tmap, mask):
    tmap_new = {}
    
    for key in mask:
        tmap_new[key] = [key]
    
    #iterate through the from keys and check feasibility
    for key_from in tmap.keys():
        if key_from in mask:
            #iterate through the to keys and check feasibility
            for key_to in tmap[key_from]:
                if(key_to != key_from and key_to in mask):
                    try:
                        tmap_new[key_from].append(key_to)
                    except(KeyError):
                        tmap_new[key_from] = [key_to]

        else:
            tmap_new[key_from] = []

    return tmap_new
    
def get_best_frontier(dg_model, tmap, probs_log, visited_topos):
    
    print "best_frontier/visited_topos", visited_topos
    topo_sing = tmap.keys()
    print "Topo_sing: ",topo_sing
    
    orients = dg_model.get_viewpoint_orientations(dg_model.num_viewpoints)
    mymask = zeros(len(dg_model.viewpoints))+log(0)

    for topo in topo_sing:
        if topo in visited_topos:
            print "Skipping topo ",topo,"-----------------------"
            continue
        
        for orient in orients:
            i = dg_model.vpt_to_num[str(topo)+"_"+str(orient)]
            mymask[i] = 0.0
    
    new_probs_log = probs_log + mymask
    

    print "old max prob log", max(probs_log), "of ", probs_log
    print "new max prob log:", max(new_probs_log), "of ", new_probs_log
    return [dg_model.viewpoints[argmax(new_probs_log)]], new_probs_log[argmax(new_probs_log)]

