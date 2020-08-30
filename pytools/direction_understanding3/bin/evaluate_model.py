from copy import deepcopy
import copy as cpcp
from du.dir_util import direction_parser_wizard_of_oz, direction_parser_sdc
from du.eval_util import get_region_to_topo_hash_containment, \
    get_topological_paths_hash, get_output_filename, string_edit_distance
from du.eval_util import get_orientations_each, get_orientations_all, get_orientations_annotated
from du.explore_util import infer_explore
from du.inference import greedy, last_sdc, topN
from du.regression_runner import current_svn_revision
from du.srel_utils import ProcessPool
from numpy import argmax, copy, zeros, radians, transpose
from numpy import *
from pyTklib import kNN_index
from routeDirectionCorpusReader import readSession
from tag_util import tag_file
import cPickle
import os
import time

class EvaluationError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)

def runSentence(*args):
    try:
        global evaluator
        return evaluator.runSentence(*args)
    except Exception, e:
        e.args = e.args + (args,)
        raise


def initialize_save_data():
    save_data = {}
    save_data["sentences"] = []
    save_data["regions"] = []
    save_data["start_regions"] = []
    save_data["end_regions"] = []
    save_data["subjects"] = []
    save_data["keywords"] = []
    save_data["keywords_orient"] = []
    save_data["path"] = []
    save_data["visited_viewpoints"] = []
    save_data["orig_path"] = []
    save_data["correct"] = []
    save_data["correct_neigh"] = []
    save_data["probability"] = []
    save_data["edit_distance"] = []
    save_data["do_exploration"] = None
    save_data["paths_topN"] = []
    save_data["probability_topN"] = []
    return save_data

