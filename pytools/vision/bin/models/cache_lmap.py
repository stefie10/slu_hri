from sys import argv
from annote_utils import *
from datatypes_lmap import *
from cPickle import *
import os

def load_extra_file(filename):
    myfile = open(filename, 'r')

    vals = []
    for line in myfile:
        myline = line.strip()
        myline = myline.replace(" ", "");
        vals.append(myline)
    return vals

def cache_lmap(prior, tagfilename=None, extraFile=None):

    names = []
    if(extraFile != None):
        names = load_extra_file(extraFile)

    print names

    lt = None
    if(tagfilename != None):
        poly, pts = load_polygons(tagfilename)

        for elt in poly:
            if(elt.tag not in names):
                names.append(elt.tag)
        for elt in pts:
            if(elt.tag not in names):
                names.append(elt.tag)
        
        print names
        lt = flickr_cache(prior, names)
    else:
        lt = flickr_cache(prior)

        
    outfilename = 'prior_hash.pck'
    print "cwd:", os.getcwd()+"/"+outfilename
    cPickle.dump(lt, open(outfilename, 'wb'), 2)


if __name__ == "__main__":
    if(len(argv) == 2):
        prior = load(open(argv[1], 'r'))
        cache_lmap(prior)
    elif(len(argv) == 3):
        prior = load(open(argv[1], 'r'))
        cache_lmap(prior, argv[2])
    elif(len(argv) == 4):
        prior = load(open(argv[1], 'r'))
        cache_lmap(prior, argv[2], argv[3])

    else:
        print "usage:\n\tpython cache_lmap.py prior [tagfile] [extratags]"
