from datatypes import *
from trajopt_utils import *
from EKF2D_utils import *
from math import pi

def test_noise_models1():
    prev_pose = [0, 0, 0]

    print "Running test 1"
    for dr in range(10):
        for dth in arange(-pi, pi, 0.1):
            dt = 1.0
            mnm, onm = initialize_sim_noise_models()
            loc1 = mnm.update_mean_copy(prev_pose, dr, dth);
    
            motion = robot2D_encoders(dr, dth, dt);
            loc2 = get_relative_motion(point(prev_pose[0],
                                             prev_pose[1], prev_pose[2]), motion)


            print "*******************************"
            print "prev_pose", prev_pose
            print "loc1:", loc1
            print "loc2:", loc2

            raw_input()

def test_noise_models2():
    mnm, onm = initialize_sim_noise_models()
    
    #set some constants
    prev_pose = [0, 0, 0]
    
    #set the test parameters
    dr = [1.0, 0.0, 1.0]
    dth = [0.0, pi/2.0, pi/2.0]
    

    for i in range(len(dr)):
        print "*******************************"
        loc1 = mnm.update_mean_copy(prev_pose, dr[i], dth[i]);
        print "dr:", dr[i], " dth:", dth[i]
        print "prev_pose", prev_pose
        print "loc1:", loc1


if __name__ == "__main__":
    test_noise_models2()
