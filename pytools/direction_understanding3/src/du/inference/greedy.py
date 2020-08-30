from du import composedModel
from du.models.hri2010_greedy_1step import FakeGm
from math import degrees
from numpy import transpose
from pyTklib import kNN_index, tklib_du_lp_obs_array
import numpy as na

class model(composedModel.model):
    """
    look ahead two, but no more, with composition so it can run on any model. 
    """
    def __init__(self, m4du):
        composedModel.model.__init__(self, m4du)

    def update_for_backtracking(self, observation_probs, path):
        for p in path:
            p_topo_i = self.m4du.vp_i_to_topo_i[p]
            for i in range(len(self.m4du.viewpoints)):
                i_topo_i = self.m4du.vp_i_to_topo_i[i]
                if p != i:
                    observation_probs[i, p] = 0


    def observation_matrices(self, sdcs, loc, sorients_rad):
        """
        Yield the sequence of observationmatrices for each SDC.  This
        combines p_obs and p_trans.
        """

        print "beginning greedy search, NOT viterbi.  It's called viterbi for compatability."
        
        i, = kNN_index(loc, transpose(self.tmap_locs.values()), 1)
        iSlocTopo = self.tmap_locs.keys()[int(i)]

        orients = self.get_viewpoint_orientations(self.num_viewpoints)
        i_tmp, = kNN_index([degrees(sorients_rad[0])], [orients], 1);
        self.iSloc = self.vpt_to_num[str(iSlocTopo)+"_"+str(orients[i_tmp])]
        
        print "preparing"
        T_seq, O_seq, SR_seq, L_seq, D_seq, self.SDC_utilized, newpi = self.m4du.inference_prepare(sdcs, loc, sorients_rad)
        

        print "looping"
        self.mygm = FakeGm()
        self.mygm.T_seq = T_seq

        
        
        for i, (T_mat) in enumerate(T_seq):

            if(not len(SR_seq) == 0 and not SR_seq[i] == None):
                SR_reshape = SR_seq[i].reshape([len(SR_seq[i])*len(SR_seq[i][0]), 
                                                len(SR_seq[i][0][0])]) + 10e-6
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
            self.mygm.update_args.append(dict(SR_curr=SR_reshape,
                                              D_curr=D_mat,
                                              L_curr=L_curr,
                                              O_curr=O_mat,
                                              vp_index_to_topo_index=self.m4du.vp_i_to_topo_i,
                                              num_topologies=len(self.tmap.keys()),
                                              ))

            # ret_mat is the observation probability of a transition from vp_1 to vp_2. 
            ret_mat = na.exp(na.array(tklib_du_lp_obs_array(len(self.m4du.viewpoints),
                                                            self.m4du.vp_i_to_topo_i + 0.0,
                                                            na.log(T_mat), na.log(D_mat),
                                                            na.log(SR_reshape),
                                                            na.log(L_curr),
                                                            na.log(O_mat),
                                                            self.m4du.topo_i_to_location_mask,
                                                            len(self.m4du.tmap.keys()))))
            ret_mat = ret_mat.reshape(len(self.m4du.viewpoints), len(self.m4du.viewpoints))
            observation_probs = ret_mat
            
            yield observation_probs


    def initialize(self):
        composedModel.model.initialize(self)
        
    def infer_path(self, sdcs, loc, sorients_rad=None):

        if(sorients_rad != None):
            #return  self.infer_path_rec(sdcs, loc, sorient_rad)
            orientations = sorients_rad
        else:
            orientations = self.m4du.get_viewpoint_orientations(self.m4du.num_viewpoints)

        best_path = None
        best_prob = -1
        best_sdc_u = None

        #print "orientations:", sorients_rad
        for orient in orientations:
            #path, prob, sdc_u = self.infer_path_rec(sdcs, loc, [radians(orient)])
            path, prob, sdc_u = self.infer_path_rec(sdcs, loc, [orient])
            
            if prob > best_prob:
                best_prob = prob
                best_path = path
                best_sdc_u = sdc_u

        return best_path, best_prob, sdc_u


    def infer_path_rec(self, sdcs, loc, sorients_rad=None):
        prob = 1.0
        
        #make the assumption that we only care about the first element
        o_ps = list(self.observation_matrices(sdcs, loc, sorients_rad))
        path = [self.iSloc] + [None for x in o_ps]
        
        allow_backtracking = False

        for i, o_p in enumerate(o_ps):
            #print "op", o_p.shape
            here = path[i]
            if not allow_backtracking:
                self.update_for_backtracking(o_p, path)

            if i+1 >= len(self.SDC_utilized):
                # last time through
                next = na.argmax(o_p[here])                
                path[i+1] = next
                prob = prob * o_p[here, next]
            else:
                next_probs = o_ps[i+1]

                # for all i
                vp_scores = na.zeros(len(self.m4du.viewpoints))
                for vp_i in range(len(self.m4du.viewpoints)):
                    vp_scores[vp_i] = o_p[here, vp_i] * na.max(next_probs[vp_i, :])
                
                next = na.argmax(vp_scores)
                path[i+1] = next
                #print "prob before multiply", prob
                prob = prob * o_p[here, next]
                #print "prob after multiply", prob

        path = [self.m4du.viewpoints[p] for p in path]
        #print "prob", prob
        return path, prob, self.SDC_utilized




