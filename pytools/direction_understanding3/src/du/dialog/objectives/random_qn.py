

def random_qn(questions, m4du, sdcs, topN_paths, previous_qns):
    #select a random question
    from random import randint
    qn_number = randint(0,len(questions))
    return questions[qn_number], 0
