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
from datatypes_lmap import *


def load_location_file(locations_filename):
    loc_file = open(locations_filename, 'r')

    locations = []
    for line in loc_file:
        locations.append(line.strip())
    return locations

def compute_most_likely_locations(locations_filename, tag_filename, lmap_cache, 
                                  skeleton_filename==None, 
                                  log_filename==None, map_filename==None):


    loc_info = load_location_file(locations_filename);
    
    print "loading polygons"
    #load the tag file
    poly, pts = load_polygons(tag_filename)
    
    if(skeleton_filename != None):
        myspline = load(open(skeleton_filename, 'r'))
        
        print "opening skeleton file"
        l_map = map_likelihood(loc_info, pts, 
                               poly, lmap_cache, myspline)

    elif(log_filename != None):
        print "opening logfile"
        thelogfile = logfile_lmap(log_filename, map_filename)
        
        l_map = map_likelihood(loc_info, pts, 
                               poly, lmap_cache, mylogfile=thelogfile)

    print "map filename:", l_map.skeleton.map_filename
    for elt in loc_info:
        print "adding context", elt
        l_map.add_context(elt)

    print l_map.MAP()

    l_map.mypath.gridmap = None
    print "dumping"
    cPickle.dump(l_map, open("test_out.pck", 'w'))                           



if __name__=="__main__":
    if(len(argv) == 5):
        print "loading prior"
        compute_most_likely_locations(argv[1], argv[2], 
                                      cPickle.load(open(argv[3], 'r')),
                                      argv[4])
    else:
        print "usage:\n\t python create_likelihood_map_v3.py loc_filename tag_file lmap_cache spline_file"



