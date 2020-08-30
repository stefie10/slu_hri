from scipy import mean, array, transpose
from sorting import quicksort
import os
from nltk.metrics.distance import edit_distance
from shortest_path import shortestPath
from du import dir_util
from scipy import radians
from du.explore import explore
from gsl_utilities import tklib_get_distance
from spatial_features_cxx import math2d_dist


def get_orientations_each(model, start_region=None, dataset_name=None):
    return [[radians(orient)] for orient in model.get_viewpoint_orientations(model.num_viewpoints)]
def get_orientations_all(model, start_region=None, dataset_name=None):
    return [[radians(orient) for orient in model.get_viewpoint_orientations(model.num_viewpoints)]]
def get_orientations_annotated(model, start_region, dataset_name):
    print "dataset_name", dataset_name
    if(dataset_name == "df8full"):
        return [radians(get_d8_full_orientations(start_region))]
    elif(dataset_name == "df8"):
        return [radians(get_d8_orientations(start_region))]
    elif(dataset_name == "df13d"):
        return [radians(get_d1_3d_orientations(start_region))]
    elif(dataset_name == "df1"):
        return [radians(get_d1_orientations(start_region))]
    
    print "Unexpected dataset"+str(dataset_name)
    raise ValueError("Unexpected dataset"+str(dataset_name))

def get_d8_orientations(start_region):
    if(start_region == "R17" or 
       start_region == "R19"):
        return [0, 270]
    elif(start_region == "R9"):
        return [180, 90]
    elif(start_region == "R10" 
         or start_region == "R1" 
         or start_region == "R16"):
        return [180, 270]
    elif(start_region == "R25"):
        return [0]

    raise ValueError("Unexpected start location: " + str(start_region))

def get_d8_full_orientations(start_region):
    
    if(start_region == "R25"):
        return [90]
    if(start_region == "R1"):
        return [0, 270]
    if( start_region == "R16"):
        return [0, 270]
    if(start_region=="R10"):
        return [0]
    if(start_region == "R17" 
       or start_region == "R19"):
        return [0, 90]
    if(start_region == "R9"):
        return [180, 90, 270, 0]

    raise ValueError("Unexpected start location: " + str(start_region))


def get_d1_orientations(start_region):
    print "getting orientations"

    orientations = { \
        "R1"  : [ 180, 270 ],
        "R2"  : [ 180 ],
        "R7"  : [ 0, 180, 270 ],
        "R8"  : [ 0 ],
        "R11" : [ 0 ],
        "R15" : [ 90 ],
        "R16" : [ 180, 270 ],
        "R17" : [ 90, 180 ],
        "R19" : [ 90, 180 ],
        "R22" : [ 90, 0 ],
     }

    if start_region not in orientations:
        raise ValueError("Unexpected start location: " + str(start_region) + " cls: " + str(start_region.__class__))
    else:
        return orientations[start_region]

def get_d1_3d_orientations(start_region):
    print "getting orientations 3d"
    orientations = { \
        "R8"  : [ 0 ],
        "R15" : [ 90 ],
        "R7"  : [ 180],
        "R22" : [ 90 ],
        "R2"  : [ 180 ],
        "R16" : [ 180 ], 
     }

    if start_region not in orientations:
        raise ValueError("Unexpected start location: " + str(start_region) + " cls: " + start_region.__class__)
    else:
        return orientations[start_region]




