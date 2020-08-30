from cooccurrence import *
from sys import argv
from tag_util import *
import orange

def load_keywords(myfilename):
    kw = []
    myfile = open(myfilename, 'r')
    for line in myfile:
        if(line.strip() != ''):
            kw.append(line.strip())
    return kw


if __name__=="__main__":
    model_type = argv[3]

    if(model_type == "esp"):
        model = cPickle.load(open("data/flickr/models/model_esp.pck", 'rb'))
    elif(model_type == "flickr"):
        model = cPickle.load(open("data/flickr/models/model_flickr.pck", 'rb'))

    mykeywords = load_keywords(argv[1])
    learner = argv[2]
    
    print "training with:", learner
    for i, keyword in enumerate(mykeywords):
        print "training ", keyword
        model.train(keyword, learner=learner)
    
    
    print "kitchen given refrigerator and microwave"
    print model.predict("kitchen", ["refrigerator", "microwave"], learner=learner)
    
    print "bathroom given toilet and soap"
    print model.predict("bathroom", ["table", "toilet", "soap"], learner=learner)
    
    print "computer given monitor chair"
    print model.predict("computer", ["monitor", "desk"], learner=learner)

    if(model_type == "esp"):
        print "saving to:", "data/flickr/models/model_esp_trained."+learner+".pck"
        cPickle.dump(model, open("data/flickr/models/model_esp_trained."+learner+".pck", 'wb'), 
                     cPickle.HIGHEST_PROTOCOL)

    elif(model_type == "flickr"):
        print "saving to:", "data/flickr/models/model_flickr_trained."+learner+".pck"
        cPickle.dump(model, open("data/flickr/models/model_flickr_trained."+learner+".pck", 'wb'), 
                     cPickle.HIGHEST_PROTOCOL)

    print "done"
    

