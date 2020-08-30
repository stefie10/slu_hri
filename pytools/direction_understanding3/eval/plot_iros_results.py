from pyTklib import *
from scipy import *
from sorting import quicksort
import pylab as mpl
from du.plot_utils import plot_distance_curve, plot_distance_curve_random, plot_distance_curve_subject, plot_markers_evenly
import cPickle
from plot_distance_curves import loadCorpus
from du.eval_util import get_region_to_topo_hash_containment
from tag_util import tag_file
from routeDirectionCorpusReader import readSession


def main():
    mpl.figure(figsize=(7, 5))
    #ofile = cPickle.load(open("data/directions/direction_floor_1_3d/output/iros_presentation_runs/helicopter_offline.output_7.pck", 'r'))  # actual ground truth
    ofile = cPickle.load(open("data/directions/direction_floor_1_3d/output/helicopter_offline.output_9.pck", 'r'))  # actual ground truth
    model = cPickle.load(open("data/directions/direction_floor_1_3d/models/helicopter_offline.pck"))

    #ofile['region_to_topology'] = get_region_to_topo_hash_containment(model.tag_file, model)

    tf = tag_file("data/directions/direction_floor_1_3d/tags/df1_small_tags.tag", 
                  "data/directions/direction_floor_1_3d/direction_floor_1_small.cmf")

    corpus = loadCorpus(ofile["corpus_fname"])
    plot_distance_curve_iros(ofile, corpus, tf, "+", "r", thelabel="Overall",
                             followedState=None, linestyle="--")

    plots = plot_distance_curve_subject_iros(ofile, tf, create_figure=False,
                                        mystyle="k")
    
    for plot in plots:
        plot.set_label("_nolgend_")
    plots[0].set_label("Subjects")
    
    plot_distance_curve_random_iros(model, 
                                    ofile["corpus_fname"],
                                    tf.tag_filename,
                                    tf.map_filename,
                                    color="b", marker="p", label="Random",
                                    region_to_topology=ofile["region_to_topology"]
                                    )

    mpl.axis((0, 35, 0, 1))
    mpl.legend(loc="upper left")
    mpl.title("Performance on a Corpus of Instructions for a MAV")
    mpl.ylabel("Proportion\nwithin $x$ m\nof the true\ndestination",
               rotation="horizontal")
    mpl.subplots_adjust(left=0.24)
    
    mpl.show()


def plot_distance_curve_iros(ofile, corpus, tag_file, marker, color, thelabel='',
                             use_strict_correctness=False,
                             followedState=None,
                             sentence_i_to_run=None, linestyle="-"):

    Dists = []
    threshold = 10
    num_correct = 0
    total = 0.0
    for i in range(len(ofile['path'])):
        if(ofile['sentences'][i] == None):
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


        #t2 = ofile['region_to_topology'][rend]
        
        #iterate over all the topologies in the final region
        curr_d = 70.0
        t2_loc = transpose(tag_file.get_tag_locations(rend))[0]
        
        
        #for myelt in t2:
        #    t2_loc = ofile['tmap_locs'][myelt]
        
        #iterate over all of the paths that end in the location
        for k in range(len(ofile['path'][i])):
            if ofile['path'][i][k] == None:
                continue
            

            t1 = ofile['path'][i][k][-1]
            t1 = float(t1.split("_")[0])
            t1_loc = ofile["tmap_locs"][t1]

            if(tklib_euclidean_distance(t2_loc, t1_loc) < curr_d):
                curr_d = tklib_euclidean_distance(t2_loc, t1_loc)

        if use_strict_correctness and sentence_i_to_run!=None:
            raise ValueError("Must pass one or the other and not both." + 
                             `use_strict_correctness` + " and " + `sentence_i_to_run`)

        if use_strict_correctness or sentence_i_to_run!=None:
            if use_strict_correctness:
                best_scoring_run_k = argmax(ofile['probability'][i])
            elif sentence_i_to_run != None:
                best_scoring_run_k = sentence_i_to_run[myelt]
                if ofile['path'][i][best_scoring_run_k] == None:
                    best_scoring_run_k = argmax(ofile['probability'][i])

            t1 = float(ofile['path'][i][best_scoring_run_k][-1].split("_")[0])
            t1_loc = ofile["tmap_locs"][t1]
            curr_d = tklib_euclidean_distance(t2_loc, t1_loc)

        
        if curr_d < threshold or ofile['correct'][i][0]:
            num_correct += 1
        total += 1
        Dists.append(curr_d)

    print thelabel, "num_correct less than %.2f meters: %d  (%.3f%%)" % (threshold, num_correct, 100.0*num_correct/total)
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
    mpl.xlabel('distance from destination (m)')
    mpl.ylabel('proportion correct')
    #draw()
    #show()
    #raw_input()
    return p



