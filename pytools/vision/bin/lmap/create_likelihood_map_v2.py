from carmen_maptools import *
from annote_utils import *
from sys import argv
import sys
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
import cPickle
from math import log
#from datatypes_lmap import *
from tag_util import tag_file

#pt is in x, y
#pts are indicies
#mymap is a tklib_log_gridmap
class map_likelihood_simple:
    
    def __init__(self, tf, prior, myskeleton):
        self.curr_posterior_num = {}
        self.curr_posterior_denom = {}
        self.prior = prior
        self.skeleton = myskeleton
        self.free_pts =  self.skeleton.ind_to_xy(self.skeleton.get_skeleton_indices())
        
        self.tf = tf
        
        self.likelihood_map = {}
        self.object_names = tf.get_tag_names()

    def initialize_object_list(self, poly, pts):
        objects_all = []

        for elt in pts:
            if(not elt.tag in objects_all):
                objects_all.append(elt.tag)
            
        for elt in poly:
            if(not elt.tag in objects_all):
                objects_all.append(elt.tag)

        return objects_all
        
    def get_lmap(self, object_name):
        
        gridmap = self.skeleton.get_map()
        
        ix = gridmap.get_map_width()
        iy = gridmap.get_map_height()
        
        lmap = zeros([ix,iy])*1.0
        
        I = array(self.skeleton.get_skeleton_indices())
        
        #print "len:", len(I), len(I[0])
        
        #tmp_lmap = []
        for i in range(len(I[0])):

            #print i
            #print "I", I
            #print "I[:,i]", I[:,i]
            ix, iy = I[:,i]
            lmap[ix,iy]=exp(self.likelihood_map[object_name][i])

            #tmp_lmap.append(exp(self.likelihood_map[object_name][i]))

            #if(lmap[ix,iy] > 0.1):
            #print "val: ", ix, iy, "-->", lmap[ix,iy]
            #lmap[ix,iy]=self.likelihood_map[object_name][i]

        #print "argmax:", argmax(tmp_lmap)
        #print "max:", max(tmp_lmap)
        
        return lmap

    def p_tag_given_objs(self, obj_name, tag):
        
        if(self.prior.has_key(obj_name) and self.prior[obj_name].has_key(tag)):
            return (1.0*self.prior[obj_name][tag])/(sum(self.prior[obj_name].values())+10e-6)

        return 10e-6
        

    def compute_posterior_norm(self, obj_name, visible_objects):
        if(not self.curr_posterior_num.has_key(obj_name)):
            self.curr_posterior_num[obj_name] = {}

        ret_prob = 0.0
        for tag in visible_objects:
            #check for the denominator
            denom = None
            if(self.curr_posterior_denom.has_key(obj_name)):
                denom = self.curr_posterior_denom[obj_name]
            elif(self.prior.has_key(obj_name)):
                denom = sum(self.prior[obj_name].values())+1
                self.curr_posterior_denom[obj_name] = denom
            else:
                denom = 1
                self.curr_posterior_denom[obj_name] = denom

            
            #check for the numerator
            num = None
            if(self.curr_posterior_num.has_key(obj_name) 
               and self.curr_posterior_num[obj_name].has_key(tag)):
                num = self.curr_posterior_num[obj_name][tag]

            elif(self.prior.has_key(obj_name) 
                 and self.prior[obj_name].has_key(tag)):
                num = self.prior[obj_name][tag]
                self.curr_posterior_num[obj_name][tag] = num
                #print "adding to cache", obj_name, tag, "of", num
                #raw_input()
            else:
                num = 10e-10
                self.curr_posterior_num[obj_name][tag] = num

            if(num/(1.0*denom) >  ret_prob):
                ret_prob = num/(1.0*denom)
            
        return ret_prob
    
    def get_lmap_nn(self, object_name, minval=0.0):
        xyFree =  array(self.tf.get_map().get_free_locations());
        indFree =  array(self.tf.get_map().get_free_inds());
        
        if(len(xyFree) == 0):
            return None
        
        #make the gridmap
        ix = self.tf.get_map().get_map_width()
        iy = self.tf.get_map().get_map_height()
        lmap = zeros([ix,iy])*1.0


        #get the nearest neighbors
        #print "starting nearest neighbors"
        self.I_nn = NNs_index(xyFree, self.free_pts)
            
        #print "filling out lmap"
        #fill out the likelihood map
        for i in range(len(self.I_nn)):
            ix, iy = indFree[:,i]
            
            v = self.likelihood_map[object_name][int(self.I_nn[i])]
            #print v
            
            if(v > minval):
                lmap[ix,iy] = v

        #print self.likelihood_map[object_name]
        #print "object_name", object_name
        #raw_input("press something")

        return lmap

    def add_context(self, obj_name):
        self.likelihood_map[obj_name] = []
        
        #if there are none
        if(len(self.free_pts) == 0):
            return
        
        print "**************adding " + obj_name + "***************"
        #when we iterate through them
        for i in range(len(self.free_pts[0])):
            if(mod(i, 500) == 0):
                print "i=", i,  " of ", len(self.free_pts[0]), " grid cells"
            x, y = self.free_pts[:,i]
            #vpts = get_visible_points([x,y], self.pts, self.skeleton.get_map())
            #vpolys = get_visible_polygons([x,y], self.poly, self.skeleton.get_map())        
            #vpolys.extend(vpts);

            vtags, itags =  self.tf.get_visible_tags([x,y])
            
            #compute the posterior
            #print vtags
            v = self.compute_posterior_norm(obj_name, vtags)
            self.likelihood_map[obj_name].append(v)
            
            '''if(len(vtags) > 0):
                print [x, y]
                print vtags
                print "v=", v'''
            #raw_input()
            


    def MAP(self):
        MAP = []
        
        for i in range(len(self.likelihood_map[self.likelihood_map.keys()[0]])):
            max_class = "";
            max_val = -10000;
            print "*************"
            all_zero = True
            for elt in self.likelihood_map.keys():
                print elt, self.likelihood_map[elt][i]
                if(self.likelihood_map[elt][i] > max_val):
                    max_val = self.likelihood_map[elt][i]
                    max_class = elt

                if(self.likelihood_map[elt][i] < 0.0):
                    all_zero = False

            if(all_zero == True):
                print "adding unknown"
                print "*******************"
                MAP.append('unknown')
            else:
                MAP.append(max_class)

        return MAP



