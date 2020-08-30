from sys import argv
from pyTklib import *
import carmen_maptools
from pylab import *
from scipy.io import savemat

def map_to_mat(filename, outfilename):
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map(filename);
    themap = gridmap.to_probability_map_carmen();

    
    map_dict = {}
    map_dict['map'] = themap
    map_dict['x_size'] = gridmap.x_size
    map_dict['y_size'] = gridmap.y_size
    map_dict['resolution'] = gridmap.resolution
    print "saving matlab file"
    savemat(outfilename, map_dict)

    print "ploting map"
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);    
    show()


if __name__ == "__main__":
    if(len(argv) == 3):
        map_to_mat(argv[1], argv[2])
    else:
        print "usage\n\t>>python map_to_mat.py filename outfilename"
