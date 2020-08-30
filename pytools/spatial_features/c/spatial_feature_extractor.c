#include "spatial_feature_extractor.h"
#include "spatial_features.h"
#include <assert.h>
#include <stdio.h>
#include <unordered_map>
#include <string.h>
using namespace __gnu_cxx;
struct eqstr
{
  bool operator()(const char* s1, const char* s2) const
  {
    return strcmp(s1, s2) == 0;
  }
};



/**
 * compute the dot product, using both sparse weights and sparse
 * feature values.  Didn't end up being faster than python; somethign
 * weird.
 */
double sfe_score_feature_map(vector<string> fnames, gsl_vector * fvalues,
                             vector<string> weight_names, gsl_vector * weights)
{

  if (fvalues == NULL || weights == NULL) {
    return 0.0;
  }
  unordered_map<const char *, double, hash< const char* >, eqstr > weightmap;

  for (unsigned int i = 0; i < weights->size; i++) {
    weightmap[weight_names[i].c_str()] = gsl_vector_get(weights, i);
  }

  double result = 0.0;
  for (unsigned int i = 0; i < fvalues->size; i++) {
    double weight = 0.0;
    if (weightmap.count(fnames[i].c_str()) != 0) {
      weight = weightmap[fnames[i].c_str()]; 
    }
    result += weight * gsl_vector_get(fvalues, i);
  }
  return result;
}

//get the word features
vector<string> crf_get_word_features(vector<string> tokens, 
				     vector<string> names, string prefix){
  
  vector<string> ret_names;
  
  string str = "";
  for(unsigned int k=0; k<tokens.size(); k++){
    for(unsigned int i=0; i<names.size(); i++){
      //print prefix+w+"_"+name,
      ret_names.push_back(str+prefix+tokens[k]+"_"+names[i]);
    }
  }
  
  return ret_names;
}



double sfe_bounding_box_normalizer(gsl_matrix* fig1_xy, 
                                   gsl_matrix* gnd_xy){

  /*combine the points if both are not null, otherwise, use one*/
  gsl_matrix* combined;
  if(fig1_xy != NULL && gnd_xy !=NULL)
    combined = math2d_combined_matrix(fig1_xy, gnd_xy);
  else if(fig1_xy == NULL)
    combined = gnd_xy;
  else if(gnd_xy == NULL)
    combined = fig1_xy;
  else
    return 0;

  //compute the bounding box and get the scale
  gsl_vector* bbox = math2d_bbox(combined);
  double scale = math2d_get_scale(bbox);
  
  //free the memory, if applicable
  if(fig1_xy != NULL && gnd_xy !=NULL)
    gsl_matrix_free(combined);
  gsl_vector_free(bbox);

  //return the scale factor
  return scale;
}


double sfe_bounding_box_area_normalizer(gsl_matrix* fig1_xy, 
                                        gsl_matrix* gnd_xy){

  /*combine the points if both are not null, otherwise, use one*/
  gsl_matrix* combined;
  if(fig1_xy != NULL && gnd_xy !=NULL)
    combined = math2d_combined_matrix(fig1_xy, gnd_xy);
  else if(fig1_xy == NULL)
    combined = gnd_xy;
  else if(gnd_xy == NULL)
    combined = fig1_xy;
  else
    return 0;

  //compute the bounding box and get the scale
  gsl_vector* bbox = math2d_bbox(combined);
  double area = math2d_bbox_area(bbox);
  
  //free the memory, if applicable
  if(fig1_xy != NULL && gnd_xy !=NULL) {
    gsl_matrix_free(combined);
  }
  gsl_vector_free(bbox);

  //return the scale factor
  return area;
}


double sfe_bounding_box_pts_normalizer(gsl_matrix* pts_xy) 
{
  if(pts_xy == NULL)
    return 0;
  
  gsl_vector* bbox = math2d_bbox(pts_xy);
  double scale = math2d_get_scale(bbox);

  if(bbox != NULL)
    gsl_vector_free(bbox);
  
  return scale;
}


double sfe_axes_normalizer(gsl_matrix* fig1_xy, 
                           gsl_matrix* gnd_xy){
  struct axes axes = math2d_compute_axes(gnd_xy, fig1_xy);

  if (axes.minor_st == NULL) {
    return 0;
  }

  double scale = math2d_dist(axes.minor_st, axes.minor_end);

  math2d_axes_free(axes);
  return scale;
}

