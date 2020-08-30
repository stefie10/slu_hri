from esdcs.groundings import Prism
from spatial_features_cxx import sfe_f_prism_l_prism, \
    sfe_f_prism_l_prism_names, math3d_higher_than, math2d_overlaps, \
    math3d_intersect_prisms, math3d_supports
import unittest
from numpy import array
from numpy import transpose as tp
from features.feature_utils import compute_fdict
import pylab as mpl
        
class TestCase(unittest.TestCase):
    def testPrism(self):
        prism1 = Prism(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                       zStart=0, zEnd=4)

        prism2 = Prism(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                       zStart=4.1, zEnd=5)

        self.assertEqual(math3d_higher_than(prism2, prism2), False)
        self.assertEqual(math3d_higher_than(prism1, prism1), False)
        
        self.assertEqual(math3d_higher_than(prism1, prism2), False)
        self.assertEqual(math3d_higher_than(prism2, prism1), True)


        self.assertEqual(math2d_overlaps(prism1.points_xy, prism2.points_xy), True)
        self.assertEqual(math2d_overlaps(prism2.points_xy, prism1.points_xy), True)
        

        #print "points", prism1.points_xy
        #print "points", prism1.points_xy[0]
        features = sfe_f_prism_l_prism(prism1, prism2, normalize=True);
        fnames = list(sfe_f_prism_l_prism_names());
        self.assertEqual(len(fnames), len(features))
        print fnames
        print features
        fmap = dict(zip(fnames, features))
        self.assertEqual(fmap['F_3dEndsHigherThanFigureLandmark'], 0);
        self.assertEqual(fmap['F_3dEndsHigherThanLandmarkFigure'], 1);

        self.assertEqual(fmap['F_3dSupportsFigureLandmark'], 1);        
        self.assertEqual(fmap['F_3dSupportsLandmarkFigure'], 0);
        
        




    def testPolygonInsideAnother(self):
        figure = Prism(array([[  7.69945323,   7.69945323,  10.97806236,  11.42204982,
                                 8.47089291],
                              [ 54.13234479,  54.13234479,  55.86027265,  54.38893454,
                                52.75711988]]),
                       0.85000741680000036, 1.8500074168000005)
        landmark = Prism(array([[  8.20976285,   7.35040178,  12.13996339,  12.99932446],
                                [ 52.3373722 ,  54.04890265,  56.4537461 ,  54.74221565]]),
                         0.44360731519999963, 0.8500074167999998)




        self.assertEqual(math2d_overlaps(figure.points_xy, landmark.points_xy),
                         True)

        self.assertEqual(math2d_overlaps(landmark.points_xy, figure.points_xy),
                         True)

        self.assertEqual(math3d_higher_than(figure, landmark),
                         True)

        self.assertEqual(math3d_higher_than(landmark, figure),
                         False)

        self.assertEqual(math3d_supports(figure, landmark),
                         False)
        
        self.assertEqual(math3d_supports(landmark, figure),
                         True)

        

        names = sfe_f_prism_l_prism_names()
        feats_obs = sfe_f_prism_l_prism(figure, landmark, normalize=True)

        features = dict(zip(names, feats_obs))
        self.assertEqual(features["F_3dSupportsLandmarkFigure"], 1)
        
        self.assertEqual(features["F_3dSupportsFigureLandmark"], 0)

        
    def testNotOverlapping(self):
        fend = Prism(array([[ 11.38086607,  11.11520079,  10.6916185 ,  10.95728378],
                          [ 50.18213065,  50.60571294,  50.34004767,  49.91646537]]), 0.0, 2.0)
        lend = Prism(array([[  8.81022941,   8.31022943,   9.34945991,   9.8494599 ],
                            [ 52.6054371 ,  53.47146252,  54.07146249,  53.20543707]]),
                     0.81463427695147927, 1.5180196621514792)
        
        features = compute_fdict(sfe_f_prism_l_prism_names(),
                                 sfe_f_prism_l_prism(fend, lend, normalize=True))


        

        self.assertEqual(math3d_higher_than(fend, lend), True)
        self.assertEqual(math3d_higher_than(lend, fend), False)
        self.assertEqual(math2d_overlaps(fend.points_xy, lend.points_xy), False)
        self.assertEqual(math3d_intersect_prisms(fend, fend), True)


        self.assertEqual(features["F_3dSupportsLandmarkFigure"], 0)
        
        self.assertEqual(features["F_3dSupportsFigureLandmark"], 0)

        
    def testSameFigureAndLandmark(self):

        
        f_prism = Prism(array([[ 21.72099827,  21.22099828,  22.26022877,  22.76022875],
                              [ 40.789814  ,  41.65583942,  42.25583939,  41.38981397]]),
                       3.3273999996559184e-06, 0.70338871259999969)
        l_prism = Prism(array([[ 21.72099827,  21.22099828,  22.26022877,  22.76022875],
                               [ 40.789814  ,  41.65583942,  42.25583939,  41.38981397]]),
                        3.3273999996559184e-06, 0.70338871259999969)
        

        features = compute_fdict(sfe_f_prism_l_prism_names(),
                                 sfe_f_prism_l_prism(f_prism, l_prism, normalize=True))

        #mpl.show()

        self.assertEqual(features["F_3dSupportsLandmarkFigure"], 0)
        self.assertEqual(features["F_3dSupportsFigureLandmark"], 0)
        self.assertEqual(features["F_3dIntersectsFigureLandmark"], 1)

    def testSupports(self):
        f_prism = Prism(array([[ 12.19116674,  11.65687213,  10.8115738 ,  11.34586841],
                               [ 49.87727769,  50.72257602,  50.18828141,  49.34298308]]), 0.0, 2.0)
        l_prism = Prism(array([[ 10.61577541,  10.11577543,  11.15500591,  11.6550059 ],
                               [ 50.24525845,  51.11128387,  51.71128384,  50.84525842]]), 0.30936596999170651, 1.0127513551917064)
        


        mpl.gca().clear()
        mpl.gca().set_aspect("equal")        

        #mpl.show()
        features = compute_fdict(sfe_f_prism_l_prism_names(),
                                 sfe_f_prism_l_prism(f_prism, l_prism,
                                                        normalize=True))
        self.assertEqual(features["F_3dSupportsLandmarkFigure"], 0)
        self.assertEqual(features["F_3dSupportsFigureLandmark"], 0)
        self.assertEqual(features["F_3dIntersectsFigureLandmark"], 0)
        

    def testSupports1(self):
        f_prism =  Prism(array([[ 16.26972295,  17.58320551,  16.85879986,  15.5453173 ],
                                [ 47.84974226,  48.57414791,  49.88763048,  49.16322482]]), 0.0, 2.0)
        l_prism =  Prism(array([[ 17.28494274,  16.78494273,  17.82417321,  18.32417321],
                                [ 48.70261888,  49.56864429,  50.16864428,  49.30261887]]),
                         0.27844635713715404, 0.98183174233715431)

        mpl.gca().clear()
        mpl.gca().set_aspect("equal")        
        #mpl.show()

        features = compute_fdict(sfe_f_prism_l_prism_names(),
                                 sfe_f_prism_l_prism(f_prism, l_prism,
                                                        normalize=True))
        self.assertEqual(features["F_3dSupportsLandmarkFigure"], 0)
        self.assertEqual(features["F_3dSupportsFigureLandmark"], 1)
        self.assertEqual(features["F_3dIntersectsFigureLandmark"], 1)

        self.assertEqual(features["F_3dEndsHigherThanLandmarkFigure"], 0)
        self.assertEqual(features["F_3dEndsHigherThanFigureLandmark"], 1)


        self.assertEqual(features["F_3dStartsHigherThanLandmarkFigure"], 1)
        self.assertEqual(features["F_3dStartsHigherThanFigureLandmark"], 0)

    def testSupports2(self):
        f_prism =  Prism(array([[ 12.40321594,  11.89190306,  10.48174026,  10.99305313],
                                [ 50.60192082,  52.01208363,  51.50077075,  50.09060794]]), 0.0, 2.0)
        l_prism =  Prism(array([[ 10.77335704,  10.26535702,  11.3045877 ,  11.81258772],
                                [ 51.37659439,  52.25647628,  52.85647637,  51.97659448]]), 0.30952800960131738, 1.3382280096013166)

        mpl.gca().clear()
        mpl.gca().set_aspect("equal")        

        #mpl.show()

        features = compute_fdict(sfe_f_prism_l_prism_names(),
                                 sfe_f_prism_l_prism(f_prism, l_prism,
                                                     normalize=True))
        self.assertEqual(features["F_3dSupportsLandmarkFigure"], 0)
        self.assertEqual(features["F_3dSupportsFigureLandmark"], 1)
        self.assertEqual(features["F_3dIntersectsFigureLandmark"], 1)

        self.assertEqual(features["F_3dEndsHigherThanLandmarkFigure"], 0)
        self.assertEqual(features["F_3dEndsHigherThanFigureLandmark"], 1)


        self.assertEqual(features["F_3dStartsHigherThanLandmarkFigure"], 1)
        self.assertEqual(features["F_3dStartsHigherThanFigureLandmark"], 0)
        
