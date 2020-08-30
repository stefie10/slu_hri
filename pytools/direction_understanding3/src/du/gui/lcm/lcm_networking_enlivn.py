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

from du.dir_util import direction_parser_sdc
from du.eval_util import get_topo_to_region_hash
from enlivn.lcmtypes.enlivnlcm import waypoint_list_t, waypoint_t

from tag_util import tag_file

import lcm
import sys
from enlivn.lcmtypes.enlivnlcm import speech_command_t
from enlivn.lcmtypes.enlivnlcm import pose_t


quad_camera_angle = 0
def filter_and_convert_waypoints(m4du, path):
    last_topo = None
    r = []
    for waypoint in path:
        topo, orient = waypoint.split("_")
        if topo != last_topo:
            x, y, z = m4du.tmap_locs_3d[float(topo)].tolist()
            w = waypoint_t()
            w.x = x
            w.y = y
            r.append(w)
        last_topo = topo
    return r

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

        self.lc.subscribe("SPEECH_COMMANDS", self.on_speech_msg)
        self.lc.subscribe("POSE", self.on_pose_msg)
        
        self.cmd = None

    def on_pose_msg(self, channel, data):
        msg = pose_t.decode(data)

        x, y, z = msg.pos
        print "msg", x, y, z
        self.cur_pose = (x, y, z, msg.yaw)

    
    def on_speech_msg(self, channel, data):
        print "got message on", channel
        msg = speech_command_t.decode(data)
        print "msg", msg.uid, msg.command
        self.cmd = msg.command
        
        
    def confirm_path(self):
        print "confirm path"

    def clear_path(self):
        print "clear path"
        
    def publish_waypoints(self, path):
        print "path", path
        msg = waypoint_list_t()

        waypoints = filter_and_convert_waypoints(self.dg_model, path)
        
        breadcrumbs = []
        for w1, w2 in zip(waypoints, waypoints[1:]):
            loc1 = w1.x, w1.y
            loc2 = w2.x, w2.y
            X, Y = self.dg_model.clusters.skel.compute_path(loc1, loc2)
            for x, y in zip(X, Y):
                w = waypoint_t()
                w.x = x
                w.y = y
                breadcrumbs.append(w)
        breadcrumbs = waypoints # turn off breadcrumbs

        num_waypoints = 20.0
        print "started with", len(breadcrumbs)
        step_size = (len(breadcrumbs)/ num_waypoints) + 1
        if step_size == 0:
            step_size = 1
        step_size = int(step_size)
        print 'step size', step_size
        for i in range(0, len(breadcrumbs), step_size):
            msg.waypoints.append(breadcrumbs[i])
            
        msg.num_waypoints = len(msg.waypoints)
        print "sending", msg.num_waypoints
        if msg.num_waypoints <= 1:
            msg.command_type = "stop"
        else:
            msg.command_type = "moveto"
        self.lc.publish("WAYPOINTS", msg.encode())


        

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
