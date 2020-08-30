from pylab import *
from classifier_util import *
from sorting import quicksort
from sys import argv
from math import fmod

def get_tp_fp(myhash_gtruth, myhash_pclass, 
              obj_type, type_detector, thresh):
    tp, fp = 0, 0
    tn, fn = 0, 0
    
    for imnum in myhash_gtruth.keys():
        
        if(not myhash_pclass.has_key(imnum)):
            #print "except"
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
            
            for det in myhash_pclass[imnum]:

                #print "testing detections"
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
            if(not isset and obj_type in gtruth):
                #this is a false negative
                fn += 1
            else:
                #this is a true negative
                tn += 1
        #print "doing something"

    return tp, tn, fp, fn

def prob_gaussian(x, mean, Sigma):
    val2 = exp((-1.0/2.0)*dot(dot(array([x-mean]), inv(Sigma)), transpose([x-mean])))[0][0]
    val1 = 1.0/(((2*pi)**(len(Sigma)/2.0)) * (det(Sigma)**0.5))

    val2_max = exp(0)
    val1_max = 1.0/(((2*pi)**(len(Sigma)/2.0)) * (det(Sigma)**0.5))

    return (val1*val2)/(val1_max*val2_max)


def get_roc_all(myhash_gtruth, myhash_pclass, 
                obj_type, type_detector):
    thresholds = arange(0, 1, 0.005)

    if(type_detector=='prob_mrf'):
        thresholds = []
        for elt in myhash_pclass.keys():
            thresholds.append(myhash_pclass[elt])
        thresholds.sort()

    tp_rate = []
    fp_rate = []
    print "type_detector", type_detector

    for thresh in thresholds:
        if(fmod(thresh, 0.01) == 0):
            print thresh

        tp, tn, fp, fn  = get_tp_fp(myhash_gtruth, myhash_pclass, 
                                    obj_type, type_detector, thresh)

        if(not tp == None and not fp == None and tp+fp > 0 and fp+tn > 0):
            tp_rate.append((tp*1.0)/(tp+fp)*1.0)
            fp_rate.append((fp*1.0)/(fp+tn)*1.0)
    

            print "threshold:", thresh, " tp:", tp_rate[-1], " fp:", fp_rate[-1]
            #raw_input()

    #sort the tp rates
    Vfp, I = quicksort(fp_rate)
    
    tp_rate = array(tp_rate)
    Vtp = tp_rate.take(I)
    
    area = 0
    for i in range(1, len(Vfp)):
        #print "recalls", recalls[i] - recalls[i-1]
        #print "precision", precisions[i]

        area += abs(Vtp[i-1] - Vtp[i])*Vfp[i-1]
        #raw_input()

    #if(area == 0):
    #    for i in range(1, len(recalls)):
    #        area += abs(recalls[i-1] - recalls[i])*precisions[i]


    return Vtp, Vfp, area



