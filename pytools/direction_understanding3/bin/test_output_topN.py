# Quick and dirty way to see the output of the topN paths.
import cPickle
from pprint import pprint
from pylab import *


def test_topN(output_fn,sentence_number=0):
    
    if sentence_number in [None, ""]:
        sentence_number=0
    else:
        sentence_number=int(sentence_number)
    
    SN = sentence_number
    save_data = cPickle.load(open(output_fn, 'r'))
    
    prob_changes = 0
    path_changes = 0
    dest_changes = 0 
    possible_improvement = 0
    num_true_paths_in = 0
    num_possible_correct_changes = 0
    simplified_data = []
    num_sentences = 0
    
    for SN in range(150):
        #the set of paths
        if save_data["paths_topN"][SN] == None:
        	print num_sentences
        	continue
        num_sentences += 1
        aba = unique([str(unique(save_data["paths_topN"][SN][i])) for i in range(5)])
        #the set of destinations
        bab = unique([str(save_data["paths_topN"][SN][i][-1]) for i in range(5)])
        does_prob_change = bool(save_data["probability_topN"][SN][0] != save_data["probability_topN"][SN][4])
        if does_prob_change:
            prob_changes += 1
            if len(aba) != 1:
#                print "ABA ",len(aba),"\n"
#                for i in range(len(aba)):
#                    print aba[i] 
                path_changes += 1
            if len(bab) != 1:
                dest_changes += 1
#                print "SENT NUMBER ",SN,"-----------------------"
#                for i,path in enumerate(save_data["paths_topN"][SN]):
#                    print unique(path), save_data["probability_topN"][SN][i]
            if len(aba) == 0:
                print "ABA:",aba
                pprint([str(unique(save_data["paths_topN"][SN][i])) for i in range(5)])
                return
                
        was_it_correct = save_data["correct"][SN][0]
        
        #can we improve actually?
        #if any of the end locations is in the end regions:

        orig_path = save_data["orig_path"][SN]
        topohash = save_data["region_to_topology"]
        can_we_improve_actually = False
        for dest in bab:
#            print dest
            meant_destination = orig_path[-1]
            true_regions = None
            for region in topohash.keys():
                if meant_destination in topohash[region]:
                    true_regions = topohash[region]
                    break
            dest_vp_topo_loc= float(dest.split("_")[0])
            if dest_vp_topo_loc in true_regions:
                can_we_improve_actually = True
                num_true_paths_in += 1
                break
            else:
                pass
#                print "Not the same? ",dest_vp_topo_loc, orig_path[-1]

        can_we_improve_eventually = bool((not was_it_correct) and can_we_improve_actually )

        if can_we_improve_eventually:
            possible_improvement += 1
        
            
        prob_dist = save_data["probability_topN"][SN]
        
        simplified_data.append((does_prob_change, len(aba), len(bab), was_it_correct, can_we_improve_eventually, can_we_improve_actually, area_under_curve(prob_dist), fst_vs_snd(prob_dist) ))
        if was_it_correct and not can_we_improve_actually:
            print "Strange one: ", orig_path[-1], bab

    aba_dist= [a[1] for a in simplified_data]
    bab_dist= [a[2] for a in simplified_data]   
                
    print "Number of sentences ",num_sentences
    print "Prob Changes ",prob_changes
    print "Path Changes ",path_changes, mean(aba_dist), stdev(aba_dist)
    print "Dest Changes ",dest_changes, mean(bab_dist), stdev(bab_dist)
    print "Possible improvement (in best case) ",possible_improvement
    print "Num True destinations in ", num_true_paths_in
    print "Simplified Data"
#    pprint(simplified_data)
#    pprint(save_data["regions"])

#    hist(bab_dist,5)
#    show()
        
    
def mean(lst):
    return (sum(lst)+0.0)/len(lst)
    
def var(lst):
    mu = mean(lst)
    return (sum(map(lambda x: float((x-mu)**2),lst))+0.0)/len(lst)

def stdev(lst):
    return sqrt(var(lst))
    
def unique(lst):
    from sets import Set
    if len(lst)==0:
        return []
    return list(Set(lst))

####### CONFIDENCE SCORES : ##########
def normalize(dst):
	sm = sum(dst)
	dst2 = [ val/sm for val in dst ]
	return dst2

# adding them up, area_under_curve
def area_under_curve(dst):
	dst2 = normalize(sorted(dst,reverse=True))
	sm = 0
	auc = 0
	for i in range(len(dst2)):
		sm += dst2[i]
		auc += sm - (i+0.0)/len(dst2)
	return auc

def fst_vs_snd(dst):
	fst = dst[0]
	snd = dst[1]
	return (fst-snd +0.0)/fst
	



def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: test_output_topN.py [options] output_fn")
    parser.add_option("--sentence_number", type="string")
    
    (options, args) = parser.parse_args()
    print "args", args
    print "options", options.__dict__
    test_topN(*args, **options.__dict__)




if __name__=="__main__":
    main()
