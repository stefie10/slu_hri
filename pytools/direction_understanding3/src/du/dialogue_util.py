from du.eval_util import get_orientations_annotated
from du.inference import greedy, last_sdc, topN
from du.questions import question_sdc_landmark
from du.dialog.objectives import random_qn, deltaH
from du.dialog.objectives import distance_reward_matrix
from du.dialog.objectives import exact_path_reward_matrix
from du.dialog.objectives import same_destination_reward_matrix
import cPickle
from du.dir_util import direction_parser_sdc, model_prototype_du
from du.dialog.answer_prompt import allways_truthful
from du.dialog import modify_sdc_seq
from copy import deepcopy
from tag_util import tag_file



def dialog_data_structure():
    dialog_data = {}
    dialog_data["N"] = -1
    dialog_data["objective"] = ""
    dialog_data["sentence_number"] = -1
    dialog_data["num_to_ask"] = -1
    dialog_data["num_to_gen"] = -1
    dialog_data["initial_save_data"] = []
    dialog_data["paths_topN"] = []
    dialog_data["selected_questions"] = []
    dialog_data["received_answers"] = []
    dialog_data["answer_distributions"] = []
    dialog_data["inference_params"] = []
    return dialog_data
    
def name_for_dialog_data(dialog_data):
    name = "dialog"
    name += "_SN_"+str(dialog_data["sentence_number"])
    name += "_obj_"+str(dialog_data["objective"])
    name += "_askd_"+str(dialog_data["num_to_ask"])
    name += "_gend_"+str(dialog_data["num_to_gen"])
    name += "_N_"+str(dialog_data["N"])    
    name += ".pck"
    return name



"""
This procedure would run topN inference, get the paths, generate & select question based on them,
ask the question to human, and modify the SDC sequce
"""
def dialog(out_fn, model_fn, gtruth_tag_fn, output_dir, num_to_generate=50, num_to_ask=2, sent_number=0, objective="deltaH"):

#    from environ_vars import TKLIB_HOME
#    map_fn=TKLIB_HOME+"/data/directions/direction_floor_8_full/direction_floor_8_full_filled.cmf.gz"
    #assuming the topN inference is run beforehand

    #parsing the arguments
    if num_to_generate in [None, ""]:
        num_to_generate=50
    else:
        num_to_generate=int(num_to_generate)

    if num_to_ask in [None, ""]:
        num_to_ask=2
    else:
        num_to_ask=int(num_to_ask)

    if sent_number in [None, ""]:
        sent_number=0
    else:
        sent_number=int(sent_number)
        
    if objective in [None, ""]:
        objective = "deltaH"
    
    #load the model and the result
    save_data = cPickle.load(open(out_fn, 'r'))
    N = len(save_data["paths_topN"][0])
    m4du_base = cPickle.load(open(model_fn, 'r'))
    m4du = topN.model(m4du_base,N)
    #function that gives us the orientations for a sentence
    orient = get_orientations_annotated

    mystart, myend = save_data['regions'][sent_number].split('to')
    mystart = mystart.strip()
    print "MY START ",mystart
#    tf = tag_file(gtruth_tag_fn, map_fn)
    print "starting at region:", save_data["start_regions"][sent_number]
    dataset_name = gtruth_tag_fn.split("/")[-1].split("_")[0]
    orientation = orient(deepcopy(m4du), mystart, dataset_name)[0]
#    orientation = orient(m4du, mystart, dataset_name)
    print "ORIENTATION: ",orientation
    
    topohash = save_data["region_to_topology"]
#    sloc = m4du.m4du.tmap_locs[topohash[mystart][0]]
    sloc = m4du.tmap_locs[topohash[mystart][0]]
    
    #use the first inference for testing purposes
    orig_path = save_data["orig_path"][sent_number]
    print "Original path\n", orig_path

    sentence = save_data["sentences"][sent_number]
    tn_paths = save_data["paths_topN"][sent_number]
    tn_probs = save_data["probability_topN"][sent_number]
    topN_paths = [(tn_paths[i],tn_probs[i]) for i in range(len(tn_paths))]
    
    #get_sdcs
    sdc_parser = direction_parser_sdc()
    sdcs = sdc_parser.extract_SDCs(sentence)
    print "SDC before", sdcs
    print type(sdcs)
    print type(sdcs[0]),sdcs[0]
    print str(type(sdcs[0]))
