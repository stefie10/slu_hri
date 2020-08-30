from glob import glob
from sys import argv
import cPickle
import Image
from scipy.misc.pilutil import *
from random import randint
from scipy import *
from pca import *

def get_random_indicies(num_elts, num_images):
    I = {}

    if(num_elts > num_images):
        I = range(num_elts)
    else:
        done = False
        while(not done):
            print len(I)
            if(len(I) == num_elts):
                done = True;
                continue
            i = randint(0, num_images-1)
            I[i] = True
    return I.keys()


def estimate_mean(image_files, I):
    mymean = None
    for i in I:
        #load the image
        im = Image.open(image_files[i])
        x = fromimage(im)

        #convert it to a vector
        y = x.flatten()

        if(mymean == None):
            mymean=y
        elif(len(y) == len(mymean)):
            mymean+=y

        del y; del x; del im;
        
    return mymean/(1.0*len(I))
    

def create_database(folder, num_elts, num_pc):
    print "getting files"
    image_files =  glob(folder+"*/*jpeg")

    print "gettting ", num_elts, " indices from ", len(image_files)
    I = get_random_indicies(num_elts, len(image_files))

    print "num in I", len(I)
    
    print "estimate mean:"
    mymean = estimate_mean(image_files, I)

    print "adding images to the database"
    X = []

    myC = None
    for i in I:
        #load the image
        im = Image.open(image_files[i])
        x = fromimage(im)

        #convert it to a vector
        y = x.flatten()

        if(myC == None and len(y) == len(mymean)):
            myC = dot(transpose([y]), array([y]))
        elif(len(y) == len(mymean)):
            myC += dot(transpose([y]), array([y]))
        
        #add it to X
        del im; del x; del y;
    
    #print "len(X)", len(X), " by ", len(X[0])
    print "len(C)", len(myC), len(myC[0])
    print "creating principal components"
    print "mean", mymean
    pc = principal_components(num_pc, C=myC, mean=mymean)
    
    return pc

if __name__=="__main__":
    if(len(argv) == 5):
        print "Creating database" 
        mydb = create_database(argv[1], int(argv[2]), int(argv[3]))

        print "Saving database"
        cPickle.dump(mydb, open(argv[4], 'w'))
    else:
        print "usage: python create_database.py folder num_elts num_pc out_filename"

