from reward_matrix_basic import *
from numpy import *

def question_selector_destination_distance(questions, m4du, sdcs, topN_paths, previous_qns, answers=None):

    N = len(topN_paths)
    
    paths = map(lambda x: x[0],topN_paths)
    destinations = map(lambda x: x[-1],paths)
    #region to topo
    topo_destinations = map(lambda x: float(x.split("_")[0]), destinations)
    #topo to location
    locations = map(lambda x:m4du.tmap_locs[x], topo_destinations)
    
    #calculate distances between topN paths destinations    
    reward_mat = array([[0 for j in range(N)] for i in range(N)])    
    for path_i in range(N):
        for path_j in range(N):
            reward_mat[path_i,path_j] = -straight_line(locations[path_i],locations[path_j])
            pass            
    
    return question_selector_reward_matrix(reward_mat, questions, m4du, sdcs, topN_paths, previous_qns, answers)


def straight_line(loc1,loc2):
    x1 = loc1[0]
    y1 = loc1[1]
    x2 = loc2[0]
    y2 = loc2[1]
    return sqrt((x1-x2)**2 + (y1-y2)**2)







