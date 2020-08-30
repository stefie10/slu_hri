from du.models import hri2010_global
import numpy as na
import cPickle

class model(hri2010_global.model):

    def p_can_see_tag(self, tag, vtags, itags):
        l = self.lmap_cache

        #if(len(vtags) == 0):
        #    return 1e-6
        
        try:
            if any([x in vtags for x in [tag, tag[0:-1], tag[0:-2]]]):
                return 1 - 1e-8
            elif any([x in itags for x in [tag, tag[0:-1], tag[0:-2]]]):        
                return 1e-8
            else:
                if tag in l._p_obj:
                    p_tag = l.sums[tag] /float(l.total_objects)
                else:
                    p_tag = 1e-6
                p_c_i_given_tag = na.prod([l.p_obj1_given_obj2(c_i, tag) for c_i in vtags])
                p_c_i_given_not_tag = na.prod([l.p_obj1_given_no_obj2(c_i, tag) for c_i in vtags])

                p_tag_given_c_i = (p_c_i_given_tag * p_tag) / (p_c_i_given_tag * p_tag + p_c_i_given_not_tag* (1 - p_tag))
                O_mat_entry = p_tag_given_c_i
                assert 0 <= O_mat_entry and O_mat_entry  <= 1, (O_mat_entry)


            return O_mat_entry
        except:
            return 1e-6



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
            
