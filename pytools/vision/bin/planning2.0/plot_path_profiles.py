from scipy import array
from carmen_maptools import *
from sys import argv
import cPickle
from sorting import *
from datatypes_planning import *
from pylab import *
from glob import glob


def plot_paths(path_filename, mymodel, threshold=0.9):
    mypath = cPickle.load(open(path_filename, 'r'))
    
    
    I_threshold, = (array(mypath.tvals) > threshold).nonzero()
    
    tvals = array(mypath.tvals).take(I_threshold)
    fvals = array(mypath.fvals).take(I_threshold)
    lvals = array(mypath.lvals).take(I_threshold)
    
    mypaths = []
    for ind in I_threshold:
        mypaths.append(mypath.queue[ind])
    
    #filter by 
    lvals_fin, I = quicksort(lvals)
    
    finpaths = []
    for ind in I:
        finpaths.append(mypaths[ind])
    
    fvals_fin = array(fvals).take(I)
    tvals_fin = array(tvals).take(I)
    
    #self.spath = shortest_path
    #self.spath_val_t = shortest_val_t
    #self.spath_val_f = shortest_val_f
    #self.spath_lval = shortest_lval
    thespath = mypath.spath
    finspath = None
    finspath_val_t = None
    finspath_lval = None
    i=0

    if(thespath == None):
        return None, None, None, None

    for elt in finpaths:
        if(thespath == elt[0:len(thespath)]):
            print "yes", i
            finspath = elt
            finspath_val_t = tvals_fin[i]
            finspath_lval = lvals_fin[i]
            #raw_input()
            break;
        i+=1

    if(finspath == None):
        return None, None, None, None

    print "orig spath=", len(thespath), "newspath=", len(finspath)
    print "best path=",  len(finpaths[0])

    return lvals_fin[0], tvals_fin[0], finspath_lval, finspath_val_t

    
if __name__ == "__main__":
    
    if(len(argv) == 3):
        myfiles = glob(argv[1]+"*.pck")
        mymodel = cPickle.load(open(argv[2], 'r'))

        L1 = []
        L2 = []

        shorter_elts = 0
        longer_elts = 0
        equal_elts = 0
        for thefile in myfiles:
            l1, t1, l2, t2 = plot_paths(thefile, mymodel)
            print thefile
            if(l1 == None):
                continue

            L1.append(l1)
            L2.append(l2)
            print "L1:", l1, " L2:", l2

            if(l1 < l2):
                shorter_elts +=1
            if(l1 > l2):
                longer_elts +=1
            if(l1 == l2):
                equal_elts += 1
        print "our paths are shorter ", shorter_elts/(len(L1)*1.0), "% of the time"
        print "our paths are longer ", longer_elts/(len(L1)*1.0), "% of the time"
        print "our paths are equal ", equal_elts/(len(L1)*1.0), "% of the time"
            
        bar(arange(len(L1)), L1, 0.35, color='r')
        bar(arange(len(L1))+0.35, L2, 0.35, color='y')
        title(argv[1].split('/')[-1])


        show()

    else:
        print "usage:\n\tpython plot_paths.py path_dir model_file.pck"

