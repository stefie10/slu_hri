from copy import deepcopy
from ans_util import *

#look at the model. If in the ground truth path such thing exist then yes.

def allways_truthful(best_question, m4du, sdcs, topN_paths, orig_path):
    if best_question.meta_data[0]=="SDC_L":
        ans, dist = answer_from_distribution(allways_truthful_SDC_L(best_question, m4du, sdcs, topN_paths, orig_path))
        return ans, dist

    #if the type is not recognized return None
    return None


def allways_truthful_SDC_L(best_question, m4du, sdcs, topN_paths, orig_path):

#    orig_locations =[m4du.viewpoints.take(vp_i) for vp_i in orig_path]

    # this line in formal code
    all_landmarks = deepcopy(m4du.m4du.lmap_cache.tagnames)
    # the topological keys
    # todo these are topo_keys, not viewpoints
    topo_keys = orig_path
#    topo_keys = [float(m4du.m4du.viewpoints[vp_i].split("_")[0]) for vp_i in orig_path]
    # list of items for every location on the path
#    print "Topo_keyzz", topo_keys
    items_in_location = [ filter(lambda x: x in vtags,all_landmarks) for vtags in [m4du.m4du.topo_key_to_vtags[topo_key] for topo_key in topo_keys]]

    found = False
    sdc_keyword = best_question.meta_data[1]["landmark"]
    landmark = best_question.meta_data[2]
    for room in items_in_location:
        if sdc_keyword!=None:
            if sdc_keyword in room and landmark in room:
                found = True
                break
        else:
            if landmark in room:
                found = True
                break
            

    if found:
        return {"yes":1.0}
    else:
        return {"no":1.0}


	
	
