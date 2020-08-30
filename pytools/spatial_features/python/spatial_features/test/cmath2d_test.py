import spatial_features_cxx as sf
from gsl_utilities import tklib_mean
import unittest
from numpy import transpose as tp
from assert_utils import assert_array_equal as aeq
import numpy as na
from numpy import array as arr
import math
from scipy import allclose

class TestCase(unittest.TestCase):

    def testIntersectPolygonLine(self):
        aeq(sf.math2d_intersect_polygon_line(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                             tp([(-1, -1), (0, 0)])),
            tp([(0, 0)]))

        aeq(sf.math2d_intersect_polygon_line(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                             tp([(-1, -1), (-0.5, 0.5)])),
            [])

        aeq(sf.math2d_intersect_polygon_line(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                             tp([(0.1, 0.1), (0.5, 0.5)])),
            [])

        aeq(sf.math2d_intersect_polygon_line(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                             tp([(0.1, 0.1), (2, 0.1)])),
            tp([(1, 0.1)]))

    def testClosestPointOnLine(self):
        aeq(sf.math2d_closest_point_on_line(tp([(0.0, 0.0), (1,1)]),
                                                           (1, 0.0)),
                           (0.5, 0.5))

        aeq(sf.math2d_closest_point_on_line(tp([(0.0, 0.0), (1,1), (2, 5)]),
                                                           (1, 0.0)),
                           (0.5, 0.5))

        aeq(sf.math2d_closest_point_on_line(tp([(0.0, 0.0), (1,1.0), (2, 5.0)]),
                                                           (5.0, 0.0)),
                           (1, 1))

        aeq(sf.math2d_closest_point_on_line(tp([(0.0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
                                                           (-1.0, 0.5)),
                           (0, 0.5))
        aeq(sf.math2d_closest_point_on_line(tp([(22.7713,25.4815), (22.388,25.0315), (22.388,25.0315), 
                                                                       (22.4067,25.0002), (22.438,24.919), (22.438,24.9065), 
                                                                       (22.463,24.969), (22.438,24.9815)]),  
                                                                      (23.324929146307721, 26.312036364557606)),
                           (22.7713, 25.4815))


        aeq(sf.math2d_closest_point_on_line(tp([(0.0, 0.0), (1,1)]),
                                                       (1, 0.0)),
                           (0.5, 0.5))
        
        aeq(sf.math2d_closest_point_on_line(tp([(0.0, 0.0), (1,1), (2, 5)]),
                                                       (1, 0.0)),
                           (0.5, 0.5))
        
        aeq(sf.math2d_closest_point_on_line(tp([(0.0, 0.0), (1,1.0), (2, 5.0)]),
                                                       (5.0, 0.0)),
                           (1, 1))
        
        aeq(sf.math2d_closest_point_on_line(tp([(0., 0.), (1, 0), (1, 1), (0, 1), (0, 0.)]),
                                                       (-1., 0.5)),
                           (0, 0.5))
        aeq(sf.math2d_closest_point_on_line(tp([(22.7713,25.4815), (22.388,25.0315), (22.388,25.0315), 
                                                                     (22.4067,25.0002), (22.438,24.919), (22.438,24.9065), 
                                                                     (22.463,24.969), (22.438,24.9815)]),  
                                                       (23.324929146307721, 26.312036364557606)),
                           (22.7713, 25.4815))

        
        
        aeq(sf.math2d_closest_point_on_line(tp([(0, 0), (1, 0), (1, 1), (0, 1), (0,0.)]),
                                                       (-1, 0.5)),
                           (0, 0.5))
        
        aeq(sf.math2d_closest_point_on_line(tp([(0, 0), (1, 0), (1, 1), (0, 1), (0,0.)]),
                                                       (1, 0.5)),
                           (1, 0.5))




    def testTrimPolygon(self):
        aeq(sf.math2d_trim_polygon(tp([(0.0, 0), (1, 1), (2, 0)]),
                                                  (0.5, 0.5),
                                                  (1.5, 0.5)),
                           tp([(0.5, 0.5), (1, 1), (1.5, 0.5)]))
        
        aeq(sf.math2d_trim_polygon(tp([(0.0, 0), (1, 1), (2, 0)],
                                                            (1.5, 0.5),
                                                            (0.5, 0.5))),
                           tp([(1.5, 0.5), (2, 0), (0, 0), (0.5, 0.5)]))
    def testTrimLine(self):
        aeq(sf.math2d_trim_line(tp([(0.0, 0), (1, 1), (2, 1)]),
                                               (0.5, 0.5),
                                               (1.5, 1)),
                           tp([(0.5, 0.5), (1, 1), (1.5, 1)]))
        
        aeq(sf.math2d_trim_line(tp([(0.0, 0), (1, 1)]),
                                               (0.5, 0.5),
                                               (0.6, 0.6)),
                           tp([(0.5, 0.5), (0.6, 0.6)]))


        arg = [(0.408545,-1.48909), (0.225273,-1.19891), (0.622364,-0.985091), (0.828545,0.366545), (0.584182,1.44327), (-0.0801818,1.16836), (-0.431455,1.45091)]
        trimmed = sf.math2d_trim_line(arg,
                                      (-0.15845056851323014, 1.2313189355432503), 
                                      (0.26737251469300988, -1.2655670876578717))
        aeq(trimmed, arg)
                         
        
    def testStepAlongLine(self):

        aeq(sf.math2d_step_along_line(tp([(20.764426155331225, 15.291993588196641), 
                                                         (20.764426155331229, 15.291993588196641)]),
                                                     3.5527136788e-17),
                           tp([(20.764426155331225, 15.291993588196641),
                               (20.764426155331229, 15.291993588196641)]))



        aeq(sf.math2d_step_along_line(tp([(0.0, 0), (1, 0)]), 1),
                         tp([(0.0,0), (1, 0)]))

        aeq(sf.math2d_step_along_line(tp([(0.0, 0), (1, 0)]), 2),
                           tp([(0,0)]))

        aeq(sf.math2d_step_along_line(tp([(0.0, 0)]), 2),
                           tp([(0,0)]))
                          
                         
        aeq(sf.math2d_step_along_line(tp([(0.0, 0), (1, 0)]),
                                                     0.5),
                           tp([(0, 0), (0.5, 0), (1, 0)]))


        aeq(sf.math2d_step_along_line(tp([(0, 0), (1.0, 0)]),
                                                     0.1),
                           tp([(0, 0), 
                               (0.1, 0),
                               (0.2, 0),
                               (0.3, 0),
                               (0.4, 0),
                               (0.5, 0),
                               (0.6, 0),
                               (0.7, 0),
                               (0.8, 0),
                               (0.9, 0),
                               (1.0, 0)]))


        aeq(sf.math2d_step_along_line(tp([(0, 0),
                                                         (1.0, 0), (1, 1)]),
                                                     0.1),
                           tp([(0, 0), 
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
                               ]))
        
        sf.math2d_step_along_line(tp([(22.800000, 29.400000),(24.400000, 21.800000),(33.000000, 20.200000),(42.200001, 19.000000),(50.800001, 18.400000),(53.000001, 26.400000),(62.200001, 25.600000),(71.400001, 25.000000),(76.200001, 20.000000),(81.200001, 15.000000),(88.400001, 18.400000),]),
                                  0.831288)

        sf.math2d_step_along_line(tp([(22.800000, 29.400000),(23.400000, 29.200000),(24.000000, 29.200000),(24.600000, 29.000000),(25.000000, 28.600000),(25.000000, 28.000000),(25.000000, 27.400000),(25.000000, 26.800000),(24.800000, 26.200000),(24.600000, 25.600000),(24.400000, 25.000000),(24.400000, 24.400000),(24.400000, 23.800000),(24.400000, 23.200000),(24.400000, 22.600000),(24.400000, 22.000000),(24.200000, 21.400000),(24.800000, 21.000000),(25.400000, 21.000000),(26.000000, 21.000000),(26.600000, 21.000000),(27.200000, 21.200000),(27.800000, 21.000000),(28.400000, 20.800000),(29.000000, 20.600000),(29.600000, 20.600000),(30.200000, 20.600000),(30.800000, 20.400000),(31.400000, 20.400000),(32.000000, 20.200000),(32.600000, 20.200000),(33.200000, 20.200000),(33.800001, 20.000000),(34.400001, 20.000000),(35.000001, 20.000000),(35.600001, 20.000000),(36.200001, 20.000000),(36.800001, 19.800000),(37.400001, 19.600000),(38.000001, 19.400000),(38.600001, 19.200000),(39.200001, 19.200000),(39.800001, 19.200000),(40.400001, 19.200000),(41.000001, 19.000000),(41.600001, 19.000000),(42.200001, 19.000000),(42.800001, 19.000000),(43.400001, 18.600000),(44.000001, 18.200000),(44.600001, 18.200000),(45.200001, 18.000000),(45.800001, 17.800000),(46.400001, 17.600000),(47.000001, 17.600000),(47.600001, 17.600000),(48.200001, 17.600000),(48.800001, 17.400000),(48.800001, 16.800000),(48.800001, 16.200000),(48.800001, 15.600000),(48.600001, 15.000000),(48.600001, 14.400000),(48.400001, 13.800000),(48.400001, 13.200000),(48.400001, 12.600000),(48.200001, 12.000000),(48.200001, 11.400000),(48.200001, 10.800000),(48.200001, 10.200000),(48.200001, 9.600000),(48.600001, 9.000000),(49.200001, 8.400000),(49.800001, 8.200000),(50.400001, 8.200000),(51.000001, 8.200000),(51.600001, 8.200000),(52.200001, 8.200000),(52.800001, 8.200000),(53.400001, 8.000000),(54.000001, 8.000000),(54.600001, 8.000000),(55.200001, 8.200000),(55.800001, 8.000000),(56.400001, 8.000000),(57.000001, 7.800000),(57.600001, 7.800000),(58.200001, 8.000000),(58.800001, 7.800000),(59.400001, 7.800000),(60.000001, 7.800000),(60.600001, 7.800000),(61.200001, 7.600000),(61.800001, 7.800000),(62.400001, 7.800000),(63.000001, 7.600000),(63.600001, 7.600000),(64.200001, 7.600000),(64.800001, 7.400000),(65.400001, 7.400000),(66.000001, 7.400000),(66.600001, 7.400000),(67.200001, 7.200000),(67.800001, 7.400000),(68.400001, 7.400000),(69.000001, 7.400000),(69.600001, 7.400000),(70.200001, 7.200000),(70.800001, 7.000000),(71.400001, 7.000000),(72.000001, 7.000000),(72.600001, 7.000000),(73.200001, 7.000000),(73.800001, 7.000000),(74.400001, 7.000000),(75.000001, 7.000000),(75.600001, 7.000000),(76.200001, 7.000000),(76.800001, 7.000000),(77.400001, 7.000000),(77.800001, 7.400000),(77.800001, 8.000000),(77.800001, 8.600000),(78.000001, 9.200000),(78.000001, 9.800000),(78.000001, 10.400000),]), 0.769950)
    def testStepAlongLineCPython(self):
        figure =[arr([-34.4109722 ,  36.53796877]), arr([-39.54816656,  39.65743409]), arr([-42.78012498,  30.83530097]), arr([ 39.55015816,  47.22064486]), arr([-14.7026671 , -37.17925864]), arr([-43.06252234,  49.81011449]), arr([  2.30778403,  38.57293883]), arr([  9.71043013,  18.37371935]), arr([ 33.8073788 ,  23.53358069]), arr([-30.98480675, -23.44172106]), arr([-46.72568417,   5.74458689]), arr([ 44.79693836, -30.45098366]), arr([ 16.9431011 ,  24.79694071]), arr([-49.33496406,  35.05335686]), arr([ 37.18273683, -36.61940509]), arr([-46.811895  , -36.37183577]), arr([ 29.70280472,   3.64882352]), arr([ 12.01472527,  16.04758815]), arr([-15.33277122,  32.70857939]), arr([-33.09346972,  11.48085643]), arr([-43.55050741,  26.45942728]), arr([  9.37337172, -23.59093203]), arr([-45.09089175, -13.65844888]), arr([ 44.49695608,  31.95748126]), arr([-20.03968775,  16.75066075]), arr([ 27.69354355, -30.78834174]), arr([-20.99523531,  42.92917723]), arr([-29.56497372,  49.3837239 ]), arr([ 41.74448442,   5.65682851]), arr([ 34.20236227,  28.13261673]), arr([  8.34045735,  45.21838519]), arr([ 14.44133542,  23.75909523]), arr([ 20.89485579,  11.55715208]), arr([ 39.4221815 , -26.41434784]), arr([ -2.35075451,  32.99036684]), arr([ -1.21114514, -24.86030826]), arr([-9.34611762,  2.28488945]), arr([-24.79801708,   3.35025253]), arr([-4.59595627,  7.65702842]), arr([-25.94450938,  29.01709807]), arr([ 39.96577764, -19.5369915 ]), arr([-44.22427665,  39.41074059]), arr([-48.47978916,  29.31617991]), arr([ -2.58911581, -23.00257887]), arr([  9.09996186,  31.51315144]), arr([ 46.75309215, -27.04243369]), arr([ -5.43373666,  27.33144954]), arr([ -3.5378969 , -27.34198791]), arr([ 29.36939252, -31.42998281]), arr([ 21.31197586,  -8.26121984]), arr([ 28.16948778,  48.29375864]), arr([-25.95514162, -22.63943068]), arr([  4.3174498 , -13.89561334]), arr([  3.89623927, -46.60511383]), arr([ 6.92370438,  5.90993029]), arr([ 29.739255  ,  23.67023584]), arr([-10.59918606, -48.87605305]), arr([-26.95248891, -25.73538142]), arr([ -1.18284085, -25.65187099]), arr([-32.21281648, -32.60447954]), arr([-49.27909758, -43.56861937]), arr([-49.83685856,   7.84541461]), arr([ -9.26232443, -34.21998808]), arr([ -7.16463912,  14.9580592 ]), arr([-28.37402083,  -5.09616458]), arr([  9.5919099 ,  48.18912048]), arr([ -5.25124571,  40.64731045]), arr([-6.83270791,  4.34934884]), arr([ 48.98657104, -46.17843197]), arr([ 47.73413883,  38.11327138]), arr([ 24.31577398,   6.18676309]), arr([-28.86590758, -29.5652911 ]), arr([ 34.75558496, -34.45488428]), arr([ 11.16790136,   4.11576647]), arr([ 28.79449518,   6.0780314 ]), arr([  8.30959224, -34.8733599 ]), arr([-6.77609589, -4.9884234 ]), arr([ -8.3511011 , -22.16194171]), arr([ 46.31020392, -47.75533939]), arr([ 41.72595967,  20.25975881]), arr([ 49.86917909,  38.24365918]), arr([ 19.03729073,  23.45800999]), arr([ 19.78902367,   2.23791365]), arr([ 43.86482208, -11.35675427]), arr([-25.58226792,  15.98113182]), arr([ -7.76806147, -36.43539808]), arr([-36.04769585,  -0.993352  ]), arr([-49.94229858,  44.00280461]), arr([-32.57572717, -23.44443414]), arr([  6.01878937, -49.4548436 ]), arr([ 43.12556105, -30.49664694]), arr([-45.22741045,  -5.19508557]), arr([ 36.45841998,   1.34441924]), arr([-38.74479128,  22.10124029]), arr([-26.97005746, -12.15287167]), arr([-19.92878577,  -5.24784386]), arr([ 18.13612737,  10.96982622]), arr([ -4.79982567,  11.0980572 ]), arr([ -8.36783821,  37.27256111]), arr([ 30.49448543,  40.34242983])]


        cstepSize = sf.math2d_line_length(tp(figure))/100.0
        cResult = tp(sf.math2d_step_along_line(tp(figure), cstepSize))


        aeq(cResult[0], (-34.4109722, 36.53796877))
        aeq(cResult[-1], (30.49448543, 40.34242983))
        self.assertEqual(len(cResult), 101)
        


    def testEigenvectorsSquare(self):
        polygon = [(0, 0), (0, 1), (1, 1), (1, 0.0)]
        estuff = sf.math2d_eigenvectors(tp(polygon))


        v = na.array(estuff.evecs)
        print "cevecs", v
        print "cevals", estuff.evals

        
        major = v[:, 0]
        minor = v[:, 1]


        self.assertEqual(na.shape(v), (2, 2))
        aeq(major,
                           [ 0.70710678,  0.70710678])
        aeq(minor,
                           [ -0.70710678,  0.70710678])
        
        caxes = sf.math2d_eigen_axes(tp(polygon))

        cmajor = na.array(caxes.major_st), na.array(caxes.major_end)
        cminor = na.array(caxes.minor_st), na.array(caxes.minor_end)

        aeq(cmajor,
                           [na.array([ 0.11109127,  0.11109127]),
                            na.array([ 0.88890873,  0.88890873])])

        
        aeq(cminor,
                           [na.array([ 0.53535534,  0.46464466]),
                            na.array([ 0.46464466,  0.53535534])])
        



    def testEigenvectorsTranslatedSquare(self):

        eigenstuff = sf.math2d_eigenvectors(
            tp([(1.0, 1), (1, 2), (2, 2), (2, 1)]))
        v = na.array(eigenstuff.evecs)
        

        major = v[:, 0]
        minor = v[:, 1]


        self.assertEqual(na.shape(v), (2, 2))
        aeq(major,
                           [ 0.70710678,  0.70710678])
        aeq(minor,
                           [ -0.70710678,  0.70710678])



        
    def testCentroid(self):
        self.assertEqual(sf.math2d_centroid(tp([(0,0), (1, 0), (1, 1), (0.0, 1)])),
                         [0.5, 0.5])
        
        self.assertEqual(sf.math2d_centroid(tp([(0, 0.0),
                                                (-1, 0), (-1, -1), (0, -1)])),
                         [-0.5, -0.5])

        self.assertEqual(sf.math2d_centroid(tp([ (-1, -3), (8, -4), (2, 1.0)])),
                         [3, -2])
        self.assertEqual(sf.math2d_centroid(tp([(8, -4), (-1, -3), (2, 1.0)])),
                         [3, -2])
        self.assertEqual(sf.math2d_centroid(tp([(8, -4),  (2, 1), (-1, -3.0)])),
                         [3, -2])



    def testArea(self):
        self.assertEqual(sf.math2d_area(tp([(0, 0), (1, 0), (1, 1), (0, 1.0)])),
                         1)

        self.assertEqual(sf.math2d_area(tp([(0, 0), (1, 0), (1, 1.0)])),
                         0.5)

        self.assertEqual(sf.math2d_area(tp([(0, 0), (1, 1), (-1, -1.0)])),
                         0)
        self.assertEqual(sf.math2d_area(tp([(0.0, 0.0), (0, 1), (1, 1.0), (1, 2), (2, 2),
                                      (2.0, 0)])),
                                     3)
        
        self.assertEqual(sf.math2d_area(tp([(-1, -3), (2, 1), (8, -4.0)])),
                         19.5)
        

    def testSignedArea(self):
        self.assertEqual(sf.math2d_signed_area(tp([(0, 0), (1, 0),
                                                   (1.0, 1), (0, 1)])),
                         1)

        self.assertEqual(sf.math2d_signed_area(tp([(0.0, 0), (1, 0), (1, 1)])),
                         0.5)

        self.assertEqual(sf.math2d_signed_area(tp([(0.0, 0), (1, 1), (-1, -1)])),
                         0)
        self.assertEqual(sf.math2d_signed_area(tp([(0.0, 0.0), (0, 1),
                                                   (1, 1), (1, 2), (2, 2),
                                                   (2.0, 0)])),
                                     -3)
        
        self.assertEqual(sf.math2d_signed_area(tp([(-1, -3), (2, 1),
                                                   (8.0, -4)])),
                         -19.5)

        self.assertEqual(sf.math2d_signed_area(tp([(8.0, -4),
                                                   (2, 1), (-1, -3)])),
                         19.5)
        
        



    def testFitLine(self):
        r = sf.math2d_fit_line(tp([(0, 0), (1, 1.0)]))
        m = r.slope
        b = r.intercept
        self.assertEqual(m, 1)
        self.assertEqual(b, 0)

        # horizontal line
        r = sf.math2d_fit_line(tp([(-0.5, 0.5), (1.5, 0.5)]))
        m = r.slope
        b = r.intercept
        self.assertEqual(m, 0)
        self.assertEqual(b, 0.5)

        # vertical line 
        r = sf.math2d_fit_line(tp([(-0.5, 0.5), (-0.5, 1)]))
        m = r.slope
        b = r.intercept
        self.assertEqual(na.isnan(m), True)
        self.assertEqual(na.isnan(b), True)
        

    def testCenterOfMass(self):
        self.assertEqual(sf.math2d_center_of_mass(tp([(0,0.0), (1, 1),
                                                      (-1, -1)])),
                         [0, 0])

        self.assertEqual(sf.math2d_center_of_mass(tp([(0,0.0), (1, 1)])),
                         [0.5, 0.5])
        self.assertEqual(sf.math2d_center_of_mass(tp([(0,1.0), (-1, 1)])),
                         [-0.5, 1])



    def testTrimLine(self):
        aeq(sf.math2d_trim_line(tp([(0.0, 0), (1, 1), (2, 1)]),
                                               (0.5, 0.5),
                                               (1.5, 1)),
                           tp([(0.5, 0.5), (1, 1), (1.5, 1)]))

        aeq(sf.math2d_trim_line(tp([(0.0, 0), (1, 1)]),
                                               (0.5, 0.5),
                                               (0.6, 0.6)),
                           tp([(0.5, 0.5), (0.6, 0.6)]))
        
        
        trimmed = sf.math2d_trim_line(tp([(0.408545,-1.48909),
                                          (0.225273,-1.19891),
                                          (0.622364,-0.985091),
                                          (0.828545,0.366545),
                                          (0.584182,1.44327),
                                          (-0.0801818,1.16836),
                                          (-0.431455,1.45091)]),
                              (-0.15845056851323014, 1.2313189355432503), 
                              (0.26737251469300988, -1.2655670876578717))
        self.assertEqual(len(tp(trimmed)),7)
                         


    def testTrimPolygon(self):
        aeq(sf.math2d_trim_polygon(tp([(0, 0), (1.0, 1), (2, 0)]),
                                                  (0.5, 0.5),
                                                  (1.5, 0.5)),
                           tp([(0.5, 0.5), (1, 1), (1.5, 0.5)]))

        aeq(sf.math2d_trim_polygon(tp([(0, 0.0), (1, 1), (2, 0)]),
                                                  (1.5, 0.5),
                                                  (0.5, 0.5)),
                           tp([(1.5, 0.5), (2, 0), (0, 0), (0.5, 0.5)]))




    def testComputeBoundaryLine(self):
        aeq(sf.math2d_compute_boundary_line(tp([(0.0, 0),
                                                               (1, 0),
                                                               (1, 1),
                                                               (0.0, 1)]),
                                                           tp([(2, 0.0), (3.0, 1)])),
                           tp([(1.0, 0.0), (1, 0), (1.0, 1.0)]))
        
        



    def testSmallestWindow(self):
        def x(r):
            return r.start_i, r.end_i
        self.assertEqual(x(sf.math2d_smallest_window([0,1,1,0,0,0],3)),
                         (3,6))
        
        self.assertEqual(x(sf.math2d_smallest_window([0,0,0,0,0,0],3)),
                         (0,3))

        self.assertEqual(x(sf.math2d_smallest_window([1,0,0,0,0,0],3)),
                         (1,4))

        self.assertEqual(x(sf.math2d_smallest_window([1,0,0,0,0,0],4)),
                         (1,5))




    def testAngleBetweenLines(self):
        
        self.assertEqual(sf.math2d_angle_between_segments((0,0),(1,1),
                                                          (0,0),(-1,1)),
                         math.pi/2)

        self.assertEqual(sf.math2d_angle_between_segments((0,0),(-1,1),
                                                          (0,0),(1,1)),
                         math.pi/2)

        self.assertEqual(sf.math2d_angle_between_segments((0,0),(1,1),
                                                          (0,0),(1,0)),
                         math.pi/4)
        
        self.assertEqual(sf.math2d_angle_between_segments((0,0),(0,1),
                                                          (0,0),(1,0)),
                         math.pi/2)
        
        self.assertEqual(sf.math2d_angle_between_segments((22.538, 15.308377141861092), 
                                                          (22.538, 15.308377141861092),
                                                          (26.99214769,  12.12461925),  
                                                          (7.22290453,  31.89386241)),
                         0)



    def testPointOnSegment(self):

        aeq(sf.math2d_point_on_segment((0, 0),
                                       (math.pow(2, 0.5), 
                                        math.pow(2, 0.5)), 
                                       1),
            [math.pow(2, 0.5)/2, math.pow(2, 0.5)/2])
        
        self.assertEqual(sf.math2d_point_on_segment((0, 0), (1, 0), 0.0),
                         [0.0,0.0])


    def testTop(self):
        aeq(sf.math2d_top(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                          (0, 1)),
            tp([(1, 1), (0, 1)]))

        aeq(sf.math2d_top(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                          (0, -1)),
            tp([(0, 0), (1, 0)]))


        aeq(sf.math2d_top(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                          (1, 1)),
            tp([(1, 0), (1, 1), (0, 1)]))                

    def testUnitVector(self):
        aeq(sf.math2d_vector_to_unit_vector((0, 1)),
            (0, 1))

        aeq(sf.math2d_vector_to_unit_vector((1, 1)),
            (math.pow(2, 0.5)/2, math.pow(2, 0.5)/2))


        

    def testIsVisible(self):
        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (-0.5, 0.5), (1.5, 0.5)),
                         False)

        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (-0.5, 2), (1.5, 2)),
                         True)

        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (-0.5, 1), (1.5, 1)),
                         False)
        

        
        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (-2, -2), (2, 2)),
                         False)

        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (4, 4), (2, 2)),
                         True)

        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (1, 1), (1, 5)),
                         True)


        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                              (1, 1), (1, 5)),
                         True)                
        

        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                              (0, 1), (0, 5)),
                         True)


        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                              (0, 5), (0, 1)),
                         True)
        
        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (1, 1), (1, 0)),
                         False)


        
        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (1, 1), (0, 0)),
                         False)


        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (1, 0), (0, 0)),
                         False)


        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                           (0, 1), (0, 0)),
                         False)

        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                              (0.5, 1), (0, 0)),
                         False)

        self.assertEqual(sf.math2d_is_visible(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                              (0.5, 1), (2, 2)),
                         True)
        
    def testHighestPoint(self):
        aeq(sf.math2d_highest_point(tp([(0, 0), (0, 1), (10, 10)]),
                                    (1, 1)),
            (10, 10))

        aeq(sf.math2d_highest_point(tp([(0, 0), (0, 1), (10, 10)]),
                                    (0, 1)),
            (10, 10))

        aeq(sf.math2d_highest_point(tp([(0, 0), (0, 1), (5, 0)]),
                                    (0, 1)),
            (0, 1))




        aeq(sf.math2d_highest_point(tp([(0, 0), (0, 1), (10, 10)]),
                                    (-1, -1)),
            (0, 0))

        aeq(sf.math2d_highest_point(tp([(0, 0), (0, 1), (10, 10)]),
                                    (0, -1)),
            (0, 0))

        aeq(sf.math2d_highest_point(tp([(0, 0), (0, 1), (5, 0)]),

                                    (0, -1)),
            (0, 0))
        
        


        
        aeq(sf.math2d_highest_point(tp([(0, 0), (-1, 0.5), (0, 1), (10, 10)]),
                                    (-1, 0)),
            (-1, 0.5))

    def testHeightInDirection(self):
        self.assertEqual(sf.math2d_height_in_direction((0, 0),
                                                       (0, 1)), 0)

        self.assertEqual(sf.math2d_height_in_direction((0, 1),
                                                       (0, 1)), 1)  

        self.assertEqual(sf.math2d_height_in_direction((0, -1),
                                                       (0, 1)), -1)        

    def testAvsHeight(self):

        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                      (1.5, -1.5),
                                      (0, 1), 1, None),
                        0.029312230751356319)

        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                      (1.5, 1.5),
                                      (0, 1), 1, None),
                        0.37754066879814541)
        
        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                       (1.5, 3),
                                       (0, 1), 1, None),
                         0.7310585786300049)

        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                       (2.5, 3),
                                       (0, 1), 1, None),
                         0.7310585786300049)

        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                       (2.5, 10),
                                       (0, 1), 1, None),
                         0.99966464986953352)

        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                       (2.5, -10),
                                       (0, 1), 1, None),
                         6.1441746022147182e-06)


        
                         
        


        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                       (1.5, 3),
                                       (1, 0), 1, None),
                         0.18242552380635635)


        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                       (-10, 3),
                                       (1, 0), 1, None),
                         2.2603242979035746e-06)

                         

        assert allclose(sf.avs_height(tp([(1, 1), (2, 2), (3, 1)]),
                                      (10, 10),
                                      (1, 0), 1, None),
                        0.9990889488055994)


    def testCmp(self):
        self.assertEqual(sf.math2d_cmp(0, 0), 0)
        self.assertEqual(sf.math2d_cmp(0, 1), -1)
        self.assertEqual(sf.math2d_cmp(0, -1), 1)

        self.assertEqual(sf.math2d_cmp(1, 0), 1)
        self.assertEqual(sf.math2d_cmp(-1, 0), -1)        


    def testCmpPoints(self):
        self.assertEqual(sf.math2d_cmp_points((0, 0), (1, 1)), -1)
        self.assertEqual(sf.math2d_cmp_points((0, 0), (0, 0)), 0)
        self.assertEqual(sf.math2d_cmp_points((1, 1), (0, 0)), 1)
        self.assertEqual(sf.math2d_cmp_points((1, 0), (1, 1)), -1)
        self.assertEqual(sf.math2d_cmp_points((1, 1), (1, 0)), 1)
        
        
    def testSlope(self):
        self.assertEqual(sf.math2d_slope((0,0),(1,1)),1)
        self.assertEqual(sf.math2d_slope((0,0),(1,2)),2)
        self.assertEqual(sf.math2d_slope((0,0),(1,0)),0)
        self.assertEqual(sf.math2d_slope((-1,-1),(-0.5,-1.5)),-1)
        self.assertEqual(sf.math2d_slope((0, 0),(1, 1)), 1)
        self.assertEqual(sf.math2d_slope((2, 0),(3, 1)), 1)
    




    def testIsOnSegment(self):
        #bool tklib_is_on_segment(gsl_vector* seg_st_xy, gsl_vector* seg_end_xy, gsl_vector* p_xy){
        
        
        self.assertEqual(sf.math2d_is_on_segment((0,0),(0,0),(0,0)),
                         True)
        self.assertEqual(sf.math2d_is_on_segment((0,0),(0,0),(1,1)),
                         False)

        self.assertEqual(sf.math2d_is_on_segment((0, 0), (1, 1), (0.5, 0.5)), 
                         True)
        self.assertEqual(sf.math2d_is_on_segment((1, 1), (0, 0), (0.5, 0.5)), 
                         True)
        self.assertEqual(sf.math2d_is_on_segment((0, 0), (1, 1), (0.5, 0.6)),
                         False)
        self.assertEqual(sf.math2d_is_on_segment((0, 0), (1, 1), (0, 0)), 
                         True)

        self.assertEqual(sf.math2d_is_on_segment((2, 0), (1.5, 14),
                                            (1.899999999999, 2.800000000000000000000003)),
                         True)

        self.assertEqual(sf.math2d_is_on_segment((0, 0), (0, 1),
                                            (0, 0.5)),
                         True)
        self.assertEqual(sf.math2d_is_on_segment((0, 0), (0, 0), (0.5, 0.5)),
                         False)

        self.assertEqual(sf.math2d_is_on_segment((0.0, 0.5), (1.0, 0.5), (0.5, 0.5)),
                         True)
        self.assertEqual(sf.math2d_is_on_segment((0.5, 1.0), (0.5, 0.0), (0.5, 0.5)),
                         True)

        self.assertEqual(sf.math2d_is_on_segment((0, 0), (1, 1), (1, 1)),
                         True)
        self.assertEqual(sf.math2d_is_on_segment((3, 0), (1, 1), (1, 1)),
                         True)

        self.assertEqual(sf.math2d_is_on_segment((0.548, -0.478),
                                             (0.344, 0.249),
                                             (0.344, 0.249)),
                         True)
        
        self.assertEqual(sf.math2d_is_on_segment((0.482, -0.388),
                                             (0.344, 0.249),
                                             (0.344, 0.249)),
                         True)

        
        # vertical messes it up...
        self.assertEqual(sf.math2d_is_on_segment((22.538,25.019), 
                                             (22.538,24.9815),
                                             (22.538, 28.749081807199808)),
                         False)
        
        
                         
    def testIntersectSegment(self):
        # lower segment is vertical.
        # upper segment goes above it.

        #gsl_vector* tklib_intersect_segments(gsl_vector* pt1_seg1, gsl_vector* pt2_seg1, 
        #                                            gsl_vector* pt1_seg2, gsl_vector* pt2_seg2, bool bound){
        
        self.assertEqual(sf.math2d_intersect_segments((23.3159,28.7462),
                                                         (10.8989,28.7922),
                                                         (22.538,25.019), 
                                                         (22.538,24.9815), True),
                         [])

        self.assertEqual(sf.math2d_intersect_segments((0.0, 0.5), (1.0, 0.5),
                                                         (0.5, 1.0), (0.5, 0.0), True),
                         [0.5, 0.5])
        
        
        self.assertEqual(sf.math2d_intersect_segments((10.8989,28.7922), 
                                                         (23.3159,28.7462),
                                                         (22.538,25.019), 
                                                         (22.538,24.9815), True),
                         [])
        self.assertEqual(sf.math2d_intersect_segments((-1.0, -1.0), (1.0, 1.0),
                                                         (1, -1), (-1, 1), True),
                         [0, 0])
        self.assertEqual(sf.math2d_intersect_segments((0, 0), (1, 1),
                                                         (0, 1), (1, 0), True),
                         [0.5, 0.5])
        
        self.assertEqual(sf.math2d_intersect_segments((2, 0), (1.5, 14),
                                                         (1, 1), (2, 3), True),
                         [1.8999999999999999, 2.8000000000000003])
        
        self.assertEqual(sf.math2d_intersect_segments((0, 0), (0, 1),
                                                         (-0.5, 0.5), (0.5, 0.5), True),
                         [0, 0.5])
        
        self.assertEqual(sf.math2d_intersect_segments((0, 0), (1, 0),
                                                         (-0.5, 0.5), (1.5, 0.5), True),
                         [])
        
        self.assertEqual(sf.math2d_intersect_segments((0, 0), (0, 1),
                                                         (-0.5, 0.5), (1.5, 0.5), True),
                         [0, 0.5])
        self.assertEqual(sf.math2d_intersect_segments((0, 0), (0, 0),
                                                         (3, 4), (4, 5), True),
                         [])
        self.assertEqual(sf.math2d_intersect_segments((3, 4), (4, 5),
                                                         (0, 0), (0, 0), True),
                         
                         [])
        
        aeq(sf.math2d_intersect_segments((0, 0), (1, 1),
                                                           (3, 0), (1, 1), True),
                           [1, 1])
        
        aeq(sf.math2d_intersect_segments((0.548, -0.478),
                                                           (0.344, 0.249),
                                                           (0.482, -0.388),
                                                           (0.344, 0.249), True),
                           [0.344, 0.249])

        aeq(sf.math2d_intersect_segments((0, 0), (1, 1),
                                         (0, 0), (1, 0), True),
            [0, 0])
        
    def testBoundingBox(self):
        #gsl_vector* tklib_bounding_box(gsl_matrix* pts_xy){
        aeq(sf.math2d_bbox(tp([(-1.0, 10), (130.0, 0.0)])), 
                           tp([-1, 0.0, 130.0, 10.0]))
        aeq(sf.math2d_bbox(tp([(-1.0, 10), (-130, 0)])), 
                           tp([-130, 0.0, -1.0, 10.]))
        

    def testClosestPointOnSegment(self):
        #gsl_vector* tklib_closest_point_on_segment(gsl_vector* seg_st_xy, 
	#				   gsl_vector* seg_end_xy, 
        #                                  gsl_vector* p_xy){
        
        aeq(sf.math2d_closest_point_on_segment((0.0, 0.0), (1, 1),
                                                        (1, 0.0)),
                         [0.5, 0.5])
        
        aeq(sf.math2d_closest_point_on_segment((0.0, 0.0), (1, 1),
                                                        (1, 2.0)),
                         (1, 1))
        
        aeq(sf.math2d_closest_point_on_segment((1.13424,0.015043), (1.13424,0.015043),
                                                        (3, 3)),
                         (1.13424, 0.015043))
        
        aeq(sf.math2d_closest_point_on_segment((22.437999999999999, 24.919), 
                                                        (22.437999999999999, 24.906500000000001),
                                                        (23.324929146307721, 26.312036364557606)),
                         (22.437999999999999, 24.919))


    def testClosestPointOnSegmentLine(self):
        aeq(sf.math2d_closest_point_on_segment_line((0.0, 0.0), (1, 1),
                                                             (1, 0.0)),
                         (0.5, 0.5))
        
        aeq(sf.math2d_closest_point_on_segment_line((0.0, 0.0), (1, 1),
                                                             (1, 2.0)),
                         (1.5, 1.5))
        
        aeq(sf.math2d_closest_point_on_segment_line((1.13424,0.015043), (1.13424,0.015043),
                                                             (3, 3)),
                         (1.13424, 0.015043))
        
        aeq(sf.math2d_closest_point_on_segment_line((22.437999999999999, 24.919), 
                                                             (22.437999999999999, 24.906500000000001),
                                                             (23.324929146307721, 26.312036364557606)),
                         (22.437999999999999, 26.312036364557606))
        

    def testLength(self):
        #double spatial_features_integrate_path(gsl_matrix* path_xy){
        self.assertEqual(sf.math2d_line_length(tp([(-2.0, 0.0), (0,0)])),
                         2)
        self.assertEqual(sf.math2d_line_length(tp([(0, 0),(1.0, 1.0)])),
                         math.sqrt(2))
        self.assertEqual(sf.math2d_line_length(tp([(-2.0, 0.0,), (0.0, 0.0), (1, 1)])),
                         2.0 + math.sqrt(2))
        self.assertEqual(sf.math2d_line_length(tp([(0, 0), (1, 0), (1.0, 1.0)])),2)
                         
    
    def testMidpoint(self):
        aeq(tklib_mean(tp([(0., 0), (0, 0)]), 0),
            (0, 0))
        aeq(tklib_mean(tp([(0., 0), (1, 1)]), 0),
            (0.5, 0.5))
        
        aeq(tklib_mean(tp([(0., 0), (0, 1)]), 0),
            (0, 0.5))
        
        aeq(tklib_mean(tp([(0., 0), (1, 0)]), 0),
            (0.5, 0))
        aeq(tklib_mean(tp([(11.462999999999999, 15.20607079731321), 
                              (11.462999999999997, 28.790125459845836)]), 0),
            (11.462999999999999999, 21.998098128579521))


    #gsl_matrix* sf.math2d_perpendicular_segment(gsl_vector* seg_st, gsl_vector* seg_end, gsl_vector* start_point){
    def testPerpendicular(self):
        aeq(sf.math2d_perpendicular_segment((0, 0), (0, 0), (0, 0)),
                                  tp([(0, 0), (0, 0)]))
        aeq(sf.math2d_perpendicular_segment((0,0), (1, 1), (0.5, 0.5)),
                                  tp([(0, 1), (1, 0)]))
        aeq(sf.math2d_perpendicular_segment((0,0), (0, 1), (0, 0.5)),
                                  tp([(-0.5, 0.5), (0.5, 0.5)]))
        aeq(sf.math2d_perpendicular_segment((0,0), (1, 0), (0.5, 0)),
                                  tp([(0.5, -0.5), (0.5, 0.5)]))
        aeq(sf.math2d_perpendicular_segment((1, 0.5), (0, 0.5), (0.5, 0.5)),
                                  tp([(0.5, 0), (0.5, 1)]))
        

        # with start point
        aeq(sf.math2d_perpendicular_segment((0,0), (2, 2), (0.5, 0.5)),
                         tp([(-0.5, 1.5), (1.5, -0.5)]))
        aeq(sf.math2d_perpendicular_segment((0,0), (0, 1), (0, 0.25)),
                         tp([(-0.5, 0.25), (0.5, 0.25)]))
        aeq(sf.math2d_perpendicular_segment((0,0), (1, 0), (0.25, 0)),
                         tp([(0.25, -0.5), (0.25, 0.5)]))
