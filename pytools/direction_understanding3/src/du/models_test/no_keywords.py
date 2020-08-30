import min_entropy
import numpy as na

class model(min_entropy.model):
    """
    Don't use keyword SDCs.
    """

    def get_usable_sdc(self, sdcs):
        return [sdc for sdc in min_entropy.model.get_usable_sdc(self, sdcs) 
                if not sdc["kwsdc"]]

    def sdc_to_distributions(self, mysdc):
        single_O_mat, T_mat, SR_mat, L_mat, D_mat = min_entropy.model.sdc_to_distributions(self, mysdc)
        if len(mysdc["landmarks"]) > 0:
            O_mat = na.ones(single_O_mat.shape) * 1.0
            for landmark in mysdc["landmarks"]:
                O_mat *= self.O_mat[:,self.names_to_index[landmark]]
        else:
            O_mat = single_O_mat
                
        return O_mat, T_mat, SR_mat, L_mat, D_mat

                                      
                
        
        

        

