from pylab import *
from sys import argv
from classifier_util import *

def get_pr_mrf(mrf_filename, obj_type):
    
    print "loading pclassfile"
    myhash = load_mrf_output(mrf_filename, obj_type)
    
    thresholds = arange(0, 1, 0.0001)

    precisions, recalls = [], []
    for thresh in thresholds:
        tp, fp, fn, tn = 0, 0, 0, 0
        
        for key in myhash.keys():
            prob = myhash[key]['prob']

            if(prob >= thresh and 
               myhash[key]['exists'] == 1):
                #this is a true positive
                tp += 1
            elif(prob >= thresh):
                #this is a false positive
                fp += 1
            elif(prob < thresh and 
                 myhash[key]['exists'] == 0):
                #this is a false negative
                fn += 1
            else:
                #this is a true negative
                tn += 1


        if(tp + fp == 0 or tp + fn == 0):
            continue

        precision = (tp*1.0) /((tp + fp)*1.0)
        recall = (tp*1.0) /((tp + fn)*1.0)
        precisions.append(precision)
        recalls.append(recall)

    return precisions, recalls


def plot_roc_mrf(mrf_filename, obj_type):
    precisions, recalls = get_pr_mrf(mrf_filename, obj_type)
    p1, = plot(recalls, precisions, 'g^-')
    xlabel("recall")
    ylabel("precision")
    #legend((p1), ("MRF"))
    show()


    
if __name__ == "__main__":
    if(len(argv) == 3):
        plot_roc_mrf(argv[1], argv[2])
    else:
        print "usage:\n\tpython plot_roc.py mrf_file obj_type"

