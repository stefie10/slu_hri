import naive_bayes
import numpy as na


class model(naive_bayes.model):
    
    def p_can_see_tag(self, tag, vtags, itags):
        """
        Find the subset of vtags that maximizes the p(x|subset_vtags)
        and use that for the value. 
        """
        
        l = self.lmap_cache
        l = [l.p_obj1_given_obj2(tag, vtag) for vtag in vtags]

        O_mat_entry = na.max(l)
        if tag in vtags:
                O_mat_entry = 1 - 1e-6
                
                
        if O_mat_entry < 0 or O_mat_entry > 1:
            raise ValueError("Bad omat:  " + `O_mat_entry`)
        return O_mat_entry
    
