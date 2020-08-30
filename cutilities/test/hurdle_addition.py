from pyTklib import *
import carmen_maptools
from pylab import *

def test1():
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map("/home/tkollar/installs/carmen/data/thickwean.map")

    #test get
    #print "getting free location"
    #gridmap.get_random_free_location(0.25)

    print "adding hurdles"
    gridmap.add_hurdles(0.2413, 0.03, 10);
    themap = gridmap.to_probability_map_carmen()
    print "saving map"
    success = gridmap.save_carmen_map("./test2.map");
    print "success", success
        
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    show()


if __name__ == "__main__":
    test1()
