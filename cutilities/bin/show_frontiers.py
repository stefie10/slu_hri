from pyTklib import *
from pylab import *
import carmen_maptools
from sys import argv

if __name__=="__main__":
    if(len(argv)==2):
        mymap = tklib_log_gridmap()
        mymap.load_carmen_map(argv[1])
        Pts =  mymap.get_frontiers()

        if(len(Pts) > 0):
            X, Y = Pts
            plot(X, Y, 'rx');
            carmen_maptools.plot_map(mymap.to_probability_map_carmen(),
                                     mymap.x_size, mymap.y_size);
            show()
        else:
            print "no frontiers found... exiting"
    else:
        print "usage:\n\t\t>>python frontier_planner.py map_filename"
