from sorting import quicksort
from pyTklib import *
from spatial_features_cxx import math2d_dist
from pylab import *
from scipy import *
from routeDirectionCorpusReader import readSession
from tag_util import tag_file
from du.eval_util import get_region_to_topo_hash_containment
from du.dir_util import direction_parser_sdc
import numpy as na

def plot_markers_evenly(X, Y, thelabel, marker, color, linewidth, markerSep=5, 
                        markersize=140, linestyle="-"):
    """
    This function plots 
    """
    

    line, = plot(X, Y, color+linestyle, label="_nolegend_", 
                 linewidth=2.5)
    line.set_marker("None")

    import math2d

    markers = [p for p in math2d.stepAlongLine(line.get_xydata(), markerSep)]

    X = [x for x, y in markers]
    Y = [y for x, y in markers]
    try:
        points = scatter(X, Y, s=markersize, color=color, marker=marker,
                         label=thelabel, facecolor="white", zorder=10)
    except:
        print "color", color
        print "marker", marker
        raise

    return line


def plot_distance_curve_random(model, corpus_fn, gtruth_tag_fn, map_fn, color, 
                               marker, label='', linestyle="-",
                               region_to_topology=None):
    """
    Needs the viewpoints and stuff from the model. 
    """
    print "starting random"
    dsession =  readSession(corpus_fn, "none")
    if gtruth_tag_fn != None:
        tf = tag_file(gtruth_tag_fn, map_fn)
        topohash = get_region_to_topo_hash_containment(tf, model)
    else:
        topohash = region_to_topology
    Dists = []
    for elt in dsession:
        for i in range(len(elt.routeInstructions)):
            
            if(elt.columnLabels[i] is None):
                print "sentence", i, "was",elt.columnLabels[i]
                continue
            
            start_true, end_true = elt.columnLabels[i].split("to")
            start_true = str(start_true.strip())
            end_true = str(end_true.strip())
            iSlocTopo = topohash[start_true][0]
            iElocTopo = topohash[end_true][0]
            eloc = model.tmap_locs[iElocTopo]
            
            total_dist = 0.0
            for vp in model.viewpoints:
                topo, orient = vp.split("_")
                vp_loc = model.tmap_locs[float(topo)]
                total_dist += math2d_dist(vp_loc, eloc)
            
            expected_dist = total_dist / len(model.viewpoints)
            Dists.append(expected_dist)
    Y = []; X=[];
    for threshold in Dists:

        #get the ones above the threshold
        #print nonzero(array(Dists) > threshold)
        #print array(Dists) > threshold
        Itrue, = nonzero(array(Dists) <= threshold)
        
        Y.append(len(Itrue)/(1.0*len(Dists)))
        X.append(threshold)

    num_correct_at_threshold = len(nonzero(array(Dists) <= 10)[0])
    print "random less than 10 meters", num_correct_at_threshold,
    print "%.3f%%" % (num_correct_at_threshold /(1.0 * len(Dists)))
    print "sorting"
    X, I = quicksort(X)
    print "taking"
    Y=array(Y).take(I)
    print "plotting"

    if(X[0] > 0.0):
        Xf = [X[0]];Xf.extend(X);
        Yf = [0];Yf.extend(Y);
        X = Xf; Y=Yf;

    p = plot_markers_evenly(X, Y, label, marker, color, linewidth=2.5, linestyle=linestyle)
    xlabel('distance from destination (m)')
    ylabel('proportion correct')
    return p        

