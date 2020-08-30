from pyTklib import *
from sys import argv
from os.path import exists

if __name__=="__main__":

    if(len(argv) == 4):
        mymap = tklib_log_gridmap()


        if(exists(argv[1])):
            print "loading map: ", argv[1]
            mymap.load_carmen_map(argv[1])
            
            print "downsizing and saving map to :", argv[2]
            mymap.downsize_and_save_map(argv[2], int(argv[3]));
        else:
            print "bad path:", argv[1]
    else:
        print "usage:\n\tpython downsize_map.py orig_filename final_filename scale_amount"

