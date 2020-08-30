import unittest
import crfEntityExtractor
from routeDirectionCorpusReader import readSession

class CrfEntityExtractorTestCase(unittest.TestCase):
    
    def destWriteTraining(self):
        fname = "data/Direction understanding subjects Floor 8 (Final).ods"
        sessions = readSession(fname, 'stefie10')
        chunker = crfEntityExtractor.CrfChunker("data/out.model")
        chunker.writeTraining(sessions, "training.txt")

        self.fail()

        
    def testChunker(self):
        chunker = crfEntityExtractor.CrfChunker("data/out.model")
        indexes, tokens, tags = chunker.chunk("go towards the door")
        self.assertEqual(tags, 
                         ["verb", "spatialRelation", "landmark", "landmark"])


    def testSpatialDescriptionClassExtractor(self):
        extractor = crfEntityExtractor.SpatialDescriptionClauseExtractor()
        
        results = extractor.chunk("Go towards the door.  Then take a right.")

        annotation = results[0]
        self.assertEqual(annotation.verb.text, "Go")
        self.assertEqual(annotation.spatialRelation.text, "towards")
        self.assertEqual(annotation.landmark.text, "the door")

        annotation = results[1]
        self.assertEqual(annotation.verb.text, "take a right")
        self.assertEqual(annotation.spatialRelation.text, "")
        self.assertEqual(annotation.landmark.text, "")
        self.assertEqual(len(results), 2)

        
        
        
    def testBring(self):
        extractor = crfEntityExtractor.SpatialDescriptionClauseExtractor()
        
        results = extractor.chunk("Bring Nick to the elevators.")
        sdc = results[0]
        self.assertEqual(len(results), 1)
        self.assertEqual(sdc.verb.text, "Bring Nick")
        self.assertEqual(sdc.spatialRelation.text, "to")
        self.assertEqual(sdc.landmark.text, "the elevators")
        