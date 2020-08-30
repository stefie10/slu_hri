import cPickle
from sys import argv
from pylab import *
from datatypes import robot_laser_message

def spline_to_logfile(spline, outfilename):

    X, Y = spline.ind_to_xy(spline.get_skeleton_indices())

    myfile = open(outfilename, 'w')
    #def __init__(self, timestamp, odometry, data, laser_number=1):
    for i in range(len(X)):
        msg = robot_laser_message(i, [X[i], Y[i], 0], zeros(180))
        myfile.write(msg.carmen_str()+"\n")

    myfile.close()
    #plot(X, Y, 'gx')
    #show()




if __name__=="__main__":
    if(len(argv) == 3):
        spline_to_logfile(cPickle.load(open(argv[1], 'r')), argv[2])
    else:
        print "usage:\n\tpython spline_to_logfile.py spline_fname outfilename"
