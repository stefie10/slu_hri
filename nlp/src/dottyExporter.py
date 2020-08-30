from routeDirectionCorpusReader import Standoff, Annotation, readSession, TextStandoff
import os
import annotations

def writeBaseNode(out, nodeName, text):
    if text != "":

        out.write('%s -> %sBaseNode;\n' % (nodeName, nodeName))
        out.write('%sBaseNode[label="%s"];\n' % (nodeName, text))

def exportAsDotty(session, instructionIdx, outFile, exportRange=None):
    if exportRange is None:
        exportRange = Standoff(session, instructionIdx, (0, len(session.routeInstructions[instructionIdx])))
    
    out = open(outFile, "w")
    out.write("digraph unix {\n")
    out.write('graph [ordering = "out"]\n');
    out.write('size="100,100";\n')
    out.write('node [color=lightblue2, style=filled];\n')



    labels = [(key, abbrv) for key, abbrv in zip(Annotation.keys, Annotation.abbrvKeys)]

    for i, annotation in enumerate(session.routeAnnotations[instructionIdx]):
        print "exportRange", exportRange.range
        print "annotation", annotation.range.range
        print "annotation", annotation.text
        if exportRange.contains(annotation.range):
            for key, label in labels:
                out.write("SDC%d -> %s%d;\n" % (i, key, i))
                writeBaseNode(out, "%s%d" % (key, i), 
                              annotation.annotationMap[key].text)
                out.write('%s%d[label="%s"];\n' % (key,i, label))

            

    tree = annotations.tree(session.routeAnnotations[instructionIdx])
    for i, annotation in enumerate(session.routeAnnotations[instructionIdx]):
        if exportRange.contains(annotation.range):
            for childIdx in range(len(session.routeAnnotations[instructionIdx])):
                if tree[i, childIdx]:

                    child = session.routeAnnotations[instructionIdx][childIdx]

                    for key in Annotation.keys:
                        if annotation.annotationMap[key].contains(child.range):
                            out.write("%s%dBaseNode -> SDC%d;\n" % (key, i, childIdx))

            numParents = tree[:,i].sum()
            if numParents == 0:
                out.write("S -> SDC%d;\n" % i)


    out.write("}\n")
    out.close()
    os.system("dot %s -Grankdir=LR -Tpng -o %s.png" % (outFile, outFile))

def main():

    fname = "data/Direction understanding subjects Floor 8 (Final).ods"

    sessions = readSession(fname, "stefie10")

    session = sessions[0]

    instructionIdx = 0

    annotation = session.routeAnnotations[instructionIdx][4]
    
    print "range", annotation.range
    exportAsDotty(session, instructionIdx, "test.dot", 
                  TextStandoff(annotation.entireText, (83, 189)))


if __name__ == "__main__":
    main()
