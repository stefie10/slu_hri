from pylab import *
import cPickle
from sys import argv
from map_partitioning2_0 import show_graph
import carmen_maptools
import cProfile

if __name__=="__main__":
    if(len(argv) == 2):
        print "loading pickled file"
        mypart = cPickle.load(open(argv[1], 'r'))
        print "showing graph"
        gridmap = mypart.get_map()
        themap = gridmap.to_probability_map_carmen()
        carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
        
        
        landmarks = mypart.get_topological_bounding_boxes()
        print "landmarks:", landmarks
        #cProfile.run("mypart.get_topological_bounding_boxes()", "testprof")
        
        
        #G, tmap_cnt, tmap_locs = mypart.get_topological_map()
        
        #for key1 in G.keys():
        #    for key2 in G[key1]:
        #        plot([tmap_locs[key1][0], tmap_locs[float(key2)][0]], 
        #             [tmap_locs[key1][1], tmap_locs[float(key2)][1]], 'k-')
                
        show()
    else:
        print "usage:"
        print "\t >>python show_graph.py filename"


