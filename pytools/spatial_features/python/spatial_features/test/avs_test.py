from spatial_features_cxx import spatial_features_names_avs_polygon_polygon, \
    spatial_features_avs_polygon_polygon
import unittest
import numpy as na
from numpy import transpose as tp
from esdcs.groundings import Prism
from numpy import array
from features.feature_utils import compute_fdict
import pylab as mpl
from scipy import allclose

class TestCase(unittest.TestCase):

    def destPolygons(self):
        fvec = spatial_features_avs_polygon_polygon(tp([(0, 0), (1, 0),
                                                           (1, 1), (0, 1)]),
                                                       tp([(2, 0), (3, 0),
                                                           (3, 1), (2, 1)]),
                                                       0)


        self.assertFalse(any(na.isnan(x) for x in fvec))



        fvec = spatial_features_avs_polygon_polygon(tp([(0, 0), (1, 0),
                                                           (1, 1), (0, 1)]),
                                                       tp([(0, 0), (1, 0),
                                                           (1, 1), (0, 1)]),
                                                       0)
        self.assertFalse(any(na.isnan(x) for x in fvec))

    def destSameOrientedPolygons(self):
        polygon = [[ 21.72099827,  40.789814  ],
                   [ 21.22099828,  41.65583942],
                   [ 22.26022877,  42.25583939],
                   [ 22.76022875,  41.38981397],]

        fvec = spatial_features_avs_polygon_polygon(tp(polygon), tp(polygon),
                                                       0)
        names = list(sfe_f_polygon_l_polygon_names())

        print names, fvec
        self.assertFalse(any(na.isnan(x) for x in fvec))


    def destFunkyTheta(self):
        p1_xy = [[10, 10, 11, 11], [50, 51, 51, 50]]
        p2_xy = [[20, 20, 21, 21], [30, 32, 32, 30]]

        fvec = spatial_features_avs_polygon_polygon(p1_xy, p2_xy, 0)
                                                       
        print fvec

    def destFromCorpus(self):
        f_prism =  Prism(array([[  8.20976285,   7.35040178,  12.13996339,  12.99932446],
                                [ 52.3373722 ,  54.04890265,  56.4537461 ,  54.74221565]]), 0.44360731519999963, 0.8500074167999998)
        l_prism =  Prism(array([[ 19.08576266,  20.43434719,  19.77759778,  18.42901326],
                                [ 34.78776701,  35.44451641,  36.79310093,  36.13635153]]), 0.0, 2.0)
        agent_theta =  [ 0.45318688,  0.44080626,  0.39198138,  0.26087461,  0.02694216,  0.04905031]


        features = compute_fdict(spatial_features_names_avs_polygon_polygon(),
                                 spatial_features_avs_polygon_polygon(f_prism.points_xy,
                                                                         l_prism.points_xy, agent_theta[0]))
        mpl.gca().set_aspect("equal")                
        #mpl.show()

        for key, value in sorted(features.iteritems()):
            print key, value


        assert allclose(features["F_avsHeight_-1_0"], -1.2797392167521806)
        assert allclose(features["F_avsHeight_0_-1"], 0.96482147016613318)
        assert allclose(features["F_avsHeight_0_1"],  0.99831498193067569)
        assert allclose(features["F_avsHeight_1_0"],  1.3390039512081222)


    def testFunkyArguments(self):
        """
        Test that it returns the same values. 
        """
        otheta = 1.1752771158
        of_points_xy = [[ 19.08576266, 20.43434719, 19.77759778, 18.42901326,],
                        [ 34.78776701, 35.44451641, 36.79310093, 36.13635153,]]
        ol_points_xy = [[ 19.08576266, 20.43434719, 19.77759778, 18.42901326,],
                        [ 34.78776701, 35.44451641, 36.79310093, 36.13635153,]]

        result = None

        for i in range(0, 20):
            print "i", i
            fvec = compute_fdict(spatial_features_names_avs_polygon_polygon(),
                                 spatial_features_avs_polygon_polygon(of_points_xy,
                                                                         ol_points_xy,
                                                                         otheta))
            if result == None:
                result = fvec
            else:
                for key in result.keys():
                    print key
                    self.assertEqual(result[key], fvec[key])


