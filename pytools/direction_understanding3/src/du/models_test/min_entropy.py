from memoized import memoized
import math2d
import naive_bayes
import numpy as na


class model(naive_bayes.model):

    def p_can_see_tag(self, tag, vtags, itags):
        """
        Find the subset of vtags that maximizes the p(x|subset_vtags)
        and use that for the value. 
        """

        l = [[subset_vtags, naive_bayes.model.p_can_see_tag(self, tag, subset_vtags, itags)]
             for subset_vtags in math2d.powerset(vtags) 
             #]
             if len(subset_vtags) <= 3]
        l = na.array(l)
        best = na.argmax(l[:, 1])
        best_subset = l[best][0]
        O_mat_entry = l[best][1]
        if O_mat_entry < 0 or O_mat_entry > 1:
            raise ValueError("Bad omat:  " + `O_mat_entry`)
        return O_mat_entry
    
