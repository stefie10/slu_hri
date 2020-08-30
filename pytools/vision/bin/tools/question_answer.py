import cPickle
from sorting import *
from sys import argv
from scipy import array
from nltk.wordnet import *
#from nltk.wntools import *

def get_groups(locations, num_levels):
    grps = []
    for i in range(len(locations)):
        grp =[locations[i]]

        for j in range(len(locations)):
            if(i==j):
                continue
            if(len(grp) > num_levels +1):
                break
            
            #print "isa", locations[i], locations[j], " -->", is_a(locations[i], locations[j])
            if(is_a(locations[i], locations[j])):
                grp.append(locations[j])
        grps.append(grp)
    return grps
            
    #elif(is_a(locations[j], locations[i])):
    #    pass


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


def get_ranking(prior, query):
    locations = prior[query]
    #print "get groups"
    #print locations.keys()
    grps = get_groups(locations.keys(), 2)
    print "groups", grps


    #V, I = quicksort(locations.values())
    #get the count based on the tree

    #print "compute new counts"
    new_cnts = []
    for grp in grps:
        cnt = 0
        for loc in grp:
            cnt += locations[loc]
        new_cnts.append(cnt)

    #print "quicksort"
    V, I = quicksort(new_cnts)
    O = array(locations.keys()).take(I)
    P = sum(new_cnts)

    #print "done"
    for i in range(len(O)):
        print i+1, ") ", O[len(O)-i-1], " ", V[len(O)-i-1]/(P*1.0)
        

    
def question_answer(prior_filename):
    prior = cPickle.load(open(prior_filename, 'r'))
    
    while(1):
        query = raw_input("What are you looking for? ")
        get_ranking(prior, query)


if __name__=="__main__":
    #print "dog is an animal", is_a("dog", "animal")
    #print "animal is a dog",  is_a("animal", "dog")

    if(len(argv) == 2):
        question_answer(argv[1])
    
    else:
        print "usage:\n\t python question_answer.py prior_filename"
