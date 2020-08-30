import unittest
import os
from routeDirectionCorpusReader import readSession, Standoff, Annotation, TextStandoff, descendentMap, ancestorMap, childrenMap


class TestCase(unittest.TestCase):
    

    def destOpen(self):
        session = None
        try:
            fname = "data/Direction understanding subjects Floor 1 (Final).ods"


            sessions = readSession(fname, "test")

            session = sessions[0]

            self.assertEqual(sessions[0].followed[0], "followed")
            self.assertEqual(sessions[6].followed[0], "questionable")
            self.assertEqual(sessions[3].followed[1], "not followed")
            self.assertEqual(sessions[14].followed[0], None)
            self.assertEqual(sessions[14].followed[9], None)

            instructionIdx = 0



            spatialRelation = Standoff(session, instructionIdx, (0, 1))
            
            session.addAnnotation(instructionIdx, 
                                  Annotation(verb=None, landmark=None,
                                             spatialRelation=spatialRelation))
            
            
            session.saveAnnotations()
            
            reloadedSessions = readSession(fname, "test")

            reloadedSession = reloadedSessions[0]
            reloadedInstruction = reloadedSession.routeAnnotations[instructionIdx][0]
            self.assertEqual(reloadedInstruction.__class__, Annotation)
            self.assertEqual(reloadedInstruction.spatialRelation.start, 0)
            self.assertEqual(reloadedInstruction.spatialRelation.end, 1)


            self.assertEqual(reloadedInstruction.verb.start, 0)
            self.assertEqual(reloadedInstruction.verb.end, 0)
        finally:
            if not (session is None):
                try:
                    os.remove(session.annotationFname)
                except OSError:
                    pass # ignore if file doesn't exist
    def destDotty(self):
        fname = "data/Direction understanding subjects Floor 1 (Final).ods"

        sessions = readSession(fname, "stefie10")

        session = sessions[0]
        
        instructionIdx = 0
        import dottyExporter
        dottyExporter.exportAsDotty(session, instructionIdx, "test.dot")
        
    def destAnnotation(self):
        text = "Go past the door, then through the hallway."
        
        annotation = Annotation(verb=TextStandoff(text, (0, 2)),
                                spatialRelation=TextStandoff(text, (3, 7)),
                                landmark=TextStandoff(text, (8, 16)))
        self.assertEqual(annotation.verb.text, "Go")
        self.assertEqual(annotation.spatialRelation.text, "past")
        self.assertEqual(annotation.landmark.text, "the door")



    def destOpenPartial(self):
        fname = "data/Direction understanding subjects Floor 1 (Final).ods"

        sessions = readSession(fname, "none", quadrant=0)
        self.assertEqual(len(sessions), 7)
        for s in sessions:
            self.assertEqual(len(s.routeInstructions), 5)


        sessions = readSession(fname, "none", quadrant=1)
        self.assertEqual(len(sessions), 7)
        for s in sessions:
            self.assertEqual(len(s.routeInstructions), 5)


        sessions = readSession(fname, "none", quadrant=2)
        self.assertEqual(len(sessions), 8)
        for s in sessions:
            self.assertEqual(len(s.routeInstructions), 5)


        sessions = readSession(fname, "none", quadrant=3)
        self.assertEqual(len(sessions), 8)
        for s in sessions:
            self.assertEqual(len(s.routeInstructions), 5)

            
    def testHelicopter(self):
        fname ="data/Direction understanding subjects Floor 1 (Helicopter).ods"
        sessions = readSession(fname, "none")
        self.assertTrue(sessions != None)
        
    def testDescendentMap(self):
        
        fname = "data/Direction understanding subjects Floor 1 (Final).ods"

        sessions = readSession(fname, "stefie10")
        for session in sessions:
            for instructionIdx, instruction in enumerate(session.routeInstructions):
                sdcs = session.routeAnnotations[instructionIdx]
                sdc_to_descendents = descendentMap(sdcs)
                for parent, children in sdc_to_descendents.iteritems():
                    for child in children:
                        self.assertEqual(parent.contains(child), True)



    def testChildrenMap(self):
        
        fname = "data/Direction understanding subjects Floor 1 (Final).ods"

        sessions = readSession(fname, "stefie10-d1-hierarchical")
        for session in sessions: 
            for instructionIdx, instruction in enumerate(session.routeInstructions):
                sdcs = session.routeAnnotations[instructionIdx]
                sdc_to_children = childrenMap(sdcs)
                for parent, children in sdc_to_children.iteritems():
                    for child in children:
                        self.assertEqual(parent.contains(child), True)
                        
                print sdc_to_children
                for sdc in sdcs:
                    count = 0
                    for parent, children in sdc_to_children.iteritems():
                        if sdc in children:
                            count += 1
                    print sdc, count
                    self.assertTrue(count <= 1)
                print
                print "printing map"
                sdc_to_children = childrenMap(sdcs)                
                for parent in sdcs:
                    children = sdc_to_children[parent]
                    print parent, len(children)                    
                    for child in children:
                        print " ", child
#                if "the words 'deli', 'soup', and 'oven' over you" in instruction:
#                    self.fail()
            


    def testAncestorMap(self):
        
        fname = "data/Direction understanding subjects Floor 1 (Final).ods"

        sessions = readSession(fname, "stefie10")
        for session in sessions:
            for instructionIdx, instruction in enumerate(session.routeInstructions):
                sdcs = session.routeAnnotations[instructionIdx]
                sdc_to_ancestors = ancestorMap(sdcs)
                for child, parents in sdc_to_ancestors.iteritems():
                    for parent in parents:
                        self.assertEqual(parent.contains(child), True)
                        

                        
                    