class model_evaluator:
    def __init__(self, dg_model, gtruth_tf, dname=None):
        #dname should be d8, d1, d8_full, or d3 right now
        self.dname = dname
        self.dg_model = dg_model
        self.gtruth_tf = gtruth_tf 
        self.region_to_topology = get_region_to_topo_hash_containment(self.gtruth_tf, self.dg_model)
        self.extractor = dir_util.direction_parser_sdc()

    def get_partitioned_map(self):
        return self.dg_model.clusters

    def get_skeleton_map(self):
        return self.dg_model.clusters.skel

    def evaluate_sentence(self, sentence, start_region=None, start_pose=None):
        sdcs = self.extractor.extract_SDCs(sentence)

        if(start_region != None):
            orients = self.get_orientations(start_region)
            sloc = self.get_starting_location(start_region)
        elif(start_pose != None):
            sloc = start_pose[0:2]
            orients = [start_pose[-1]]
        
        path, lprob, sdc_utilized = self.dg_model.infer_path(sdcs, sloc, orients)
        
        poses = []
        for elt in path:
            topo, orient = elt.split("_")
            x, y = self.dg_model.tmap_locs[float(topo)]
            poses.append([x,y,radians(float(orient))])

        return transpose(poses), lprob, sdc_utilized, sdcs

    def evaluate_sentence_explore(self, sentence, start_region=None, start_pose=None):
        self.dg_explore = explore(self.dg_model)

        sdcs = self.extractor.extract_SDCs(sentence)

        if(start_region != None):
            orients = self.get_orientations(start_region)

            print "orientations", orients


            sloc = self.get_starting_location(start_region)
        elif(start_pose != None):
            sloc = start_pose[0:2]
            orients = [start_pose[-1]]
        
        self.dg_explore.initialize(sloc, orients)
        
        frontier = []
        frontiers_all = []
        allowed_frontiers = []
        
        for sdc in sdcs:
            curr_dest, all_dests, allowed_front = self.dg_explore.add_sdc(sdc)
            frontier.append(curr_dest)
            frontiers_all.append(all_dests)
            allowed_frontiers.append(allowed_front)
            
        path, lprob, sdc_utilized = self.dg_explore.infer_path_incremental()
        
        poses = []
        for elt in path:
            topo, orient = elt.split("_")
            x, y = self.dg_model.tmap_locs[float(topo)]
            poses.append([x,y,radians(float(orient))])

        return transpose(poses), lprob, sdc_utilized, sdcs, frontier, frontiers_all, allowed_front


    def get_d8_orientations(self, start_region):
        if(start_region == "R17" or 
           start_region == "R19"):
            return [0, 270]
        elif(start_region == "R9"):
            return [180, 90]
            #return [90]
        elif(start_region == "R10" 
             or start_region == "R1" 
             or start_region == "R16"):
            return [180, 270]
        elif(start_region == "R25"):
            return [0]

        raise ValueError("Unexpected start location: " + str(start_region))

    def get_d1_orientations(self, start_region):
        print "getting orientations"
        if(start_region == "R19" or 
           start_region == "R17"):
            return [90, 180]
        elif(start_region == "R1" 
             or start_region=="R16"):
            return [180, 270]
        elif(start_region == "R7"):
            return [0, 270]
        elif(start_region == "R22"):
            return [90, 0]
        elif(start_region == "R11"):
            return [0]
    
        print "Unexpected start location: " + str(start_region)
        raise ValueError("Unexpected start location: " + str(start_region))
    

    def get_orientations(self, start_region):
        if(self.dname == "d8"):
            return radians(self.get_d8_orientations(start_region))

        elif(self.dname == "d1"):
            return radians(self.get_d1_orientations(start_region))

        return [[radians(orient) 
                 for orient in self.dg_model.get_viewpoint_orientations(self.dg_model.num_viewpoints)]]

    def get_starting_location(self, start_region):
        return self.dg_model.tmap_locs[self.region_to_topology[start_region][0]]


def string_edit_distance(orig_path, predicted_path):
    orig_str = ""
    pred_str = ""

    for loc in orig_path:
        orig_str += chr(int(loc)+97)

    for loc_i, loc in enumerate(predicted_path):
        if(loc_i > 0 and predicted_path[loc_i-1] == predicted_path[loc_i]):
            continue
        pred_str += chr(int(loc)+97)
    
    return edit_distance(orig_str, pred_str)


