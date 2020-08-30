import du.models.hri2010_global 
from du.inference.align_gm import *

class model(du.models.hri2010_global.model):

    def infer_path(self, sdcs, loc, sorient_rad=None):
        
        print "performing local L_seq opt"
        dists = self.inference_prepare(sdcs, loc, sorient_rad)
        
        T_seq, O_seq, SR_seq, L_seq, D_seq, SDC_utilized, newpi = dists
        #Create the model and perform the inference here
        self.mygm = align_gm(SDC_utilized, T_seq, O_seq, SR_seq, L_seq, newpi, 
                             self.viewpoints,self.vp_i_to_topo_i, self.reg_to_vis_locations_mask, 
                             len(self.tmap_keys), D_seq)
        
        mypath, myprob = self.mygm.inference()
        
        #return the relevant things
        return mypath, myprob, SDC_utilized

