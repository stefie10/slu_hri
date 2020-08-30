import cPickle
import math2d
import numpy as na

class PartitionsOlin(object):
    """
    Make a topological map with three dimensions
    """
    def __init__(self, clusterfile, boundingBox=None):
        self.clusterfile = clusterfile
        self.boundingBox = boundingBox
        self._clusters = cPickle.load(open(self.clusterfile))
        
    
    @property 
    def skel(self):
        return self._clusters.skel
    
    def get_tf(self):
        return self._clusters.tf
    
    
    def set_tf(self, tf):
        self._clusters.tf = tf

    tf = property(get_tf, set_tf)
        
    def get_map(self):
        return self._clusters.get_map()
    
    def unload(self):
        return self._clusters.unload()

    def get_topological_map(self):
        print "clusters", self._clusters
        
        # nodes manually annotated for the hsp d2 map.
        # (361, 314), # camp charlie, gator can't make turn
        nodes = [(564, 497), (435, 396), (417, 359), 
                 (591, 319), (445, 237), 
                 (253, 253)]
        stmap_locs = {}
        for i, node in enumerate(nodes):
            i = float(i)
            stmap_locs[i] = node
        stmap = {}
        for skey, sloc in stmap_locs.iteritems():
            for ekey, eloc in stmap_locs.iteritems():
                X, Y = self._clusters.skel.compute_path(sloc, eloc)
                #length = math2d.length(na.transpose((X, Y)))
                #if length < 10:
                stmap.setdefault(skey, [])
                stmap[skey].append(ekey)

        up_idx = float(int(max(stmap.keys()) + 1))

        for node in stmap.keys(): 
            stmap[up_idx] = list(stmap[node]) + [up_idx]
            stmap_locs[up_idx] = na.append(stmap_locs[node], 6.0)
            for elt in stmap[up_idx]:
                stmap[elt] = na.append(stmap[elt], up_idx)
            up_idx += 1
        
        tmap = dict(stmap)
        tmap_locs = {}
        for key, loc in stmap_locs.iteritems():
            if self.boundingBox == None or math2d.isInteriorPoint(self.boundingBox,
                                                                  loc[0:2]):
                if len(loc) == 2:
                    tmap_locs[key] = na.append(loc, 4.5)
                else:
                    tmap_locs[key] = loc
            else:
                del tmap[key]
                for key1, lst in tmap.iteritems():
                    tmap[key1] = [x for x in lst if x != key]
        
        return tmap, None, tmap_locs
