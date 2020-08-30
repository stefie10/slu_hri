
"""
A question should have text field.
Then after this text is read to the subject, and answer is received:

1. Pattern matching to see which of the possible answers we've gotten.

2. To every answer corresponds a set of actions that should be performed on the sdc sequence.

"""

class question:

	def __init__(self,qn_text,ans_to_actions):
		self.qn_text = qn_text
		self.ans_to_actions = ans_to_actions
		if ans_to_actions == None:
			self.ans_to_actions = {}
		if qn_text == None:
		    self.qn_text = "NO TEXT"
		self.meta_data = ["generic"]
		
	
	
# Example of action generation:
#------------------
#    A = {}	
#    A["action"]="modify"
#    A["position"]=0
#    A["sdc"]={"figure":None, "sr":None, "verb":"straight", "landmark":"EPSILON", "kwsdc":False, "landmarks":[]}
#    question.actn_seq["no"]=[].append(A)
