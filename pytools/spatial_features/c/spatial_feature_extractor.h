#ifndef SPATIAL_FEATURE_EXTRACTOR_H
#define SPATIAL_FEATURE_EXTRACTOR_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_math.h>
#include <math.h>
#include "spatial_features.h"

#include <vector>
#include <string>
#include <math3d.h>

using namespace std;

#ifdef __cplusplus
extern "C" {
#endif
/*

This module contains the public-facing interface to the feature
extraction library.  It should be agnostic to specific models.

Naming conventions for spatial_feature_extractor.c:
* sfe_GEOM_DESC_features for all the low level feature groups.  DESC
   can be blank if there are not multiple subgroups.  Example:
   sfe_path_polygon_features, sfe_polygon_features, sfe_prism_features,
   sfe_polygon_avs_features

* For feature groups associated with edges in the model we have:
   sfe_extract_ESDCTYPE_GEOM_ESDCTYPE_GEOM.  Examples:
   sfe_extract_f_path_l_polygon sfe_extract_f_polygon_l_polygon,
*/
    
/*******************************************************************************/
/* get the feature transition names */
/* extract all the transition features */
gsl_vector* sfe_extract_path_path(gsl_matrix* fig1_xyth, 
                                  gsl_matrix* fig2_xyth);
							 


/* extract all the observation features */
gsl_vector* sfe_extract_f_path_l_polygon(gsl_matrix* fig1_xyth, 
                                         gsl_matrix* gnd1_xy, 
                                         bool normalize);
  

/*******************************************************************************/
/* Normalization Routines, use the above and then normalize using these functions*/
/*******************************************************************************/


enum spatial_feature_normalization_methods 
{
  NORMALIZATION_NONE,
  NORMALIZATION_BBOX_ALL,
  NORMALIZATION_BBOX_AREA,
  NORMALIZATION_BBOX_FIGURE,
  NORMALIZATION_FIGURE_LENGTH,
  NORMALIZATION_AXES
 };

gsl_vector* sfe_get_normalization_mask(vector<string> feat_names);

gsl_vector* sfe_normalize_feature_vector(gsl_matrix* pts1, 
                                         gsl_matrix* pts2,
                                         gsl_vector* mask,
                                         gsl_vector* feat_vec);


/*******************************************************************************/
/* lists of the returned features are documented along with each function in the .c file*/
/*******************************************************************************/

/* landmark only*/
gsl_vector* sfe_polygon_features(gsl_matrix* landmark);

/* path only*/
gsl_vector* sfe_path_features(gsl_matrix* path_xyth);

#define NAMED_ENUM_LIST \
  X(F_front_st),                                       \
    X(F_right_st),                                     \
    X(F_left_st),                                      \
    X(F_behind_st),                                    \
    X(F_front_end),                                    \
    X(F_right_end),                                    \
    X(F_left_end),                                     \
    X(F_behind_end),                                   \
    X(F_displacementFromLandmark)
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  angle_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  angle_features_names
#define NAMED_ENUM_COUNT_NAME()  angle_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME


/* path-landmark features*/
gsl_vector* sfe_path_polygon_features(gsl_matrix* path_xy, 
                                      gsl_matrix* landmark_xy);

/* path-path overlap features*/
gsl_vector* sfe_overlap_features(double t1_st, double t1_end, 
                                 double t2_st, double t2_end);


gsl_vector * sfe_merge_feature_vectors(vector<gsl_vector *> features);
void sfe_free_features(vector<gsl_vector *> features);

/*******************************************************************************/
/* Internal functions */
/*******************************************************************************/
vector<string> sfe_polygon_names();
vector<string> sfe_path_names();
vector<string> sfe_overlap_names();
vector<string> sfe_path_path_names();
vector<string> sfe_path_polygon_names();
vector<string> sfe_f_prism_l_prism_names();
vector<string> sfe_f_polygon_l_polygon_names();
vector<string> sfe_f_polygon_l_polygon_l_polygon_names();
vector<string> sfe_f_path_l_polygon_names(void);

gsl_vector* sfe_f_polygon_l_polygon(gsl_matrix* p1_xy,
                                    gsl_matrix* p2_xy,
                                    bool normalize);

gsl_vector* sfe_f_polygon_l_polygon_l_polygon(gsl_matrix* f_xy,
                                              gsl_matrix* l1_xy,
                                              gsl_matrix* l2_xy);


gsl_vector* sfe_f_prism_l_prism(math3d_prism_t p1, math3d_prism_t p2, bool normalize);

gsl_vector* flu_polygon(vector<string> figure, 
                        gsl_matrix* gnd1_xy, 
                        bool perform_scaling);

vector<string> flu_polygon_names(vector<string> figure);

vector<string> crf_get_word_features(vector<string> tokens, 
				     vector<string> names, string prefix);

double sfe_score_feature_map(vector<string> fnames, gsl_vector * fvalues,
                             vector<string> weight_names, gsl_vector * weights);
#ifdef __cplusplus
}
#endif


#endif
