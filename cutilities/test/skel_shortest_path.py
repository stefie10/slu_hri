import cPickle
from sys import argv
from pylab import *
from carmen_maptools import *

if __name__=="__main__":

    if(len(argv) == 3):
        print "loading"
        mskel = cPickle.load(open(argv[1], 'r'))
        print "loaded", mskel.__class__
        print "map filename", mskel.map_filename
        mskel.map_filename = argv[2]
        
        sloc = [10,10]
        #eloc = [25,50]
        #eloc = [50, 7]
        eloc = [80, 7]

        #sloc = [80, 7]
        #eloc = [10, 10]
        
        plot([sloc[0]],[sloc[1]], 'go')
        plot([eloc[0]],[eloc[1]], 'ro')
        print "getting map"
        gm = mskel.get_map()
        print "get pm map"
        mymap = gm.to_probability_map_carmen()
        
        #get path
        X, Y= mskel.compute_path(sloc, eloc)
        
        plot(X, Y, 'yx-')
        plot_map(mymap, gm.x_size, gm.y_size)
        show()

    else:
        print "usage:\n\t python skel_shortest_path.py skeleton.pck map.cmf.gz"
