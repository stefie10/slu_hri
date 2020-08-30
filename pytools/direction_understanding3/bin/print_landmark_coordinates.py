from sys import argv
from routeDirectionCorpusReader import readSession
import cPickle
from tag_util import *


if __name__=="__main__":
    dg_cache_fn = argv[1]
    dg_model = cPickle.load(open(dg_cache_fn, 'r'))
    mymap = dg_model.clusters.tf.get_map()
    for tag in dg_model.clusters.tf.get_points_and_polygons():
        stuff = [tag.tag, "%.3f, %.3f" % tag.centroid(), "%.3f, %.3f" % tuple(mymap.to_xy(tag.centroid()))]
        strs = [str(x).ljust(20) for x in stuff]
        for s in strs:
            print s,
        print 
