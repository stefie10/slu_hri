from sys import argv
from routeDirectionCorpusReader import readSession
import cPickle
from tag_util import *
from du.eval_util import *
import math2d

if __name__=="__main__":
    sentence_fn = argv[1]
    dg_cache_fn = argv[2]
    gtruth_tag_fn = argv[3]
    map_fn = argv[4]
    dsession =  readSession(sentence_fn, "none")
    dg_model = cPickle.load(open(dg_cache_fn, 'r'))
    sent_num = 0
    tf = tag_file(gtruth_tag_fn, map_fn)
    topohash = get_region_to_topo_hash_containment(tf, dg_model)
    
    total_length = 0.0

    for elt in dsession:
        for i in range(len(elt.routeInstructions)):
            sentence = elt.routeInstructions[i]
            start_true, end_true = elt.columnLabels[i].split("to")
            start_true = start_true.strip()
            end_true = end_true.strip()
            sloc = topohash[start_true][0]
            eloc = topohash[end_true][0]


            print "sloc", sloc
            print "eloc", eloc

            sloc_point = dg_model.tmap_locs[float(sloc)]
            eloc_point = dg_model.tmap_locs[float(eloc)]

            X, Y = dg_model.clusters.skel.compute_path(sloc_point, eloc_point)
            path = [(x, y) for x, y in zip(X, Y)]
            length = math2d.length(path)

            total_length += length
            
            slocs = dg_model.vpts_for_topo(float(sloc))
            elocs = dg_model.vpts_for_topo(float(eloc))


            print "sent_num", sent_num
            print "subject", elt.subject
            print "region", elt.columnLabels[i]
            print "start", sloc

            print "sentence", sentence
            print "slocs", slocs
            print "elocs", elocs
            print
            sent_num += 1
    print "average route length: ", total_length / sent_num
