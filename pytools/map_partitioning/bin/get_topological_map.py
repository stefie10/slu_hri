from pylab import *
from sys import argv
from map_partitioner import *
from carmen_maptools import *
from cPickle import load, dump

def get_topological_map(mp):
    print "getting topo map"
    tmap, locs = mp.get_topological_map()

    myfile = open("tmap.txt", 'w')

    gmap = mp.get_map()
    plot_map(gmap.to_probability_map_carmen(), gmap.x_size, gmap.y_size)
    
    mylocations = []
    for key in locs.keys():
        myfile.write(str(key) + " , " + str(locs[key])+"\n")
        mylocations.append(locs[key])
    mylocations = transpose(mylocations)

    for key in tmap:
        myfile.write(str(key) + " --> ")
        for elt in tmap[key]:
            myfile.write(str(elt) + " , ")
            
            x1, y1 = locs[key]
            x2, y2 = locs[elt]

            plot([x1, x2], [y1, y2], 'g-')
            
        myfile.write("\n")


    plot(mylocations[0], mylocations[1], 'ro')
    show()
        

if __name__=="__main__":
    if(len(argv) == 2):
        #load the gridmap
        
        mp = load(open(argv[1], 'r'))

        get_topological_map(mp)
        
        
    else:
        print "usage:"
        print "\t >>python partition_map.py map_partitioner.pck"
