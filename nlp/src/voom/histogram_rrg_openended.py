from corpus_rrg_openended import Corpus
from environ_vars import TKLIB_HOME
from histograms import Histogram, graphStacked
import chunker
import matplotlib.pylab as mpl
import numpy as na

def commandFilter(c):
    if len(c.strip()) != 0:
        return True
    else:
        return False

def main():
    corpus = Corpus("%s/data/verbs/corpus-11-2009.ods" % TKLIB_HOME)
    posTagger = chunker.makeTagger()
    
    print len(corpus.sessions), "subjects", len(corpus.commands), "commands"
    print len([x.command for x in corpus.commands if commandFilter(x.command)]),
    print "filtered commands"
    print na.mean([len([x for x in s.commands if commandFilter(x.command)]) 
                   for s in corpus.sessions]), "commands per subject"

    figsize=(6,10)
    bottomAdjust=0.07
    topAdjust=0.9

    histograms = {}
    commandTypes = corpus.commandTypes
    #commandTypes = ["Guiding people"]
    #commandTypes = ["Surveillance"]
    for commandType in commandTypes:
        histogram = Histogram()
        histograms[commandType] = histogram
        for command in corpus.commandsForType(commandType):
            indexes, tokens = chunker.tokenize(command.command)
            tokens = [t.lower() for t in tokens]
            tags = posTagger.tag(tokens)        
            for token, tag in tags:
                if tag[0] == "V":
                    histogram.add(token)

        graphStacked({"All":histogram}, "histogram", commandType, maxCols=50,
                     xticks=None, figsize=figsize, topAdjust=topAdjust,
                     bottomAdjust=bottomAdjust)
                                      
    graphStacked(histograms, "histogram", "All", maxCols=10, figsize=figsize,
                 topAdjust=topAdjust, bottomAdjust=bottomAdjust)
    mpl.legend()
    mpl.show()

if __name__ == "__main__":
    main()
    