def plot_roc(gtruth_filename, pclass_filename, obj_type, 
             fzclass_filename=None, mrf_filename=None, gtruth_mrf=None):

    print "loading groundtruth"
    myhash_gtruth = load_groundtruth(gtruth_filename)
    print "loading pclassfile"
    myhash_pclass, myhash_pclass_jnt, myconfig = load_pclassfile(pclass_filename)



    #def get_roc_all(myhash_gtruth, myhash_pclass, 
    #            obj_type, type_detector):
    myhash_fz = None
    Vtp_fz, Vfp_fz, area_fz = [], [], []
    if(fzclass_filename != None):
        myhash_fz = load_fz(fzclass_filename)

        Vtp_fz, Vfp_fz, area_fz = get_roc_all(myhash_gtruth, 
                                                       myhash_fz, 
                                                       obj_type, "prob_im")
    if(mrf_filename != None):
        myhash_mrf = load_mrf_file(mrf_filename)
        mrf_gtruth = load_groundtruth(gtruth_mrf)
        Vtp_mrf, Vfp_mrf, area_mrf = get_roc_all(mrf_gtruth, 
                                                 myhash_mrf[obj_type], 
                                                 obj_type, "prob_mrf")

        raw_input()
        #print Vtp_mrf[0:100], Vfp_mrf[0:100]
        #raw_input()
    
    print "c3"
    Vtp_c3, Vfp_c3, area_c3 = get_roc_all(myhash_gtruth, myhash_pclass, 
                                                   obj_type, "prob_c3")
    

    print "image-only"
    Vtp_im, Vfp_im, area_im = get_roc_all(myhash_gtruth, myhash_pclass, 
                                                   obj_type, "prob_im")
    print "c1"
    Vtp_c1, Vfp_c1, area_c1 = get_roc_all(myhash_gtruth, myhash_pclass, 
                                                   obj_type, "prob_c1")
    print "c2"
    Vtp_c2, Vfp_c2, area_c2 = get_roc_all(myhash_gtruth, myhash_pclass, 
                                                   obj_type, "prob_c2")
    
    
    print "all"
    Vtp_all, Vfp_all, area_all = get_roc_all(myhash_gtruth, myhash_pclass, 
                                                      obj_type, "prob_fin")


    print "plotting"
    
    p1, = plot(Vfp_im, Vtp_im, 'g^-')
    p3, = plot(Vfp_c1, Vtp_c1, 'k>-')
    p4, = plot(Vfp_c2, Vtp_c2, 'ys-')
    p5, = plot(Vfp_c3, Vtp_c3, 'o-.')
    p2, = plot(Vfp_all, Vtp_all, 'b<-')

    xlabel(" false positive rate ")
    ylabel(" true positive rate ")

    if(Vtp_fz != [] and mrf_filename != None):
        p6, = plot(Vfp_fz, Vtp_fz, 'k+-')
        p7, = plot(Vfp_mrf, Vtp_mrf, 'ko-')
        legend((p1, p6, p3, p4, p5, p2, p7), ("image-only (AUC=%.3f)" % area_im, 
                                              "Felzenszwalb et. al. (AUC=%.3f)" % area_fz, 
                                              "with size (AUC=%.3f)" % area_c1, 
                                              "with disparity (AUC=%.3f)" % area_c2, 
                                              "with height (AUC=%.3f)" % area_c3, 
                                              "all physical (AUC=%.3f)" % area_all,
                                              "MRF (AUC=%.3f)" % area_mrf));
    elif(Vtp_fz != []):
        p6, = plot(Vfp_fz, Vtp_fz, 'k+-')
        legend((p1, p6, p3, p4, p5, p2), ("image-only (AUC=%.3f)" % area_im, 
                                          "Felzenszwalb et. al. (AUC=%.3f)" % area_fz, 
                                          "with size (AUC=%.3f)" % area_c1, 
                                          "with disparity (AUC=%.3f)" % area_c2, 
                                          "with height (AUC=%.3f)" % area_c3, 
                                          "all physical (AUC=%.3f)" % area_all));
    elif(mrf_filename != None):
        p6, = plot(Vfp_mrf, Vtp_mrf, 'k+-')
        legend((p1, p3, p4, p5, p2, p6), ("image-only (AUC=%.3f)" % area_im, 
                                          "with size (AUC=%.3f)" % area_c1, 
                                          "with disparity (AUC=%.3f)" % area_c2, 
                                          "with height (AUC=%.3f)" % area_c3, 
                                          "all physical (AUC=%.3f)" % area_all,
                                          "MRF (AUC=%.3f)" % area_mrf));
    else:
        legend((p1, p3, p4, p5, p2), ("image-only (AUC=%.3f)" % area_im, 
                                      "with size (AUC=%.3f)" % area_c1, 
                                      "with disparity (AUC=%.3f)" % area_c2, 
                                      "with height (AUC=%.3f)" % area_c3, 
                                      "all physical (AUC=%.3f)" % area_all));

    show()




if __name__ == "__main__":
    if(len(argv) == 4):
        plot_roc(argv[1], argv[2], argv[3])
    elif(len(argv) == 5):
        plot_roc(argv[1], argv[2], argv[3], argv[4])
    elif(len(argv) == 7):
        plot_roc(argv[1], argv[2], argv[3], mrf_filename=argv[5], gtruth_mrf=argv[6])
    elif(len(argv) == 8):
        plot_roc(argv[1], argv[2], argv[3], argv[4], argv[6], argv[7])
    else:
        print "usage:\n\tpython plot_roc.py groundtruthfile pablo_classifierfile obj_type [fz_file] [--mrf mrf_file mrf_gtruth]"



