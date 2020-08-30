from environ_vars import *
from math import atan2
from math_util import *
from nltk.tokenize import sent_tokenize, word_tokenize
from pyTklib import tklib_random, tklib_init_rng
from gsl_utilities import tklib_normalize_theta
from routeDirectionCorpusReader import readSession
from scipy import *
from spatialRelationClassifier import SpatialRelationClassifier
from tag_util import tag_file
import cPickle
import crfEntityExtractor
import math2d
import numpy as na
import time
#from hmm import *
def sigmoid(x):
    return 1.0 / (1 + e**(-x))
def normalize(distribution):
    return distribution + 10e-10
def entropy(distribution):
    return -na.sum(na.log2(normalize(distribution + 10e-10)) * distribution)

#this loads the model
def load(model_fname):
    "loads a model from a pickle file."
    m4du = cPickle.load(open(model_fname, 'r'))
    m4du.initialize()
    return m4du

def print_tmat(T_mat, start_num, end_num):
    print "%d->%d" % (start_num, end_num), T_mat[end_num, start_num]
    
def is_loc_visible_from_pose(loc_st, theta_st, loc_end, fov=None):
    """
    Returns true if loc is visible from start_loc, start_theta with the given field of view
    """
    abs_orient = atan2(loc_end[1]-loc_st[1], loc_end[0]-loc_st[0])        
    
    if math2d.dist(loc_st, loc_end) < 0.00000001:
        return True
    elif (0 >= tklib_normalize_theta(theta_st - fov/2.0 - abs_orient) and
          0 <= tklib_normalize_theta(theta_st + fov/2.0 - abs_orient)):
        return True
    else:
        return False
        
def get_total_turn_amount(x1, y1, th1, x2, y2, th2, debug=False):
    theta = atan2(y2-y1, x2-x1)
    total_turn = abs(tklib_normalize_theta(th1 - theta)) +  abs(tklib_normalize_theta(th2 - theta))
    if debug:
        print "theta", math.degrees(theta)
        print "totalturn", math.degrees(total_turn)
        print "x1,y1,th1", x1, y1, math.degrees(th1)
        print "x2,y2,th2", x2, y2, math.degrees(th2)
            
    if x1 == x2 and y1 == y2 and th1 == th2:
        total_turn = 0

    direction = None
    if(abs(tklib_normalize_theta(theta - th1)) > abs(tklib_normalize_theta(th2 - theta))):
        direction = sign(tklib_normalize_theta(theta - th1))
    else:
        direction = sign(tklib_normalize_theta(th2 - theta))
        
    return total_turn, direction

