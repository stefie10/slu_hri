from sys import argv
from sorting import quicksort
from scipy import array
from pylab import *
import cPickle
#from wordnet import *
#from wntools import *

def filter_load(filename):
    myfile = open(filename, 'r')
    mylist = {}

    for line in myfile:
        mylist[line.strip().replace(' ', '')] = True

    return mylist

def flickr_stats(filename, filter_filename=None):
    prior = cPickle.load(open(filename, 'r'))

    print "number of tags:", len(prior.keys())

    myfilter = None
    if(filter_filename != None):
        myfilter = filter_load(filter_filename)
    
    mytags_hash = {}
    
    for obj in prior.keys():
        location = prior[obj]
        
        #for elt in myfilter:
        try:
            if(myfilter != None and myfilter[obj]):
                mytags_hash[obj] = sum(location.values())
            elif(myfilter == None):
                mytags_hash[obj] = sum(location.values())
        except:
            continue

                    
    num_locations = len(prior.keys())
    num_objects = len(mytags_hash.keys())

    print "number of locations:", num_locations
    print "number of objects:", num_objects
    
    K = array(mytags_hash.keys())
    Vs = array(mytags_hash.values())
    V, I = quicksort(mytags_hash.values())

    print "number of flowers:", mytags_hash["flower"]

    #for i in range(len(mytags_hash.keys())):
    #    print mytags_hash.keys()[i], mytags_hash.values()[i]
    #print "final key", K[I[len(V)-1]]
    #print "final value", Vs[I[len(V)-1]]

    print len(I), len(V)
    
    mf_keys = K.take(I[len(I)-100:len(I)]).tolist()
    mf_vals = array(Vs).take(I[len(I)-100:len(I)]).tolist()


    mf_keys.reverse()
    mf_vals.reverse()

    p2 = bar(arange(len(mf_vals)), mf_vals, color='b', width=0.8)

    setp(gca(), 'xticks', arange(len(mf_vals)))
    labels = setp(gca(), 'xticklabels', mf_keys)
    setp(labels, 'rotation', 'vertical')

    print mf_keys
    #labels = xticks(arange(len(mf_vals)), mf_keys)
    #xticks(arange(len(mf_vals)), mf_keys)
    show()
    


if __name__=="__main__":

    if(len(argv)==2):
        flickr_stats(argv[1])
    if(len(argv)==3):
        flickr_stats(argv[1], argv[2])
    else:
        print "usage:\n\t python flickr_stats.py prior.pck filter_filename"
