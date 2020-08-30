from pyTklib import tklib_log_gridmap, kNN_index
from map_partitioning2_0 import show_graph, partition_map, show_partitions
from map_partitioning2_0 import show_explosion, get_colors, show_graph_no_map
from map_partitioner import *
import carmen_maptools
from sys import argv
from pylab import *
from scipy import *
from cPickle import load, dump


def semantic_map_partitioner(argv):

    print len(argv)
    if(len(argv) == 6):
        mp = map_partitioner_semantic(argv[1], argv[2], numkmeans=1,
                                      gridcell_skip=float(argv[3]),
                                      map_filename=argv[4])
        outfilename = argv[5]

    elif(len(argv) == 7):
        mp = map_partitioner_semantic(argv[1], argv[2], numkmeans=1,
                                      gridcell_skip=float(argv[3]),
                                      map_filename=argv[4], alpha=float(argv[5]))
        outfilename = argv[6]

    elif(len(argv) == 8):
        #print int(argv[6])
        print "seed=", argv[6]
        mp = map_partitioner_semantic(argv[1], argv[2], numkmeans=1,
                                      gridcell_skip=float(argv[3]),
                                      map_filename=argv[4], alpha=float(argv[5]),
                                      seed_number=int(argv[6]))
        outfilename = argv[7]
    else:
        print "usage:\n\t see file"
        return
    #else:
    #    print "usage:"
    #    print "\t >>python partition_map.py skel_filename tag_filename [alpha, numclasses numsamples] gridcell_skip=15.0 outfile"
    #    return
    """    
# Old argument handling.  I updated it to take a map_filename and
# didnt' want to take the time to fix it because I can't test it. It's
# better to leave it in a known-broken state than to fix it wrong and
# have a subtle bug.

    if(len(argv) == 8):
        #load the gridmap
        mp = map_partitioner_semantic(argv[1], argv[2], float(argv[3]),
                                      int(argv[4]), int(argv[5]), numkmeans=1, 
                                      gridcell_skip=float(argv[6]))
        outfilename=argv[7]
    elif(len(argv) == 5):
        mp = map_partitioner_semantic(argv[1], argv[2], numkmeans=1,
                                      gridcell_skip=float(argv[3]))
        outfilename = argv[4]
    elif(len(argv) == 6):
        mp = map_partitioner_semantic(argv[1], argv[2], float(argv[3]), 
                                      numkmeans=1, gridcell_skip=float(argv[4]))
        outfilename = argv[5]
    else:
        print "usage:"
        print "\t >>python partition_map.py skel_filename tag_filename [alpha, numclasses numsamples] gridcell_skip=15.0 outfile"
        return
        """    

    
    mp.run()
    
##    print "showing figures"
##    for i in range(mp.numkmeans):
##        figure()
##        title(str(i))
##        show_explosion(mp.get_map(), mp.samples, mp.mylabels[i]);
##        figure()
##        title(str(i))
##        show_partitions(mp.get_map(), mp.samples, mp.mylabels[i])

    mp.unload()
    out = outfilename + ".pck"
    print "saving", out
    dump(mp, open(out, 'wb'), 2)
    show()


if __name__=="__main__":
    semantic_map_partitioner(argv);







#figure()
#themap = mp.get_map().to_probability_map_carmen()
#carmen_maptools.plot_map(themap, mp.get_map().x_size, mp.get_map().y_size);
    
    
#show the explosion
#tf = tag_file(tagfilename, mp.skel.map_filename)
    
#tf_names = tf.get_tag_names()

#for elt in tf_names:
#    X, Y = tf.get_tag_locations(elt)
#    plot(X, Y, 'ro')

#show()