vector<string> sfe_bounding_box_normalizer_names(){
  //could be included: 'edist_sp', 'int_path_sp'
  vector<string> mynames;
  
  mynames.push_back("F_displacementFromLandmark");
  mynames.push_back("F_distFigureStartToLandmarkCentroid");
  mynames.push_back("F_distFigureCenterOfMassToLandmarkCentroid");
  mynames.push_back("F_distFigureEndToLandmarkCentroid");
  mynames.push_back("F_distFigureStartToLandmark");
  mynames.push_back("F_distFigureEndToLandmark");
  mynames.push_back("F_averageDistStartEndLandmark");
  mynames.push_back("F_distFigureCenterOfMassToLandmark");
  mynames.push_back("F_centroidToAxesOrigin");
  mynames.push_back("F_figureCenterOfMassToAxesOrigin");
  mynames.push_back("F_figureCenterOfMassToLandmarkCentroid");
  mynames.push_back("F_axesStartToLandmark");
  mynames.push_back("F_axesEndToLandmark");
  mynames.push_back("F_axesToLandmarkSum");
  mynames.push_back("F_axesStartToFigureStart"); 
  mynames.push_back("F_axesEndToFigureEnd");
  mynames.push_back("F_axesToFigureSum");
  mynames.push_back("F_landmarkPerimeter");
  mynames.push_back("F_distBtwnCentroids");

  return mynames;
}

vector<string> sfe_figure_length_normalizer_names(){
  vector<string> mynames;
  return mynames;
}

vector<string> sfe_bounding_box_area_normalizer_names(){
  vector<string> names;
  names.push_back("F_landmarkArea");
  return names;
}

vector<string> sfe_bounding_box_figure_normalizer_names(){
  //could be included: 'edist_sp', 'int_path_sp'
  vector<string> mynames;
  mynames.push_back("F_peakDistToAxes");
  mynames.push_back("F_figureStartToEnd");
  mynames.push_back("F_pastAxesLength");
  mynames.push_back("F_distStartLandmarkBoundary");
  mynames.push_back("F_distEndLandmarkBoundary");
  mynames.push_back("F_averageDistStartEndLandmarkBoundary");

  return mynames;
}



vector<string> sfe_axes_minor_normalizer_names(){
  vector<string> mynames;
  mynames.push_back("F_ratioFigureToAxes");
  mynames.push_back("F_ratioLengthFigureToAxes");
  return mynames;
}

static bool vector_contains(vector<string> names, string name) {
  for(size_t i=0; i < names.size(); i++) {
    if (names[i] == name) {
      return true;
    }
  }
  return false;
}
gsl_vector* sfe_get_normalization_mask(vector<string> feat_names){
  gsl_vector* mask = gsl_vector_calloc(feat_names.size());
  vector<string> bb_names = sfe_bounding_box_normalizer_names();
  vector<string> bb_figure_names = sfe_bounding_box_figure_normalizer_names();
  vector<string> figure_length_names = sfe_figure_length_normalizer_names();
  vector<string> bb_area_names = sfe_bounding_box_area_normalizer_names();

  for(unsigned int i=0; i<feat_names.size(); i++) {
    if (vector_contains(bb_names, feat_names[i])) {
      gsl_vector_set(mask, i, NORMALIZATION_BBOX_ALL);
    } else if (vector_contains(bb_figure_names, feat_names[i])) {
      gsl_vector_set(mask, i, NORMALIZATION_BBOX_FIGURE);
    } else if (vector_contains(bb_figure_names, feat_names[i])) {
      gsl_vector_set(mask, i, NORMALIZATION_FIGURE_LENGTH);
    } else if (vector_contains(bb_area_names, feat_names[i])) {
      gsl_vector_set(mask, i, NORMALIZATION_BBOX_AREA);
    } else {
      gsl_vector_set(mask, i, NORMALIZATION_NONE);
    }
  }
  
  return mask;
}


gsl_vector* sfe_normalize_feature_vector(gsl_matrix* figure_xy, 
                                         gsl_matrix* ground_xy,
                                         gsl_vector* mask,
                                         gsl_vector* feat_vec) 
{
  gsl_vector* ret_vec = gsl_vector_calloc(feat_vec->size);
  gsl_vector_memcpy(ret_vec, feat_vec);
  
  double scale_bb = 1;   double scale_axes = 1;
  double scale_bb_figure = 1;
  double scale_figure_length = 1;
  double scale_bb_area = 1;

  if(figure_xy == NULL && ground_xy == NULL){
    return ret_vec;
  } else if (figure_xy == NULL) {
    scale_bb = sfe_bounding_box_normalizer(NULL, ground_xy);
    scale_axes = sfe_axes_normalizer(NULL, ground_xy);
  } else if(ground_xy == NULL){
    //gsl_matrix_view figure_xy = gsl_matrix_submatrix(figure_xyth, 0, 0, 2, figure_xyth->size2);
    scale_bb = sfe_bounding_box_normalizer(figure_xy, NULL);
    scale_axes = sfe_axes_normalizer(figure_xy, NULL);
    scale_bb_figure = sfe_bounding_box_pts_normalizer(figure_xy);
    scale_figure_length = math2d_line_length(figure_xy);
  } else {
    //gsl_matrix_view figure_xy = gsl_matrix_submatrix(figure_xyth, 0, 0, 2, figure_xyth->size2);
    scale_bb = sfe_bounding_box_normalizer(figure_xy, ground_xy);
    scale_axes = sfe_axes_normalizer(figure_xy, ground_xy);
    scale_bb_figure = sfe_bounding_box_pts_normalizer(figure_xy);
    scale_figure_length = math2d_line_length(figure_xy);
  }
  if (scale_bb_figure == 0) {
    scale_bb_figure = sfe_bounding_box_pts_normalizer(ground_xy);
  }
  scale_bb_area = sfe_bounding_box_normalizer(figure_xy, ground_xy);

  //printf("scale:%f\n", scale_bb);
  
  for(size_t i=0; i<feat_vec->size; i++){
    int normalization_method = gsl_vector_get(mask, i);
    if (normalization_method == NORMALIZATION_NONE) {
      // do nothing
    } else if (normalization_method == NORMALIZATION_BBOX_ALL) {
      gsl_vector_set(ret_vec, i, gsl_vector_get(feat_vec, i)/scale_bb);
    } else if (normalization_method == NORMALIZATION_BBOX_FIGURE) {
      gsl_vector_set(ret_vec, i, gsl_vector_get(feat_vec, i)/scale_bb_figure);
    } else if (normalization_method == NORMALIZATION_FIGURE_LENGTH) {
      gsl_vector_set(ret_vec, i, gsl_vector_get(feat_vec, i)/scale_figure_length);
    } else if (normalization_method == NORMALIZATION_AXES) {
      gsl_vector_set(ret_vec, i, gsl_vector_get(feat_vec, i)/scale_axes);
    } else if (normalization_method == NORMALIZATION_BBOX_AREA) {
      gsl_vector_set(ret_vec, i, gsl_vector_get(feat_vec, i)/scale_bb_area);
    } else {
      printf("Unknown normalization method: %d\n", normalization_method);
      assert(0); 
    }
  }
  
  return ret_vec;
}

