import unittest
import crfEntityExtractor
from spatialRelationClassifier import SpatialRelationClassifier, isPolygon, ensurePolygon
import spatialRelationClassifier
from tag_util import pointToSmallPolygon
from numpy import array
from routeDirectionCorpusReader import readSession, Standoff, Annotation

class SpatialRelationClassifierTest(unittest.TestCase):
    def testVerticalSegmentError(self):
        src = SpatialRelationClassifier()

        
        classifier, isValid, score = \
        src.classify("towards", figure=[array([
        1.16521661, 1.79445365]), array([ 1.17431053, 1.810358 ]),
        array([ 1.17685383, 1.83220017]), array([ 1.17846236,
        1.8309133 ]), array([ 1.08655326, 1.85139911]), array([
        1.04491159, 1.85715779]), array([ 1.02414257, 1.85796336]),
        array([ 1.01261087, 2.03829384]), array([ 1.00472829, 2.120413
        ]), array([ 1.10639252, 2.10638181]), array([ 1.15350338,
        2.05383215]), array([ 1.18654435, 1.95352735]), array([
        1.18111801, 1.88050301]), array([ 1.18039583, 1.83389818]),
        array([ 1.18053703, 1.83085798])], landmark=
        [[-0.15579999254941945, 8.1590001475214962],
        [2.4442000461935995, 8.1590001475214962], [2.5442000476837157,
        4.2590000894069675], [4.2442000730156897,
        -0.34099997913837443], [-0.25579999403953557,
        -0.34099997913837443], [-0.25579999403953557,
        3.1590000730156897]])

        self.assertEqual(isValid.__class__, bool)
        print "score", score
        self.assertTrue(0 <= score)
        self.assertTrue(score <= 1)
        self.assertTrue(isinstance(classifier.name(), str))
