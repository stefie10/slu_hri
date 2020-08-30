from spatial_features_cxx import math3d_intersect_line_plane
import unittest
from numpy import array
from numpy import transpose as tp
from features.feature_utils import compute_fdict
import pylab as mpl
from assert_utils import assert_array_equal as aeq
        
class TestCase(unittest.TestCase):
    def testIntersectLinePlane(self):
        line = [(0, 0, 0), (1, 1, 1)]
        plane = [(0, 0, 0), (1, 1, 0), (3, 4, 0)]
        intersect_point = math3d_intersect_line_plane(tp(line), tp(plane))
        print "point", intersect_point
        aeq(intersect_point, (0, 0, 0))
        

        line = [(1, 1, 1), (1, 1, 0.5)]
        plane = [(0, 0, 0), (1, 1, 0), (3, 4, 0)]
        intersect_point = math3d_intersect_line_plane(tp(line), tp(plane))
        print "point", intersect_point
        aeq(intersect_point, (1, 1, 0))

        

        line = [(-1, -1, -1), (-2, -2, -2)]
        plane = [(0, 0, 0), (1, 1, 0), (3, 4, 0)]
        intersect_point = math3d_intersect_line_plane(tp(line), tp(plane))
        print "point", intersect_point
        aeq(intersect_point, (0, 0, 0))


        line = [(-1, -1, -1), (-2, -2, -2)]
        plane = [(0, 0, 0), (1, 1, 1), (4, 4, 4)]
        intersect_point = math3d_intersect_line_plane(tp(line), tp(plane))
        print "point", intersect_point
        aeq(intersect_point, [])




