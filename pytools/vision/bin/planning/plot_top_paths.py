from sys import argv
import cPickle
from scipy import *
from carmen_maptools import *
from pylab import *
from datatypes_dp import *

def plot_top_paths(dp, num_paths, num_steps=None):

    tkmap = dp.lmap.skeleton.get_map()
    f = figure()
    f.text(.5, .95, dp.object_name, horizontalalignment='center', fontsize=16) 
    color = ['rx', 'bx', 'gx', 'kx', 'yx', 'mx', 
             'ro', 'bo', 'go', 'ko', 'yo', 'mo']

    print "computing best paths"
    if(num_steps == None):
        V, I, P = dp.compute_best_paths(dp.steps)
    else:
        V, I, P = dp.compute_best_paths(num_steps)

    print "plotting maps"
    done = False

    i = len(V)-1
    count = 0
    curr_paths = []
    #title(dp.object_name)
    while(not done):
        if(count >= num_paths):
            break

        #compute the similarities of paths
        mysim = compute_similarity(P[i], curr_paths)

        #compute what values are very like others
        I, = (mysim > 0.85).nonzero(); i-=1;

        #continue if they are
        if(len(I) > 0):
            continue
        
        #plot them if they are not similar
        #print "plotting ", i
        #figure()
        #subplot(ceil(sqrt(num_paths)), ceil(sqrt(num_paths)), count+1)
        #subplot(2, ceil(num_paths/2.0), count+1)
        subplot(1, num_paths, count+1)
        axis('off')
        plot_map(tkmap.to_probability_map_carmen(), 
                 tkmap.x_size, tkmap.y_size)
        
        X, Y = P[i]
        print "**********", i, "***********"
        print "i", V[i]
        mylen = 0
        for k in range(1, len(X)):
            mylen += sqrt((X[k-1]-X[k])**2.0 + (Y[k-1]-Y[k])**2.0)
        
        print "len:", mylen

        #print "paths equal?", P[i]==P[i-1]
        plot(X, Y, 'r-')
        plot([X[0]], [Y[0]], 'ro')
        plot([X[-1]], [Y[-1]], 'go')
        #title(str(count)+": "+" v="+ str(V[i]))

        count+=1
        curr_paths.append(P[i])
        
    #figure()
    #gray()
    #mylmap = dp.lmap.get_lmap(dp.object_name)
    #imshow(mylmap, origin='lower')
    print "saving figure"
    savefig('top_paths.png');
    show()

def compute_similarity(p, paths):

    if(len(paths) == 0):
        return array([])

    percentages = []
    for path in paths:
        
        inside = 0
        total = 0
        for i in range(len(p[0,:])):
            if((p[:,i] == path[:,i]).all()):
                inside += 1.0
            total += 1.0

        #print inside*1.0/total*1.0
        percentages.append(inside*1.0/total*1.0)

    return array(percentages)


if __name__ == "__main__":
    if(len(argv) == 3):
        print "loading files"
        plot_top_paths(cPickle.load(open(argv[1], 'r')), int(argv[2]))
    elif(len(argv) == 4):
        print "loading files"
        plot_top_paths(cPickle.load(open(argv[1], 'r')), int(argv[2]), int(argv[3]))
    else:
        print "usage:\n\t python flickr_plot_likelihood_map_v3.py dp.pck num_paths [path_length]"