class Evaluator:
    def __init__(self, corpus_fn, model_fn, gtruth_tag_fn, map_fn, output_dir, options, 
                 evaluation_mode="specialized", 
                 num_to_run=None, is_sum_product=False, num_align=None,
                 no_spatial_relations=False, do_exploration=False, quadrant_number=None,
                 wizard_of_oz_sdcs=None, run_description=None, inference="global", topN_num_paths=None,num_explorations=None,exploration_heuristics_name=None, parameters=None):
        print "num_to_run", num_to_run
        print "options", options
        options["model_fn"] = model_fn
        options["corpus_fn"] = corpus_fn
        options["gtruth_tag_fn"] = gtruth_tag_fn
        if inference == "":
            inference = "global"
            options["inference"]=inference
        self.range_to_run = None
        if num_to_run == "":
            num_to_run = None
        elif type(num_to_run)==type("abc") and num_to_run.find(":")!=-1:
            range_from = int(num_to_run.split(":")[0])
            range_to = int(num_to_run.split(":")[1])
            self.range_to_run = range(range_from,range_to)
            num_to_run = range_to
        elif num_to_run != None:
            num_to_run = int(num_to_run)

        if type(num_to_run) == type(1) and self.range_to_run==None:
            self.range_to_run = range(num_to_run)
        if self.range_to_run == None:
            #running all of them.
            if(quadrant_number==None):
                self.dsession = readSession(corpus_fn, "none")
            else:
                self.dsession = readSession(corpus_fn, "none", quadrant=int(quadrant_number))
            self.range_to_run = []
            sent_num_i = 0
            for elt in self.dsession:
                for i in range(len(elt.routeInstructions)):
                    self.range_to_run.append(sent_num_i)
                    sent_num_i += 1

        if num_explorations in [None, ""]:
            num_explorations=50
        else:
            num_explorations=int(num_explorations)                
                
        self.options = options
        self.output_dir = output_dir
        self.inference = inference

        self.num_align = num_align
        self.num_to_run = num_to_run
        self.is_sum_product = is_sum_product
        self.num_align = num_align

        if run_description == None:
            run_description = model_fn
            if inference !=None:
                run_description += " " + run_description
            if no_spatial_relations:
                run_description += " -sr"
            else:
                run_description += " +sr"
        self.run_description = run_description
        
            

        if(quadrant_number==None):
            self.dsession = readSession(corpus_fn, "none")
            #res = raw_input("running all examples!  Continue?")
            #if(res.lower() == 'n' or res.lower() == "no"):
            #    sys.exit(0);
        else:
            self.dsession = readSession(corpus_fn, "none", quadrant=int(quadrant_number))
        
        self.dg_model = cPickle.load(open(model_fn, 'r'))
        self.dg_model.use_spatial_relations = not no_spatial_relations
        
        if inference == "greedy":
            self.dg_model = greedy.model(self.dg_model)
        elif inference == "last_sdc":
            self.dg_model = last_sdc.model(self.dg_model)
        elif inference == "topN":
            if topN_num_paths == None or topN_num_paths=="":
                self.topN_num_paths = 10
            else:
                self.topN_num_paths = int(topN_num_paths)
            self.dg_model = topN.model(self.dg_model,self.topN_num_paths)
        elif inference == "global":
            pass
        else:
            raise ValueError("Bad inference value: " + inference)
        
        #self.do_exploration = eval(str(do_exploration))
        self.do_exploration = do_exploration
        
        if evaluation_mode == "best_path":
            self.orient = get_orientations_each
        elif evaluation_mode == "max_prob":
            self.orient = get_orientations_all
        elif evaluation_mode == "specialized":
            self.orient = get_orientations_annotated
        else:
            raise ValueError("Unexpected mode: " + `evaluation_mode`)
        #this will load the srel_mat
        #if(isinstance(self.dg_model, model4_du.model4_du)):
        print "loading srel_mat"
        self.dg_model.initialize()
    
        #open the ground truth file
        self.tf = tag_file(gtruth_tag_fn, map_fn)
        self.gtruth_tag_fn = gtruth_tag_fn
        
        #map the topological regions to teh ground truth regions
        self.topohash = get_region_to_topo_hash_containment(self.tf, self.dg_model)

        print "getting topological paths"
        self.topo_graph_D = get_topological_paths_hash(self.dg_model.clusters)
        #cPickle.dump(self.topo_graph_D, open("topo_graph_D", "wb"), 2)
        #self.topo_graph_D = cPickle.load(open("topo_graph_D", "r"))
        
        if wizard_of_oz_sdcs != None:
            print "using wizard", wizard_of_oz_sdcs
            self.sdc_parser = direction_parser_wizard_of_oz(corpus_fn, wizard_of_oz_sdcs)
        else:
            print "using crfs"
            self.sdc_parser = direction_parser_sdc()
        
        if num_explorations in [None, ""]:
            #TODO replace 2 by the branching factor or something else.
            self.num_explorations=len(self.dg_model.tmap_locs.keys()) / 2
        else:
            self.num_explorations=int(num_explorations)
            
        if exploration_heuristics_name in [None,""]:
            self.exploration_heuristics_name = "lifted_stairs"
        else:
            self.exploration_heuristics_name = exploration_heuristics_name
            
        if self.exploration_heuristics_name == "slope_offset_delay":
            if parameters not in [None, ""]:
                params_str = parameters.split(":")  
                if len(params_str)==3:
                    self.params_num = map(float,params_str)
                else:
                    self.params_num = None
        else:
            self.params_num = None
        





    def get_singly_connected_topologies(self, tmap):
        ret_keys = []
        for key in tmap.keys():
            if(len(tmap[key]) == 1):
                ret_keys.append(key)
        
        return ret_keys



            



    def evaluateParallel(self):
        save_data = initialize_save_data()
        save_data["tmap"] = self.dg_model.tmap
        save_data["tmap_locs"] = self.dg_model.tmap_locs
        save_data["tmap_graph_D"] = self.topo_graph_D
        save_data["region_to_topology"] = self.topohash
        save_data["corpus_fname"] = self.dsession.fname
        save_data["run_description"] = self.run_description
        save_data["options"] = self.options
        calls = []
        sent_number = 0
        
        for elt in self.dsession:
            if self.num_to_run != None and sent_number >= self.num_to_run:
                break
            for i in range(len(elt.routeInstructions)):
                if self.num_to_run != None and sent_number >= self.num_to_run:
                    break

                if self.range_to_run==None or sent_number in self.range_to_run:
                    sentence = elt.routeInstructions[i]

                    #print "sentence:", sentence

                    startRegionTag = elt.startRegionTags[i]
                    endRegionTag= elt.endRegionTags[i]
                    
                    desc = "%d ``%s''" % (sent_number, sentence)
                    calls.append((desc, runSentence, (sent_number, sentence, 
                                                      startRegionTag, endRegionTag,
                                                      elt.subject,
                                                      elt.columnLabels[i])))
                        
                sent_number += 1
        numcors = os.sysconf('SC_NPROCESSORS_ONLN')
        #numcors = 1
        
        print "running with", numcors, "cores"
        pool = ProcessPool(calls, numcors)
        totalExamples = pool.jobSize
        print "starting call"
        #calls[0][1](*calls[0][2])
        pool.start()
        startTime = time.time()
        processedExamples = 0.0
        correctCount = 0.0
        first = True
        while processedExamples < totalExamples:
            result = pool.doneQueue.get()
            #desc, func, args = calls[int(processedExamples)]
            #result = func(*args)
            if "exception" in result:
                pool.terminate()
                raise EvaluationError("Exception in one of the worker threads: " + result["exception"])
            processedExamples += 1
            was_correct = result["was_correct"]
            if was_correct:
                correctCount += 1
            del result["was_correct"]
            sent_number = result["sent_number"]
            del result["sent_number"]
            
            if first:
                for key, value in result.iteritems():
                    save_data[key] = [None for x in range(0, max(self.range_to_run)+1)]
                first = False
            for key, value in result.iteritems():
                #if(type(value) == bool):
                #print "key:", key
                #print "value:", value
                if(key == "do_exploration"):
                    save_data[key][sent_number] = value
                else:
                    #print "key", key
                    #print "value", value
                    #print "length", len(value)

                    if len(value) == 1:
                        save_data[key][sent_number] = value[0]
                    else:
                        assert len(value) == 0, (key, value, sent_number)


            now = time.time()
            progress = processedExamples/totalExamples
            elapsedMinutes = (now - startTime) / 60.0
            estimatedTotal = elapsedMinutes / progress
            
            
            print "got", correctCount, "of", processedExamples, "so far."
            print "progress: %.2f%%" % (progress * 100.0),
            print "(going for %.2f minutes," % elapsedMinutes,
            print "about %.2f minutes remaining)" % (estimatedTotal - elapsedMinutes)
            outfilename = get_output_filename(self.output_dir,self.dg_model)
                       
        print "saving data", outfilename
        cPickle.dump(save_data, open(outfilename, 'w'))
        return correctCount, outfilename

    def runSentence(self, sent_number, 
                    sentence, startRegionTag, endRegionTag,
                    subject, region):
        print
        print "-->SENT:", sent_number, ":", sentence
        

        save_data = initialize_save_data()
        save_data["do_exploration"] = self.do_exploration

        #convert the start region into a location in the topology
        #  there may be multiple possible start locations... choose
        #  the closest one
        sloc = self.dg_model.tmap_locs[self.topohash[startRegionTag][0]]

        #want to convert from a region to a topo map location
        #keywords, kw_direction = parse_sentence(sentence, self.dg_model)

        print "creating SDC"
        keywords = self.sdc_parser.extract_SDCs(sentence)
        kw_direction = keywords
        print "done creating SDCs"


        print "kw_direction"
        save_data['start_regions'].append(self.tf.get_tag_locations(startRegionTag))
        save_data['end_regions'].append(self.tf.get_tag_locations(endRegionTag))
        save_data["sentences"].append(sentence)
        save_data["regions"].append(region)
        save_data["subjects"].append(subject)
        save_data["keywords"].append(keywords)
        save_data["keywords_orient"].append(kw_direction)
        save_data["was_correct"] = False
        save_data["sent_number"] = sent_number

        #print save_data['']

        #get the original path
        mystart, myend = save_data['regions'][-1].split('to')
        mystart = mystart.strip()
        myend = myend.strip()
        t1 = self.topohash[mystart]
        t2 = self.topohash[myend]
        save_data["orig_path"].append(self.topo_graph_D[t1[0]][t2[0]])

        #print "orig path", self.topo_graph_D[t1[0]][t2[0]]
        #raw_input()

        if(len(keywords) == 0):
            print "no keywords continuing"
            return save_data

        ###########################################
        #otherwise, utilize the viewpoints
        ###########################################
        save_data["path"].append([])
        save_data["visited_viewpoints"].append([])
        save_data["probability"].append([])
        save_data["correct"].append([])
        save_data["correct_neigh"].append([])
        save_data["edit_distance"].append([])
        save_data["was_correct"] = False
        
        dataset_name = self.gtruth_tag_fn.split("/")[-1].split("_")[0]

        for orient in self.orient(self.dg_model, mystart, dataset_name):

            print "_____________________________________________"
            vals = None; lprob = None;
            '''if(isinstance(self.dg_model, du.models.hri2010_global.model) and self.is_sum_product == True):
                print "starting sum product"
                vals, lprob, sdc_eval = self.dg_model.is_sum_product(kw_direction, sloc, 
                                                             radians(orient))
                save_data["keywords_orient"][-1] = sdc_eval'''
            print "starting inference"

            vals, lprob, sdc_eval = [None, None, None]
            
            #print self.gtruth_tag_fn
            #print self.gtruth_tag_fn.split("/")[-1].split("_")[0]
            
            if not self.do_exploration:
                #do this for the 8th floor to prior the start orientation
                print "allowed orientations:", orient
                print "starting at region:", self.tf.get_tag_locations(startRegionTag)
                vals, lprob, sdc_eval = self.dg_model.infer_path(kw_direction, sloc, orient)
            else:
                #do this for exploration
                print "--------->doing exploration"
                print "allowed orientations:", orient
