
from du.dir_util import print_tmat
from du.models_test import min_entropy_extended, naive_bayes
from du.partitions_hsp import partitions_hsp
from scipy import transpose, ones
import cPickle
import os
import tempfile

super = min_entropy_extended.model

class model(super):
    
    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename, 
                 tag_filename, **args):

        self.boundingBox=None

        tmpfile, newclusterfile = tempfile.mkstemp()
        tmpfile = open(newclusterfile, 'wb')
        cPickle.dump(partitions_hsp(clusterfile, self.boundingBox), tmpfile)
        tmpfile.close()
        
        super.__init__(self, newclusterfile, cachelmap, srelMatFname, map_filename,
                       tag_filename, boundingBox=self.boundingBox, **args)
        
        



        
    def initialize(self):
        super.initialize(self)
        self.sr_class.tokenToEngine["down"] = self.sr_class.engineMap["down"]
        #self.O_mat = self.O_mat_oriented
        self.T_mat_face = self.get_transition_matrix("face")
        self.T_mat_back = self.get_transition_matrix("back")
        self.T_mat_up = self.get_vertical_transition_matrix("up")
        self.T_mat_down = self.get_vertical_transition_matrix("down")
        self.T_mat_stay = self.get_vertical_transition_matrix("stay")

        self.allow_backtracking = True
    def get_usable_sdc(self, sdcs):
        output_sdcs = []
        for sdc in naive_bayes.model.get_usable_sdc(self, sdcs):
            if not sdc["kwsdc"] and not sdc["landmark"] == "EPSILON":
                output_sdcs.append(sdc)

        
                #output_sdcs.append({"figure":None, "sr":None, "verb":"face", 
                #            "landmark":output_sdcs[-1]["landmark"], 
                #            "kwsdc":False, "landmarks":output_sdcs[-1]["landmark"]})
        return output_sdcs
        

    def sdc_to_distributions(self, mysdc):
        """
        Convert the SDC to distributions used in the inference.    
        """
        print "*******************************"
        if "right" in  mysdc["verb"]:
            D_mat = transpose(self.T_mat_right)
        elif "left" in mysdc["verb"]:
            D_mat = transpose(self.T_mat_left)
        elif "turn_around" in mysdc["verb"]:
            D_mat = transpose(self.T_mat_back * self.T_mat_face)
        elif "face" in mysdc["verb"]:
            print "using face"
            D_mat = transpose(self.T_mat_face)
        else:
            D_mat = transpose(self.T_mat_str)
            D_mat = ones(self.T_mat_str.shape)
        
        
        
        print "before vertical"
        print_tmat(transpose(D_mat), 40, 42)                        


    
        if "up" in mysdc["verb"]:
            print "using up"
            D_mat = D_mat * transpose(self.T_mat_up)
        elif "down" in mysdc["verb"]:
            D_mat = D_mat * transpose(self.T_mat_down)
        else:
            print "using stay"
            D_mat = D_mat * transpose(self.T_mat_stay)

        print "dmat final"
        print_tmat(transpose(D_mat), 40, 42)                            
        

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
                print "using O_mat_oriented"
                O_mat = O_mat_oriented
            else:
                O_mat = O_mat_topo
            print "shape", O_mat_topo.shape
            print "O_mat_topo", O_mat_topo[18]
            print "O_mat_oriented", O_mat_oriented[18]
        else:
            O_mat = None
        
        
        return O_mat, T_mat, SR_mat, L_mat, D_mat

    def createGround(self, l):
        return self.createGroundFromPolygon(l)
