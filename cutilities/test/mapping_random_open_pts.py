from pyTklib import *
import carmen_maptools
from pylab import *

def test1():
    gridmap  = tklib_log_gridmap()
    print "loading thickwean"
    gridmap.load_carmen_map("/home/tkollar/installs/carmen/data/thickwean.map")

    loc = gridmap.get_random_open_location(0.2);
    plot([loc[0]], [loc[1]], 'b^')
    
    locations = []
    for i in range(100):
        print i
        open_loc = gridmap.get_random_open_location(0.2) #_location_from_pt(loc, 2.0, 0.2);
        locations.append(open_loc);

    locations = transpose(locations);

    X, Y = locations
    plot(X, Y, 'ro');
    
    themap = gridmap.to_probability_map_carmen()
    #print themap
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    show()


if __name__ == "__main__":
    test1()