/* Get the observation feature names here */
vector<string> sfe_f_path_l_polygon_names()
{  
  vector<string> ret_names;
  
  vector<string> lmark_names = sfe_polygon_names();
  for(unsigned int k=0; k<lmark_names.size(); k++)
    ret_names.push_back(lmark_names[k]);

  vector<string> spath_names = sfe_path_names();
  for(unsigned int k=0; k<spath_names.size(); k++)
    ret_names.push_back(spath_names[k]);

  /*vector<string> olap_names = sfe_overlap_names();
  for(unsigned int k=0; k<olap_names.size(); k++)
  ret_names.push_back(olap_names[k]);*/
  
  vector<string> path_lmark_names = sfe_path_polygon_names();
  for(unsigned int k=0; k<path_lmark_names.size(); k++)
    ret_names.push_back(path_lmark_names[k]);
  
  return ret_names;
}




/* Get the observation feature values here */
gsl_vector* sfe_extract_unnormalized_f_path_l_polygon(gsl_matrix* fig1_xyth, 
                                                      gsl_matrix* gnd1_xy)
{
  vector<gsl_vector *> features;
  features.push_back(sfe_polygon_features(gnd1_xy));
  features.push_back(sfe_path_features(fig1_xyth));  
  features.push_back(sfe_path_polygon_features(fig1_xyth, 
                                               gnd1_xy));
  
  gsl_vector * result = sfe_merge_feature_vectors(features);
  sfe_free_features(features);
  return result; 
}


gsl_vector * sfe_merge_feature_vectors(vector<gsl_vector *> features)
{
  int vector_length = 0;
  for (size_t i = 0; i < features.size(); i++) {
    gsl_vector * vector = features[i];
    vector_length += vector->size;
  }
    
  gsl_vector* ret_vec = gsl_vector_calloc(vector_length);

  int ret_idx = 0;
  for (size_t i = 0; i < features.size(); i++) {
    gsl_vector * vector = features[i];
    gsl_vector * feature_view = &(gsl_vector_subvector(ret_vec, ret_idx, 
                                                       vector->size).vector);
    gsl_vector_memcpy(feature_view, vector);
    ret_idx += vector->size;
  }
  return ret_vec;
}


void sfe_free_features(vector<gsl_vector *> features) 
{
  for (size_t i = 0; i < features.size(); i++) {
    gsl_vector * vector = features[i];
    gsl_vector_free(vector);
  }
}

/* Get the observation feature names here */
vector<string> sfe_f_polygon_l_polygon_names()
{  
  vector<string> ret_names;

  for (size_t i = 0; i < distance_polygon_polygon_features_count; i++) {
    ret_names.push_back(distance_polygon_polygon_features_names[i]);
  }

  return ret_names;
}

gsl_vector* sfe_f_polygon_l_polygon(gsl_matrix* p1_xy,
                                    gsl_matrix* p2_xy,
                                    bool normalize)
{

  vector<gsl_vector *> features;
  features.push_back(spatial_features_distance_polygon_polygon(p1_xy,
                                                               p2_xy));


  //features.push_back(spatial_features_avs_polygon_polygon(p1_xy,
  //p2_xy));

  
  gsl_vector * result = sfe_merge_feature_vectors(features);
  sfe_free_features(features);

  if (normalize) {
    vector<string> all_names = sfe_f_polygon_l_polygon_names();
    gsl_vector* mask = sfe_get_normalization_mask(all_names);
    gsl_vector * normalized_result = sfe_normalize_feature_vector(p1_xy, p2_xy, mask, result);
    
    gsl_vector_free(mask);
    gsl_vector_free(result);
    return normalized_result;
  } 
  else {
    return result; 
  }
}


