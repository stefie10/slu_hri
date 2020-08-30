from pylab import *
from classifier_util import *
from sys import argv
from math import fmod
from pyTklib import gaussian_log_prob
from copy import deepcopy
from scipy import mod

        
def get_tp_fp(myhash_gtruth, myhash_pclass, 
              obj_type, type_detector, 
              thresh, mu=None, Sigma=None):
    tp, fp = 0, 0
    tn, fn = 0, 0
    
    for imnum in myhash_gtruth.keys():
        if(not myhash_pclass.has_key(imnum)):
            continue

        elif(type_detector == "prob_joint" or 
             type_detector == "prob_mrf"):
            gtruth = myhash_gtruth[imnum]
            
            #process this separately

            myval = myhash_pclass[imnum]
            
            if(myval >= thresh and 
               obj_type in gtruth):
                #this is a true positive
                tp += 1
            elif(myval >= thresh):
                #this is a false positive
                fp += 1
            elif(obj_type in gtruth):
                #this is a false negative
                fn += 1
            else:
                #this is a true negative
                tn += 1
        #not myhash_pclass.has_key(imnum)
        elif((len(myhash_pclass[imnum]) == 0   
              and obj_type in myhash_gtruth[imnum])):
            #print "fn"
            fn += 1
        #not myhash_pclass.has_key(imnum)):
        elif(len(myhash_pclass[imnum]) == 0): 
            #print "tn"
            tn += 1
        else:
            isset = False
            gtruth = myhash_gtruth[imnum]
            
            detnum = 0
            for det in myhash_pclass[imnum]:

                myval = det[type_detector]

                if(type_detector == "prob_c1" or 
                   type_detector == "prob_c2" or 
                   type_detector == "prob_c3"):
                    myval = myval * det["prob_im"]

                if(myval >= thresh and 
                   obj_type in gtruth):
                    #this is a true positive
                    tp += 1
                    isset=True
                    break
                elif(myval >= thresh):
                    #this is a false positive
                    fp += 1
                    isset = True
                    break
                detnum += 1
            if(not isset and obj_type in gtruth):
                #this is a false negative
                fn += 1
            else:
                #this is a true negative
                tn += 1
        #print "doing something"

    return tp, tn, fp, fn

def get_new_hash(myhash_pclass, 
                 mu_h=None, Sigma_h=None,
                 mu_win=None, Sigma_win=None, 
                 mu_disp=None, Sigma_disp=None):
    myhash_pclass_new = deepcopy(myhash_pclass)
    
    for imnum in myhash_pclass_new.keys():
        #not myhash_pclass.has_key(imnum)
        if(len(myhash_pclass[imnum]) == 0):
            continue
        else:
            detnum = 0
            for det in myhash_pclass[imnum]:
                #new values for size

                p1  =  myhash_pclass_new[imnum][detnum]["prob_c1"] 
                if(mu_win != None):
                    #print mu_win, Sigma_win
                    p1 = prob_gaussian(transpose([[det["size_width"], 
                                                   det["size_height"]]]), mu_win, Sigma_win)
                    myhash_pclass_new[imnum][detnum]["prob_c1"] = p1
                
                #same values for disparity
                p2 = myhash_pclass_new[imnum][detnum]["prob_c2"]
                if(mu_disp != None):
                    p2 = prob_gaussian(transpose([[det["disparity"]]]), mu_disp, Sigma_disp)
                    myhash_pclass_new[imnum][detnum]["prob_c2"] = p2

                #new values for height
                p3  =  myhash_pclass_new[imnum][detnum]["prob_c3"] 
                if(mu_h != None):
                    #print mu_h, Sigma_h
                    p3 = prob_gaussian(transpose([[det["height"]]]), mu_h, Sigma_h)
                    myhash_pclass_new[imnum][detnum]["prob_c3"] = p3

                
                p_im = myhash_pclass_new[imnum][detnum]["prob_im"]
                
                myhash_pclass_new[imnum][detnum]["prob_fin"] = p1*p2*p3*p_im
                detnum += 1

    return myhash_pclass_new

