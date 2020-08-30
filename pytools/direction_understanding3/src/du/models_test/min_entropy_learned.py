import cPickle
import math2d
import learned_landmark
import numpy as na

class model(learned_landmark.model):
    
    def p_can_see_tag(self, tag, vtags, itags):
        """
        Find the subset of vtags that maximizes the p(x|subset_vtags)
        and use that for the value. 
        """

        if tag in vtags:
            return 1 - 1e-8
        elif tag in itags:
            return 1e-8

            
        l = [[subset_vtags, learned_landmark.model.p_can_see_tag(self, tag, subset_vtags, itags)]
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
    
    def get_usable_sdc(self, sdcs):
        output_sdcs = []
        for sdc in learned_landmark.model.get_usable_sdc(self, sdcs):
            #if(sdc["kwsdc"]==True):
            #    continue
            output_sdcs.append(sdc)

            for kw in sdc["landmarks"]:
                mysdc = {"figure":None, "sr":None, "verb":"straight", "landmark":kw, 
                         "kwsdc":True, "landmarks":[kw]}
                output_sdcs.append(mysdc)
            
            #if len(sdc["landmarks"]) == 1:
            #kw = sdc["landmark"]
            #if(sdc["landmarks"] == None):
            #    continue
            
            #for kw in sdc["landmarks"]:
            #    for i in range(3):
            #        mysdc = {"figure":None, "sr":None, "verb":"straight", "landmark":kw, 
            #                 "kwsdc":True, "landmarks":[kw]}
            #        output_sdcs.append(mysdc)
                    
        #for sdc in output_sdcs:
        #    print sdc
        #raw_input()
        return output_sdcs

    def load_lmap(self, fname):
        print "loading lmap", fname
        f = open(fname, "r")
        self.lmap_cache = cPickle.load(f)
        f.close()
        mynames = self.lmap_cache.tagnames
        
        
        #get the non-redundant names
        self.mynames = []
        for elt in mynames:
            if not elt in self.mynames:
                if (not "lda" in self.__module__ or
                    not elt in ["room", "type", "back", "area", "end", 
                                "intersection", "set", "space", "facing", 
                                "corner", "keep", "carpet", "grey", "gray", 
                                "stand", "till", "way", "ceiling", "cross", 
                                "number", "lead", "point", "row", "first"]):
                    self.mynames.append(elt)
        self.mynames.extend(self.clusters.tf.get_tag_names())    
        self.mynames.append('EPSILON')
    

        #get a tag name to index hash
        i = 0
        self.names_to_index = {}
        for elt in self.mynames:
            self.names_to_index[elt] = i
            i+=1
            