gsl_vector* sfe_extract_f_path_l_polygon(gsl_matrix* fig1_xyth, 
					 gsl_matrix* gnd1_xy, 
					 bool normalize)
{
  gsl_vector* feats;
  gsl_vector* feats_tmp = sfe_extract_unnormalized_f_path_l_polygon(fig1_xyth, gnd1_xy);
  
  if (normalize) {
    vector<string> all_names = sfe_f_path_l_polygon_names();
    gsl_vector* mask = sfe_get_normalization_mask(all_names);
    gsl_matrix_view fig1_xy = gsl_matrix_submatrix(fig1_xyth, 0, 0, 2, fig1_xyth->size2);
    
    feats = sfe_normalize_feature_vector(&fig1_xy.matrix, gnd1_xy, 
                                                               mask, feats_tmp);
    gsl_vector_free(feats_tmp);
    gsl_vector_free(mask);
  }  else {
    feats=feats_tmp;
  }
  return feats;
}


/****************************************************************/
/*  Below are a list of individual feature extractors */


/*  Get the names of the landmark features */
vector<string> sfe_polygon_names(){  
  vector<string> ret_names;
  for (size_t i = 0; i < polygon_features_count; i++) {
    ret_names.push_back(polygon_features_names[i]);
  }
  
  return ret_names;
}

//features: ["lmark_area", "lmark_perimeter"]
//these still need to be scaled
gsl_vector* sfe_polygon_features(gsl_matrix* landmark){
  gsl_vector* ret_vals = gsl_vector_alloc(polygon_features_count);

  if(landmark == NULL){
    gsl_vector_add_constant(ret_vals, GSL_NAN);
    return ret_vals;
  }
    
  gsl_vector_set(ret_vals, F_landmarkArea, math2d_area(landmark));
  gsl_vector_set(ret_vals, F_landmarkPerimeter, math2d_perimeter(landmark));
  
  return ret_vals;
}


/*  Get the names of the spath features */
vector<string> sfe_path_names(){  
  vector<string> ret_names;
  
  for (int i = 0; i < path_features_count; i++) {
    ret_names.push_back(path_features_names[i]);
  }
  return ret_names;
}


//features: "edist_sp", "int_path_sp", "orient_st_end_sp", "orient_dir_spath_str", 
//    "orient_dir_spath_left", "orient_dir_spath_right"
//these still need to be scaled

gsl_vector* sfe_path_features(gsl_matrix* path_xyth){
  gsl_vector* ret_vals = gsl_vector_alloc(path_features_count);

  if(path_xyth == NULL){
    gsl_vector_add_constant(ret_vals, GSL_NAN);
    return ret_vals;
  }
  gsl_matrix_view path_xy = gsl_matrix_submatrix(path_xyth, 0, 0, 2, path_xyth->size2);

  gsl_vector_view path_st = gsl_matrix_subcolumn(path_xyth, 0, 0, 2);
  gsl_vector_view path_end = gsl_matrix_subcolumn(path_xyth, path_xyth->size2-1, 0, 2);
  double path_length  = math2d_line_length(&path_xy.matrix);

  //gsl_vector_set(ret_vals, F_pathLength, path_length);
  
  gsl_vector_set(ret_vals, F_ratioDistStartEndByPathLength,
                 math2d_dist(&path_st.vector, &path_end.vector) / path_length);


  /* get the orientation feature */
  double th_st = gsl_matrix_get(path_xyth, 2, 0);
  double th_end = gsl_matrix_get(path_xyth, 2, path_xyth->size2-1);
  gsl_vector_set(ret_vals, F_orientStEndSp, tklib_normalize_theta(th_end-th_st));

  /* get the percentage of orientations that go straight*/
  gsl_vector_view p1_st = gsl_matrix_column(path_xyth, 0);
  double v = spatial_features_orientation_direction_between(&p1_st.vector, path_xyth, -M_PI/4.0, M_PI/4.0);
  gsl_vector_set(ret_vals, F_orientDirSpathStraight, v);

  /*behind*/
  v = spatial_features_orientation_direction_between(&p1_st.vector, path_xyth, M_PI, 3*M_PI/4.0);
  v += spatial_features_orientation_direction_between(&p1_st.vector, path_xyth, -M_PI, -3*M_PI/4.0);
  gsl_vector_set(ret_vals, F_orientDirSpathBehind, v);
  
  /*  right */
  v = spatial_features_orientation_direction_between(&p1_st.vector, path_xyth, -3*M_PI/4.0, -M_PI/4.0);
  gsl_vector_set(ret_vals, F_orientDirSpathRight, v);

  /*  left */
  v = spatial_features_orientation_direction_between(&p1_st.vector, path_xyth, M_PI/4.0, 3*M_PI/4.0);
  gsl_vector_set(ret_vals, F_orientDirSpathLeft, v);
  
  return ret_vals;
}

