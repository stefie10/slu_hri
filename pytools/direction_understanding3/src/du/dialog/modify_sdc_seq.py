

def modify_sdc_seq_wrt_ans(sdcs, best_question, answer):

    answer = str(answer)
    if answer not in best_question.ans_to_actions.keys():
        print "ERROR: Invallid answer ",answer
        return sdcs
    else:
        for action in best_question.ans_to_actions[answer]:
            sdcs = perform_action_on_seq(sdcs,action)

    return sdcs

    #check what is the series of actions

def perform_action_on_seq(sdcs,action):
    act = action["action"]
    pos = action["position"]
    if action.has_key("sdc"):
        sdc = action["sdc"]
    else:
        sdc = None

    if pos>len(sdcs) or pos<0:
        print "ERROR: invalid position", pos
        return sdcs

    if act=="insert":
        sdcs.insert(pos,sdc)        
    elif act=="modify":
        sdcs[pos]=sdc
    elif act=="delete":
        for p in range(pos,len(sdcs)-1):
            sdcs[p]=sdcs[p+1]
        sdcs.pop()
    else:
        print "ERROR: invalid action", act
        return sdcs

    return sdcs
