from du.models_test import min_entropy_extended
from numpy import *

class model(min_entropy_extended.model):
    """
    This one is a version of wei et al
    * no transition matrix
    * no spatial relations
    """
    
    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename,
                 tag_filename):
        min_entropy_extended.model.__init__(self, clusterfile, cachelmap, 
                                            srelMatFname, map_filename, tag_filename)

    def initialize(self):
        min_entropy_extended.model.initialize(self)
        self.T_mat_uniform = self.get_uniform_transition_matrix()

    def sdc_to_distributions(self, mysdc):
        O_mat, T_mat, SR_mat, L_mat, D_mat = min_entropy_extended.model.sdc_to_distributions(self, mysdc)
        return O_mat, self.T_mat_uniform, None, None, None
    
    
