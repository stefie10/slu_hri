from scipy import *
from pyTklib import tklib_model4_5_du_compute_observation_probs
from pyTklib import tklib_get_transition_matrix_maxprob


class align_gm:
    #the last argument could ostensibly be made optional, but speeds things up in practice
    #    because it reduces the size of the spatial relation matrix
    def __init__(self, sdcs, T_seq, O_seq, SR_seq, L_seq, mypi, 
                 state_names, vp_i_to_topo_i, topo_to_location_mask, 
                 num_topo_regions, D_seq=None, max_skip=1):
                 
                 
        self.T_seq = T_seq
        self.O_seq = O_seq
        self.D_seq = D_seq
        self.SR_seq = SR_seq
        self.L_seq = L_seq
        self.mypi = mypi
        self.state_names = state_names
        self.vp_i_to_topo_i  = vp_i_to_topo_i
        self.num_topo_regions = num_topo_regions
        self.sdcs = sdcs
        self.topo_to_location_mask = topo_to_location_mask
        self.max_pathlength=len(self.sdcs)+20
        self.max_skip = max_skip+2
        self.prepare_seq()
        
        

    def prepare_seq(self):
        print len(self.T_seq), len(self.O_seq), len(self.sdcs)
        
        for i in range(len(self.T_seq)):

            if(self.T_seq[i] == None):
                self.T_seq[i] = array([[]])

            if(self.O_seq[i] == None):
                self.O_seq[i] = array([])

            if(self.D_seq[i] == None):
                self.D_seq[i] = array([[]])

            if(self.SR_seq[i] == None):
                self.SR_seq[i] = array([[]])
            else:
                self.SR_seq[i] = self.SR_seq[i].reshape([len(self.SR_seq[i])*len(self.SR_seq[i][0]), 
                                                         len(self.SR_seq[i][0][0])])

            
            if(self.L_seq[i] == None):
                self.L_seq[i] = array([])
        

    def cache_probs(self):
        print "caching O_probs"
        self.O_probs = zeros([len(self.sdcs), len(self.state_names), len(self.state_names)])*1.0
        for j in range(len(self.sdcs)):
            self.O_probs[j,:,:]= tklib_model4_5_du_compute_observation_probs(len(self.state_names),
                                                                             self.vp_i_to_topo_i,
                                                                             self.SR_seq[j],
                                                                             self.L_seq[j],
                                                                             self.O_seq[j],
                                                                             self.topo_to_location_mask,
                                                                             self.num_topo_regions);

        print "caching other probs"
        self.D_probs = zeros([len(self.sdcs), self.max_skip, len(self.state_names), len(self.state_names)])*1.0
        self.T_probs = zeros([len(self.sdcs), self.max_skip, len(self.state_names), len(self.state_names)])*1.0
        

        for j in range(len(self.sdcs)):
            print "sdc num:", j
            for delta in range(self.max_skip):
                #if(delta == 0):
                #    self.D_probs[j,delta,:,:] = diag(diag(self.D_probs[j,delta,:,:])+0.01)
                #    self.T_probs[j,delta,:,:] = diag(diag(self.T_probs[j,delta,:,:])+0.01)
                #else:
                self.D_probs[j,delta,:,:] = tklib_get_transition_matrix_maxprob(self.D_seq[j], delta)
                self.T_probs[j,delta,:,:] = tklib_get_transition_matrix_maxprob(transpose(self.T_seq[j]), delta)

                
    def inference(self):
        if(not len(self.O_seq) == len(self.T_seq)):
            print "error: observation sequence and transition matrix sequence not of equal length"
            exit(0)

        print "caching probabilities"
        self.cache_probs()
        
        print "running algorithm"
        Q = log(zeros([self.max_pathlength, len(self.sdcs), len(self.state_names), len(self.state_names)])*1.0)
        Q[0,0,:,:]= log(diag(self.mypi))
        
        #p_i_given_i_minus_d = 1.0/(1.0*self.max_skip+1)
        
        parents = zeros([self.max_pathlength, len(self.sdcs)-1, len(self.state_names), len(self.state_names),3])*1.0
        
        for j in range(len(self.sdcs)):
            print "sdc:", j
            for i in range(self.max_pathlength):            
                #print "path-length:", i
                for vp3 in range(len(self.state_names)):
                    for vp2 in range(len(self.state_names)):
                        o_prob = self.O_probs[j,vp2,vp3]
                        
                        for delta in range(self.max_skip):
                            #need to fix this... this changes 
                            #        based on the number of transitions
                            #        and is therefore dependent on delta
                            o_prob *= self.D_probs[j,delta,vp2,vp3]
                            if(o_prob == 0.0 or i-delta < 0):
                                continue
                            
                            
                            for vp1 in range(len(self.state_names)):
                                if(self.T_probs[j,delta,vp2,vp3] == 0.0 or 
                                   Q[i-delta, j-1, vp1, vp2] == -inf):
                                    continue

                                #q_curr = o_prob*p_i_given_i_minus_d*Q[i-delta, j-1, vp1, vp2]*self.T_probs[j,delta,vp1,vp2]
                                q_curr = log(o_prob)+Q[i-delta, j-1, vp1, vp2]+log(self.T_probs[j,delta,vp1,vp2])
                                
                                if(q_curr+log(self.T_probs[j,delta,vp2, vp3]) > Q[i,j,vp2,vp3]):
                                    Q[i,j,vp2,vp3] = q_curr
                                    
                                    if(j > 0):
                                        parents[i,j-1,vp2,vp3] = [i-delta, vp1, vp2]

            print "maximum element:", Q[:,j,:,:].max()
            

        #print Q
        #print Q[:,-1,:,:].max(axis=None)

        print "max1:", Q[:,-1,:,:].max()
        mymax, myind = self.get_best_index(Q)
        print "max2:", mymax, " ind:",myind
        #exit(0)

        if(myind == None):
            return 0.0, []
        
        retpath = self.state_names.take(self.get_best_path(parents, myind))
        print "prob:", exp(mymax), " path=", retpath
        
        return  retpath, exp(mymax)

    
    def get_best_index(self, Q):
        
        myQ = Q[:,-1,:,:]
        
        mymax = -inf; myindex = None
        for i in range(len(myQ)):
            for j in range(len(myQ[0])):
                for k in range(len(myQ[0][0])):
                    
                    if(myQ[i,j,k] > mymax):
                        mymax = myQ[i,j,k]
                        myindex = [i,j,k]

        return mymax, myindex
        

    def get_best_path(self, parents, start_index):
        
        mypath = [start_index]
        
        for j in range(len(self.sdcs)-2, -1, -1):
            p = mypath[-1]
            mypath.append(parents[p[0], j, p[1], p[2],:])

        finpath = []
        for e_i, elt in enumerate(mypath):
            finpath.append(elt[2])
            finpath.append(elt[1])
            
            #if(e_i == len(mypath)-1):
            #    finpath.append(elt[1])
                
        finpath.reverse()
        return finpath
    
    
