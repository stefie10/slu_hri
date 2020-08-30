"""
Listens for natural language directions on the LCM channel EMAIL.

As directions are received on this channel, they are run through
the direction understanding code to generate a list of waypoints.

These waypoints are then published on the NAV_GOAL_LIST channel, 
with the hopes that a mission planner (e.g., carmen3d execute_path)
process will command the robot to follow that list of waypoints.

This script is designed specifically for use with the mav@virgo.csail.mit.edu
account, developed for an IROS 2010 submission.
"""

from carmen3d.navigator_goal_list_t import navigator_goal_list_t
from carmen3d.navigator_goal_msg_t import navigator_goal_msg_t
from carmen3d.mission_control_msg_t import mission_control_msg_t
from carmen3d.point_t import point_t
from carmen3d.pose_t import pose_t
from du.dir_util import direction_parser_sdc
from du.eval_util import get_topo_to_region_hash
from quaternion import Quaternion
from scipy import radians
from tag_util import tag_file
from pyTklib import tklib_normalize_theta
import email
import lcm
import sys
import time
import math

quad_camera_angle = 0

class App:
    def __init__(self, m4du, region_tagfile, map_filename):
        self.lc = lcm.LCM()

        #load the model
        print "Loading model..."
        self.dg_model = m4du
        self.sdc_parser = direction_parser_sdc()

    #    for k1 in dg_model.tmap.keys():
    #        print "===="
    #        for k2 in dg_model.tmap[k1]:
    #            print k2
    #            print dg_model.tmap_locs[k1]
    #            print dg_model.tmap_locs[k2]

        #get the topo_to_region_hash
        self.dataset_name = region_tagfile.split("/")[-1].split("_")[0]
        tf_region = tag_file(region_tagfile, map_filename)
        self.topo_to_region = get_topo_to_region_hash(tf_region, self.dg_model)
        
        self.waypoints = []
        self.cur_pose = None

        self.lc.subscribe("EMAIL", self.on_email_msg)
        self.lc.subscribe("POSE", self.on_pose_msg)
        
        self.cmd = None

    def on_pose_msg(self, channel, data):
        msg = pose_t.decode(data)
        q = Quaternion(msg.orientation)
        roll, pitch, yaw = q.to_roll_pitch_yaw()
        x, y, z = msg.pos[0:3]
        yaw = tklib_normalize_theta(yaw + quad_camera_angle)
        self.cur_pose = (x, y, z, yaw)

    
    def on_email_msg(self, channel, data):
        msg = email.message_from_string(data)
        self.cmd = msg.get_payload().strip()
        print "received: [%s]" % self.cmd
        
    def confirm_path(self):
        print "confirm path"
        msg = mission_control_msg_t()
        msg.utime = int(time.time()*1000000)
        msg.type = mission_control_msg_t.NAVIGATOR_GO
        msg.value_1 = 0
        msg.value_2 = 0
        self.lc.publish("MISSION_CONTROL", msg.encode())

    def clear_path(self):
        print "clear path"
        print "confirm path"
        msg = mission_control_msg_t()
        msg.utime = int(time.time()*1000000)
        msg.type = mission_control_msg_t.NAVIGATOR_CLEAR_GOAL
        msg.value_1 = 0
        msg.value_2 = 0
        self.lc.publish("MISSION_CONTROL", msg.encode())
        
    def publish_waypoints(self, path):
        self.waypoints = []
        for myreg in path:
            topo, orient = myreg.split("_")

            p_xyz = self.dg_model.tmap_locs_3d[float(topo)].tolist()
            p_theta = radians(float(orient))
            if len(p_xyz) == 3:
                self.waypoints.append((p_xyz[0], p_xyz[1], p_xyz[2], p_theta))
            else:
                self.waypoints.append((p_xyz[0], p_xyz[1], 1.6, p_theta))
        print "waypoints: ", self.waypoints

        print "set goal to:", self.waypoints[-1]

        msg = navigator_goal_list_t()
        msg.utime = int(time.time()*1000000)
        msg.numWaypoints = len(self.waypoints)
        msg.waypoints = []
        msg.sender = navigator_goal_list_t.SENDER_YOUR_MOM
        msg.nonce = 0

        for k in range(msg.numWaypoints):

            wp = self.waypoints[k]

            g1 = navigator_goal_msg_t()
            g1.utime = msg.utime

            g1.goal = point_t()
            g1.goal.x = wp[0]
            g1.goal.y = wp[1]
            g1.goal.z = wp[2]
            g1.goal.yaw = tklib_normalize_theta(wp[3] - quad_camera_angle)
            g1.goal.pitch = 0.0
            g1.goal.roll = 0.0
            g1.velocity = 1.0
            
            assert g1.goal.x < 1e200 and g1.goal.y < 1e200 and \
                   g1.goal.x > -1e200 and g1.goal.y > -1e200

            g1.yaw_direction = 0
            g1.use_theta = False
            g1.nonce = 0
            g1.sender = navigator_goal_msg_t.SENDER_YOUR_MOM

            msg.waypoints.append(g1)

        print "Publishing NAV_GOAL_LIST.  goal (%6.2f, %6.2f, %6.2f)" % (msg.waypoints[-1].goal.x,
                                                        msg.waypoints[-1].goal.y, 
                                                        msg.waypoints[-1].goal.yaw)

        self.lc.publish("NAV_GOAL_LIST", msg.encode())
        print "G",

    def run(self):
        print "Waiting for command"
        while True:
            self.lc.handle()
        
            
if __name__ == "__main__":
    if(len(sys.argv) == 4):
        app = App(sys.argv[1], sys.argv[2], sys.argv[3])
        app.run()
    else:
        print "usage:\n\tpython run_carmen.py model_filename.pck gtruth_tag_file"
