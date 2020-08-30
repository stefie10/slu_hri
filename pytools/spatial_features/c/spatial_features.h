#ifndef SPATIAL_FEATURES_H
#define SPATIAL_FEATURES_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_math.h>
#include <assert.h>
#include <vector>
#include <string>
#include "gsl_utilities.h"
#include "math2d.h"
#include <math3d.h>
using namespace std;
#ifdef __cplusplus
extern "C" {
#endif

gsl_vector* spatial_features_distance_path_to_landmark(gsl_matrix* path_xy, 
						       gsl_matrix* landmark_xy);

double spatial_features_overlap_feature(double t1_st, double t1_end, 
					double t2_st, double t2_end);

double spatial_features_orientation_direction_between(gsl_vector* pose, gsl_matrix* path, 
						      double st_ang, double end_ang);

double spatial_features_theta_between(double theta, double theta_st, double theta_end);


#define NAMED_ENUM_LIST \
  X(F_distFigureStartToLandmarkCentroid),                \
    X(F_distFigureCenterOfMassToLandmarkCentroid),       \
    X(F_distFigureEndToLandmarkCentroid),                \
    X(F_distFigureStartToLandmark),                      \
    X(F_distFigureEndToLandmark),                        \
    X(F_distFigureCenterOfMassToLandmark)
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  distance_path_to_landmark_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  distance_path_to_landmark_features_names
#define NAMED_ENUM_COUNT_NAME()  distance_path_to_landmark_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME


/* these are features taken from stefanie's list */
gsl_vector* spatial_features_distance_path_to_landmark(gsl_matrix* path_xy, gsl_matrix* landmark_xy);



#define NAMED_ENUM_LIST \
  X(F_centroidToAxesOrigin),                           \
    X(F_figureCenterOfMassToAxesOrigin),                 \
    X(F_figureCenterOfMassToLandmarkCentroid),           \
    X(F_axesStartToLandmark),                            \
    X(F_axesEndToLandmark),                              \
    X(F_axesToLandmarkSum),                              \
    X(F_axesStartToFigureStart),                         \
    X(F_axesEndToFigureEnd),                             \
    X(F_axesToFigureSum),                                \
    X(F_ratioFigureToAxes),                              \
    X(F_ratioLengthFigureToAxes),                        \
    X(F_distAlongLandmarkBtwnAxes),                      \
    X(F_eigenAxesRatio)

#define NAMED_ENUM_FEATURE_INDEXES_NAME()  axes_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  axes_features_names
#define NAMED_ENUM_COUNT_NAME()  axes_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME


gsl_vector* spatial_features_axes(gsl_matrix* figure_xy, gsl_matrix* landmark_xy);

double spatial_features_displacement_feature(gsl_matrix* figure, gsl_matrix* landmark);


#define NAMED_ENUM_LIST                            \
  X(F_distStartLandmarkBoundary),                  \
    X(F_distEndLandmarkBoundary),                  \
    X(F_averageDistStartEndLandmarkBoundary),  \
    X(F_figureStartToEnd),                         \
    X(F_peakDistToAxes),                           \
    X(F_stdDevToAxes),  \
    X(F_averageDistToAxes),				\
    X(F_angleBtwnLinearizedObjects)
  
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  boundary_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  boundary_features_names
#define NAMED_ENUM_COUNT_NAME()  boundary_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME


gsl_vector* spatial_features_boundary(gsl_matrix* figure_xy, gsl_matrix* landmark_xy);





#define NAMED_ENUM_LIST \
  X(F_angleFigureToPastAxes),                      \
    X(F_pastAxesLength)
    
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  past_axes_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  past_axes_features_names
#define NAMED_ENUM_COUNT_NAME()  past_axes_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME


gsl_vector* spatial_features_past_axes(gsl_matrix* figure_xy, gsl_matrix* landmark_xy);




#define NAMED_ENUM_LIST \
  X(F_endPointsInLandmarkBoundingBox),             \
    X(F_startPointsInLandmarkBoundingBox)
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  bounding_box_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  bounding_box_features_names
#define NAMED_ENUM_COUNT_NAME()  bounding_box_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME


gsl_vector* spatial_features_bounding_box(gsl_matrix* figure_xy, gsl_matrix* landmark_xy);




#define NAMED_ENUM_LIST \
  X(F_distBtwnCentroids)

#define NAMED_ENUM_FEATURE_INDEXES_NAME()  distance_polygon_polygon_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  distance_polygon_polygon_features_names
#define NAMED_ENUM_COUNT_NAME()  distance_polygon_polygon_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME

gsl_vector* spatial_features_distance_polygon_polygon(gsl_matrix* figure_xy, 
                                                      gsl_matrix* landmark_xy);



#define NAMED_ENUM_LIST                         \
  X(F_avsResult),                               \
    X(F_avsHeightExp),                          \
    X(F_avsHeight),                             \
    X(F_avsg)

#define NAMED_ENUM_FEATURE_INDEXES_NAME()  avs_base_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  avs_base_features_names
#define NAMED_ENUM_COUNT_NAME()  avs_base_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME

#define AVS_DIRECTION_COUNT 4

static double avs_directions[AVS_DIRECTION_COUNT][2] = {
  {1, 0},
  {0, 1},
  {-1, 0},
  {0, -1}};

gsl_vector * spatial_features_avs_polygon_polygon(gsl_matrix * figure,
                                                  gsl_matrix * landmark,
                                                  double direction_theta);

vector<string> spatial_features_names_avs_polygon_polygon();


#define NAMED_ENUM_LIST                                                 \
  X(F_3dEndsHigherThanFigureLandmark),                                  \
    X(F_3dEndsHigherThanLandmarkFigure),                                \
    X(F_3dStartsHigherThanLandmarkFigure),                              \
    X(F_3dStartsHigherThanFigureLandmark),                              \
    X(F_3dSupportsFigureLandmark),                                      \
    X(F_3dSupportsLandmarkFigure),                                      \
    X(F_3dIntersectsFigureLandmark)
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  prism_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  prism_features_names
#define NAMED_ENUM_COUNT_NAME()  prism_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME
gsl_vector * spatial_features_prism_prism(math3d_prism_t figure,
                                          math3d_prism_t landmark);




#define NAMED_ENUM_LIST            \
  X(F_distFigureCentroidAxes)
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  between_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  between_features_names
#define NAMED_ENUM_COUNT_NAME()  between_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME
gsl_vector * spatial_features_three_polygons(gsl_matrix * figure,
                                             gsl_matrix * l1,
                                             gsl_matrix * l2);






#define NAMED_ENUM_LIST            \
  X(F_landmarkArea),               \
  X(F_landmarkPerimeter)
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  polygon_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  polygon_features_names
#define NAMED_ENUM_COUNT_NAME()  polygon_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME
gsl_vector * spatial_features_three_polygons(gsl_matrix * figure,
                                             gsl_matrix * l1,
                                             gsl_matrix * l2);


  //X(F_pathLength),							\  


#define NAMED_ENUM_LIST                                                 \
  X(F_ratioDistStartEndByPathLength),					\
    X(F_orientStEndSp),                                                 \
    X(F_orientDirSpathStraight),                                        \
    X(F_orientDirSpathBehind),                                         \
    X(F_orientDirSpathLeft),                                            \
    X(F_orientDirSpathRight)                                           \
    
#define NAMED_ENUM_FEATURE_INDEXES_NAME()  path_features_fi
#define NAMED_ENUM_CHAR_LIST_NAME()  path_features_names
#define NAMED_ENUM_COUNT_NAME()  path_features_count
#include "named_enum.h"
#undef NAMED_ENUM_LIST
#undef NAMED_ENUM_CHAR_LIST_NAME
#undef NAMED_ENUM_FEATURE_INDEXES_NAME
#undef NAMED_ENUM_COUNT_NAME
gsl_vector * spatial_features_three_polygons(gsl_matrix * figure,
                                             gsl_matrix * l1,
                                             gsl_matrix * l2);


char * flu_binarize_feature_uniform(char * name, double value, double min_val, 
                                    double max_val, int num_units);






#ifdef __cplusplus
}
#endif


#endif




