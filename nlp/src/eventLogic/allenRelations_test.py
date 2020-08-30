from eventLogic import allenRelations
from eventLogic.spanningInterval import Interval, CL
import unittest


class TestCase(unittest.TestCase):
    def testRelations(self):
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0, 1, CL), 
                                                     Interval(CL, 1, 2, CL)), 
                         allenRelations.overlaps)
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 1, 2, CL), 
                                                     Interval(CL, 0, 1, CL)), 
                         allenRelations.iOverlaps)
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0, 1.5, CL), 
                                                     Interval(CL, 1, 2, CL)), 
                         allenRelations.overlaps)
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 1, 2, CL), 
                                                     Interval(CL, 0, 1.5, CL)),
                         allenRelations.iOverlaps)
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0, 1.5, CL), 
                                                     Interval(CL, 0, 0.1, CL)), 
                         allenRelations.iStarts)
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0, 0.1, CL),
                                                     Interval(CL, 0, 1.5, CL)), 
                         allenRelations.starts)
        
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0, 0.1, CL), 
                                                     Interval(CL, 0.5, 1.5, CL)), 
                         allenRelations.lessThan)
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0.5, 1.5, CL), 
                                                     Interval(CL, 0, 0.1, CL)), 
                         allenRelations.greaterThan)

        self.assertEqual(allenRelations.findRelation(Interval(CL, 0.5, 1, CL), 
                                                     Interval(CL, 0, 1, CL)),
                         allenRelations.finishes)
                    
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0, 1, CL), 
                                                     Interval(CL, 0.5, 1, CL)),
                         allenRelations.iFinishes)
        
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0.5, 0.75, CL), 
                                                     Interval(CL, 0, 1, CL)),
                         allenRelations.during)
        
        self.assertEqual(allenRelations.findRelation(Interval(CL, 0, 1, CL), 
                                                     Interval(CL, 0.5, 0.75, CL)),
                         allenRelations.iDuring)