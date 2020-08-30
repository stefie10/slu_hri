from Inference import *
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

#model 2 includes uncertainty in the measurements
#   it assumes true observations (even though they will be noisy)

def load_location_file(locations_filename):
    loc_file = open(locations_filename, 'r')

    locations = []
    for line in loc_file:
        locations.append(line.strip())
    return locations

def run_model2(objects_filename, 
               flickr_cache, thelogfile, outfilename):

    #load a location file
    loc_info = load_location_file(objects_filename)

    print "creating map likelihood"
    l_map = likelihood_map_model2(loc_info, flickr_cache, thelogfile)

    #note that this uses a random number 
    #    generator, so one should make sure
    #    not to do anything in between.
    print "performing inference for:"
    for elt in loc_info:
        print elt
    
    l_map.perform_inference()
    l_map.mylogfile.gridmap = None

    print "dumping the data"
    cPickle.dump(l_map, open(outfilename+"_m2.pck", 'w'))


if __name__=="__main__":
    if(len(argv) == 5):
        print "loading prior"
        run_model2(argv[1], cPickle.load(open(argv[2], 'r')),
                   cPickle.load(open(argv[3], 'r')), argv[4])
    else:
        print "usage:\n\t python run_model2.py loc_filename flickr_cache.pck logfile.pck outfileprefix"



