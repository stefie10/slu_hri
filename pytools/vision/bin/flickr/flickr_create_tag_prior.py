from glob import glob
from sys import argv
import cPickle

def count_words(path):
    #filter_words = []


    print "getting files"
    tag_files =  glob(path+"*/*tags*")
    tag_files1 =  glob(path+"*tags*")
    tag_files.extend(tag_files1)


    #for each file 
    i = 0
    myhash = {}
    for filename in tag_files:
        print "processing i=", i, " of ", len(tag_files)
        tag_file = open(filename, 'r')
        
        #setup entries for the various tags in the current file
        #  and effectively get all the entries
        curr_tags = []
        for tag in tag_file:
            tag = tag.strip()
            curr_tags.append(tag)

        #if the tag exists in my hash
        #   then add all the related tags to the database
        for tag in curr_tags:
            try:
                myhash[tag] += 1
            except:
                myhash[tag] = 1

        i+=1

    return myhash
            
            

if __name__=="__main__":
    if(len(argv) == 3):
        myhash = count_words(argv[1])
        print "Saved: ", len(myhash.keys()), " unique tags"
        cPickle.dump(myhash, open(argv[2], 'w'))
    else:
        print "usage: python count_words.py path out_file"