def plot_roc_curve(ofile):
    figure()
    probs_orig = ofile['probability']
    correctness_orig = ofile['correct_neigh']

    #get the probs
    probs = []; 
    for ps_i, ps in enumerate(probs_orig):
        if(not array(ps).max() is None):
            probs.append(array(ps).max())
        else:
            probs.append(0)

        #if(len(probs) == 0):
        #    print "is empty"
        #    raw_input()


    # get whether the question was correct
    correctness = []
    for crr in correctness_orig:
        if(True in crr):
            correctness.append(True)
        else:
            correctness.append(False)
            

    #root by the length of the path
    i = 0
    for elt in ofile['keywords']:
        print "test", elt
        print "after test"
        print "probs[i]=",probs[i]
        if(len(elt) > 0):
            probs[i] = pow(probs[i], 1/(1.0*len(elt)-1))
        else:
            probs[i]
        i+=1
        
    print "number correct:", sum(correctness)
    print "total directions:", len(correctness)
    TPR = []; FPR = []
    for threshold in probs:

        #get the ones above the threshold
        #print nonzero(array(probs) > threshold)
        #print array(probs) > threshold
        Itrue, = nonzero(array(probs) >= threshold)
        iscorrect = array(correctness).take(Itrue)

        TP = sum(iscorrect)*1.0
        TP_FP = len(iscorrect)*1.0
        FP = TP_FP - TP

        #get the ones below the threshold
        Ifalse, = nonzero(array(probs) <= threshold)
        is_not_correct = array(correctness).take(Ifalse)

        FN = sum(is_not_correct)*1.0
        TN_FN = len(is_not_correct)*1.0
        TN = TN_FN-FN

        TPR.append(1.0*TP / ((TP + FN)+0.00000000001))
        FPR.append(1.0*TN / ((TN + FP)+0.00000000001))
        

    V, I = quicksort(FPR)
    
    X = array(FPR).take(I)
    Y = array(TPR).take(I)

    plot(X, Y, 'r-', linewidth=2.5)
    #font = FontProperties(size='x-small')
    xlabel('false positive rate')
    ylabel('true positive rate')

    AUC = 0.0
    for i in range(len(X)-1):
        AUC+=(X[i+1]-X[i])*Y[i]
    
    title("AUC="+str(AUC))
    draw()
    #show()
    #raw_input()


def plot_distance_curve(ofile, corpus, marker, color, thelabel='',
                        use_strict_correctness=False,
                        followedState=None,
                        sentence_i_to_run=None, linestyle="-"):

    Dists = []
    threshold = 10
    num_correct = 0
    total = 0.0
    for i in range(len(ofile['path'])):
        if(ofile['sentences'][i] is None):
            print "sentence", i, "was",ofile['sentences'][i]
            continue
        
        rst, rend = ofile['regions'][i].split("to")
        rst = rst.strip()
        rend = rend.strip()

        direction = corpus.directions[i]

        if followedState != None and direction.was_followed != followedState:
            assert direction.start==rst, (direction.start, rst)
            assert direction.end==rend, (direction.end, rend)
            continue

        #print "r", ofile['region_to_topology']
        t2 = ofile['region_to_topology'][rend]
        
        #iterate over all the topologies in the final region
        curr_d = 70.0
        for myelt in t2:
            t2_loc = ofile['tmap_locs'][myelt]

        
            #iterate over all of the paths that end in the location
            for k in range(len(ofile['path'][i])):
                if ofile['path'][i][k] is None:
                    continue


                t1 = ofile['path'][i][k][-1]
                t1 = float(t1.split("_")[0])
                t1_loc = ofile["tmap_locs"][t1]
            
                if(math2d_dist(t2_loc, t1_loc) < curr_d):
                    curr_d = math2d_dist(t2_loc, t1_loc)

            if use_strict_correctness and sentence_i_to_run!=None:
                raise ValueError("Must pass one or the other and not both." + 
                                 `use_strict_correctness` + " and " + `sentence_i_to_run`)

            if use_strict_correctness or sentence_i_to_run!=None:
                if use_strict_correctness:
                    best_scoring_run_k = argmax(ofile['probability'][i])
                elif sentence_i_to_run != None:
                    best_scoring_run_k = sentence_i_to_run[myelt]
                    if ofile['path'][i][best_scoring_run_k] is None:
                        best_scoring_run_k = argmax(ofile['probability'][i])

                t1 = float(ofile['path'][i][best_scoring_run_k][-1].split("_")[0])
                t1_loc = ofile["tmap_locs"][t1]
                curr_d = math2d_dist(t2_loc, t1_loc)

        
        if curr_d < threshold or ofile['correct'][i][0]:
            num_correct += 1
        total += 1
        Dists.append(curr_d)


    all_visited_topos = []
    import cPickle
    model = cPickle.load(open(ofile["options"]["model_fn"], 'r'))
    print "len", len(ofile["visited_viewpoints"])
    for visited_vps in ofile["visited_viewpoints"]:
        assert len(visited_vps) == 1, len(visited_vps)
        
        visited_topos = set()
        for vp in visited_vps[0]:
            #print "vp", vp
            topo_i, orient = vp.split("_")
            visited_topos.add(topo_i)
        all_visited_topos.append(float(len(visited_topos))/len(model.tmap_locs))
    #print "visited", all_visited_topos
    #print "ofile", ofile["path"][0]
    print "average # of nodes visited", mean(all_visited_topos)
    print thelabel, "num_correct less than %.2f meters: %d  (%.3f%%), visited %.3f%%" % (threshold, num_correct, 100.0*num_correct/total, 100 * mean(all_visited_topos))
    Y = []; X=[];
    for threshold in Dists:

        #get the ones above the threshold
        #print nonzero(array(Dists) > threshold)
        #print array(Dists) > threshold
        Itrue, = nonzero(array(Dists) <= threshold)
        
        Y.append(len(Itrue)/(1.0*len(Dists)))
        X.append(threshold)
        
    X, I = quicksort(X)
    Y=array(Y).take(I)
    
    p = plot_markers_evenly(X, Y, thelabel, marker, color, linewidth=2.5, linestyle=linestyle)
    xlabel('distance from destination (m)')
    ylabel('proportion correct')
    #draw()
    #show()
    #raw_input()
    return p

