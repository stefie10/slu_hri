from eventLogic.interval import OP, Interval, NINF, CL, PINF
from eventLogic.spanningInterval import SpanningIntervalSet, SpanningInterval, \
    emptySpanningIntervalSet, emptySpanningInterval
import unittest


class TestCase(unittest.TestCase):
    def testEqual(self):
        sis = SpanningIntervalSet([SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL)])
                                 
        self.assertEqual(sis, sis, True)
        
    def destIntersect(self):
        """
        erased intersect because it's hard to implement correctly
        """
        sis = SpanningIntervalSet([SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL)])
        self.assertEqual(sis, sis.intersect(sis))
        
    def testSomething(self):
        si1 = SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(CL, 1.0, 1.0, CL), OP)
        si2 = SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(CL, 1.0, 1.0, CL), OP)
        
        self.assertEquals(si1.containsInterval(Interval(CL, 0, 1, OP)), True)
        self.assertNotEqual(si1, emptySpanningInterval)        
        self.assertNotEqual(si1.normalized(), emptySpanningInterval)        
        print "si1", si1.normalized()
        
        sis = SpanningIntervalSet([si1, si2])
        

    def testEq(self):
        print "eq empty"
        self.assertEqual(emptySpanningIntervalSet, emptySpanningIntervalSet)
        print "neq empty"
        self.assertEqual(emptySpanningIntervalSet != emptySpanningIntervalSet, False)
        
        print "eq con"
        self.assertEqual(emptySpanningIntervalSet, SpanningIntervalSet([]))
        print "neq con"
        self.assertEqual(emptySpanningIntervalSet != SpanningIntervalSet([]), False)
        
    def testAverageLength(self):
        self.assertEqual(emptySpanningIntervalSet.averageLength, 0)
        self.assertEqual(emptySpanningIntervalSet.averageLength, 0)