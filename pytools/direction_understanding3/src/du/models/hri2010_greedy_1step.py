from pyTklib import kNN_index
from gsl_utilities import tklib_normalize_theta
import du.models.hri2010_global
import numpy as na
from numpy import radians, transpose, degrees, pi, zeros, mod
from du.dir_util import get_total_turn_amount


class FakeGm:
    def __init__(self):
        self.update_args = []

#class model(du.models_test.min_entropy.model):
class model(du.models.hri2010_global.model):
    """
    a greedy algorithm. Always take the locally best transition. 
    """
    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename,
                 tag_filename):
        du.models.hri2010_global.model.__init__(self, clusterfile, cachelmap, 
                                                srelMatFname, map_filename, tag_filename)
        print "loaded"


    def update_for_backtracking(self, observation_probs, path):
        for p in path:
            for i in range(len(self.viewpoints)):
                if p != i:
                    observation_probs[i, p] = 0


    def observation_matrices(self, sdcs, loc, sorients_rad):
        """
        Yield the sequence of observationmatrices for each SDC.  This
        combines p_obs and p_trans.
        """

        print "beginning greedy search, NOT viterbi.  It's called viterbi for compatability."
        from pyTklib import tklib_du_lp_obs as tklib_observation_probs
        i, = kNN_index(loc, transpose(self.tmap_locs.values()), 1)
        iSlocTopo = self.tmap_locs.keys()[int(i)]

        orients = self.get_viewpoint_orientations(self.num_viewpoints)
        i_tmp, = kNN_index([degrees(sorients_rad[0])], [orients], 1);
        self.iSloc = self.vpt_to_num[str(iSlocTopo)+"_"+str(orients[i_tmp])]
        
        print "preparing"
        T_seq, O_seq, SR_seq, L_seq, D_seq, self.SDC_utilized, newpi = self.inference_prepare(sdcs, loc, sorients_rad)
        

        print "looping"
        self.mygm = FakeGm()
        self.mygm.T_seq = T_seq

        T_mat_prev = [[]]
        
        for i, (T_mat) in enumerate(T_seq):

            if(not len(SR_seq) == 0 and not SR_seq[i] == None):
                SR_reshape = SR_seq[i].reshape([len(SR_seq[i])*len(SR_seq[i][0]), 
                                                len(SR_seq[i][0][0])])
                L_curr = L_seq[i].astype(float)
            else:
                SR_reshape = [[]]
                L_curr = []
            
            if(O_seq[i] == None):
                O_mat = []
            else:
                O_mat = O_seq[i]
            if(D_seq == None or D_seq[i] == None):
                D_mat = [[]]
            else:
                D_mat = D_seq[i]

            # for the gui
            self.mygm.update_args.append(dict(T_prev=T_mat_prev,
                                              SR_curr=SR_reshape,
                                              D_curr=D_mat,
                                              L_curr=L_curr,
                                              O_curr=O_mat,
                                              vp_index_to_topo_index=self.vp_i_to_topo_i,
                                              num_topologies=len(self.tmap.keys()),
                                              ))
            T_mat = na.transpose(T_mat)
            
            # ret_mat is the observation probability of a transition from vp_1 to vp_2. 
            ret_mat = na.array(tklib_observation_probs(len(self.viewpoints),
                                                       self.vp_i_to_topo_i,
                                                       SR_reshape,
                                                       L_curr,
                                                       O_mat,
                                                       self.topo_to_location_mask,
                                                       len(self.tmap.keys())))
            ret_mat = ret_mat.reshape(len(self.viewpoints), len(self.viewpoints))
            observation_probs = T_mat * ret_mat * D_mat
            T_mat_prev = T_mat
            yield observation_probs

    def infer_path(self, sdcs, loc, sorients_rad):
        prob = 1.0
        path = None
        allow_backtracking = False
        for observation_probs in self.observation_matrices(sdcs, loc, sorients_rad):

            if path == None:
                path = [self.iSloc] 

            if not allow_backtracking:
                self.update_for_backtracking(observation_probs, path)

            here = path[-1]
            next = na.argmax(observation_probs[here])
            prob *= observation_probs[here, next]
            path.append(next)



        path = [self.viewpoints[p] for p in path]
        return path, prob, self.SDC_utilized


    def initialize(self):
        du.models.hri2010_global.model.initialize(self)
        print "reloading matrix"
        self.T_mat_str = self.get_transition_matrix("straight")
        self.T_mat_right = self.get_transition_matrix("right")
        self.T_mat_left = self.get_transition_matrix("left")
        self.topo_to_location_mask = self.get_topo_i_to_location_mask()
        
    def get_transition_matrix(self, direction="straight", p_self=1.0 ):
        """
        Use children and grandchildren
        """
        T_mat = zeros([self.num_regions*self.num_viewpoints, 
                       self.num_regions*self.num_viewpoints])*1.0
        
        if(direction == "straight"):
            new_tmap = self.get_topological_map_viewpoint(pi, 0)
        elif(direction == "right"):
            new_tmap = self.get_topological_map_viewpoint(pi, -1.0*pi/2.0)
        elif(direction == "left"):
            new_tmap = self.get_topological_map_viewpoint(pi, +1.0*pi/2.0)
        
        #for each of the viewpoints
        for i in range(len(self.viewpoints)):
            connections = new_tmap[self.viewpoints[i]]
            
            
            #find the areas connected and if they are reasonable            
            for conn in connections:
                cconn = conn 
                connofconn = [conn]
                connofconn.extend(new_tmap[conn])
                
                #if(i==0):
                #    print "start viewpoint:", self.viewpoints[i]
                #    print "tmap:", self.tmap[0.0], "to", self.tmap_locs[11.0]
                #    print "connections", connofconn
                #    raw_input()

                for conn_i, cconn in enumerate(connofconn):

                    #convert this into topo numbers
                    topo_st, topo_st_ang = self.viewpoints[i].split("_")
                    topo_end, topo_end_ang = cconn.split("_")

                    if(cconn < 0 or self.viewpoints[i] == -1):
                        continue
                    elif(topo_st == topo_end):
                        continue

                    loc1 = self.tmap_locs[float(topo_st)]
                    loc2 = self.tmap_locs[float(topo_end)]

                    #for each of the to-node's orientations, check its relative angle to 
                    #          the from node's orientation and give it a relative probability
                    #          accordingly
                    start_num = self.vpt_to_num[self.viewpoints[i]]
                    end_num = self.vpt_to_num[cconn]

                    #make this dependent on how much we turn in total
                    orient_diff, d_turn = get_total_turn_amount(loc1[0], loc1[1], 
                                                                radians(float(topo_st_ang)),
                                                                loc2[0], loc2[1], 
                                                                radians(float(topo_end_ang)))
                    #going to end_num from i
                    if(direction == 'straight'):
                        T_mat[end_num,start_num] = max(-1.75/pi*abs(orient_diff)+1, 0.0)
                        #T_mat[start_num][end_num] = max(-1.5/pi*abs(orient_diff)+1, 0.0)
                    elif(direction == 'right' and d_turn < 0):
                        diff_from_neg_pi2 = tklib_normalize_theta(d_turn*orient_diff+(pi/2.0))
                        T_mat[end_num,start_num] = max(-2.5/pi*abs(diff_from_neg_pi2)+1, 0.0)
                        #T_mat[start_num][end_num] = max(-1.5/pi*abs(diff_from_neg_pi2)+1, 0.0)
                    elif(direction == 'left' and d_turn > 0):
                        diff_from_pi2 = tklib_normalize_theta(d_turn*orient_diff-(pi/2.0))
                        T_mat[end_num,start_num] = max(-2.5/pi*abs(diff_from_pi2)+1, 0.0)
                        #T_mat[start_num][end_num] = max(-1.5/pi*abs(diff_from_pi2)+1, 0.0)

                    if(not conn == cconn):
                        T_mat[end_num,start_num] = T_mat[end_num,start_num]*0.3
                        
            #connect self transitions
            topo_st, topo_st_ang = self.viewpoints[i].split("_")
            if(direction == "straight"):
                T_mat[i,i] = p_self
            elif(direction == "right"):
                newang = mod(int(float(topo_st_ang))-int(float(self.get_viewpoint_diff())), 360)*1.0
                T_mat[self.vpt_to_num[str(topo_st)+"_"+str(newang)],i] = p_self
            elif(direction == "left"):
                newang = mod(int(float(topo_st_ang))+int(float(self.get_viewpoint_diff())), 360.0)*1.0
                T_mat[self.vpt_to_num[str(topo_st)+"_"+str(newang)],i] = p_self
        
        return T_mat




    # ******************************
    # Something about these targets causes model 16 to get two more right.
    # I *thought* it was redundent with the get_val fix in model13, but
    # it's not.    So we should figure out why it's better and merge it
    # with model9/13.  
    # But this is what was run for HRI 2010.
    # - stefie10, 10/2/2010
    def p_obj1_given_obj2(self, obj1, obj2):
        try: 
            return self.lmap_cache.prior[obj2][obj1] / float(sum([v for v in self.lmap_cache.prior[obj2].values()]))
        except KeyError: 
            return 1e-6

    def p_obj_i_can_see_x(self, i, x):
        vtags, itags_t = self.clusters.tf.get_visible_tags((self.obj_locations[0,i],
                                                           self.obj_locations[1,i]))

        if x in vtags:
            return 1.0
        else:
            return self.p_obj1_given_obj2(x, self.obj_names[i])

    def get_prob_l_is_x_flickr(self, objtype_x):
        return self.get_prob_l_can_see_x_flickr(objtype_x)

    def get_prob_l_can_see_x_flickr(self, obj_type):
        ret_probs = []

        for i, obj_i in enumerate(self.obj_names):
            #get the visibility here
            p_obj_i_can_see_x = self.p_obj_i_can_see_x(i, obj_type)
            if obj_i == obj_type:
                ret_probs.append(1)
            else:
                ret_probs.append(p_obj_i_can_see_x)
        return ret_probs





