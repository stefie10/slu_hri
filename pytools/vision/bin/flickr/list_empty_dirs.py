from glob import glob
from sys import argv
import cPickle

def list_empty_dirs(path, outfile):
    print "loading filenames"
    tag_files =  glob(path+"*/*tags*")
    word_dirs =  glob(path+"*")

    print "finding unseen elements"
    no_elts = []
    for elt in word_dirs:
        isIn = False
        myelt = elt.split("/")[-1]
        print "processing ", myelt        

        for path in tag_files:
            if(myelt in path):
                isIn = True
        
        if(not isIn):
            print "none of ", myelt
            no_elts.append(myelt)

    
    #write to a file
    myfile = open(outfile, 'w')
    for elt in no_elts:
        myfile.write(elt+"\n")
    myfile.close()


if __name__=="__main__":
    if(len(argv) == 3):
        list_empty_dirs(argv[1], argv[2])

    else:
        print "usage: python list_empty_dirs.py path outfile"

