from pyRobot import *

class RobotCallback(Robot):
    def __init__(self):
        Robot.__init__(self)
        self.curr_pose_msg = None
        self.has_data = False

    @property
    def position(self):
        if self.curr_pose_msg != None:
            return self.curr_pose_msg.x, self.curr_pose_msg.y
        else:
            return None

    @property
    def orientation(self):
        if self.curr_pose_msg != None:
            return self.curr_pose_msg.theta
        else:
            return None        

    def callback(self, the_type, msg):
        if(the_type == "global_pose"):
            self.curr_pose_msg = msg.globalpos
            self.has_data = True

    def initialize_pose(self, x, y, theta):
        pt = pyCarmen.carmen_point_t()
        pt.x = x
        pt.y = y
        pt.theta = theta
        stddev = pyCarmen.carmen_point_t()
        stddev.x = 0.2
        stddev.y = 0.2
        stddev.theta = 4.0
        pyCarmen.carmen_localize_initialize_gaussian_command(pt, stddev)
        
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

