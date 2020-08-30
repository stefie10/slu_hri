from carmen_util import *
from pyTklib import occupancy_grid_mapper
from pyTklib import carmen_util_init_vasco, carmen_util_vasco_scan_match
from map_partitioning2_0 import *;

class submap:
    def __init__(self, vertex_number):
        self.gridmap = occupancy_grid_mapper(0.95, 0.95, 0.5,
                                             40, 40, 0.05,
                                             [20, 20, 0], 0.1)
                                             
        self.vertex_number = vertex_number;
        self.num_clusters = None
        self.label_number = None
        self.labels = []
        self.samples = []
        self.readings = []
        self.poses = []

        
    def update(self, pose_pt, readings, rel_start_angle, rel_end_angle):
        if(rel_start_angle == -pi/2.0):
            self.poses.append(pose_pt)
            self.readings.append(readings)

        print "update reading"
        self.update_reading(pose_pt, readings, rel_start_angle, rel_end_angle);

        if(len(self.readings) > 30
           and mod(len(self.readings),50)==0
           and rel_start_angle == -pi/2.0):
            print "update clusters"
            self.update_clusters()
            
            myI = num_as_str(len(self.readings))
            savefig("cluter"+str(self.vertex_number)+myI+".eps")

            #raw_input()
    
    def update_reading(self, pose_pt, reading, rel_start_angle, rel_end_angle):
        self.gridmap.update(pose_pt, reading, rel_start_angle, rel_end_angle);

    
    def update_clusters(self):
        #do clustering here
        #   to determine clusters
        self.label_number = None;
        self.num_clusters = None;
        
        samples, labels, k = partition_map(self.gridmap.map, None, 500)
        
        self.samples = samples
        self.labels = labels
        self.num_clusters = k
        self.label_number = self.xy_to_label(self.poses[0][0], self.poses[0][1])

    def get_samples(self, num_samples):
        self.labels = array(self.labels)
        free_locs = array(self.gridmap.map.get_free_locations());
        
        #get nearest neighbors
        index_labels = []
        for i in range(len(free_locs[0])):
            curr_index, = kNN_index(free_locs[:,i], self.samples, 1);
            index_labels.append(curr_index);

        grid_labels = self.labels[index_labels]
        
        #get the indices for the open locations
        I, = (array(grid_labels) == self.label_number).nonzero()

        ret_locs = []
        ret_readings = []
        angles = array(arange(0, 2*pi, pi/360.0))
        for i in range(num_samples):
            #get a random entry in the gridcells
            ri = tklib_randint(0, len(I)-1)

            #ray trace the map
            x, y = array(free_locs[:,I[ri]])
            dists = self.gridmap.map.ray_trace(x, y, angles)
            
            #append the right things
            ret_locs.append(free_locs[:,I[ri]])
            ret_readings.append(dists);
            
        return transpose(ret_locs), ret_readings

    def write_submap(self, outfile, num_samples):
        #now sample some number from this set
        # by ray tracing
        poses, readings = self.get_samples(num_samples)
        #print "readings", readings
        
        outfile.write("##################NEW SUBMAP#################");
        for i in range(num_samples):
            outfile.write("TRAIN_SAMPLE")
            outfile.write(" lb:"+str(self.vertex_number))
            outfile.write(" rp:"+str(poses[:,i]))
            outfile.write(" d:"+str(readings[i]))
            outfile.write("\n")
        
    def get_label(self):
        return self.label_number
    
    def xy_to_label(self, x, y):

        if(self.samples == []):
            return -1;
        curr_index, = kNN_index([x, y], self.samples, 1);

        return self.labels[int(curr_index)]

    def not_in_submap(self, x, y):
        curr_label = self.xy_to_label(x, y);
        if(curr_label == -1):
            return False
        
        if(curr_label != self.get_label()):
            return True
        
        return False
