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

#model 2 includes uncertainty in the measurements
#   it assumes true observations (even though they will be noisy)

def run_model5(l_map, outfilename, num_iterations=100):
    l_map.my_inference.bpIterations = num_iterations
    print "performing inference with ", l_map.my_inference.bpIterations, " iterations"
    l_map.perform_inference()
    l_map.mylogfile.gridmap = None
    
    print "dumping the data"
    cPickle.dump(l_map, open(outfilename+"_m5_run.pck", 'w'))

if __name__=="__main__":
    if(len(argv) == 3):
        print "loading model"
        run_model5(cPickle.load(open(argv[1], 'r')), argv[2])
    elif(len(argv) == 4):
        print "loading model"
        run_model5(cPickle.load(open(argv[1], 'r')), argv[2], int(argv[3]))
    else:
        print "usage:\n\t python run_model3.py mymodel.pck outfilename [num_iterations]"

