from sys import argv
from copy import deepcopy
import sys
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
from math import log
from datatypes_lmap import *
from model1 import *

#model 1 is the simplest model... it assumes true
#   observations (even though they will be noisy)
#   this creates datasets and computes
#   the corresponding likelihood
#   map for each of these datasets
def load_location_file(locations_filename):
    loc_file = open(locations_filename, 'r')

    locations = []
    for line in loc_file:
        locations.append(line.strip())
    return locations

def run_model1(objects_filename, 
               flickr_cache, thelogfile, outfilename):

    #load a location file
    loc_info = load_location_file(objects_filename);

    print "creating map likelihood"
    l_map = likelihood_map_model1(loc_info, flickr_cache, thelogfile)

    #note that this uses a random number 
    #    generator, so one should make sure
    #    not to do anything in between.
    mynames = deepcopy(l_map.object_names)
    for elt in mynames:
        print "adding context", elt
        l_map.add_context(elt)

    #print l_map.MAP()

    l_map.mylogfile.gridmap = None

    print "dumping the data"
    cPickle.dump(l_map, open(outfilename+"_m1.pck", 'w'))                  


if __name__=="__main__":
    if(len(argv) == 5):
        print "loading prior"
        run_model1(argv[1], cPickle.load(open(argv[2], 'r')),
                   cPickle.load(open(argv[3], 'r')), argv[4])
    else:
        print "usage:\n\t python run_model1.py loc_filename flickr_cache.pck logfile.pck outfileprefix"



