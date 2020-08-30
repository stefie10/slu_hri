from du.dialog.answer_prompt import allways_truthful
from du.dialog.answer_prompt.ans_util import *

from numpy import log

def question_selector(questions, m4du, sdcs, topN_paths, previous_qns, answers=None):
    
    if answers == None:
        answers = allways_truthful.allways_truthful

    # it is proven that deltaH >= 0, and the equality in trivial cases
    max_deltaH = 0
    best_question = None

    for question in questions:
        curr_objective = deltaH(question, m4du, sdcs, topN_paths, previous_qns, answers)
        if curr_objective > max_deltaH:
            max_deltaH = curr_objective
            best_question = question

    return best_question, max_deltaH

def unique(lst):
    from sets import Set
    if len(lst)==0:
        return []
    return list(Set(lst))

def deltaH(question, m4du, sdcs, topN_paths, previous_qns, answers):

    #H(expected answer) - average H(answer|path)
    expected_dist = {}
    average_H = 0
    for path, prob in topN_paths:
#        print "looking at path ", path
        #Prob(quesiton | path)
        # path must be in numbers
        #viewpoints
#        path = unique(map(lambda l: list(m4du.m4du.viewpoints).index(l),path))
#        print "path converted to ",path

        topo_path = unique(map(lambda l: float(l.split("_")[0]),path))
        
        some_ans, ans_dist = answers(question, m4du, sdcs, topN_paths, topo_path)
#        print "some_ans, ans_dist", some_ans, ans_dist
        expected_dist = add_dicts(expected_dist,multiply_dict(ans_dist,prob))
        average_H += H(ans_dist) * prob

    expected_H = H(expected_dist)

    return expected_H - average_H


def H(dist):
    total_H = 0
#    print "Dist is ",dist
    for key in dist.keys():
        p = dist[key]
#        print "P is ",p
        total_H += -p*log(p)
    return total_H

