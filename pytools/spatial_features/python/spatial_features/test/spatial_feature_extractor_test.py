import unittest
from spatial_features_cxx import sfe_path_features, sfe_extract_path_path, \
    sfe_overlap_features, sfe_polygon_features, sfe_path_polygon_features, \
    sfe_f_path_l_polygon_names, sfe_get_normalization_mask, \
    sfe_extract_f_path_l_polygon, sfe_normalize_feature_vector
from scipy import array
from math import pi

class SpatialFeatureExtractorTestCase(unittest.TestCase):

    def test_spatial_feature_extractor_path_features(self):
        fnames = ["edist_sp", "int_path_sp", "orient_st_end_sp", "orient_dir_spath_str",    
                  "orient_dir_spath_left", "orient_dir_spath_right"]

        path = [[0, 1, 100], 
                [0, 1, 100],
                [0, pi/2.0, pi]]

        #first is the crow distance and second is the integrated distance
        print array(path)
        print "path:", zip(fnames, sfe_path_features(path));

        path = [[0, 1, 100], 
                [0, 1, 100],
                [0, pi/2.0, pi-0.01]]

        #first is the crow distance and second is the integrated distance
        print array(path)
        print "path:", zip(fnames, sfe_path_features(path));

        path = [[0, 0, 100],
                [0, 100, 100],
                [0, pi/2.0, pi]]

        #first is the crow distance and second is the integrated distance
        print array(path)
        print "path:", zip(fnames, sfe_path_features(path));

        path = [[0, 0, 100, 100],
                [0, 100, 100, 1000],
                [pi, pi/2.0, pi, pi]]

        #first is the crow distance and second is the integrated distance
        print array(path)
        print "path:", zip(fnames, sfe_path_features(path));

    #features: "edist_end_st_pp", "edist_end_end_pp", "edist_st_st_pp", "edist_st_end_pp", "edist_mean_pp"
    def test_spatial_feature_extractor_path_path_features(self):
        fnames = [ "edist_end_st_pp", "edist_end_end_pp", "edist_st_st_pp", "edist_st_end_pp", "edist_mean_pp",
                   "orient_st_end_pp", "orient_end_end_pp", "orient_st_st_pp", "orient_end_st_pp", 
                   "orient_dir_st_pp_45deg", "orient_dir_end_pp_45deg", "orient_dir_st_pp_90deg", "orient_dir_end_pp90deg", 
                   "orient_dir_st_pp_45deg_right", "orient_dir_end_pp_45deg_right", "orient_dir_st_pp_45deg_left", "orient_dir_end_pp_45deg_left"]

        path = [[0, 10, 20], 
                [0, 10, 20],
                [0, pi/2.0, pi]]
        print "edist_end_st_pp", "edist_end_end_pp", "edist_st_st_pp", "edist_st_end_pp", "edist_mean_pp"
        print sfe_extract_path_path(path, path);

        print array(path);
        print array(path)
        for e in zip(fnames, sfe_extract_path_path(path, path)):
            print e


        path2 = [[20, 30, 40], 
                [20, 30, 40],
                [0, pi/2.0, pi]]
        print array(path);
        print array(path2)
        for e in zip(fnames, sfe_extract_path_path(path, path2)):
            print e

        path2 = [[20, 30, 40], 
                [20, 30, 40],
                [0, 0, 0]]
        print array(path);
        print array(path2)
        for e in zip(fnames, sfe_extract_path_path(path, path2)):
            print e


        path = [[0, 10, 20], 
                [0, 10, 20],
                [0,0, 0]]
        print array(path);
        print array(path2)
        for e in zip(fnames, sfe_extract_path_path(path, path2)):
            print e


    def test_spatial_feature_extractor_overlap_features(self):
        fnames = ["overlap_end_st", "overlap_st_end"]
        print fnames
        print sfe_overlap_features(100, 200, 150, 250);
        print sfe_overlap_features(100, 200, 150, 650);
        print sfe_overlap_features(100, 1000, 150, 250);

    def test_spatial_feature_extractor_landmark_features(self):
        features = ["lmark_area", "lmark_perimeter"];
        lmark = array([[100, 100, 110, 110.0], 
                       [-10, 10, 10, -10]]);

        print zip(features, sfe_polygon_features(lmark));


    def test_spatial_feature_extractor_path_polygon(self):
        fnames = ["front_st", "right_st", "left_st", "behind_st", 
                  "front_end", "right_end", "left_end", "behind_end", "displacementFromGround", 
                  "distFigureStartToGroundCentroid", "distFigureCOMToGroundCentroid", "distFigureEndToGroundCentroid",
                  "distFigureStartToGround", "distFigureEndToGround", 'averageDistStartGroundDistEndGround', "distFigureCOMToGround", 
                  "centroidToAxesOrigin", "figureCenterOfMassToAxesOrigin", "figureCenterOfMassToGroundCentroid",
                  "axesStartToGround", "axesEndToGround", "axesToGroundSum",
                  "axesStartToFigureStart", "axesEndToFigureEnd", "axesToFigureSum", 
                  "ratioFigureToAxes", "ratioLengthFigureToAxes"]
        path_xy = array([[0, 10, 20], 
                         [0, 0, 0],
                         [0,0, 0.0]])

        landmark_xy = array([[100, 100, 110, 110.0], 
                             [-10, 10, 10, -10]]);

        print sfe_path_polygon_features(path_xy, landmark_xy)
        print zip(fnames, sfe_path_polygon_features(path_xy, landmark_xy))

        landmark_xy = array([[100, 100, 110, 110.0], 
                             [0, 10, 10, 0]]);

        print zip(fnames, sfe_path_polygon_features(path_xy, landmark_xy))

        landmark_xy = array([[100, 100, 110, 110.0], 
                             [-10, 0, 0, -10]]);

        print zip(fnames, sfe_path_polygon_features(path_xy, landmark_xy))

        path_xy = array([[300, 310, 320], 
                         [0, 0, 0],
                         [0,0, 0.0]])                    
        print zip(fnames, sfe_path_polygon_features(path_xy, landmark_xy))

        #for i in range(100000):
        #    #print zip(fnames, sfe_path_polygon_features(path_xy, 
        #landmark_xy))
        #    sfe_path_polygon_features(path_xy, landmark_xy)

    def test_extract_all_features(self):
        print "starting normalized features"
        all_names = sfe_f_path_l_polygon_names();
        #names = vectors(list(all_names));
        #print list(all_names), names
        mask = sfe_get_normalization_mask(all_names);

        print "normalization mask"
        print zip(all_names, mask)

        #print list(all_names)
        #raw_input()
        path_xyth = array([[0, 10, 20], 
                         [0, 0, 0],
                         [0,0, 0.0]])

        path_xy = path_xyth[0:2,:]

        landmark_xy = array([[100, 100, 110, 110.0], 
                             [-10, 10, 10, -10]]);

        feats = sfe_extract_f_path_l_polygon(path_xyth, landmark_xy, False);

        print zip(all_names, feats);
        print len(mask), len(feats)
        feats_norm = sfe_normalize_feature_vector(path_xy, landmark_xy, mask, feats);
        print "norm", zip(all_names, feats_norm);

        landmark_xy = array([[100, 100, 110, 110.0], 
                             [0, 10, 10, 0]]);

        feats = sfe_extract_f_path_l_polygon(path_xyth, landmark_xy, False);
        print zip(all_names, feats);

        feats_norm = sfe_normalize_feature_vector(path_xy, landmark_xy, mask, feats);
        print "norm", zip(all_names, feats_norm);

        landmark_xy = array([[100, 100, 110, 110.0], 
                             [-10, 0, 0, -10]]);

        feats = sfe_extract_f_path_l_polygon(path_xyth, landmark_xy, False);
        print zip(all_names, feats);

        feats_norm = sfe_normalize_feature_vector(path_xy, landmark_xy, mask, feats);
        print "norm", zip(all_names, feats_norm);

        path_xyth = array([[300, 310, 320], 
                         [0, 0, 0],
                         [0,0, 0.0]])                    
        path_xy = path_xyth[0:2,:]

        feats = sfe_extract_f_path_l_polygon(path_xyth, landmark_xy, False);
        print zip(all_names, feats);

        feats_norm = sfe_normalize_feature_vector(path_xy, landmark_xy, mask, feats);
        print "norm", zip(all_names, feats_norm);

        for i in range(len(all_names)):
            print all_names[i], feats[i], feats_norm[i]
        #raw_input()