vector<string> sfe_overlap_names(){  
  vector<string> ret_names;
  ret_names.push_back("overlap_end_st");
  ret_names.push_back("overlap_st_end");
  return ret_names;
}

//features: ["overlap_end_st", "overlap_st_end"]
gsl_vector* sfe_overlap_features(double t1_st, double t1_end, double t2_st, double t2_end){
  gsl_vector* ret_vals = gsl_vector_alloc(2);
  
  //double spatial_features_overlap_feature(double t1_st, double t1_end, 
  //double t2_st, double t2_end){  
  gsl_vector_set(ret_vals, 0, spatial_features_overlap_feature(t1_st, t1_end, t2_st, t2_end));
  gsl_vector_set(ret_vals, 1, spatial_features_overlap_feature(t2_st, t2_end, t1_st, t1_end));
    
  return ret_vals;
}



vector<string> sfe_path_path_names(){  
  vector<string> ret_names;

  ret_names.push_back("edist_end_st_pp");
  ret_names.push_back("edist_end_end_pp");
  ret_names.push_back("edist_st_st_pp");
  ret_names.push_back("edist_st_end_pp");
  ret_names.push_back("edist_mean_pp");
  ret_names.push_back("orient_st_end_pp");
  ret_names.push_back("orient_end_end_pp");
  ret_names.push_back("orient_st_st_pp");
  ret_names.push_back("orient_end_st_pp");
  ret_names.push_back("orient_dir_st_pp_45deg");
  ret_names.push_back("orient_dir_end_pp_45deg");
  ret_names.push_back("orient_dir_st_pp_90deg");
  ret_names.push_back("orient_dir_end_pp90deg");
  ret_names.push_back("orient_dir_st_pp_45deg_right");
  ret_names.push_back("orient_dir_end_pp_45deg_right");
  ret_names.push_back("orient_dir_st_pp_45deg_left");
  ret_names.push_back("orient_dir_end_pp_45deg_left");
  
  return ret_names;
}

// features: "edist_end_st_pp", "edist_end_end_pp", "edist_st_st_pp", "edist_st_end_pp", "edist_mean_pp"
//"orient_st_end_pp", "orient_end_end_pp", "orient_st_st_pp", "orient_end_st_pp", 
//"orient_dir_st_pp_45deg", "orient_dir_end_pp_45deg", "orient_dir_st_pp_90deg", "orient_dir_end_pp90deg", 
//"orient_dir_st_pp_45deg_right", "orient_dir_end_pp_45deg_right", "orient_dir_st_pp_45deg_left", "orient_dir_end_pp_45deg_left"

