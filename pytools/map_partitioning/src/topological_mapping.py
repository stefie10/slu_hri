from carmen_util import *
from pyTklib import occupancy_grid_mapper
from pyTklib import carmen_util_init_vasco, carmen_util_vasco_scan_match
from map_partitioning2_0 import *;
from sys import argv
import pylab
from submap import *
from pylab import *
import psyco
from time import sleep


class spectral_mapping_logfile:
    def __init__(self, infilename, outfilename):
        #initialize vasco
        carmen_util_init_vasco("sick");

        #initialize all this junk
        vals = load_carmen_logfile(infilename)
        self.front_readings, self.rear_readings, self.true_position = vals
        
        #initialize the robot pose
        self.curr_robot_pose = None

        #initialize the current reading number
        self.curr_reading_num_f = 0;
        self.curr_reading_num_r = 0;
        
        #initialize the submaps
        self.curr_submap_number = 0;
        self.curr_submap = self.new_submap()
        self.mygridmaps = [self.curr_submap]

        #initialize the outfile
        self.outfile = open(outfilename, 'w');

    def update_submap(self):
        self.curr_robot_pose = array(self.get_curr_scan_matched_odometry_front())
        
        #update the gridmapper with a new reading
        self.curr_submap.update(self.curr_robot_pose,
                                self.get_curr_front_laser(), -pi/2.0, pi/2.0)

        #self.curr_robot_pose = array(self.get_curr_scan_matched_odometry_rear())
        self.curr_submap.update(self.curr_robot_pose,
                                self.get_curr_rear_laser(), pi/2.0, 3*pi/2.0)
        self.update_reading_nums()
        
        #add a new gridmap is we are not in the current submap
        x, y, theta = self.curr_robot_pose
        if(self.curr_submap.not_in_submap(x,y)):
            self.curr_submap.write_submap(self.outfile, 250)
            self.curr_submap = self.new_submap()
            self.mygridmaps.append(self.curr_submap)
        
    def new_submap(self):
        #update the plotting
        rp = self.get_curr_front_odometry()
        laser_f = self.get_curr_front_laser().tolist()
        laser_r = self.get_curr_rear_laser()
        laser_f.extend(laser_r);

        self.curr_robot_pose = carmen_util_vasco_scan_match(rp, laser_f,
                                                            arange(-pi/2.0,
                                                                   3*pi/2.0+0.0001,pi/180.0), 1)

        #rp = self.get_curr_rear_odometry()
        #laser = self.get_curr_rear_laser()
        #self.curr_robot_pose = carmen_util_vasco_scan_match(rp, laser,
        #                                                    arange(pi/2.0,
        #                                                           3*pi/2.0+0.0001,pi/180.0), 0)
        self.update_reading_nums()
        self.curr_submap_number+=1
        return submap(self.curr_submap_number)


    def get_curr_scan_matched_odometry_front(self):
        rp = self.get_curr_front_odometry()
        front_laser = self.get_curr_front_laser().tolist()
        rear_laser = self.get_curr_rear_laser()
        front_laser.extend(rear_laser)
        cp =  carmen_util_vasco_scan_match(rp, front_laser, 
                                           arange(-pi/2.0,
                                                  3*pi/2.0+0.0001, pi/180.0), 0)
        cp[0]+=20; cp[1]+=20;
        
        return cp

    def get_curr_scan_matched_odometry_rear(self):
        rp = self.get_curr_front_odometry()
        rear_laser = self.get_curr_rear_laser()
        cp =  carmen_util_vasco_scan_match(rp, rear_laser, 
                                           arange(pi/2.0,
                                                  3*pi/2.0+0.0001, pi/180.0), 0)
        cp[0]+=20; cp[1]+=20;

        return cp
    
    def has_more_readings(self):
        if(self.curr_reading_num_f >= min(len(self.front_readings),
                                        len(self.rear_readings))):
            return False
        return True
    
    def get_curr_front_odometry(self):
        return self.front_readings[self.curr_reading_num_f].location.toarray()

    def get_curr_rear_odometry(self):
        return self.rear_readings[self.curr_reading_num_r].location.toarray()

    def get_curr_front_laser(self):
        return array(self.front_readings[self.curr_reading_num_f].data)

    def update_reading_nums(self):
        self.curr_reading_num_f+=1

        while(self.front_readings[self.curr_reading_num_f].timestamp >
              self.rear_readings[self.curr_reading_num_r].timestamp):
            if(self.curr_reading_num_r > min(len(self.front_readings),
                                             len(self.rear_readings))):
                break
            self.curr_reading_num_r+=1;

    def get_curr_rear_laser(self):
        return array(self.rear_readings[self.curr_reading_num_r].data)

