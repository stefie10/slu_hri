from glob import glob
from os.path import dirname
from voom.gui.assignments import assignmentData
from voom.verbs import follow, meet, bring, avoid, wander, go
import os
import tag_util

def verbAssignment(username, fname, tagFile, skeleton):
    engineMap = dict((x.name, x) for x in 
                   [bring.Engine(), follow.Engine(), meet.Engine(), 
                    avoid.Engine(), wander.Engine(), go.Engine()])


    print "verbs", engineMap
    assignmentFname = "data/aaai_2010_smv/%s/%s" % (username, fname)
    dir = dirname(assignmentFname)
    if not os.path.exists(dir):
        os.makedirs(dir)

    entries = []
    for verb_fname in glob("data/motion_commands/aaai2010_multiple_commands2.txt"):
        print "fname", verb_fname
        dir, fname = os.path.split(verb_fname)
        verb, suffix = fname.split(".")
        
        #assert verb in engineMap, (verb, engineMap.keys())
        commands = [c for c in open(verb_fname, "r") if c.strip() != '']
        for c in commands:
            verb = c.split()[0].lower()
            print "verb", verb
            entry = assignmentData.VerbAssignmentEntry(verb, c, tagFile, skeleton)
            entries.append(entry)



    assignment = assignmentData.Assignment(entries, tagFile, skeleton)
    print 'saving', assignmentFname
    assignment.save(assignmentFname)


def main():
    from sys import argv
    import cPickle
    
    map_fn = argv[1]
    gtruth_tag_fn = argv[2]
    skeleton_fn = argv[3]
    tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
    tagFile.get_map()
    tagFile.get_tag_names()

    skeleton = cPickle.load(open(skeleton_fn, 'r'))

    verbAssignment("stefie10", "1.yaml", tagFile, skeleton)
        
if __name__ == "__main__":
    main()