#                vals, lprob, sdc_eval = self.infer_explore(self.dg_model, kw_direction, sloc, orient)
                (vals, lprob, sdc_eval), visited_viewpoints = infer_explore(self.dg_model, kw_direction, sloc, orient, self.num_explorations, self.exploration_heuristics_name,self.params_num)   
                print "got:",(vals, lprob, sdc_eval), visited_viewpoints             
                save_data['visited_viewpoints'][-1].append(visited_viewpoints)
            save_data["keywords_orient"][-1] = sdc_eval



            if(vals == [] or vals is None):
                print "INFERENCE FAILED"
                save_data["path"][-1].append(None)
                save_data["probability"][-1].append(None)
                save_data["correct"][-1].append(False)
                save_data["correct_neigh"][-1].append(False)
                save_data["edit_distance"][-1].append(1000000)
                continue
            elif(self.inference=="topN"):
            	save_data["paths_topN"].append(vals)
                save_data["probability_topN"].append(lprob)
            	
                vals = vals[0]
            	lprob = lprob[0]
            	print "vals:", vals
                print "lprob:", lprob
            
            if(float(vals[-1].split("_")[0]) in self.topohash[endRegionTag]):
                print "Was correct"
                save_data["path"][-1].append(vals)
                save_data["probability"][-1].append(lprob)
                save_data["correct"][-1].append(True)
                save_data["was_correct"] = True

            else:
                print "was not correct"
                save_data["correct"][-1].append(False)
                save_data["path"][-1].append(vals)
                save_data["probability"][-1].append(lprob)

            if not self.do_exploration:
                if self.inference == "greedy":
                    save_data['visited_viewpoints'][-1].append(vals)
                else:
                    save_data['visited_viewpoints'][-1].append(self.dg_model.viewpoints)


            ############################################
            #check if the region is in 
            #    the neighbors of the current region
            is_in_neighbors = False
            for telt in self.topohash[endRegionTag]:
                if(float(vals[-1].split("_")[0]) in self.dg_model.tmap[telt]):
                    is_in_neighbors = True
            if(float(vals[-1].split("_")[0]) in self.topohash[endRegionTag]):
                is_in_neighbors = True
            save_data["correct_neigh"][-1].append(is_in_neighbors)


            ###############################################
            #get the predicted path through topologies 
            #    and then the string edit distance
            path_pred = []
            for myreg in vals:
                topo, orient = myreg.split("_")
                path_pred.append(float(topo))


            d = string_edit_distance(save_data["orig_path"][-1], path_pred)
            save_data["edit_distance"][-1].append(d)
        return save_data
        
