import sys
import cPickle
from pyTklib import kNN_index
import numpy as na



        
def compare_runs(model, runfile1, runfile2):
    #import gui.model4Browser
    #gui1 = gui.model4Browser.MainWindow(model)
    #gui1.setWindowTitle("run 1")
    #gui2 = gui.model4Browser.MainWindow(model)
    #gui2.setWindowTitle("run 2")
    #gui1.show()
    #gui2.show()
    

    ofile1 = cPickle.load(open(runfile1, 'r'))
    ofile2 = cPickle.load(open(runfile2, 'r'))
    print "cls", ofile1.__class__
    diffCount = 0
    leniantDiffCount = 0
    attempt = 0
    for i, (corr1, corr2) in enumerate(zip(ofile1['correct'], 
                                           ofile2['correct'])):
        
        if corr1 == None or corr2 == None:
        	continue       

        if corr1 !=corr2:
            print
            print "*******************************************************"
            print "difference", i, corr1, corr2
            correctnessFlip = any(corr1) != any(corr2)
            if correctnessFlip:
                print "***correctness flip!!!"
            else:
                print "No correctness flip."
            assert ofile1["sentences"][i] == ofile2["sentences"][i]
            sentence = ofile1["sentences"][i]
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
            print "run1", ofile1["run_description"], ofile1["probability"][i]
            print "run2", ofile2["run_description"], ofile2["probability"][i]
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
    print diffCount
    print leniantDiffCount

if __name__=="__main__":
    from sys import argv
    if len(argv) == 4:
        dg_model = cPickle.load(open(argv[1], 'r'))
        dg_model.initialize()
        compare_runs(dg_model, argv[2], argv[3])
    else:
        print "usage: <model.pck> <ofile1> <ofile2>"
