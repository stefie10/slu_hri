
from du.dir_util import print_tmat
from du.models_test import min_entropy_extended, naive_bayes
from du.partitions_3d import partitions_3d
from scipy import transpose, ones
import cPickle
import os
import tempfile
import numpy as na

super = min_entropy_extended.model

class model(super):
    
    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename, 
                 tag_filename, **args):
        
        # whole video plan
        #self.boundingBox = [(60, 100), (60, 27), (97, 27), (97, 100)]
        
        # Just Gerry's area
        if "boundingBox" in args:
            self.boundingBox = args["boundingBox"]
        else:
            self.boundingBox = [(63, 100), (63, 74), (80, 74), (80, 100)]

        # area by the entrance
        self.boundingBox = [(60, 94), (78, 94), (78, 120), (60, 120)]
        #self.boundingBox=None
        
        print "clusters", clusterfile.__class__, clusterfile
        tmpfile, newclusterfile = tempfile.mkstemp()
        tmpfile = open(newclusterfile, 'wb')
        cPickle.dump(partitions_3d(clusterfile, self.boundingBox), tmpfile)
        tmpfile.close()
        
        super.__init__(self, newclusterfile, cachelmap, srelMatFname, map_filename,
                       tag_filename, boundingBox=self.boundingBox, **args)
        self.allow_backtracking = True
        os.remove(newclusterfile)
        
        
    def initialize(self):
        super.initialize(self)
        self.T_mat_face = self.get_transition_matrix("face")
        self.T_mat_back = self.get_transition_matrix("back")
        self.T_mat_up = self.get_vertical_transition_matrix("up")
        self.T_mat_down = self.get_vertical_transition_matrix("down")
        self.T_mat_stay = self.get_vertical_transition_matrix("stay")

        
    def get_usable_sdc(self, sdcs):
        output_sdcs = []
        for sdc in naive_bayes.model.get_usable_sdc(self, sdcs):
            if not sdc["kwsdc"]:
                output_sdcs.append(sdc)
                for kw in sdc["landmarks"]:
                    for i in range(0, 0):
                        mysdc = {"figure":None, "sr":sdc["sr"], "verb":"straight", "landmark":kw, 
                                 "kwsdc":True, "landmarks":[kw]}
                        output_sdcs.append(mysdc)

        return output_sdcs
        

    def sdc_to_distributions(self, mysdc):
        """
        Convert the SDC to distributions used in the inference.    
        """
        if "right" in  mysdc["verb"]:
            D_mat = transpose(self.T_mat_right)
        elif "left" in mysdc["verb"]:
            D_mat = transpose(self.T_mat_left)
        elif "turn_around" in mysdc["verb"]:
            D_mat = transpose(self.T_mat_back * self.T_mat_face)
        elif "face" in mysdc["verb"]:
            D_mat = transpose(self.T_mat_face)
        else:
            D_mat = transpose(self.T_mat_str)
        
        
        #print_tmat(transpose(D_mat), 40, 42)                        


    
        if "up" in mysdc["verb"]:
            D_mat = D_mat * transpose(self.T_mat_up)
        elif "down" in mysdc["verb"]:
            D_mat = D_mat * transpose(self.T_mat_down)
        else:
            D_mat = D_mat * transpose(self.T_mat_stay)


        #print_tmat(transpose(D_mat), 40, 42)                            
        

        T_mat = ones([len(D_mat), len(D_mat[0])])*1.0
        
        
        if mysdc["sr"] != None and len(mysdc["landmarks"]) > 0 and self.use_spatial_relations:
            sr_i = self.sr_class.engineToIdx(mysdc["sr"])
            SR_mat = self.srel_mat[sr_i,:,:,:]
            L_mat = self.get_prob_landmark_given_sdc_modifiers(mysdc)
        else:
            SR_mat = None
            L_mat = None
            
        if mysdc["landmark"] != None:
            landmark_i = self.names_to_index[mysdc["landmark"]]
            O_mat_oriented = self.O_mat_oriented[:, landmark_i]
            O_mat_topo = self.O_mat[:, landmark_i]
            if "face" in mysdc["verb"]:
                O_mat = O_mat_oriented
            else:
                O_mat = O_mat_topo
        else:
            O_mat = None
        
        
        return O_mat, T_mat, SR_mat, L_mat, D_mat

