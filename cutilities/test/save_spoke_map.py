from pyTklib import *
import carmen_maptools
from pylab import *
from scipy import mod
from math import *

def get_spoke_map():
    gridmap  = tklib_log_gridmap(50, 50, 0.05)

    x_size = gridmap.get_map_width()
    y_size = gridmap.get_map_height()

    #fill first with nothing
    for i in range(x_size):
        for j in range(y_size):
            gridmap.set_value(i, j, -10000.0)

    #fill in the left/right wall
    for i in range(x_size):
        gridmap.set_value(i, 0, 10000.0)
        gridmap.set_value(i, y_size-1, 10000.0)

    #fill in the top/bottom wall
    for i in range(y_size):
        gridmap.set_value(0, i, 10000.0)
        gridmap.set_value(x_size-1, i, 10000.0)


    print "x_size", x_size, x_size*0.1
    print "y_size", y_size, y_size*0.1

    map_center_x, map_center_y = 500, 500
    spoke_frequency = pi/20.0
    spoke_distance = 100
    
    for i in range(x_size):
        for j in range(y_size):
            
            d = sqrt((map_center_x-i)**2.0 + (map_center_y-j)**2.0);
            th = atan2(map_center_y-j,map_center_x-i);
            if(d > spoke_distance and abs(mod(th, spoke_frequency)) < 0.02
                                     and mod(th, 2*pi) > 0.02):
                gridmap.set_value(i, j, 10000.0)

        
    return gridmap

def test1():
    print "getting sawtooth map"
    gm = get_spoke_map()

    #print "getting probability map"
    themap = gm.to_probability_map_carmen()

    #print "plotting map"
    carmen_maptools.plot_map(themap, gm.y_size, gm.x_size)
    
    print "saving map"
    gm.save_carmen_map("spoke_map.cmf.gz");
        
    show()


if __name__ == "__main__":
    test1()
