import sys
import cPickle
from pyTklib import kNN_index
import numpy as na
from chunker import IndexedTokenizer
from nltk.tokenize import PunktWordTokenizer, TreebankWordTokenizer



        
def compare_runs(model, runfile1, runfile2):

    ofile1 = cPickle.load(open(runfile1, 'r'))
    ofile2 = cPickle.load(open(runfile2, 'r'))
    print "cls", ofile1.__class__
    diffCount = 0
    leniantDiffCount = 0
    attempt = 0
    
    subject_to_num_o1_o2_flips = {}
    subject_to_num_o2_o1_flips = {}

    route_to_num_o1_o2_flips = {}
    route_to_num_o2_o1_flips = {}

    o1_o2 = []
    o2_o1 = []


    total_past_flip = 0.0
    total_past = 0.0

    total_through_flip = 0.0
    total_through = 0.0
    total_flips = 0.0

    total_length = 0.0
    total_length_flip = 0.0

    total_to = 0.0
    total_to_flip = 0.0

    tokenizer = IndexedTokenizer(PunktWordTokenizer())    
    for i, (corr1, corr2) in enumerate(zip(ofile1['correct'], 
                                           ofile2['correct'])):

        route = ofile1["regions"][i]
        assert route == ofile2["regions"][i]
        subject = ofile1["subjects"][i]
        assert subject == ofile2["subjects"][i]    
        subject_to_num_o1_o2_flips.setdefault(subject, 0)
        subject_to_num_o2_o1_flips.setdefault(subject, 0)
        route_to_num_o1_o2_flips.setdefault(route, 0)
        route_to_num_o2_o1_flips.setdefault(route, 0)

        sentence = ofile1["sentences"][i]
        assert sentence == ofile2["sentences"][i]

        indexes, tokens = tokenizer.tokenize(sentence)


        
        num_through = len([x for x in tokens 
                           if x.lower() in ("through","thru")])

        num_past = len([x for x in tokens 
                        if x.lower() in ("past", "pass")])

        num_to = len([x for x in tokens 
                        if x.lower() in ("to", "into")])
        total_past += num_past
        total_through += num_through
        total_to += num_to
        total_length += len(tokens)

        if subject == "Subject 06":
            total_through_flip += num_through
            total_past_flip += num_past
            total_to_flip += num_to
            total_length_flip += len(tokens)
            total_flips += 1


        if corr1 !=corr2:
            print
            print "*******************************************************"


            print "subject", subject
            print "region", route
            print "difference", i, corr1, corr2
            correctnessFlip = any(corr1) != any(corr2)
            if correctnessFlip:
                print "***correctness flip!!!"
                if any(corr1):
                    subject_to_num_o2_o1_flips[subject] += 1
                    route_to_num_o2_o1_flips[route] += 1
                    o2_o1.append((i,sentence))
                else:
                    
                    assert any(corr2)
                    subject_to_num_o1_o2_flips[subject] += 1
                    route_to_num_o1_o2_flips[route] += 1
                    o1_o2.append((i, sentence))

            else:
                print "No correctness flip."
                total_through_no_flip += num_through
            assert ofile1["sentences"][i] == ofile2["sentences"][i]
            

            print sentence
            sloc = ofile1["start_regions"][i] 
            sloc = (sloc[0][0], sloc[1][0])
            eloc = ofile1["end_regions"][i] 
            eloc = (eloc[0][0], eloc[1][0])
            print "sloc", sloc
            print "eloc", eloc
            
            iElocTopo = model.loc_to_idx(eloc)
            iSlocTopo = model.loc_to_idx(sloc)
            print "ieloc", iElocTopo
            print corr1
            print corr2
            slocs = [path[0] for path in ofile1["path"][i] if path != None]
            print "islocs", [model.vpts_for_topo(iSlocTopo)]
            print "ielocs", [model.vpts_for_topo(iElocTopo)]
            #if any(corr2) and not any(corr1): # one is right, and 2 is wrong
            if any(corr1) != any(corr2): # any differences
                for o, (p1, p2) in enumerate(zip(ofile1["path"][i], 
                                                 ofile2["path"][i])):
                    if corr1[o] != corr2[o]:
                        if p1 != None or p2 != None:
                            if attempt == 2 and False:
                                
                                print "correct", corr1[o], corr2[o]
                                sloc1 = model.vpt_to_num[p1[0]] 
                                sloc2 = model.vpt_to_num[p2[0]] 
                                print "sloc1", sloc1
                                print "sloc2", sloc2
                                assert sloc1 == sloc2
                                #gui1.runSentence(sentence, sloc1)
                                print "execing"
                                #import basewindow
                                #app = basewindow.makeApp()
                                #retval = app.exec_()                            

                            attempt += 1
                            
                    

                leniantDiffCount += 1
            diffCount += 1
    print "differences", diffCount

    print "flips o1->o2"
    print "\n\n".join([str(x) for x in o1_o2])
    print "***************************"
    print "flips o2->o1"
    print "\n\n".join([str(x) for x in o2_o1])

    print "o1->o2", route_to_num_o1_o2_flips
    print "o2->o1", route_to_num_o2_o1_flips

    print "average number of through", total_through/len(ofile1['correct'])
    print "average number of through, subject 6", total_through_flip/total_flips
    print
    print "average number of past", total_past/len(ofile1['correct'])
    print "average number of past, subject 6", total_past_flip/total_flips
    print
    print "average number of to", total_to/len(ofile1['correct'])
    print "average number of to, subject 6", total_to_flip/total_flips
    print 
    print "average length", total_length/len(ofile1['correct'])
    print "average length, subject 6", total_length_flip/total_flips

if __name__=="__main__":
    from sys import argv
    if len(argv) == 4:
        dg_model = cPickle.load(open(argv[1], 'r'))
        dg_model.initialize()
        compare_runs(dg_model, argv[2], argv[3])
    else:
        print "usage: <model.pck> <ofile1> <ofile2>"
