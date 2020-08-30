from os import system
import math2d
import os
import shutil

def inference(directory, words):
    
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)
    
    input_fname = "%s/model.dat" % directory
    outfile = open(input_fname, "w")
    outfile.write("%d\n" % len(words))
    for wlist in words:
        outfile.write(" ".join(wlist))
        outfile.write("\n")
    outfile.close()
    
    cmd = "3rdParty/gibbslda++/GibbsLDA++-0.2/src/lda -inf " + \
        "-dir data/flickrLda/ -model model-00500 -niters 1000 -twords 20 -dfile input/model.dat"
    print "cmd", cmd
    system(cmd)

def main():
    docs = list(math2d.powerset(["window", "door", "microwave", "refrigerator", "desk", "table", "chair",
                                 "elevator", "clock", "urinal", "sink", "nice", "view"]))

    inference("data/flickrLda/input", docs)
if __name__ == "__main__":
    main()
    
    
