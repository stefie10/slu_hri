from pylab import *
import orngStat
import numpy as na

def negOneToZero(lst):
    return [0 if x == -1 else x for x in lst]


def thresholdConfusionMatrices(results, classIndex=0, stepSize=0.01):
    thresholds = list(na.arange(0 - stepSize, 1 + stepSize, stepSize))
    # if zero is in here, kill it because it make sit go back to the
    # default behavior.
    thresholds = [t for t in thresholds if t != 0]

    return thresholds, [orngStat.confusionMatrices(results, classIndex, cutoff=threshold)[0]
                        for threshold in thresholds]


def costCurve(results, titleText, classIndex=0):
    pass
def rocCurve(results, titleText, classIndex=0, stepSize=0.01, marker='x', plotArgs=dict()):
    thresholds, confusionMatrices = thresholdConfusionMatrices(results, classIndex, stepSize)
    recalls = [orngStat.recall(cm) for cm in confusionMatrices]
    specificities = [1 - orngStat.spec(cm) for cm in confusionMatrices]

    #fig = figure()

    xlabel("FP", fontsize=25)
    ylabel("TP", fontsize=25)
    #plot([0, 1], [0, 1])
    line = plot(specificities, recalls, marker=marker, **plotArgs)
    #scatter(specificities, recalls, picker=True, marker=marker) # to get picking.
    def onclick(event):
        #point = event.artist.get_data()
        indexes = event.ind
        str = "\n".join(["%.3f" % thresholds[idx] for idx in indexes])
        print str
        print
#    fig.canvas.mpl_connect('pick_event', onclick)

    xlim(0,1.1)
    ylim(0,1.1)
    title(titleText)
    return line


def precisionRecallCurve(results, titleText, classIndex=0, stepSize=0.01):
    thresholds, confusionMatrices = thresholdConfusionMatrices(results, classIndex, stepSize)
    recalls = negOneToZero(map(orngStat.recall, confusionMatrices))
    precisions = negOneToZero(map(orngStat.precision, confusionMatrices))

    

    fig = figure()
    xlabel("Recall")
    ylabel("Precision")
    scatter(recalls, precisions, picker=True)


    def onclick(event):
        #point = event.artist.get_data()
        indexes = event.ind
        str = "\n".join(["%.3f" % thresholds[idx] for idx in indexes])
        print str
        print
    fig.canvas.mpl_connect('pick_event', onclick)

    xlim(0,1.1)
    ylim(0,1.1)
    title(titleText)

