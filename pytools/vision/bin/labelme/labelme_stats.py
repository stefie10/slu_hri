from sys import argv
from sorting import quicksort
from scipy import array
from pylab import *

def labelme_stats(filename):
    myfile = open(filename, 'r')

    mytags = {}
    num_lines = 0

    for line in myfile:
        num_lines +=1
        tags = line.split(',')[3:]
        
        for tag in tags:
            if(tag == " " or tag == ''):
                continue
            try:
                mytags[tag] +=1
            except:
                mytags[tag] = 1



    print "number of images", num_lines
    print "number of unique tags", len(mytags.keys())

    K = array(mytags.keys())
    V, I = quicksort(mytags.values())

    mf_keys = K.take(I[-100:-2]).tolist()
    mf_vals = array(mytags.values()).take(I[-100:-2]).tolist()

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
        labelme_stats(argv[1])
    else:
        print "usage:\n\t python labelme_stats.py labelme_tags"

