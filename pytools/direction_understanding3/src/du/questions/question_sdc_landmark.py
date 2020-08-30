from random import randint
from copy import deepcopy
from generate_Q import *

class question_seq_sdc_landmark(question_seq):
    #Gets an SDC and ask if at that position in the path we see an extra landmark. 
    def __init__(self,sdcs,m4du,topN_paths):
        question_seq.__init__(self,sdcs,m4du,topN_paths)
        # get the landmarks
        # from the sdcs first
   
        self.landmarks = []
        self.sdc_pos=-1;
        self.curr_landmark = None
        self.fill_landmarks()
        print "NUM SDCS = ",len(sdcs)
        

        
    def next_question(self):

        self.sdc_pos += 1;
        self.sdc_pos %= len(self.sdcs)
        if self.sdc_pos == 0:
            if len(self.landmarks)>0:
                self.curr_landmark = self.landmarks[0]
                self.landmarks = self.landmarks[1:]
            else:
                print "no more landmarks"
                return None
        
        return self.sdc_question(self.sdcs[self.sdc_pos],self.sdc_pos,self.curr_landmark)            
        
        
    def sdc_question(self,sdc,pos,lmrk):
#        print "=====Next Question========"
#        print "forming sdc = ",sdc
        #binary question.
        qn = question(None,None)
        qn.qn_text = "As <FIGURE> go <VERB> <SR> <LANDMARK>, do <FIGURE> see a <QN_LANDMARK>?"
        
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
        
            
        
    def landmark_sdc(self,lmrk):
        return {"figure":None, "sr":None, "verb":"straight", "landmark":lmrk, "kwsdc":False, "landmarks":[lmrk]}
    
    def fill_landmarks(self):
        for sdc in self.sdcs:
            lmrk = sdc["landmark"]
            if lmrk not in self.landmarks:
                self.landmarks.append(lmrk)

        all_landmarks = self.m4du.clusters.tf.get_tag_names()
        filtered_landmarks = filter(lambda x: x not in self.landmarks,all_landmarks)
        self.landmarks.extend(filtered_landmarks)
        self.landmarks = self.landmarks[1:]
    
        

