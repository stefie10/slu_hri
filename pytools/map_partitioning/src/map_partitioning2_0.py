from math import *
from carmen_util import *
from spectral_clustering import *
from sys import argv, maxint
from scipy import *
from scipy.misc import *
import carmen_maptools
from carmen_maptools import *
from matplotlib import *
from pylab import *
import numpy
from random import random
from pyTklib import tklib_arctan2

def get_colors():
    colors = []
    for i in arange(0.1, 0.88, 0.05):
        for j in arange(0.1, 0.88, 0.05):
            for k in arange(0.1, 0.88, 0.05):
                colors.append([i, j, k])
    colors.reverse()
    return colors


def partition_map(gridmap, skel, numkmeans=1, 
                  alpha=1.0, numclasses=None, 
                  numsamples=None, seed_number=987):
    success = False
    samples, labels, k = None, None, None
    while(not success):
        try:
            print "getting samples"
            #ion()

            samples = array(get_samples(gridmap, skel, numsamples))

            #plot_map(gridmap.to_probability_map_carmen(), 
            #         gridmap.x_size, gridmap.y_size)
            #plot(samples[0,:], samples[1,:], 'ro')
            #show()
            print "getting graph"
            dists = get_graph(gridmap, samples)
            print "getting weights"
            W = dists2weights_perona(dists, alpha)
            print "doing spectral clustering"
            labels, k = spectral_clustering_W(W,numclasses,numkmeans,seed_number=seed_number)
            success = True
        except(numpy.linalg.linalg.LinAlgError):
            print "linalg error"

    return samples, labels, k, dists


def partition_map_semantic(gridmap, mytagfile, skel, numkmeans=10,
                           alpha=1.0, numclasses=None, numsamples=None, 
                           seed_number=987):
    success = False
    samples, labels, k = None, None, None
    while(not success):
        try:
            print "getting samples"
            #ion()

            #if(len(samples[0]) > 
            if(len(skel.get_skeleton_indices()[0]) > 3000):
                print "setting numsamples=1300"
                numsamples = 1300
            
            
            samples = array(get_samples(gridmap, skel, numsamples))
            print "number of samples", len(samples[0])


            print "getting graph"
            dists = get_graph_semantic(gridmap, mytagfile, samples)

            gray()
            imshow(dists)
            axis('off')
            title("distances")
            
            print "getting weights"
            print "alpha=", alpha
            W = dists2weights_perona(dists, alpha)

            figure()
            gray()
            imshow(W)
            axis('off')
            title("Weights")
            #show()

            print "doing spectral clustering"
            print "numclasses", numclasses, "numkmeans", numkmeans,
            print "seed_number", seed_number
            labels, k = spectral_clustering_W(W,numclasses,numkmeans,seed_number=seed_number)
            success = True
        except(numpy.linalg.linalg.LinAlgError):
            print "linalg error"

    return samples, labels, k, dists

def get_graph(my_gridmap, samples):
    #check this at some point
    adj_graph = zeros([len(samples[0]), len(samples[0])])*1.0-1
    
    i = 0
    for i in range(len(samples[0])):
        #find the angles to the points
        curr_sample = samples[:,i]
        sample_diff = samples - transpose([curr_sample])
        thetas =  tklib_arctan2(sample_diff[1], sample_diff[0]);
        
        #ray trace these values
        dists = array(my_gridmap.ray_trace(curr_sample[0], curr_sample[1], thetas))
        
        #get the true distance based on euclidean distance
        true_dists = array(tklib_get_distance(samples, curr_sample));
        
        #find out which ones are valid
        I, = (true_dists <= dists).nonzero();
        I_longer, = (true_dists > dists).nonzero();

        #take only the values that are less than maxrange
        dists_s = dists.take(I);
        I2, = (dists_s != 30.0).nonzero()
        I = I.take(I2)

        #fill in the adjacency graph
        #make sure we didn't get a max range reading
        for j in I:
            adj_graph[j,i]=true_dists[j]
            adj_graph[i,j]=true_dists[j]
        
        #for j in I_longer:
        #    if(true_dists[j] < 5.0 and random() > 0.9):
        #        adj_graph[j,i]=true_dists[j]**10
        #        adj_graph[i,j]=true_dists[j]**10
      
    return adj_graph


