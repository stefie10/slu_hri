from carmen_util import *
from pyTklib import tklib_log_gridmap
import carmen_maptools
from pylab import *
from sys import argv


def clog2logfile(map_file, log_file, outfile):
    #load the map and plot it 
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map(map_file)
    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    
    #initialize all this junk
    vals = load_carmen_logfile(log_file)
    front_readings, rear_readings, true_positions = vals
    
    X, Y = [], []

    print "getting the poses"
    #append the poses

    #tout = open("tmpf", 'w')
    i=0;
    for pose in true_positions:
        
        #c = mod(i, 10);
        #print pose
        X.append(pose.x)
        Y.append(pose.y)

        #tout.write(str(c) + " " + str(pose.x) + " " + str(pose.y) + "\n")
        i+=1
        
    #tout.close()

    print "ray tracing"
    #do the ray_tracing
    angles = array(arange(0, 2*pi, pi/360.0))
    D = []
    for i in range(len(X)):
        dists = gridmap.ray_trace(X[i], Y[i], angles)
        D.append(dists)
    
    #write to a logfile
    print "writing the logfile"
    write_logfile(X, Y, D, outfile);

    print "plotting the trajectory"
    #plot the trajectory
    plot(X, Y, 'k-');
    plot([X[0]], [Y[0]], 'go');
    plot([X[len(X)-1]], [Y[len(Y)-1]], 'ro');
    show()

def write_logfile(X, Y, readings, outfile):
    outfile.write("##################NEW SUBMAP#################\n");
    for i in range(len(X)):
        outfile.write("TRAIN_SAMPLE")
        outfile.write(" lb:"+str(0))
        pt = [X[i], Y[i]]
        outfile.write(" rp:"+str(pt))
        outfile.write(" d:"+str(readings[i]))
        outfile.write("\n")


if __name__=="__main__":
    if(len(argv)==4):
        of = open(argv[3], 'w')
        clog2logfile(argv[1], argv[2], of)
        of.close()
    else:
        print "usage:\n\t>>python clog2logfile.py map_file log_file outfile"
