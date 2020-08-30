import matplotlib.pylab as mpl
from routeDirectionCorpusReader import readSession, SessionGroup
from histograms import Histogram, graphStacked
import numpy as na


def graphSession(sessions, title, key, maxCols, leftAdjust, bottomAdjust, topAdjust, figsize, showEntries):
    userToHistogram = {}
    for session in sessions:
        histogram = Histogram()
        for instructionIdx, instruction in enumerate(session.routeInstructions):
            for annotation in session.routeAnnotations[instructionIdx]:
                print "text", annotation[key].text
                binKey = annotation[key].text.lower().strip()
                print "binKey", binKey
                if binKey != "": # and binKey != "you":
                    histogram.add(binKey)
        userToHistogram[session.subject] = histogram
    graphStacked(userToHistogram, "histogram", title, leftAdjust=leftAdjust,
                 bottomAdjust=bottomAdjust, topAdjust=topAdjust,
                 maxCols=maxCols, figsize=figsize, showEntries=showEntries,
                 condensed=False, xticks=na.arange(0, 251, 50))
    graphStacked(userToHistogram, "histogram", title, leftAdjust=leftAdjust,
                 bottomAdjust=bottomAdjust, topAdjust=topAdjust,
                 maxCols=maxCols, figsize=figsize, showEntries=showEntries,
                 condensed=True, xticks=na.arange(0, 251, 50))

#    bins = sorted(bins.iteritems(), key=lambda x: x[1], reverse=True)[0:50]
#    showHistogram("histogram", title, bins)
        
def count_words(sessions):
    import chunker
    from pos_histograms import pos_histograms
    discourses = []

    for session in sessions:
        for instructionIdx, instruction in enumerate(session.routeInstructions):
            discourses.append(instruction)
         

    posTagger = chunker.makeTagger()
    pos_histograms(discourses, posTagger)
   
    #print len(wordlist), "words"
    #print len(set(wordlist)), "unique words"


def main():
    floor8 = readSession("data/Direction understanding subjects Floor 8 (Final).ods", "stefie10") 
    floor1 = readSession("data/Direction understanding subjects Floor 1 (Final).ods", "stefie10") 
    quad = readSession("data/Direction understanding subjects Floor 1 (Helicopter).ods", "stefie10") 
    sessions = SessionGroup(floor8.sessions)
    sessions = SessionGroup(floor1.sessions + floor8.sessions)
    sessions = SessionGroup(floor1.sessions + floor8.sessions + quad.sessions)
    
    maxCols=10
    leftAdjust=0.45
    bottomAdjust=0.24
    topAdjust=0.85
    figsize=(5,4)
    mpl.rcParams.update({'font.family':'serif',})

    graphSession(sessions, "Landmarks", "landmark", 
                 maxCols=maxCols, leftAdjust=leftAdjust,
                 bottomAdjust=bottomAdjust, topAdjust=topAdjust,
                 figsize=figsize, showEntries=False)

    graphSession(sessions, "Spatial Relations", "spatialRelation", 
                 maxCols=maxCols, leftAdjust=leftAdjust, 
                 bottomAdjust=bottomAdjust, topAdjust=topAdjust,
                 figsize=figsize, showEntries=False)


    graphSession(sessions, "Verbs and Satellites", "verb", maxCols=maxCols,
                 leftAdjust=leftAdjust,
                 bottomAdjust=bottomAdjust, topAdjust=topAdjust,
                 figsize=figsize, showEntries=False)

    graphSession(sessions, "Figures", "figure", maxCols=maxCols,
                 leftAdjust=leftAdjust,
                 bottomAdjust=bottomAdjust, topAdjust=topAdjust,
                 figsize=figsize, showEntries=False)
    count_words(sessions)
    mpl.show()
if __name__ == "__main__":
    main()
