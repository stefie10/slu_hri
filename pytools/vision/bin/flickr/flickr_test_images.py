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
        else:
            mymean+=y

        del y; del x; del im;
        
    return mymean/(1.0*len(I))
    
def test_image(myregex, pca_database):
    print "getting files"
    image_files =  glob(myregex)

    for i in range(len(image_files)):
        print i

        #load the image
        im = Image.open(image_files[i])
        x = fromimage(im)
        filenames = pca_database.knn(x, 10)

        for file in range(len(filenames)):
            myim = fromimage(Image.open(open(file, 'r')))
            print "showing ", file
            imshow(myim)
            draw()
            raw_input()
        
        del im; del x; del y;


if __name__=="__main__":
    if(len(argv) == 3):
        print "Creating database" 
        test_image(argv[1], load(open(argv[2])))
    else:
        print "usage: python create_database.py folder num_elts num_pc out_filename"

