import cPickle
import math2d
import naive_bayes
import numpy as na

class model(naive_bayes.model):
    
    def p_can_see_tag(self, tag, vtags, itags):
        """
        Find the subset of vtags that maximizes the p(x|subset_vtags)
        and use that for the value. 
        """

        if any([x in vtags for x in [tag, tag[0:-1], tag[0:-2]]]):
            return 1 - 1e-8
        elif any([x in itags for x in [tag, tag[0:-1], tag[0:-2]]]):        
            return 1e-8

            
        l = [[subset_vtags, naive_bayes.model.p_can_see_tag(self, tag, subset_vtags, itags)]
             for subset_vtags in math2d.powerset(vtags) 
             if 1 <= len(subset_vtags) <= 3]
        l = na.array(l)
        if len(l) == 0:
            return naive_bayes.model.p_can_see_tag(self, tag, [], itags)
        else:
            best = na.argmax(l[:, 1])
            O_mat_entry = l[best][1]
            assert 0 <= O_mat_entry <= 1, O_mat_entry
            return O_mat_entry
    
    def get_usable_sdc(self, sdcs):
        output_sdcs = []
        for sdc in naive_bayes.model.get_usable_sdc(self, sdcs):
            if not sdc["kwsdc"]:
                output_sdcs.append(sdc)
                for kw in sdc["landmarks"]:
                    for i in range(0, 2):
                        mysdc = {"figure":None, "sr":sdc["sr"], "verb":"straight", "landmark":kw, 
                                 "kwsdc":True, "landmarks":[kw]}
                        output_sdcs.append(mysdc)

        return output_sdcs