#plot the map when necessary
def update_map_plt(hmap, i, outfile, run_now=False, is_prev_map=False, plt=None):
    if(run_now):
        pass
    elif(mod(i, 20)!=0):
        return

    myI = num_as_str(i)
    if(len(hmap.samples) > 0):
        print "update map with explosion"
        themap = hmap.gridmap.map.to_probability_map_carmen()
        show_explosion(hmap.gridmap.map, hmap.samples, hmap.labels, plt);
    else:
        print "update map wo explosion"
        themap = hmap.gridmap.map.to_probability_map_carmen()
        carmen_maptools.plot_map(themap, hmap.gridmap.map.x_size, hmap.gridmap.map.y_size, curr_plt=plt);

    if(run_now == True and is_prev_map==True):
        savefig(outfile + myI + "_part_" + ".eps");
    else:
        savefig(outfile + myI + ".eps");
    #gcf().canvas.blit();
    draw()
    
#run the spectral mapping stuff 
def run_spectral_mapping(infilename, outfilename):
    #initialize the plot
    ion()
    rbt_plt, = plot([20], [20], 'ro');
    rbt_dir_plt, = plot([], [], 'g-');
    rbt_start_plt, = plot([20], [20], 'go');

    #initialize the mapping process
    sm = spectral_mapping_logfile(infilename, outfilename)

    #while there are more readings, we update the submap
    i = 0
    curr_submap_num = 0;
    
    mymap = (zeros([100.0,100.0])*1.0)-1.0
    myim = carmen_maptools.plot_map(ones([1000, 1000])*1.0, 40, 40)


    while(sm.has_more_readings()):
        #update the current submap
        sm.update_submap()

        #plot imdiately
        if(curr_submap_num < sm.curr_submap_number):
            print "new submap made"
            update_map_plt(sm.mygridmaps[len(sm.mygridmaps)-2], i, outfilename, True, True, myim)
            x_st= sm.mygridmaps[len(sm.mygridmaps)-2].poses[0][0]
            y_st= sm.mygridmaps[len(sm.mygridmaps)-2].poses[0][1]
            rbt_start_plt.set_data([x_st], [y_st])
            
            #update the map
            update_map_plt(sm.mygridmaps[len(sm.mygridmaps)-1], i, outfilename, True, False, myim)
            curr_submap_num = sm.curr_submap_number
            
        #do some plotting here
        update_map_plt(sm.curr_submap, i, outfilename, plt=myim)
        if(len(sm.mygridmaps[len(sm.mygridmaps)-1].poses) > 0):
            x_st = sm.mygridmaps[len(sm.mygridmaps)-1].poses[0][0]
            y_st = sm.mygridmaps[len(sm.mygridmaps)-1].poses[0][1]
            rbt_start_plt.set_data([x_st], [y_st])
            
        i+=1
        
        #update the robot pose
        x, y, theta = sm.curr_robot_pose
        rbt_plt.set_data([x, y])
        rbt_dir_plt.set_data([x, x+0.2*cos(theta)],
                             [y, y+0.2*sin(theta)])

        #print "drawing ow"
        axis([0, 40, 0, 40])
        draw()
        
    sm.curr_submap.write_submap(sm.outfile, 300)
    sm.outfile.close()
    
if __name__=="__main__":
    if(len(argv) == 3):
        #import hotshot
        #prof = hotshot.Profile("topo_map");
        infilename = argv[1]
        outfilename = argv[2]
        psyco.full()
        run_spectral_mapping(infilename, outfilename)
        #prof.runcall(run_spectral_mapping, infilename, outfilename)
        #prof.close();
    else:
        print "usage:\n\t>>python topological_mapping.py input_logfile outputfilename"

