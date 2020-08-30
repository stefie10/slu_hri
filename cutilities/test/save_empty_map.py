from pyTklib import *
import carmen_maptools
from pylab import *

def get_empty_map():
    gridmap  = tklib_log_gridmap(3, 3, 0.1)

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

    return gridmap

def test1():
    print "getting empty map"
    gm = get_empty_map()

    print "getting probability map"
    themap = gm.to_probability_map_carmen()

    print "plotting map"
    carmen_maptools.plot_map(themap, gm.x_size, gm.y_size)

    print "saving map"
    gm.save_carmen_map("empty_map.cmf.gz");
        
    show()


if __name__ == "__main__":
    test1()
