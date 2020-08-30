from carmen_map_skeletonizer import *
from cPickle import *
from sys import argv
from pylab import *

if __name__=="__main__":
    
    if(len(argv) == 5):
        map_filename = argv[1]
        out_filename = argv[2]
        mfilter_width = int(argv[3])
        num_iterations = int(argv[4])
        
        tklib_skeleton = carmen_map_skeletonizer(map_filename, mfilter_width, num_iterations)
        curr_map = tklib_skeleton.get_skeleton()

        print "*******************RESULTS********************"
        print tklib_skeleton.get_end_points()
        print "number of end points", len(tklib_skeleton.get_end_points()[0])
        print "number of ction points", len(tklib_skeleton.get_junction_points()[0])
        gridmap = tklib_skeleton.gridmap
        extent = [0 + gridmap.x_offset, gridmap.x_size + gridmap.x_offset,
                  0 + gridmap.y_offset, gridmap.y_size + gridmap.y_offset]
        
        imshow(curr_map, origin=1, cmap=cm.gray, extent=extent)  

        #Ix, Iy = tklib_skeleton.ind_to_xy(tklib_skeleton.get_end_points())
        #Ix2, Iy2 = tklib_skeleton.ind_to_xy(tklib_skeleton.get_junction_points())

        #plot(Ix, Iy, 'ro')
        #plot(Ix2, Iy2, 'ro')
        
        tklib_skeleton.gridmap = None
        dump(tklib_skeleton, open(out_filename + ".pck", 'w'))
        
        title("skeleton with staircases removed")

        
        show()

    else:
        print "usage:\n\tpython skeletonize.py map_filename out_filename mfilter_width iterations"
    
