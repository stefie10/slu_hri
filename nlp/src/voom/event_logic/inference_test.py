from datetime import datetime
from environ_vars import TKLIB_HOME
from eventLogic.inference import inference
from eventLogic.interval import OP, Interval, CL
from eventLogic.spanningInterval import SpanningIntervalSet, SpanningInterval, \
	emptySpanningIntervalSet
from voom.event_logic.features import modelForSituation
from voom.event_logic.primitives import approach, Inverted, IsClose, following
from voom.gui.assignments.assignmentData import Assignment
import cProfile
import carmen_map_skeletonizer
import tag_util
import unittest


class TestCase(unittest.TestCase):
	def testNormal(self):
		map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
		cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
		gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
		assignment_fn = "%s/nlp/data/aaai_2010_smv/stefie10/assignment1.1.yaml" % TKLIB_HOME
		tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
		tagFile.get_map()
		tagFile.get_tag_names()

		skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)
		assignment = Assignment.load(assignment_fn, tagFile, skeleton)

		slowEntry = assignment.entries[27]


		model = modelForSituation(slowEntry.situation) 
		print "model", model
		
		results = inference(model, Inverted(IsClose("figure", "landmark")))
		self.assertEqual(results,  SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 0.0, 23500.0, OP), Interval(OP, 0.0, 23500.0, CL), OP)]) != SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 0.0, 23600.0, OP), Interval(OP, 0.0, 23600.0, CL), OP)]))
		
		results = inference(model, IsClose("figure", "landmark"))
		self.assertEqual(results, SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 23600.0, 28500.0, CL), Interval(CL, 23600.0, 28500.0, CL), OP)]))
		
		
		results = inference(model, approach("figure", "landmark"))
		print "results", results
		self.assertEqual(results, SpanningIntervalSet([
	        SpanningInterval(CL, Interval(CL, 0.0, 23600.0, CL), Interval(CL, 23600.0, 28500.0, CL), OP)])) 
		
		
		results = inference(model, following("figure", "landmark"))
		print "results", results
		self.assertEqual(results, emptySpanningIntervalSet)

		
		
		
	def testSpeed(self):
		map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
		cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
		gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
		assignment_fn = "%s/nlp/data/aaai_2010_smv/stefie10/assignment1.1.yaml" % TKLIB_HOME
		tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
		tagFile.get_map()
		tagFile.get_tag_names()

		skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)
		assignment = Assignment.load(assignment_fn, tagFile, skeleton)

		slowEntry = assignment.entries[30]


		model = modelForSituation(slowEntry.situation) 
		
		def run():
			results = inference(model, approach("figure", "landmark"))
			print "results", results
			self.assertEqual(results,
SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 0.0, 3600.0, CL), Interval(CL, 3600.0, 6300.0, CL), OP),SpanningInterval(CL, Interval(CL, 6300.0, 24800.0, CL), Interval(CL, 24800.0, 31800.0, CL), OP)]))

		start = datetime.now()
		cProfile.runctx("run()", globals(), locals(), "profile.out")
		end = datetime.now()
		
		print "took", end - start
		


	def testFollow(self):
		map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
		cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
		gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
		assignment_fn = "%s/nlp/data/aaai_2010_smv/stefie10/assignment1.1.yaml" % TKLIB_HOME
		tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
		tagFile.get_map()
		tagFile.get_tag_names()

		skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)
		assignment = Assignment.load(assignment_fn, tagFile, skeleton)

		slowEntry = assignment.entries[0]


		model = modelForSituation(slowEntry.situation) 
		print "model", model
		

		results = inference(model, following("figure", "landmark"))
		
		self.assertEqual(results, SpanningIntervalSet([
             SpanningInterval(CL, Interval(CL, 1100.0, 5700.0, OP), Interval(OP, 1100.0, 5700.0, CL), OP),
             SpanningInterval(CL, Interval(CL, 6200.0, 15900.0, OP), Interval(OP, 6200.0, 15900.0, CL), OP),
             SpanningInterval(CL, Interval(CL, 16000.0, 21000.0, OP), Interval(OP, 16000.0, 21000.0, CL), OP)]))




