from sys import argv
import cPickle
from pylab import *

if(len(argv) == 2):
    myfile = cPickle.load(open(argv[1], 'r'))
    gray()
    imshow(myfile.skeleton)
    show()

else:
    print "usage:\n\tpython view_skeleton.py skeleton"
