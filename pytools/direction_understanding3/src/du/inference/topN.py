from du import composedModel
from du.dir_util import *
from du.srel_utils import *
from numpy import *
from pyTklib import tklib_du_update_log_topN
from pyTklib import tklib_du_get_path_topN
from scipy import *


class model(composedModel.model,model_prototype_du):
    """
    This is Dimitar's topN version. It returns the N most likely paths. 
    To do so it increases the memory N times and remembers the N most likely paths at every step.    
    """
    def __init__(self, m4du,topN_num_paths):
        self.is_initialized = False
        self.topN_num_paths = topN_num_paths
        composedModel.model.__init__(self, m4du)
        
    def initialize(self):
        self.is_initialized = True
        self.m4du.initialize()
   
    def infer_path(self, sdcs, loc=None, sorient_rad=None, vp_slocs_i=None):
        if(not self.is_initialized):
            self.initialize()
        
        print "performing local L_seq opt"
        dists = self.m4du.inference_prepare(sdcs, loc, sorient_rad, vp_slocs_i)
        
        T_seq, O_seq, SR_seq, L_seq, D_seq, SDC_utilized, newpi = dists
        #Create the model and perform the inference here
        self.mygm = topN_gm(SDC_utilized, T_seq, O_seq, SR_seq, L_seq, newpi, self.m4du.viewpoints,
                                   self.m4du.vp_i_to_topo_i, self.m4du.topo_i_to_location_mask,
                                   self.m4du.path_lengths, 
                                   len(self.m4du.tmap_keys), D_seq, allow_multiple_sdcs_per_transition=True,
                                   allow_backtracking=self.m4du.allow_backtracking,
                                   num_topN_paths=self.topN_num_paths)
        
        #perform inference
        mypaths, myprobs = self.mygm.inference_approx()
        #return the relevant things
        return mypaths, myprobs, SDC_utilized
        

class topN_gm:
    #the last argument could ostensibly be made optional, but speeds things up in practice
    #    because it reduces the size of the spatial relation matrix
    def __init__(self, sdcs, T_seq, O_seq, SR_seq, L_seq, mypi, 
                 state_names, vp_i_to_topo_i, topo_i_to_location_mask, path_lengths, 
                 num_topo_regions, D_seq=None, allow_multiple_sdcs_per_transition=False, 
                 allow_backtracking=False,num_topN_paths=10):
        
        self.T_seq = T_seq
        self.O_seq = O_seq
        self.D_seq = D_seq
        self.SR_seq = SR_seq
        self.L_seq = L_seq
        self.mypi = mypi
        self.state_names = state_names
        self.vp_i_to_topo_i  = vp_i_to_topo_i + 0.0 # convert to float
        self.num_topo_regions = num_topo_regions
        self.path_lengths = path_lengths
        if self.path_lengths == None: 
            self.path_lengths = array([[]])
        
        self.sdcs = sdcs
        self.allow_multiple_sdcs_per_transition = allow_multiple_sdcs_per_transition
        self.topo_i_to_location_mask = topo_i_to_location_mask
        self.allow_backtracking = allow_backtracking
        self.num_paths = num_topN_paths #this is N from topN
        print "topN_gm initialized"
        
     #This will do update as usual but will consider the N most likely paths
    def inference_approx(self):
        N = self.num_paths
        num_states = len(self.state_names)
        print "starting inference_approx"
        #INICIALIZATION
        self.log_update_args = []
        if(not len(self.O_seq) == len(self.T_seq)):
            print "error: observation sequence and transition matrix sequence not of equal length"
            exit(0)
        
        #probabilities Pr[vp1,vp2]
        P_prev_log = log(zeros([N*len(self.state_names), len(self.state_names)])*1.0)

        for i in range(len(self.mypi)):
            P_prev_log[0:num_states,i] = log(self.mypi[i])
#        print "Start input", nonzero(exp(P_prev_log))
	    

#        print "P_prev_log:",P_prev_log
#        print "self.mypi",self.mypi
#        return
		
        parents_prev = zeros([len(self.state_names), N*(len(self.T_seq)-1)])-100
        parents_iN = zeros([len(self.state_names), N*(len(self.T_seq)-1)])-1
        used_epsilons = zeros((len(self.T_seq), num_states, len(self.state_names))) - 100
        #apply the first observation here
        #compute the initialization of the parameters
        #print "starting viterbi"
        #do the viterbi-style update
        #ITERATION

        print "staring iterations..."
