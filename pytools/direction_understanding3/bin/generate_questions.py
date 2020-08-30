from du.inference import greedy, last_sdc, topN
from du.questions import generate_Q, question_sdc_landmark
import cPickle
from du.dir_util import direction_parser_sdc, model_prototype_du

"""
In Rakefile add the following line
#{d8_home_full}/output/#{ENV['OUT1']}
"""


def generate(out_fn,model_fn,num_to_generate=50,sent_number=0):
#    generate questions and print them and their properties
    
    #parsing the arguments
    if num_to_generate in [None, ""]:
        num_to_generate=50
    else:
        num_to_generate=int(num_to_generate)
        
    if sent_number in [None, ""]:
        sent_number=0
    else:
        sent_number=int(sent_number)
    
    #load the model and the result
    m4du = cPickle.load(open(model_fn, 'r'))
    m4du = topN.model(m4du)
    save_data = cPickle.load(open(out_fn, 'r'))
    
    sdc_parser = direction_parser_sdc()
    print "num_sentences =",len(save_data["sentences"])
    
    #use the first inference for testing purposes
    sentence = save_data["sentences"][sent_number]
    tn_paths = save_data["paths_topN"][sent_number]
    tn_probs = save_data["probability_topN"][sent_number]
    topN_paths = [(tn_paths[i],tn_probs[i]) for i in range(len(tn_paths))]
    
    sdcs = sdc_parser.extract_SDCs(sentence)
    sdcs = m4du.m4du.get_usable_sdc(sdcs)

    all_qns = question_sdc_landmark.question_seq_sdc_landmark(sdcs,m4du,topN_paths)

    for i in range(num_to_generate):
        q = all_qns.next_question()   
        print q.qn_text
        print q.ans_to_actions


	
def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: generate_questions.py [options] output_fn, model_fn")
    parser.add_option("--num_to_generate", type="string")
    parser.add_option("--sent_number", type="string")
    
    (options, args) = parser.parse_args()
    print "args", args
    print "options", options.__dict__
    generate(*args, **options.__dict__)



#	This describes what the path is:
d8_full_home ="/home/mitko/Desktop/UROP2010_Dimitar/tklib/data/directions/direction_floor_8_full/"
default_path_to_output_file = d8_full_home+"/output/specialized/topN.output_0.pck"
default_path_to_model_file = d8_full_home+"/models/min_entropy_extended.pck"

if __name__=="__main__":
    main()