class model_prototype_du:

    def __init__(self, myclusterfile, mycachelmap, num_viewpoints=4,
                 map_filename=None, tag_filename=None, boundingBox=None):
        tklib_init_rng(1)

        #load the clusters 
        print "loading clusters", myclusterfile
        self.clusters = cPickle.load(open(myclusterfile, 'r'))
        print "cluster class", self.clusters.__class__
        self.clusters.skel.G = None
        print "skel", self.clusters.skel
        print "skel", self.clusters.skel.__class__
        self.load_lmap(mycachelmap)
        self.allow_backtracking = False

        #model.clusters.tf.compute_path()

        if tag_filename != None:
            print "overwriting tag file", tag_filename
            self.clusters.tf = tag_file(tag_filename, map_filename)
            
            #if(boundingBox != None):
            self.clusters.tf.filter(boundingBox)
        self.tag_file = self.clusters.tf

        if map_filename != None:
            print "mapFile", map_filename
            self.clusters.skel.map_filename = map_filename
            self.clusters.tf.map_filename = map_filename
            
        
        #load the topological map
        print "getting topological map"
        self.tmap, tmap_cnt, self.tmap_locs_3d = self.clusters.get_topological_map()
        self.tmap_locs = dict([(key, loc[0:2]) for key, loc in self.tmap_locs_3d.iteritems()])
        self.tmap_keys = sorted(self.tmap.keys())
        
        self.num_regions = len(self.tmap.keys())

        #get the viewpoints... assumes that self.tmap is loaded
        self.num_viewpoints = num_viewpoints
        self.viewpoints, self.vpt_to_num = self.get_viewpoints(self.num_viewpoints)
        
        print "computing shortest paths"
        #self.shortest_paths, self.path_lengths = self.compute_shortest_paths()
        self.shortest_paths = None
        self.path_lengths = None


        self.vpt_to_tmap_index = {}
        self.vp_i_to_pose = {}
        for vp_i,vp in enumerate(self.viewpoints):
            topo, orient = vp.split("_")
            self.vpt_to_tmap_index[vp] = self.tmap_keys.index(float(topo));
            self.vp_i_to_pose[vp_i] = radians(float(orient))

        self.vp_i_to_topo_i = zeros(len(self.viewpoints), dtype=int32)
        for elt in self.viewpoints:
            self.vp_i_to_topo_i[self.vpt_to_num[elt]] = self.vpt_to_tmap_index[elt]
            
        
        
        #get the visible tags for each region
        self.topo_key_to_vtags, self.topo_key_to_itags = self.get_region_to_object_visibility_hash(self.tmap_locs)
        self.vp_i_to_vtags = self.get_vp_i_to_vtags()

        self.myparser = direction_parser()
        self.sr_class = SpatialRelationClassifier()
        self.spatial_relations = self.sr_class.engineNames

    @property
    def lmap_esp(self):
        try:
            if(self.lmap_esp != None):
                return self.lmap_esp
        except:
            self.lmap_esp = cPickle.load(open(TKLIB_HOME+"/data/flickr/models/model_esp_trained.svm.pck"))
        
        return self.lmap_esp

    @property
    def lmap_flickr(self):
        try:
            if(self.lmap_flickr != None):
                return self.lmap_flickr
        except:
            self.lmap_flickr = cPickle.load(open(TKLIB_HOME+"/data/flickr/models/model_flickr_trained.svm.pck"))
        
        return self.lmap_flickr
        


    def compute_shortest_paths(self):
        shortest_paths = {}
        path_lengths = na.zeros((max(self.tmap_keys) + 1,
                                 max(self.tmap_keys) + 1)) + 0.0
        for i in self.tmap_keys:
            for j in self.tmap_keys:
                sloc = self.tmap_locs[i]
                eloc = self.tmap_locs[j]
                shortest_paths.setdefault(i, {})
                print "i, j", i, j
                X, Y = self.clusters.skel.compute_path(sloc, eloc)
                shortest_paths[i][j] = X, Y
                path_lengths[i, j] = math2d.length(na.transpose((X, Y)))
        return shortest_paths, path_lengths

    def vp_i_to_loc(self, vp_i):
        return self.tmap_locs[self.vp_i_to_topo_key(vp_i)]
    
    def vp_i_to_topo_key(self, vp_i):
        topo_i = self.vp_i_to_topo_i[vp_i]
        return self.tmap_keys[topo_i]
        
    

    def vpts_for_topo(self, topo):
        result = []
        for i, vp in enumerate(self.viewpoints):
            topo_st, topo_st_ang = vp.split("_")
            topo_key = float(topo_st)
            if topo_key == topo:
                result.append(i)
        return result

    def get_observation_matrix(self):

        """
        O_mat[viewpoint_index][landmark_index] = probability of seeing
        something corresponding to that keyword, given a viewpoint.
        """
        
        #add the observation probabilities
        O_mat = zeros([self.num_regions*self.num_viewpoints, 
                       len(self.mynames)])*1.0
                       
        O_mat_oriented = zeros([self.num_regions*self.num_viewpoints, 
                                len(self.mynames)])*1.0                       
                       
        
        #set the default value for EPSILON
        eps_val = 1.0/(1.0*len(self.mynames))
        O_mat[:,self.names_to_index['EPSILON']] = ones(self.num_regions*self.num_viewpoints)*eps_val
        O_mat_oriented[:,self.names_to_index['EPSILON']] = ones(self.num_regions*self.num_viewpoints)*eps_val

        startTime = time.time()
        if  len(self.viewpoints) == 0:
            raise ValueError("No viewpoints")

        for vp_i in range(len(self.viewpoints)):
            print "processing viewpoint ", vp_i

            topo_key = float(self.viewpoints[vp_i].split("_")[0])

            j_tag = 0
            for tag in self.mynames:
                if(tag == 'EPSILON'):
                    continue

                try:
                    O_mat[vp_i][j_tag] = self.p_can_see_tag(tag, 
                                                            self.topo_key_to_vtags[topo_key],
                                                            self.topo_key_to_itags[topo_key])
                    
                    O_mat_oriented[vp_i][j_tag] = self.p_can_see_tag(tag, 
                                                                     self.vp_i_to_vtags[vp_i],
                                                                     self.vp_i_to_itags[vp_i]
                                                                     )
                    
                except(KeyError):
                    print "KeyErrors should no longer happen at this level"
                    print "tag", tag
                    print "topo_key", topo_key
                    print "vp", vp_i
                    print "jtag", j_tag
                    raise
                    
                j_tag+=1
                
            #normalize the probabilities
            #O_mat[vp_i,:] = O_mat[vp_i,:]/(1.0*sum(O_mat[vp_i,:]))
            
            print "itags:", self.topo_key_to_itags[topo_key]
            print "vtags:", self.topo_key_to_vtags[topo_key]
            
            l = 0
            for myelt in self.mynames:
                if myelt in ['kitchen', 'couch', 'door', 'sofa' ,
                             'toaster', 'bathroom', 'sink', 'elevator',
                             'bottle', 'whiteboard', 'lobby', 'stairs', 'hallway', 'room', 'corridor'
                             'window', 'windows', 'mailbox', 'toaster', 'refrigerator', 'microwave', 'fountain']:
                    print myelt, O_mat[vp_i, l]

                assert 0 <= O_mat[vp_i, l] <= 1.0
                assert 0 <= O_mat_oriented[vp_i, l] <= 1.0

                l+=1
            now = time.time()
            progress = float(vp_i + 1) / len(self.viewpoints)
            elapsedMinutes = (now - startTime) / 60.0
            estimatedTotal = elapsedMinutes / progress

            print "going for %.3f minutes, about %.3f minutes remaining)" % (elapsedMinutes, (estimatedTotal - elapsedMinutes))
            #raw_input()

        #print "epsilon prob:", O_mat[:,self.names_to_index['EPSILON']]
        print "o_mat took %.3f minutes" % elapsedMinutes
        return O_mat, O_mat_oriented


    def get_transition_matrix_uniform(self):
        T_mat = zeros([self.num_regions*self.num_viewpoints, 
                       self.num_regions*self.num_viewpoints])*1.0
        
        orients = self.get_viewpoint_orientations(self.num_viewpoints)
        
        for r_st in self.tmap_keys:
            for o_st in orients:
                #create the connections to all connected regions
                v_st_i = self.vpt_to_num[str(r_st)+"_"+str(o_st)]
                for r_end in self.tmap[r_st]:
                    for o_end in orients:
                        v_end_i = self.vpt_to_num[str(r_end)+"_"+str(o_end)]
                        T_mat[v_end_i, v_st_i] = 1.0
                
                #do the self connections
                for o_end in orients:
                    v_end_i = self.vpt_to_num[str(r_st)+"_"+str(o_end)]
                    T_mat[v_end_i, v_st_i] = 1.0

        return T_mat



    def get_uniform_transition_matrix(self):
        """
        Get a transition matrix that allows self transitions to any
        viewpoint at that location, and transitions to any viewpoint
        you can see, ignoring orientation completely.
        """

        T_mat = zeros([self.num_regions*self.num_viewpoints, 
                       self.num_regions*self.num_viewpoints])*1.0        
        new_tmap = self.get_topological_map_viewpoint(math.pi, 0)
        for i in range(len(self.viewpoints)):
            connections = new_tmap[self.viewpoints[i]]
            topo_st, topo_st_ang = self.viewpoints[i].split("_")
            
            for vp_i in self.vpts_for_topo(float(topo_st)):
                for conn in connections:
                    topo_end, topo_end_ang = conn.split("_")
                    for vp_j in self.vpts_for_topo(float(topo_end)):
                        T_mat[vp_j, vp_i] = 1.0

            T_mat[vp_i, vp_i] = 1.0

        return T_mat
        
    def get_snapped_transition_matrix(self, direction="straight", p_self=1.0):
        T_mat = self.get_transition_matrix(direction, p_self)
        for vp_i in range(len(self.viewpoints)):
            for vp_j in range(len(self.viewpoints)):
                if T_mat[vp_j, vp_i] >= 0.7:
                    T_mat[vp_j, vp_i] = 1
        return T_mat
    
        
    def get_vertical_transition_matrix(self, direction="stay", p_self=1.0 ):
        
        assert direction in ["stay", "up", "down"]
                
        T_mat = zeros([self.num_regions*self.num_viewpoints, 
                       self.num_regions*self.num_viewpoints])*1.0
        new_tmap = self.get_topological_map_viewpoint(None, 0)

        print "verticaldirection", direction
        print "vpt", 18, [self.vpt_to_num[x] for x in new_tmap[self.viewpoints[18]]]
        
        
        #for each of the viewpoints
        for i in range(len(self.viewpoints)):
            connections = new_tmap[self.viewpoints[i]]
            
            #find the areas connected and if they are reasonable            
            for conn in connections:
                cconn = conn 
                #connofconn = [conn]
                #connofconn.extend(new_tmap[conn])
                #for conn_i, cconn in enumerate(connofconn):

                #convert this into topo numbers
                topo_st, topo_st_ang = self.viewpoints[i].split("_")
                topo_end, topo_end_ang = cconn.split("_")

                if(cconn < 0 or self.viewpoints[i] == -1):
                    continue
                
                x1, y1, z1 = self.tmap_locs_3d[float(topo_st)]
                x2, y2, z2 = self.tmap_locs_3d[float(topo_end)]

                #for each of the to-node's orientations, check its relative angle to 
                #          the from node's orientation and give it a relative probability
                #          accordingly
                start_num = self.vpt_to_num[self.viewpoints[i]]
                end_num = self.vpt_to_num[cconn]

                #going to end_num from i
                if direction == 'stay':
                    if z1 == z2:
                        val = 1.0
                    else:
                        val = 1e-6
                elif direction == 'up':
                    if z1 < z2:
                        val = 1.0
                    elif z1 == z2:
                        val = 0.2
                    else:
                        val = 1e-6
                        
                    if math2d.dist((x1, y1), (x2, y2)) > 0.5:
                        val = 0.9 * val                        
                elif direction == 'down':
                    if z2 < z1:
                        val = 1.0
                    elif z1 == z2:
                        val = 0.2
                    else:
                        val = 1e-6
                    if math2d.dist((x1, y1), (x2, y2)) > 0.5:
                        val = 0.9 * val                        
                else:
                    raise ValueError("Bad direction: " + `direction`)
                
                T_mat[end_num,start_num] = val
                
            #connect self transitions
            topo_st, topo_st_ang = self.viewpoints[i].split("_")
            if(direction == "stay"):
                T_mat[i,i] = p_self
        
        return T_mat
        
    def get_transition_matrix(self, direction="straight", p_self=1.0 ):
        T_mat = zeros([self.num_regions*self.num_viewpoints, 
                       self.num_regions*self.num_viewpoints])*1.0
        print
        print "direction", direction
        if(direction == "straight"):
            new_tmap = self.get_topological_map_viewpoint(pi, 0)
        elif(direction == "back"):
            new_tmap = self.get_topological_map_viewpoint(pi, pi)            
        elif(direction == "right"):
            new_tmap = self.get_topological_map_viewpoint(pi, -1.0*pi/2.0)
        elif(direction == "left"):
            new_tmap = self.get_topological_map_viewpoint(pi, +1.0*pi/2.0)
        elif(direction == "face"):
            new_tmap = self.get_topological_map_viewpoint(None, 0)            
        else:
            raise ValueError("Unexpected direction: " + `direction`)

        
        #for each of the viewpoints
        for i in range(len(self.viewpoints)):
            connections = new_tmap[self.viewpoints[i]]
            
            #find the areas connected and if they are reasonable            
            for conn in connections:
                cconn = conn 
                #connofconn = [conn]
                #connofconn.extend(new_tmap[conn])
                #for conn_i, cconn in enumerate(connofconn):

                #convert this into topo numbers
                topo_st, topo_st_ang = self.viewpoints[i].split("_")
                topo_end, topo_end_ang = cconn.split("_")

                if(cconn < 0 or self.viewpoints[i] == -1):
                    continue

                loc1 = self.tmap_locs[float(topo_st)]
                loc2 = self.tmap_locs[float(topo_end)]

                #for each of the to-node's orientations, check its relative angle to 
                #          the from node's orientation and give it a relative probability
                #          accordingly
                start_num = self.vpt_to_num[self.viewpoints[i]]
                end_num = self.vpt_to_num[cconn]

                #make this dependent on how much we turn in total
                debug = False
                if (start_num == 18 or start_num == 16) and end_num == 42 and False:
                    print "***************", start_num, end_num
                    debug = True
                orient_diff, d_turn = get_total_turn_amount(loc1[0], loc1[1], 
                                                            radians(float(topo_st_ang)),
                                                            loc2[0], loc2[1], 
                                                            radians(float(topo_end_ang)),
                                                            debug=debug)
                #going to end_num from i
                if(direction == 'straight'):
                    if debug:
                        print "val", max(-1.75/pi*abs(orient_diff)+1, 0.0)
                    T_mat[end_num,start_num] = -abs(orient_diff)
                    T_mat[end_num, start_num] = sigmoid(T_mat[end_num, start_num])
                elif(direction == 'back'):
                    diff_from_pi = tklib_normalize_theta(d_turn*orient_diff-pi)
                    T_mat[end_num,start_num] = -abs(diff_from_pi)
                    T_mat[end_num, start_num] = sigmoid(T_mat[end_num, start_num])
                    #T_mat[start_num][end_num] = max(-1.5/pi*abs(orient_diff)+1, 0.0)                    
                elif(direction == 'right' and d_turn < 0):
                    diff_from_neg_pi2 = tklib_normalize_theta(d_turn*orient_diff+(pi/2.0))
                    T_mat[end_num,start_num] = -abs(diff_from_neg_pi2)
                    T_mat[end_num, start_num] = sigmoid(T_mat[end_num, start_num])
                    #T_mat[start_num][end_num] = max(-1.5/pi*abs(diff_from_neg_pi2)+1, 0.0)
                elif(direction == 'left' and d_turn > 0):
                    diff_from_pi2 = tklib_normalize_theta(d_turn*orient_diff-(pi/2.0))
                    T_mat[end_num,start_num] = -abs(diff_from_pi2)
                    T_mat[end_num, start_num] = sigmoid(T_mat[end_num, start_num])
                elif direction == "face":
                    if math2d.dist(loc1, loc2) < 0.01:
                        T_mat[end_num, start_num] = p_self
                    else:
                        T_mat[end_num, start_num] = 0
                assert 0 <= T_mat[end_num, start_num] <= 1, T_mat[end_num, start_num]

                    #T_mat[start_num][end_num] = max(-1.5/pi*abs(diff_from_pi2)+1, 0.0)
                #if(not conn == cconn):
                #    T_mat[end_num,start_num] = T_mat[end_num,start_num]*0.3
            
            #connect self transitions
            topo_st, topo_st_ang = self.viewpoints[i].split("_")
            if(direction == "straight"):
                T_mat[i,i] = p_self
            elif(direction == "right"):
                newang = mod(int(float(topo_st_ang))-int(float(self.get_viewpoint_diff())), 360.0)*1.0
                T_mat[self.vpt_to_num[str(topo_st)+"_"+str(newang)],i] = p_self
            elif(direction == "left"):
                newang = mod(int(float(topo_st_ang))+int(float(self.get_viewpoint_diff())), 360.0)*1.0
                T_mat[self.vpt_to_num[str(topo_st)+"_"+str(newang)],i] = p_self
            elif(direction == "back"):
                newang = mod(int(float(topo_st_ang)) + 180, 360)*1.0
                T_mat[self.vpt_to_num[str(topo_st)+"_"+str(newang)],i] = p_self
        return T_mat



    def smooth_T_mat(self, T_mat):
        for vp1_i in range(len(self.viewpoints)):
            for vp2_i in range(len(self.viewpoints)):
                topo1_i = self.vp_i_to_topo_i[vp1_i]
                topo2_i = self.vp_i_to_topo_i[vp2_i]
                if topo2_i in self.tmap[topo1_i] or topo1_i == topo2_i:
                    T_mat[vp2_i, vp1_i] = max(T_mat[vp2_i, vp1_i], 1e-32)
        
    def get_usable_sdc(self, sdcs):
        SDC_utilized = []
        
        print "getting prob distributions"
        curr_i = 0
        for sdc in sdcs:
            print "sdc:", sdc
            if(sdc == "EPSILON"):
                SDC_curr = {"figure":None, "sr":None, "verb":"straight", "landmark":"EPSILON", "kwsdc":False, "landmarks":[]}
                SDC_utilized.append(SDC_curr)
                continue
            

            SDC_curr = {"figure":None, "sr":None, "verb":None, "landmark":None, "kwsdc":False, "landmarks":[]}

            ##########################################
            #find the keyword for this element, if one exists
            #    if it does not exist, then move on to the next SDC

            #fig_kws = extract_keywords(sdc["figure"].text.lower(), self.mynames)
            fig_kws, fig_kws_turn = self.myparser.parse_sentence_string(sdc["figure"].text.lower(), 
                                                                        self.mynames)
            
            #ldmk_kws = extract_keywords(sdc["landmark"].text.lower(), self.mynames)
            ldmk_kws, ldmk_kws_turn = self.myparser.parse_sentence_string(sdc["landmark"].text.lower(),
                                                                          self.mynames)
            #if we haven't found any keywords, then return
            #if(len(fig_kws) == 0 and len(ldmk_kws) == 0):
            #    pass
            if(len(ldmk_kws) > 0):
                SDC_curr["landmark"] = ldmk_kws[0];
                SDC_curr["landmarks"] = ldmk_kws
                ldmk_kws_turn.remove(ldmk_kws[0])
            elif(len(fig_kws) > 0):
                SDC_curr["landmark"] = fig_kws[0];
                SDC_curr["landmarks"] = fig_kws;
                fig_kws_turn.remove(fig_kws[0])

            
            #get the left, right and straight keywords
            # if the previous element was a turn command, then use it
            # sdcs[curr_i-1]["landmark"] == "" and sdcs[curr_i-1]["landmark"] == "")):
            verb = sdc.verb.text.lower()
            if "right" in verb:
                SDC_curr["verb"] = "right"
            elif "left" in verb:
                SDC_curr["verb"] = "left"
            elif "up" in verb:
                SDC_curr["verb"] = "up"
            elif "down" in verb:
                SDC_curr["verb"] = "down"
            elif "around" in verb:
                SDC_curr["verb"] = "turn_around"
            elif any([x in verb for x in ["face", "facing", "orient"]]):
                SDC_curr["verb"] = "face"
            elif "stop" in verb:
                SDC_curr["verb"] = "stop"
            else:
                SDC_curr["verb"] = "straight"

            #in case we haven't parsed anything useful, then continue
            if(SDC_curr["landmark"] == None 
               and SDC_curr["verb"] == "straight"):
                continue

            #############################################
            #    find the first spatial relation that matches
            #        and add it to the list
            #srEngine = self.sr_class.sdcToClassifier_keyword(sdc) # original algorithm

            #print "sdc to classifier"
            srEngine = self.sr_class.sdcToClassifier(sdc)
            if not (srEngine is None):
                SDC_curr["sr"] = srEngine.name()

            ############################################
            #add the current SDC to the list
            SDC_utilized.append(SDC_curr)

            ##############################################
            #  Now append the other things that we 
            #            didn't previously capture
            ##############################################
            #get all the keywords
            all_keywords = list(copy(fig_kws_turn))
            all_keywords.extend(ldmk_kws_turn)
            
            for kw_i, kw in enumerate(all_keywords):
                #assuming that I didn't extract left and right, then do something here
                if(not kw  == "RIGHT" and not kw == "LEFT"):
                    mysdc = {"figure":None, "sr":None, "verb":"straight", "landmark":kw, "kwsdc":True, "landmarks":[kw]}
                    
                    #if the previous keyword was left or right then set the verb properly
                    if(kw_i > 0 and (all_keywords[kw_i-1] == "RIGHT" 
                                     or all_keywords[kw_i-1] == "LEFT")):
                        mysdc["verb"] = all_keywords[kw_i-1]

                    if(mysdc["landmark"] == None 
                       and mysdc["verb"] == "straight"):
                        continue

                    SDC_utilized.append(mysdc)

            curr_i += 1



        #TODO, Stefanie, what does this do... is this a null starting SDC
        SDC_utilized.insert(0, {"figure":None, "sr":None, "verb":"straight", 
                           "landmark":"EPSILON", "kwsdc":False, "landmarks":[]})

        return SDC_utilized

    def get_topo_i_to_location_mask(self):
        """
        Returns a map from topo_i to a mask of what objects are visible from that topo_i.
        """
        print "get_region_to_visible_locations"
        region_to_visible_locations  = zeros([len(self.tmap_keys), len(self.obj_locations[0])])*1.0
        
        for topo_i, topo in enumerate(self.tmap_keys):
            xy = self.tmap_locs[topo][0:2]
            
            loc_mask = []
            for i in range(len(self.obj_locations[0])):
                mygm = self.clusters.skel.get_map()

                if mygm.is_visible(xy, self.obj_locations[:,i]):
                    loc_mask.append(1)
                else:
                    loc_mask.append(0)
            region_to_visible_locations[topo_i] = loc_mask

        return region_to_visible_locations



    def load_lmap(self, fname):
        print "loading lmap", fname
        f = open(fname, "r")
        self.lmap_cache = cPickle.load(f)
        f.close()
        mynames = self.lmap_cache.tagnames
        
        
        #get the non-redundant names
        self.mynames = []
        for elt in mynames:
            if not elt in self.mynames:
                if (not "lda" in self.__module__ or
                    not elt in ["room", "type", "back", "area", "end", 
                                "intersection", "set", "space", "facing", 
                                "corner", "keep", "carpet", "grey", "gray", 
                                "stand", "till", "way", "ceiling", "cross", 
                                "number", "lead", "point", "row", "first"]):
                    self.mynames.append(elt)
        self.mynames.append('EPSILON')
        #self.mynames.extend(self.clusters.tf.get_tag_names())

        #get a tag name to index hash
        i = 0
        self.names_to_index = {}
        for elt in self.mynames:
            self.names_to_index[elt] = i
            i+=1
        
        
        
    #only get things in the fov of the locations
    #def get_viewpoint_tmap(self, fov, turn_amount):
    def get_topological_map_viewpoint(self, fov, turn_amount):
        tmap_new = {}
        
        #iterate through all the viewpoints
        for i in range(len(self.viewpoints)):
            #get the start location
            tf, tfor = self.viewpoints[i].split("_");tf = float(tf);
            loc_st = self.tmap_locs[tf]
            st_orient = float(tfor)*pi/180.0;
            
            tmap_new[self.viewpoints[i]] = []
            
            #iterate through all the viewpoints
            for j in range(len(self.viewpoints)):

                #get the end location
                tt, ttor = self.viewpoints[j].split("_"); tt = float(tt)
                loc_end = self.tmap_locs[tt]
                end_orient = float(ttor)*pi/180.0;    

                #absolute difference in orientation
                abs_orient = atan2(loc_end[1]-loc_st[1], loc_end[0]-loc_st[0])
                
                #if we're connected and we're in the fov
                if i == 40 and j == 42 and True:
                    print i, j
                    print "vp1", self.viewpoints[i]
                    print "vp2", self.viewpoints[j]
                    print "l1", loc_st, "=>", loc_end
                    
                    print
                    print "tt", tt in self.tmap[tf]
                    if fov != None:
                        print "fov/2.0", math.degrees(fov/2.0)
                        print "c1", (0 >= tklib_normalize_theta(st_orient - fov/2.0 - abs_orient + turn_amount))
                        print "c2", (0 <= tklib_normalize_theta(st_orient + fov/2.0 - abs_orient + turn_amount))
                        print "c1 angle", math.degrees(st_orient - fov/2.0 - abs_orient + turn_amount)                    
                        print "c2 angle", math.degrees(st_orient + fov/2.0 - abs_orient + turn_amount)
                        print "normalized"                    
                        print "c1 angle", tklib_normalize_theta(math.degrees(st_orient - fov/2.0 - abs_orient + turn_amount))                    
                        print "c2 angle", tklib_normalize_theta(math.degrees(st_orient + fov/2.0 - abs_orient + turn_amount))                    
                    else:
                        print "fov is None"
                    print
                    print "st_orient", math.degrees(st_orient)
                    
                    print "abs_orient",abs_orient
                    print "turn_amount", turn_amount
                    

                    

                    print
                
                if tt in self.tmap[tf]:
                    append = False
                    if fov == None:
                        append = True
                    elif (0 >= tklib_normalize_theta(st_orient - fov/2.0 - abs_orient + turn_amount) and
                          0 <= tklib_normalize_theta(st_orient + fov/2.0 - abs_orient + turn_amount)):
                        append = True
                    elif math2d.dist(loc_st, loc_end) < 0.00001:
                        append = True
                    if append:
                        tmap_new[self.viewpoints[i]].append(self.viewpoints[j])
        return tmap_new

    

    def get_vp_i_to_vtags(self):
        """
        A map from vp_i to the set of tags visible from that vp, taking 
        into account field of view.
        """
        self.vp_i_to_vtags = {}
        self.vp_i_to_itags = {}
        for vp_i, vp in enumerate(self.viewpoints):
            loc = self.vp_i_to_loc(vp_i)
            vtags = set([])
            itags = set([]) 
            vobjects, iobjects = self.clusters.tf.get_visible_objects(loc)
            for o in vobjects:
                obj_loc = self.clusters.tf.get_map().to_xy(o.centroid())
                if is_loc_visible_from_pose(loc, self.vp_i_to_pose[vp_i], obj_loc, 
                                            fov=math.pi/2):
                    vtags.add(o.tag)
                else:
                    itags.add(o.tag)
                    
            for o in iobjects:
                itags.add(o.tag)
                
            itags = itags - vtags
                        
            self.vp_i_to_vtags[vp_i] = frozenset(vtags)
            self.vp_i_to_itags[vp_i] = frozenset(itags)
            
            
        return self.vp_i_to_vtags
        
    #def get_visibility_hash(self, tmap_locs):
    def get_region_to_object_visibility_hash(self, tmap_locs):

        #compute the visible objects from the mean location
        topo_key_to_vtags = {}
        topo_key_to_itags = {}
        for topo_key in tmap_locs.keys():
            myloc = tmap_locs[topo_key]
            vtags = []; itags = []

            #make sure you get "some" tag
            numiters = 0

            while len(vtags) == 0:
                r1, r2 = tklib_random()-0.5, tklib_random()-0.5
                vtags,itags_t=self.clusters.tf.get_visible_tags((myloc[0]+numiters*0.1*r1, 
                                                                 myloc[1]+numiters*0.1*r2))
                
                itags = []
                for elt_t in itags_t:
                    if(not elt_t in vtags and not elt_t in itags):
                        itags.append(elt_t)

                numiters +=1
            assert len(vtags) > 0
            #vtags, itags = self.clusters.tf.get_visible_tags(myloc)
            
            #add these tags to the list
            topo_key_to_vtags[topo_key] = vtags
            topo_key_to_itags[topo_key] = tuple(itags)

        return topo_key_to_vtags, topo_key_to_itags

    def make_tag_probability_map(self):
        """
        Returns a map from tag to p(an object in this environment is tag)
        """
        out = {}
        for tag in self.obj_names:
            out.setdefault(tag, 0.0)
            out[tag] += 1
        
        for key, value in out.iteritems():
            out[key] = value / len(self.obj_names)

        return out
        

        

    def get_object_to_object_visibility_hash(self):
        result = []
        print "getting object_to_object visibility hash"
        for i, name in enumerate(self.obj_names):
            vtags, itags_t = self.clusters.tf.get_visible_tags((self.obj_locations[0, i],
                                                                self.obj_locations[1, i]))
            result.append((vtags, itags_t))
        return result
    
    def get_viewpoints(self, num_orientations=4):
        viewpoint_names = []
        viewpoint_to_num_hash = {}

        angles = self.get_viewpoint_orientations(num_orientations)
        i = 0
        for elt in self.tmap.keys():
            for viewpoint in angles:
                viewpoint_names.append(str(elt)+"_" + str(viewpoint))
                viewpoint_to_num_hash[str(elt)+"_" + str(viewpoint)] = i
                i+=1
        
        return array(viewpoint_names), viewpoint_to_num_hash

    def get_viewpoint_orientations(self, num_orientations):
        return linspace(0, 360, num_orientations+1)[0:-1]

    def get_viewpoint_diff(self):
        vo = self.get_viewpoint_orientations(self.num_viewpoints)
        return vo[1]-vo[0]
    def p_srel(self, sr, ground_pts, figure_pts):
        """
        Returns estimate for p(sr | t, o)
        """
        return self.p_phi_srel(sr, ground_pts, figure_pts)
    

    def p_phi_srel(self, sr, ground_pts, figure_pts, phi_value = True):
        """
        Returns p(phi_sr | t, o)
        """
        if sr in self.sr_class.engineMap:
            engine = self.sr_class.engineMap[sr]
            mycl, isval, sc = self.sr_class.doClassify(engine, ground_pts, figure_pts)
            result = sc
        else:
            result = 1

        if phi_value:
            return result
        else:
            return 1 - result
        

    def p_can_see_tag_max(self, tag, vtags, itags):
        """
        Return the probability you can see a word, given visible and
        invisible objects. uses the max hack.
        """
        if len(vtags) == 0:
            #raise ValueError("Empty vtags: " + `vtags`)
            return 1e-6
        elif tag in vtags:
            return 1 - 1e-6
        else:
            return na.max([self.lmap_cache.p_obj1_given_obj2(tag, vtag) 
                           for vtag in vtags]) # 56/150




