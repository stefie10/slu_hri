from random import random
from scipy import sum

def normalize(probs, epsilon=0.000001):
    return (probs)/(sum(probs)+0.000001)

def sample_discrete(P, ns):
    indexes = []

    #add one extra element
    #to buffer
    tmp = [None]
    tmp.extend(P)
    P = tmp

    #generate the cdf
    cdf = []
    c=0
    for p in P:
        if(not p == None):
            c += p
            cdf.append(c)

        
    #sample from it
    u0 = random()*(1/(1.0*ns))
    uj = 0
    i=0
    
    for j in range(1,ns+1):

        uj = u0 + (1/(1.0*ns))*(j-1)
        
        while(uj > cdf[i]):
            i+=1
        
        indexes.append(i)
    
    return indexes

