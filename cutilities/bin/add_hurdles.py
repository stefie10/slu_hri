from pyTklib import *
import carmen_maptools
from pylab import *
from sys import argv

def add_hurdles(in_filename, number, width_apart, post_size, out_filename):
    gridmap  = tklib_gridmap()
    gridmap.load_carmen_map(in_filename)

    gridmap.add_hurdles(width_apart, post_size, number);
    themap = gridmap.get_map()

    success = gridmap.save_carmen_map(out_filename);

if __name__ == "__main__":

    if(len(argv)==4):
        in_filename = argv[1]
        number_of_hurdles = int(argv[2])
        out_filename = argv[3]
        add_hurdles(in_filename, number_of_hurdles, 0.2413, 0.03, out_filename);
    else:
        print "usage:\n    >>python add_hurdles.py in_filename num_hurdles out_filename"
