import unittest
import math2d
from math2d import assert_array_equal
import math
import numpy as na
class Math2dTestCase(unittest.TestCase):

    def testDerivativeLine(self):
        x = [1,2,3,4,5]
        y = x
        d = math2d.derivative(x,y)
        for v in d:
            assert v == 1
        assert len(d) == (len(x) - 1)

    def testDerivativeConst(self):
        x = [1,2,3,4,5]
        y = [3,3,3,3,3]
        d = math2d.derivative(x,y)
        for v in d:
            assert v == 0
        assert len(d) == (len(x) - 1)
    def testSlope(self):
        self.assertEqual(math2d.slope([(0,0),(1,1)]),1)
        self.assertEqual(math2d.slope([(0,0),(1,2)]),2)
        self.assertEqual(math2d.slope([(0,0),(1,0)]),0)
        self.assertEqual(math2d.slope([(-1,-1),(-0.5,-1.5)]),-1)
        self.assertEqual(math2d.slope([(0, 0),(1, 1)]), 1)
        self.assertEqual(math2d.slope([(2, 0),(3, 1)]), 1)
    
    def testAngleBetweenLines(self):
        math2d.assert_sorta_eq(math2d.angleBetweenLines([(19.389336154019233, 42.15152942637345), (19.464743879790959, 41.891026265250737)],
                                                  [(19.389336154019233, 42.15152942637345), (19.528665819159336, 41.670072090631557)]),
                               0)

        
        self.assertEqual(math2d.angleBetweenLines([(0,0),(1,1)],
                                                  [(0,0),(-1,1)]),
                         math.pi/2)

        self.assertEqual(math2d.angleBetweenLines([(0,0),(-1,1)],
                                                  [(0,0),(1,1)]),
                         math.pi/2)

        self.assertEqual(math2d.angleBetweenLines([(0,0),(1,1)],
                                                  [(0,0),(1,0)]),
                         math.pi/4)

        self.assertEqual(math2d.angleBetweenLines([(0,0),(0,1)],
                                                  [(0,0),(1,0)]),
                         math.pi/2)

        self.assertEqual(math2d.angleBetweenLines([(22.538, 15.308377141861092), 
                                                   (22.538, 15.308377141861092)],
                                                  [(26.99214769,  12.12461925),  
                                                   (7.22290453,  31.89386241)]),
                         0)

    def testCenterOfMass(self):
        self.assertEqual(math2d.centerOfMass([(0,0), (1, 1), (-1, -1)]),
                         (0, 0))

        self.assertEqual(math2d.centerOfMass([(0,0), (1, 1)]),
                         (0.5, 0.5))
        self.assertEqual(math2d.centerOfMass([(0,1), (-1, 1)]),
                         (-0.5, 1))

    def testArea(self):
        self.assertEqual(math2d.area([(0, 0), (1, 0), (1, 1), (0, 1)]),
                         1)

        self.assertEqual(math2d.area([(0, 0), (1, 0), (1, 1)]),
                         0.5)

        self.assertEqual(math2d.area([(0, 0), (1, 1), (-1, -1)]),
                         0)
        self.assertEqual(math2d.area([(0.0, 0.0), (0, 1), (1, 1), (1, 2), (2, 2),
                                      (2.0, 0)]),
                                     3)
        
        self.assertEqual(math2d.area([(-1, -3), (2, 1), (8, -4)]),
                         19.5)
        

    def testSignedArea(self):
        self.assertEqual(math2d.signedArea([(0, 0), (1, 0), (1, 1), (0, 1)]),
                         1)

        self.assertEqual(math2d.signedArea([(0, 0), (1, 0), (1, 1)]),
                         0.5)

        self.assertEqual(math2d.signedArea([(0, 0), (1, 1), (-1, -1)]),
                         0)
        self.assertEqual(math2d.signedArea([(0.0, 0.0), (0, 1), (1, 1), (1, 2), (2, 2),
                                      (2.0, 0)]),
                                     -3)
        
        self.assertEqual(math2d.signedArea([(-1, -3), (2, 1), (8, -4)]),
                         -19.5)

        self.assertEqual(math2d.signedArea([(8, -4), (2, 1), (-1, -3)]),
                         19.5)
        

    def testCentroid(self):
        self.assertEqual(math2d.centroid([(0,0), (1, 0), (1, 1), (0, 1)]),
                         (0.5, 0.5))

        self.assertEqual(math2d.centroid([(0,0), (-1, 0), (-1, -1), (0, -1)]),
                         (-0.5, -0.5))

        self.assertEqual(math2d.centroid([ (-1, -3), (8, -4), (2, 1)]),
                         (3, -2))
        self.assertEqual(math2d.centroid([(8, -4), (-1, -3), (2, 1)]),
                         (3, -2))
        self.assertEqual(math2d.centroid([(8, -4),  (2, 1), (-1, -3)]),
                         (3, -2))


    def testIsOnSegment(self):

        self.assertEqual(math2d.isOnSegment([(0,0),(0,0)],(0,0)),
                         True)
        self.assertEqual(math2d.isOnSegment([(0,0),(0,0)],(1,1)),
                         False)

        self.assertEqual(math2d.isOnSegment([(0, 0), (1, 1)], (0.5, 0.5)), 
                         True)
        self.assertEqual(math2d.isOnSegment([(1, 1), (0, 0)], (0.5, 0.5)), 
                         True)
        self.assertEqual(math2d.isOnSegment([(0, 0), (1, 1)], (0.5, 0.6)),
                         False)
        self.assertEqual(math2d.isOnSegment([(0, 0), (1, 1)], (0, 0)), 
                         True)

        self.assertEqual(math2d.isOnSegment([(2, 0), (1.5, 14)],
                                            (1.899999999999, 2.800000000000000000000003)),
                         True)

        self.assertEqual(math2d.isOnSegment([(0, 0), (0, 1)],
                                            (0, 0.5)),
                         True)
        self.assertEqual(math2d.isOnSegment([(0, 0), (0, 0)], (0.5, 0.5)),
                         False)

        self.assertEqual(math2d.isOnSegment([(0.0, 0.5), (1.0, 0.5)], (0.5, 0.5)),
                         True)
        self.assertEqual(math2d.isOnSegment([(0.5, 1.0), (0.5, 0.0)], (0.5, 0.5)),
                         True)

        self.assertEqual(math2d.isOnSegment([(0, 0), (1, 1)], (1, 1)),
                         True)
        self.assertEqual(math2d.isOnSegment([(3, 0), (1, 1)], (1, 1)),
                         True)

        self.assertEqual(math2d.isOnSegment([(0.548, -0.478),
                                            (0.344, 0.249)],
                                            (0.344, 0.249)),
                         True)
        
        self.assertEqual(math2d.isOnSegment([(0.482, -0.388),
                                             (0.344, 0.249)],
                                            (0.344, 0.249)),
                         True)


        

    def testIsOnLine(self):
        self.assertEqual(math2d.isOnLine([(0, 0), (1, 1)], (0.5, 0.5)), 
                         True)
        self.assertEqual(math2d.isOnLine([(1, 1), (0, 0)], (0.5, 0.5)), 
                         True)
        self.assertEqual(math2d.isOnLine([(0, 0), (1, 1)], (0.5, 0.6)),
                         False)
        self.assertEqual(math2d.isOnLine([(0, 0), (1, 1)], (0, 0)), 
                         True)

        self.assertEqual(math2d.isOnLine([(2, 0), (1.5, 14)],
                                            (1.899999999999, 2.800000000000000000000003)),
                         True)

        self.assertEqual(math2d.isOnLine([(0, 0), (0, 1)],
                                            (0, 0.5)),
                         True)
        # degenerate lines

        self.assertEqual(math2d.isOnLine([(-1, 0), (0, 0), (0, 0)], (0.5, 0.5)),
                         False)
        
        # vertical messes it up...
        self.assertEqual(math2d.isOnSegment([(22.538,25.019), 
                                             (22.538,24.9815)],
                                            (22.538, 28.749081807199808)),
                         False)
    def testIntersectLines(self):
        self.assertEqual(math2d.intersectLines([(0, 0), (1, 1), (2, 3)],
                                               [(0, 1), (1, 0), (2, 0)]),
                                               [(0.5, 0.5)])

        self.assertEqual(math2d.intersectLines([(0, 0), (1, 1), (2, 3)],
                                               [(0, 1), (1, 0), (2, 0), 
                                                (1.5, 14)]),
                         [(0.5, 0.5), (1.8999999999999999, 2.7999999999999998)])

        self.assertEqual(math2d.intersectLines([(0, 0), (1, 0), (1, 1), (0, 1)],
                                               [(-0.5, 0.5), (1.5, 0.5)]),
                         [(1, 0.5)])
        self.assertEqual(math2d.intersectLines([(0, 0), (1, 0), (1, 1), (0, 1),
                                                (0, 0)],
                                               [(-0.5, 0.5), (1.5, 0.5)]),
                         [(1, 0.5), (0, 0.5)])

        self.assertEqual(math2d.intersectLines([(0, 0), (1, 1)],
                                               [(3, 0), (1, 1)]),
                         [(1, 1)])

        assert_array_equal(math2d.intersectLines([(-0.12, 0.431), 
                                                         (0.548, -0.478),
                                                         (0.344, 0.249)],
                                                        
                                                        [(-0.12, 0.431),
                                                         (0.482, -0.388),
                                                         (0.344, 0.249)]),
                                  [(-0.12, 0.431), 
                                   (0.48205794570672578, -0.38826747402307443),
                                   (0.344, 0.249)])

        # because there are two 0,0's on the line.
        # not sure what the correct behavior should be.
        self.assertEqual(math2d.intersectLines([(0, 0), (1, 1), (1, 0), (0, 0)],
                                               [(0, 0), (0, 1)]),
                         [(0, 0)]) 


        # from map/robot corpus. It's sticking the first potin on the end for some reason.
        figure = [(22.8,29.4), (23,29.2), (23.2,29.2), (23.4,29.2), (23.6,29.2), (23.8,29.2), (24,29.2), (24.2,29.2), (24.4,29), (24.6,29), (24.8,29), (25,28.8), (25,28.6), (25,28.4), (25,28.2), (25,28), (25,27.8), (25,27.6), (25,27.4), (25,27.2), (25,27), (25,26.8), (24.8,26.6), (24.8,26.4), (24.8,26.2), (24.8,26), (24.6,25.8), (24.6,25.6), (24.4,25.4), (24.4,25.2), (24.4,25), (24.4,24.8), (24.4,24.6), (24.4,24.4), (24.4,24.2), (24.4,24), (24.4,23.8), (24.4,23.6), (24.4,23.4), (24.4,23.2), (24.4,23), (24.4,22.8), (24.4,22.6), (24.4,22.4), (24.4,22.2), (24.4,22), (24.4,21.8), (24.4,21.6), (24.2,21.4), (24.4,21.2), (24.6,21), (24.8,21), (25,21), (25.2,21), (25.4,21), (25.6,21), (25.8,21), (26,21), (26.2,21), (26.4,21), (26.6,21), (26.8,21), (27,21), (27.2,21.2), (27.4,21), (27.6,21), (27.8,21), (28,20.8), (28.2,20.8), (28.4,20.8), (28.6,20.8), (28.8,20.8), (29,20.6), (29.2,20.6), (29.4,20.6), (29.6,20.6), (29.8,20.6), (30,20.6), (30.2,20.6), (30.4,20.4), (30.6,20.4), (30.8,20.4), (31,20.4), (31.2,20.4), (31.4,20.4), (31.6,20.4), (31.8,20.2), (32,20.2), (32.2,20.2), (32.4,20.2), (32.6,20.2), (32.8,20.2), (33,20.2), (33.2,20.2), (33.4,20), (33.6,20), (33.8,20), (34,20), (34.2,20), (34.4,20), (34.6,20), (34.8,20), (35,20), (35.2,20), (35.4,20), (35.6,20), (35.8,20), (36,20), (36.2,20), (36.4,19.8), (36.6,19.8)]
        ground = [(25.2,20.2), (25.2,22.2), (27.2,22.2), (27.2,20.2)]
        math2d.assert_array_equal(math2d.intersectLines(figure, ground),
                                  [(25.2, 21), (27.2, 21.2)])
        
    def testIntersectPolygons(self):
        self.assertEqual(math2d.intersectPolygons([(0, 0), (1, 0), 
                                                   (1, 1), (0, 1)],
                                                  [(2, 0), (3, 0), 
                                                   (3, 1), (2, 1)]),
                         False)

        self.assertEqual(math2d.intersectPolygons([(0, 0), (1, 0), 
                                                   (1, 1), (0, 1)],
                                                  [(0.5, 0.5), (1, 0.5), 
                                                   (1, 3), (0.5, 3)]),
                         True)

        self.assertEqual(math2d.intersectPolygons([(0, 0), (1, 0), 
                                                   (1, 1), (0, 1)],
                                                  [(0, 0), (1, 0), 
                                                   (1, 1), (0, 1)]),
                         True)

        self.assertEqual(math2d.intersectPolygons([(0, 0), (1, 0), 
                                                   (1, 1), (0, 1)],
                                                  [(0.2, 0.2), (0.3, 0.2), 
                                                   (0.3, 0.3), (0.2, 0.3)]),
                         True)
        
                         
    def testIntersectSegment(self):
        # lower segment is vertical.
        # upper segment goes above it.
        self.assertEqual(math2d.intersectSegment([(23.3159,28.7462),
                                                  (10.8989,28.7922)
                                                  ],
                                                 [(22.538,25.019), 
                                                  (22.538,24.9815)]),
                         None)

        self.assertEqual(math2d.intersectSegment([(0.0, 0.5), (1.0, 0.5)],
                                                 [(0.5, 1.0), (0.5, 0.0)]),
                         (0.5, 0.5))


        self.assertEqual(math2d.intersectSegment([(10.8989,28.7922), 
                                                  (23.3159,28.7462)],
                                                 [(22.538,25.019), 
                                                  (22.538,24.9815)]),
                         None)
        self.assertEqual(math2d.intersectSegment([(-1.0, -1.0), (1.0, 1.0)],
                                          [(1, -1), (-1, 1)]),
                         (0, 0))
        self.assertEqual(math2d.intersectSegment([(0, 0), (1, 1)],
                                                 [(0, 1), (1, 0)]),
                         (0.5, 0.5))

        self.assertEqual(math2d.intersectSegment([(2, 0), (1.5, 14)],
                                                 [(1, 1), (2, 3)]),
                         (1.8999999999999999, 2.8000000000000003))

        self.assertEqual(math2d.intersectSegment([(0, 0), (0, 1)],
                                                 [(-0.5, 0.5), (0.5, 0.5)]),
                         (0, 0.5))
        
        self.assertEqual(math2d.intersectSegment([(0, 0), (1, 0)],
                                                 [(-0.5, 0.5), (1.5, 0.5)]),
                         None)

        self.assertEqual(math2d.intersectSegment([(0, 0), (0, 1)],
                                                 [(-0.5, 0.5), (1.5, 0.5)]),
                         (0, 0.5))
        self.assertEqual(math2d.intersectSegment([(0, 0), (0, 0)],
                                                 [(3, 4), (4, 5)]),
                         None)
        self.assertEqual(math2d.intersectSegment([(3, 4), (4, 5)],
                                                 [(0, 0), (0, 0)]),
                         
                         None)

        assert_array_equal(math2d.intersectSegment([(0, 0), (1, 1)],
                                                          [(3, 0), (1, 1)]),
                                  (1, 1))
        
        assert_array_equal(math2d.intersectSegment([(0.548, -0.478),
                                                           (0.344, 0.249)],
                                                          [(0.482, -0.388),
                                                           (0.344, 0.249)]),
                                  (0.344, 0.249))
        
    def testBoundingBox(self):
        self.assertEqual(math2d.boundingBox([(-1.0, 10), (130.0, 0.0)]), 
                         ((-1, 0), (131, 10)))
        self.assertEqual(math2d.boundingBox([(-1.0, 10), (-130, 0)]), 
                         ((-130, 0), (129, 10)))


        
    def testStepAlongLine(self):

        math2d.assert_array_equal(math2d.stepAlongLine([(20.764426155331225, 15.291993588196641), 
                                                        (20.764426155331229, 15.291993588196641)],
                                                       3.5527136788e-17),
                                  [(20.764426155331225, 15.291993588196641)])


        self.assertEqual([x for x in math2d.stepAlongLine([(0, 0), (1, 0)], 1)],
                         [(0,0), (1, 0)])

        self.assertEqual([x for x in math2d.stepAlongLine([(0, 0), (1, 0)], 2)],
                         [(0,0)])

        self.assertEqual([x for x in math2d.stepAlongLine([(0, 0)], 2)],
                         [(0,0)])
                          
                         
        self.assertEqual([x for x in math2d.stepAlongLine([(0, 0), (1, 0)], 0.5)],
                         [(0, 0), (0.5, 0), (1, 0)])


        assert_array_equal([x for x in math2d.stepAlongLine([(0, 0), (1, 0)], 0.1)],
                              [(0, 0), 
                               (0.1, 0),
                               (0.2, 0),
                               (0.3, 0),
                               (0.4, 0),
                               (0.5, 0),
                               (0.6, 0),
                               (0.7, 0),
                               (0.8, 0),
                               (0.9, 0),
                               (1.0, 0)])


        assert_array_equal([x for x in math2d.stepAlongLine([(0, 0), (1, 0), (1, 1)], 0.1)],
                              [(0, 0), 
                               (0.1, 0),
                               (0.2, 0),
                               (0.3, 0),
                               (0.4, 0),
                               (0.5, 0),
                               (0.6, 0),
                               (0.7, 0),
                               (0.8, 0),
                               (0.9, 0),
                               (1, 0),
                               (1, 0.1),
                               (1, 0.2),
                               (1, 0.3),
                               (1, 0.4),
                               (1, 0.5),
                               (1, 0.6),
                               (1, 0.7),
                               (1, 0.8),
                               (1, 0.9),
                               (1, 1),
                               ])
        math2d.stepAlongLine([(22.800000, 29.400000),(24.400000, 21.800000),(33.000000, 20.200000),(42.200001, 19.000000),(50.800001, 18.400000),(53.000001, 26.400000),(62.200001, 25.600000),(71.400001, 25.000000),(76.200001, 20.000000),(81.200001, 15.000000),(88.400001, 18.400000),],
                             0.831288)

        math2d.stepAlongLine([(22.800000, 29.400000),(23.400000, 29.200000),(24.000000, 29.200000),(24.600000, 29.000000),(25.000000, 28.600000),(25.000000, 28.000000),(25.000000, 27.400000),(25.000000, 26.800000),(24.800000, 26.200000),(24.600000, 25.600000),(24.400000, 25.000000),(24.400000, 24.400000),(24.400000, 23.800000),(24.400000, 23.200000),(24.400000, 22.600000),(24.400000, 22.000000),(24.200000, 21.400000),(24.800000, 21.000000),(25.400000, 21.000000),(26.000000, 21.000000),(26.600000, 21.000000),(27.200000, 21.200000),(27.800000, 21.000000),(28.400000, 20.800000),(29.000000, 20.600000),(29.600000, 20.600000),(30.200000, 20.600000),(30.800000, 20.400000),(31.400000, 20.400000),(32.000000, 20.200000),(32.600000, 20.200000),(33.200000, 20.200000),(33.800001, 20.000000),(34.400001, 20.000000),(35.000001, 20.000000),(35.600001, 20.000000),(36.200001, 20.000000),(36.800001, 19.800000),(37.400001, 19.600000),(38.000001, 19.400000),(38.600001, 19.200000),(39.200001, 19.200000),(39.800001, 19.200000),(40.400001, 19.200000),(41.000001, 19.000000),(41.600001, 19.000000),(42.200001, 19.000000),(42.800001, 19.000000),(43.400001, 18.600000),(44.000001, 18.200000),(44.600001, 18.200000),(45.200001, 18.000000),(45.800001, 17.800000),(46.400001, 17.600000),(47.000001, 17.600000),(47.600001, 17.600000),(48.200001, 17.600000),(48.800001, 17.400000),(48.800001, 16.800000),(48.800001, 16.200000),(48.800001, 15.600000),(48.600001, 15.000000),(48.600001, 14.400000),(48.400001, 13.800000),(48.400001, 13.200000),(48.400001, 12.600000),(48.200001, 12.000000),(48.200001, 11.400000),(48.200001, 10.800000),(48.200001, 10.200000),(48.200001, 9.600000),(48.600001, 9.000000),(49.200001, 8.400000),(49.800001, 8.200000),(50.400001, 8.200000),(51.000001, 8.200000),(51.600001, 8.200000),(52.200001, 8.200000),(52.800001, 8.200000),(53.400001, 8.000000),(54.000001, 8.000000),(54.600001, 8.000000),(55.200001, 8.200000),(55.800001, 8.000000),(56.400001, 8.000000),(57.000001, 7.800000),(57.600001, 7.800000),(58.200001, 8.000000),(58.800001, 7.800000),(59.400001, 7.800000),(60.000001, 7.800000),(60.600001, 7.800000),(61.200001, 7.600000),(61.800001, 7.800000),(62.400001, 7.800000),(63.000001, 7.600000),(63.600001, 7.600000),(64.200001, 7.600000),(64.800001, 7.400000),(65.400001, 7.400000),(66.000001, 7.400000),(66.600001, 7.400000),(67.200001, 7.200000),(67.800001, 7.400000),(68.400001, 7.400000),(69.000001, 7.400000),(69.600001, 7.400000),(70.200001, 7.200000),(70.800001, 7.000000),(71.400001, 7.000000),(72.000001, 7.000000),(72.600001, 7.000000),(73.200001, 7.000000),(73.800001, 7.000000),(74.400001, 7.000000),(75.000001, 7.000000),(75.600001, 7.000000),(76.200001, 7.000000),(76.800001, 7.000000),(77.400001, 7.000000),(77.800001, 7.400000),(77.800001, 8.000000),(77.800001, 8.600000),(78.000001, 9.200000),(78.000001, 9.800000),(78.000001, 10.400000),], 0.769950)

        

            
    def testPointOnSegment(self):

        assert_array_equal(math2d.pointOnSegment([(0, 0), (math.pow(2, 0.5), 
                                                               math.pow(2, 0.5))], 
                                                     1),
                               (math.pow(2, 0.5)/2, math.pow(2, 0.5)/2))

        self.assertEqual(math2d.pointOnSegment([(0, 0), (1, 0)], 0.0),
                         (0,0))
        self.assertRaises(ValueError, math2d.pointOnSegment, [(0, 0), (1, 1), 
                                                             (3, 5)], 10)


    def testPointOnLine(self):
        assert_array_equal(math2d.pointOnLine([(-1, 0), (0, 0), 
                                                   (math.pow(2, 0.5), 
                                                    math.pow(2, 0.5))], 
                                                  2),
                               (math.pow(2, 0.5)/2, math.pow(2, 0.5)/2))

        self.assertEqual(math2d.pointOnLine([(0, 0), (1, 0)], 1),
                         (1, 0))
        self.assertEqual(math2d.pointOnLine([(0, 0), (1, 0), (1.0, 1.0)], 1),
                         (1, 0))

        math2d.assert_sorta_eq(math2d.length([(0, 0), (3, 3)]), 
                               3*math.pow(2, 0.5))        

        assert_array_equal(math2d.pointOnSegment([(0, 0), (3, 3)], 
                                                        math.pow(2, 0.5)),
                                  (1, 1))
        assert_array_equal(math2d.pointOnLine([(0, 0), (3, 3)], 
                                                     math.pow(2, 0.5)),
                                  (1, 1))

        assert_array_equal(math2d.pointOnLine([(0, 0), (3, 3)], 
                                                     2*math.pow(2, 0.5)),
                                  (2, 2))

        assert_array_equal(math2d.pointOnLine([(0, 0), (3, 3)], 
                                                     3*math.pow(2, 0.5)),
                                  (3, 3))



    def testClosestPointOnSegment(self):
        self.assertEqual(math2d.closestPointOnSegment([(0.0, 0.0), (1, 1)],
                                                      (1, 0.0)),
                         (0.5, 0.5))

        self.assertEqual(math2d.closestPointOnSegment([(0.0, 0.0), (1, 1)],
                                                      (1, 2.0)),
                         (1, 1))

        self.assertEqual(math2d.closestPointOnSegment([(1.13424,0.015043), (1.13424,0.015043)],
                                                      (3, 3)),
                         (1.13424, 0.015043))

        self.assertEqual(math2d.closestPointOnSegment([(22.437999999999999, 24.919), 
                                                       (22.437999999999999, 24.906500000000001)],
                                                      (23.324929146307721, 26.312036364557606)),
                         (22.437999999999999, 24.919))


    def testClosestPointOnSegmentLine(self):
        self.assertEqual(math2d.closestPointOnSegmentLine([(0.0, 0.0), (1, 1)],
                                                      (1, 0.0)),
                         (0.5, 0.5))

        self.assertEqual(math2d.closestPointOnSegmentLine([(0.0, 0.0), (1, 1)],
                                                          (1, 2.0)),
                         (1.5, 1.5))

        self.assertEqual(math2d.closestPointOnSegmentLine([(1.13424,0.015043), (1.13424,0.015043)],
                                                      (3, 3)),
                         (1.13424, 0.015043))

        self.assertEqual(math2d.closestPointOnSegmentLine([(22.437999999999999, 24.919), 
                                                       (22.437999999999999, 24.906500000000001)],
                                                      (23.324929146307721, 26.312036364557606)),
                         (22.437999999999999, 26.312036364557606))

    def testClosestPointOnLine(self):
        self.assertEqual(math2d.closestPointOnLine([(0.0, 0.0), (1,1)],
                                                   (1, 0.0)),
                         (0.5, 0.5))

        self.assertEqual(math2d.closestPointOnLine([(0.0, 0.0), (1,1), (2, 5)],
                                                   (1, 0.0)),
                         (0.5, 0.5))

        self.assertEqual(math2d.closestPointOnLine([(0.0, 0.0), (1,1.0), (2, 5.0)],
                                                   (5.0, 0.0)),
                         (1, 1))

        self.assertEqual(math2d.closestPointOnLine([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
                                                      (-1, 0.5)),
                         (0, 0.5))
        self.assertEqual(math2d.closestPointOnLine([(22.7713,25.4815), (22.388,25.0315), (22.388,25.0315), 
                                                    (22.4067,25.0002), (22.438,24.919), (22.438,24.9065), 
                                                    (22.463,24.969), (22.438,24.9815)],  
                                                   (23.324929146307721, 26.312036364557606)),
                         (22.7713, 25.4815))

        
                         

    def testClosestPointOnPolygon(self):
        self.assertEqual(math2d.closestPointOnPolygon([(0, 0), (1, 0), (1, 1), (0, 1)],
                                                      (-1, 0.5)),
                         (0, 0.5))

        self.assertEqual(math2d.closestPointOnPolygon([(0, 0), (1, 0), (1, 1), (0, 1)],
                                                      (1, 0.5)),
                         (1, 0.5))


    def testDistAlongSegment(self):
        self.assertEqual(math2d.distAlongSegment([(0.0, 0.0), (1.0, 1.0)],
                                                 (0.5, 0.5)),
                         math.sqrt(0.5))

        self.assertRaises(ValueError,
                          math2d.distAlongSegment,
                          [(0.0, 0.0), (1.0, 1.0)],
                          (0.5, 0.6))

    def testDistAlongLine(self):
        self.assertEqual(math2d.distAlongLine([(0.0, 0.0), (1.0, 1.0)],
                                              (0.5, 0.5)),
                         math.sqrt(0.5))

        self.assertEqual(math2d.distAlongLine([(0.0, 0.0), (1.0, 1.0), (2.0, 5.0)],
                                              (0.5, 0.5)),
                         math.sqrt(0.5))

        self.assertEqual(math2d.distAlongLine([(-2, 0), (0.0, 0.0), (1.0, 1.0), (2.0, 5.0)],
                                              (0.5, 0.5)),
                         math.sqrt(0.5) + 2)
        self.assertRaises(ValueError,
                          math2d.distAlongLine,
                          [(-2, 0), (0.0, 0.0), (1.0, 1.0), (2.0, 5.0)],
                          (100, 100))


        self.assertEqual(math2d.distAlongLine([(-2, 0), (0.0, 0.0), (1.0, 1.0), (2.0, 5.0)],
                                              (0.0, 0.0)),
                         2.0)

    def testLength(self):
        self.assertEqual(math2d.length([(-2.0, 0.0), (0,0)]),
                                       2)
        self.assertEqual(math2d.length([(0, 0),(1.0, 1.0)]),
                         math.sqrt(2))
        self.assertEqual(math2d.length([(-2.0, 0.0,), (0.0, 0.0), (1, 1)]),
                         2.0 + math.sqrt(2))
        self.assertEqual(math2d.length([(0, 0), (1, 0), (1.0, 1.0)]),2)
                         
    def testDistBetweenPointsAlongPolygon(self):
        self.assertEqual(math2d.distBetweenPointsAlongPolygon([(0, 0), (1,0), 
                                                               (1, 1), (0, 1)],
                                                              (0, 0), (1, 1)),
                         2)

        self.assertEqual(math2d.distBetweenPointsAlongPolygon([(0, 0), (1,0), 
                                                               (1, 1), (0, 1)],
                                                              (0.5, 0), 
                                                              (0.5, 1)),
                         2)

        self.assertEqual(math2d.distBetweenPointsAlongPolygon([(0, 0), (1,0), 
                                                               (1, 1), (0, 1)],
                                                              (0, 0.5), 
                                                              (0.5, 0)),
                         1)
    def testDistBetweenPointsAlongLine(self):
        self.assertEqual(math2d.distBetweenPointsAlongLine(
                [(0.0, 0.0), (1.0, 1.0), (3, 5)],
                (0.5, 0.5),
                (1, 1)),
                         math.sqrt(2)/2)

        self.assertEqual(math2d.distBetweenPointsAlongLine(
                [(0.0, 0.0), (1.0, 1.0), (3, 5)],
                (1, 1),
                (0.5, 0.5)),
                         -math.sqrt(2)/2)


        self.assertEqual(math2d.distBetweenPointsAlongLine([(0, 0), (1,0), 
                                                            (1, 1), (0, 1),
                                                            (0, 0)],
                                                           (0, 0.5), 
                                                           (0.5, 0)),
                         -3)
                                       
    
    def testMidpoint(self):
        self.assertEqual(math2d.midpoint([(0, 0), (0, 0)]),
                         (0, 0))
        self.assertEqual(math2d.midpoint([(0, 0), (1, 1)]),
                         (0.5, 0.5))

        self.assertEqual(math2d.midpoint([(0, 0), (0, 1)]),
                         (0, 0.5))

        self.assertEqual(math2d.midpoint([(0, 0), (1, 0)]),
                         (0.5, 0))
        self.assertEqual(math2d.midpoint([(11.462999999999999, 
                                          15.20607079731321), 
                                         (11.462999999999997, 
                                          28.790125459845836)]),
                         (11.462999999999999999, 21.998098128579521))



    def testMidpointLine(self):
        self.assertEqual(math2d.midpointLine([(0, 0), (1, 1)]),
                         (0.5, 0.5))

        self.assertEqual(math2d.midpointLine([(0, 0), (0, 1)]),
                         (0, 0.5))

        self.assertEqual(math2d.midpointLine([(0, 0), (1, 0)]),
                         (0.5, 0))

        self.assertEqual(math2d.midpointLine([(0, 0), (1, 0), (1.0, 1.0)]),
                         (1, 0))


    def testPerpendicular(self):
        self.assertEqual(math2d.perpendicular([(0, 0), (0, 0)]),
                         [(0, 0), (0, 0)])
        self.assertEqual(math2d.perpendicular([(0,0), (1, 1)]),
                         [(0, 1), (1, 0)])
        self.assertEqual(math2d.perpendicular([(0,0), (0, 1)]),
                         [(-0.5, 0.5), (0.5, 0.5)])
        self.assertEqual(math2d.perpendicular([(0,0), (1, 0)]),
                         [(0.5, -0.5), (0.5, 0.5)])
        self.assertEqual(math2d.perpendicular([(1, 0.5), (0, 0.5)]),
                         [(0.5, 0), (0.5, 1)])



        # with start point
        self.assertEqual(math2d.perpendicular([(0,0), (2, 2)], (0.5, 0.5)),
                         [(-0.5, 1.5), (1.5, -0.5)])
        self.assertEqual(math2d.perpendicular([(0,0), (0, 1)], (0, 0.25)),
                         [(-0.5, 0.25), (0.5, 0.25)])
        self.assertEqual(math2d.perpendicular([(0,0), (1, 0)], (0.25, 0)),
                         [(0.25, -0.5), (0.25, 0.5)])
#        self.assertEqual(math2d.perpendicular([(1, 0.5), (0, 0.5)]),
#                         [(0.5, 1), (0.5, 0)])

        # vertical
        self.assertEqual(math2d.perpendicular([(0, 0), (0, 1)]),
                         [(-0.5, 0.5), (0.5, 0.5)])
                         
        # horizontal
        self.assertEqual(math2d.perpendicular([(-0.5, 0.5), (0.5, 0.5)]),
                         [(0, 0), (0, 1)])

        math2d.assert_array_equal(math2d.perpendicular([(-0.12615290168030427, 0.19801488833746889), 
                                                        (0.94040262547026343, 0.19801488833746894)]),
                                  [(0.40712486189497959, -0.33526287523781501), 
                                (0.40712486189497959, 0.73129265191275272)])

        math2d.assert_array_equal(math2d.perpendicular([(10.905160982291914, 3.6322744099268141), (4.7442000804662703, 3.6325956465404006)]),

                         [(7.8246805313790926, 0.55179395482661953), (7.8246805313790926, 6.7127548650270086)])

        

    def testGeometricMean(self):
        self.assertEqual(math2d.geometric_mean([2, 8]), 4)

    def testStandardDeviation(self):
        self.assertEqual(math2d.stdDeviation([3, 7, 7, 19]),
                         6)
    def testIsInteriorPoint(self):
        self.assertEqual(math2d.isInteriorPoint([(0, 0), (0, 1), 
                                                 (1, 1), (1, 0)],
                                                (0.5, 0.5)),
                         True)

        self.assertEqual(math2d.isInteriorPoint([(0, 0), (0, 1), 
                                                 (1, 1), (1, 0)],
                                                (3, 3)),
                         False)

        self.assertEqual(math2d.isInteriorPoint([(0, 0), (0, 1), 
                                                 (1, 1), (1, 0)],
                                                (0, 0)),
                         True)

        self.assertEqual(math2d.isInteriorPoint([(0, 0), (0, 1), 
                                                 (1, 1), (1, 0)],
                                            (0, 0.5)),
                         True)
        self.assertEqual(math2d.isInteriorPoint([(0, 0), (0, 1), 
                                                 (1, 1), (1, 0)],
                                                (0.5, 0)),
                         True)


        self.assertEqual(math2d.isInteriorPoint([(0, 0), (1, 2), 
                                                 (2, 0)],
                                                (0.5, 0.5)),
                         True)
        self.assertEqual(math2d.isInteriorPoint([(0, 0), (1, 2), 
                                                 (2, 0)],
                                                (0.9, 1.9)),
                         False)
        self.assertEqual(math2d.isInteriorPoint([(0, 0), (1, 2), 
                                                 (2, 0)],
                                                (2, 0)),
                         True)

        self.assertEqual(math2d.isInteriorPoint([(0, 0), (1, 2), 
                                                 (2, 0)],
                                                (1, 2)),
                         True)

        self.assertEqual(math2d.isInteriorPoint([(0, 0), (1, 2), 
                                                 (2, 0)],
                                                (10, 20)),
                         False)
                     
    def testPolygonToLine(self):
        self.assertEqual(math2d.polygonToLine([(0, 0), (1, 0), (1, 1), (0, 1)]),
                         [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])


        

    def testPolygonToGrid(self):
        self.assertEqual(math2d.polygonToOccupancyGrid(
                [(0, 0), (0, 1), (1, 1), (1, 0)],
                resolution=4),
                         [(0.25, 0.25), (0.25, 0.75), 
                          (0.75, 0.25), (0.75, 0.75)])

        self.assertEqual(math2d.polygonToOccupancyGrid(
                [(0, 0), (1, 2),  (2, 0)], 
                resolution=4),
                         [(0.5, 0.5), (1.5, 0.5)])

    

    def testEigenvectorsSquare(self):
        polygon = [(0, 0), (0, 1), (1, 1), (1, 0)]
        u, v = math2d.eigenvectors(polygon)
        

        major = v[:, 0]
        minor = v[:, 1]


        self.assertEqual(na.shape(v), (2, 2))
        assert_array_equal(major,
                                  [ 0.70710678,  0.70710678])
#                                  [1., 0.])
        assert_array_equal(minor,
                                  [ -0.70710678,  0.70710678])
#                                  [0., 1.])

        eMajor, eMinor = math2d.eigenAxes(polygon)
        print "eMajor, eMinor", eMajor, eMinor
        #assert_array_equal(eMajor, [(0, 0), (1, 1)])
        #assert_array_equal(eMinor, [(0, 1), (1, 0)])

        assert_array_equal(eMajor,
                           [na.array([ 0.11109127,  0.11109127]),
                            na.array([ 0.88890873,  0.88890873])])
        assert_array_equal(eMinor,
                           [na.array([ 0.53535534,  0.46464466]),
                            na.array([ 0.46464466,  0.53535534])])
        


    def testEigenvectorsTranslatedSquare(self):

        u, v = math2d.eigenvectors(
            [(1, 1), (1, 2), (2, 2), (2, 1)])
        

        major = v[:, 0]
        minor = v[:, 1]


        self.assertEqual(na.shape(v), (2, 2))
        assert_array_equal(major,
                                  [ 0.70710678,  0.70710678])
        assert_array_equal(minor,
                                  [ -0.70710678,  0.70710678])




    def testArrayEqual(self):
        self.assertEqual(math2d.array_equal(na.array([1, 2, 3]),
                                            na.array([1, 2, 3])),
                         True)

        self.assertEqual(math2d.array_equal(na.array([1, 2, 3.1]),
                                            na.array([1, 2, 3])),
                         False)

        self.assertEqual(math2d.array_equal(na.array([-1, -2, -3]),
                                            na.array([-1, -2, -3])),
                         True)

        self.assertEqual(math2d.array_equal(na.array([-1, -2, -3.1]),
                                            na.array([-1, -2, -3])),
                         False)

        self.assertEqual(math2d.array_equal(na.array([-1, -2, -3]),
                                            na.array([1, 2, 3])),
                         False)



    def testTrimPolygon(self):
        self.assertEqual(math2d.trimPolygon([(0, 0), (1, 1), (2, 0)],
                                     (0.5, 0.5),
                                     (1.5, 0.5)),
                         [(0.5, 0.5), (1, 1), (1.5, 0.5)])        

        self.assertEqual(math2d.trimPolygon([(0, 0), (1, 1), (2, 0)],
                                            (1.5, 0.5),
                                            (0.5, 0.5)),
                         [(1.5, 0.5), (2, 0), (0, 0), (0.5, 0.5)])
    def testTrimLine(self):
        self.assertEqual(math2d.trimLine([(0, 0), (1, 1), (2, 1)],
                                     (0.5, 0.5),
                                     (1.5, 1)),
                         [(0.5, 0.5), (1, 1), (1.5, 1)])

        self.assertEqual(math2d.trimLine([(0, 0), (1, 1)],
                                     (0.5, 0.5),
                                     (0.6, 0.6)),
                         [(0.5, 0.5), (0.6, 0.6)])

        
        trimmed = math2d.trimLine([(0.408545,-1.48909), (0.225273,-1.19891), (0.622364,-0.985091), (0.828545,0.366545), (0.584182,1.44327), (-0.0801818,1.16836), (-0.431455,1.45091)],
                              (-0.15845056851323014, 1.2313189355432503), 
                              (0.26737251469300988, -1.2655670876578717))
        self.assertEqual(len(trimmed),7)
                         

    def testFitLine(self):
        m, b = math2d.fitLine([(0, 0), (1, 1)])
        self.assertEqual(m, 1)
        self.assertEqual(b, 0)

        # horizontal line
        m, b = math2d.fitLine([(-0.5, 0.5), (1.5, 0.5)])
        self.assertEqual(m, 0)
        self.assertEqual(b, 0.5)

        # vertical line 
        m, b = math2d.fitLine([(-0.5, 0.5), (-0.5, 1)])
        self.assertEqual(na.isnan(m), True)
        self.assertEqual(na.isnan(b), True)

    def testIntersectSegmentAnalytic(self):
        self.assertEqual(math2d.intersectSegmentAnalytic([(1, 0), (0, 0)], 0, 0.5),
                         None)

        self.assertEqual(math2d.intersectSegmentAnalytic([(0, 0), (1, 0)], 0, 0.5),
                         None)

        self.assertEqual(math2d.intersectSegmentAnalytic([(0, 0), (0, 1)], 0, 0.5),
                         (0,0.5))


    def testIntersectPolygonAnalytic(self):
        self.assertEqual(math2d.intersectPolygonAnalytic([(0, 0), (1, 0), (1, 1), (0, 1)],
                                                         1, 0),
                         [(0.0, 0.0), (1.0, 1.0)])

        self.assertEqual(set(math2d.intersectPolygonAnalytic([(0, 0), (1, 0), (1, 1), (0, 1)],
                                                         0, 0.5)),
                         set([(0, 0.5), (1, 0.5)]))


    def testConcave(self):
        self.assertEqual(math2d.isConcave([(0, 0), (1, 0), (1, 1), (0, 1)]), False)
        self.assertEqual(math2d.isConcave([(0, 0), (1, 0), (1, 1), (0.5, 0.5), (0, 1)]), True)
        self.assertEqual(math2d.isConcave([(0.501992,-0.909861), 
                                           (-0.886853,-0.0062749), 
                                           (-0.39741,0.817829), 
                                           (0.715339,0.964243), 
                                           (0.953785,-0.023008), 
                                           (0.953785,-0.023008)]), 
                         False)

        
        
    def testIsParallel(self):
        self.assertEqual(math2d.isParallel([(0, 0), (1, 1)], [(0, 0), (1, 1)]), True)
        self.assertEqual(math2d.isParallel([(0, 0), (1, 1)], [(0, 1), (1, 2)]), True)

        self.assertEqual(math2d.isParallel([(0, 0), (1, 1)], [(0, 0), (1, -1)]), False)

        self.assertEqual(math2d.isParallel([(0, 0), (0, 1)], [(1, 0), (1, 1)]), True)

        self.assertEqual(math2d.isParallel([(0, 0), (0, 1)], [(1, 0), (1.9, 1.9)]), False)
    def testIsVertical(self):
        self.assertEqual(math2d.isVertical([(0, 0), (1, 1)]), False)
        self.assertEqual(math2d.isVertical([(0, 0), (0, 1)]), True)

        self.assertEqual(math2d.isVertical([(0, 0), (0, 0)]), False)
        self.assertEqual(math2d.isVertical([(78.954088821985337, 9.200000137090683), 
                                            (78.954088821985337, 9.2000001385807995)]),
                         False) #it's degenerate, not vertical.
        
    def testBetween(self):
        self.assertEqual(math2d.between(1.0, 0.0, 0.5), True)
        self.assertEqual(math2d.between(0.0, 1.0, 0.5), True)

    def testClip(self):

        # line completely inside the polygon
        self.assertEqual(math2d.clip([(0.1, 0.5), (0.2, 0.5)], 
                                     [(0, 0), (1, 0), (1, 1), (0, 1)]),
                         [(0.1, 0.5), (0.2, 0.5)])


        # line with one intersect
        self.assertEqual(math2d.clip([(-0.1, 0.5), (0.2, 0.5)], 
                                     [(0, 0), (1, 0), (1, 1), (0, 1)]),
                         [(0, 0.5), (0.2, 0.5)])

                         



        # line with two intersect points
        self.assertEqual(math2d.clip([(-1, -1), (1, 1)], 
                                     [(0, 0), (1, 0), (1, 1), (0, 1)]),
                         [(0, 0), (1, 1)])



        self.assertEqual(math2d.clip([(-1, -1), (2, 2)], 
                                     [(0, 0), (1, 0), (1, 1), (0, 1)]),
                         [(0, 0), (1, 1)])

                         

        # line with no points
        self.assertEqual(math2d.clip([(-1, -1), (-0.1, -0.1)], 
                                     [(0, 0), (1, 0), (1, 1), (0, 1)]),
                         [])


        assert_array_equal(math2d.clip([(0.1, 0.5), (2, 0.5)], 
                                              [(0, 0), (1, 0), (1, 1), (0, 1)]),
                                  [(0.1, 0.5), (1, 0.5)])
        


        # from map/robot corpus. It's sticking the first potin on the end for some reason.
        figure = [(22.8,29.4), (23,29.2), (23.2,29.2), (23.4,29.2), (23.6,29.2), (23.8,29.2), (24,29.2), (24.2,29.2), (24.4,29), (24.6,29), (24.8,29), (25,28.8), (25,28.6), (25,28.4), (25,28.2), (25,28), (25,27.8), (25,27.6), (25,27.4), (25,27.2), (25,27), (25,26.8), (24.8,26.6), (24.8,26.4), (24.8,26.2), (24.8,26), (24.6,25.8), (24.6,25.6), (24.4,25.4), (24.4,25.2), (24.4,25), (24.4,24.8), (24.4,24.6), (24.4,24.4), (24.4,24.2), (24.4,24), (24.4,23.8), (24.4,23.6), (24.4,23.4), (24.4,23.2), (24.4,23), (24.4,22.8), (24.4,22.6), (24.4,22.4), (24.4,22.2), (24.4,22), (24.4,21.8), (24.4,21.6), (24.2,21.4), (24.4,21.2), (24.6,21), (24.8,21), (25,21), (25.2,21), (25.4,21), (25.6,21), (25.8,21), (26,21), (26.2,21), (26.4,21), (26.6,21), (26.8,21), (27,21), (27.2,21.2), (27.4,21), (27.6,21), (27.8,21), (28,20.8), (28.2,20.8), (28.4,20.8), (28.6,20.8), (28.8,20.8), (29,20.6), (29.2,20.6), (29.4,20.6), (29.6,20.6), (29.8,20.6), (30,20.6), (30.2,20.6), (30.4,20.4), (30.6,20.4), (30.8,20.4), (31,20.4), (31.2,20.4), (31.4,20.4), (31.6,20.4), (31.8,20.2), (32,20.2), (32.2,20.2), (32.4,20.2), (32.6,20.2), (32.8,20.2), (33,20.2), (33.2,20.2), (33.4,20), (33.6,20), (33.8,20), (34,20), (34.2,20), (34.4,20), (34.6,20), (34.8,20), (35,20), (35.2,20), (35.4,20), (35.6,20), (35.8,20), (36,20), (36.2,20), (36.4,19.8), (36.6,19.8)]
        ground = [(25.2,20.2), (25.2,22.2), (27.2,22.2), (27.2,20.2)]
        math2d.assert_array_equal(math2d.clip(figure, ground),
                                  [(25.2, 21), 
                                   (25.4,21), (25.6,21), (25.8,21), (26,21), (26.2,21), 
                                   (26.4,21), (26.6,21), (26.8,21), (27,21), (27.2, 21.2)])

        
        


    def testConvexHull(self):
        self.assertEqual(set(math2d.convexHull([(0, 0), (1, 0), (1, 1), (0, 1)])),
                         set([(0, 0), (1, 0), (1, 1), (0, 1)]))
        
        self.assertEqual(set(math2d.convexHull([(0, 0), (1, 0), (1, 1), (0, 1), 
                                            (0.5, 0.5)])),
                         set([(0, 0), (1, 0), (1, 1), (0, 1)]))

    def destFitLineToPath(self):
        self.assertEqual(math2d.fitLineToPath([(0, 0),(1,1)]), 
                         [(0, 0), (1,1)])

        self.assertEqual(math2d.fitLineToPath([(0, 0),(1, 1), (2,0)]), 
                         [(0, 0), (2,0)])
    def destAreaBetweenPaths(self):
        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (1, 1)],
                                                 [(0, 1), (1, 2)]),
                         1)

        self.assertEqual(math2d.areaBetweenPaths([(1, 1), (0, 0)],
                                                 [(0, 1), (1, 2)]),
                         1)

        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (1, 0)],
                                                 [(0, 1), (1, 1)]),
                         1)

        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (0, 1)],
                                                 [(1, 0), (1, 1)]),
                         1)

        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (0, 2)],
                                                 [(1, 0), (1, 2)]),
                         2)


        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (0, 2)],
                                                 [(1, 0), (1, 1)]),
                         1.5)

        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (0, 0.5), (0, 2)],
                                                 [(1, 0), (1, 1)]),
                         1.5)

        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (2, 0)],
                                                 [(0, 1), (1, 2), (2, 1)]),
                         3)



        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (1, 1)],
                                                 [(0, 1), (1, 0)]),
                         0.5)


        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (1, 1), 
                                                  (2, 1), (3, 0)],
                                                 [(0, 0), (1, 0), (3, 2)]),
                         2)

        self.assertEqual(math2d.areaBetweenPaths([(0.548, -0.478),
                                                  (0.344, 0.249)],
                                                 [(-0.12, 0.431),
                                                  (0.482, -0.388)]),
                         0.15003700000000003)


        self.assertEqual(math2d.areaBetweenPaths([(0, 0), (1, 1)],
                                                 [(0, 1), (1, 0)]),
                         0.5)


        math2d.assert_sorta_eq(math2d.areaBetweenPaths([(0.960729,0.452733), (-0.952227,0.112652)],
                                                       [(-0.36724341486030215, 0.37898874142662475), 
                                                        (-0.30618594145588185, -0.57905711030055362)]),
                               0.347)
        
        self.assertEqual(math2d.areaBetweenPaths(
                [(17.7979,25.1594), (17.7979,25.1594), (18.0607,24.7454), (18.2385,24.6277), (18.4605,24.5688), (18.6179,24.6804), (18.7488,24.6533), (18.8918,24.6321), (18.9481,24.5059), (18.6634,24.4754), (18.4657,24.5036), (18.2167,24.5135), (18.3507,24.5276), (18.274,24.5344), (18.3954,24.6164), (18.2399,24.6452), (18.0078,24.6541), (17.777,24.699), (17.8132,24.6663), (17.9627,24.6612), (18.147,24.6516), (18.1006,24.6776), (17.9739,24.6887), (17.8259,24.6801), (17.6169,24.6679), (17.4483,24.6506), (17.1643,24.6509), (16.7702,24.6584), (16.4675,24.6761), (16.2595,24.6816), (16.071,24.7145), (15.9156,24.7327), (15.7654,24.7179), (15.5617,24.6459), (15.4049,24.5653), (15.2667,24.4818), (15.1349,24.4362), (15.0334,24.5041), (14.9019,24.4756), (14.8005,24.3957), (14.6863,24.326), (14.5478,24.3342), (14.4153,24.3792), (14.2914,24.3505), (14.1465,24.2292), (14.0438,24.1284), (13.9671,24.0121), (13.8518,23.7869), (13.7757,23.5944), (13.6868,23.4123), (13.6155,23.2368), (13.5468,23.0459), (13.5137,23.0392), (13.4338,23.0258), (13.3254,22.7697), (13.2825,22.589), (13.2778,22.4315), (13.2537,22.2932), (13.2665,22.1225), (13.2569,21.9739), (13.3131,21.7995), (13.3296,21.6732), (13.3398,21.5477), (13.374,21.3154), (13.4209,21.1069), (13.4685,20.9367), (13.5472,20.6777), (13.6333,20.4609), (13.7233,20.2949), (13.8267,20.1465), (13.9135,20.0362), (13.9687,19.9001), (14.0203,19.7834), (14.1518,19.5716), (14.2913,19.3599), (14.4093,19.2187), (14.5071,19.1058), (14.6291,18.9792), (14.7413,18.862), (14.9009,18.7128), (15.0822,18.6004), (15.2544,18.5047), (15.3973,18.4463), (15.5383,18.347), (15.6591,18.2415), (15.7784,18.1385), (15.9437,18.0191), (16.1278,17.878), (16.2994,17.7663), (16.4397,17.6854), (16.5686,17.6302), (16.7141,17.4872), (16.8386,17.38), (16.955,17.2572), (17.1534,17.158), (17.3822,16.927), (17.546,16.736), (17.6854,16.5745), (17.8055,16.5399), (17.913,16.4114), (18.0589,16.2261), (18.1631,16.0795), (18.2999,16.0191), (18.425,15.9442)],
                [(12.879296102427876, 15.219153964540009), 
                 (23.260070104187772, 15.315047331736194)]),


                         100)
                              
                                                  
    def testAverageDistance(self):
        self.assertEqual(math2d.averageDistance([(0, 0), (1, 0)],
                                                [(0, 1), (1, 1)]),
                         1)
        math2d.assert_sorta_eq(math2d.averageDistance([(0, 0), (1, 1)],
                                                      [(0, 1), (1, 2)]),
                               0.7608325)
    def testLineEquation(self):
        self.assertEqual(math2d.slope([(3, 0), (1, 1)]), -0.5)
        self.assertEqual(math2d.lineEquation([(3, 0), (1, 1)]),
                         (-0.5, 1.5))
        
    def testPowerSet(self):
        self.assertEqual([x for x in math2d.powerset([1,2])],
                         [set([]), set([1]), set([1, 2]), set([2])])

        self.assertEqual([x for x in math2d.powerset([1,2,3])],
                         [set([]), set([1]), set([1, 2]), set([2]), 
                          set([2, 3]), set([1, 2, 3]), set([1, 3]), set([3])])
                         
    def testCutPolygon(self):
        self.assertEqual(math2d.cutPolygon([(0, 0), (1, 0), (1, 1), (0, 1)],
                                           [(0.5, 0), (0.5, 1)]),
                         ([(0.5, 1.0), (0, 1), (0, 0), (0.5, 0.0)], [(0.5, 0.0), (1, 0), (1, 1), (0.5, 1.0)]))


        assert_array_equal(math2d.cutPolygon([(0, 0), (1, 0), (1, 1), (0, 1)],
                                             [(0.4, 0), (0.3, 1)]),
                           ([(0.3, 1.0), (0, 1), (0, 0), (0.4, 0.0)], [(0.4, 0.0), (1, 0), (1, 1), (0.3, 1.0)]))

        

    def testXHalf(self):
        assert_array_equal(math2d.xHalf([(0, 0), (1, 0), (1, 1), (0, 1)],
                                        (1, 0)),
                           [(0.5, 0.0), (1, 0), (1, 1), (0.5, 1.0)])
        #[(1, 0), (1, 1), (0.5, 1.0), (0.5, 0.0)])


        assert_array_equal(math2d.xHalf([(0, 0), (1, 0), (1, 1), (0, 1)],
                                        (-1, 0)),
                           [(0.5, 1.0), (0, 1), (0, 0), (0.5, 0.0)])

        assert_array_equal(math2d.xHalf([(371, 215), (798, 256), 
                                         (794, 712), (312, 710)],
                                        (1,0)),
                           [(565.1448577438282, 233.64154371779148), (798, 256), (794, 712), (565.1448577438282, 711.05039360059675)])
                           



    def testPathToPolygon(self):
        assert_array_equal(math2d.pathToPolygon([(0, 0), (1, 0), 
                                                 (1, 1), (0, 1)]),
                           [(0, 0), (1, 0), (1, 1), (0, 1), (0.29999999999999999, 1.3), (1.3, 1.3), (1.3, 0.29999999999999999), (0.29999999999999999, 0.29999999999999999)])

    def testClipPoint(self):
        assert_array_equal(math2d.clipPoint([(0, 0),(1, 0)], 
                                            (0.1, 0), (0.3, 0)),
                           [(0.1, 0), (0.3, 0)])


        assert_array_equal(math2d.clipPoint([(0, 0),(1, 0), (1, 1), (3, 1)], 
                                            (0.1, 0), (0.3, 0)),
                           [(0.1, 0), (0.3, 0)])

        assert_array_equal(math2d.clipPoint([(0, 0),(1, 0), (1, 1), (3, 1)], 
                                            (0.1, 0), (3, 1)),
                           [(0.1, 0), (0, 0), (1, 0), (1, 0), (1, 1), (3, 1)])


        assert_array_equal(math2d.clipPoint([(0, 0),(1, 0), (1, 1), (3, 1)], 
                                            (0, 0), (3, 1)),
                           [(0, 0), (1, 0), (1, 0), (1, 1), (3, 1)])

                           
        assert_array_equal(math2d.clipPoint([(0, 0), (1, 0)], 
                                            (0, 0), (0.6, 0.0)),
                           [(0, 0), (0.6, 0)])

    def testSlideWindowAlongPath(self):
        result = list(math2d.slideWindowAlongPath([(0, 0), (1, 0)], 
                                                    0.1,
                                                    fractionSize=0.6))
        for r, e in zip(result,
                        [[(0, 0), (0.6, 0.0)], [(0.1, 0.0), (0.7, 0.0)], 
                         [(0.2, 0.0), (0.8, 0.0)], [(0.3, 0.0), (0.9, 0.0)], 
                         [(0.4, 0.0), (1, 0)]]):
            try:
                assert_array_equal(r, e)
            except:
                print result
                raise
                        
                        
        
        
        result = list(math2d.slideWindowAlongPath([(0, 0), (1, 0), 
                                                   (1, 1)], 
                                                  0.5,
                                                  fractionSize=0.6))
        for r, e in zip(result, 
                        [[(0, 0), (1, 0), (1.0, 0.2)], 
                         [(0.5, 0.0), (0, 0), (1, 0), (1.0, 0.7)]]):
            try:
                assert_array_equal(r, e)
            except:
                print result
                raise


            
        
    def testIsDegenerate(self):
        val = math2d.isDegenerate([(0,0), (0,0)])
        print "got", val
        print "cls", val.__class__
        self.assertEqual(math2d.isDegenerate([(0,0), (0,0)]), True)
        self.assertEqual(math2d.isDegenerate([(0,0), (0,1)]), False)

        self.assertEqual(math2d.isDegenerate([(78.954088821985337, 9.200000137090683), 
                                              (78.954088821985337, 9.2000001385807995)]),
                         True)
    def testBoxToPolygon(self):
        self.assertEqual(math2d.boxToPolygon((0,0),(1,1)),
                         [(0,0),(1,0),(1,1),(0,1)])

        self.assertEqual(math2d.boxToPolygon((0,0),(2,3)),
                         [(0,0),(2,0),(2,3),(0,3)])


    def testSmallestWindow(self):
        self.assertEqual(math2d.smallestWindow([0,1,1,0,0,0],3),
                         (3,6))

        self.assertEqual(math2d.smallestWindow([0,0,0,0,0,0],3),
                         (0,3))

        self.assertEqual(math2d.smallestWindow([1,0,0,0,0,0],3),
                         (1,4))

        self.assertEqual(math2d.smallestWindow([1,0,0,0,0,0],4),
                         (1,5))
    def testRotate(self):
        assert_array_equal(math2d.rotate([(0,0), (1,1)], math.pi/2),
                           [(0,0), (-1, 1)])
        assert_array_equal(math2d.rotate([(0,0), (1,1)], math.pi/2, (1,1)),
                           [(2,0), (1, 1)])





    

    def testArgMax(self):
        self.assertEqual(math2d.argMax([0,2,10,0]), (2, 10))

    def testArgMin(self):
        self.assertEqual(math2d.argMin([0,2,10,0]), (0, 0))
        
    def testLineEquationToPoints(self):
        def test(self, m, b):
            segment = math2d.lineEquationToPoints(m, b)
            self.assertEqual(math2d.lineEquation(segment), (m, b))

        test(self, 0, 1)
        test(self, 1, 0)
        test(self, 2, 10)

    def testAngleBetweenSegments(self):
        math2d.assert_sorta_eq(math2d.angleBetweenSegments([(0, 0), (0, 0)],
                                                          [(0, 0), (1, 0)]),
                               0)
        math2d.assert_sorta_eq(math2d.angleBetweenSegments([(0, 0), (1, 0)],
                                                           [(0, 0), (1, 1)]),
                               math.pi / 4)

        math2d.assert_sorta_eq(math2d.angleBetweenSegments([(0, 0), (1, 0)],
                                                           [(0, 0), (-1, 1)]),
                               3* math.pi / 4)

        math2d.assert_sorta_eq(math2d.angleBetweenSegments([(1, 1), (2, 1)],
                                                           [(1, 1), (2, 2)]),
                               math.pi / 4)
    def testDistNotTuple(self):
        self.assertEqual(math2d.dist([0, 0], [1, 1]),
                         math.pow(2, 0.5))
    def testSegmentEqual(self):
        self.assertEqual(math2d.segmentEqual([(0, 0), (1, 1)],
                                             [(0, 0), (1, 1)]),
                         True)

        self.assertEqual(math2d.segmentEqual([(0, 0), (1, 1)],
                                             [(0, 0), (1, 10)]),
                         False)

        self.assertEqual(math2d.segmentEqual([(0, 0), (1, 1)],
                                             [(0, 0), (10, 1)]),
                         False)

        self.assertEqual(math2d.segmentEqual([(0, 0), (1, 1)],
                                             [(0, 3), (1, 1)]),
                         False)

        self.assertEqual(math2d.segmentEqual([(0, 0), (1, 1)],
                                             [(3, 0), (1, 1)]),
                         False)


    def testSquareDistances(self):
        result = math2d.squareDistances([(0,0), (1, 1)],
                                        [(1, 0), (2, 2)])
        self.assertEqual(result.__class__, na.ndarray)

        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 2)
        self.assertEqual(len(result), 2)


    def testSubSample(self):
        math2d.assert_array_equal(math2d.subSample([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                                                    3),
                                   [(0, 0), (2, 2), (4, 4)])

        
        
    def testRemoveDuplicatePoints(self):
        self.assertEqual(math2d.removeDuplicates([(0, 0), (0, 0), (1, 1), (1, 1), 
                                                  (2, 2)]),
                         [(0, 0), (1, 1), (2, 2)])
                         
                         
        

    def testCartesianToPolar(self):
        self.assertEqual(math2d.cartesianToPolar((0, 0)),
                         (0, 0))

        self.assertEqual(math2d.cartesianToPolar((1, 1)),
                         (math.sqrt(2), math.pi/4))

    def testHeading(self):
        self.assertEqual(math.degrees(math2d.heading([(0, 0), (-1, -1)])),
                         math.degrees(5*math.pi/4))
        # m = 1
        # theta = 45

        self.assertEqual(math2d.heading([(0, 0), (1, 1)]),
                         math.pi/4)

        self.assertEqual(math2d.heading([(1, 1), (0, 0)]),
                         5*math.pi/4)

        self.assertEqual(math2d.heading([(2, 0), (1, -1)]),
                         5*math.pi/4)


        self.assertEqual(math.degrees(math2d.heading([(1, 1), (2, 0)])),
                         math.degrees(-math.pi/4))


        self.assertEqual(math.degrees(math2d.heading([(-2, 0), (-1, 1)])),
                         math.degrees(math.pi/4))

        self.assertEqual(math.degrees(math2d.heading([(-1, -1), (-2, 0)])),
                         math.degrees(3*math.pi/4))

    def testDeltaHeading(self):

        self.assertEqual(math2d.deltaHeading([(0, 0), (1, 0)],
                                             [(1, 0), (2, 0)]),
                         0)


        self.assertEqual(math2d.deltaHeading([(0, 0), (1, 1)],
                                             [(1, 1), (0, 0)]),
                         -math.pi)


        self.assertEqual(math2d.deltaHeading([(0, 0), (-1, -1)],
                                             [(-1, -1), (0, 0)]),
                         -math.pi)

        self.assertEqual(math2d.deltaHeading([(0, 0), (-1, -1)],
                                             [(-1, -1), (-2, 0)]),
                         -math.pi/2)


        self.assertEqual(math2d.deltaHeading([(0, 0), (1, -1)],
                                             [(1, -1), (0, -2)]),
                         -math.pi/2)


        self.assertEqual(math2d.deltaHeading([(0, 0), (1, 1)],
                                             [(1, 1), (2, 2)]),
                         0)

        self.assertEqual(math2d.deltaHeading([(0, 0), (1, 1)],
                                             [(1, 1), (0, 2)]),
                         math.pi/2)

        self.assertEqual(math2d.deltaHeading([(0, 0), (1, 1)],
                                             [(1, 1), (2, 0)]),
                         -math.pi/2)


        self.assertEqual(math2d.deltaHeading([(0, 0), (1, 1)],
                                             [(1, 1), (1, 1)]),
                         0)


        self.assertEqual(math2d.deltaHeading([(0, 0), (0, 1)],
                                             [(0, 1), (-1, 1)]),
                         math.pi/2)

        self.assertEqual(math2d.deltaHeading([(0, 0), (0, 1)],
                                             [(0, 1), (1, 1)]),
                         -math.pi/2)

        self.assertEqual(math2d.deltaHeading([(0, 0), (0, 1)],
                                             [(0, 1), (1, 2)]),
                         -math.pi/4)
        
        self.assertEqual(math2d.deltaHeading([(1, 1), (2, 0)],
                                             [(2, 0), (1, -1)]),
                         -math.pi/2)

        self.assertEqual(math2d.deltaHeading([(1, 1), (2, 0)],
                                             [(2, 0), (3, 1)]),
                         math.pi/2)


        self.assertEqual(math2d.deltaHeading([(1, 1), (2, 0)],
                                             [(2, 0), (1, 1)]),
                         -math.pi)

        self.assertEqual(math2d.deltaHeading([(1, 1), (2, 0)],
                                             [(2, 0), (3, -1)]),
                         0)
        


    def testDirection(self):
        math2d.assert_sorta_eq(math2d.direction((0, 0), (1, 1)),
                               math.pi / 4)
        
        
        math2d.assert_sorta_eq(math2d.direction((1, 1), (2, 2)),
                               math.pi / 4)
        
        
        math2d.assert_sorta_eq(math2d.direction((1, 1), (0, 0)),
                               -3*math.pi / 4)
    def testAngle(self):
        math2d.assert_sorta_eq(math2d.angle((1, 1)), math.pi/4)
        math2d.assert_sorta_eq(math2d.angle((-1, -1)), -3*math.pi/4)
        
    def testInterpolate(self):
        
        assert_array_equal(math2d.interpolate(0, (0, 0, 45), 1, (1, 1, 45), 0.5),
                                  (0.5, 0.5, 45))
        assert_array_equal(math2d.interpolate(0, (0, 0, 45), 1, (1, 1, 45), 0),
                                  (0, 0, 45))
        
        assert_array_equal(math2d.interpolate(0, (0, 0, 45), 1, (1, 1, 45), 1),
                                  (1, 1, 45))
        
        
    def testComputeBoundaryLine(self):
        assert_array_equal(math2d.computeBoundaryLine([(0.0, 0),
                                                       (1, 0),
                                                       (1, 1),
                                                       (0, 1)],
                                                      [(2, 0), (3,1)]),
                           [(1.0, 0.0), (1, 0), (1.0, 1.0)])