#        for i in range(2): #for debug, to see when the N paths are the same.
        for i in range(len(self.T_seq)):
            print "update iteration ", i
            if(not len(self.SR_seq) == 0 and not self.SR_seq[i] == None):
                SR_reshape = self.SR_seq[i].reshape([len(self.SR_seq[i])*len(self.SR_seq[i][0]), 
                                                     len(self.SR_seq[i][0][0])])
                L_curr = self.L_seq[i].astype(float)
            else:
                SR_reshape = array([[]])
                L_curr = array([])
            
            #we want the previous transition matrix
            if(not i==0):
                T_mat_prev = self.T_seq[i-1]
            else:
                T_mat_prev = array([[]])

            T_curr = self.T_seq[i]
            if T_curr == None:
                T_curr = array([[]])
            
            #O_mat will be none if we don't see a keyword, but we do see
            #  a transition
            if(self.O_seq[i] == None):
                O_mat = array([])
            else:
                O_mat = self.O_seq[i]
                
            if(self.D_seq == None or self.D_seq[i] == None):
                D_mat = array([[]])
            else:
                D_mat = self.D_seq[i]
            
            # myparents is a structure that contains two elements
            # therefore two arrays: makes it easier in C
            if(i>1):
                myparents_prev = parents_prev[:,0:(i-1)*N]
                myparents_iN = parents_iN[:,0:(i-1)*N]
            else:
                myparents_prev = [[]]
                myparents_iN = [[]]

            if i >= 1:
                my_used_epsilons = used_epsilons[0:i]
                my_used_epsilons = my_used_epsilons.reshape(i*len(self.state_names), len(self.state_names))
            else:
                my_used_epsilons = [[]]


            sdc = self.sdcs[i]

            if sdc["landmark"] == "EPSILON":
                sdc_is_epsilon = True
            else:
                sdc_is_epsilon = False

            
            
            # cache the arguments so the gui can display them later. 
            updateArgs = dict(P_log_prev=P_prev_log,
                              myparents_prev=myparents_prev,
                              myparents_iN=myparents_iN,
                              used_epsilons=my_used_epsilons,
                              T_log_curr=log(T_curr),
                              SR_log_curr=log(SR_reshape+10e-6),
                              D_log_curr=log(D_mat),
                              L_log_curr=log(L_curr+10e-6),
                              O_log_curr=log(O_mat+10e-6),
                              vp_index_to_topo_index=self.vp_i_to_topo_i,
                              topo_i_to_location_mask=self.topo_i_to_location_mask,
                              num_topologies=self.num_topo_regions,
                              allow_multiple_sdcs_per_transition=self.allow_multiple_sdcs_per_transition,
                              sdc_is_epsilon=sdc_is_epsilon,
                              allow_backtracking=self.allow_backtracking,
                              max_epsilon_transitions=-1,
                              N = self.num_paths
                              )
                              
            #self.log_update_args.append(updateArgs)
            
            #Now perform an update in C because its much faster
#            print "jumping into C" #for debug
            out = tklib_du_update_log_topN(**updateArgs)
#            print "done with C" #for debug
            mymat = array(out)
#            print "output \n", nonzero(exp(mymat))
#            print "P_prev_log",P_prev_log #for debug
            ###########
            P_prev_log = mymat[0:len(P_prev_log), 0:len(P_prev_log[0])]
#            print "after update \n", nonzero(exp(P_prev_log))
            
            if(i>0):
            	for N_i in range(N):
		            parents_prev[:,(i-1)*N+N_i] = mymat[-2*N+N_i,:]
		            parents_iN[:,(i-1)*N+N_i] = mymat[-N+N_i,:]	
            used_epsilons[i] = mymat[len(P_prev_log):len(P_prev_log)+num_states, 0:len(P_prev_log[0])]
            
            if i==1:
                parents_prev[:,1:]=-100
                parents_iN[:,1:]=-1

#            set_printoptions(threshold=nan) #for debug, prints the whole matrix.
#            if i>=1:
#            	print "parents_prev",nonzero(parents_prev+100)
#            print "parents_iN", parents_iN
#            if i>1:
#            	return None
        
        
        #get the final best index after applying the last transition 
        
        best_dests_and_probs = []
        # must sort in decreasing order!
        def prob_comparison(x,y):
            if x[3]>y[3]:
                return -1
            if x[3]<y[3]:
                return 1
            return 0
            
#        print "out_probs=",out_probs
        for v1_i in range(len(self.state_names)):
            for v2_i in range(len(self.state_names)):
                for N_i in range(N):
                    #p_new = P_prev[v1_i,v2_i]*self.T_seq[-1][v2_i,v1_i]
                    best_dests_and_probs.append((v1_i,v2_i,N_i,P_prev_log[v1_i+N_i*num_states,v2_i]))
                best_dests_and_probs.sort(prob_comparison)
                best_dests_and_probs = best_dests_and_probs[:N]
        
        #print "diag(T_mat)", diag(T_mat_prev)
        #print "curr_best_path", curr_best_path
#        self.update_args = [convert_to_probs(args) 
#                            for args in self.log_update_args]
        
        print "best destinations:", best_dests_and_probs

        #get the best location
        best_i_paths = [tklib_du_get_path_topN(parents_prev,parents_iN,
                                         path[0],len(parents_prev[0])/N-1, path[2], N) for path in best_dests_and_probs]
        #formatting
        print "best_i_paths before formatting",array(best_i_paths)
        for i in range(len(best_i_paths)):
            best_i_paths[i].append(best_dests_and_probs[i][1])  
        print "best_i_paths again",array(best_i_paths)
        formatted_best_i_paths=[self.state_names.take(path) for path in best_i_paths]
        print "and again",formatted_best_i_paths                       
        self.used_epsilons = used_epsilons
        
        return formatted_best_i_paths, exp([path[3] for path in best_dests_and_probs])
 


def convert_to_probs(update_arg):
    newmap = {}
    for key, value in update_arg.iteritems():
        if "_log_" in key:
            newkey = "".join(key.split("_log"))
            newmap[newkey] = exp(value)
        else:
            newmap[key] = value
    return newmap

