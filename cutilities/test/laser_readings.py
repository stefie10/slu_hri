from pyTklib import *
import carmen_maptools
from pylab import *

def test1():
    figure()
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map("/home/tkollar/repositories/tklib/pytools/map_partitioning/maps/ubremen-cartesium/cartesium.cmf.gz")

    x,y  = gridmap.get_random_open_location(0.2)
    thetas = arange(0, 2*pi, pi/180)
    myrange = gridmap.ray_trace(x, y, thetas)
    
    X = myrange*cos(thetas)+ x
    Y = myrange*sin(thetas)+ y

    plot([x], [y], 'ro')
    plot(X, Y, 'gx')
    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);

    show()


if __name__ == "__main__":
    test1()