//these still need to be scaled
gsl_vector* sfe_extract_path_path(gsl_matrix* p1_xyth, gsl_matrix* p2_xyth){
  gsl_vector* ret_vals = gsl_vector_alloc(17);

  if(p1_xyth == NULL || p2_xyth == NULL){
    gsl_vector_add_constant(ret_vals, GSL_NAN);
    return ret_vals;
  }
  
  gsl_vector_view p1_st = gsl_matrix_subcolumn(p1_xyth, 0, 0, 2);
  gsl_vector_view p1_end = gsl_matrix_subcolumn(p1_xyth, p1_xyth->size2-1, 0, 2);

  gsl_vector_view p2_st = gsl_matrix_subcolumn(p2_xyth, 0, 0, 2);
  gsl_vector_view p2_end = gsl_matrix_subcolumn(p2_xyth, p2_xyth->size2-1, 0, 2);
  
  /* Get the first distances between the two paths */
  gsl_vector_set(ret_vals, 0, math2d_dist(&p1_end.vector, &p2_st.vector));
  gsl_vector_set(ret_vals, 1, math2d_dist(&p1_end.vector, &p2_end.vector)); 
  gsl_vector_set(ret_vals, 2, math2d_dist(&p1_st.vector, &p2_st.vector));
  gsl_vector_set(ret_vals, 3, math2d_dist(&p1_st.vector, &p2_end.vector));
  

  /* Get the mean distances between the two paths */
  gsl_matrix_view p1_xy = gsl_matrix_submatrix(p1_xyth, 0, 0, 2, p1_xyth->size2);
  gsl_vector* p1_mean = tklib_mean(&p1_xy.matrix, 0);

  gsl_matrix_view p2_xy = gsl_matrix_submatrix(p2_xyth, 0, 0, 2, p2_xyth->size2);
  gsl_vector* p2_mean = tklib_mean(&p2_xy.matrix, 0);
  
  gsl_vector_set(ret_vals, 4, math2d_dist(p1_mean, p2_mean));

  /* Get orientation features */
  double p1_th_st = gsl_matrix_get(p1_xyth, 2, 0);
  double p1_th_end =gsl_matrix_get(p1_xyth, 2, p1_xyth->size2-1);
  double p2_th_st =  gsl_matrix_get(p2_xyth, 2, 0);
  double p2_th_end = gsl_matrix_get(p2_xyth, 2, p2_xyth->size2-1);
  
  gsl_vector_set(ret_vals, 5, tklib_normalize_theta(p2_th_end - p1_th_st));
  gsl_vector_set(ret_vals, 6, tklib_normalize_theta(p2_th_end - p1_th_end));
  gsl_vector_set(ret_vals, 7, tklib_normalize_theta(p2_th_st - p1_th_st));
  gsl_vector_set(ret_vals, 8, tklib_normalize_theta(p2_th_st - p1_th_end));
  
  p1_st = gsl_matrix_column(p1_xyth, 0);
  p1_end = gsl_matrix_column(p1_xyth, p1_xyth->size2-1);

  /*compute if the orientation is roughly straight ahead*/
  double v = spatial_features_orientation_direction_between(&p1_st.vector, p2_xyth, -M_PI/4.0, M_PI/4.0);
  gsl_vector_set(ret_vals, 9, v);
  v = spatial_features_orientation_direction_between(&p1_end.vector, p2_xyth, -M_PI/4.0, M_PI/4.0);
  gsl_vector_set(ret_vals, 10, v);

  /*compute if the orientation is roughly straight ahead*/
  v = spatial_features_orientation_direction_between(&p1_st.vector, p2_xyth, -M_PI/2.0, M_PI/2.0);
  gsl_vector_set(ret_vals, 11, v);
  v = spatial_features_orientation_direction_between(&p1_end.vector, p2_xyth, -M_PI/2.0, M_PI/2.0);
  gsl_vector_set(ret_vals, 12, v);
  
  /*compute if the orientation is roughly to the right*/
  v = spatial_features_orientation_direction_between(&p1_st.vector, p2_xyth, -3*M_PI/4.0, -M_PI/4.0);
  gsl_vector_set(ret_vals, 13, v);
  v = spatial_features_orientation_direction_between(&p1_end.vector, p2_xyth, -3*M_PI/4.0, -M_PI/4.0);
  gsl_vector_set(ret_vals, 14, v);

  /*compute if the orientation is roughly to the left*/
  v = spatial_features_orientation_direction_between(&p1_st.vector, p2_xyth, M_PI/4.0, 3*M_PI/4.0);
  gsl_vector_set(ret_vals, 15, v);
  v = spatial_features_orientation_direction_between(&p1_end.vector, p2_xyth, M_PI/4.0, 3*M_PI/4.0);
  gsl_vector_set(ret_vals, 16, v);

  /* Free the generated memory */
  gsl_vector_free(p1_mean);
  gsl_vector_free(p2_mean);
  return ret_vals;
}