#    def infer_explore(self, dg_model, sdcs, sloc, orient):
#        dg_model_cp = cpcp.copy(dg_model)
#        tmap_orig = deepcopy(dg_model_cp.tmap)
#        dg_model_cp.tmap = tmap_orig

#        allowed_topologies = []
#        visited_frontiers = []
#        visited_viewpoints = []

#        #append the starting topology
#        i, = kNN_index(sloc, transpose(dg_model_cp.tmap_locs.values()), 1)
#        mytopo_i = dg_model_cp.tmap_locs.keys()[int(i)]
#        allowed_topologies.append(mytopo_i)
#        allowed_topologies.extend(list(tmap_orig[mytopo_i]))
#        visited_frontiers.append(mytopo_i)

#        
#        #print "starting topologies", allowed_topologies
#        for i in range(len(sdcs)):
#            #create the correct topological map
#            tmap_new = self.tmap_mask(tmap_orig, allowed_topologies)
#            #print "new topological map", tmap_new            
#            
#            #set the topological map in the model
#    #        dg_model_cp.set_topo_map(tmap_new)   
#            dg_model_cp.tmap = tmap_new         
#            
#            #give the current number of sdcs
#            curr_sdcs = sdcs[0:i+1]

#            dg_model_cp.initialize_transition_matrices()
#            #infer the best destinations

