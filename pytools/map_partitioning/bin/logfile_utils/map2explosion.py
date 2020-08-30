from pyTklib import tklib_log_gridmap, kNN_index
from map_partitioning2_0 import show_graph, partition_map, show_partitions
from map_partitioning2_0 import show_explosion, get_colors, show_graph_no_map
import carmen_maptools
from sys import argv
from pylab import *
from scipy import *


    
if __name__=="__main__":
    if(len(argv) == 5):
        #load the gridmap
        gridmap  = tklib_log_gridmap()

        print "loading gridmap"
        gridmap.load_carmen_map(argv[1])

        print "partitioning map"
        #partition the map
        samples = []
        labels = []
        num_classes = int(argv[2])
        if(num_classes < 0):
            samples, labels, k = partition_map(gridmap, None, int(argv[3]));            
        else:
            #partition the map
            samples, labels, k = partition_map(gridmap, num_classes, int(argv[3]));

        outfilename=argv[4]

        print "showing explosion"
        show_explosion(gridmap, samples, labels);
        savefig(outfilename + ".explosion.eps")
        
        #make a new figure
        figure()
        
        #show the map
        print "showing partitions"
        show_partitions(gridmap, samples, labels)
        savefig(outfilename + ".partitions.eps")

        #figure()
        #show_graph_no_map(gridmap, samples, labels)
        #savefig(outfilename + ".graph.eps")
        #axis("equal")
        
        figure()
        themap = gridmap.to_probability_map_carmen()
        carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
        #show the explosion
        savefig(outfilename + ".map.eps")
        show()
    else:
        print "usage:"
        print "\t >>python map2explosion.py filename numclasses numsamples"
