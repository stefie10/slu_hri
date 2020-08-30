from carmen_util import *
from pyTklib import tklib_log_gridmap
import carmen_maptools
from pylab import *
from sys import argv


def logfile2truepose(map_file, log_file,
                     x_offset_st=0, y_offset_st=0,
                     x_offset_end=0, y_offset_end=0):

    #load the map and plot it 
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map(map_file)
    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    
    #initialize all this junk
    vals = load_carmen_logfile(log_file)
    front_readings, rear_readings, true_positions = vals
    
    X, Y = [], []

    for pose in true_positions:
        X.append(pose.x)
        Y.append(pose.y)

    #plot the trajectory
    plot(X, Y, 'k-');
    
    #plot the start location
    plot([X[0]], [Y[0]], 'go');
    print "x,y offsets", x_offset_st, y_offset_st
    text(X[0]+x_offset_st,Y[0]+y_offset_st,"start",color='w')

    #plot the end location
    plot([X[len(X)-1]], [Y[len(Y)-1]], 'ro');
    print "x,y offsets", x_offset_end, y_offset_end
    text(X[len(X)-1]+x_offset_end,Y[len(Y)-1]+y_offset_end,"end",color='w')
    show()


if __name__=="__main__":
    if(len(argv)==3):
        logfile2truepose(argv[1], argv[2])
    if(len(argv)==7):
        logfile2truepose(argv[1], argv[2],
                         float(argv[3]), float(argv[4]),
                         float(argv[5]), float(argv[6]))
    else:
        print "usage:\n\t>>python logfile2truepose.py map_file log_file [x_off_st, y_off_st, x_off_end, y_off_end]"
