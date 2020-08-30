from sys import argv
import sys
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
from math import log
from datatypes_lmap import *

class likelihood_map_model1(likelihood_map):
    
    def add_context(self, obj_name):
        self.likelihood_map[obj_name] = []
        
        #if there are none
        if(len(self.mylogfile.path_pts_unique) == 0):
            return

        print "**************adding " + obj_name + "***************"
        #when we iterate through them
        for i in range(len(self.mylogfile.path_pts_unique[0])):
            #print "i=", i,  " of ", len(self.mylogfile.path_pts_unique[0]), " grid cells"
            vobjs = self.mylogfile.visible_objects[i]
            
            #compute the posterior
            v = exp(self.compute_posterior(obj_name, vobjs))
            self.likelihood_map[obj_name].append(v)

    def compute_posterior(self, obj_name, vpolygons):
        
        if(not obj_name in self.flickr_cache.tagnames):
            print "bad context name"
            sys.exit(0)
        
        visible_objects = []
        for elt in vpolygons:
            print "visible:", elt.tag
            visible_objects.append(elt.tag)

        numer = log(1.0)
        denom = log(1.0)
        for tag in self.known_classes:
            #if(not tag in self.known_classes):
            #    continue
            
            if(not tag in visible_objects):
                pos_prob = self.flickr_cache.get_val(tag, False, obj_name, True)
                neg_prob = self.flickr_cache.get_val(tag, False, obj_name, False)
            else:
                pos_prob = self.flickr_cache.get_val(tag, True,  obj_name, True)
                neg_prob = self.flickr_cache.get_val(tag, True, obj_name, False)


            numer = numer + pos_prob
            denom = denom + neg_prob
        

        
        ret_prob = numer - log(exp(numer) + exp(denom))

        return ret_prob

