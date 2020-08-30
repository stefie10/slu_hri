import lcm
from carmen3d.navigator_goal_list_t import navigator_goal_list_t
from carmen3d.navigator_goal_msg_t import navigator_goal_msg_t
from carmen3d.point_t import point_t
import time
from math import pi

msg = navigator_goal_list_t()
msg.utime = int(time.time()*1000000)
msg.numWaypoints = 1

g1 = navigator_goal_msg_t()
g1.utime = msg.utime

g1.goal = point_t()
g1.goal.x = 0
g1.goal.y = 1
g1.goal.z = 2
g1.goal.yaw = 0.0
g1.goal.pitch = 0.0
g1.goal.roll = 0.0
g1.velocity = 1.0

g1.yaw_direction = 0
g1.use_theta = False
g1.nonce = 0
g1.sender = navigator_goal_msg_t.SENDER_YOUR_MOM

msg.waypoints = [g1]

msg.sender = navigator_goal_list_t.SENDER_YOUR_MOM
msg.nonce = 0

lcm.LCM().publish("MISSION_PLAN", msg.encode())
