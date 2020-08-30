from carmen_map_skeletonizer import *
#from location_selection_core import *
import carmen_maptools
from sys import argv
from pylab import *
from cPickle import *


if __name__=="__main__":
    
    if(len(argv) == 2):
        tklib_skeleton = load(open(argv[1], 'r'))
        curr_map = tklib_skeleton.get_skeleton()
        gm = tklib_skeleton.get_map()

        #get the junctions and ends
        XYe  = tklib_skeleton.get_end_points()
        XYj = tklib_skeleton.get_junction_points()

        themap = gm.to_probability_map_carmen()
        carmen_maptools.plot_map(themap,
                                 gm.x_size,
                                 gm.y_size)

        pj, = plot(XYj[0], XYj[1], 'bo')
        pe, = plot(XYe[0], XYe[1], 'g^')
        legend((pj, pe), ("Junction Points","End Points"), shadow=True)

        #show the skeleton

        figure()
        imshow(curr_map, origin=1, cmap=cm.gray)
        title("skeleton with staircases removed")

        figure()
        imshow(tklib_skeleton.b_map, origin=1, cmap=cm.gray)
        title("median filtered map")

        figure()
        imshow(tklib_skeleton.skeleton_prestaircase, origin=1, cmap=cm.gray)
        title("before staircase removal")


        figure()
        imshow(tklib_skeleton.skeleton_prestaircase, origin=1, cmap=cm.gray)
        title("before staircase removal")

        figure()
        mymap = tklib_skeleton.to_binary_map(gm)
        imshow(mymap, origin=1, cmap=cm.gray)
        title("original binary map")
        
        show()

    else:
        print "usage:\n\tpython destination_points.py skeletonized_file"

