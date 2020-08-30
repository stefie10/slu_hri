from pyTklib import *
import carmen_maptools
from pylab import *

def test1():
    gridmap  = tklib_gridmap()
    gridmap.load_carmen_map("/home/tkollar/repositories/tklib/pytools/map_partitioning/maps/ubremen-cartesium/cartesium.cmf.gz")

    themap = gridmap.get_map()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);

    figure()
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map("/home/tkollar/repositories/tklib/pytools/map_partitioning/maps/ubremen-cartesium/cartesium.cmf.gz")

    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);

    show()


if __name__ == "__main__":
    test1()
