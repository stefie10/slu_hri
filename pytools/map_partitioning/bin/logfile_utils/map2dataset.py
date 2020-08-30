from sys import argv
from map_partitioning2_0 import *
from pyTklib import *

#This file will convert a map to a dataset
#     for Emma to work with
def convert_to_dataset(gridmap, numclasses, numsamples, outfilename):
    samples = []
    labels = []
    if(numclasses < 0):
        samples, labels, k = partition_map(gridmap, None, numsamples);            
    else:
        #partition the map
        samples, labels, k = partition_map(gridmap, numclasses, numsamples);
    #samples, labels = partition_map(gridmap, numclasses, numsamples)
    
    samples = array(samples)
    print len(samples), len(samples[0])

    colors = get_colors()
    show_partitions(gridmap, samples, labels, colors)
    
    #char = raw_input(">>continue y/n")

    #if(char == "y"):
    print "saving"
    outfile = open(outfilename, 'w')
    outfile.write("####################################################\n")
    outfile.write("#TRAIN_SAMPLE lb:label" + " rp:robot_pose" + " d:range_reading\n")
    outfile.write("####################################################\n")
    outfile.write("#Range readings start in global coordinates from 0\n")
    outfile.write("#        and proceed in 1 degree increments to 2pi\n")

    angles = array(arange(0, 2*pi, pi/360.0))
    for i in range(len(samples[0])):
        dists = gridmap.ray_trace( samples[0,i], samples[1,i], angles)
        outfile.write("TRAIN_SAMPLE")
        outfile.write(" lb:"+str(labels[i]))
        outfile.write(" rp:"+str(samples[:,i]))
        outfile.write(" d:"+str(dists))
        outfile.write("\n")
        i+=1
    outfile.close()

if __name__=="__main__":
    if(len(argv) == 5):
        #load the gridmap
        gridmap  = tklib_log_gridmap()
        gridmap.load_carmen_map(argv[1])
        convert_to_dataset(gridmap, int(argv[2]), int(argv[3]), argv[4])
        
        #show the map
        savefig(argv[4]+".eps")
        show()
    else:
        print "usage:"
        print "\t >>python map2dataset.py mapfile numclasses numsamples outfilename"

