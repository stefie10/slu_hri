from reward_matrix_basic import *
from deltaH import unique

def question_selector_exact_path(questions, m4du, sdcs, topN_paths, previous_qns, answers=None):

    N = len(topN_paths)
    
    paths_strings = map(lambda x: str(unique(x[0])),topN_paths)    
    #are the paths going to the same destination    
    reward_mat = array([[0 for j in range(N)] for i in range(N)])    
    for path_i in range(N):
        for path_j in range(N):
            if paths_strings[path_i] == paths_strings[path_j]:
                reward_ij = 1
            else:
                reward_ij = 0
            reward_mat[path_i,path_j] = reward_ij
    
    return question_selector_reward_matrix(reward_mat, questions, m4du, sdcs, topN_paths, previous_qns, answers)
