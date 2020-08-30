from pyTklib import noise_model2D, motion_noise_model_slip
from pyTklib import occupancy_grid_mapper
from pyTklib import carmen_util_reading_to_xy, tklib_sse, tklib_normalize_theta
from pyTklib import carmen_util_init_vasco, carmen_util_vasco_scan_match
from matplotlib.widgets import CheckButtons
import carmen_maptools
from pylab import *
from scipy import mod
from pyRobot import *
import pyCarmen
from sys import argv
import pyTklib
from tklib_ipc import tklib_ipc_handler
from scipy import arange

class myRobot(Robot):
    def __init__(self, map_size, init_pose, show_map=False):
        Robot.__init__(self)
        self.mapper = self.initialize_mapper(init_pose, map_size)
        self.init_pose = array(init_pose)
        self.prev_pose = None
        self.current_pose = None
        self.reading_seen = False
        self.show_map=show_map
        carmen_util_init_vasco("sick")

        self.ax = None
        if(show_map):
            ion()
            self.ax = gca()
            self.init_plot()
        
        self.robot_handler = myTklibHandler(self.mapper, self.ax)
        self.i = 0
        
    def initialize_mapper(self, start_pose, map_size):
        mymap = occupancy_grid_mapper(0.8,0.8, 0.5, map_size[0],
                                      map_size[1], 0.2, start_pose, 0.5)
        return mymap

    def callback(self, the_type, msg):
        if(not self.reading_seen and the_type == "front_laser"):
            self.prev_pose = msg["laser_pose"];
            laser_pose = msg["laser_pose"]
            laser_range = msg["range"]
            self.reading_seen = True;
            curr_pose =  carmen_util_vasco_scan_match(laser_pose, laser_range,
                                                      arange(-pi/2.0, pi/2.0+0.0001, pi/180.0), 1)

            self.mapper.update(array(curr_pose)+self.init_pose, laser_range);

        elif(the_type == "front_laser"):
            laser_pose = msg["laser_pose"]
            laser_range = msg["range"]
            diff = array(laser_pose) - self.prev_pose
            diff[2] = tklib_normalize_theta(diff[2])

            #curr_pose = array(laser_pose)+self.init_pose
            curr_pose = self.mapper.get_pose() + diff 
            curr_pose[2] = tklib_normalize_theta(self.prev_pose[2])

            curr_pose =  carmen_util_vasco_scan_match(laser_pose, laser_range,
                                                      arange(-pi/2.0, pi/2.0+0.0001, pi/180.0), 0)

            self.current_pose = array(curr_pose)+self.init_pose
            self.mapper.update(self.current_pose, laser_range);
            self.mapper.map.publish()

            #update the pose and publish it
            self.prev_pose = laser_pose;
            x, y, theta = self.current_pose;
            pyTklib.carmen_publish_gridmapping_pose_message(x, y, theta);
            
            #show the map
            if(self.show_map):
                self.plot_map(self.mapper, self.i)
            self.i+=1

    def init_plot(self):
        #setup the plotting environment
        self.robot_pose_plt, = self.ax.plot([], [], 'bo');
        self.robot_orient_plt, = self.ax.plot([], [], 'k', linewidth=2);
        
    def plot_map(self, mymap, i):
        if(show_map):
            x, y, theta = self.current_pose
            self.robot_pose_plt.set_data([x], [y]);
            self.robot_orient_plt.set_data([x, x+1.5*cos(theta)], [y, y+1.5*sin(theta)]);
            
            if(mod(i,10) == 0):
                curr_map=mymap.map.downsample_map(2)
                carmen_maptools.plot_map(curr_map, mymap.map.x_size, mymap.map.y_size,
                                         cmap="binary", curraxis=self.ax);
                self.ax.images = [self.ax.images[len(self.ax.images)-1]]
            
                draw()

class myTklibHandler(tklib_ipc_handler):
    def __init__(self, themap, theaxis):
        tklib_ipc_handler.__init__(self)
        self.themap = themap
        pyTklib.subscribe_spline_free_request_message(self);
        pyTklib.subscribe_spline_free_response_message(self);
        self.theaxis = theaxis
        self.init_plot()

    def callback(self, the_type, msg):
        if(the_type == "spline_free_request"):
            isfree = self.themap.map.path_free(msg)
            pyTklib.carmen_publish_spline_free_response_message(isfree, 0);
            self.plot(msg)
        
    def init_plot(self):
        if(not self.theaxis == None):
            self.spline_plt, = self.theaxis.plot([], [], 'g')

    def plot(self, spline):
        if(not self.theaxis == None):
            t = arange(0, 1, 0.05);
            X,Y = spline.value(t);
            self.spline_plt.set_data(X, Y);


def run_program(show_map):
    map_size = [100,100]
    init_pose = [map_size[0]/2.0, map_size[1]/2.0, 0]

    #carmen handlers
    robot = myRobot(map_size, init_pose, show_map).__disown__()
    pyCarmen.front_laser(robot)
    
    #other handlers not covered in carmen
    #robot_extras = myTklibHandler()
    #pyTklib.subscribe_spline_free_request_message(robot_extras);
    #pyTklib.subscribe_spline_free_response_message(robot_extras);

    i = 0
    while(1):
        #pyTklib.carmen_publish_spline_free_request_message(pyTklib.SplineC([0, 0, 0], [10, 10, 1], 10.0, 10.0));
        pyTklib.carmen_ipc_sleep(0.05);
        pyCarmen.carmen_ipc_sleep(0.05);

if __name__ == "__main__":
    
    if(len(argv)==2 and argv[1] == "--no-display"):
        show_map = False
    else:
        show_map = True
        
        
    run_program(show_map)



