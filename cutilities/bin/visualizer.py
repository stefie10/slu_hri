import pyCarmen
from pyRobot import *
from EKF2D import *
from EKF2D_utils import *
from datatypes import *
from tklib_ipc import *
from pyRobot import Robot
from trajopt_utils import *
from threading import Semaphore
from copy import copy
from time import sleep

ion()
robot_plt = plot_robot('r');

class visualizer_robot(Robot):
    def __init__(self):
        self.name = ""
        pyMessageHandler.__init__(self)
        self.curr_odometry = None
        self.curr_laser = None
        self.semaphore = Semaphore();
        
    def initialize_ekf_noise_models(self):
        slip_nm = noise_model2D(-0.0182, -0.1050, 0.0000, 0.0612)
        tv_nm = noise_model2D(1.0065, -0.0072, 0.0932, 0.0000)
        rv_nm = noise_model2D(0.0144, 0.8996, 0.0000, 0.3699)
    
        #make the papa of noise models here 
        nm =  motion_noise_model_slip(tv_nm, rv_nm, slip_nm)
        onm = observation_noise_model(0.3, 0.07, 0.1)
        
        return nm, onm


    def callback(self, the_type, msg):
        self.semaphore.acquire()
        if(the_type == "front_laser"):
            #set the current values
            self.curr_odometry = msg["robot_pose"]
            self.curr_laser = msg["range"]
            
            #plot the odometry
            p = point()
            p.fromarray(self.curr_odometry)
            update_robot(robot_plt, p)
            
        self.semaphore.release()

        x, y, theta = self.curr_odometry
        axis([x-10, x+10, y-10, y+10])
        draw()
        
    def get_odometry(self):
        return self.curr_odometry

dest_plt, = plot([], [], 'y-')
spline_plt, = plot([], [], 'y', linewidth=5)
#this should take a set of destinations and do the planning
#   to subsequent destinations when in the "go" state
class visualizer_tklib(tklib_ipc_handler):
    def __init__(self, robot):
        #Thread.__init__(self)
        self.curr_dests = [[],[]]
        self.robot = robot
        #need to get the classifier and the action space
        tklib_ipc_handler.__init__(self)


    def callback(self, the_type, msg):
        print the_type
        if(the_type == "trajopt_destinations_message"):
            self.set_destinations(array(msg))
        elif(the_type == "curr_spline"):
            print "got spline"
            X, Y = msg.value(arange(0, 1, 0.01));
            spline_plt.set_data(X, Y);

        x, y, theta = self.robot.get_odometry()
        axis([x-10, x+10, y-10, y+10])
        draw()
        
    def set_destinations(self, relative_dests):

        odometry = self.robot.get_odometry();
        R = get_rotation_matrix2D(odometry[2])
        X, Y = dot(R, relative_dests)+transpose([odometry[0:2]])
        dest_plt.set_data(X, Y)
        
        


if __name__ == "__main__":
    #create a robot and subscribe to odometry messages
    myrobot = visualizer_robot()
    odo = pyCarmen.front_laser(myrobot)
    
    #run the planner
    ct = visualizer_tklib(myrobot)
    pyTklib.subscribe_trajopt_destinations_message(ct)
    pyTklib.subscribe_trajopt_curr_spline_message(ct)
    #class subscribe_ekf_message{
    #ct.start()
    
    while(1):
        pyTklib.carmen_ipc_sleep(0.05);
        pyCarmen.carmen_ipc_sleep(0.05);
        sleep(0.05)
