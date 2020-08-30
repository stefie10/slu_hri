import cPickle
from sys import argv
from datatypes import *
from pyTklib import tklib_normalize_theta

def pickle_to_carmen(filename, outfilename):
    myfile = open(filename, 'r')
    messages = []
    while(1):
        try:
            data = cPickle.load(myfile)
        except(EOFError):
            break
        
        x = data['x']
        y = data['y']
        theta = data['theta']
        #print data
        #raw_input()x
        ts = data['time_stamp']
        message = robot_laser_message(ts, [x,y,tklib_normalize_theta(theta)], [])
        
        #om = odometry_message(ts, [x, y, 0])
        messages.append(message)
        
    outfile = open(outfilename, 'w')
    #for m in reversed(messages):
    for m in messages:
        outfile.write(m.carmen_str()+"\n")

    
if __name__=="__main__":
    if(len(argv) == 3):
        pickle_to_carmen(argv[1], argv[2])
    else:
        print "usage:\n\tpython pickle_to_carmen_sachi.py pickle_filename outfilename"
