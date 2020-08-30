from flickrLda.ldaModel import LdaModel
from glob import glob
import os.path

    
def main():
    for f in ["data/flickrLda.stemmed.100topics/model-final",
              "data/flickrLda.stemmed.200topics/model-final",
              "data/flickrLda.keywords/model-01800",]:
    #for f in sorted(glob("data/flickrLda.keywords/model-*.twords"))[0:3]:
        dirname, fname = os.path.split(f)
        f = dirname + os.path.sep + fname.split(".")[0]
        
        run = LdaModel(f)
        print "f", f 
        print run.logLiklihood()
        print
    
    
if __name__ == "__main__":
    main()
    