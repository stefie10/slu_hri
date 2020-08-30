import cPickle
from pyTklib import kNN
from topological_util import *
from topological_map import *
from scipy import arctan2, array, nan
from optparse import OptionParser


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-s", "--skeleton_file",dest="skel_file", 
                      help="Skeleton File", metavar="FILE")

    parser.add_option("-c", "--carmen_map",dest="carmen_map", 
                      help="Carmen Map Filename", metavar="FILE")

    parser.add_option("-o", "--output_topology",dest="outfile_topology", 
                      help="Output Filename Test", metavar="FILE")
    
    (options, args) = parser.parse_args()    

    skel = cPickle.load(open(options.skel_file, 'r'))
    skel.map_filename = options.carmen_map
        
    print "getting topological map"
    adj_list, paths_I, XY = compute_topological_map(skel, 40)
    
    print "1875", adj_list[1875]
    print "1896", adj_list[1896]
    #print "1905", adj_list[1905]
        
    tnodes = []
    for key in adj_list.keys():
        tnodes.append(topological_node(key, XY[:,key]))


    #do a check of the adj_list
    for key1 in adj_list.keys():
        for key2 in adj_list[key1]:
            assert key1 in adj_list[key2]
            
    tedges = []
    for path_I in paths_I:
        XY_path = XY.take(path_I, axis=1)
        Theta = list(arctan2(XY_path[1,1:]-XY_path[1,:-1], XY_path[0,1:]-XY_path[0,:-1]))
        if(len(Theta) > 0):
            Theta.append(Theta[-1])
        else:
            Theta.append(nan)
        tedges.append(topological_edge(path_I[0], path_I[-1], array([XY_path[0], XY_path[1], Theta])))

        XY_path = XY.take(list(reversed(path_I)), axis=1)
        Theta = list(arctan2(XY_path[1,1:]-XY_path[1,:-1], XY_path[0,1:]-XY_path[0,:-1]))

        if(len(Theta) > 0):
            Theta.append(Theta[-1])
        else:
            Theta.append(nan)
        tedges.append(topological_edge(path_I[-1], path_I[0], array([XY_path[0], XY_path[1], Theta])))

    
    t_map = topological_map(adj_list, tnodes, tedges)
    print "topological map generated with", len(tnodes), "nodes and", len(tedges), "edges"
    print "saving to ", options.outfile_topology
    cPickle.dump(t_map, open(options.outfile_topology, 'wb'), cPickle.HIGHEST_PROTOCOL)