#            dest, prob, sdcs_u, probs = dg_model_cp.infer_destination(sdcs, sloc, orient)
#            dest, prob = self.get_best_frontier(dg_model_cp, tmap_new, probs, visited_frontiers)

#            #dest, prob, sdcs_u, probs = dg_model_cp.infer_path(sdcs, sloc, orient)
#            mydest = float(dest[0].split("_")[0])
#            
#            #print "mydest", mydest
#            #print "allowed_topo:", allowed_topologies
#            
#            if(not mydest in tmap_new.keys()):
#                print "probability", prob
#                print tmap_new
#                raise KeyError("Bad key value")

#            visited_frontiers.append(mydest)
#            visited_viewpoints.append(dest[0])
#            allowed_topologies.extend(tmap_orig[mydest])
#            
#        ret_vals = dg_model_cp.infer_path(sdcs, sloc, orient)
#    #    dg_model_cp.set_topo_map(tmap_orig)
#        dg_model_cp.tmap = tmap_orig
#        
#        return ret_vals

#    def tmap_mask(self, tmap, mask):
#        tmap_new = {}
#        
#        #iterate through the from keys and check feasibility
#        for key_from in tmap.keys():
#            if key_from in mask:
#                #iterate through the to keys and check feasibility
#                for key_to in tmap[key_from]:
#                    if(key_to == key_from):
#                        tmap_new[key_from] = []                        
#                    elif(key_to in mask):
#                        try:
#                            tmap_new[key_from].append(key_to)
#                        except(KeyError):
#                            tmap_new[key_from] = [key_to]

#            else:
#                tmap_new[key_from] = []

#        return tmap_new
#    
#    def get_best_frontier(self, dg_model, tmap, probs, visited_topos):

#        topo_sing = tmap.keys()
#        
#        orients = dg_model.get_viewpoint_orientations(dg_model.num_viewpoints)
#        mymask = zeros(len(dg_model.viewpoints))*1.0

#        for topo in topo_sing:
#            if(topo in visited_topos):
#                continue
#            
#            for orient in orients:
#                i = dg_model.vpt_to_num[str(topo)+"_"+str(orient)]
#                mymask[i] = 1.0
#        
#        new_probs = probs*mymask

#        print "old max prob", max(probs)
#        print "new max prob:", max(new_probs)
#        return [dg_model.viewpoints[argmax(new_probs)]], new_probs[argmax(new_probs)]

#this assumes a list of integer location indicies
def evaluate(*args, **options):
    global evaluator
    options["options"] = dict(options)
    print "args", args
    evaluator = Evaluator(*args, **options)
    start = time.time()
    correctCount = evaluator.evaluateParallel()
    end = time.time()
    print "Took", (end - start)/60.0, "minutes."
    print "svn: ", current_svn_revision()
    print "host:", os.uname()[1]
    return correctCount


def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] corpus_fn, model_fn, gtruth_tag_fn, map_fn output_dir")
    parser.add_option("--num_to_run", type="string")
    parser.add_option("--is_sum_product", default=False, help="Use sum-product for inference.")
    parser.add_option("--no_spatial_relations", default=False, action="store_true", help="Don't use spatial relations.")
    parser.add_option("--evaluation_mode", type="choice", choices=["best_path", "max_prob", "specialized"],
                      help="The evaluation mode - try all four starting orientations or not.")
    parser.add_option("--do_exploration", default=False, action="store_true", 
                      help="Instead of performing global inference, only allow certain regions and then compute the best path.")
    parser.add_option("--quadrant_number", default=None, choices=[None, "1", "2", "3", "4"], 
                      help="Perform inference over a certain part of the directions.")
    parser.add_option("--wizard_of_oz_sdcs", default=None, help="Choose a set of gold-standard SDCs instead of automatic.")
    parser.add_option("--run_description", default=None, help="Description of the run.")
    parser.add_option("--inference", default="global", type="string")
    parser.add_option("--topN_num_paths", default=None, type="string")
    parser.add_option("--num_explorations", default=None, type="string")
    parser.add_option("--exploration_heuristics_name", default=None, type="string")
    parser.add_option("--parameters", default=None, type="string")
    (options, args) = parser.parse_args()
    print "args", args
    print "options", options.__dict__
    evaluate(*args, **options.__dict__)


if __name__=="__main__":
    main()








