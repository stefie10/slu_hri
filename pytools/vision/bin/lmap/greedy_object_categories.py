from sys import argv
from cPickle import *
from annote_utils import *
from datatypes_lmap import *

def learn_object_categories(prior, ):
    poly, pts = load_polygons(tagfilename)
    
    names = []
    for elt in poly:
        names.append(elt.tag)
    for elt in pts:
        names.append(elt.tag)

    




if __name__ == "__main__":

    if(len(argv) == 3):
        prior = load(open(argv[2], 'r'))
        
        learn_object_categories(argv[1], prior)

    else:
        print "usage:\n\tpython greedy_object_categories.py tagfile prior"
