from glob import glob
from sys import argv
import cPickle

def flickr_count_images(path):
    tag_files =  glob(path+"*/*tags*")
    tag_files1 =  glob(path+"*tags*")
    tag_files.extend(tag_files1)
    print "number of images:", len(tag_files) 

if __name__=="__main__":
    if(len(argv) == 2):
        myhash = flickr_count_images(argv[1])
    else:
        print "usage: python flickr_image_count.py path"

