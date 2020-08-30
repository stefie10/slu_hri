
from spatial_features_cxx import sfe_score_feature_map

import unittest

class TestCase(unittest.TestCase):
    def testScoreFeatureMap(self):
        features = {"x":1, "y":3, "z":6}
        weights = {"x":1, "y":3, "z":6}

        r = sfe_score_feature_map(features.keys(), features.values(),
                              weights.keys(), weights.values())
        
        self.assertEqual(r, 46)


    def testScoreFeatureMapMissingFeature(self):
        features = {"x":1, "y":3, }
        weights = {"x":1, "y":3, "z":6}

        r = sfe_score_feature_map(features.keys(), features.values(),
                              weights.keys(), weights.values())
        
        self.assertEqual(r, 10)

    def testScoreFeatureMapMissingWeight(self):
        features = {"x":1, "y":3, "z":6 }
        weights = {"x":1, "y":3, }

        r = sfe_score_feature_map(features.keys(), features.values(),
                              weights.keys(), weights.values())
        
        self.assertEqual(r, 10)

    def testEmpty(self):
        features = {"x":1, "y":3, "z":6 }
        weights = {}

        r = sfe_score_feature_map(features.keys(), features.values(),
                              weights.keys(), weights.values())
        
        self.assertEqual(r, 0)
