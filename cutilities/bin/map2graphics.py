from carmen_maptools import *
from pyTklib import *
import carmen_maptools
from pylab import *
from sys import argv

def save_png(in_filename, out_filename):
    gridmap  = tklib_gridmap()
    gridmap.load_carmen_map(in_filename)
    themap = gridmap.get_map()
    plot_map(themap, gridmap.x_size, gridmap.y_size)
    
    savefig(out_filename)
    
if __name__ == "__main__":
    if(len(argv)==3):
        in_filename = argv[1]
        out_filename = argv[2]
        save_png(in_filename, out_filename)
    else:
        print "usage:\n    >>python map2png.py in_filename out_filename"