#    return
    sdcs = m4du.m4du.get_usable_sdc(sdcs)
    print "SDC after", sdcs
    print type(sdcs)
    print type(sdcs[0]),sdcs[0]
    print str(type(sdcs[0]))
#    return
    
    #previous questions
    previous_qns = []

    #choose objective
    if objective== "deltaH":
        select_questions = deltaH.question_selector
    elif objective== "random" :
        select_questions = random_qn.random_qn
    elif objective== "distance_RM":
        select_questions = distance_reward_matrix.question_selector_destination_distance
    elif objective== "exact_path_RM":
        select_questions = exact_path_reward_matrix.question_selector_exact_path
    elif objective== "same_dest_RM":
        select_questions = same_destination_reward_matrix.question_selector_same_destination      
    
    # Set up the helper functions. This will add variety in the dialog.
    qn_generator = question_sdc_landmark.question_seq_sdc_landmark
    ask_question = allways_truthful.allways_truthful
    
    dialog_data = dialog_data_structure()
    dialog_data["N"]=N
    dialog_data["objective"] = objective
    dialog_data["sentence_number"] = sent_number
    dialog_data["num_to_ask"] = num_to_ask
    dialog_data["num_to_gen"] = num_to_generate
    dialog_data["initial_save_data"] = save_data
    dialog_data["paths_topN"].append(topN_paths)
    
    dialog_dump_fn = output_dir+name_for_dialog_data(dialog_data)
    cPickle.dump(dialog_data, open(dialog_dump_fn, 'w'))    
    print "Saved at", dialog_dump_fn
    
    for curr_question_number in range(num_to_ask):
        print "Looping the dialog" #so that the loop is non-empty
        #run question generation and select a bunch of questions, & evaluate them
        all_qns = qn_generator(sdcs,m4du,topN_paths)
        questions = []
        for qn_i in range(num_to_generate):
            questions.append(all_qns.next_question())
        questions = filter(lambda x: x!=None ,questions)
        questions = filter(lambda x: bool(x.qn_text not in map(lambda x: x.qn_text, previous_qns)),questions)

        #select questions
        best_question, objective_value = select_questions(questions, m4du, sdcs, topN_paths, previous_qns,answers=ask_question)
        previous_qns.append(best_question)
        dialog_data["selected_questions"].append(best_question)

        #prompt for answer
        answer , ans_dist = ask_question(best_question, m4du, sdcs, topN_paths, orig_path)
        dialog_data["received_answers"].append(answer)
        dialog_data["answer_distributions"].append(ans_dist)

        #modify sdc seq
        sdcs = modify_sdc_seq.modify_sdc_seq_wrt_ans(sdcs, best_question, answer)

        # rerun inference 
        vals, lprob, sdc_eval = m4du.infer_path(sdcs, sloc, orientation)
        topN_paths = [(vals[i],lprob[i]) for i in range(len(vals))]
        dialog_data["paths_topN"].append(topN_paths)
        
        #dump intermediate data into a pickle file
        # this is a good time to save data.
        cPickle.dump(dialog_data, open(dialog_dump_fn, 'w'))
        print "Saved at", dialog_dump_fn

    return dialog_dump_fn
    
    
#from evaluate_model import *
#from run_dialog import *
import cPickle


def name_for_combined_dialog_data(dialog_data,dirname):
    name = dirname+"combined_dialog"
    name += "_obj_"+str(dialog_data["objective"])
    name += "_askd_"+str(dialog_data["num_to_ask"])
    name += "_gend_"+str(dialog_data["num_to_gen"])
    name += "_N_"+str(dialog_data["N"])    
    name += ".pck"
    return name