#get all of the alignments
def create_alignments_sdc(sdcs, num_eps):
    if(num_eps <= 0):
        return sdcs
        
    #observations = array(observations)

    #how many slots are there for observations
    total_vals = len(sdcs) + num_eps

    #only allows for 150 characters
    all_alignments = zeros([binom(total_vals, num_eps), total_vals], '|S150')
    all_alignments.fill('EPSILON')

    #now fill in the relevant observations
    curralign = 0
    
    all_alignments = all_alignments.tolist()
    for combo in unique_combinations(range(total_vals), num_eps):
        
        currlocation = 0
        
        for i in range(len(combo)):
            if(i == 0):
                newlocation = currlocation + combo[i]
                all_alignments[curralign][0:combo[i]] = sdcs[currlocation:newlocation]
            else:
                newlocation = currlocation + (combo[i] - combo[i-1]-1)
                all_alignments[curralign][combo[i-1]+1:combo[i]] = sdcs[currlocation:newlocation]
            currlocation = newlocation

        all_alignments[curralign][combo[-1]+1:] = sdcs[newlocation:]
        
        curralign+=1
        
    return all_alignments
    

def parse_sentence(mystr, mymodel):
    return parse_sentence_string(mystr, mymodel.mynames)

def parse_sentence_string(mystr, obj_names, mytagger=None):
    if(mytagger == None):
        mytagger = cPickle.load(open('%s/pytools/direction_understanding3/data/tagger/tagger.pck' % TKLIB_HOME, 'r'))
    
    keywords = []
    keywords_and_turns = []
    for s in sent_tokenize(mystr):
        words = word_tokenize(s)
        
        #print "words:", words

        mytags = mytagger.tag(words)

        if('right' in words or 'left' in words 
           or 'Right' in words or 'Left' in words):
            print s
            #print mytags
            #raw_input()

        k = 0
        for pair in mytags:
            w, t = pair
            w = w.lower()
            #print "word, tag:", w, t
            print w,t
            if t in ['NN', 'NNP', 'CD', 'JJ', 'VBG', 'NNS']:
                if w[0:-2] in obj_names:
                    keywords.append(w[0:-2])
                    keywords_and_turns.append(w[0:-2])
                elif w[0:-1] in obj_names:
                    keywords.append(w[0:-1])
                    keywords_and_turns.append(w[0:-1])                    
                elif w in obj_names:
                    keywords.append(w)
                    keywords_and_turns.append(w)
                

            #elif(t[0:2] == 'NN'):
            #    print "not added", w, t
            
            #try to get out the turns
            try:
                if('turn' in w or 'take' in w 
                   or 'bear' in w or 'make' in w or w == 'go'):
                    for m in range(3):
                        if(mytags[k+m][0].lower() == 'right'):
                            keywords_and_turns.append('RIGHT')
                            break
                        elif(mytags[k+m][0].lower() == 'left'):
                            keywords_and_turns.append('LEFT')
                            break
            except(IndexError):
                print "key error in persing... no problem here"


            k+=1
    
    print "keywords", keywords
    return keywords, keywords_and_turns


