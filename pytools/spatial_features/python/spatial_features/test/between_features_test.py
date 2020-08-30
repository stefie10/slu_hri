from spatial_features_cxx import sfe_f_polygon_l_polygon_l_polygon, \
    sfe_f_polygon_l_polygon_l_polygon_names
from scipy import transpose as tp
import unittest

class TestCase(unittest.TestCase):
    def test_between(self):

        p0 = [(2, 0), (3, 0), (3, 1), (2, 1)]
        
        p1 = [(0, 0), (1, 0), (1, 1), (0, 1)]
        p2 = [(4, 0), (5, 0), (5, 1), (4, 1)]


        features = sfe_f_polygon_l_polygon_l_polygon(tp(p0), tp(p1), tp(p2))
        fmap = dict(zip(sfe_f_polygon_l_polygon_l_polygon_names(), features))
        self.assertEqual(len(fmap), len(features))
        self.assertEqual(fmap['F_distFigureCentroidAxes'], 0);


        features = sfe_f_polygon_l_polygon_l_polygon(tp(p1), tp(p0), tp(p2))
        fmap = dict(zip(sfe_f_polygon_l_polygon_l_polygon_names(), features))
        self.assertEqual(len(fmap), len(features))
        self.assertEqual(fmap['F_distFigureCentroidAxes'], 3);        


        features = sfe_f_polygon_l_polygon_l_polygon(tp(p2), tp(p0), tp(p1))
        fmap = dict(zip(sfe_f_polygon_l_polygon_l_polygon_names(), features))
        self.assertEqual(len(fmap), len(features))
        self.assertEqual(fmap['F_distFigureCentroidAxes'], 3);        
        

        



    
