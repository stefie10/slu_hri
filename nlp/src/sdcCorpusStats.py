from routeDirectionCorpusReader import readSession,  TextStandoff
from chunker import IndexedTokenizer
from nltk.tokenize import PunktWordTokenizer
import spatialRelationClassifier
from stopwords import stopwords

def sdcsWithoutLandmarks(sessions):
    count = 0.0
    noLandmarkCount = 0.0
    for session, instructionIdx, instruction, sdcs in sessions.sdcs():
        for sdc in session.routeAnnotations[instructionIdx]:
            if sdc.landmark.isNull():
                noLandmarkCount += 1
            count += 1
    print noLandmarkCount, "of", count, "without landmark.",
    print "%.3f" % (100.0* noLandmarkCount/count )
def handledSdcs(sessions, printIgnored=False):
    handledCount = 0
    count = 0.0
    countMap = {}
    srel_class = spatialRelationClassifier.SpatialRelationClassifier()
    for session, instructionIdx, instruction, sdcs in sessions.sdcs():
        for sdc in session.routeAnnotations[instructionIdx]:
            classifier = srel_class.sdcToClassifier(sdc)
            if not (classifier is None):
                handledCount += 1
                countMap.setdefault(classifier.name(), 0)
                countMap[classifier.name()] += 1

            else:
                if printIgnored:
                    print "ignored", sdc
                pass
            count += 1
    print "handled", handledCount, "of", count,
    print "(%.2f%%)" % (100.0*handledCount/count)
    print countMap


def containedInAny(things, range):
    for thing in things:
        if thing.contains(range):
            return True
    return False

def extractWord(token):
    import re
    match = re.match(r'(\w+)[.,?!")(]?', token)
    if match is None:
        return None
    else:
        return match.group(1)
    

def orphanedWords(sessions, withStopwords=True):
    orphanCount = 0
    count = 0.0
    tokenizer = IndexedTokenizer(PunktWordTokenizer())
    for session, instructionIdx, instruction, sdcs in sessions.sdcs():
        indexes, tokens = tokenizer.tokenize(instruction)
        for i, token in enumerate(tokens):
            idx = indexes[i]
            word = extractWord(token)

            if not(word is None):
                range = TextStandoff(instruction, (idx, idx + len(word)))
                if not containedInAny(sdcs, range):
                    if withStopwords or not word.lower() in stopwords:
                        orphanCount += 1
            count += 1

    orphanFraction = orphanCount/count
    print orphanCount, "orphans in", count,
    print "words. (%.2f%%)" % (orphanFraction * 100)

                

def main():
    floor8 = readSession("data/Direction understanding subjects Floor 8 (Final).ods", "stefie10") 
    floor1 = readSession("data/Direction understanding subjects Floor 1 (Final).ods", "stefie10") 
    #sessions = SessionGroup(floor8.sessions + floor1.sessions)
    sessions = floor8

    print "all words"
    orphanedWords(sessions, withStopwords=True)

    print "all non-stopword orphans"
    orphanedWords(sessions, withStopwords=False)
    
    print "floor 8"
    handledSdcs(floor8)

    print "all"
    sdcsWithoutLandmarks(sessions)
    
if __name__ == "__main__":
    main()
