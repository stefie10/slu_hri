import cPickle
from sorting import *
from sys import argv
from scipy import array
from wordnet import *
from wntools import *

def is_a(location, other_location):
    senses_l = N[location]
    senses_l2 = N[other_location]
    
    for sense in senses_l:

        for sense2 in senses_l2:
            l1 = closure(sense, HYPERNYM)
            for cl in range(1,len(l1)):
                for si in l1[cl].senses():
                    if(si.getWord() == sense2.getWord()):
                        return True
    return False



print is_a("sanctuary", "nave")
