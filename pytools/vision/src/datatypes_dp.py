from sys import argv, exit
import cPickle
from pylab import *
from math import exp
from scipy import *
from random import randint
from copy import deepcopy
from datatypes_lmap import *
import carmen_maptools
from sorting import *

class path_finding_dp_spline:

    def __init__(self, object_name, likelihood_map_spline, 
                 steps=100, rx_in=None, ry_in=None):

        self.object_name = object_name
        self.lmap = likelihood_map_spline
        
        #for i in range(len(self.lmap.free_pts[0,:])):
        #    print i, " -->", self.lmap.free_pts[:,i]

        if(rx_in == None or ry_in == None):
            self.rx, self.ry =  self.lmap.free_pts[:,1179]
        else:
            self.rx, self.ry = rx_in, ry_in

        self.steps = steps
        self.initialize_dp_vars()



    def initialize_dp_vars(self):
        #create the optimal paths up to the current point
        self.paths = zeros([len(self.lmap.free_pts[0,:]), 
                            self.steps], 'i')-1


        #get the index in the new map
        self.dp_prev = zeros(len(self.lmap.free_pts[0,:]))*1.0-10000000000.0

        self.index_hash = {}
        for i in range(len(self.lmap.free_pts[0,:])):
            #print "free pts[0]", self.lmap.free_pts[:,i]
            rx, ry = self.lmap.free_pts[:,i]
            self.index_hash[str([rx, ry])] = i

        m = self.index_hash[str([self.rx, self.ry])]
        self.dp_prev[m] = self.get_val(m)
        #print "initial value", self.dp_prev[m]
        self.paths[:,0] = ones(len(self.lmap.free_pts[0,:]))*m

        #print "seed index", self.im, self.jm
        #create the dp map
        self.dp_curr = zeros(len(self.lmap.free_pts[0,:]))*1.0-10000000000.0


        self.dp_vals = zeros([len(self.lmap.free_pts[0,:]), self.steps+1])*1.0
        self.dp_vals[:,0] = self.dp_prev

    def compute_optimal_path(self):
        for l in range(self.steps):
            print "-----------------------STEP:", l, "------------------------"

            for k in range(len(self.dp_curr)):
                if(self.dp_prev[k] > -10000000000.0):
                    #update it
                    rx,ry = self.fromflattened_index(k)
                    #print "**************UPDATING: ", rx , ry, "**************"               
                    self.dp_update(rx,ry, 0, 0, l)
                    self.dp_update(rx,ry, 0, 1, l)
                    self.dp_update(rx,ry, 0,-1, l)
                    self.dp_update(rx,ry, 1, 0, l)
                    self.dp_update(rx,ry,-1, 0, l)
                    self.dp_update(rx,ry, 1, 1, l)
                    self.dp_update(rx,ry, 1,-1, l)
                    self.dp_update(rx,ry,-1, 1, l)
                    self.dp_update(rx,ry,-1,-1, l)

            #print "curr values", self.dp_curr

            self.dp_prev = self.dp_curr
            self.dp_vals[:,l+1] = self.dp_curr
            self.dp_curr = zeros(len(self.lmap.free_pts[0,:]))*1.0-10000000000.0

        i_best = argmax(self.dp_prev)

        #print "destination", i_best, " --> value=", self.dp_prev[i_best]
        #for i in range(15):
        #    print self.dp_prev[i],
        #print ""
        

        path = self.compute_path(i_best, self.steps-1)
        path.reverse()
        X, Y = [], []

        print path

        for k in path:
            rx, ry = self.fromflattened_index(k)
            X.append(rx)
            Y.append(ry)
        
        return X, Y

    def dp_update(self, rx, ry, v1, v2, curr_step):
        
        #get the updated rx and ry locations
        themap = self.lmap.skeleton.get_map();
        rx_new = rx + v1*themap.resolution;
        ry_new = ry + v2*themap.resolution;
        
        #get the current location
        curr_i = self.toflattened_index(rx, ry)
        next_i = self.toflattened_index(rx_new, ry_new)

        #print "-----------DP Update:--------------"
        #print "curr index:", curr_i
        #print "next index:", next_i

        #if there is nothing to update
        if(next_i == None):
            return
        
        #value of moving to rx_new, ry_new
        if(self.get_val(next_i) < -40.0):
            val = -40.0+self.dp_prev[curr_i]
        else:
            val = self.get_val(next_i)+self.dp_prev[curr_i]

        val_visited = -40.0+self.dp_prev[curr_i]

        #the value of exploring a new place
        #this can be replaced with a cached version
        
        curr_path = self.compute_path(curr_i, curr_step-1)
        #print "curr path", curr_path
        #raw_input()
        
        if(val > self.dp_curr[next_i] 
           and next_i not in curr_path
           and -1 not in curr_path):
            self.paths[next_i,curr_step] = curr_i
            self.dp_curr[next_i] = val
        #the value of revisiting is zero
        #elif(val_visited > self.dp_curr[next_i] 
        #    and next_i in curr_path
        #     and -1 not in curr_path):
        #print "in the second if"
        #    self.paths[next_i,curr_step] = curr_i
        #    self.dp_curr[next_i] = val_visited


    def compute_path(self, k, curr_step):
        mypath = []

        #initialize the path
        j = k;
        mypath.append(j)
 
        #get the rest of the path
        #print "curr_step", curr_step
        for i in range(curr_step+1):
            j = self.paths[j, curr_step-i]
            mypath.append(j)

        return mypath


    def compute_best_paths(self, step, num_paths=None):
        V, I = quicksort(self.dp_vals[:,step])
        
        if(num_paths != None):
            V = V[len(V)-num_paths-1:-1]
            I = I[len(I)-num_paths-1:-1]

        paths = []
        for i in I:
            mypath = self.compute_path(i, step-1)
            xy_path = self.lmap.free_pts.take(mypath, axis=1)
            paths.append(xy_path)

        return V, I, paths

    def get_val(self, m):
        return self.lmap.likelihood_map[self.object_name][m]

    def toflattened_index(self, rx, ry):
        try:
            return self.index_hash[str([rx, ry])]
        except(KeyError):
            return None

    def fromflattened_index(self, k):
        return self.lmap.free_pts[:,k]

