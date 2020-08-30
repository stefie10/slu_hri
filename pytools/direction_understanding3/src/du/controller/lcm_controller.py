import math
#from pyRobot import *
import lcm
from carmen3d.pose_t import pose_t
from quaternion import Quaternion

class RobotCallback:
    def __init__(self, lc):
        #Robot.__init__(self)
        self.lc = lc 
        self.lc.subscribe("POSE", self.callback)
        
        self.curr_pose_msg = None
        self.has_data = False

    @property
    def position(self):
        if self.curr_pose_msg != None:
            return self.curr_pose_msg[0], self.curr_pose_msg[1]
        else:
            return None

    @property
    def orientation(self):
        if self.curr_pose_msg != None:
            return self.curr_pose_msg[2]
        else:
            return None

    def callback(self, channel, data):
        msg = pose_t.decode(data)
        q = Quaternion(msg.orientation)
        roll, pitch, yaw = q.to_roll_pitch_yaw()
        x, y, z = msg.pos[0:3]
        self.curr_pose_msg = [x, y, z, yaw]
        self.has_data = True


    '''def initialize_pose(self, x, y, theta):
        pt = pyCarmen.carmen_point_t()
        pt.x = x
        pt.y = y
        pt.theta = theta
        stddev = pyCarmen.carmen_point_t()
        stddev.x = 0.2
        stddev.y = 0.2
        stddev.theta = 4.0
        pyCarmen.carmen_localize_initialize_gaussian_command(pt, stddev)'''
        
def main():
    print "carmen"
    robot = RobotCallback().__disown__()


    robot.initialize_pose(5.3, 11.5, 0)
    print "loc"
    loc = pyCarmen.global_pose(robot)
    
    robot.set_goal(15, 12)
    robot.command_go()
    while True:
        pyCarmen.carmen_ipc_sleep(0.1)
        if robot.has_data:
            print "pos", robot.position
            print "orient", math.degrees(robot.orientation)


if __name__=="__main__":
    main()