def plot_distance_curve_subject(ofile, create_figure=True, 
                                mystyle=None, 
                                best_sub_only=False, best_question_only=False,
                                included_subjects=None):
    
    styles = ["ro-", "b^-", "k>-", "g<-", 
              "ro--", "b^--", "k>--", "g<--", 
              "ro-.", "b^-.", "k>-.", "g<-.",
              "ro:", "b^:", "k>:", "g<:"]
    if(create_figure):
        figure()
    Dists = {}
    Dists_question = {}
    for i in range(len(ofile['path'])):
        #Dists.append([])

        if(ofile['sentences'][i] is None):
            print "sentence", i, "was",ofile['sentences'][i]
            continue
        
        rst, rend = ofile['regions'][i].split("to")
        rend = rend.strip()
        
        t2 = ofile['region_to_topology'][rend]
        
        #iterate over all the topologies in the final region
        curr_d = 100000000000000000000000000000.0
        for myelt in t2:
            t2_loc = ofile['tmap_locs'][myelt]
        
            #iterate over all of the paths that end in the location
            for k in range(len(ofile['path'][i])):

                path = ofile['path'][i][k]
                if path is None:
                    curr_d = 100000000000000000
                else:
                        t1 = path[-1]
                        t1 = float(t1.split("_")[0])
                        t1_loc = ofile["tmap_locs"][t1]
                        if(math2d_dist(t2_loc, t1_loc) < curr_d):
                            curr_d = math2d_dist(t2_loc, t1_loc)
                        
        #subjects
        if(not Dists.has_key(ofile["subjects"][i])):
            Dists[ofile["subjects"][i]] = []

        Dists[ofile["subjects"][i]].append(curr_d)

        #regions
        if(not Dists_question.has_key(ofile["regions"][i])):
            Dists_question[ofile["regions"][i]] = []

        Dists_question[ofile["regions"][i]].append(curr_d)

        


    xlabel('distance from destination (m)')
    ylabel('percentage correct')

    mylabel = None
    if(best_sub_only):
        dvals = sum(Dists.values(), axis=1)
        i = argmin(dvals)
        new_vals = Dists.values()[i]
        new_key = Dists.keys()[i]

        Dists = {}
        Dists[new_key] = new_vals

        #mylabel=thelabel+" (Best Subject)"
        
    if(best_question_only):
        dvals = sum(Dists_question.values(), axis=1)
        i = argmin(dvals)
        new_vals = Dists_question.values()[i]
        new_key = Dists_question.keys()[i]
        
        Dists = {}
        Dists[new_key] = new_vals
        
        #mylabel=thelabel+" (Best Question)"

    plots = []
    for k,subject in enumerate(Dists.keys()):
        if included_subjects != None and not subject in included_subjects:
            continue
        Y = []; X=[];
        for threshold in Dists[subject]:
            #get the ones above the threshold

            Itrue, = nonzero(array(Dists[subject]) <= threshold)
        
            Y.append(len(Itrue)/(1.0*len(Dists[subject])))
            X.append(threshold)
            
        X, I = quicksort(X)
        Y=array(Y).take(I)
        sub_plt = subject.replace("Subject", "Sub.")
        if mystyle is None:
            style = styles[k % len(styles)]
        else:
            style = mystyle

        if(X[0] > 0.0):
            Xf = [X[0]];Xf.extend(X);
            Yf = [0];Yf.extend(Y);
            X = Xf; Y=Yf;

        plots.extend(plot(X, Y, style, label=sub_plt, linewidth=2.5))

        num_correct_at_threshold = len(nonzero(array(Dists[subject]) <= 10)[0])
        print k, subject, "less than 10 meters", num_correct_at_threshold,
        print "%.3f%%" % ((100.0*num_correct_at_threshold) /(1.0 * len(Dists[subject])))
    return plots

    
