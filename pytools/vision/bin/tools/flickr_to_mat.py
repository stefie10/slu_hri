from pylab import *
from sys import argv
from cPickle import load
from numpy import max
from scipy.io.mio import savemat

def load_filter(filter_filename):
    myfile = open(filter_filename, 'r')
    myfilter = []
    for line in myfile:
        myfilter.append(line.strip())

    print myfilter
    return myfilter

def flickr_to_mat(prior_filename, filter_filename, max_val=4, min_val=3):

    myfilter = load_filter(filter_filename)
    prior_obj = load(open(prior_filename, 'r'))
    


    mymatrix_rel = zeros([len(myfilter), len(myfilter)])*1.0
    mymatrix_rel_filter = zeros([len(myfilter), len(myfilter)])*1.0
    mymatrix_freq = zeros([len(myfilter), len(myfilter)])*1.0
    
    print mymatrix_rel
    print len(myfilter)
    
    i = 0
    for elt in myfilter:
        j=0
        for elt2 in myfilter:
            try:
                val = prior_obj[elt][elt2]
                mymatrix_rel[i,j] = 1
                mymatrix_rel[j,i] = 1

                if(val > max_val):
                    mymatrix_freq[i,j] = max_val
                    mymatrix_freq[j,i] = max_val
                else:
                    mymatrix_freq[i,j] = val
                    mymatrix_freq[j,i] = val

                if(val > min_val):
                    mymatrix_rel_filter[i,j] = 1
                    mymatrix_rel_filter[j,i] = 1

            except:
                pass

            j+=1
        i+=1


    savemat('flickr_categories_subset_frequency.mat', 
            {'names':myfilter , 'data':mymatrix_freq})
    savemat('flickr_categories_subset_cooccurance.mat', 
            {'names':myfilter, 'data':mymatrix_rel})
    savemat('flickr_categories_subset_cooccurance_filter.mat', 
            {'names':myfilter, 'data':mymatrix_rel_filter})

    figure()
    gray()
    mymax = max(mymatrix_freq)
    imshow(mymax - mymatrix_freq, interpolation='nearest')
    yticks(range(len(myfilter)), myfilter, fontsize='small')
    xticks(range(len(myfilter)), myfilter, rotation='vertical', fontsize='small')
    
    figure()
    gray()
    imshow(1.0-mymatrix_rel, interpolation='nearest')
    yticks(range(len(myfilter)), myfilter, fontsize='small')
    xticks(range(len(myfilter)), myfilter, rotation='vertical', fontsize='small')

    figure()
    gray()
    imshow(1.0-mymatrix_rel_filter, interpolation='nearest')
    yticks(range(len(myfilter)), myfilter, fontsize='small')
    xticks(range(len(myfilter)), myfilter, rotation='vertical', fontsize='small')

    show()


if __name__=="__main__":

    if(len(argv) == 3):
        flickr_to_mat(argv[1], argv[2])
    else:
        print "usage:\n\tpython flickr_to_mat.py prior_filename filter_filename"
