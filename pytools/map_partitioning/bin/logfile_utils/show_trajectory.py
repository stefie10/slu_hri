from pyTklib import tklib_log_gridmap
import carmen_maptools
from sys import argv
from pylab import *

def load_logfile(filename):
    filein = open(filename, 'r')
    C =[]
    X = []
    Y = []
    for line in filein:
        c, x, y = line.split()
        C.append(float(c))
        X.append(float(x))
        Y.append(float(y))
    filein.close()
    return C, X, Y

def show_trajectory(map_file, log_file):
    #load the map and plot it 
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map(map_file)
    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    #initialize all this junk
    L, X, Y = load_logfile(log_file)
    pltypes = ['o','^','<','>','s','d','p','h','x', 'o']
    plcolors = ['r','g','b','m','k','y','c','r','g','b']    

    #plot the trajectory
    XHash = {}
    YHash = {}
    
    for i in range(len(L)):
        try:
            XHash[L[i]].append(X[i])
            YHash[L[i]].append(Y[i])
        except(KeyError):
            XHash[L[i]] = []
            YHash[L[i]] = []

    for key in XHash.keys():
        plot(XHash[key], YHash[key], plcolors[int(key)]+pltypes[int(key)]);

    plot([X[0]], [Y[0]], 'go');
    plot([X[len(X)-1]], [Y[len(Y)-1]], 'ro');
    show()

if __name__=="__main__":
    if(len(argv)==3):
        show_trajectory(argv[1], argv[2])
    else:
        print "usage:\n\t>>python show_trajectory.py map_file emma_logfile"
