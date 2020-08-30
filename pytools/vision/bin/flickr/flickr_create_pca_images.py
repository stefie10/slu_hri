from glob import glob
from sys import argv
import cPickle
import Image
from scipy.misc.pilutil import *
from random import randint
from scipy import *
from pca import *


def create_database(folder, pca, num_pc):
    print "getting files"
    image_files =  glob(folder+"*/*jpeg")
    pca.order = num_pc
    
    for i in range(len(image_files)):
        print i
        #load the image
        im = Image.open(image_files[i])
        x = fromimage(im)

        #convert it to a vector
        y = x.flatten()
        

        #encode the image
        try:
            encIm = pca.encode(transpose([y]))
        except:
            print "error"
            continue
        
        myImOut = open(image_files[i].split(".jpeg")[0]+"_pca.pck", 'w')
        cPickle.dump(encIm, myImOut)
        myImOut.close()
        
        del im; del x; del y;

if __name__=="__main__":
    if(len(argv) == 4):
        print "loading PCA"
        myPCA = cPickle.load(open(argv[2], 'r'))
        create_database(argv[1], myPCA, int(argv[3]))
                        
        
    else:
        print "usage: python create_database.py folder pca.pck num_pc"