vector<string> sfe_path_polygon_names()
{  
  vector<string> ret_names;

  for (int i = 0; i < angle_features_count; i++) {
    ret_names.push_back(angle_features_names[i]);
  }

  for (int i = 0; i < distance_path_to_landmark_features_count; i++) {
    ret_names.push_back(distance_path_to_landmark_features_names[i]);
  }

  for (int i = 0; i < axes_features_count; i++) {
    ret_names.push_back(axes_features_names[i]);
  }


  for (int i = 0; i < boundary_features_count; i++) {
    ret_names.push_back(boundary_features_names[i]);
  }

  for (int i = 0; i < bounding_box_features_count; i++) {
    ret_names.push_back(bounding_box_features_names[i]);
  }

  for (int i = 0; i < past_axes_features_count; i++) {
    ret_names.push_back(past_axes_features_names[i]);
  }


  
  return ret_names;
}
//features: ["front_st", "right_st", "left_st", "behind_st", 
//    "front_end", "right_end", "left_end", "behind_end", "displacementFromLandmark", 
//    "distFigureStartToLandmarkCentroid", "distFigureCOMToLandmarkCentroid", "distFigureEndToLandmarkCentroid",
//    "distFigureStartToLandmark", "distFigureEndToLandmark", 'averageDistStartEndLandmark', "distFigureCOMToLandmark", 
//    "centroidToAxesOrigin", "figureCenterOfMassToAxesOrigin", "figureCenterOfMassToLandmarkCentroid",
//    "axesStartToLandmark", "axesEndToLandmark", "axesToLandmarkSum",
//    "axesStartToFigureStart", "axesEndToFigureEnd", "axesToFigureSum", 
//    "ratioFigureToAxes", "ratioLengthFigureToAxes"]
gsl_vector* sfe_path_polygon_features(gsl_matrix* path_xyth, 
                                       gsl_matrix* landmark_xy){
  
  gsl_matrix_view path_xy; gsl_vector* distance_feats; gsl_vector* axes_feats;
  gsl_vector* boundary_feats;
  gsl_vector* bounding_box_feats;
  gsl_vector* past_axes_feats;

  if(path_xyth != NULL && landmark_xy != NULL){
    path_xy = gsl_matrix_submatrix(path_xyth, 0, 0, 2, path_xyth->size2);
    
    /* features from stefanie... don't need theta */ 
    distance_feats = spatial_features_distance_path_to_landmark(&path_xy.matrix, landmark_xy);
    axes_feats = spatial_features_axes(&path_xy.matrix, landmark_xy);
    boundary_feats = spatial_features_boundary(&path_xy.matrix, landmark_xy);
    bounding_box_feats = spatial_features_bounding_box(&path_xy.matrix, landmark_xy);
    past_axes_feats = spatial_features_past_axes(&path_xy.matrix, landmark_xy);
  }
  else{
    distance_feats = spatial_features_distance_path_to_landmark(NULL, NULL);
    axes_feats = spatial_features_axes(NULL, NULL);
    boundary_feats = spatial_features_boundary(NULL, NULL);
    bounding_box_feats = spatial_features_bounding_box(NULL, NULL);
    past_axes_feats = spatial_features_past_axes(NULL, NULL);
  }


  //printf("alloc\n");
  gsl_vector* ret_vals = gsl_vector_calloc(angle_features_count +
                                           distance_feats->size + 
                                           axes_feats->size + 
                                           boundary_feats->size +
                                           bounding_box_feats->size + 
                                           past_axes_feats->size
                                           );
  
  if(path_xyth == NULL || landmark_xy == NULL){
    gsl_vector_add_constant(ret_vals, GSL_NAN);
    gsl_vector_free(axes_feats);
    gsl_vector_free(distance_feats);
    gsl_vector_free(boundary_feats);
    gsl_vector_free(bounding_box_feats);
    gsl_vector_free(past_axes_feats);
    return ret_vals;
  }

  /***************************************/
  /*  Compute additional features        */
  
  /* get the start location of the path */
  gsl_vector_view p_st = gsl_matrix_column(path_xyth,0);
  gsl_vector_view p_st_xy = gsl_vector_subvector(&p_st.vector, 0, 2);
  double p_stx = gsl_vector_get(&p_st.vector, 0);   
  double p_sty = gsl_vector_get(&p_st.vector, 1); 
  double p_stth = gsl_vector_get(&p_st.vector, 2); 

  /* get the end location in the path */
  gsl_vector_view p_end = gsl_matrix_column(path_xyth,path_xyth->size2-1);
  gsl_vector_view p_end_xy = gsl_vector_subvector(&p_end.vector, 0, 2);
  double p_endx = gsl_vector_get(&p_end.vector, 0);   
  double p_endy = gsl_vector_get(&p_end.vector, 1); 
  double p_endth = gsl_vector_get(&p_end.vector, 2); 

  /* get the center of mass (com) of the landmark */
  gsl_vector* com = math2d_centroid(landmark_xy); 
  double comx = gsl_vector_get(com, 0);   
  double comy = gsl_vector_get(com, 1);
  

  /* get the relative angle of the landmark to the start and end
     locations of the robot */
  double theta_st = tklib_normalize_theta(p_stth-atan2(comy-p_sty, comx-p_stx));
  double theta_end = tklib_normalize_theta(p_endth-atan2(comy-p_endy, comx-p_endx));

  
  /*  compute the relative orientation for the start point on the path */
  gsl_vector_set(ret_vals, F_front_st, 
                 spatial_features_theta_between(theta_st, -M_PI/2.0,  M_PI/2.0));
  gsl_vector_set(ret_vals, F_right_st, 
                 spatial_features_theta_between(theta_st, 0, M_PI));
  gsl_vector_set(ret_vals, F_left_st, 
                 spatial_features_theta_between(theta_st, -M_PI, 0));
  gsl_vector_set(ret_vals, F_behind_st, 
                 GSL_MAX(spatial_features_theta_between(theta_st, -M_PI, -M_PI/2.0),
				      spatial_features_theta_between(theta_st, M_PI/2.0, M_PI)));


  //printf("mid mid pl\n");
  /*  compute the relative orientation for the end point on the path */
  gsl_vector_set(ret_vals, F_front_end, 
                 spatial_features_theta_between(theta_end, -M_PI/2.0,  M_PI/2.0));
  gsl_vector_set(ret_vals, F_right_end, 
                 spatial_features_theta_between(theta_end, 0, M_PI));
  gsl_vector_set(ret_vals, F_left_end, 
                 spatial_features_theta_between(theta_end, -M_PI, 0));
  gsl_vector_set(ret_vals, F_behind_end, 
                 GSL_MAX(spatial_features_theta_between(theta_end, -M_PI, -M_PI/2.0),
                         spatial_features_theta_between(theta_end, M_PI/2.0, M_PI)));


  gsl_vector_set(ret_vals, F_displacementFromLandmark,  
                 spatial_features_displacement_feature(&path_xy.matrix, landmark_xy));



  /* copy the distance features */
  gsl_vector_view dist_view = gsl_vector_subvector(ret_vals, 
                                                   angle_features_count, 
                                                   distance_feats->size);
  gsl_vector_memcpy(&dist_view.vector, distance_feats);

    /* copy the axes features */
  gsl_vector_view axes_view = gsl_vector_subvector(ret_vals, 
                                                   angle_features_count +
						   distance_feats->size, 
						   axes_feats->size);
  gsl_vector_memcpy(&axes_view.vector, axes_feats);

  /* copy the boundary features */
  gsl_vector_view boundary_view = gsl_vector_subvector(ret_vals, 
                                                       angle_features_count +
                                                       distance_feats->size +
                                                       axes_feats->size,
                                                       boundary_feats->size);
  gsl_vector_memcpy(&boundary_view.vector, boundary_feats);


  /* copy the bounding box features */
  gsl_vector_view bounding_box_view = gsl_vector_subvector(ret_vals, 
                                                           angle_features_count +
                                                           distance_feats->size +
                                                           axes_feats->size + 
                                                           boundary_feats->size,
                                                           bounding_box_feats->size);
  gsl_vector_memcpy(&bounding_box_view.vector, bounding_box_feats);

  /* copy the past axes features */
  gsl_vector_view past_axes_view = gsl_vector_subvector(ret_vals, 
                                                        angle_features_count +
                                                        distance_feats->size +
                                                        axes_feats->size + 
                                                        boundary_feats->size + 
                                                        bounding_box_feats->size,
                                                        past_axes_feats->size
                                                        );
  gsl_vector_memcpy(&past_axes_view.vector, past_axes_feats);


  gsl_vector_free(past_axes_feats);
  gsl_vector_free(bounding_box_feats);
  gsl_vector_free(distance_feats);
  gsl_vector_free(axes_feats);
  gsl_vector_free(boundary_feats);
  gsl_vector_free(com);
  return ret_vals;
}
vector<string> sfe_f_prism_l_prism_names()
{  
  vector<string> names;
  vector<string> polygon_names = sfe_f_polygon_l_polygon_names();
  for (size_t i = 0; i < polygon_names.size(); i++) {
    names.push_back(polygon_names[i]);
  }

  for (int i = 0; i < prism_features_count; i++) {
    names.push_back(prism_features_names[i]);
  }
  return names;
}

