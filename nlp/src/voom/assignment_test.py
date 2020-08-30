from environ_vars import TKLIB_HOME
from voom.gui.assignments.assignmentData import Assignment
import carmen_map_skeletonizer
import os
import tag_util
import unittest


class TestCase(unittest.TestCase):
    def testLoad(self):
        map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
        cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
        gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
        assignment_fn = "%s/nlp/data/aaai_2010_smv/stefie10/assignment1.2.yaml" % TKLIB_HOME
        tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
        tagFile.get_map()
        tagFile.get_tag_names()
    

        skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)
        assignment = Assignment.load(assignment_fn, tagFile, skeleton)
         

        firstEntry = assignment.entries[0]
        
        self.assertEqual(firstEntry.verb, "follow")
        self.assertEqual(firstEntry.command, "Follow the person to the kitchen.\n")
        self.assertTrue(firstEntry.situation != None)
        
        sdcs = firstEntry.sdcs("stefie10")
        self.assertEqual(len(sdcs), 2)
        self.assertEqual(sdcs[0].verb.text, "Follow")
        self.assertEqual(sdcs[1].spatialRelation.text, "to")
        
        fname = "test.yaml"
        assignment.save(fname)
        os.remove(fname)
        