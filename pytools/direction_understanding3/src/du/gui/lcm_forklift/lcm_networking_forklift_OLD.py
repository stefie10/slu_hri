"""
Listens for natural language directions on the LCM channel DIRECTION_INPUT.
Also receives information about robot pose and GPS to local transformation from forklift sim
via the channels POSE and GPS_TO_LOCAL respectively

The direction are run through the code to generate a list of waypoints (XY and RNDF IDs).

These waypoints are then published on the NAV_GOAL_LIST and NAVIGATOR_PLAN channels, 
with the hope that the agile code will command the forklift
to follow that list of waypoints.
"""

from arlcm.comment_t import comment_t
from arlcm.waypoint_list_t import waypoint_list_t
from arlcm.waypoint_t import waypoint_t
from arlcm.navigator_plan_t import navigator_plan_t
from arlcm.waypoint_id_t import waypoint_id_t
from arlcm.gps_to_local_t import gps_to_local_t
from botlcm.pose_t import pose_t

from du.dir_util import direction_parser_sdc
from du.eval_util import get_topo_to_region_hash
from tag_util import tag_file

import cPickle
import lcm
import sys
import time
import math
import socket
import select
import du.rndf_util as ru

class App:
    def __init__(self, m4du, rndf_file):
        self.lc = lcm.LCM()

        #load the model
        print "Loading model..."
        self.dg_model = cPickle.load(open(m4du, 'r'))
        self.rndf = ru.rndf(rndf_file, True)
        self.sdc_parser = direction_parser_sdc()

        self.trans_xyz = (0, 0, 0)
        self.trans_latlon = self.rndf.origin
        self.trans_theta = 0

        self.run_inference = True
        self.waypoints = []
        self.cmd = None

        self.curr_location = None
        self.curr_orientation = None

        # Change these two for testing; to be replaced by LCM message
        #self.curr_location = (0, 0, 0)
        #self.cmd = str("Go to the truck")

        self.lc.subscribe("DIRECTION_INPUT", self.on_comment_msg)
        self.lc.subscribe("POSE", self.on_pose_msg)
        self.lc.subscribe("GPS_TO_LOCAL", self.on_transform_msg)
    
    def socketActivated(self):
        self.lc.handle()
        if self.cmd != None:
            self.publish_waypoints()
            self.cmd = None

    def on_transform_msg(self, channel, data):
        #print 'got trans'
        msg = gps_to_local_t.decode(data)
        self.trans_xyz = msg.local
        self.trans_latlon = (msg.lat_lon_el_theta[0], msg.lat_lon_el_theta[1])
        self.trans_theta = msg.lat_lon_el_theta[3]
        
    def on_comment_msg(self, channel, data):
        msg = comment_t.decode(data)
        self.cmd = msg.comment.strip()
        self.run_inference = True
        print "received: [%s]" % self.cmd 

    def on_pose_msg(self, channel, data):
        
        msg = pose_t.decode(data)
        x, y, z = msg.pos[0:3]
        self.curr_location = self.robot_pose_to_rndf((x, y, z))

        #compute orientation in rndf frame
        o_vec = self.bot_quat_rotate(msg.orientation, (1,0,0))
        robot_orientation = math.atan2(o_vec[1], o_vec[0])
        self.curr_orientation = robot_orientation + self.trans_theta
        #print 'orientation:', self.curr_orientation

    def robot_pose_to_rndf(self, xyz):
        th = self.trans_theta
        sec2th = 1.0 / math.cos(2*th)

        #unrotate robot coordinate frame
        dx = -sec2th*((self.trans_xyz[0]-xyz[0])*math.cos(th) + (-self.trans_xyz[1] + xyz[1])*math.sin(th))
        dy = -sec2th*((self.trans_xyz[1]-xyz[1])*math.cos(th) + (-self.trans_xyz[0] + xyz[0])*math.sin(th))

        lat, lon = ru.xy_to_latlon(dx, dy, self.trans_latlon)

        rndf_x, rndf_y = ru.latlon_to_xy(lat, lon, self.rndf.origin)
        rndf_z = xyz[2] - self.trans_xyz[2]

        return (rndf_x, rndf_y, rndf_z)
        
    def rndf_pose_to_robot(self, xyz):
        th = self.trans_theta
        lat, lon = ru.xy_to_latlon(xyz[0], xyz[1], self.rndf.origin)
        dx, dy = ru.latlon_to_xy(lat, lon, self.trans_latlon)

        robot_x = dx * math.cos(th) + dy * math.sin(th) + self.trans_xyz[0]
        robot_y = dx * math.sin(th) + dy * math.cos(th) + self.trans_xyz[1]
        robot_z = xyz[2] + self.trans_xyz[2]

        return (robot_x, robot_y, robot_z)

    def bot_quat_rotate(self, rot, v):
        ab  =  rot[0]*rot[1]
        ac  =  rot[0]*rot[2]
        ad  =  rot[0]*rot[3]

        nbb = -rot[1]*rot[1]
        bc  =  rot[1]*rot[2]
        bd  =  rot[1]*rot[3]

        ncc = -rot[2]*rot[2]
        cd  =  rot[2]*rot[3]
        ndd = -rot[3]*rot[3]

        result = (
        2*( (ncc + ndd)*v[0] + (bc -  ad)*v[1] + (ac + bd)*v[2] ) + v[0],
        2*( (ad +  bc)*v[0] + (nbb + ndd)*v[1] + (cd - ab)*v[2] ) + v[1],
        2*( (bd -  ac)*v[0] + (ab +  cd)*v[1] + (nbb + ncc)*v[2] ) + v[2])

        return result

    def dist_to_line(self, point, seg1, seg2):
        #computes distance from point to the line segment through seg1 and seg2
        x0, y0 = point
        x1, y1 = seg1
        x2, y2 = seg2

        num = abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1))
        denom = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        dist = num/denom
        return dist

        
    def publish_waypoints(self):
        if self.cmd == None:
            return

        if self.run_inference:
            keywords = self.sdc_parser.extract_SDCs(self.cmd)
            path, lprob, sdc_eval = self.dg_model.infer_path(keywords, self.curr_location[0:2], [self.curr_orientation])       

            self.waypoints = []
            for myreg in path:
                topo, orient = myreg.split("_")

                p_xy = self.dg_model.tmap_locs[float(topo)]
                r_xy = self.rndf_pose_to_robot((p_xy[0], p_xy[1],0))
                self.waypoints.append((p_xy[0], p_xy[1]))
            #eliminate duplicates
            unique_wpts = []
            for wp in self.waypoints:
                if not wp in unique_wpts:
                    unique_wpts.append(wp)
            self.waypoints = unique_wpts[:]
            
            #gets rndf transition ids
            self.transitions = ru.xy_path_to_waypoints(self.waypoints, self.rndf)
            '''
            for exit_pair in self.transitions:
                for idstr in exit_pair:
                    rndf_pt = self.rndf.get_object_by_id(idstr)
                    pt = ru.latlon_to_xy(rndf_pt.lat, rndf_pt.lon, self.rndf.origin)
                    
                    min_dist = float('inf')
                    min_idx = -1
                    for i in range(len(self.waypoints)-1):
                        s1 = self.waypoints[i]
                        s2 = self.waypoints[i+1]
                        #d1 = math.hypot(pt[0]-s1[0], pt[1]-s1[1])
                        #d2 = math.hypot(pt[0]-s2[0], pt[1]-s2[1])
                        d = self.dist_to_line(pt, s1, s2)
                        if d < min_dist:
                            min_dist = d
                            min_idx = i+1
                    #check if it belongs at beginning or end
                    if math.hypot(pt[0] - self.curr_location[0], pt[1] - self.curr_location[1]) < min_dist:
                        min_idx = 0
                    if math.hypot(pt[0] - self.waypoints[-1][0], pt[1] - self.waypoints[-1][1]) < min_dist:
                        min_idx = len(self.waypoints)
                    self.waypoints.insert(min_idx, pt)
            '''
            self.run_inference = False

        

        #find current checkpoint
        dist = [math.hypot(self.curr_location[0] - x, self.curr_location[1] - y) for x,y in self.waypoints]
        idx = dist.index(min(dist))
        remaining_path = self.waypoints[idx:]
        remaining_trans = ru.xy_path_to_waypoints(remaining_path, self.rndf)
        
        if len(remaining_trans) and remaining_trans[0] in self.transitions:
            self.chkpoint = self.transitions.index(remaining_trans[0])
        else:
            self.chkpoint = 0
        
        #print "transitions: ", self.transitions
        
        msg = waypoint_list_t()
        msg.utime = int(time.time() * 1000000)
        msg.numWaypoints = len(self.waypoints)
        msg.waypoints = []

        for k in range(msg.numWaypoints):

            wp = self.waypoints[k]

            w1 = waypoint_t()
            w1.utime = msg.utime

            w1.id = k
            robot_xy = self.rndf_pose_to_robot((wp[0], wp[1], 0))
            w1.x = robot_xy[0]
            w1.y = robot_xy[1]
 
            print "Waypoint (%6.2f, %6.2f)" % (wp[0], wp[1])
            
            assert w1.x < 1e200 and w1.y < 1e200 and \
                   w1.x > -1e200 and w1.y > -1e200

            msg.waypoints.append(w1)

        #print "Publishing NAV_GOAL_LIST.  goal (%6.2f, %6.2f)" % (msg.waypoints[-1].x, msg.waypoints[-1].y)

        self.lc.publish("NAV_GOAL_LIST", msg.encode())

        msgt = navigator_plan_t()
        msgt.utime = int(time.time() * 1000000)
        msgt.num_waypoints = len(self.transitions)
        msgt.waypoints = []
        
        if len(self.transitions):
            for k in range(msgt.num_waypoints):
                for i in range(1):
                    wp_id = self.transitions[k][i].split(".")

                    w1 = waypoint_id_t()
                
                    w1.segment = int(wp_id[0])
                    w1.lane    = int(wp_id[1])
                    w1.point   = int(wp_id[2])

                    print "Waypoint_ID (%d, %d, %d)" % (w1.segment, w1.lane, w1.lane)

                    msgt.waypoints.append(w1)

        msgt.checkpoint_index = self.chkpoint
        msgt.checkpoints_remaining = msgt.num_waypoints - self.chkpoint
        
        #print "Publishing NAV_GOAL_PLAN_LIST.  goal (%d.%d.%d)" % (msgt.waypoints[-1].segment, msgt.waypoints[-1].lane, msgt.waypoints[-1].point)

        self.lc.publish("NAVIGATOR_GOAL_PLAN_LIST", msgt.encode())

        print "location:", self.rndf_pose_to_robot(self.curr_location)
        print "orientation:", self.curr_orientation
        print "path:", [(wp.x,wp.y) for wp in msg.waypoints]
        print "checkpoints:", self.transitions
        
    def run(self):
        print "Waiting for command"
        old_time = time.time()
        while True:
            if len(select.select([self.lc],[],[],0.01)[0]):
                self.lc.handle()
            
            #publish waypoint every 0.5 seconds
            curr_time = time.time()
            if curr_time > old_time + 0.5:
                self.publish_waypoints()
                old_time = curr_time                                  

if __name__ == "__main__":
    if(len(sys.argv) == 3):
        app = App(sys.argv[1], sys.argv[2])
        app.run()
    else:
        print "usage:\n\tpython lcm_networking.py model_filename.pck rndf_modelname.rndf"
