import crfEntityExtractor
import unittest
class TestCase(unittest.TestCase):
    def testChunking(self):
        extractor = crfEntityExtractor.SpatialDescriptionClauseExtractor("data/smv.crf.model")
        
        result = extractor.chunk("Go towards the windows.")
        self.assertEqual(len(result), 1)
        
        sdc = result[0]
        
        self.assertEqual(sdc.verb.text, "Go")
        self.assertEqual(sdc.spatialRelation.text, "towards")
        self.assertEqual(sdc.landmark.text, "the windows")
        self.assertEqual(sdc.landmark2.text, "")

        
        result = extractor.chunk("Bring the person to the windows.")
        self.assertEqual(len(result), 1)
        
        sdc = result[0]
        
        self.assertEqual(sdc.verb.text, 'Bring')
        self.assertEqual(sdc.landmark.text, "the person")
        self.assertEqual(sdc.landmark2.text, "to the windows")
        

        
