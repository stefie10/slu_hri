from glob import glob
from sys import argv
import cPickle
from os import mkdir
import Image

def resize_images(path, topath):
    print "loading files"
    tag_files =  glob(path+"*/*jpeg")

    print "resizing files"
    visited_dirs = []
    for filename in tag_files:
        location_name = filename.split('/')[-2]
        file_number = filename.split('/')[-1]
        location_name = location_name.strip()

        #print each new directory that we visit
        if(not location_name in visited_dirs):
            print "converting-->", location_name
            visited_dirs.append(location_name)
        try:
            mkdir(topath + "/" + location_name)
        except:
            pass
        
        im = Image.open(filename)
        im2 = im.resize((32, 32), Image.ANTIALIAS)
        #print "saving:", topath+"/"+location_name+ "/" + file_number
        im2.save(topath+"/"+location_name+ "/" + file_number)
        #raw_input()
        
            
            

if __name__=="__main__":
    if(len(argv) == 3):
        myhash = resize_images(argv[1], argv[2])
    else:
        print "usage: python resize_images.py path topath"
