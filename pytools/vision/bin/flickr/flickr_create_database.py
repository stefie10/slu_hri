from glob import glob
from sys import argv
import cPickle
import Image
from scipy.misc.pilutil import *
from random import randint
from scipy import *
from pca import *
import tables

def get_random_indicies(num_elts, num_images):
    I = {}

    if(num_elts > num_images):
        I = range(num_images)
        return I
    else:
        done = False
        while(not done):
            print len(I)
            if(len(I) == num_elts):
                done = True;
                continue
            i = randint(0, num_images-1)
            I[i] = True
    #print "number loading", len(I.keys())
    return I.keys()


def create_database(path, pca_filename, num_elts, out_filename):
    print "getting files"
    image_files =  glob(path+"*/*.pck")
    I = get_random_indicies(num_elts, len(image_files))
    
    print "loading images"
    filenames, images = [], []

    for i in I:
        #load the image

        tmp_file = open(image_files[i], 'r')
        filenames.append(image_files[i])

        pca_im = cPickle.load(tmp_file)

        if(images == []):
            print "making array of size:", [len(pca_im[:,0]), len(I)]
            images = zeros([len(pca_im[:,0]), len(I)])*1.0
        print "i", i
        #otherwise, add elements elementwise
        for k in range(len(pca_im[:,0])):
            images[k, i] = pca_im[k,0]

        del pca_im; tmp_file.close()

    print "creating database"
    db = pca_database(pca_filename)
    print "adding images"
    db.add_images(filenames, images)
    #print "knn:", db.knn(zeros(3072), 3)
    
    print "saving database"
    db.save(out_filename)
    


    
if __name__=="__main__":
    if(len(argv) == 5):
        print "Creating database" 
        create_database(argv[1], argv[2], int(argv[3]), argv[4])
    else:
        print "usage: python create_database.py folder pca_filename num_elts out_filename"





#scipy_array = scipy.array(Dataset1)    
#datasets = h5file.createGroup(root, "data", "Flickr 700k database")
#scipy_array = scipy.array(Dataset2)
#h5file.createArray(datasets, 'dataset2', scipy_array, "Test data set #2")
#scipy_array = scipy.zeros((100,100))
#h5file.createArray(datasets, 'dataset3', scipy_array, "Test data set #3")
#cPickle.dump(db, open(out_filename+".pck", 'w'))