def get_graph_semantic(my_gridmap, mytf, samples):
    #check this at some point
    #print "getting graph"
    #adj_graph = zeros([len(samples[0]), len(samples[0])])*1.0-1
    adj_graph = zeros([len(samples[0]), len(samples[0])])*1.0-1.0


    semantic_vecs = []
    tags = mytf.get_tag_names()
    print "getting visible tags"
    for i in range(len(samples[0])):
        curr_sample = samples[:,i]
        #print "compute_visibility_tag"
        #labels, ilabels = mytf.compute_visibility_tag(curr_sample[0], curr_sample[1])
        labels, ilabels = mytf.get_visible_tags(curr_sample)
        
        vec = []
        for elt in tags:
            if(elt in labels):
                vec.append(1);
            else:
                vec.append(0);

        #print vec
        '''if("refrigerator" in labels or "sink" in labels 
           or "microwave" in labels or "kitchen" in labels 
           or "cup" in labels or "espresso" in labels):
            #print "kitchen obj:", labels, ilabels
            #raw_input()
        elif("railing" in labels):
            print "railing", labels, ilabels
            #raw_input()'''
            
        semantic_vecs.append(vec)

    print "creating graph"
    for i in range(len(samples[0])):
        #find the angles to the points
        curr_sample = samples[:,i]
        sample_diff = samples - transpose([curr_sample])
        thetas =  tklib_arctan2(sample_diff[1], sample_diff[0]);
        
        #ray trace these values
        dists = array(my_gridmap.ray_trace(curr_sample[0], curr_sample[1], thetas))

        #get the true distance based on euclidean distance
        true_dists = array(tklib_get_distance(samples, curr_sample));
        semantic_dists = array(tklib_get_distance(transpose(semantic_vecs)*1.0, array(semantic_vecs[i])*1.0))
        #print semantic_dists 
        #raw_input()

        #find out which ones are valid
        I, = logical_and(true_dists <= dists, true_dists<=5.0).nonzero();
        I_longer, = logical_or(logical_and(true_dists <= dists, 
                                           true_dists>=5.0), true_dists > dists).nonzero();

        #take only the values that are less than maxrange
        dists_s = dists.take(I);
        I2, = (dists_s != 30.0).nonzero()
        I = I.take(I2)

        beta = 0.7
        #fill in the adjacency graph
        #make sure we didn't get a max range reading
        for j in I:
            #exp_fac = (2.0/(sum(semantic_vecs[j])
            #    +sum(semantic_vecs[i])+1.0))*(semantic_dists[j]+1.0001)
            exp_fac = semantic_dists[j]+1.000
            #adj_graph[j,i]=true_dists[j]**(exp_fac)
            #adj_graph[i,j]=true_dists[j]**(exp_fac)
            adj_graph[j,i]=exp_fac*beta + true_dists[j]*(1-beta)
            adj_graph[i,j]=exp_fac*beta + true_dists[j]*(1-beta)
            
        #for j in I_longer:
        #    if(true_dists[j] < 0.45): #and random() > 0.95):
        #        #        #exp_fac = (2.0/(sum(semantic_vecs[j])
        #        #        #     +sum(semantic_vecs[i])+1.0))*(semantic_dists[j]+1.0001)
        #        exp_fac = semantic_dists[j]+1.000
        #        #        #adj_graph[j,i]=(true_dists[j]*10.0)**(exp_fac)
        #        #        #adj_graph[i,j]=(true_dists[j]*10.0)**(exp_fac)
        #        adj_graph[j,i]=(exp_fac*beta+(true_dists[j])*(1-beta))*1.1
        #        adj_graph[i,j]=(exp_fac*beta+(true_dists[j])*(1-beta))*1.1

    print "done creating graph"
    return adj_graph

def get_samples(my_gridmap, skel, count=None):
    I = skel.get_skeleton_indices();
    XY = skel.ind_to_xy(I);

    if(count == None):
        div = 1
    else:
        div = len(XY[0])/count

    pts = []
    done = False; i=0;
    while(not done):
        if(i >= len(XY[0])):
            break
        
        if(my_gridmap.location_free(XY[:,i])):
            pts.append(XY[:,i])
        i+= div

    pts = transpose(pts)
    #print "num_pts:", len(pts[0])

    #for i in range(count):
    #    pt = my_gridmap.get_random_open_location(0.2);
    #    pts[:,i]=pt

    return pts