def prob_gaussian(X, mu, Sigma):
    #val2 = exp((-1.0/2.0)*dot(dot(array([x-mu]), inv(Sigma)), transpose([x-mu])))[0][0]
    #val1 = 1.0/(((2*pi)**(len(Sigma)/2.0)) * (det(Sigma)**0.5))

    #print val1*val2
    #gsl_vector* gaussian_log_prob(gsl_matrix* X, gsl_vector* u, gsl_matrix* cov){
    v12, = exp(gaussian_log_prob(X, mu, Sigma))
    #raw_input()

    val2_max = exp(0)
    val1_max = 1.0/(((2*pi)**(len(Sigma)/2.0)) * (det(Sigma)**0.5))

    return v12/(val1_max*val2_max)


def get_precision_recall(myhash_gtruth, myhash_pclass, 
                         obj_type, type_detector, 
                         thresh, mu=None, Sigma=None):

    tp, tn, fp, fn = get_tp_fp(myhash_gtruth, myhash_pclass, 
                               obj_type, type_detector, thresh, mu, Sigma)

    precision, recall = None, None
    if(tp + fp == 0 or tp + fn == 0):
        pass
    else:
        precision = (tp*1.0) /((tp + fp)*1.0)
        recall = (tp*1.0) /((tp + fn)*1.0)
    
    return precision, recall

def get_precision_recall_all(myhash_gtruth, myhash_pclass, 
                             obj_type, type_detector, mu=None, Sigma=None):
    thresholds = arange(0, 1, 0.005)
    #thresholds = []

    if(type_detector=='prob_mrf'):
        thresholds = []
        for elt in myhash_pclass.keys():
            thresholds.append(myhash_pclass[elt])
        thresholds.sort()
    '''elif(type_detector=='prob_c1' or 
         type_detector=='prob_c2' or
         type_detector=='prob_c3'):
        for elt in myhash_pclass.keys():
            for det in myhash_pclass[elt]:
                if(not det[type_detector]*det['prob_im'] in thresholds):
                    thresholds.append(det[type_detector]*det['prob_im'])
        thresholds.sort()
    else:
        for elt in myhash_pclass.keys():
            for det in myhash_pclass[elt]:
                if(not det[type_detector] in thresholds):
                    thresholds.append(det[type_detector])
        thresholds.sort()'''

    precisions = []
    recalls = []
    #print "type_detector", type_detector

    #myskip = 20
    #i =0 
    for thresh in thresholds:
        #print i, myskip
        #if(not mod(i, myskip) == 0):
        #    i+=1
        #    continue
        #print thresh
        pr, re = get_precision_recall(myhash_gtruth, myhash_pclass, 
                                      obj_type, type_detector, 
                                      thresh, mu, Sigma)

        if(not pr == None and not re == None):
            precisions.append(pr)
            recalls.append(re)
            

            #print "threshold:", thresh, " precision:", pr, " recall:", re
        #i+=1

    recalls.reverse()
    precisions.reverse()
    
    area = 0
    for i in range(1, len(recalls)):
        #print "recalls", recalls[i] - recalls[i-1]
        #print "precision", precisions[i]

        area += abs(recalls[i-1] - recalls[i])*precisions[i-1]
        #raw_input()

    if(area == 0):
        for i in range(1, len(recalls)):
            area += abs(recalls[i-1] - recalls[i])*precisions[i]


    return precisions, recalls, area


