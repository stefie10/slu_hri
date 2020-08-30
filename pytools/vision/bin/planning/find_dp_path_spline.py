from sys import argv, exit
import cPickle
from pylab import *
from math import exp
from scipy import *
from random import randint
from copy import deepcopy
from datatypes_lmap import *
import carmen_maptools
from sorting import *
from datatypes_dp import *
from create_likelihood_map_v2 import *


def plot_likelihood_map(object_type, lmap, steps=5):
    pd = path_finding_dp_spline(object_type, lmap, steps)

    #compute the optimal path
    X, Y = pd.compute_optimal_path()

    #plot the map
    mymap = lmap.skeleton.get_map()
    themap = mymap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, mymap.x_size, mymap.y_size);

    plot(X, Y, 'ro-');

    title("search for "+ object_type)
    pd.lmap.skeleton.gridmap = None
    
    print "dumping dp solution"
    cPickle.dump(pd, open(object_type+'_dp_soln.pck', 'w'))
    print "showing"
    show()

if __name__== "__main__":
    if(len(argv) ==3):
        plot_likelihood_map(argv[1], cPickle.load(open(argv[2], 'r')))
    elif(len(argv) ==4):
        plot_likelihood_map(argv[1], cPickle.load(open(argv[2], 'r')), int(argv[3]))
    else:
        print "usage:\n\tpython find_dp_path_spline.py object_type lmap.pck steps"