'''print "iteration:", j
            for vp3 in range(len(self.state_names)):
                print "vp3:", vp3
                for vp2 in range(len(self.state_names)):
                    #print self.SR_seq[j]
                    #print self.L_seq[j]
                    #print self.O_seq[j]
                    #make sure the ordering of vp2 and vp3 is right
                    #if(self.SR_seq[j] == None or self.L_seq[j] == None or self.O_seq[j] == None):
                    #    print "is none"
                    try:
                        o_prob = tklib_model4_5_du_compute_observation_prob(vp2, vp3,
                                                                            self.vp_i_to_topo_i,
                                                                            self.SR_seq[j],
                                                                            self.L_seq[j],
                                                                            self.O_seq[j],
                                                                            self.num_topo_regions);
                    except:
                        print "exception:", vp2, vp3
                        print self.SR_seq[j]
                        
                        #print len(self.SR_seq[j]), len(self.SR_seq[j][0]), len(self.SR_seq[j][0][0]), len(self.SR_seq[j][0][0][0])
                        #print self.SR_seq[j]
                        #print self.L_seq[j]
                        #print self.O_seq[j]
                        #print self.num_topo_regions
                        #print self.vp_i_to_topo_i
                        exit(0)
                    self.O_probs[j,vp3,vp2] = o_prob'''

'''def compute_maximum(self, M, delta):
        if(delta == 0 or delta == 1):
            return M

        M_conn = deepcopy(M)
        M_max = deepcopy(M)
        
        for d in range(delta-1):
            for i in range(len(M)):
                for j in range(len(M)):
                    for k in range(len(M)):
                        new_val = M_conn[i,j]*M[j,k]
                        
                        if(new_val > M_conn[i,k]):
                            M_conn[i,k] = new_val
                        
                        if(new_val > 0):
                            M_max[i,k] = max(M_max[i,k], M[j,k])
        return M_max'''
