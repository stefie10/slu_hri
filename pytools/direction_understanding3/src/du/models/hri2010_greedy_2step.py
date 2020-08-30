import du.models.hri2010_greedy_1step
from numpy import *
import numpy as na

class FakeGm:
    def __init__(self, update_args):
        self.update_args = update_args

class model(du.models.hri2010_greedy_1step.model):
    """
    look ahead two, but no more. 
    """
    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename,
                 tag_filename):
        du.models.hri2010_greedy_1step.model.__init__(self, clusterfile, cachelmap, 
                                                      srelMatFname, map_filename, tag_filename)
        print "loaded"

    def infer_path(self, sdcs, loc, sorients_rad=None):

        if(sorients_rad != None):
            #return  self.infer_path_rec(sdcs, loc, sorient_rad)
            orientations = sorients_rad
        else:
            orientations = self.get_viewpoint_orientations(self.num_viewpoints)

        best_path = None
        best_prob = -1
        best_sdc_u = None

        #print "orientations:", sorients_rad
        for orient in orientations:
            #path, prob, sdc_u = self.infer_path_rec(sdcs, loc, [radians(orient)])
            path, prob, sdc_u = self.infer_path_rec(sdcs, loc, [orient])
            
            if(prob > best_prob):
                best_prob = prob
                best_path = path
                best_sdc_u = sdc_u

        return best_path, best_prob, sdc_u


    def infer_path_rec(self, sdcs, loc, sorients_rad=None):
        prob = 1.0
        
        #make the assumption that we only care about the first element
        o_ps = list(self.observation_matrices(sdcs, loc, sorients_rad))
        path = [self.iSloc] + [None for x in o_ps]
        
        allow_backtracking = True

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
                vp_scores = zeros(len(self.viewpoints))
                for vp_i in range(len(self.viewpoints)):
                    vp_scores[vp_i] = o_p[here, vp_i] * na.max(next_probs[vp_i, :])
                
                next = na.argmax(vp_scores)
                path[i+1] = next
                #print "prob before multiply", prob
                prob = prob * o_p[here, next]
                #print "prob after multiply", prob

        path = [self.viewpoints[p] for p in path]
        #print "prob", prob
        return path, prob, self.SDC_utilized



