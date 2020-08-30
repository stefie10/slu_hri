import cPickle
from sorting import *
from sys import argv
from scipy import array
from nltk.wordnet import *
#from wntools import *


def get_hyponyms(thing):
    hyponyms = [thing]

    try:
        senses_l = N[thing]
    except:
        return hyponyms
    
    for sense in senses_l:
        l1 = closure(sense, HYPONYM)
        for cl in range(1,len(l1)):
            for si in l1[cl].senses():
                hyponyms.append(str(si.getWord())[0:-4].replace(" ", ""))


    return hyponyms

def get_ranking(prior, query):
    print "-------------------------------------------------"
    hyponyms = get_hyponyms(query)
    
    loc_votes = {}
    for i in range(len(hyponyms)):
        print "trying:", hyponyms[i]
        try:
            locations = prior[hyponyms[i]]
        except:
            #print "."
            continue
        
        for key in locations.keys():
            try:
                loc_votes[key] += locations[key]
            except:
                loc_votes[key] = locations[key]
    print "-------------------------------------------------"
    #print "quicksort"
    V, I = quicksort(loc_votes.values())
    O = array(loc_votes.keys()).take(I)
    P = sum(V)

    #print "done"
    for i in range(len(O)):
        print len(O)-(i+1), ") ", O[i], " ", V[i]/(P*1.0)
        

    
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
        print "usage:\n\t python question_answer_mul.py prior_filename"
