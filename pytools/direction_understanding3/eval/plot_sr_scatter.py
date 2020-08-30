from du.plot_utils import plot_distance_curve, plot_performance_with_num_spatial_relations
import cPickle
import pylab as mpl
import sys


def plot_utilized_sr():
    min_entropy_with_sr = cPickle.load(open("data/directions/direction_floor_8/output/lenient/min_entropy.output_33.pck", 'r'))    
    min_entropy_without_sr = cPickle.load(open("data/directions/direction_floor_8/output/lenient/min_entropy.output_34.pck", 'r'))    

    greedy_with_sr = cPickle.load(open("data/directions/direction_floor_8/output/lenient/hri2010_greedy_2step.output_16.pck", 'r'))    
    greedy_without_sr = cPickle.load(open("data/directions/direction_floor_8/output/lenient/hri2010_greedy_2step.output_14.pck", 'r'))    


    plot_distance_curve(min_entropy_with_sr, False, "r*-", 
                        thelabel="Global with spatial relations")
    plot_distance_curve(min_entropy_without_sr, False, "b+-", 
                        thelabel="Global without spatial relations")


    plot_distance_curve(greedy_with_sr, False, "rx-", 
                        thelabel="local with spatial relations")
    plot_distance_curve(greedy_without_sr, False, "bp-", 
                        thelabel="local without spatial relations")
    mpl.legend(loc='lower right')
    mpl.show()


def main():    
    dg_model = cPickle.load(open(sys.argv[1], 'r'))
    dg_model.initialize()
    results = cPickle.load(open(sys.argv[2], 'r'))
    plot_performance_with_num_spatial_relations(dg_model, results)


if __name__=="__main__":
    main()