gsl_vector* sfe_f_prism_l_prism(math3d_prism_t p1, math3d_prism_t p2, bool normalize)
{
  vector<gsl_vector *> features;
  features.push_back(sfe_f_polygon_l_polygon(p1.points_xy, p2.points_xy, normalize));
  features.push_back(spatial_features_prism_prism(p1, p2));

  gsl_vector * result = sfe_merge_feature_vectors(features);
  sfe_free_features(features);    
  
  return result;
}

vector<string> sfe_f_polygon_l_polygon_l_polygon_names()
{
  vector<string> names;

  for (int i = 0; i < between_features_count; i++) {
    names.push_back(between_features_names[i]);
  }
  return names;  
}

gsl_vector* sfe_f_polygon_l_polygon_l_polygon(gsl_matrix* f_xy,
                                              gsl_matrix* l1_xy,
                                              gsl_matrix* l2_xy)
{
  vector<gsl_vector *> features;
  features.push_back(spatial_features_three_polygons(f_xy, l1_xy, l2_xy));
  gsl_vector * result = sfe_merge_feature_vectors(features);
  sfe_free_features(features);  
  return result;  
}






gsl_vector* flu_polygon(vector<string> figure, 
                        gsl_matrix* gnd1_xy, 
                        bool perform_scaling){
  if(figure.size() == 0)
    return NULL;
  
  /* compute the low-level features for each component*/
  gsl_vector* feats_fig;  
  gsl_vector* feats_fig_tmp = sfe_polygon_features(gnd1_xy);
  
  if(perform_scaling){

    vector<string> names_fig = sfe_polygon_names();
    gsl_vector* mask_fig = sfe_get_normalization_mask(names_fig);

    assert(mask_fig->size == feats_fig_tmp->size);
    feats_fig = sfe_normalize_feature_vector(NULL, gnd1_xy, mask_fig, feats_fig_tmp);

    gsl_vector_free(feats_fig_tmp);
    gsl_vector_free(mask_fig);
  }
  else{
    feats_fig=feats_fig_tmp;
  }
  int num_features = feats_fig->size*figure.size();
  gsl_vector* ret_vec = gsl_vector_calloc(num_features);
  
  size_t i;
  for(i=0; i<figure.size(); i++){
    gsl_vector_memcpy(&gsl_vector_subvector(ret_vec, feats_fig->size*i, feats_fig->size).vector, feats_fig);
  }
  
  gsl_vector_free(feats_fig);
  
  return ret_vec;
}

vector<string> flu_polygon_names(vector<string> figure)
{
  /* cross the words with the feature names */
  vector<string> names_fig = sfe_polygon_names();
  vector<string> f_names = crf_get_word_features(figure, names_fig, "f_");
  
  /* create the return feature names */
  vector<string> ret_names;
  
  for(unsigned int k=0; k<f_names.size(); k++)
    ret_names.push_back(f_names[k]);

  return ret_names;
}

