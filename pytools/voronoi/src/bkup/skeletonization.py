from pyTklib import *
import carmen_maptools
from pylab import *
from sys import argv
from carmen_util import get_euclidean_distance
from sorting import quicksort
from math import atan2
from scipy.ndimage import *
from copy import deepcopy

def skeletonize(binary_map, is_step1):
    new_map = deepcopy(binary_map)
    num_deleted = 0
    for i in range(len(binary_map)):
        for j in range(len(binary_map[0])):

            en = binary_map[i-1:i+2,j-1:j+2]
            if(binary_map[i][j] == 0.0):
                continue
            elif(is_deleted(en, is_step1)):
                num_deleted +=1
                new_map[i,j] = 0.0

    return new_map, num_deleted

def is_deleted(en, is_step1=True):

    if(not len(en) == 3 or not len(en[0]) == 3):
        print "not an eight neighbor"
        exit(1)
    else:
        
        s = sum(en)
        n = num_transitions(en)
        
        if(is_step1):
            p1 = en[0,1]*en[1,2]*en[2,1]
            p2 = en[1,2]*en[2,1]*en[1,0]
        else:
            p1 = en[1,0]*en[0,1]*en[1,2]
            p2 = en[0,1]*en[2,1]*en[1,0]
        
        if(s <= 7 and s >= 3 and n == 1 and p1 == 0 and p2 == 0):
            return True

    return False

def num_transitions(en):
    flat_en = concatenate((en[0,:], en[1:,2], [en[2,1], en[2,0], en[1,0]]))
    
    zero_one_count = 0
    for i in range(len(flat_en)):
        if(flat_en[i-1] == 0 and flat_en[i] == 1):
            zero_one_count += 1
    
    return zero_one_count

    
def make_binary_map(gm):
    binary_map = 1.0*zeros([gm.get_map_height(), gm.get_map_width()])
    I = array(gm.get_free_inds())

    for m in range(len(I[0])):
        i, j = I[:,m]
        binary_map[j][i] = 1.0

    return binary_map

def median_filter(binary_map, filter_size):
    new_map = deepcopy(binary_map)
    
    for i in range(filter_size, len(binary_map)-filter_size):
        for j in range(filter_size, len(binary_map[0])-filter_size):
            neigh = binary_map[i-filter_size:i+filter_size+1,j-filter_size:j+filter_size+1]
            
            v = median(neigh.flatten())
            new_map[i,j] = v

    return new_map

def get_filter(style):
    myfilter = None
    
    if(style == 1):
        myfilter = array([[1.0, 0.0],
                          [1.0, 1.0]])
    elif(style == 2):
        myfilter = array([[0.0, 1.0],
                          [1.0, 1.0]])
    elif(style == 3):
        myfilter = array([[1.0, 1.0],
                          [0.0, 1.0]])
    elif(style == 4):
        myfilter = array([[1.0, 1.0],
                          [1.0, 0.0]])
    return myfilter

def remove_staircases(b_map):
    #curr_map = deepcopy(b_map)
    tmp_map = deepcopy(b_map)

    for k in range(1, 5):
        myfilter = get_filter(k)
        height = len(myfilter)
        width  = len(myfilter[0])
        
        for i in range(1,len(tmp_map)-height-1):
            for j in range(1, len(tmp_map[0])-width-1):
                neigh = tmp_map[i:i+height,j:j+width]
                
                if(sum(neigh*myfilter) == 3):
                    if(k == 1):
                        ic, jc = i+1, j
                    elif(k == 2):
                        ic, jc = i+1, j+1
                    elif(k == 3):
                        ic, jc = i, j+1
                    elif(k == 4):
                        ic, jc = i, j
                    
                    #check this neighborhood for connectivity
                    neigh = deepcopy(tmp_map[ic-1:ic+2,jc-1:jc+2])
                    print "size",  len(neigh), len(neigh[0])
                    neigh[1, 1] = 0.0
                    iscon = is_connected(neigh)
                    
                    if(iscon):
                        tmp_map[ic,jc] = 0.0
    return tmp_map

