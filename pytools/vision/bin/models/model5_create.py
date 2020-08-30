from Inference import *
from sys import argv
import sys
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
from math import log
from glob import glob
from datatypes_lmap import *
from model5 import *
import psyco


def create_model5(pclass_log_dir,flickr_cache, thelogfile, outfilename):
    #load a location file
    myfiles = glob(pclass_log_dir+"/*.log")

    print "creating map likelihood"
    l_map = likelihood_map_model5([], flickr_cache, thelogfile)

    #note that this uses a random number 
    #    generator, so one should make sure
    #    not to do anything in between.
    
    psyco.full()   
    l_map.create_model(myfiles)
    l_map.mylogfile.gridmap = None
    
    print "dumping the data"
    cPickle.dump(l_map, open(outfilename+"_m5.pck", 'w'))

if __name__=="__main__":
    if(len(argv) == 5):
        print "loading prior"
        create_model5(argv[1], cPickle.load(open(argv[2], 'r')),
                     	        cPickle.load(open(argv[3], 'r')), argv[4])
    else:
        print "usage:\n\t python run_model3.py pclass_log_dir flickr_cache.pck logfile.pck outfileprefix"
