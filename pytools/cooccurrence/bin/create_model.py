from cooccurrence import *
from sys import argv
from tag_util import *

def load_keywords(myfilename):
    kw = []
    myfile = open(myfilename, 'r')
    for line in myfile:
        if(line.strip() != ''):
            kw.append(line.strip())
    return kw

def load_keywords_tagfile(tag_filename, map_filename):
    tf = tag_file(tag_filename, map_filename)
    
    return tf.get_tag_names()

if __name__=="__main__":
    
    kw = load_keywords_tagfile(argv[2], argv[3])
    print kw
    
    input_dir = argv[1]
    dataset_type = argv[4]
    co = cooccurrence(input_dir, kw, dataset_type, max_entries=1000000)
    
    if(dataset_type == "esp"):
        print "saving data/flickr/models/model_esp.pck"
        cPickle.dump(co, open('data/flickr/models/model_esp.pck', 'wb'),
                     cPickle.HIGHEST_PROTOCOL);
    elif(dataset_type == "flickr"):
        print "saving data/flickr/models/model_flickr.pck"
        cPickle.dump(co, open('data/flickr/models/model_flickr.pck', 'wb'))
        #,cPickle.HIGHEST_PROTOCOL);

    
