from pyTklib import *
from math import pi

def test():


    #gsl_matrix* tklib_rtheta_to_xy(gsl_vector* pose, gsl_vector* reading);
    #gsl_matrix* tklib_xy_to_rtheta(gsl_vector* curr_pose, gsl_matrix* features);
    pts = [[1, 0], [-1, 2]]
    print pts
    rtheta = tklib_xy_to_rtheta([1, 1, pi/2.0], pts);
    print rtheta
    

if __name__=="__main__":
    test()
