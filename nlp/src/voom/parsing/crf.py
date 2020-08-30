from crfEntityExtractor import CrfChunker
from environ_vars import TKLIB_HOME
from voom.gui.assignments.assignmentData import Assignment
import carmen_map_skeletonizer
import tag_util


def main():
    
    map_fn = "%s/data/directions/direction_floor_3/direction_floor_3_small_filled.cmf" % TKLIB_HOME
    cluster_fn = "%s/data/directions/direction_floor_3/skels/direction_floor_3_skel.pck" % TKLIB_HOME
    gtruth_tag_fn = "%s/data/directions/direction_floor_3/tags/df3_small_tags.tag" % TKLIB_HOME
    assignment_fns = ["%s/nlp/data/aaai_2010_smv/stefie10/assignment1.2.yaml" % TKLIB_HOME, "%s/nlp/data/aaai_2010_smv/stefie10/assignment_multiple_1.yaml" % TKLIB_HOME]
    tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
    tagFile.get_map()
    tagFile.get_tag_names()
    

    skeleton = carmen_map_skeletonizer.load(cluster_fn, map_fn)

    
    modelFile = "%s/nlp/data/smv.crf.model" % TKLIB_HOME
    
    
    chunker = CrfChunker(modelFile)
    

    trainingFile = "%s/nlp/training.txt" % TKLIB_HOME

    out = open(trainingFile, "w")
    for assignment_fn in assignment_fns:
        assignment = Assignment.load(assignment_fn, tagFile, skeleton)
        for entry in assignment.entries:
            chunker.writeTrainingForText(entry.command, entry.sdcs("stefie10"),
                                         out)
    
    out.close()
    chunker.runTraining(TKLIB_HOME+"/nlp/etc/crf++/test.template",
                        trainingFile, modelFile)

            
    

    

if __name__ == "__main__":
    main()
