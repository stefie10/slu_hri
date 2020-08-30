from sys import argv
import sys
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
from math import log
from datatypes_lmap import *
from model2 import *
from copy import deepcopy

def load_location_file(locations_filename):
    loc_file = open(locations_filename, 'r')

    locations = []
    for line in loc_file:
        locations.append(line.strip())
    return locations


def test_run_model2(objects_filename, 
                    flickr_cache, thelogfile):
    
    #load a location file
    loc_info = load_location_file(objects_filename);

    thelogfile.tp = 0.98
    thelogfile.tn = 0.98

    print "creating map likelihood"
    l_map = likelihood_map_model2(loc_info, flickr_cache, thelogfile)

    while(1):
        i = randint(0,len(l_map.mylogfile.path_pts_unique[0])-1)
        #i = 300
        print "location:", i
        
        vobjs = l_map.mylogfile.visible_objects[i]
        print "*****************"
        
        print "visible objects"
        mynames = deepcopy(l_map.object_names)
        #mynames = deepcopy(l_map.known_classes)
        for elt in vobjs:
            print elt.tag
            if(not elt.tag in mynames):
                mynames.append(elt.tag)


        print "*****************"
        print "inference names"
        for elt in mynames:
            print elt
        print "*****************"
        
        myinf, hnodes = l_map.create_model(mynames, vobjs)
        for elt in hnodes:
            probs = myinf.marginal(elt)
            print elt.name, "->", probs

        raw_input()

if __name__=="__main__":
    if(len(argv) == 4):
        print "loading prior"
        test_run_model2(argv[1], cPickle.load(open(argv[2], 'r')),
                        cPickle.load(open(argv[3], 'r')))
    else:
        print "usage:\n\t python run_model2.py loc_filename lmap_cache.pck logfile.pck"



