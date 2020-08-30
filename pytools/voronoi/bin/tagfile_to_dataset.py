from sys import argv
import cPickle
from pylab import *
from tag_util import *

print len(argv)

if(len(argv) == 5):
    myskel = cPickle.load(open(argv[1], 'r'))
    myskel.map_filename = argv[3]

    XY = myskel.ind_to_xy(myskel.get_skeleton_indices())

    ofile = open(argv[4], 'w')

    tfile = tag_file(argv[2], argv[3])

    for i in range(len(XY[0])):
        
        if(mod(i, 100)==0):
            print i, " of ", len(XY[0])
        vtags, itags = tfile.get_visible_tags(XY[:,i], max_dist=5.0)
        ofile.write(str(XY[0,i]) + " " + str(XY[1,i]) + " ")
        for t in vtags:
            #print t
            ofile.write(t + " ")
        ofile.write("\n")
    ofile.close()
    
else:
    print "usage:\n\tpython view_skeleton.py skeleton tagfilename map_filename ofile"