#        aeq(sf.math2d_perpendicular_segment((1, 0.5), (0, 0.5)),
#                         tp([(0.5, 1), (0.5, 0)]))
        
        # vertical
        aeq(sf.math2d_perpendicular_segment((0, 0), (0, 1), (0.,0.5)),
                                  tp([(-0.5, 0.5), (0.5, 0.5)]))
        
        # horizontal
        aeq(sf.math2d_perpendicular_segment((-0.5, 0.5), (0.5, 0.5), (0., 0.)),
                                  tp([(0, 0), (0, 1)]))

        aeq(sf.math2d_perpendicular_segment((-0.12615290168030427, 0.19801488833746889), 
                                                              (0.94040262547026343, 0.19801488833746894), 
                                                              (0.40712486189497965, 0.19801488833746889)),
                                  tp([(0.40712486189497959, -0.33526287523781501), 
                                                (0.40712486189497959, 0.73129265191275272)]))

        aeq(sf.math2d_perpendicular_segment((10.905160982291914, 3.6322744099268141), 
                                                              (4.7442000804662703, 3.6325956465404006), 
                                                              (7.8246805313790926, 3.6324350282336075)),
                                  tp([(7.8246805313790926, 0.55179395482661953), (7.8246805313790926, 6.7127548650270086)]))
        
        

    def testIsInteriorPoint(self):
        #bool tklib_is_interior_point(gsl_vector* pt, gsl_matrix* polygon_xy){
        self.assertEqual(sf.math2d_is_interior_point(na.array([0.5, 0.5]), 
                                                  tp([(0.0, 0), (0, 1), 
                                                                (1., 1), (1, 0)])), 
                         True)
        
        self.assertEqual(sf.math2d_is_interior_point((3., 3), 
                                                   tp([(0., 0), (0, 1), 
                                                                 (1., 1), (1, 0)])),
                           False)
        
        self.assertEqual(sf.math2d_is_interior_point((0, 0.), 
                                                   tp([(0., 0), (0, 1), 
                                                                 (1, 1.), (1, 0)])),
                                                   
                           True)

        self.assertEqual(sf.math2d_is_interior_point((0, 0.5),
                                                   tp([(0., 0), (0, 1), 
                                                                 (1, 1), (1, 0)])),
                           True)
        self.assertEqual(sf.math2d_is_interior_point((0.5, 0), 
                                                   tp([(0., 0), (0, 1), 
                                                                 (1, 1.), (1, 0)])),
                           True)


        self.assertEqual(sf.math2d_is_interior_point((0.5, 0.5), 
                                                   tp([(0, 0.), (1, 2), 
                                                                 (2, 0)])),
                           True)
        self.assertEqual(sf.math2d_is_interior_point((0.9, 1.9), 
                                                 tp([(0., 0), (1, 2), 
                                                               (2, 0)])),
                           False)
        #self.assertEqual(sf.math2d_is_interior_point((2, 0.), 
        #                                           tp([(0., 0), (1, 2), (2, 0)])),
        #x                 True)
        
        #self.assertEqual(sf.math2d_is_interior_point((1, 2.), 
        #                                         tp([(0., 0), (1, 2), 
        #                                               (2, 0)])),
        #                 True)
        
        self.assertEqual(sf.math2d_is_interior_point((10., 20), 
                                                 tp([(0., 0), (1, 2), 
                                                               (2, 0)])),
                           False)
        

    def testIntersectSegmentAnalytic(self):
        #gsl_vector* tklib_intersect_line_segment_line(gsl_vector* pt1_seg, gsl_vector* pt2_seg, double m, double b){
        self.assertEqual(sf.math2d_intersect_line_segment_line((1, 0), (0, 0), 0, 0.5),
                         [])
        
        self.assertEqual(sf.math2d_intersect_line_segment_line((0, 0), (1, 0), 0, 0.5),
                         [])

        self.assertEqual(sf.math2d_intersect_line_segment_line((0, 0), (0, 1), 0, 0.5),
                         [0,0.5])


    def testIntersectPolygonAnalytic(self):

        aeq(sf.math2d_intersect_polygon_line_analytic(tp([(0., 0), (1, 0), (1, 1), (0, 1)]),
                                                        1., 0.),
                           tp([(0.0, 0.0), (1.0, 1.0)]))

        #print "c version", sf.math2d_intersect_polygon_line_analytic(tp([(0., 0), (1, 0), (1, 1), (0, 1)]),
        #                                                0, 0.5)
        #print "goal", tp([(1, 0.5), (0, 0.5)])
        
        aeq(sf.math2d_intersect_polygon_line_analytic(tp([(0., 0), (1, 0), (1, 1), (0, 1)]),
                                                        0, 0.5),
                           tp([(1, 0.5), (0, 0.5)]))
        

    def testBetween(self):
        self.assertEqual(sf.math2d_between(1.0, 0.0, 0.5), True)
        self.assertEqual(sf.math2d_between(0.0, 1.0, 0.5), True)


    def testLineEquation(self):
        self.assertEqual(sf.math2d_slope((3, 0), (1, 1)), -0.5)
        self.assertEqual(sf.math2d_line_equation((3, 0), (1, 1)),
                         [-0.5, 1.5])

    def testRotate(self):
        aeq(sf.math2d_rotate((1, 0), 0),
            [1, 0])

        aeq(sf.math2d_rotate((1, 0), math.pi/2),
            [0, 1])

        aeq(sf.math2d_rotate((1, 0), -math.pi/2),
            [0, -1])  

        
    def testIntersectLines(self):
        aeq(sf.math2d_intersect_lines(tp([(0, 0), (1, 1), (2, 3)]),
                                      tp([(0, 1), (1, 0), (2, 0)])),
            tp([(0.5, 0.5)]))

        aeq(sf.math2d_intersect_lines(tp([(0, 0), (1, 1), (2, 3)]),
                                      tp([(0, 1), (1, 0), (2, 0), (1.5, 14)])),
            tp([(0.5, 0.5), (1.8999999999999999, 2.7999999999999998)]))

        aeq(sf.math2d_intersect_lines(tp([(0, 0), (1, 0), (1, 1), (0, 1)]),
                                      tp([(-0.5, 0.5), (1.5, 0.5)])),
            tp([(1, 0.5)]))

        aeq(sf.math2d_intersect_lines(tp([(0, 0), (1, 0), (1, 1), (0, 1),
                                                (0, 0)]),
                                      tp([(-0.5, 0.5), (1.5, 0.5)])),
            tp([(1, 0.5), (0, 0.5)]))

        aeq(sf.math2d_intersect_lines(tp([(0, 0), (1, 1)]),
                                      tp([(3, 0), (1, 1)])),
            tp([(1, 1)]))

        aeq(sf.math2d_intersect_lines(tp([(-0.12, 0.431), 
                                          (0.548, -0.478),
                                          (0.344, 0.249)]),
                                      tp([(-0.12, 0.431),
                                          (0.482, -0.388),
                                          (0.344, 0.249)])),
            tp([(-0.12, 0.431), (0.48205794570672578, -0.38826747402307443),
                (0.344, 0.249)]))

        # because there are two 0,0's on the line.
        # not sure what the correct behavior should be.
        aeq(sf.math2d_intersect_lines(tp([(0, 0), (1, 1), (1, 0), (0, 0)]),
                                      tp([(0, 0), (0, 1)])),
            tp([(0, 0)]))


        # from map/robot corpus. It's sticking the first potin on the end for some reason.
        figure = [(22.8,29.4), (23,29.2), (23.2,29.2), (23.4,29.2), (23.6,29.2), (23.8,29.2), (24,29.2), (24.2,29.2), (24.4,29), (24.6,29), (24.8,29), (25,28.8), (25,28.6), (25,28.4), (25,28.2), (25,28), (25,27.8), (25,27.6), (25,27.4), (25,27.2), (25,27), (25,26.8), (24.8,26.6), (24.8,26.4), (24.8,26.2), (24.8,26), (24.6,25.8), (24.6,25.6), (24.4,25.4), (24.4,25.2), (24.4,25), (24.4,24.8), (24.4,24.6), (24.4,24.4), (24.4,24.2), (24.4,24), (24.4,23.8), (24.4,23.6), (24.4,23.4), (24.4,23.2), (24.4,23), (24.4,22.8), (24.4,22.6), (24.4,22.4), (24.4,22.2), (24.4,22), (24.4,21.8), (24.4,21.6), (24.2,21.4), (24.4,21.2), (24.6,21), (24.8,21), (25,21), (25.2,21), (25.4,21), (25.6,21), (25.8,21), (26,21), (26.2,21), (26.4,21), (26.6,21), (26.8,21), (27,21), (27.2,21.2), (27.4,21), (27.6,21), (27.8,21), (28,20.8), (28.2,20.8), (28.4,20.8), (28.6,20.8), (28.8,20.8), (29,20.6), (29.2,20.6), (29.4,20.6), (29.6,20.6), (29.8,20.6), (30,20.6), (30.2,20.6), (30.4,20.4), (30.6,20.4), (30.8,20.4), (31,20.4), (31.2,20.4), (31.4,20.4), (31.6,20.4), (31.8,20.2), (32,20.2), (32.2,20.2), (32.4,20.2), (32.6,20.2), (32.8,20.2), (33,20.2), (33.2,20.2), (33.4,20), (33.6,20), (33.8,20), (34,20), (34.2,20), (34.4,20), (34.6,20), (34.8,20), (35,20), (35.2,20), (35.4,20), (35.6,20), (35.8,20), (36,20), (36.2,20), (36.4,19.8), (36.6,19.8)]
        ground = [(25.2,20.2), (25.2,22.2), (27.2,22.2), (27.2,20.2)]
        aeq(sf.math2d_intersect_lines(tp(figure), tp(ground)),
            tp([(25.2, 21), (27.2, 21.2)]))
