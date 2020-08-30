import cPickle
from sys import argv
from pylab import *
from scipy.io.mio import *

def show_model(mymodel_pck):
    
    tp = mymodel_pck.mylogfile.tp
    tn = mymodel_pck.mylogfile.tn

    print "true positives", tp
    print "true negatives", tn

    #for object in mymodel_pck.object_names:
    print "keys", mymodel_pck.likelihood_map.keys()

    myhash = {}
    for object in mymodel_pck.likelihood_map.keys():
        mylmap = mymodel_pck.get_lmap_nn(object)

        figure()
        gray()
        myhash[object] = mylmap
        imshow(transpose(mylmap), origin='lower', interpolation='nearest', vmin=0.0, vmax=1.0)
        title("local MRF for "+object+":"+ " tp="+str(tp)+" tn="+str(tn))
        savefig("output/"+object+"_"+str(tp)+"_"+str(tn)+".png")

    savemat('lmaps.mat', myhash)
        
    show()
    

if __name__=="__main__":

    if(len(argv) == 2):
        show_model(cPickle.load(open(argv[1], 'r')))

    else:
        print "usage:\n\tpython show_model.py model_file.pck"
