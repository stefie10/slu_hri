import unittest
from routeDirectionCorpusReader import readSession, Annotation, parent_in_set
import annotations

class AnnotationTestCase(unittest.TestCase):
    def test_parent_in_set(self):
        fname = "data/Direction understanding subjects Floor 8 (Final).ods"
        sessions = readSession(fname, 'stefie10')
        
        sdcs = sessions[0].routeAnnotations[0]
        for i, sdc in enumerate(sdcs):
            print i, sdc
        
        self.assertEqual(parent_in_set(sdcs[0], sdcs), False)
        self.assertEqual(parent_in_set(sdcs[5], sdcs), True)


        
        
                                                
    def testMatrix(self):
        fname = "data/Direction understanding subjects Floor 8 (Final).ods"
        sessions = readSession(fname, 'stefie10')
        
        entities = sessions[0].routeAnnotations[0]
        untilTopLevel = entities[4]
        untilContained = entities[5]
        print "top", untilTopLevel.landmark.range
        for key in Annotation.keys:
            print key, untilTopLevel[key].range, untilTopLevel[key].text
        print
        for key in Annotation.keys:
            print key, untilContained[key].range, untilContained[key].text
            
        print "contained", untilContained.range.range
        self.assertEqual(untilTopLevel.contains(untilContained), True)

        
        matrix = annotations.containmentMatrix(entities)
        print matrix
        print matrix.any()
        self.assertEqual(matrix.any(), True)
        self.assertEqual(matrix[4, 5], True)
        matrix[4,5] = False
        self.assertEqual(matrix.any(), False)
                    
    def testTreeSingle(self):
        fname = "data/Direction understanding subjects Floor 8 (Final).ods"
        sessions = readSession(fname, 'stefie10')
        
        entities = sessions[0].routeAnnotations[0]
        matrix = annotations.tree(entities)
        self.assertEqual(matrix[4,5], True)
        
        # another test
        entities = sessions[12].routeAnnotations[5]
        matrix = annotations.tree(entities)

        
    def testTreeAll(self):
        fname = ["data/Direction understanding subjects Floor 8 (Final).ods",
                 "data/Direction understanding subjects Floor 1 (Final).ods"]
        sessions = []
        for f in fname:
            sessions.extend([x for x in readSession(f, 'stefie10')])

        for i, session in enumerate(sessions):
            for instructionIdx, entities in session.routeAnnotations.iteritems():
                print "subject", i, session.subject
                print "instruction", instructionIdx
                matrix = annotations.tree(entities)
        
