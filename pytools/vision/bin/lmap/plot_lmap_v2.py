from sys import argv
import cPickle
from scipy import *
from flickr_plot_likelihood_map_v2 import *
from carmen_maptools import *
from pylab import *

def show_l_map(lmap):
    ion()
    figure()

    mymap = lmap.MAP()
    f_loc = lmap.free_pts

    tkmap = lmap.skeleton.get_map()
    plot_map(tkmap.to_probability_map_carmen(), 
             tkmap.x_size, tkmap.y_size)

    color = ['rx', 'bx', 'gx', 'kx', 'yx', 'mx', 
             'ro', 'bo', 'go', 'ko', 'yo', 'mo']


    cache = {}
    i = 0
    for elt in mymap:
        

        try:
            cache[elt].append(f_loc[:,i])
        except:
            cache[elt] = []
            cache[elt].append(f_loc[:,i])
            
        i+=1


    i=0
    plots = []
    for elt in cache.keys():
        X, Y = transpose(cache[elt])

        pi, = plot(X, Y, color[i])
        plots.append(pi)
        i+=1

    legend(plots, cache.keys(), 3)
    show()

if __name__ == "__main__":
    if(len(argv) == 2):
        
        show_l_map(cPickle.load(open(argv[1], 'r')))
    else:
        print "usage:\n\t python flickr_plot_likelihood_map_v3.py l_map.pck"