#def parse_and_chunk_SDCs(mystr):
#    extractor = crfEntityExtractor.SdcExtractor()
#    results = extractor.chunk(mystr)
#    return results


class direction_parser:
    def __init__(self):
        self.mytagger = cPickle.load(open('%s/pytools/direction_understanding3/data/tagger/tagger.pck' % TKLIB_HOME, 'r'))
        
    def parse_sentence_string(self, mystr, obj_names):
        return parse_sentence_string(mystr, obj_names, self.mytagger)

class direction_parser_sdc:
    def __init__(self):
        self.extractor = crfEntityExtractor.SdcExtractor()

    def extract_SDCs(self, mystr):
        return self.extractor.chunk(mystr)



class direction_parser_wizard_of_oz:
    def __init__(self, corpus_fn, annotations):
        self.dsession = readSession(corpus_fn, annotations)
        self.data = {}
        
        for session in self.dsession:
            for instructionIdx, instruction in enumerate(session.routeInstructions):
                annotations = session.routeAnnotations[instructionIdx]
                self.data[str(instruction)] = annotations
                
    def extract_SDCs(self, mystr):
        from routeDirectionCorpusReader import TextStandoff, Annotation
        annotations =  self.data[mystr]

        # the annotations contain a pointer to the containing
        # class, which doesn't pickle, and breaks multiprocessing.
        # this gets rid fo that pointer. 
        # to get a better error message, add a cPickle.dump to the return value...
        # otherwise the error message comes out in a weird place. 
        cleaned_annotations = []
        for a in annotations:
            argmap = {}
            for key, standoff in a.annotationMap.iteritems():
                argmap[key] = TextStandoff(mystr, standoff.range)
            cleaned_annotations.append(Annotation(**argmap))
        assert len(cleaned_annotations) != 0
        cleaned_annotations.sort(key=lambda x: x.range.start)
        
        #out = [x for x in cleaned_annotations if not parent_in_set(x, cleaned_annotations)]
        out = cleaned_annotations
        return out



