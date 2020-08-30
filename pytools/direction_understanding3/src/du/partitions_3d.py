import cPickle
import math2d
import numpy as na

class partitions_3d(object):
    """
    Make a topological map with three dimensions
    """
    def __init__(self, clusterfile, boundingBox):
        self.clusterfile = clusterfile
        self.boundingBox = boundingBox
        self._clusters = None
        
    
    @property 
    def skel(self):
        return self.clusters.skel
    @property
    def clusters(self):
        if self._clusters == None:
            self._clusters = cPickle.load(open(self.clusterfile))
        return self._clusters
    
    
    def get_tf(self):
        return self.clusters.tf
    
    
    def set_tf(self, tf):
        self.clusters.tf = tf
    tf = property(get_tf, set_tf)
        
    def get_map(self):
        return self.clusters.get_map()
    
    def unload(self):
        return self.clusters.unload()
    def get_topological_map(self):
        print "clusters", self.clusters
        stmap, stmap_cnt, stmap_locs = self.clusters.get_topological_map()
        #stmap_locs[45.0] = na.array([72.5, 84.4])
        #stmap_locs[63.0] = na.array([66.64, 110])
        
        up_idx = float(int(max(stmap.keys()) + 1))
        #[45.0, 16.0, 46.0, 2.0]
        for node in stmap.keys(): 
            stmap[up_idx] = list(stmap[node]) + [up_idx]
            stmap_locs[up_idx] = na.append(stmap_locs[node], 4.0)
            for elt in stmap[up_idx]:
                stmap[elt] = na.append(stmap[elt], up_idx)
            up_idx += 1
        
        tmap = dict(stmap)
        tmap_locs = {}
        for key, loc in stmap_locs.iteritems():
            if self.boundingBox == None or math2d.isInteriorPoint(self.boundingBox,
                                                                  loc[0:2]):
                if len(loc) == 2:
                    tmap_locs[key] = na.append(loc, 1)
                else:
                    tmap_locs[key] = loc
            else:
                del tmap[key]
                for key1, lst in tmap.iteritems():
                    tmap[key1] = [x for x in lst if x != key]
        
        return tmap, None, tmap_locs

    def get_topological_distance_graph(self):
        return self.clusters.get_topological_distance_graph()