def combine(file_lst, dirname):

    output_data = dialog_data_structure()
    output_data["sentence_number"]=[]

    for filename in file_lst:
        dialogue_data = cPickle.load(open(filename,"r"))
        for key in ["sentence_number", "paths_topN", "selected_questions", "received_answers", "answer_distributions"]:
            output_data[key].append(dialogue_data[key])

    dialogue_data = cPickle.load(open(file_lst[0],"r"))
    for key in ["N", "objective", "num_to_ask", "num_to_gen", "initial_save_data"]:
        output_data[key] = dialogue_data[key]
        
    output_fname = name_for_combined_dialog_data(output_data, dirname)

    # save the data as specified
    cPickle.dump(output_data, open(output_fname, "w") )
    print "Saved at "+output_fname
    
def process_dialogue(top_n_file_name, model_fn, gtruth_tag_fn, num_to_generate=50, num_to_ask=2, sent_number=0, objective="deltaH"):
    #assume we had run topN
    file_lst = []

    #dirname
    from environ_vars import TKLIB_HOME
    dirname = TKLIB_HOME+"/data/directions/direction_floor_8_full/dialog/"
    
    sentence_numbers = range(150)
    #TODO open the topN file name
    #get sentence numbers

    #run dialogue: just call the corresponding function several times
    for sent_number in sentence_numbers:
        out_i_name = dialog(top_n_file_name, model_fn, gtruth_tag_fn, dirname, num_to_generate=num_to_generate, num_to_ask=num_to_ask, sent_number=sent_number, objective=objective)
        file_lst.append(out_i_name)
        
    #combine dialogue
    combine(file_lst,dirname)

    #TODO show results in specific log file    
    
    pass    
    
    
import cPickle
from pprint import pprint
from pylab import *



def test_dialogue(output_fn):
    dialog_data = cPickle.load(open(output_fn, 'r'))
    
    num_sentences = len(dialog_data["paths_topN"])
    num_qns = len(dialog_data["paths_topN"][0])
    
    correctness_mat = [[None for j in range(num_qns)] for i in range(num_sentences)]
    
    for sent_i in range(num_sentences):
        for num_qn_i in range(len(dialog_data["paths_topN"][sent_i])):
            print sent_i
            print num_qn_i
            #format [sent_i][num_qn][num_path(best=0)][path==0 prob==1]
            path = dialog_data["paths_topN"][sent_i][num_qn_i][0][0]
            correctness_mat[sent_i][num_qn_i] = was_correct(path,sent_i,dialog_data["initial_save_data"],dialog_data)
    
    correctness_mat = array(correctness_mat)
    
    corr_after_qn_i = [len(filter(lambda x: x==True,correctness_mat[:,num_qn_i])) for num_qn_i in range(num_qns)]
    wrong_after_qn_i = [len(filter(lambda x: x==False,correctness_mat[:,num_qn_i])) for num_qn_i in range(num_qns)]
    
    
    print correctness_mat
    print corr_after_qn_i
    print wrong_after_qn_i
    
    wronged = enumerate(map(lambda m: [bool(m[i]==True and m[i+1]==False) for i in range(len(m)-1)], correctness_mat))
    wronged = filter( lambda x: bool(True in x[1]) ,wronged)
    
    wronged_num = map( lambda x: x[0], wronged)
    
    print "Wronged", wronged_num
    
    for sn in range(num_sentences):#wronged_num:
        print "SN:",dialog_data["sentence_number"][sn]," Questions:",map(lambda q: q.qn_text+str(q.ans_to_actions) ,dialog_data["selected_questions"][sn])
        print dialog_data["sentence_number"][sn],"answers :",dialog_data["received_answers"][sn]
    


# path should contain viewpoints for this function 
# to work correctly.
def was_correct(path, sent_i, save_data, dialog_data):
    was_correct = False
    dest = path[-1]
    orig_path = save_data["orig_path"][dialog_data["sentence_number"][sent_i]]
    topohash = save_data["region_to_topology"]
    meant_destination = orig_path[-1]
    for region in topohash.keys():
        if meant_destination in topohash[region]:
            true_regions = topohash[region]
            break
    dest_vp_topo_loc= float(dest.split("_")[0])
    if dest_vp_topo_loc in true_regions:
        was_correct = True
    return was_correct
    