def plot_string_edit_curve(ofile):
    figure()
    ed = ofile["edit_distance"] 

    D ={}
    print "getting edit dist"
    for edit_dist in ed:
        if(array(edit_dist).min() > 1000):
            continue
        if(D.has_key(array(edit_dist).min())):
            D[array(edit_dist).min()]+=1
        else:
            D[array(edit_dist).min()]=1
    
    #V, I = quicksort(D.values())
    #K = array(D.keys()).take(I)
    
    X = range(array(D.keys()).max())
    Y = []
    for key in X:
        if(key is None):
            continue
        if(D.has_key(key)):
            v = D[key]
        else:
            v = 0
        Y.append(v)

    print "plotting edit dist"
    #plot(X, Y, 'rx-', linewidth=1.5)
    print X
    print Y
    bar(X, Y, 0.5, color='k')
    xlabel("Edit Distance")
    ylabel("Number of Paths")
    draw()
    


def correct_at_threshold(results, threshold=10):
    result = []

    for i, paths in enumerate(results['path']):
        t1_loc = results["end_regions"][i] 
        t1_loc = (t1_loc[0][0], t1_loc[1][0])

        correct = False
        for path in paths:
            t2_i = float(path[-1].split("_")[0])
            t2_loc = results["tmap_locs"][t2_i]
            curr_d = math2d_dist(t2_loc, t1_loc)
            if curr_d < 10:
                correct = True
                break
        result.append(correct)
    return result

def plot_performance_with_num_spatial_relations(model, results):
    threshold = 10
    correct = correct_at_threshold(results, threshold)


    sdc_parser = direction_parser_sdc()
    #sdc_parser = direction_parser_wizard_of_oz(results['corpus_fname'], 'stefie10')

    subject_to_sr = {}

    subject_to_num_correct = {}
    
    total_sdcs = 0.0
    total_sr_sdcs = 0.0
    total_landmark_sdcs = 0.0

    total_sentences = 0.0
    total_raw_sdcs = 0.0
    total_raw_sr_sdcs = 0.0
    total_raw_landmark_sdcs = 0.0

    for i, paths in enumerate(results['path']):
        sentence = results["sentences"][i]
        total_sentences += 1
        subject = results["subjects"][i]        

        sdcs = sdc_parser.extract_SDCs(sentence)
        for sdc in sdcs:
            total_raw_sdcs += 1
            if not sdc["spatialRelation"].isNull():
                total_raw_sr_sdcs += 1
            if not sdc["landmark"].isNull():
                total_raw_landmark_sdcs += 1
        
        usable_sdcs = model.get_usable_sdc(sdcs)
        
        sr_count = 0.0
        for sdc in usable_sdcs:
            total_sdcs += 1
            print "sr", sdc["sr"]
            #if sdc["sr"] != None and sdc["sr"] in ["to", "past", "through"]:
            if sdc["sr"] != None:
                total_sr_sdcs += 1
                sr_count += 1
            if sdc["landmark"] != None:
                total_landmark_sdcs += 1
            
        key = str(i)
        #key = subject
        subject_to_sr.setdefault(key, [])
        subject_to_sr[key].append(sr_count / len(usable_sdcs))

        subject_to_num_correct.setdefault(key, 0)
        subject_to_num_correct[key] += correct[i]
        

    X = []
    Y = []
    label_map = {}
    for subject in subject_to_sr.keys():
        x = na.mean(subject_to_sr[subject])
        y = subject_to_num_correct[subject]
        X.append(x)
        Y.append(y)
        pt = (x, y)

        label = subject.replace("Subject", "")
        label_map.setdefault(pt, [])
        label_map[pt].append(label)

    for location, labels in label_map.iteritems():
        x, y = location
        y_curr = y
        for label in labels:
            mpl.text(x, y_curr, label)
            y_curr += 0.05
        
    mpl.scatter(X, Y)
    mpl.xlabel("Average # of spatial relations")
    mpl.ylabel("Number correct at %.0f meters" % threshold)
    print "average utilized sdcs", total_sdcs / total_sentences
    print "average utilized sr sdcs", total_sr_sdcs / total_sentences
    print "average utilized landmark sdcs", total_landmark_sdcs / total_sentences

    print "average raw sdcs", total_raw_sdcs / total_sentences
    print "average raw sr sdcs", total_raw_sr_sdcs / total_sentences
    print "average raw landmark sdcs", total_raw_landmark_sdcs / total_sentences
    
    mpl.show()