def parse_sentence_chunk(mystr, mymodel):
    return parse_sentence_chunk_string(mystr, mymodel.mynames)


def parse_sentence_chunk_string(mystr, obj_names):
    extractor = crfEntityExtractor.SdcExtractor()
    #results = extractor.chunk(mystr)
    results = extractor.chunk(mystr)
    
    keywords = []
    keywords_and_turns = []
    for sdc in results:
        '''print "****************"
        print "figure:", sdc['figure'].text
        print "verb:", sdc['verb'].text
        print "spatial relation:", sdc['spatialRelation'].text
        print "landmark:", sdc['landmark'].text'''
        
        fspl = word_tokenize(sdc['figure'].text)
        gspl = word_tokenize(sdc['landmark'].text)

        vspl = word_tokenize(sdc['verb'].text)
        
        for myword in fspl:
            if(myword.lower() in obj_names):
                keywords.append(myword.lower())
                keywords_and_turns.append(myword.lower())
            elif(myword[0:-1].lower() in obj_names):
                keywords.append(myword[0:-1].lower())
                keywords_and_turns.append(myword[0:-1].lower())
            elif(myword[-2:] == 'es' and myword[0:-2].lower() in obj_names):
                keywords.append(myword[0:-2].lower())
                keywords_and_turns.append(myword[0:-2].lower())

        for myword in vspl:
            if(myword.lower() == 'left'):
                keywords_and_turns.append(myword.upper())
            elif(myword.lower() == 'right'):
                keywords_and_turns.append(myword.upper())

        for myword in gspl:
            if(myword.lower() in obj_names):
                keywords.append(myword.lower())
                keywords_and_turns.append(myword.lower())
            elif(myword[-1] == 's' and myword[0:-1].lower() in obj_names):
                keywords.append(myword[0:-1].lower())
                keywords_and_turns.append(myword[0:-1].lower())
            elif(myword[-2:] == 'es' and myword[0:-2].lower() in obj_names):
                keywords.append(myword[0:-2].lower())
                keywords_and_turns.append(myword[0:-2].lower())

    return keywords, keywords_and_turns



def extract_keywords(mystr, obj_names):

    #print "extracting keywords from", mystr
    keywords = []
    
    for s in sent_tokenize(mystr):
        words = word_tokenize(s)
        
        for w in words:
            w = w.lower()
            if(w in obj_names):
                keywords.append(w)
            elif(w[-1] == 's' and w[0:-1] in obj_names):
                keywords.append(w[0:-1])
            elif(w[-2:] == 'es' and w[0:-2] in obj_names):
                keywords.append(w[0:-2])
    
    return keywords



if __name__=="__main__":
    test = parse_sentence_chunk()


