from pyTklib import tklib_log_gridmap
from scipy import array
from map_partitioning2_0 import partition_map, show_partitions
from map_partitioning2_0 import show_graph_no_map, show_graph
import carmen_maptools
from sys import argv
from pylab import *

if __name__=="__main__":
    if(len(argv) == 4):
        #load the gridmap
        gridmap  = tklib_log_gridmap()
        gridmap.load_carmen_map(argv[1])

        #partition the map
        samples, labels, k = partition_map(gridmap, int(argv[2]), int(argv[3]));

        #show the map
        show_partitions(gridmap, samples, labels)

        figure()
        show_graph(gridmap, samples, labels)

        figure()
        show_graph_no_map(gridmap, samples, labels)
        axis("equal")

        show()
    else:
        print "usage:"
        print "\t >>python show_graph.py filename numclasses numsamples"


