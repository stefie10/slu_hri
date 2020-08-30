import math
import min_entropy_extended
import numpy as na
import os
import cProfile
from du.srel_utils import loadSrelMatrix

def nthbit(integer, n):
    return (integer >> n) & 1

super = min_entropy_extended.model

class model(super):
    def initialize(self):
        super.initialize(self)
        basename, ext = os.path.splitext(self.srelMatFname)
        self.normalizedSrelMatFname = basename + "-normalized" + ext

        print "fname", self.normalizedSrelMatFname
        self.original_srel_mat = self.srel_mat
        
        if not os.path.exists(self.normalizedSrelMatFname):
            self.ones = na.ones((len(self.tmap), len(self.tmap), 
                                 len(self.obj_locations[0])))
            #cProfile.runctx("self.srel_mat = self.normalize_srel_mat(self.original_srel_mat)", globals(), locals(), "out.prof")
            self.srel_mat = self.normalize_srel_mat(self.original_srel_mat)
            print "saving", self.normalizedSrelMatFname, "..."
            self.srel_mat.tofile(self.normalizedSrelMatFname)
            print "done saving"
        else:
            self.srel_mat = loadSrelMatrix(self.normalizedSrelMatFname, self.srel_mat_expected_shape())

        
    def p_phi_sr_given_t_o(self, srel_mat, sr_i, phi_value, dest):
        dest[:] = srel_mat[sr_i]
        if not phi_value:
            na.subtract(self.ones, dest, dest)
            
    def normalize_srel_mat(self, srel_mat):

        print "normalizing"
        new_srel = na.zeros(srel_mat.shape)
        working_srel = na.zeros(srel_mat.shape)

        for sr0_i, sr0 in enumerate(self.spatial_relations):
            #if sr0 != "to":
            #    continue
            print "doing", sr0
            count = 0
            for packed_phi in range(int(math.pow(2, len(self.spatial_relations)))):

                Phi = [nthbit(packed_phi, sr_i) 
                       for sr_i, sr in enumerate(self.spatial_relations)]
                print "phi", Phi
                phi_sr0 = Phi[sr0_i]
                if sum(Phi) != 0 and phi_sr0 != 0:
                    value = float(phi_sr0) / sum(Phi)
                    for sr_i, sr in enumerate(self.spatial_relations):
                        self.p_phi_sr_given_t_o(srel_mat, sr_i, Phi[sr_i], working_srel[sr_i])
                    p_phi_sr_given_t_o = na.prod(working_srel, axis=0)
                    
                    new_srel[sr0_i] += value * p_phi_sr_given_t_o
                    count += 1
            print "done", sr0
            print


        assert new_srel.shape == srel_mat.shape, (new_srel.shape, srel_mat.shape)
        return new_srel
