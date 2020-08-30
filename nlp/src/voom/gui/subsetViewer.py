import matplotlib
matplotlib.use("Qt4Agg")

from environ_vars import TKLIB_HOME
from voom import trainer_pacman
from voom.gui.assignments.assignmentData import Assignment, VerbAssignmentEntry
from voom.gui.assignments.assignmentEditor import MainWindow
from voom.verbs import follow

import tag_util


def main():
    
    
    from sys import argv
    import cPickle
    import basewindow
    app = basewindow.makeApp()
    
    map_fn = argv[1]
    gtruth_tag_fn = argv[2]
    cluster_fn = argv[3]
    assignment_fn = argv[4]
    tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
    tagFile.get_map()
    tagFile.get_tag_names()

    skeleton = cPickle.load(open(cluster_fn, 'r'))

    wnd = MainWindow(tagFile, skeleton, isEditable=True)
    wnd.show()
    humanAssignment = Assignment.load("%s/nlp/data/aaai_2010_smv/stefie10/assignment1.1.yaml" % TKLIB_HOME, tagFile, skeleton)
    
    engine = follow.Engine()
    
    table = trainer_pacman.makeTable(engine, [humanAssignment])
    
    subsetTable = trainer_pacman.makeSubsetExamples(engine, table)
    
    entries = []
    for i,ex in enumerate(subsetTable):
        print "making entry", i
        entry = VerbAssignmentEntry(ex["entry"].value.verb, ex["entry"].value.command,
                                    tagFile, skeleton,
                                    situation=ex["situation"].value)
        entries.append(entry)        
        if i > 10:
            break
    
    wnd.load(Assignment(entries, tagFile, skeleton))


    retval = app.exec_()
if __name__ == "__main__":
    main()