def plot_roc(gtruth_filename, pclass_filename, obj_type, 
             mu_h=None, sigma_h=None, 
             mu_imwidth=None, mu_imheight=None, 
             sig_imwidth=None, sig_imheight=None,
             mu_disparity=None, sig_disparity=None):

    print "loading groundtruth"
    myhash_gtruth = load_groundtruth(gtruth_filename)
    print "loading pclassfile"
    myhash_pclass, myhash_pclass_jnt, myconfig = load_pclassfile(pclass_filename)
    
    Mu_h = None;    Sigma_h = None;
    Mu_width = None; Sig_width = None;
    Mu_disparity = None; Sig_disparity = None;

    if(mu_h != None):
        Mu_h = array([mu_h]); 
        Sigma_h = array([[sigma_h]])
    if(mu_imwidth != None):
        Mu_width = array([mu_imwidth, mu_imheight])
        Sig_width = array([[sig_imwidth, 0.0],[0.0, sig_imheight]])
    if(mu_disparity != None):
        Mu_disparity = array([mu_disparity])
        Sig_disparity = array([[sig_disparity]])
        
    
    myhash_pclass_new = get_new_hash(myhash_pclass,
                                     Mu_h, Sigma_h,
                                     Mu_width, Sig_width,
                                     Mu_disparity, Sig_disparity)
    
    print "c3"
    precision_c3, recall_c3, area_c3 = get_precision_recall_all(myhash_gtruth, 
                                                                myhash_pclass_new,
                                                                obj_type, "prob_c3")
    

    print "all"
    precision_all, recall_all, area_all = get_precision_recall_all(myhash_gtruth, 
                                                                   myhash_pclass_new, 
                                                                   obj_type, "prob_fin")

    print "image-only"
    precision_im, recall_im, area_im = get_precision_recall_all(myhash_gtruth, myhash_pclass_new, 
                                                                obj_type, "prob_im")

    print "c1"
    precision_c1, recall_c1, area_c1 = get_precision_recall_all(myhash_gtruth, 
                                                                myhash_pclass_new, 
                                                                obj_type, 
                                                                "prob_c1") 


    print "c2"
    precision_c2, recall_c2, area_c2 = get_precision_recall_all(myhash_gtruth, 
                                                                myhash_pclass_new, 
                                                                obj_type, "prob_c2")

    print "plotting"
    
    p1, = plot(recall_im, precision_im, 'g^-')
    p3, = plot(recall_c1, precision_c1, 'k>-')
    p4, = plot(recall_c2, precision_c2, 'ys-')
    p5, = plot(recall_c3, precision_c3, 'o-.')
    p2, = plot(recall_all, precision_all, 'b<-')


    #p6, = plot(recall_joint, precision_joint, 'bx-')
    xlabel("recall")
    ylabel("precision")

    legend((p1, p3, p4, p5, p2), ("image-only (AUC=%.3f)" % area_im, 
                                  "with size (AUC=%.3f)" % area_c1, 
                                  "with disparity (AUC=%.3f)" % area_c2, 
                                  "with height (AUC=%.3f)" % area_c3, 
                                  "all context (AUC=%.3f)" % area_all));
    
    copy_and_save_pclassfile(pclass_filename,
                             pclass_filename+".new", myhash_pclass_new)
    show()




if __name__ == "__main__":
    
    if(len(argv) == 4):
        plot_roc(argv[1], argv[2], argv[3])
    elif(len(argv) == 6):
        #just do the height
        plot_roc(argv[1], argv[2], argv[3],
                 float(argv[4]),float(argv[5]))
    elif(len(argv) == 8):
        #just do the height
        plot_roc(argv[1], argv[2], argv[3],None, None,
                 float(argv[4]),float(argv[5]),float(argv[6]),float(argv[7]))
    elif(len(argv) == 10):
        plot_roc(argv[1], argv[2], argv[3],
                 float(argv[4]),float(argv[5]),
                 float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]))
    elif(len(argv) == 12):
        plot_roc(argv[1], argv[2], argv[3],
                 float(argv[4]),float(argv[5]),
                 float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]),
                 float(argv[10]), float(argv[11]))
    else:
        print "usage:\n\tpython plot_roc.py groundtruthfile pablo_classifierfile obj_type [mu_height sig_height mu_imwidth mu_imheight sig_imwidth sig_imheight mu_disparity sig_disparity"



