import sys
from histograms import Histogram, graphStacked
import re
import pylab as mpl


class Annotation:
    def __init__(self, command, annotation):
        self.command = command
        self.annotation = annotation
        
def main():
    annotation_fname = sys.argv[1]

    command = ""
    annotation = ""
    
    annotations = []
    for line in open(annotation_fname, "r"):
        line = line.strip()

        
        if line == "":
            if command != "" and annotation != "":
                annotations.append(Annotation(command, annotation))
                command = ""
                annotation = ""
        else:

            if line[0] != "(":
                command += line
            else:
                annotation += line
    histogram = make_histogram(annotations, "V")
    graphStacked({"stefie10":histogram}, "histogram", "verbs")

    graphStacked({"stefie10":make_histogram(annotations, "SR")}, 
                 "histogram", "spatial relations")
    mpl.show()
    
def make_histogram(annotations, key):
    pattern = re.compile("\((%s)\s+([^)]+)\)" % key)
    hist = Histogram()
    for a in annotations:
        for match in pattern.finditer(a.annotation):
            print match.group(1), match.group(2)
            hist.add(match.group(2).lower())
    return hist
            

    
if __name__ == "__main__":
    main()

    
