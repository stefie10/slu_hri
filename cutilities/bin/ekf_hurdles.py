import pyCarmen
import pyTklib
from pyRobot import *
from sys import *
from EKF2D import *
from datatypes import *
from datatypes import point
from pylab import *
from gaussian import normal_get_ellipse

class ekf_robot(Robot):
    def __init__(self, filename, show_gui=True):
        #load the logfile and get the relevant EKF
        #policies, problem, myEKF = load_problem_with_EKF(filename)
        trajopt = carmen_util_load_pck(filename)
        self.myEKF = trajopt.get_ekf(point(0,0,0))
        
        #open up a robot and subscribe to front_laser messages
        Robot.__init__(self)
        fl = pyCarmen.front_laser(self)

        #initialize pyTklib message passing to allow
        #  ekf messages to be published
        pyTklib.carmen_ipc_initialize(1, ["python"])


        #initialize relevant state
        self.prev_odo = None
        self.prev_timestamp = maxint
        self.last_message_timestamp = maxint
        self.dt = 0.1

        self.show_gui = show_gui


        if(show_gui):
            self.init_plot()

    def callback(self, the_type, msg):
        if(the_type == "front_laser"):
            if((msg["timestamp"]-self.last_message_timestamp) < 0.01):
                self.last_message_timestamp = msg["timestamp"]
                return
            self.last_message_timestamp = msg["timestamp"]

            curr_odo = point(msg["robot_pose"][0], msg["robot_pose"][1], msg["robot_pose"][2])
            curr_laser = msg["range"]
            curr_timestamp = msg["timestamp"]
            if(not self.prev_timestamp == maxint):
                self.dt = curr_timestamp - self.prev_timestamp
                self.update_ekf(self.prev_timestamp, self.prev_odo,
                                curr_timestamp, curr_odo, curr_laser)
            self.prev_timestamp = curr_timestamp
            self.prev_odo = curr_odo

        

    def update_ekf(self, prev_timestamp, prev_odo, curr_timestamp, curr_odo, curr_laser):
        if(self.myEKF==None):
            return

        #use the odometry to get the relative motion
        motion = get_robot_motion(prev_odo, curr_odo, curr_timestamp-prev_timestamp);
        
        #update the EKF
        self.myEKF.motion_update(motion)

        #create the laser reading
        #get the laser reading and project it using the mapped position
        reading = laser_message(curr_timestamp, curr_laser)
        curr_location = self.myEKF.getposePt()
        X, Y = get_laser_reading_robot_frame(curr_location, reading)

        #extrace the hurdles
        features = hurdles_extract_optimized(array([X,Y]), 0.2413, 0.03, 1.2, 1.2, 7.0, 15)

        #convert to R/Theta coordinates
        R, TH =  globalXY_to_r_theta(curr_location, features);
        Sig = zeros(len(R))*1.0

        #update the EKF
        self.myEKF.measurement_updateC(array([R, TH, Sig]), 50.0)
        pyTklib.carmen_publish_ekf_message(self.myEKF.U, self.myEKF.SIGMA);

        if(self.show_gui):
            self.update_plot(features)

        

    def init_plot(self):
        ion()
        self.robot_dir_plt, = plot([], [], 'k', linewidth=3);
        self.robot_plt, = plot([], [], 'bo', markersize=10);
        self.features_plt, = plot([], [], 'ro', markersize=13);
        self.curr_features_plt, = plot([], [], 'go', markersize=9);

        self.uncertainty_plts = []
                        
        axis([-10, 10, -10, 10])


    def update_plot(self, curr_observations):
        robot_curr_pose = self.myEKF.getpose()
        
        self.robot_plt.set_data([0], [0])
        self.robot_dir_plt.set_data([0, 0.5*cos(robot_curr_pose[2])], [0, 0.5*sin(robot_curr_pose[2])])

        feat = self.myEKF.getfeatures()
        if(not len(feat) == 0):
            X, Y, SIG = feat
            self.features_plt.set_data(X-robot_curr_pose[0], Y-robot_curr_pose[1])
            
            ##############################
            #do the uncertainty plots
            #############################
            for i in range(len(feat[0])-len(self.uncertainty_plts)):
                new_plt, = plot([], [], 'k', linewidth=3);
                self.uncertainty_plts.append(new_plt)
            feat_cov = self.myEKF.getfeatures_covariance()

            for i in range(len(feat_cov)):
                X, Y = normal_get_ellipse(feat_cov[i][0:2,0:2], feat[:,i][0:2]-robot_curr_pose[0:2]);
                self.uncertainty_plts[i].set_data(X, Y)

        
        if(len(curr_observations) > 0):
            X, Y = curr_observations
            self.curr_features_plt.set_data(X-robot_curr_pose[0], Y-robot_curr_pose[1]);
        else:
            self.curr_features_plt.set_data([], []);
        
        axis([-10, 10, -10, 10])
        draw()
    
if __name__=="__main__":
    if(len(argv) == 2):
        infilename = argv[1]
        
        myrobot = ekf_robot(infilename)
        
        while(1):
            pyCarmen.carmen_ipc_sleep(0.05);
            pyTklib.carmen_ipc_sleep(0.05);

    else:
        print "usage: >> python ekf_hurdles.py psdpfilename.out [mapfilename]"

    
