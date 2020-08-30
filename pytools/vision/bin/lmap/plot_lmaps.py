from sys import argv
import cPickle
from scipy import *
from create_likelihood_map_v2 import map_likelihood_simple
from datatypes_lmap import *
from carmen_maptools import *
from pylab import *


def show_l_map(lmap, minval=0.0):
    gray()    
    i=1
    f = figure()
    f.text(.5, .95, "Likelihood Maps", 
            horizontalalignment='center', fontsize=16) 


    for key in lmap.likelihood_map.keys():
        #figure()
        mylen = len(lmap.likelihood_map.keys())
        #subplot(ceil(sqrt(mylen)), ceil(sqrt(mylen)), i)
        #subplot(2, ceil(mylen/2.0), i)
        subplot(1, mylen, i)
        axis('off')
        title(key)
        #mylmap = lmap.get_lmap(key)
        mylmap = lmap.get_lmap_nn(key, minval)
        mylmap[0,0] = 1.0
        mylmap=transpose(mylmap)
        imshow(mylmap, origin='lower')
        i+=1

    print "saving lmaps"
    savefig("lmaps.png")
    print "showing figure"
    show()


if __name__ == "__main__":
    if(len(argv) == 2):
        show_l_map(cPickle.load(open(argv[1], 'r')))
    elif(len(argv) == 3):
        show_l_map(cPickle.load(open(argv[1], 'r')), float(argv[2]))
    else:
        print "usage:\n\t python plot_lmap_object_v2.py l_map.pck [minvalue]"