def compute_most_likely_locations(map_filename, tag_filename, prior, skeleton_filename):
                                  

    myspline = cPickle.load(open(skeleton_filename, 'r'))
    
    print "loading polygons"
    #load the tag file
    tf =  tag_file(tag_filename, map_filename)
    
    print "getting likelihood map"
    l_map = map_likelihood_simple(tf, prior, myspline)
    
    print "map filename:", l_map.skeleton.map_filename
    #################
    #debug information
    #ion()
    #figure()
    #tkmap = l_map.skeleton.get_map()
    #plot_map(tkmap.to_probability_map_carmen(), 
    #         tkmap.x_size, tkmap.y_size)
    #x, y = [36.4, 31.5]
    #vpts = get_visible_points([x,y], l_map.pts, l_map.skeleton.get_map())
    #vpolys = get_visible_polygons([x,y], l_map.poly, l_map.skeleton.get_map()) 
    #for elt in vpts:
    #    print elt.tag
    #for elt in vpolys:
    #    print elt.tag
    #plot([x], [y], 'ro')
    #draw()
    #raw_input("waiting")
    #################

    #for elt in loc_info:
    #    print "adding context", elt
    l_map.add_context("zebra")
    #print l_map.MAP()
    print "getting nearest neighbors"
    ret_lmap =  l_map.get_lmap_nn("zebra")
    

    l_map.skeleton.gridmap = None
    l_map.tf = None
    print "dumping"
    cPickle.dump(ret_lmap, open("test_out.pck", 'w'))



if __name__=="__main__":
    if(len(argv) == 5):
        print "loading prior"
        compute_most_likely_locations(argv[1], argv[2], cPickle.load(open(argv[3], 'r')),argv[4])
                                      
    else:
        print "usage:\n\t python flickr_compute_most_likely_locations.py map_filename tag_file prior spline_file"



