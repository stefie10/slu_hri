from sys import argv, exit
import cPickle
from pylab import *
from math import exp
from scipy import *

def plot_likelihood_map(likelihood_map, min_valid_value=0.0):
    vmin = likelihood_map.min()

    if(vmin >= 0):
        print "error vmin not < 0"
        exit(1);

    for i in range(len(likelihood_map)):
        for j in range(len(likelihood_map[0])):
            if(likelihood_map[i][j] == 0):
                likelihood_map[i][j] = vmin

    likelihood_map = transpose(likelihood_map)
    
    vmax = likelihood_map.max()
    vmin = likelihood_map.min()
    
    #normalize the values to be of length 1
    for i in range(len(likelihood_map)):
        for j in range(len(likelihood_map[0])):
            likelihood_map[i][j] = (likelihood_map[i][j]/abs(vmax-vmin))
    
    #normalize them between 0 and 1
    vmin = likelihood_map.min()
    likelihood_map -= vmin

    for i in range(len(likelihood_map)):
        for j in range(len(likelihood_map[0])):
            if(likelihood_map[i][j] < min_valid_value):
                likelihood_map[i][j] = min_valid_value

    #I = []
    #for i in range(len(likelihood_map)):
    #    for j in range(len(likelihood_map[0])):
    #        if(likelihood_map[i][j] > min_valid_value):
    #            I.append([i,j])
    #I = transpose(I)
    #plot(I[1], I[0], 'ro')

    print likelihood_map.max()
    print likelihood_map.min()
    
    title("search for exit")
    gray()
    imshow(likelihood_map, origin=1)
    show()


if __name__== "__main__":

    if(len(argv) ==2):
        plot_likelihood_map(cPickle.load(open(argv[1], 'r')))
    elif(len(argv) ==3):
        plot_likelihood_map(cPickle.load(open(argv[1], 'r')), float(argv[2]))
    else:
        print "usage:\n\tpython plot_likelihood_map.py lmap.pck [min_valid_value=0.0]"
