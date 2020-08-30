import du.models.hri2010_global
from numpy import *

class model(du.models.hri2010_global.model):
    """
    This one is a version of wei et al
    * no transition matrix
    * no spatial relations
    """
    
    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename,
                 tag_filename):
        du.models.hri2010_global.model.__init__(self, clusterfile, cachelmap, 
                                                srelMatFname, map_filename, tag_filename)

    def initialize(self):
        du.models.hri2010_global.model.initialize(self)
        self.T_mat_uniform = self.get_uniform_transition_matrix()

    def sdc_to_distributions(self, mysdc):
        O_mat, T_mat, SR_mat, L_mat, D_mat = du.models.hri2010_global.model.sdc_to_distributions(self, mysdc)
        return O_mat, self.T_mat_uniform, None, None, None
    
    
