from sys import argv, exit
import cPickle
from pylab import *
from math import exp
from scipy import *
from random import randint
from copy import deepcopy
from create_likelihood_map_v2 import *


class path_finding_dp:

    def __init__(self, likelihood_map, steps=100, im=None, jm=None):
        self.likelihood_map = likelihood_map
        self.lenrow = len(self.likelihood_map)
        self.lencol = len(self.likelihood_map[0])
        self.likelihood_map = self.renormalize_map()
        
        if(im == None or jm == None):
            self.im,self.jm = self.get_starting_location()
        else:
            self.im = im
            self.jm = jm

        self.steps = steps
        self.initialize_dp_vars()


    def initialize_dp_vars(self):
        #create the optimal paths up to the current point
        self.paths = zeros([self.lenrow*self.lencol, self.steps], 'i')-1


        #get the index in the new map
        self.dp_prev = zeros(self.lenrow*self.lencol)*1.0
        m = self.toflattened_index(self.im,self.jm)
        self.dp_prev[m] = self.likelihood_map[self.im,self.jm]
        self.paths[:,0] = ones(self.lenrow*self.lencol)*m

        #print "seed index", self.im, self.jm
        #create the dp map
        self.dp_curr = zeros(self.lenrow*self.lencol)*1.0
        

    def dp_update(self, i, j, v1, v2, curr_step):
        
        #print "<<<<<<<<<<<<<<<< dp_update:", i+v1, i+v2, " >>>>>>>>>>>>>>>>"
        #if we have exceeded our boundaries
        if(i+v1 < 0 or i+v2 < 0 or i+v1 >= self.lenrow or j+v2 >= self.lencol):
            return


        k = self.toflattened_index(i,j)
        val = self.likelihood_map[i,j]+self.dp_prev[k]
        myk = self.toflattened_index(i+v1,j+v2)

        #the value of exploring a new place
        #this can be replaced with a cached version
        curr_path = self.compute_path(k, curr_step-1)
        #print "current path", curr_path

        if(val > self.dp_curr[myk] 
           and self.likelihood_map[i+v1,j+v2] != 0 
           and myk not in curr_path):
            #print "updating:", i+v1, j+v2, " to--> ", val
            self.paths[myk,curr_step] = k
            self.dp_curr[myk] = val
        #the value of revisiting is zero
        elif(self.dp_prev[k] >= self.dp_curr[myk] 
             and myk in curr_path):
            #print "updating2:", i, j, " to-->", self.dp_prev[k]
            self.paths[myk,curr_step] = k
            self.dp_curr[myk] = self.dp_prev[k]


    #checking the paths needs to be fixed

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


    def compute_optimal_path(self):
        for l in range(self.steps):
            print "-----------------------STEP:", l, "------------------------"
            for k in range(len(self.dp_curr)):
                if(self.dp_prev[k] != 0):
                    #update it
                    i,j = self.fromflattened_index(k)
                    #print "**************UPDATING: ", i , j, "**************"                    
                    self.dp_update(i,j,0, 0, l)
                    self.dp_update(i,j, 0, 1, l)
                    self.dp_update(i,j, 0,-1, l)
                    self.dp_update(i,j, 1, 0, l)
                    self.dp_update(i,j,-1, 0, l)

            #print "curr values", self.dp_curr

            self.dp_prev = self.dp_curr
            self.dp_curr = zeros(self.lenrow*self.lencol)*1.0
            
            #raw_input()

        i = argmax(self.dp_prev)
        path = self.compute_path(i, self.steps-1)
        path.reverse()
        X, Y = [], []

        for k in path:
            i, j = self.fromflattened_index(k)
            X.append(i)
            Y.append(j)
        
        return self.dp_prev.reshape([self.lenrow, self.lencol]), X, Y
    
    def get_starting_location(self):
        done = False
        
        while(not done):
            i = randint(0, len(self.likelihood_map)-1);
            j = randint(0, len(self.likelihood_map[0])-1);
            
            if(self.likelihood_map[i,j] != 0):
                done = True
            
        return i, j

    def renormalize_map(self):
        mymin = self.likelihood_map.min()
        for i in range(len(self.likelihood_map)):
            for j in range(len(self.likelihood_map[0])):
                if(self.likelihood_map[i,j] !=0):
                    self.likelihood_map[i,j] -= mymin
        return self.likelihood_map
    

    def toflattened_index(self, i,j):
        return i*self.lencol + j

    def fromflattened_index(self, k):
        i = int(k)/int(self.lencol)
        j = mod(int(k), int(self.lencol))
        
        return i,j
    
def plot_likelihood_map(likelihood_map, steps):
    pd = path_finding_dp(likelihood_map, steps)
    dp_map, X, Y = pd.compute_optimal_path()
    
    title("search for exit")
    gray()
    #imshow(likelihood_map, origin=1)
    dp_map = transpose(dp_map)
    imshow(dp_map, origin=1)
    plot([pd.im],[pd.jm], 'ro');
    plot(X, Y)

    figure()
    
    imshow(transpose(likelihood_map), origin=1)
    plot([pd.im],[pd.jm], 'ro');
    plot(X, Y)
    show()


if __name__== "__main__":
    if(len(argv) ==2):
        plot_likelihood_map(cPickle.load(open(argv[1], 'r')))
    elif(len(argv) ==3):
        plot_likelihood_map(cPickle.load(open(argv[1], 'r')), int(argv[2]))
    else:
        print "usage:\n\tpython find_dp_path.py lmap.pck steps"
