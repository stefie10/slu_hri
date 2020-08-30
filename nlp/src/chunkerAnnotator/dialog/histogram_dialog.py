from histograms import Histogram, graphStacked
import chunker
import matplotlib.pylab as mpl
from reader import readDialogs


def main():
    dialog_fname = "sdc_annotations/stefie10.dialog.xml"

    dialogs = readDialogs(dialog_fname)

    figsize=(6,4.5)
    bottomAdjust=0.14
    topAdjust=0.9

    histograms = {"landmark":Histogram(),
                  "verb":Histogram(),
                  "figure":Histogram(),
                  "spatialRelation":Histogram()}

    
    for dialog in dialogs:
        for turn in dialog.turns:
            for sdc in turn.sdcs:
                indexes, allTokens = chunker.tokenize(sdc.text)
                movementWords = set(["go", "going", "walk","walking"])
                lowerTokens = [t.lower() for t in allTokens]
                if len(movementWords.intersection(lowerTokens)) != 0:
                    print sdc.text
                for key in sdc.keys:

                    if key in histograms:
                        histogram = histograms[key]
                    elif key[:-1] in histograms:
                        histogram = histograms[key[:-1]]
                    else:
                        raise ValueError("No histogram for: " + `key`)

                    text = sdc.annotationMap[key].text
                    indexes, tokens = chunker.tokenize(text)
                    for t in tokens:
                        histogram.add(t)

                    

    for key, histogram in histograms.iteritems():
        print "doing", key, histogram
        title = "%s" % key
        graphStacked({"all":histogram}, "histogram", title, maxCols=10,
                     xticks=None, figsize=figsize, topAdjust=topAdjust,
                 bottomAdjust=bottomAdjust)
        mpl.legend()


    mpl.show()

if __name__ == "__main__":
    main()
    