def show_partitions(gridmap, samples, labels, colors_in=None, show_map=True):
    #plot the samples
    samples = array(samples)

    if(colors_in == None):
        plcolors = get_colors()
    else:
        plcolors = colors_in


    pltypes = ['o','^','<','>','s','d','p','h','x']    
    numclasses = max(labels)+1
    colorNum = 0
    typeNum = 0
    
    myplots = []
    mylabels = []
    for cl in range(numclasses):

        #if(mod(cl, len(pltypes)-1) == 0):
        #    typeNum += 1 

        if(colorNum >= len(plcolors)):
            colorNum = 0
        if(typeNum >= len(pltypes)):
            typeNum = 0
        
        color = plcolors[colorNum]
        ttype = pltypes[typeNum]
        for i in range(len(labels)):
            if(labels[i] == cl):
                #print int(labels[i])
                p1, = plot([samples[0,i]], [samples[1,i]], ttype, mfc=color)
                #plcolors[int(labels[i])])
                
                if(not str(cl) in mylabels):
                    myplots.append(p1)
                    mylabels.append(str(cl))
        colorNum += 1
        typeNum += 1

    legend(myplots, mylabels)
    
    if(show_map):
        themap = gridmap.to_probability_map_carmen()
        carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size,
                                 gridmap.x_offset, gridmap.y_offset);
    
    draw()


def is_visible(pt1, pt2, mymap, epsilon=0.0):
    x, y = pt1
    xp, yp = pt2
    
    #theta = atan2(xp-y, yp-x)
    theta = atan2(yp-y, xp-x)
    
    d, = mymap.ray_trace(x, y, [theta])
    d_elt = sqrt((y-yp)**2.0 + (x-xp)**2.0)
    
    if(d_elt <= d):
        return True
    elif(abs(d-d_elt) < epsilon):
        return True

    return False


def show_explosion(mp, plt=None):
    free_locs, free_inds, index_labels = mp.get_labeled_map()
    gridmap = mp.get_map()    
    occupied_indexes = array(gridmap.get_occupied_inds());
    
    #labels = array(labels)
    #free_locs = array(gridmap.get_free_locations());
    #free_indexes = array(gridmap.get_free_inds());

    
    #get nearest neighbors
    '''index_labels = []
    for i in range(len(free_locs[0])):
        indicies = kNN_index(free_locs[:,i], samples, len(samples[0,:]));
        
        found = False
        for j in indicies:
            #we can see this pt from the current location
            if(is_visible(samples[:,j], free_locs[:,i], gridmap)): 
                #print "adding label", j
                index_labels.append(j);
                found = True
                break

        if(found == False):
            index_labels.append(indicies[0])'''
    
    colors = get_colors()
    free_map = zeros([gridmap.get_map_height(),
                      gridmap.get_map_width(), 3])*1.0+array([0.0,0.0,1.0])
    
    #set the various classes
    for i in range(len(free_inds[0])):
        #curr_class = labels[index_labels[i]]
        curr_class = index_labels[i]
        if(curr_class == -1):
            continue
        ix, iy = free_inds[:,i]
        free_map[iy,ix,:] = array(colors[int(curr_class)])

    for i in range(len(occupied_indexes[0])):
        ix, iy = occupied_indexes[:,i]
        free_map[iy,ix,:] = array([0.0, 0.0, 0.0])
        
    if(plt == None):
        extent = [0 + gridmap.x_offset, gridmap.x_size + gridmap.x_offset,
                  0 + gridmap.y_offset, gridmap.y_size + gridmap.y_offset]        
        imshow(free_map, origin=1, extent=extent)
    else:
        #print "setting data"
        plt.set_data(free_map)


def show_graph(gridmap, samples, labels, colors=None):
    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    dists = get_graph(gridmap, samples)


    for i in range(len(dists[0])):
        for j in range(len(dists[1])):
            if(dists[i,j] > 0):
                plot([samples[0,i], samples[0,j]], [samples[1,i], samples[1,j]], 'k-')
                
    show_partitions(gridmap, samples, labels, colors)                
    draw()

def show_graph_no_map(gridmap, samples, labels, colors=None):
    #themap = gridmap.to_probability_map_carmen()
    #carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    dists = get_graph(gridmap, samples)

    for i in range(len(dists[0])):
        for j in range(len(dists[1])):
            if(dists[i,j] > 0):
                plot([samples[0,i], samples[0,j]], [samples[1,i], samples[1,j]],
                     'k-', linewidth=0.05)
                
    show_partitions(gridmap, samples, labels, colors, show_map=False)                
    draw()

    
'''if(__name__ == "__main__"):
    if(len(argv) == 4):
        #load the gridmap
        gridmap  = tklib_log_gridmap()
        gridmap.load_carmen_map(argv[1])

        num_classes = int(argv[2])
        samples = []
        labels = []

        if(num_classes < 0):
            samples, labels, k = partition_map(gridmap, None, int(argv[3]));            
        else:
            #partition the map
            samples, labels, k = partition_map(gridmap, num_classes, int(argv[3]));

        #show the map
        show_partitions(gridmap, samples, labels)
        show()
    else:
        print "usage:"
        print "\t >>python map_partitioning.py filename numclasses numsamples"'''
    
