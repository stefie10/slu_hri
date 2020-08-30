import cPickle
from sys import argv
from tag_util import tag_file
from du.eval_util import model_evaluator
from du.explore import explore

if __name__=="__main__":
    if(len(argv) == 4):
        #try out standard inference
        gtruth_tf = tag_file(argv[2], argv[3])
        me = model_evaluator(cPickle.load(open(argv[1], 'r')), gtruth_tf, "d8")
        print me.evaluate_sentence("Go through the doors and past the elevators to the fountains", start_region="R17")

        #try out exploration
        myexp = explore(cPickle.load(open(argv[1], 'r')))
        me = model_evaluator(myexp, gtruth_tf, "d8")
        print me.evaluate_sentence("Go through the doors and past the elevators to the fountains", start_region="R17")

    else:
        print "usage:\n\tpython evaluate_model.py dg_model.pck gtruth.tag map_filename"

