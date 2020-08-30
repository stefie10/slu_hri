from scipy import array
from carmen_maptools import *
from sys import argv
import cPickle
from sorting import *
from datatypes_planning import *
from pylab import *


def plot_paths(path_filename, model_filename, threshold=0.9):
    mypath = cPickle.load(open(path_filename, 'r'))
    mymodel = cPickle.load(open(model_filename, 'r'))
    
    I_threshold, = (array(mypath.tvals) > threshold).nonzero()
    
    print "number of candidates", len(I_threshold)
    
    tvals = array(mypath.tvals).take(I_threshold)
    fvals = array(mypath.fvals).take(I_threshold)
    lvals = array(mypath.lvals).take(I_threshold)
    
    mypaths = []
    for ind in I_threshold:
        mypaths.append(mypath.queue[ind])

    #filter by 
    lvals_fin, I = quicksort(lvals)
    
    finpaths = []
    for ind in I:
        finpaths.append(mypaths[ind])
    
    fvals_fin = array(fvals).take(I)
    tvals_fin = array(tvals).take(I)
    #lvals_fin = array(lvals).take(I)
    
    print tvals_fin[0:10]
    print lvals_fin[0:10]

    themap = mymodel.mylogfile.get_map()
    themapdata = themap.to_probability_map_carmen()
    
    #X, Y = mymodel.mylogfile.path_pts_unique
    #plot_map(themapdata, themap.x_size, themap.y_size)
    #plot(X, Y, 'rx')
    #show()
    end_locs = []
    done = False
    i = 0;
    while(not done):
        print "doing i"
        end_pt = mymodel.mylogfile.path_pts[:,finpaths[i][-1]]
        
        #print end_pt
        #print end_locs
        #raw_input()
        
        D=None
        if(end_locs == []):
            end_locs.append(end_pt)
        else:
            D =[]
            for pt in end_locs:
                d = sqrt(sum((array(pt) - array(end_pt))**2.0))
                D.append(d)

        #plot only if 
        if(D == None or min(D) > 2.0):
            print "plotting"
            figure()
            X, Y = mymodel.mylogfile.path_pts.take(finpaths[i], axis=1)
            plot_map(themapdata, themap.x_size, themap.y_size)
            plot([X[0]], [Y[0]], 'go')
            plot([X[-1]], [Y[-1]], 'ro')
            plot(X, Y, 'b-')
            title("Expected path length:"+str(lvals_fin[i])+"Prob:"+str(tvals_fin[i]))
            savefig("output/"+path_filename.split("/")[-1]+"_"+str(i)+".png")
            end_locs.append(end_pt)
                
        i+=1
        if(len(end_locs) > 20 or i >= len(finpaths)):
            done = True
        

    thespath = mypath.spath

    if(thespath != None):
        i=0
        for elt in finpaths:
            
            if(thespath == elt[0:len(thespath)]):
                print "yes", i
                finspath = elt
                finspath_val_t = tvals_fin[i]
                finspath_lval = lvals_fin[i]
                #raw_input()
                break;
            i+=1

        figure()
        X, Y = mymodel.mylogfile.path_pts.take(finspath, axis=1)
        plot_map(themapdata, themap.x_size, themap.y_size)
        plot([X[0]], [Y[0]], 'go')
        plot([X[-1]], [Y[-1]], 'ro')
        plot(X, Y, 'b-')
        title("Shortest path, Expected path length:"+str(finspath_lval)+"Prob:"+str(finspath_val_t))
        savefig("output/"+path_filename.split("/")[-1]+"_sp.png")

    show()
    
    

if __name__ == "__main__":
    
    if(len(argv) == 3):
        plot_paths(argv[1], argv[2])
    else:
        print "usage:\n\tpython plot_paths.py path_file.pck model_file.pck"

