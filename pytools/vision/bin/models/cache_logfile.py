from sys import argv
from datatypes_lmap import *
from carmen_maptools import *
import cPickle
from pyTklib import *


def cache_logfile(tag_filename, log_filename, 
                  map_filename, image_dir, 
                  tp=0.9, tn=0.9, myseed=1):
                  

    #print "loading polygons"
    #polys_tag, pts_tag = load_polygons(tag_filename)

    print "create logfile"
    '''ion()
    mymap = tklib_log_gridmap()
    mymap.load_carmen_map(map_filename)
    themap = mymap.to_probability_map_carmen()
    plot_map(themap, mymap.x_size, mymap.y_size)'''

    thelogfile = logfile_lmap(log_filename, 
                              map_filename, 
                              tag_filename,
                              image_dir, 
                              tp, tn, myseed)
                     

    

    print "dumping the data"
    myfilename = log_filename.split("/")[-1]+"_"+str(tp)+"_"+str(tn)+"_"+str(myseed)+".pck"
    print myfilename
    thelogfile.gridmap = None
    thelogfile.tfile.map = None

    cPickle.dump(thelogfile, 
                 open(myfilename, 'w'))

    print "done"


if __name__=="__main__":
    if(len(argv) == 8):
        cache_logfile(argv[1], argv[2], argv[3], argv[4],
                      float(argv[5]), float(argv[6]), int(argv[7]))
    else:
        print "usage:\n\t python cache_logfile.py tag_file logfile mapfilename image_dir tp tn seed"



