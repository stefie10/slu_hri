from pyTklib import tklib_log_gridmap, kNN_index
from map_partitioning2_0 import show_graph, partition_map, show_partitions
from map_partitioning2_0 import show_explosion, get_colors, show_graph_no_map
from map_partitioner import *
import carmen_maptools
from sys import argv
from pylab import *
from scipy import *
from cPickle import load, dump

def mypartition_map(argv):
    if(len(argv) == 7):
        #load the gridmap
        mp = map_partitioner(argv[1], float(argv[2]),
                             int(argv[3]), int(argv[4]), gridcell_skip=float(argv[5]))
        outfilename=argv[6]
    elif(len(argv) == 4):
        mp = map_partitioner(argv[1], gridcell_skip=float(argv[2]))
        outfilename = argv[3]
    elif(len(argv) == 5):
        mp = map_partitioner(argv[1], float(argv[2]), gridcell_skip=float(argv[3]))
        outfilename = argv[4]
    else:
        print "usage:"
        print "\t >>python partition_map.py skel_filename [alpha, numclasses numsamples] gridcell_skip=15.0 outfile"
        return

    print "running"
    mp.run()
    
    print "showing explosion"
    show_explosion(mp.get_map(), mp.samples, mp.labels);
    savefig(outfilename + ".explosion.eps")
    
    #make a new figure
    figure()
    
    #show the map
    print "showing partitions"
    show_partitions(mp.get_map(), mp.samples, mp.labels)
    savefig(outfilename + ".partitions.eps")
    
    figure()
    themap = mp.get_map().to_probability_map_carmen()
    carmen_maptools.plot_map(themap, mp.get_map().x_size, mp.get_map().y_size);
    #show the explosion
    savefig(outfilename + ".map.eps")
    show()
    
    mp.gridmap = None
    mp.skel.gridmap = None
    dump(mp, open(outfilename + ".pck", 'w'))



if __name__=="__main__":
    mypartition_map(argv);
