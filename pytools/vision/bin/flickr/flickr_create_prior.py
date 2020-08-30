from glob import glob
from sys import argv
import cPickle



def count_words(path, filter_filename):
    print "loading filter"
    filter_words_file = open(filter_filename, 'r')
    #filter_words = []
    myhash = {}
    for word in filter_words_file:
        word = word.strip()
        word = word.replace(' ', '')
        print word
        myhash[word] = {}

    print "getting files"
    tag_files =  glob(path+"*/*tags*")
    tag_files1 =  glob(path+"*tags*")
    tag_files.extend(tag_files1)


    #for each file 
    i = 0
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
                myhash[tag]

                for tag2 in curr_tags:
                    if(tag == tag2):
                        continue
                    #index by tag
                    try:
                        myhash[tag][tag2] += 1
                    except:
                        myhash[tag][tag2] = 1
            except:
                continue

        i+=1
    return myhash
            
            

if __name__=="__main__":
    if(len(argv) == 4):
        myhash = count_words(argv[1], argv[2])
        print "Saved: ", len(myhash.keys()), " unique tags"
        cPickle.dump(myhash, open(argv[3], 'w'))
    else:
        print "usage: python flickr_create_prior.py path filter_words myhash"

