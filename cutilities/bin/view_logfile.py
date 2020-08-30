from carmen_util import *
from sys import argv
from pyTklib import *
import carmen_maptools
from pylab import *

def view_logfile(filename, logfile, x_offset=0, y_offset=0):
    gridmap  = tklib_gridmap()
    gridmap.load_carmen_map(filename);
    themap = gridmap.get_map()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    freadings, rreadings, tp, odom = load_carmen_logfile(logfile)
    print "len(freadings)", freadings
    

    #for elt in freadings:
    #    print elt
    #x_offset = 0#freadings[0].location.x - 19.25
    #y_offset = 0#freadings[0].location.y - 50.75
    
    X, Y = [], []

    myfile = open('test_out.log', 'w');
    for elt in freadings:
        pt = elt.location

        X.append(pt.x-x_offset)
        Y.append(pt.y-y_offset)
        
        elt.location.x = elt.location.x - x_offset
        elt.location.y = elt.location.y - y_offset
        
        myfile.write(elt.carmen_str()+"\n");
        
    myfile.close()

    plot(X, Y, 'r-')

    show()


if __name__ == "__main__":
    if(len(argv) == 3):
        view_logfile(argv[1], argv[2])
    elif(len(argv) == 5):
        view_logfile(argv[1], argv[2], float(argv[3]), float(argv[4]))
    else:
        print "usage\n\t>>python view_map.py map_file log_file [x_offset, y_offset]"
