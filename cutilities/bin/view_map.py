from sys import argv
from pyTklib import *
import carmen_maptools
from carmen_maptools import *
from pylab import *

def view_map(filename):

    gridmap  = tklib_log_gridmap()
    #while(1):
    gridmap.load_carmen_map(filename);
    #del gridmap
    
    themap = gridmap.to_probability_map_carmen();
    #carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size, cmap="carmen_cmap_gray");
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    show()


if __name__ == "__main__":
    if(len(argv) == 2):
        view_map(argv[1])
    else:
        print "usage\n\t>>python view_map.py filename"
