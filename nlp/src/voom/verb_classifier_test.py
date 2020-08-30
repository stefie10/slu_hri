from agents import Situation, Agent
from environ_vars import TKLIB_HOME
from voom import trainer_pacman
import carmen_map_skeletonizer
import tag_util
import unittest



class TestCase(unittest.TestCase):
    
    def testFollow(self):
        map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
        cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
        gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
        tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
        tagFile.get_map()
        tagFile.get_tag_names()
        
        skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)

    
        situation = Situation([Agent("figure", 
                                     [(0, (25.400000378489494, 9.0000001341104507, 0.0)), 
                                      (1, (25.400000378489494, 9.200000137090683, -1.5707963267948966)), 
                                      (2, (25.400000378489494, 9.4000001400709152, -1.5707963267948966)), 
                                      (3, (25.400000378489494, 9.6000001430511475, -1.5707963267948966)), 
                                      (4, (25.400000378489494, 9.8000001460313797, -1.5707963267948966)), 
                                      (5, (25.200000375509262, 10.000000149011612, -0.78539816339744828)), 
                                      (6, (25.200000375509262, 10.200000151991844, -1.5707963267948966)), 
                                      (7, (25.400000378489494, 10.400000154972076, -2.3561944901923448)), 
                                      (8, (25.400000378489494, 10.600000157952309, -1.5707963267948966)), 
                                      (9, (25.400000378489494, 10.800000160932541, -1.5707963267948966)), 
                                      (10,(25.600000381469727, 11.000000163912773, -2.3561944901923448)), 
                                      (11,(25.600000381469727, 11.000000163912773, 0.0))]),
                               Agent("landmark",
                                     [(0, (25.200000375509262, 11.800000175833702, 0.0)), 
                                      (1, (25.400000378489494, 12.000000178813934, -2.3561944901923448)), 
                                      (2, (25.400000378489494, 12.200000181794167, -1.5707963267948966)), 
                                      (3, (25.400000378489494, 12.400000184774399, -1.5707963267948966)), 
                                      (4, (25.200000375509262, 12.600000187754631, -0.78539816339744828)), 
                                      (5, (25.200000375509262, 12.800000190734863, -1.5707963267948966)), 
                                      (6, (25.200000375509262, 13.000000193715096, -1.5707963267948966)), 
                                      (7, (25.200000375509262, 13.200000196695328, -1.5707963267948966)), 
                                      (8, (25.00000037252903, 13.40000019967556, -0.78539816339744828)), 
                                      (9, (24.800000369548798, 13.600000202655792, -0.78539816339744828)), 
                                      (10,(24.600000366568565, 13.800000205636024, -0.78539816339744828)), 
                                      (11,(24.600000366568565, 13.800000205636024, 0.0))])],
                                tagFile, 
                                skeleton)
                                
        classifiers = trainer_pacman.versionOne()

        followClassifier = classifiers["follow"]
        
        followClassifier.classify(situation)
        
        self.assertTrue(followClassifier.pTrue > 0.5)

    def testVerbClassifierTrue(self):
        
        
        map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
        cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
        gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
        tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
        tagFile.get_map()
        tagFile.get_tag_names()
        
        skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)

    
        situation = Situation([Agent("figure", 
                                     # a list of tuples
                                     # [(time1, (x1, y1, theta1)),
                                     #  (time2, (x2, y2, theta2))]
                                     [(0, (0, 0, 0)), 
                                      (1, (0, 1, 1)),
                                      (2, (0, 2, 2))]),
                               Agent("landmark",
                                     [(0, (0, -1, -1)), 
                                      (1, (0, 0, 0)),
                                      (2, (0, 1, 1))])],
                                tagFile, 
                                skeleton
                                      )

        classifiers = trainer_pacman.versionOne()

        followClassifier = classifiers["follow"]

        self.assertEqual(followClassifier.classify(situation), False)
        print "true", followClassifier.pTrue
        print "false", followClassifier.pFalse
        self.assertTrue(0 <= followClassifier.pTrue <=  1)
        self.assertTrue(0 <= followClassifier.pFalse <= 1)
        

        situation = Situation([Agent("figure", 
                                     [(0, (0, 0, 0)), 
                                      (1, (0, 1, 1)),
                                      (2, (0, 2, 2))]),
                               Agent("landmark",
                                     [(0, (0, 100, 100)), 
                                      (1, (0, 101, 101)),
                                      (2, (0, 102, 102))])],
                                tagFile,
                                skeleton)
        self.assertEqual(followClassifier.classify(situation), False)




    def testFollowStationary(self):
        from spatialRelationClassifier import SpatialRelationClassifier
        
        
        sr_class = SpatialRelationClassifier()
        
        result = sr_class.classify("to", [(0, 0), (10, 10)], [(9, 9), (9, 10), (10, 10), (10, 9)])
        
        map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
        cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
        gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
        tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
        tagFile.get_map()
        tagFile.get_tag_names()
        
        skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)

    
        situation = Situation([Agent("figure", 
                                     [(0, (25.400000378489494, 9.0000001341104507, 0.0))]),
                               Agent("landmark",
                                     [(0, (25.200000375509262, 11.800000175833702, 0.0)), 
                                      (1, (25.400000378489494, 12.000000178813934, -2.3561944901923448)), 
                                      (2, (25.400000378489494, 12.200000181794167, -1.5707963267948966)), 
                                      (3, (25.400000378489494, 12.400000184774399, -1.5707963267948966)), 
                                      (4, (25.200000375509262, 12.600000187754631, -0.78539816339744828)), 
                                      (5, (25.200000375509262, 12.800000190734863, -1.5707963267948966)), 
                                      (6, (25.200000375509262, 13.000000193715096, -1.5707963267948966)), 
                                      (7, (25.200000375509262, 13.200000196695328, -1.5707963267948966)), 
                                      (8, (25.00000037252903, 13.40000019967556, -0.78539816339744828)), 
                                      (9, (24.800000369548798, 13.600000202655792, -0.78539816339744828)), 
                                      (10,(24.600000366568565, 13.800000205636024, -0.78539816339744828)), 
                                      (11,(24.600000366568565, 13.800000205636024, 0.0))])],
                                tagFile, 
                                skeleton)
                                
        classifiers = trainer_pacman.versionOne()
        
        for name, c in classifiers.iteritems():
            print "domain", name, c.classifier.domain.classVar.values
            self.assertEqual(len(c.classifier.domain.classVar.values), 2)
        
        sr_class = SpatialRelationClassifier()
        result = sr_class.classify("to", [(0, 0), (10, 10)], [(9, 9), (9, 10), (10, 10), (10, 9)])


        followClassifier = classifiers["follow"]
        
        followClassifier.classify(situation)
        
        sr_class = SpatialRelationClassifier()
        result = sr_class.classify("to", [(0, 0), (10, 10)], [(9, 9), (9, 10), (10, 10), (10, 9)])

        followClassifier.classify(situation)
        self.assertTrue(followClassifier.pTrue > 0.5)
