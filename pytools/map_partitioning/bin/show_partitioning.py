from pylab import *
import cPickle
from sys import argv
from map_partitioning2_0 import show_graph
import carmen_maptools

if __name__=="__main__":
    if(len(argv) == 2):
        print "loading pickled file"
        mypart = cPickle.load(open(argv[1], 'r'))
        print "showing graph"
        #show_graph(mypart.get_map(), mypart.samples, mypart.labels)
        
        gridmap = mypart.get_map()
        themap = gridmap.to_probability_map_carmen()
        carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
        
        #dists = get_graph(gridmap, samples)
        
        G, tmap_cnt, tmap_locs = mypart.get_topological_map()
        
        for key1 in G.keys():
            for key2 in G[key1]:
                plot([tmap_locs[key1][0], tmap_locs[float(key2)][0]], 
                     [tmap_locs[key1][1], tmap_locs[float(key2)][1]], 'k-')
                
                
        #show_partitions(gridmap, samples, labels, colors)
        #drawa()

        '''gridmap  = tklib_log_gridmap()
        gridmap.load_carmen_map(argv[1])

        #partition the map
        samples, labels, k = partition_map(gridmap, int(argv[2]), int(argv[3]));

        #show the map
        show_partitions(gridmap, samples, labels)

        figure()
        show_graph(gridmap, samples, labels)

        figure()
        show_graph_no_map(gridmap, samples, labels)
        axis("equal")'''

        show()
    else:
        print "usage:"
        print "\t >>python show_graph.py filename"