def plot_distance_curve_subject_iros(ofile, tag_file, create_figure=True, 
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

        if(ofile['sentences'][i] == None):
            print "sentence", i, "was",ofile['sentences'][i]
            continue
        
        rst, rend = ofile['regions'][i].split("to")
        rend = rend.strip()
        
        #t2 = ofile['region_to_topology'][rend]
        #iterate over all the topologies in the final region
        curr_d = 100000000000000000000000000000.0
        #for myelt in t2:
        #t2_loc = ofile['tmap_locs'][myelt]
        t2_loc = transpose(tag_file.get_tag_locations(rend))[0]
        
        #iterate over all of the paths that end in the location
        for k in range(len(ofile['path'][i])):

            path = ofile['path'][i][k]
            if path == None:
                curr_d = 100000000000000000
            else:
                    t1 = path[-1]
                    t1 = float(t1.split("_")[0])
                    t1_loc = ofile["tmap_locs"][t1]
                    if(tklib_euclidean_distance(t2_loc, t1_loc) < curr_d):
                        curr_d = tklib_euclidean_distance(t2_loc, t1_loc)
                        
        #subjects
        if(not Dists.has_key(ofile["subjects"][i])):
            Dists[ofile["subjects"][i]] = []

        Dists[ofile["subjects"][i]].append(curr_d)

        #regions
        if(not Dists_question.has_key(ofile["regions"][i])):
            Dists_question[ofile["regions"][i]] = []

        Dists_question[ofile["regions"][i]].append(curr_d)

        


    mpl.xlabel('distance from destination (m)')
    mpl.ylabel('percentage correct')

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
        if mystyle == None:
            style = styles[k % len(styles)]
        else:
            style = mystyle

        if(X[0] > 0.0):
            Xf = [X[0]];Xf.extend(X);
            Yf = [0];Yf.extend(Y);
            X = Xf; Y=Yf;

        plots.extend(mpl.plot(X, Y, style, label=sub_plt, linewidth=2.5))

        num_correct_at_threshold = len(nonzero(array(Dists[subject]) <= 10)[0])
        print "subject:", subject, "less than 10 meters", num_correct_at_threshold,
        print "%.3f%%" % ((100.0*num_correct_at_threshold) /(1.0 * len(Dists[subject])))
    return plots


def plot_distance_curve_random_iros(model, corpus_fn, gtruth_tag_fn, map_fn, color, 
                                    marker, label='', linestyle="-",
                                    region_to_topology=None):
    """
    Needs the viewpoints and stuff from the model. 
    """
    print "starting random"
    dsession =  readSession(corpus_fn, "none")
    #if gtruth_tag_fn != None:
    #    tf = tag_file(gtruth_tag_fn, map_fn)
    #    topohash = get_region_to_topo_hash_containment(tf, model)
    #else:
    tf = tag_file(gtruth_tag_fn, map_fn)
    topohash = region_to_topology
    Dists = []
    for elt in dsession:
        for i in range(len(elt.routeInstructions)):
            
            if(elt.columnLabels[i] == None):
                print "sentence", i, "was",elt.columnLabels[i]
                continue
            
            start_true, end_true = elt.columnLabels[i].split("to")
            start_true = str(start_true.strip())
            end_true = str(end_true.strip())
            iSlocTopo = topohash[start_true][0]
            #iElocTopo = topohash[end_true][0]
            #eloc = model.tmap_locs[iElocTopo]
            eloc = transpose(tf.get_tag_locations(end_true))[0]
            
            total_dist = 0.0
            for vp in model.viewpoints:
                topo, orient = vp.split("_")
                vp_loc = model.tmap_locs[float(topo)]
                total_dist += tklib_euclidean_distance(vp_loc, eloc)
            
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
    mpl.xlabel('distance from destination (m)')
    mpl.ylabel('proportion correct')
    return p        


if __name__=="__main__":
    main()


