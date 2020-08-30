from pylab import *
from sys import argv
from cPickle import load
from carmen_maptools import plot_map
from pylab import show, plot, draw, ion, figure, imshow
from pyTklib import kNN, tklib_euclidean_distance
import time
from topological_map import *


if __name__ == "__main__":
    if(len(argv) == 3):
        skel = load(open(argv[1], 'r'))
        skel.map_filename = argv[2]
        
        print "getting topological map"
        t1=time.time()
        tmap, paths, XY = compute_topological_map(skel, 10)

        #print "getting hash"
        #t2=time.time()
        #xy_ind_to_path_ind = compute_xy_ind_to_ppath_ind(paths)
        #print xy_ind_to_path_ind
        #t3=time.time()

        #print "time to compute topology:", t2-t1
        #print "time to compute hash:", t3-t2
        #raw_input("press enter>>")

        #ion()
        figure()
        imshow(array(skel.get_skeleton()), origin='lower', cmap=cm.gray, interpolation='nearest')
        draw()
        
        figure()
        plot_map(skel.get_map().to_probability_map_carmen(), skel.get_map().x_size, skel.get_map().y_size)
        
        for i in range(len(paths)):
            print i, "of", len(paths)
            X, Y = XY.take(paths[i], axis=1)
            plot(X, Y)

        print "done"
        draw()

        draw()
        figure()
        plot_map(skel.get_map().to_probability_map_carmen(), skel.get_map().x_size, skel.get_map().y_size)
        X, Y = XY.take(tmap.keys(), axis=1)
        plot(X, Y, 'r^')

        figure()

        X, Y = XY.take(tmap.keys(), axis=1)
        plot(X, Y, 'r^')

        for elt in tmap.keys():
            for val in tmap[elt]:
                x1 = XY[:,elt]
                x2 = XY[:,val]

                plot([x1[0], x2[0]], [x1[1], x2[1]])


        figure()
        
        #X, Y = XY.take(tmap.keys(), axis=1)
        #plot(X, Y, 'r^')

        for path in paths:
            if(not tmap.has_key(path[0]) or not tmap.has_key(path[-1])):
                x1 = XY.take(path, axis=1)
                plot(x1[0], x1[1])
                raw_input("yikes!>>")

        title("Yikes!")

        figure()
        #X, Y = XY.take(tmap.keys(), axis=1)
        #plot(X, Y, 'r^')
        xyi_to_pi_ext, xyi_to_pi_center = compute_xy_ind_to_ppath_ind(paths)
        for i in xyi_to_pi_ext.keys():
            pinds =  xyi_to_pi_ext[i]
            mypaths = list(paths[j] for j in pinds)
            
            if(len(pinds) > 1):
                for path in mypaths:
                    if(not i == path[0] and not i == path[-1]):
                        print "error:", " index", i, " not at extremities of path:", path
                        
        title("Yikes!")
        figure()
        
        for elt in tmap.keys():
            conn = tmap[elt]
            for c in conn:
                sx, sy = XY.take([elt], axis=1)
                ex, ey = XY.take([c], axis=1)
                
                plot([sx, ex], [sy, ey])
        
        show()
    else:
        print "usage\n\tpython pomdp_command.py skel_file map_file"
