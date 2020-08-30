from random import randint
from copy import deepcopy
from generate_Q import *

class question_compare_two_paths(question_seq):
    #Gets an SDC and ask if at that position in the path we see an extra landmark. 
    def __init__(self,sdcs,m4du,topN_paths):
        question_seq.__init__(self,sdcs,m4du,topN_paths)
        # get the landmarks
        # from the sdcs first
   
        self.landmarks = []
        self.sdc_pos=-1;
        self.curr_landmark = None
        self.fill_landmarks()
        self.qn_queue = []
        self.path_pair_queue = []
        
        #TODO load all the path_pairs
        # paths are sequences of viewpoints
        print "NUM SDCS = ",len(sdcs)
        

        
    def next_question(self):

        # if question queue is empty get the qns for pair of paths
        while len(self.qn_queue)<1 and len(self.path_pair_queue)>0 :
            path_pair = self.path_pair_queue[0]
            self.path_pair_queue = self.path_pair_queue[1:]
            fill_queue_with_qns(path_pair)
        
        if len(self.qn_queue)==0:
            return None
        else:
            qn = self.qn_queue[0]
            self.qn_queue = self.qn_queue[1:]
            return qn
        
          
        
        
    def fill_queue_with_qns(self,path_pair):
        path_divisions = divide_paths(path_pair)
        #path divisions are sequences of pair of sequences that correspond
        #to same part of the path. They are either totally the same or totally
        #different
        for div_i in range(len(path_divisions)):
            qn = division_question(path_divisions,div_i)
            if qn != None:
                self.qn_queue.append(qn)
                
            
    def division_question(self.divs,i):
        div = divs[i]
        if div[0]==div[1]: #same part
            return None

        qn = question(None,None)
        qn.qn_text= "Should I <task_1> (1), or should I <task_2> (2), both (3) or none (0)?"
        
        
        
        #check what does the SDC contain and modify the question to fit it.    
        if sdc["figure"]==None:
#            print "NO FIGURE"
            qn.qn_text = qn.qn_text.replace("As <FIGURE> go ","")
            qn.qn_text = qn.qn_text.replace(" do <FIGURE> see","is there")
        else:
            qn.qn_text = qn.qn_text.replace("<FIGURE>",str(sdc["figure"]))

        if sdc["verb"]==None:
            qn.qn_text = qn.qn_text.replace("<VERB>","")
        else:
            qn.qn_text = qn.qn_text.replace("<VERB>","going "+str(sdc["verb"]))

        if sdc["sr"]==None:
            qn.qn_text = qn.qn_text.replace("<SR>","")
        else:
            qn.qn_text = qn.qn_text.replace("<SR>",str(sdc["sr"]))

        if sdc["landmark"]==None:
            qn.qn_text = qn.qn_text.replace("<LANDMARK>","")
        elif sdc["landmark"]=="EPSILON":
            #sdc landmark should not be epsilon
            return None
        else:
            qn.qn_text = qn.qn_text.replace("<LANDMARK>","by the "+str(sdc["landmark"]))
        
        if str(lmrk)!=sdc["landmark"]:
            qn.qn_text = qn.qn_text.replace("<QN_LANDMARK>",str(lmrk))
        else:   
            #question landmark should be different
            return None
        
        #for every possible answer device a corresponding action
        qn.ans_to_actions["yes"]=[]
        modified_sdc = deepcopy(sdc)
        modified_sdc["landmarks"]=self.landmark_sdc(lmrk)
        yes_actn = {"action":"insert","position":pos,"sdc":modified_sdc}
        qn.ans_to_actions["yes"].append(yes_actn)      
        qn.ans_to_actions["no"]=[]

        qn.meta_data=["SDC_L",deepcopy(sdc),lmrk]
        return qn









        
        
        
    def divide_paths(path_pair):
        #TODO this should be done with dynamic programming
        path1, path2 = path_pair
        #get largest common subsequence
        common_vps = lcs(path1,path2)
        
        pass
            
        
        
        
        
        
        
        
        
        
        

