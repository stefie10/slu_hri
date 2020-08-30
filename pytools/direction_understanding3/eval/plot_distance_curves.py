import matplotlib
matplotlib.use("Qt4Agg")

from sys import argv
import os.path
import cPickle
from du.plot_utils import plot_distance_curve, plot_distance_curve_subject
from matplotlib.font_manager import  FontProperties
from pylab import rc, show, legend
import pylab as mpl
import numpy as na
from environ_vars import TKLIB_HOME
from memoized import memoized


@memoized
def loadCorpus(corpus_fname):
    from routeDirectionCorpusReader import readSession
    tokens = corpus_fname.split("/")
    after_tokens = []

    for token in tokens:
        if len(after_tokens) > 0:
            after_tokens.append(token)
        else:
            if "slu" in token:
                after_tokens.append(token)
    corpus_fname = os.path.join(*[TKLIB_HOME] + after_tokens[1:])
    print corpus_fname
    return readSession(corpus_fname, "stefie10")


def main():
    rc('font', size=20)

    print "number of models:", len(argv)-1
    for i, runFile in enumerate(argv[1:]):
        if os.path.isdir(runFile):
            continue
        #mylabel = runFile.split("/")[-1].split(".")[0]    
        

        ofile = cPickle.load(open(runFile, 'r'))
        if ofile["options"]["no_spatial_relations"]:
            srLabel = "-" 
            color="b"
        else:
            srLabel = "+" 
            color="r"
        inference = ofile["options"]["inference"]
        if inference == "greedy":
            label = "Local inference"
            if ofile["options"]["no_spatial_relations"]:
                marker="x"
            else:
                marker="o"
            color="r"
        elif inference == "global":
            label = "Global inference"
            if ofile["options"]["no_spatial_relations"]:
                marker="+"
            else:
                marker="d"
        else:
            marker = "o"
            label = inference

        label += " (" + os.path.basename(ofile["options"]["model_fn"]) + ")"
        label = "%s %s" % (label, srLabel)
        label += "sr"

        if True in ofile["do_exploration"]:
            label += " (exploration)"


        corpus = loadCorpus(ofile["corpus_fname"])
        plot_distance_curve(ofile, corpus, marker, color, thelabel=label)
        #plot_distance_curve_subject(ofile, create_figure=False)

        font = FontProperties(size='small')
        legend(loc='lower right', prop=font)
        mpl.xticks(na.arange(0, 100, 10))
        mpl.xlim(0, 60)
        mpl.ylim(0, 1)
        mpl.yticks(na.arange(0, 1.1, 0.1))
        mpl.savefig("%s/pytools/direction_understanding3/plot%d.png" % (TKLIB_HOME, i))


    show()
    
if __name__=="__main__":
    main()
