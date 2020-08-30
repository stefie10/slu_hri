from reward_matrix_basic import *

def question_selector_same_destination(questions, m4du, sdcs, topN_paths, previous_qns, answers=None):

    N = len(topN_paths)
    
    paths = map(lambda x: x[0],topN_paths)
    destinations = map(lambda x: x[-1],paths)
    
    #are the paths going to the same destination    
    reward_mat = array([[0 for j in range(N)] for i in range(N)])    
    for path_i in range(N):
        for path_j in range(N):
            if destinations[path_i] == destinations[path_j]:
                reward_ij = 1
            else:
                reward_ij = 0
            reward_mat[path_i,path_j] = reward_ij
    
    return question_selector_reward_matrix(reward_mat, questions, m4du, sdcs, topN_paths, previous_qns, answers)
