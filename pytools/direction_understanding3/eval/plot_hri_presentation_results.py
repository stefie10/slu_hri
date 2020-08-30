from du.plot_utils import plot_distance_curve, plot_distance_curve_random
from environ_vars import TKLIB_HOME
from matplotlib.font_manager import fontManager, FontProperties
import cPickle
import numpy as na
import pylab as mpl
from plot_distance_curves import loadCorpus


    
def plot_sr_curves(title, runfiles, sr_label=True, 
                   followedState=None, random_colors=True):
    mpl.rc('font', size=20)
    fname = title.replace(" ", "_").replace(",","")
    markers = ["x", "+",  "^", "8", "o"]
    linestyles = ["-", "--", "-.", "-", "--", "-.", "-", "--", "-."]
    if followedState == None:
        colors = ["b", "r",  "k", "g", "y"]
    elif followedState == "followed":
        colors = ["c", "m",  "k", "y", "g"]
    elif followedState == "not followed":
        colors = ["k", "y",  "k", "y", "g"]
    else:
        raise ValueError("Unexpected followedState: " + `followedState`)
    
    for i, runFile in enumerate(runfiles):

        ofile = cPickle.load(open(runFile, 'r'))
        

        corpus = loadCorpus(ofile["corpus_fname"])

        if ofile["options"]["no_spatial_relations"]:
            srLabel = "-" 
            color=colors[0]
        else:
            srLabel = "+" 
            color=colors[1]
        inference = ofile["options"]["inference"] if "inference" in ofile["options"] else "global"
        if inference == "greedy":
            label = "no initial map (our approach)"
            if ofile["options"]["no_spatial_relations"]:
                marker="x"
            else:
                marker="o"
        elif inference == "global":
            label = "complete map (our approach)"
            if ofile["options"]["no_spatial_relations"]:
                marker="+"
            else:
                marker="d"
        else:
            label = inference

        if "last" in ofile["run_description"]:
            label = "complete map (last SDC only)"
            color = colors[0]
            marker = "^"
        elif "wei" in ofile["run_description"]:
            label = "complete map (landmarks only)"
            color = colors[0]
            marker = "s"


        if sr_label:
            label = "%s %s" % (label, srLabel)
            label += "sr"
        if followedState != None:
            label += " " + followedState
        if True in ofile["do_exploration"]:
            label += " (exploration)"

        #print linestyles[i]
        if(random_colors):
            plot_distance_curve(ofile, corpus, marker, colors[i], thelabel=label,
                                followedState=followedState, linestyle=linestyles[i])
        else:
            plot_distance_curve(ofile, corpus, marker, color, thelabel=label,
                                followedState=followedState, linestyle=linestyles[i])
        font = FontProperties(size='small')
        mpl.legend(loc='lower right', prop=font)
        mpl.xticks(na.arange(0, 100, 10))
        mpl.xlim(0, 30)
        mpl.ylim(0, 1)
        mpl.yticks(na.arange(0, 1.1, 0.1))
        mpl.title(title)
        #mpl.subplots_adjust(left=leftAdjust)
        
        mpl.savefig("%s/pytools/direction_understanding3/%s_%d.png" % (TKLIB_HOME, fname, i))

    mpl.savefig("%s/pytools/direction_understanding3/%s.png" % (TKLIB_HOME, fname))



def plot_landmark_curves(title, runfiles):
    mpl.rc('font', size=20)
    fname = title.replace(" ", "_").replace(",","")
    markers = ["x", "+",  "^", "8", "o"]
    colors = ["r", "b",  "k", "y", "g"]
    mpl.figure(figsize=(14,7))
    for i, runFile in enumerate(runfiles):

        ofile = cPickle.load(open(runFile, 'r'))
        corpus = loadCorpus(ofile["corpus_fname"])


        #if True in ofile["do_exploration"]:
        #    label += " (exploration)"

        landmark_type = runFile.split(".")[-2].split("_")[-1]

        inference = ofile["options"]["inference"] if "inference" in ofile["options"] else "global"
        if inference == "greedy":
            label = "no initial map (" + landmark_type  
        elif inference == "global":
            label = "complete map (" + landmark_type 
        else:
            label = inference

        if(landmark_type == "all"):
            label+=")"
        else:
            label+="-only)"

        plot_distance_curve(ofile, corpus, markers[i], colors[i], thelabel=label)
        font = FontProperties(size='small')
        mpl.legend(loc='lower right', prop=font)
        mpl.xticks(na.arange(0, 100, 10))
        mpl.xlim(0, 60)
        mpl.ylim(0, 1)
        mpl.yticks(na.arange(0, 1.1, 0.1))
        mpl.title(title)
        #mpl.subplots_adjust(left=leftAdjust)
        
        mpl.savefig("%s/pytools/direction_understanding3/%s_%d.png" % (TKLIB_HOME, fname, i))

    mpl.savefig("%s/pytools/direction_understanding3/%s.png" % (TKLIB_HOME, fname))







    
