from pyTklib import *
import carmen_maptools
from pylab import *
from sys import argv
from math import atan2
from copy import deepcopy
from carmen_map_skeletonizer import *


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

def test1(filename, mfilter_width, num_iterations):
    tklib_skeleton = carmen_map_skeletonizer(filename, mfilter_width, num_iterations)
    curr_map = tklib_skeleton.get_skeleton()
    imshow(curr_map, origin=1, cmap=cm.gray)
    title("skeleton with staircases removed")

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
    themap = tklib_skeleton.gridmap.to_probability_map_carmen()
    carmen_maptools.plot_map(themap,
                             tklib_skeleton.gridmap.x_size,
                             tklib_skeleton.gridmap.y_size);
    
    XYj = ind_to_xy(tklib_skeleton.gridmap, Ij)
    XYe = ind_to_xy(tklib_skeleton.gridmap, Ie)
    pj, = plot(XYj[0], XYj[1], 'bo')
    pe, = plot(XYe[0], XYe[1], 'g^')
    legend((pj, pe), ("Junction Points","End Points"), shadow=True)
    
    show()




if __name__ == "__main__":
    if(len(argv) == 4):
        test1(argv[1], int(argv[2]), int(argv[3]))
    else:
        print "usage:\n\t>>python skeleton.py map_filename mfilter_width num_iterations"
