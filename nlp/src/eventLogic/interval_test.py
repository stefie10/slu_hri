from eventLogic import spanningInterval
from eventLogic.interval import Interval, CL, OP, NINF, PINF, min_inf, max_inf, \
    cmp_inf
import unittest




class TestCase(unittest.TestCase):
    
    def containment(self, i1, i2, isSubset, isSuperset):
        try:
            
            if i1 == i2:
                self.assertEqual(i1.subset(i2), False)
                self.assertEqual(i1.superset(i2), False)
            else:
                if isSubset or isSuperset:
                    self.assertEqual(i1.subset(i2), isSubset)
                    self.assertEqual(i2.subset(i1), not isSubset)
                    self.assertEqual(i1.superset(i2), not isSubset)
                    self.assertEqual(i1.superset(i2), isSuperset)
                    self.assertEqual(i2.superset(i1), isSubset)
                else:
                    self.assertEqual(i1.subset(i2), False)
                    self.assertEqual(i2.subset(i1), False)
                    self.assertEqual(i1.superset(i2), False)
                    self.assertEqual(i2.superset(i1), False)
                    
                    
        except:
            print "i1", i1
            print "i2", i2
            print "isSubset", isSubset
            print "isSuperset", isSuperset  
            raise
            
        
    
    def testSubsetAndSuperset(self):
        self.containment(Interval(CL, 0, 1, CL),
                         Interval(CL, -1, 2, CL), 
                         isSubset=True, isSuperset=False)
        
        self.containment(Interval(CL, -1, 2, CL),
                         Interval(CL, 0, 1, CL), 
                         isSubset=False, isSuperset=True)
        
        self.containment(Interval(OP, 0, 1, OP),
                         Interval(CL, 0, 1, CL), 
                         isSubset=True, isSuperset=False)
        
        self.containment(Interval(CL, 0, 1, CL),
                         Interval(OP, 0, 1, OP), 
                         isSubset=False, isSuperset=True)
        self.containment(Interval(OP, 0, 1, OP),
                         Interval(CL, 0, 1, CL), 
                         isSubset=True, isSuperset=False)
        
        self.containment(Interval(CL, 0, 1, OP),
                         Interval(CL, 0, 1, CL), 
                         isSubset=True, isSuperset=False)
                
        self.containment(Interval(OP, 0, 1, CL),
                         Interval(CL, 0, 1, CL), 
                         isSubset=True, isSuperset=False)
        
        self.containment(Interval(CL, 0, 1, CL),
                         Interval(CL, 0, 1, CL), 
                         isSubset=False, isSuperset=True)
        
        self.containment(Interval(CL, 0, 1, CL),
                         Interval(CL, 0.5, 1.5, CL), 
                         isSubset=False, isSuperset=False)
        
        self.containment(Interval(CL, 0, 1, CL),
                         Interval(CL, 10, 11, CL), 
                         isSubset=False, isSuperset=False)        
        
        self.containment(Interval(CL, 0.0, 1.0, CL),
                         Interval(CL, 0.0, 2.0, CL),
                         isSubset=True, isSuperset=False)
    def testCLInterval(self):
        interval = spanningInterval.Interval(CL, 0, 1, CL)
        
        self.assertEqual(interval.contains(0), True)
        self.assertEqual(interval.contains(0.5), True)
        self.assertEqual(interval.contains(1), True)
        
        self.assertEqual(interval.contains(2), False)
        self.assertEqual(interval.contains(-1), False)
        
        

    def testOPInterval(self):
        interval = spanningInterval.Interval(OP, 0, 1, OP)
       
        self.assertEqual(interval.contains(0), False)
        self.assertEqual(interval.contains(0.5), True)
        self.assertEqual(interval.contains(1), False)
        
        self.assertEqual(interval.contains(2), False)
        self.assertEqual(interval.contains(-1), False)
        
        


    def testHalfOPInterval1(self):
        interval = spanningInterval.Interval(CL, 0, 1, OP)
       
        self.assertEqual(interval.contains(0), True)
        self.assertEqual(interval.contains(0.5), True)
        self.assertEqual(interval.contains(1), False)
        
        self.assertEqual(interval.contains(2), False)
        self.assertEqual(interval.contains(-1), False)
        
        
    def testHalfOPInterval2(self):
        interval = spanningInterval.Interval(OP, 0, 1, CL)
       
        self.assertEqual(interval.contains(0), False)
        self.assertEqual(interval.contains(0.5), True)
        self.assertEqual(interval.contains(1), True)
        
        self.assertEqual(interval.contains(2), False)
        self.assertEqual(interval.contains(-1), False)
        
        
    def testInfinityLowerNeg(self):    
        interval = spanningInterval.Interval(OP, NINF, 1, CL)        
        self.assertEqual(interval.contains(0), True)
        self.assertEqual(interval.contains(0.5), True)
        self.assertEqual(interval.contains(1), True)
        
        self.assertEqual(interval.contains(2), False)
        self.assertEqual(interval.contains(-1), True)
        
        
    def testInfinityLowerPos(self):    
        interval = spanningInterval.Interval(OP, PINF, 1, CL)        
        self.assertEqual(interval.contains(0), False)
        self.assertEqual(interval.contains(0.5), False)
        self.assertEqual(interval.contains(1), False)
        
        self.assertEqual(interval.contains(2), False)
        self.assertEqual(interval.contains(-1), False)        
        
        
    def testInfinityUpperNeg(self):    
        interval = spanningInterval.Interval(OP, 1, NINF, CL)        
        self.assertEqual(interval.contains(0), False)
        self.assertEqual(interval.contains(0.5), False)
        self.assertEqual(interval.contains(1), False)
        
        self.assertEqual(interval.contains(2), False)
        self.assertEqual(interval.contains(-1), False)
        
        
    def testInfinityUpperPos(self):    
        interval = spanningInterval.Interval(OP, 1, PINF, CL)        
        self.assertEqual(interval.contains(0), False)
        self.assertEqual(interval.contains(0.5), False)
        self.assertEqual(interval.contains(1), False)
        
        self.assertEqual(interval.contains(2), True)
        self.assertEqual(interval.contains(-1), False)
                
                
    def testMin(self):
        self.assertEqual(min_inf([0,1]), 0)
        self.assertEqual(max_inf([0,1]), 1)        
        self.assertEqual(min_inf([0, PINF]), 0)
        self.assertEqual(max_inf([0, PINF]), PINF)
        
        
        self.assertEqual(min_inf([PINF, 3.0]), 3.0)        
                         
                         
        self.assertEqual(min_inf([0, NINF]), NINF)
        self.assertEqual(max_inf([0, NINF]), 0)                         
        
    def testCmp(self):
        self.assertEqual(cmp_inf(0, 0), 0)
        self.assertEqual(cmp_inf(NINF, PINF), -1)
        self.assertEqual(cmp_inf(0, 1), cmp(0, 1))
        self.assertEqual(cmp_inf(0, 1), -1)
        self.assertEqual(cmp_inf(NINF, 1), -1)
        self.assertEqual(cmp_inf(0, PINF), -1)        

        self.assertEqual(cmp_inf(1, 0), 1)
        
    def testSpan(self):
        self.assertEqual(Interval.span(Interval(OP, 1, 4, OP),
                                       Interval(CL, 2, 6, CL)),
                         Interval(OP, 1, 6, CL))
        
    def testCenter(self):
        self.assertEqual(Interval(OP, 1, 4, OP).center, 2.5)
        self.assertEqual(Interval(OP, -1, 3, OP).center, 1)
        
        self.assertEqual(Interval(OP, NINF, PINF, OP).center, 0)
        
    def testLength(self):
        self.assertEqual(Interval(OP, 1, 4, OP).length, 3)
        self.assertEqual(Interval(OP, -1, 3, OP).length, 4)
        
        self.assertEqual(Interval(OP, NINF, PINF, OP).length, PINF)
        