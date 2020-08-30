from scipy.io.mio import loadmat
from sys import argv
from spectral_clustering import spectral_clustering_W
from numpy import max, exp
from numpy.random import random

def flickr_spectral_clustering(matfilename):
    
    myhash = loadmat(matfilename)

    data = myhash['data']
    data = exp(data +(random([len(data), len(data)]))*0.0001) # - 0.00005)
    keys = myhash['names']

    #maxval = max(data)
    #data = max_val-data+(randn(len(data), len(data))*0.0001)


    classes, k = spectral_clustering_W(data, 20) 

    for i in range(k):
        print "*************"
        for j in range(len(classes)):
            if(i == int(classes[j])):
                print keys[j]


if __name__=="__main__":
    
    if(len(argv) == 2):
        flickr_spectral_clustering(argv[1])
    else:
        print "usage\n\t python spectral_clustering.py matfilename"
