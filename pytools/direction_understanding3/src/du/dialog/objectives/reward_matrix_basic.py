from du.dialog.answer_prompt import allways_truthful
from du.dialog.answer_prompt.ans_util import *
from deltaH import H

from numpy import *


def reward_matrix_basic(reward_mat,posterior_mat,ans_prob_vec):

	# suppose we have N policies (like in topN)
	# suppose we have A answers
	
	# reward_mat is NxN
	# posterior_mat is NxA
	# ans_prob is Ax1
	
	# multiply matrices
	B = dot(reward_mat,posterior_mat)
#	print "Reward Mat", reward_mat
#	print "Posterior Mat", posterior_mat
	ans_prob_vec = matrix(ans_prob_vec)
		
#	print "BMAX before", B
	Bmax = matrix([ max_per_column(B[:,i]) for i in range(len(B[0]))])
#  	print "BMAX after", Bmax
#    		
#	print Bmax.shape
#	print ans_prob_vec.shape
	
	Question_value = dot(Bmax,transpose(ans_prob_vec))
	
	print "Question Value: ",Question_value	
	return Question_value
	
def max_per_column(lst):
	max_elmnt = lst[0]
	for elmnt in lst:
		if elmnt > max_elmnt:
			max_elmnt = elmnt
	return max_elmnt

def reward_matrix_with_mat(reward_mat, question, m4du, sdcs, topN_paths, previous_qns, answers):

    posterior_mat, ans_prob_vec = posterior_and_ans_prob(question, m4du, sdcs, topN_paths, previous_qns, answers)

    return reward_matrix_basic(reward_mat,posterior_mat,ans_prob_vec)
    
def posterior_and_ans_prob(question, m4du, sdcs, topN_paths, previous_qns, answers):

    expected_dist = {}
    average_H = 0
    posterior_mat_dict = array([{} for bla in range(len(topN_paths))])
    for (i,(path, prob)) in enumerate(topN_paths):
#        print "looking at path ", path
        #Prob(quesiton | path)
        # path must be in numbers
#        path = unique(map(lambda l: list(m4du.m4du.viewpoints).index(l),path))
#        print "path converted to ",path
        topo_path = unique(map(lambda l: float(l.split("_")[0]),path))
        
        some_ans, ans_dist = answers(question, m4du, sdcs, topN_paths, topo_path)
        for ans_key in ans_dist.keys():
        	posterior_mat_dict[i][ans_key] = (ans_dist[ans_key]+0.0)*prob
#        print "some_ans, ans_dist", some_ans, ans_dist
        expected_dist = add_dicts(expected_dist,multiply_dict(ans_dist,prob))
        average_H += H(ans_dist) * prob
  
    #post-processing
        #make sure no ans_prob = 0 (then there would be division by zero)
        #get rid of dictionary
    for key in expected_dist.keys():
        if expected_dist[key] == 0:
            del expected_dist[key]
  
    ans_names = expected_dist.keys()
    ans_prob_vec = expected_dist.values()

    def ans_name_to_number(name):
        return ans_names.index(name)
 
    #calculate posterior matrix (this is good for any type of reward matrix)
    #To calculate posterior matri|x (Bayes`s Rule):
    #prob(path|answer) = prob(ans|path) * prob(path) / prob(ans)  
    posterior_mat = array([[0 for bla1 in range(len(ans_names))] for bla0 in range(len(topN_paths))])    
    for name in ans_names:
        collumn_i = ans_name_to_number(name)
        for row_i in range(len(topN_paths)):
            if posterior_mat_dict[row_i][name] != None:
                posterior_mat[row_i,collumn_i] = (posterior_mat_dict[row_i][name]+0.0)
                posterior_mat[row_i,collumn_i] /= ans_prob_vec[collumn_i]

    return posterior_mat, ans_prob_vec
    
#general question selector
def question_selector_reward_matrix(reward_mat, questions, m4du, sdcs, topN_paths, previous_qns, answers=None):

    max_objective = reward_matrix_with_mat(reward_mat, questions[0], m4du, sdcs, topN_paths, previous_qns, answers)
    best_question = questions[0]
    #Then, for every question, calculate objective, and keep max.
    for question in questions[1:]:
        new_objective = reward_matrix_with_mat(reward_mat, question, m4du, sdcs, topN_paths, previous_qns, answers)
        if new_objective > max_objective:
            max_objective = new_objective
            best_question = question
        
    #At the end return best question and corresponding expected value added.
    return best_question, max_objective  

	