def is_connected(neigh):
    unreached = get_open_locations(neigh)
    reached = [unreached.pop()]

    while(len(reached) > 0):

        ind = reached.pop()
        tmp_unreached = deepcopy(unreached)
        for i in range(len(unreached)):
            if(sqrt(sum((ind-array(unreached[i]))**2.0)) <= sqrt(2.0)):
                reached.append(unreached[i])
                tmp_unreached.remove(unreached[i])
        unreached = tmp_unreached

    if(len(unreached) > 0.0):
        return False

    return True

def get_open_locations(neigh):
    I = []
    for i in range(len(neigh)):
        for j in range(len(neigh)):
            if(neigh[i][j] == 1.0):
                I.append([i, j])
    return I
    
def find_junction_points(b_map):
    new_map = deepcopy(b_map)

    I = []
    filter_size = 1
    for i in range(filter_size, len(b_map)-filter_size):
        for j in range(filter_size, len(b_map[0])-filter_size):

            if(new_map[i,j] == 0):
                continue
            
            neigh = b_map[i-filter_size:i+filter_size+1,j-filter_size:j+filter_size+1]
            s = sum(neigh)

            i1, i2 = not [j-1, i] in I, not [j-1, i-1] in I
            i3, i4 = not [j, i-1] in I, not [j-1, i+1] in I
            i5, i6 = not [j+1, i] in I, not [j+1, i+1] in I
            i7, i8 = not [j, i+1] in I, not [j+1, i-1] in I
            if(s >= 4 and i1 and i2 and i3 and i4 and i5 and i6 and i7 and i8):
                I.append([j,i])
            else:
                new_map[i,j]=0.0

    return new_map, transpose(I)

def find_end_points(b_map):
    new_map = deepcopy(b_map)

    I = []
    filter_size = 1
    for i in range(filter_size, len(b_map)-filter_size):
        for j in range(filter_size, len(b_map[0])-filter_size):

            if(new_map[i,j] == 0):
                continue
            
            neigh = b_map[i-filter_size:i+filter_size+1,j-filter_size:j+filter_size+1]
            s = sum(neigh)

            if(s == 2):
                I.append([j,i])
            else:
                new_map[i,j]=0.0

    return new_map, transpose(I)

def ind_to_xy(gm, X):
    XY = []
    for i in range(len(X[0])):
        ind = X[0,i], X[1,i]
        xy = gm.to_xy(ind)
        XY.append(xy)

    return transpose(XY)


ion()
def test1(filename, num_iterations):
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map(filename);

    #make a binary map from a gridmap
    b_map = make_binary_map(gridmap)
    
    b_map = median_filter(b_map, 6)
    #imshow(filtered_map, origin=1, cmap=cm.gray)
    #figure()

    for i in range(num_iterations):
        if(i%2 == 0):
            b_map, num_deleted = skeletonize(b_map, True)
        else:
            b_map, num_deleted = skeletonize(b_map, False)
        imshow(b_map, origin=1, cmap=cm.gray)
        if(num_deleted < 2):
            break

    #show the staircase removed map
    figure()
    curr_map  = remove_staircases(b_map)
    imshow(curr_map, origin=1, cmap=cm.gray)
    title("staircases removed")
    
    
    #show the control point map
    figure()
    junction_map, Ij  = find_junction_points(curr_map)
    imshow(junction_map, origin=1, cmap=cm.gray)
    title("junction points")

    figure()
    end_map, Ie  = find_end_points(curr_map)
    imshow(end_map, origin=1, cmap=cm.gray)
    title("end points")

    figure()
    themap = gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    
    XYj = ind_to_xy(gridmap, Ij)
    XYe = ind_to_xy(gridmap, Ie)
    pj, = plot(XYj[0], XYj[1], 'bo')
    pe, = plot(XYe[0], XYe[1], 'g^')
    legend((pj, pe), ("Junction Points","End Points"), shadow=True)
    
    show()




if __name__ == "__main__":
    if(len(argv) == 3):
        test1(argv[1], int(argv[2]))
    else:
        print "usage:\n\t>>python skeleton.py map_filename num_iterations"
