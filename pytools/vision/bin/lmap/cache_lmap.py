from sys import argv
from annote_utils import *
from datatypes_lmap import *
from cPickle import *

def load_extra_file(filename):
    myfile = open(filename, 'r')

    vals = []
    for line in myfile:
        myline = line.strip()
        vals.append(myline)
    return vals

def cache_lmap(prior, tagfilename=None, skeleton, name="zebra"):
    lt = None
    if(tagfilename != None):
        tf = tag_file(tagfilename, None)

        likelihood_map(tf.get_tag_names(), prior, skeleton, num_iterations=50)
        
        lt = lmap_tools(prior, tf.get_tag_names())
    else:
        lt = lmap_tools(prior)
    
    cPickle.dump(lt, open('lmap_out.pck', 'w'))


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
