from cooccurrence import *
from sys import argv
from tag_util import *
import orange
from sorting import quicksort
from pylab import *

def plot_roc_curve(model, mykeyword, learner):
    training_docs, test_docs, train_label, test_label = model.get_training_test_sets(mykeyword, 0.8)
    print test_label

    Scores = []
    Thresholds = set([])
    for i, doc_i in enumerate(test_docs):
        res = model.predict(mykeyword, model.documents[doc_i], learner=learner)
        if(res == None):
            continue
        
        Scores.append(res[1].values()[-1])
        Thresholds.add(res[1].values()[-1])
    
    Thresholds = list(Thresholds)
    Thresholds.sort()
    print "scores:", Scores

    TPR = []
    FPR = []
    for i, s in enumerate(Thresholds):
        #print "thresh:", s
        #print "diff", abs(Thresholds[i]-Thresholds[i-1])
        #print "diff", abs(Thresholds[i]-Thresholds[i-1]) < 10^-2
        #print 10**-2
        #if(i > 0 and abs(Thresholds[i]-Thresholds[i-1]) < 10**-3):
        #    print "cont"
        #    continue

        tp, fp, tn, fn = get_statistics(Scores, s, test_label)
        
        if(tp+fn == 0):
            TPR.append(0)
        else:
            TPR.append((1.0*tp)/(tp+fn))

        if(fp+tn == 0):
            FPR.append(0)
        else:
            FPR.append((1.0*fp)/(fp+tn))


    FPR_srt, I = quicksort(FPR)
    TPR = array(TPR)
    TPR_srt = TPR.take(I)

    plot(FPR_srt, TPR_srt, 'kx-')
    title(mykeyword)
    xlabel("False positive rate")
    ylabel("True positive rate")
    

def get_statistics(Scores, threshold, test_label):
    tp = 0; fp =0; fn=0; tn=0
    for i, s in enumerate(Scores):
        if(Scores[i] == None):
            continue

        if(Scores[i] >= threshold and test_label[i] == 1):
            tp += 1
        elif(Scores[i] >= threshold and test_label[i] == -1):
            fp += 1
        elif(Scores[i] < threshold and test_label[i] == 1):
            fn += 1
        elif(Scores[i] < threshold and test_label[i] == -1):
            tn += 1

    return tp, fp, tn, fn

print "loading:", "data/flickr/models/model_" +argv[3]+"_trained."+argv[2]+".pck"
model = cPickle.load(open("data/flickr/models/model_"+argv[3]+"_trained."+argv[2]+".pck", 'r'))
plot_roc_curve(model, argv[1], argv[2])
show()
