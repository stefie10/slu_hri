from pyRobot import *
import pyCarmen
from corner_extractor import *
from datatypes import point
from carmen_util import rtheta_to_xy

ion()
axis([0, 20, -10, 10])

#class Robot(pyMessageHandler):
class test_robot(Robot):
    def __init__(self):
        Robot.__init__(self)
	fl = pyCarmen.front_laser(self)
        self.range_plt, = plot([], [], 'gx');
        self.my_corner_plt, = plot([], [], 'ro');

        
    def callback(self, the_type, msg):
        #print msg.keys()
        #msg["robot_pose"]
        #msg["range"]
        pts = rtheta_to_xy(point(0, 0, 0), msg["range"])
        corners = corner_extractor(pts, 5, 0.2)
        pts = array(pts)

        X, Y = pts
        print pts
        self.range_plt.set_data(X, Y)
        
        X = pts[0].take(corners);  Y = pts[1].take(corners); 
        self.my_corner_plt.set_data(X, Y)

        
        axis([-5, 15, -10, 10])
        draw()

if __name__=="__main__":

    myrobot = test_robot()


    while(1):
        pyCarmen.carmen_ipc_sleep(0.01)