if __name__=="__main__":
    d1="%s/data/directions/direction_floor_1/output/hri_presentation_runs/spatialRelations" % TKLIB_HOME
    d8="%s/data/directions/direction_floor_8_full/" % TKLIB_HOME
    d8_models = "%s/output/hri_presentation_runs/spatialRelations" % d8
    
    
    mpl.figure(figsize=(14, 7))
    plot_sr_curves("Stata 1, Quadrant 1",
                   ["%s/global_with_sr_q1.pck" % d1,
                    # "%s/global_without_sr_q1.pck" % d1,
                    "%s/greedy_with_sr_q1.pck" % d1,
                    #"%s/greedy_without_sr_q1.pck" % d1,
                    ], 
                   sr_label=False)
                   
    """
    mpl.figure(figsize=(9, 7))
    '''plot_sr_curves("Stata 1, Quadrant 3",
                   [#"%s/global_with_sr_q3.pck" % d1,
                    "%s/global_without_sr_q3.pck" % d1,
                    "%s/greedy_with_sr_q3.pck" % d1,
                    #"%s/greedy_without_sr_q3.pck" % d1,
                    ]
                   )'''
       """            
    mpl.figure(figsize=(14, 7))

    plot_sr_curves("Stata 8, Followed vs Not Followed",
                   ["%s/global_with_sr.pck" % d8_models,
                    "%s/global_without_sr.pck" % d8_models,
                    ],
                   followedState="followed"
                   )
    

    plot_sr_curves("Stata 8, Followed vs Not Followed",
                   ["%s/global_with_sr.pck" % d8_models,
                    "%s/global_without_sr.pck" % d8_models,
                    ],
                    followedState="not followed"
                   )
    
    mpl.figure(figsize=(14, 7))        
    plot_sr_curves("Stata 8, Spatial Relations",
                   ["%s/global_with_sr.pck" % d8_models,
                    "%s/global_without_sr.pck" % d8_models,
                    "%s/greedy_with_sr.pck" % d8_models,
                    "%s/greedy_without_sr.pck" % d8_models,
                    ], 
                   random_colors=False)

    mpl.figure(figsize=(14, 7))
    plot_landmark_curves("Stata 8, Landmarks",
                         ["%s/../landmark/min_entropy_extended_all.pck" % d8_models,
                          "%s/../landmark/min_entropy_extended_detectable.pck" % d8_models,
                          "%s/../landmark/min_entropy_extended_signs.pck" % d8_models,
                          ]
                         )

    mpl.figure(figsize=(14, 7))

    #model = cPickle.load(open("data/directions/direction_floor_8_full/models/min_entropy_extended.pck"))
#    plot_distance_curve_random(model, 
#                               "%s/nlp/data/Direction understanding subjects Floor 8 (Final).ods" % TKLIB_HOME,
#                               "%s/regions/df8full_gtruth_regions.tag" % d8,
#                               "%s/direction_floor_8_full_filled.cmf.gz" % d8,
#                               color="b", marker="p", label="Random"
#                               )

    #plot_sr_curves("Stata 8",
    #               ["%s/global_with_sr.pck" % d8_models,],
    #               sr_label=False)
    plot_sr_curves("Stata 8",
                   [ "%s/global_with_sr.pck" % d8_models,
                     "%s/hri2010_wei_extended.output.pck" % d8_models,
                     "%s/last_sdc.pck" % d8_models,
                     "%s/greedy_with_sr.pck" % d8_models
                     ],
                   sr_label=False
                   )

    mpl.show()
