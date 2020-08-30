from carmen_map_skeletonizer import *
from location_selection_core import *
from sys import argv
from pylab import *
from cPickle import *


def generate_visibility_graph(tklib_skeleton):
    curr_map = tklib_skeleton.get_skeleton()
    gm = tklib_skeleton.get_map()
    
    #get the junctions and ends
    junction_map, Ij  = find_junction_points(curr_map)
    end_map, Ie  = find_end_points(curr_map)
    
    XYj = ind_to_xy(gm, Ij); XYe = ind_to_xy(gm, Ie);
    XYj = XYj.tolist()
    XYj[0].extend(XYe[0]); XYj[1].extend(XYe[1]);
    XYj = array(XYj)

    V = zeros([len(XYj[0]), len(XYj[0])])*1.0
    for i in range(len(XYj[0])):
        for j in range(len(XYj[0])):
            if(gm.is_visible(XYj[:,i], XYj[:,j])):
                V[i,j] = 1.0

    return V, XYj

def plot_visibility_graph(tklib_skeleton, XYj, V):
    curr_map = tklib_skeleton.get_skeleton()
    gm = tklib_skeleton.get_map()
    
    themap = gm.to_probability_map_carmen()
    carmen_maptools.plot_map(themap,gm.x_size,gm.y_size)

    plot(XYj[0,:], XYj[1,:], 'r^')
    for i in range(len(V)):
        for j in range(len(V)):
            if(V[i,j] == 1.0):
                plot([XYj[0,i], XYj[0,j]], [XYj[1,i], XYj[1,j]])
    
    show()



if __name__=="__main__":
    
    if(len(argv) == 2):
        tklib_skeleton = load(open(argv[1], 'r'))
        V, XY =  generate_visibility_graph(tklib_skeleton)
        plot_visibility_graph(tklib_skeleton, XY, V)
        show()

    else:
        print "usage:\n\tpython generate_graph.py filename"




