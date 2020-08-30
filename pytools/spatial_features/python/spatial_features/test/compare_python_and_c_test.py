import unittest

from spatial_features_cxx import sfe_extract_f_path_l_polygon, \
    sfe_f_path_l_polygon_names

from features.feature_utils import compute_fdict
from assert_utils import assert_sorta_eq

class ComparePythonAndCSpatialFeaturesTestCase(unittest.TestCase):
    def test_features(self):
        from spatial_feature_expected_results import results
        
        for result in results:
            fig_xyth = result["args"]["fig_xyth"]
            gnd_xy = result["args"]["gnd_xy"]
            result_dict = result["result"]
            
            feats_C = sfe_extract_f_path_l_polygon(fig_xyth, gnd_xy, 
                                                   normalize=True);
            names_C = sfe_f_path_l_polygon_names();

            fdict = compute_fdict(names_C, feats_C)
            for key, value in fdict.iteritems():
                expected_value = result_dict[key]
                assert_sorta_eq(value, expected_value)
                

