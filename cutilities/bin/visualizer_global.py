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


ion()
robot_plt = plot_robot('r');

class visualizer_robot(Robot):
    def __init__(self):
        self.name = ""
        pyMessageHandler.__init__(self)
        self.true_pose = None
        self.semaphore = Semaphore();
        
    def callback(self, the_type, msg):
        self.semaphore.acquire()
        if(the_type == "sim_global_pose"):

            self.true_pose = msg["truepose"]
            #plot the odometry
            p = point()
            p.fromarray(self.true_pose)
            update_robot(robot_plt, p)
        self.semaphore.release()

        x, y, theta = self.true_pose
        axis([x-10, x+10, y-10, y+10])
        draw()

    def get_true_pose(self):
        return self.true_pose

dest_plt, = plot([], [], 'r-')
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
            X, Y = msg.value(arange(0, 1, 0.01));
            spline_plt.set_data(X, Y);
        
        x, y, theta = self.robot.get_true_pose()
        print "robot pose", x, y, theta
        axis([x-10, x+10, y-10, y+10])
        draw()
        
    def set_destinations(self, true_dests):
        self.curr_dests = array(true_dests)
        X, Y = true_dests
        dest_plt.set_data(X, Y)
        print X, Y
        

if __name__ == "__main__":
    #create a robot and subscribe to odometry messages
    myrobot = visualizer_robot()
    truepos = pyCarmen.sim_global_pose(myrobot)    

    #run the planner
    ct = visualizer_tklib(myrobot)
    pyTklib.subscribe_trajopt_destinations_message(ct)
    pyTklib.subscribe_trajopt_curr_spline_message(ct)

    #class subscribe_ekf_message{
    #ct.start()
    
    while(1):
        pyTklib.carmen_ipc_sleep(0.01);
        pyCarmen.carmen_ipc_sleep(0.01);
