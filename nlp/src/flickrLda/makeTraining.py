from environ_vars import TKLIB_HOME
from memoized import memoized
from nltk.probability import FreqDist
from nltk.stem.porter import PorterStemmer
from stopwords import stopwords
import glob
import os
import random


def anySubstring(string, lst):
    for l in list:
        if string in l:
            return True
    return False

def hasKeywords(keywords, lst):
    return len(keywords.intersection(lst)) > 0

lmtzr = PorterStemmer()
@memoized
def stem(t):
    return lmtzr.stem(t)

def readTokens(fname, keywords=None):
    f = open(fname, "r")
    tokens = [x.strip().lower() for x in f]
    
    tokens = set([stem(t) for t in tokens 
                  if (not t in stopwords and t != "" and not "=" in t and t.isalpha())])
    
                
    f.close()
    if not hasKeywords(keywords, tokens):
        return []
    else:
        return tokens
        
def ldaFromFiles(files, keywords):
    tmpname = "flickrLda.tmp.dat"
    tmpname1 = "flickrLda1.tmp.dat"
    
    wordCounts = FreqDist()
    print len(files), "total docs",
    
    tmpfile = open(tmpname1, "w")
    #outfile.write("%d\n" % len(files))
    for i, fname in enumerate(files):
        tokens = readTokens(fname, keywords)
        if len(tokens) != 0:
            for t in tokens:
                wordCounts.inc(t)
            tmpfile.write(" ".join(tokens))
            tmpfile.write("\n")
        if i % 100 == 0:
            print "word dist: ", i
    
    tmpfile.close()
    tmpfile = open(tmpname1, "r")
    docCount = 0
    outfile = open(tmpname, "w")
    for i, line in enumerate(tmpfile):
        tokens = line.split()

        tokens = [t for t in tokens if wordCounts[t] > 10]
        if len(tokens) != 0:
            outfile.write(" ".join(tokens))
            outfile.write("\n")
            docCount += 1
        if i % 100 == 0:
            print "doc", i
    
    outfile.close()
    
    dir = "data/flickrLda.keywords"
    if not os.path.exists(dir):
        os.makedirs(dir)    
    fname = "data/flickrLda.keywords/flickrLda.dat"
    print "writing", fname
    outfile = open(fname, "w")
    outfile.write("%d\n" % docCount)
    print "rewriting file"
    for l in open(tmpname, "r"):
        outfile.write(l)
    outfile.close()
    os.remove(tmpname)    
    os.remove(tmpname1)    
    print "used", docCount, "docs."
    print len(wordCounts), "words overall"
    
def main():
    keywords = set([stem(l.strip()) 
                for l in open("%s/data/directions/labels.txt" % TKLIB_HOME)])
    print "keywords", keywords
    files = glob.glob("%s/data/flickr/FlickrNotes/*/*.txt" % TKLIB_HOME)
    #files = random.sample(files, 100000)
    ldaFromFiles(files, keywords)
    #cProfile.runctx("ldaFromFiles(files, keywords)", globals(), locals(), "profile.out")
if __name__ == "__main__":
    main()
