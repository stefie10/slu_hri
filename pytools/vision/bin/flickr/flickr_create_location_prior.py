from glob import glob
from sys import argv
import cPickle



def count_words(path):
    tag_files =  glob(path+"*/*tags*")
    tag_files1 =  glob(path+"*tags*")
    tag_files.extend(tag_files1)

    myhash = {}
    for filename in tag_files:
        location_name = filename.split('/')[-2]
        location_name = location_name.strip()

        tag_file = open(filename, 'r')
        for tag in tag_file:
            tag = tag.strip()
            #index by tag
            tag_hash = None
            try:
                tag_hash = myhash[tag]
            except:
                myhash[tag] = {}
                tag_hash = myhash[tag]

            #add one to the count of locations
            bad_tag = False

            lname = location_name.split()
            for spl in lname:
                if(spl in tag or tag in spl):
                    bad_tag = True
                    
            if(not bad_tag):
                try:
                    tag_hash[location_name]+=1
                except:
                    tag_hash[location_name]=1
    return myhash
            
            

if __name__=="__main__":
    if(len(argv) == 3):
        myhash = count_words(argv[1])

        #for elt in myhash.keys():

        #   num_elts = 0
        #    for e in myhash[elt].keys():
        #        num_elts += myhash[elt][e]

        #    if(num_elts > 10):
        #        print elt, "-->", myhash[elt]
        #raw_input()
        
        print "Saved: ", len(myhash.keys()), " unique tags"
        cPickle.dump(myhash, open(argv[2], 'w'))
    else:
        print "usage: python count_words.py path myhash"

