from general_question import *


# get sdcs
# get model?
# get topN paths

class question_seq:

	def __init__(self,sdcs,m4du,topN_paths):
		self.m4du = m4du
		self.sdcs = sdcs
		self.topN_paths = topN_paths
	
#	def next_question(self):
#	    print "ERROR: next_question() not yet implemented"
	    
	def next_n_questions(self,n):
	    qns = []
	    for i in range(n):
	        qns.append(next_question())
