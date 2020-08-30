from pca import *
import cPickle
from glob import glob
import Image
from sys import argv
from scipy.misc import fromimage
import os
import shutil

def flickr_nn(folder_name, pd, num_nn):
    files = glob(folder_name + "*.jpeg")


    for file in files:
        #run nearest neighbors, get the 100 nearest neighbors for each image 
        #   and copy them to the right location
        #   along wi,th the tag files
        print "opening image"
        im = Image.open(file)
        im2 = fromimage(im.resize((32, 32), Image.ANTIALIAS))
        
        
        print "performing nearest neighbors"
        filenames = pd.knn(im2, num_nn)
        
        mydir = file.split(".")[0]
        try:
            os.mkdir(mydir)
        except:
            print "directory already exists"

        
        for my_match_file in filenames:
            my_match_file = my_match_file.replace("_pca.pck", ".jpeg")
            shutil.copy(my_match_file, mydir+"/"+my_match_file.split("/")[-1])
            my_match_file = my_match_file.replace("FlickrResized", "FlickrImages")
            tofile = my_match_file.split("/")[-1].split(".")[-2]
            shutil.copy(my_match_file, mydir+"/"+tofile+"_small.jpeg")
            my_match_file = my_match_file.replace(".jpeg", "_tags.txt")
            my_match_file = my_match_file.replace("FlickrImages", "FlickrNotes")
            try:
                shutil.copy(my_match_file, mydir+"/"+my_match_file.split("/")[-1])
            except:
                print "no tag files"
        
        #print "filenames:", filenames 
        #raw_input()

if __name__=="__main__":
    if(len(argv) == 4):
        print "loading database"
        pd = pca_database()
        pd.load(argv[2])
        
        flickr_nn(argv[1], pd, int(argv[3]));
    else:
        print "usage:\n\t python flickr_nn.py test_folder pca_database num_nn"