def get_topological_paths_hash(map_part):
    #print "get d graph"
    mygraph = map_part.get_topological_distance_graph()
    

    mypaths = {}
    for topo1 in mygraph.keys():
        #print "iteration:", topo1
        mypaths[topo1] = {}
        for topo2 in mygraph.keys():
            mypaths[topo1][topo2] = shortestPath(mygraph, topo1, topo2)

    return mypaths

def get_topo_to_region_hash(tf_region, dg_model):
    topo_to_region = {}
    region_to_topo = get_region_to_topo_hash_containment(tf_region, dg_model)

    for r in region_to_topo.keys():

        for topo in region_to_topo[r]:
            if(not topo_to_region.has_key(topo)):
                topo_to_region[topo] = []

            if(not r in topo_to_region[topo]):
                topo_to_region[topo].append(r)
    
    return topo_to_region


def get_region_to_topo_hash_containment(tf_region, dg_model):
    #the tagfile here is of the regions
    
    ret_hash = {}
    ppoly = tf_region.polygons
    mymap = tf_region.get_map()

    for pp in ppoly:
        #add all of the topologies based on containment
        pts_I = [];
        for tm_key in dg_model.tmap_keys:
            tm_loc = dg_model.tmap_locs[tm_key]
            tm_loc = mymap.to_index(tm_loc)
            
            bbx1 = min(pp.X); bby1 = min(pp.Y);
            bbx2 = max(pp.X); bby2 = max(pp.Y);
            
            if(tm_loc[0] <= bbx2 and tm_loc[0] >= bbx1 and 
               tm_loc[1] <= bby2 and tm_loc[1] >= bby1):
                #it is contained
                if(len(dg_model.tmap[tm_key]) == 0):
                    continue

                if(ret_hash.has_key(pp.tag)):
                    ret_hash[pp.tag].append(tm_key)

                else:
                    ret_hash[pp.tag] = [tm_key]
                pts_I.append(tm_loc)

        #resort them by distance from the center 
        #         of the original region 
        if(ret_hash.has_key(pp.tag) and len(ret_hash[pp.tag]) > 1) and len(pts_I) != 0:
            D = tklib_get_distance(transpose(pts_I), [mean(pp.X), mean(pp.Y)]);
            D_srt, I_srt = quicksort(D)
            ret_hash[pp.tag] = list(array(ret_hash[pp.tag]).take(I_srt))

        
        #in case nothing was added for a particular tag
        if(not ret_hash.has_key(pp.tag)):
            print "region not found via containment"
            #raw_input()
            best_tmkey = None
            best_tmdist = 10000000000000000.0
            
            best_tmkey_dist = None
            best_tmdist_dist = 10000000000000000.0
            tm_loc1, tm_loc_dist = None, None
                
            for tm_key in dg_model.tmap_keys:
                tm_loc = dg_model.tmap_locs[tm_key]
                
                #tm_loc is in xy and we need to convert to 
                #  an index
                #print "getting euclidean dist"
                tm_d = math2d_dist([mean(pp.X), mean(pp.Y)], 
                                   mymap.to_index(tm_loc))
                #print "getting distances"
                tm_d_dist = pp.min_dist(mymap.to_index(tm_loc))
                
                #print "next"
                if(tm_d < best_tmdist):
                    best_tmdist = tm_d
                    best_tmkey = tm_key
                    tm_loc1 = tm_loc

                if(tm_d_dist < best_tmdist_dist):
                    best_tmdist_dist = tm_d_dist
                    best_tmkey_dist = tm_key
                    tm_loc_dist = tm_loc
    
            pts_I.extend([tm_loc_dist, tm_loc1])
            
            ret_hash[pp.tag] = [best_tmkey_dist, best_tmkey]
            
            
    return ret_hash


def get_output_filename(dirname, dg_model):
    basefn = str(dg_model.__class__).split('.')[-2]+".output"

    i = 0
    myfn = "%s/%s_%d.pck" % (dirname, basefn, i)
    while(os.path.exists(myfn)):
        i += 1
        myfn = "%s/%s_%d.pck" % (dirname, basefn, i)
    
    return myfn


