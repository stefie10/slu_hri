from eventLogic.spanningInterval import Interval, SpanningInterval, \
    emptySpanningInterval, NINF, PINF, CL, OP, SpanningIntervalSet
import unittest



class TestCase(unittest.TestCase):
    def containment(self, i1, i2, isProperSubset, isSuperset):
        try:
            
            self.assertEqual(i1.properSubset(i2), isProperSubset)
            
            if i1.properSubset(i2):
                self.assertEqual(i1.subset(i2), True)
            
            if i2.properSubset(i1):
                self.assertEqual(i2.subset(i1), True)
                                 
            if i1 == i2:
                self.assertEqual(isProperSubset, False)
                self.assertEqual(isSuperset, False)
                self.assertEqual(i1.subset(i2), True)
                self.assertEqual(i2.subset(i1), True)
                self.assertEqual(i1.properSubset(i2), False)
                self.assertEqual(i1.superset(i2), False)
                self.assertEqual(SpanningInterval.intersection(i1, i2),
                                 i1)
                self.assertEqual(SpanningInterval.intersection(i1, i2),
                                 i2)
            else:
                if isProperSubset or isSuperset:
                    self.assertEqual(i1.properSubset(i2), isProperSubset)
                    self.assertEqual(i2.properSubset(i1), not isProperSubset)
                    self.assertEqual(i1.superset(i2), not isProperSubset)
                    self.assertEqual(i1.superset(i2), isSuperset)
                    self.assertEqual(i2.superset(i1), isProperSubset)
                    
                    if isProperSubset:
                        self.assertEqual(SpanningInterval.intersection(i1, i2),
                                         i1)
                        self.assertEqual(SpanningInterval.intersection(i2, i1),
                                         i1)
                    if isSuperset:
                        self.assertEqual(SpanningInterval.intersection(i1, i2),
                                         i2)
                        self.assertEqual(SpanningInterval.intersection(i2, i1),
                                         i2)                    
                else:
                    self.assertEqual(i1.properSubset(i2), False)
                    self.assertEqual(i2.properSubset(i1), False)
                    self.assertEqual(i1.superset(i2), False)
                    self.assertEqual(i2.superset(i1), False)
                    
                    
        except:
            print "i1", i1
            print "i2", i2
            print "isProperSubset", isProperSubset
            print "isSuperset", isSuperset  
            raise

    def testContainsSubset(self):
        self.containment(SpanningInterval(CL, Interval(CL, 0, 1, CL),
                                          Interval(CL, 2, 3, CL), CL),
                         SpanningInterval(CL,Interval(CL, 0, 1, CL),
                                           Interval(CL, 2, 3, CL), CL),
                         isProperSubset=False, isSuperset=False)
        
        self.containment(SpanningInterval(CL, Interval(OP, 0, 1, CL),
                                          Interval(CL, 2, 3, CL), CL),
                         SpanningInterval(CL,Interval(CL, 0, 1, CL),
                                           Interval(CL, 2, 3, CL), CL),
                         isProperSubset=True, isSuperset=False)        
        
        self.containment(SpanningInterval(CL, Interval(CL, 0, 1, OP),
                                          Interval(CL, 2, 3, CL), CL),
                         SpanningInterval(CL,Interval(OP, 0, 1, OP),
                                           Interval(CL, 2, 3, CL), CL),
                        isProperSubset=False, isSuperset=True)
        

        
        self.containment(SpanningInterval(CL, Interval(CL, 0, 1, CL),
                                          Interval(OP, 2, 3, CL), CL),
                         SpanningInterval(CL,Interval(OP, 0, 1, OP),
                                           Interval(CL, 2, 3, CL), CL),
                        isProperSubset=False, isSuperset=False)
        
        self.containment(SpanningInterval(CL, Interval(CL, 0, 1, CL),
                                          Interval(OP, 2, 3, CL), CL),
                         SpanningInterval(CL,Interval(OP, 10, 11, OP),
                                           Interval(CL, 12, 13, CL), CL),
                        isProperSubset=False, isSuperset=False)
        
        
        self.containment(SpanningInterval(CL, Interval(CL, 0, 1, CL),
                                          Interval(OP, 2, 3, CL), CL),
                        SpanningInterval(OP,Interval(CL, 0, 1, CL),
                                           Interval(CL, 2, 3, CL), CL),
                        isProperSubset=False, isSuperset=False)
        self.containment(SpanningInterval(CL, Interval(CL, 0, 1, CL),
                                          Interval(OP, 2, 3, CL), CL),
                        SpanningInterval(CL,Interval(CL, 0, 1, CL),
                                           Interval(CL, 2, 3, CL), OP),
                        isProperSubset=False, isSuperset=False)        
        
        
        
        self.containment(SpanningInterval(CL, Interval(CL, 0.0, 1.0, CL), Interval(CL, 0.0, 1.0, CL), CL),
                         SpanningInterval(CL, Interval(CL, 0.0, 1.0, CL), Interval(CL, 0.0, 2.0, CL), CL),
                         isProperSubset=True, isSuperset=False)

        self.containment(SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP),
                         SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
                         isProperSubset=True, isSuperset=False)
        
        
        self.containment(SpanningInterval(CL, Interval(CL, 1.0, 1.0, CL), Interval(CL, 1.0, 1.0, CL), CL),
                         SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL),
                         isProperSubset=True, isSuperset=False)
        
        self.containment(SpanningInterval(CL, Interval(CL, 1.0, 1.0, CL), Interval(CL, 1.0, 1.0, CL), CL),
                         SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL),
                         isProperSubset=True, isSuperset=False)



        
    def testUnion1(self):
        si1 = SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), CL)
        si2 = SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL)
        self.containment(si1, si2, isProperSubset=False, isSuperset=False)
        
        self.assertEqual(si1.containsInterval(Interval(CL, 1, 1, CL)),
                        False)
        
        self.assertEqual(si2.containsInterval(Interval(CL, 1, 1, CL)),
                        True)
        
        csi1 = si1.complement()
        
        interval = csi1.intersectInterval(si2)
        
        self.assertEqual(SpanningInterval.union(si1, si2),
                         SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL),
                                                               Interval(CL,1.0, PINF, OP), CL)]))
        
        self.assertEqual(SpanningInterval.union(SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), CL),
                                                SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), CL)),
                        SpanningIntervalSet([SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL)]))
                                                
            
    def testContainsInterval(self):
        
        
        si = SpanningInterval(CL, 
                              Interval(CL, 0, 1, CL),
                              Interval(CL, 2, 3, CL),
                              CL)
        
        self.assertEqual(si.containsInterval(Interval(CL, 0.5, 2.5, CL)), True)
        
    def testContains(self):
        
        
        si = SpanningInterval(CL, 
                              Interval(CL, 0, 1, CL),
                              Interval(CL, 2, 3, CL),
                              CL)
        
        self.assertEqual(si.contains(0), True)
        
        self.assertEqual(si.contains(1.5), True)
        
        self.assertEqual(si.contains(3.1), False)
        
    def testEmptyInterval(self):
        self.assertEqual(emptySpanningInterval.containsInterval(Interval(CL, 0.5, 2.5, CL)), False)
        
        self.assertEqual(emptySpanningInterval.containsInterval(Interval(OP, 0.5, 2.5, OP)), False)
        
    def testNormalizeNoop(self):
            
        si = SpanningInterval(CL, 
                              Interval(CL, 0, 1, CL),
                              Interval(CL, 2, 3, CL),
                              CL)
        nsi = si.normalized()
        self.assertEqual(si, nsi)
        
    def testEqual(self):
        self.assertEqual(SpanningInterval(CL, 
                                          Interval(CL, 0, NINF, CL),
                                          Interval(CL, 2, 3, CL),
                                          CL),
                         SpanningInterval(CL, 
                                          Interval(CL, 0, NINF, CL),
                                          Interval(CL, 2, 3, CL),
                                          CL))
        
        
                                
    def testNormalizeC1(self):
            
        self.assertEqual(SpanningInterval(CL, 
                              Interval(CL, 0, NINF, CL),
                              Interval(CL, 2, 3, CL),
                              CL).normalized(),
                         emptySpanningInterval)
        
        self.assertEqual(SpanningInterval(CL, 
                              Interval(CL, PINF, 1, CL),
                              Interval(CL, 2, 3, CL),
                              CL).normalized(),
                              emptySpanningInterval)        
                
        self.assertEqual(SpanningInterval(CL, 
                              Interval(CL, 0, 1, CL),
                              Interval(CL, 2, NINF, CL),
                              CL).normalized(),
                              emptySpanningInterval)
        
        self.assertEqual(SpanningInterval(CL, 
                              Interval(CL, 0, 1, CL),
                              Interval(CL, PINF, 3, CL),
                              CL).normalized(),
                              emptySpanningInterval)        


    def testNormalizeC2(self):

        ns1 = SpanningInterval(CL, 
                              Interval(CL, NINF, 1, CL),
                              Interval(CL, 2, 3, CL),
                              CL).normalized()
                              
        self.assertEqual(ns1.i1.alpha, OP)
        self.assertEqual(ns1.i1.beta, CL)
        
        print "failing"
        ns1 = SpanningInterval(CL, 
                              Interval(CL, 1, PINF, CL),
                              Interval(CL, 2, 3, CL),
                              CL).normalized()
        self.assertEqual(ns1.j, 3)                      
        self.assertEqual(ns1.gamma, CL)
        self.assertEqual(ns1.delta, CL)
        
                
                              

    def testNormalizeOp(self):
        si = SpanningInterval(OP, Interval(CL, 1.0, 3.0, CL), 
                              Interval(CL, 1.0, 3.0, CL), OP)        
        self.assertEqual(si.normalized(), 
                         SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), 
                              Interval(OP, 1.0, 3.0, CL), OP))
                         
                         
        si2 = SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), 
                               Interval(CL, 1.0, 3.0, CL), CL)
        
        self.assertEqual(si2.normalized(),
                         SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), 
                              Interval(CL, 1.0, 3.0, CL), CL))
                         
                         
    def testIntersect(self):
        
        s1 = SpanningInterval(CL,
                              Interval(CL, NINF, 1, CL),
                              Interval(CL, 2, 3, CL),
                              CL).normalized()
        
        s2 = SpanningInterval(CL,
                              Interval(CL, NINF, 1, CL),
                              Interval(CL, 2.1, 2.9, CL),
                              CL).normalized()        
        
        self.assertEqual(SpanningInterval.intersection(s1, emptySpanningInterval),
                         emptySpanningInterval)
        
        
        self.assertEqual(SpanningInterval.intersection(s1, s1), s1)
        
                                                       
        self.assertEqual(SpanningInterval.intersection(s1, s2), s2)
    
    
    def testIntersect2(self):
        
        s1 = SpanningInterval(CL,
                              Interval(CL, 1, 2, CL),
                              Interval(CL, 2, 3, CL),
                              CL)
        
        s2 = SpanningInterval(CL,
                              Interval(CL, 1.5, 2.5, CL),
                              Interval(CL, 2.1, 2.9, CL),
                              CL)        
        
        self.assertEqual(SpanningInterval.intersection(s1, s2),
                         SpanningInterval(CL, Interval(CL, 1.5, 2, CL),
                                          Interval(CL, 2.1, 2.9, CL), CL))
        
        

        
    def testSnapToZero(self):
        self.assertEqual(Interval(CL, NINF, 1, OP).snappedToMin(value=0),
                         Interval(CL, 0, 1, OP))
        
        
    def testSpan(self):
        self.assertEqual(SpanningInterval.span(SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, 0, 1, CL), CL),
                                               SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, 0, 1, CL), CL)),
                        SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, 0, 1, CL), CL)]))
        
        self.assertEqual(SpanningInterval.span(SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, 0, 1, CL), CL),
                                               SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, 0, 2, CL), CL)).condensed(),
                        SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, 0, 2, CL), CL)]))        

        self.assertEqual(SpanningInterval.span(SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, 0, 1, CL), CL),
                                               SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, -1, 2, CL), CL)).condensed(),
                        SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, -1, 2, CL), CL)]))
        
        
        self.assertEqual(SpanningInterval.span(SpanningInterval(CL, Interval(CL, 0, 1, OP), Interval(CL, 0, 1, CL), CL),
                                               SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, -1, 2, CL), CL)).condensed(),
                        SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 0, 1, CL), Interval(CL, -1, 2, CL), CL)]))
        
        
    def testCondense(self):
        setFromInference = SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), CL),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL)])
        
        self.assertEqual(setFromInference.condensed(),
                         SpanningIntervalSet([
             SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
             SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
             SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL)])) 


        self.assertEqual(SpanningIntervalSet([
             SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, 3.0, PINF, OP), CL),
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP),
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP)]).condensed(),
                         SpanningIntervalSet([
             SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, 3.0, PINF, OP), CL),
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP),
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP)                    
                                              ]))



        sis = SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 1, OP), Interval(OP, NINF, 1, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 1, OP), Interval(OP, NINF, 1, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 1, OP), Interval(OP, NINF, 1, OP), OP),
            SpanningInterval(CL, Interval(OP, NINF, 1, OP), Interval(OP, NINF, 1, OP), CL),
            SpanningInterval(OP, Interval(OP, 3, PINF, OP), Interval(OP, 3, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, 3, PINF, OP), Interval(OP, 3, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, 3, PINF, OP), Interval(OP, 3, PINF, OP), OP),
            SpanningInterval(CL, Interval(OP, 3, PINF, OP), Interval(OP, 3, PINF, OP), CL)])
        self.assertEqual(sis.condensed(), sis)
        
        
        sis = SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), CL),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL)])

        self.assertEqual(sis.condensed(), SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL)]))
                         

        self.assertEqual(SpanningIntervalSet([
            SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP), 
            SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, PINF, OP), CL), 
            SpanningInterval(CL, Interval(OP, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP), 
            SpanningInterval(CL, Interval(OP, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), CL), 
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP), 
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL), 
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP), 
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL), 
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP), 
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), CL), 
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP), 
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL), 
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), CL), 
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), CL), 
            SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), CL), 
            SpanningInterval(CL, Interval(OP, 1.0, 3.0, CL), Interval(OP, 1.0, 3.0, CL), CL), 
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP), 
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), CL), 
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP), 
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), CL), 
            SpanningInterval(OP, Interval(OP, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP), 
            SpanningInterval(OP, Interval(OP, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, OP), CL), 
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP), 
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL)]).condensed(),
                SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL)]))            
            


    def testCenter(self):
        self.assertEqual(SpanningInterval(CL, 
                                          Interval(OP, 0, 3.0, CL), 
                                          Interval(CL, 4, 7, OP), CL).averageLength,
                                          4.0)
        
        self.assertEqual(SpanningInterval(CL, 
                                          Interval(OP, 0, 3.0, CL), 
                                          Interval(CL, 3, 7, OP), CL).averageLength,
                                          3.5)
        
        self.assertEqual(SpanningInterval(CL, 
                                          Interval(OP, 0, 3.0, CL), 
                                          Interval(CL, 1.5, 3, OP), CL).averageLength,
                                          0.75)
        
        
        #self.assertEqual(SpanningInterval(CL, 
        #                                  Interval(OP, 0, 3.0, CL), 
        #                                  Interval(OP, 0, 3.0, CL), 
        #                                  CL).averageLength,
        #                                 help)
