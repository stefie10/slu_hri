import min_entropy
from os.path import basename, dirname


class model(min_entropy.model):
    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename,
                 tag_filename, **args):

        srel = dirname(srelMatFname) + "polygon_" + basename(srelMatFname)
        min_entropy.model.__init__(self, clusterfile, cachelmap, srel,
                                   map_filename, tag_filename, **args)



    def get_object_to_object_visibility_hash(self):
        result = []
        print "getting object_to_object visibility hash"
        for i, geom in enumerate(self.obj_geometries):
            vtags, itags_t = self.clusters.tf.get_objects_visible_from_object(geom)
            result.append((vtags, itags_t))
        return result        

    def createGround(self, l):
        return self.createGroundFromPolygon(l)
