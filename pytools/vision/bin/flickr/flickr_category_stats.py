from sys import argv
from sorting import quicksort
from pylab import *
import cPickle
#from wordnet import *
#from wntools import *
from scipy import array, mean, var, exp

def filter_load(filename):
    myfile = open(filename, 'r')
    mylist = []

    for line in myfile:
        mylist.append(line.strip().replace(' ', ''))

    return mylist


def flickr_stats(filename, object, filter_filename):
    
    
    prior = cPickle.load(open(filename, 'r'))


    #plot the curve
    mu = mean(prior[object].values())
    v = var(prior[object].values())
    
    print mu
    print v
    
    X = array(range(0, max(prior[object].values())))
    Y = 1.0/(1.0+exp(-1.0*(X-mu-min(prior[object].values()))/v ))
    print "x", X
    print "x-mu", (X-mu)/v
    print "y:", Y
    
    plot(X, Y);
    xlabel("object count")
    ylabel("probability of " + object)

    figure()    

    filter = filter_load(filter_filename)
    
    mytags_hash = prior[object]

    for key in mytags_hash.keys():
        if(not key in filter):
            mytags_hash.pop(key)
    
    K = array(mytags_hash.keys())
    V, I = quicksort(mytags_hash.values())
    
    mf_keys = K.take(I[len(I)-20:len(I)]).tolist()
    mf_vals = array(mytags_hash.values()).take(I[len(I)-20:len(I)]).tolist()

    #mf_keys.reverse()
    #mf_vals.reverse()
    
    p2 = barh(arange(len(mf_vals)), mf_vals, color='b', height=0.8)

    setp(gca(), 'yticks', arange(len(mf_vals)))
    labels = setp(gca(), 'yticklabels', mf_keys)
    #setp(labels, 'rotation', 'vertical')

    #labels = xticks(arange(len(mf_vals)), mf_keys)
    #xticks(arange(len(mf_vals)), mf_keys)
    
    
    title("Location counts for "+object)
    show()
    


if __name__=="__main__":

    if(len(argv)==4):
        flickr_stats(argv[1], argv[2], argv[3])
    else:
        print "usage:\n\t python flickr_category_stats.py prior.pck object filter_filename"
