import cPickle
from sorting import *
from sys import argv
from scipy import array
from nltk.wordnet import *
#from wntools import *


def get_ranking(prior, query):
    
    locations = prior[query]

    V, I = quicksort(locations.values())
    #get the count based on the tree

    O = array(locations.keys()).take(I)
    P = sum(locations.values())

    for i in range(len(O)):
        print len(O)-(i+1), ") ", O[i], " ", V[i]/(P*1.0)
        

    
def question_answer(prior_filename):
    prior = cPickle.load(open(prior_filename, 'r'))
    
    while(1):
        query = raw_input("What are you looking for? ")
        try:
            get_ranking(prior, query)
        except:
            continue


if __name__=="__main__":

    if(len(argv) == 2):
        question_answer(argv[1])
    
    else:
        print "usage:\n\t python question_answer.py prior_filename"
