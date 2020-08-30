from scipy import *
import cPickle
from copy import deepcopy
from sys import argv
from datatypes_planning import *

def get_nn(myspline):
    print "getting indicies"
    I = myspline.get_skeleton_indices() 

    print "getting index"
    myindex = myspline.get_skeleton_indices_index()

    myneighbors = []
    
    for ind in range(len(I[0])):
        myneighbors.append([])
        
        I1 = myspline.get_neighbors(I[0][ind], I[1][ind])

        #iterate through the neighbors and add them to the 
        #    list
        for k in range(len(I1[0])):
            i = myindex[str(I1[:,k].tolist())]
            myneighbors[ind].append(i)

        #print "neighbors: ", myneighbors[ind],  " of ", ind
        #raw_input()

    return myneighbors


def plan_path(mymodel, myspline, 
              object, outfilename, sind=100, iterations=1000):

    #basically what I want to do here is to
    #  take a start location and plan a path that maximizes the
    #  likelihood of finding a query object (e.g. minimizes the 
    #  travel time).  We will assume that each location is independent
    #  and that their observations are independent.  

    #For model 3, all of the neighbors are already included... so I
    #  shouldn't penalize it twice.... but that's for the future.
    
    #The path that allows you to be sure that with P > x you have found
    #   an object.
    #mylocs = mymodel.mylogfile.path_pts_unique
    #myneighs = mymodel.mylogfile.path_pts_unique_nn

    print "getting nn"
    myneighs = get_nn(myspline)
    print "len(newneighs)", len(myneighs)
    print "len(ppts)", len(mymodel.mylogfile.path_pts[0])
    print "len(ppts_unique)", len(mymodel.mylogfile.path_pts_unique[0])
    mylmap = mymodel.likelihood_map[object]
    
    myqueue = [[sind]]
    myqueue_vals_t = [0.0]
    myqueue_vals_f = [1.0]
    myqueue_lvals = [0.0]
    myqueue_btrack = [False]
    
    done = False
    first_path = False
    shortest_path,  shortest_val_t, shortest_val_f, shortest_lval = None, None, None, None

    print "running"
    i = 0
    while(not done):
        #print myqueue
        #get the current path
        curr_path = myqueue.pop()
        prev_val_t = myqueue_vals_t.pop()
        prev_lval = myqueue_lvals.pop()
        prev_prob_f = myqueue_vals_f.pop()
        btrack = myqueue_btrack.pop()

        #get the new value given that the current location 
        #   returned false
        last_ind = curr_path[-1]

        if(len(myneighs[last_ind]) == 1):
            btrack=True
        
        added_path = False
        #print "connections to ", last_ind, " are:", myneighs[last_ind]
        for next_ind in myneighs[last_ind]:
            next_ind = int(next_ind)

            new_prob_f = prev_prob_f * (1.0-mylmap[next_ind])

            next_ind_cnt = curr_path.count(next_ind)
            if(next_ind_cnt == 0):
                new_val_t = prev_val_t + prev_prob_f * mylmap[next_ind]
                new_lval = prev_lval + prev_prob_f*mylmap[next_ind]*len(curr_path)
            else:
                new_val_t = prev_val_t 
                new_lval = prev_lval + prev_prob_f*len(curr_path)

            if(btrack==True and next_ind_cnt == 0):
                btrack = False

            if(next_ind_cnt == 0 or  
               (btrack==True and next_ind_cnt == 1)):
                added_path = True
                new_path = deepcopy(curr_path)
                new_path.append(next_ind)
                myqueue.insert(0, new_path)
                myqueue_vals_f.insert(0, new_prob_f)
                myqueue_vals_t.insert(0, new_val_t)
                myqueue_lvals.insert(0, new_lval)
                myqueue_btrack.insert(0, btrack)
            

            if(mylmap[next_ind] > 0.9 and not first_path):
                new_path = deepcopy(curr_path)
                new_path.append(next_ind)     
                shortest_path = new_path
                shortest_val_t = new_val_t
                shortest_val_f = new_prob_f
                shortest_lval  = new_lval
                first_path = True
                

        #in case there is nothing to be done (e.g. there are no connections)
        #if(not added_path):
        #    myqueue.insert(0, curr_path)
        #    myqueue_vals_t.insert(0, prev_val_t)
        #    myqueue_vals_f.insert(0, prev_prob_f)
        #    myqueue_lvals.insert(0, prev_lval)

        if(i > iterations):
            done=True
        i+=1
 
    print "lvals", myqueue_lvals
    print "vals", myqueue_vals_t

    print "maximum prob:", argmax(myqueue_vals_t), max(myqueue_vals_t)
    print "minimum prob:", argmin(myqueue_vals_t), min(myqueue_vals_t)
    print "mean prob:", mean(myqueue_vals_t)
    print "minimum expected length:", argmin(myqueue_lvals), min(myqueue_lvals)
    print "maximum expected length:", argmax(myqueue_lvals), max(myqueue_lvals)
    print "mean length:", mean(myqueue_lvals)
    print "length of queue", len(myqueue)

    pq = path_queue_shortest(myqueue, myqueue_vals_t, myqueue_vals_f, myqueue_lvals, 
                             shortest_path,  shortest_val_t, shortest_val_f, shortest_lval)

    cPickle.dump(pq, open(outfilename+"_"+str(sind)+"_pathplan.pck", 'w'))


if __name__=="__main__":
    if(len(argv) == 7):
        print "loading things"
        mfile = cPickle.load(open(argv[1], 'r'))
        myspline = cPickle.load(open(argv[2], 'r'))
        
        inds = ceil(linspace(0,len(mfile.mylogfile.path_pts_unique[0])-1, int(argv[5])))
        
        print "beginning path optimization on ", inds
        for ind in inds:
            plan_path(mfile, myspline, argv[3], argv[4], int(ind), int(argv[6]))
    else:
        print "usage:\n\t python plan_path.py model_file.pck spline_file object outfilename num_locations iterations"
