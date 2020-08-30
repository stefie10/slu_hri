from pylab import *
import cPickle
from carmen_maptools import plot_map
from pyTklib import kNN, tklib_euclidean_distance, tklib_log_gridmap
from topological_map import *
from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-c", "--carmen_map",dest="carmen_map", 
                      help="Carmen Map Filename", metavar="FILE")

    parser.add_option("-t", "--topology",dest="topology", 
                      help="Topology", metavar="FILE")
    
    (options, args) = parser.parse_args()    


    topology = cPickle.load(open(options.topology, 'r'))

    print "getting topological map"
    #ion()
    figure()
    cmap = tklib_log_gridmap()
    cmap.load_carmen_map(options.carmen_map)
    
    plot_map(cmap.to_probability_map_carmen(), cmap.x_size, cmap.y_size)
    
    XY = transpose([node.xy for node in topology.nodes])
    plot(XY[0], XY[1], 'ko')
    
    for edge in topology.edges:
        plot(edge.path[0], edge.path[1])
        #axis([36.0,38.0, 45, 47])
        #print edge.start_i
        #draw()
        #if(edge.path[0][0] < 38 and edge.path[0][0] > 36 and 
        #   edge.path[1][0] < 47 and edge.path[1][0] > 45):
        #    raw_input("enter")
    
    for edge in topology.edges:
        #print "start theta", edge.path[2][0]
        plot([edge.path[0][0], edge.path[0][0]+0.05*cos(edge.path[2][0])], 
             [edge.path[1][0], edge.path[1][0]+0.05*sin(edge.path[2][0])], 'b-', linewidth=3)
        
    
    
    
    
    '''for i in range(len(paths)):
            print i, "of", len(paths)
            X, Y = XY.take(paths[i], axis=1)
            plot(X, Y)

        draw()

        figure()
        plot_map(skel.get_map().to_probability_map_carmen(), skel.get_map().x_size, skel.get_map().y_size)
        X, Y = XY.take(tmap.keys(), axis=1)
        plot(X, Y, 'r^')
        
        figure()
        
        X, Y = XY.take(tmap.keys(), axis=1)
        plot(X, Y, 'r^')
        
        for elt in tmap.keys():
            for val in tmap[elt]:
                x1 = XY[:,elt]
                x2 = XY[:,val]

                plot([x1[0], x2[0]], [x1[1], x2[1]])'''


    show()

