from environ_vars import TKLIB_HOME
import cPickle
import carmen_maptools
from pylab import *

ion()
model = cPickle.load(open(TKLIB_HOME+'/data/directions/direction_floor_8_full/models/min_entropy_extended.pck', 'r'))

mymap  = model.clusters.get_map()
themap = mymap.to_probability_map_carmen()
carmen_maptools.plot_map(themap, mymap.x_size, mymap.y_size)

p1, = plot([], [], 'ro')

for topo in model.tmap_locs.keys():
    print "-----------------------------"
    print topo
    print model.tmap_locs[topo]
    print model.vtags[topo]
    print "-----------------------------"

    p1.set_data([model.tmap_locs[topo][0]], [model.tmap_locs[topo][1]])
    draw()
    raw_input()
    





