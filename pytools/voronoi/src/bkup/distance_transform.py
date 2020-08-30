from pyTklib import *
import carmen_maptools
from pylab import *
from sys import argv
from carmen_util import get_euclidean_distance
from sorting import quicksort
from math import atan2
from scipy.ndimage import *

#1) compute the boundary cells
#2) for each empty cell, compute the distance to all other cells
#3) if its exactly the same distance to two of the other visible cells, its
#      a voronoi cell, otherwise, its not.
#4) plot
def compute_boundary_cells(gm):
    
    boundary = []
    #fill first with nothing
    x_size = gm.get_map_width()
    y_size = gm.get_map_height()

    for i in range(x_size):
        for j in range(y_size):
            if(gm.ind_occupied([i, j])):

                b1 = gm.ind_free([i-1, j])
                b2 = gm.ind_free([i+1, j])
                b3 = gm.ind_free([i, j-1])
                b4 = gm.ind_free([i, j+1])
                b5 = gm.ind_free([i-1, j-1])
                b6 = gm.ind_free([i-1, j+1])
                b7 = gm.ind_free([i+1, j-1])
                b8 = gm.ind_free([i+1, j+1])

                if(b1 or b2 or b3 or b4 or b5 or b6 or b7 or b8):
                    boundary.append([i,j])

    return transpose(boundary)


def ind_to_xy(gm, X):
    XY = []
    for i in range(len(X[0])):
        ind = X[0,i], X[1,i]
        xy = gm.to_xy(ind)
        XY.append(xy)

    return transpose(XY)
        



def compute_distance_transform_skeleton(gm):
    boundary = compute_boundary_cells(gm);

    binary_map = 1.0*zeros([gm.get_map_height(), gm.get_map_width()]) +1.0
    for i in range(len(boundary[0])):
        j, k = boundary[:,i]

        #if(k > 4 and j > 4):
        binary_map[k][j] = 0.0

    distance_map =  distance_transform_bf(binary_map, metric='cityblock');

    medial_map = 1.0*zeros([gm.get_map_height(), gm.get_map_width()])
    for i in range(1, len(distance_map)-1):
        for j in range(1, len(distance_map[0])-1):
            dc = distance_map[i, j]
            d1 = distance_map[i-1, j]
            d2 = distance_map[i+1, j]
            d3 = distance_map[i, j-1]
            d4 = distance_map[i, j+1]

            if(d1 > dc or d2 > dc or d3 > dc or d4 > dc):
                pass
            elif(str(gm.get_value(j, i)) == "nan"):
                pass
            else:
                medial_map[i,j]=1.0

    return medial_map

    


def test1(filename):
    gridmap  = tklib_log_gridmap()
    gridmap.load_carmen_map(filename);
    themap = gridmap.to_probability_map_carmen()
    figure()
    carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);
    #print "starting computation"
    
    #print "number of boundary points", len(bd[0,:])
    bd = compute_boundary_cells(gridmap)
    X, Y = ind_to_xy(gridmap, bd)
    plot(X, Y, 'ro')


    figure()
    vd = compute_distance_transform_skeleton(gridmap)
    imshow(vd, origin=1, cmap=cm.gray)
    show() 


if __name__ == "__main__":
    if(len(argv) == 2):
        test1(argv[1])
    else:
        print "usage:\n\t>>python voronoi.py map_filename"
