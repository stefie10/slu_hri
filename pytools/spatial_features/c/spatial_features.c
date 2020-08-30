#include "spatial_features.h"
#include "avs.h"
/*************************************************************/
/*                  Get the features here                    */
/*************************************************************/

double spatial_features_theta_between(double theta, double theta_st, double theta_end){
  if(theta >= theta_st and theta <= theta_end)
    return 1;
  else
    return 0;
}



//this determines how many values are within the window defined by st_ang and end_ang
//  relative to the original pose theta
double spatial_features_orientation_direction_between(gsl_vector* pose, gsl_matrix* path, 
						      double st_ang, double end_ang){
  double theta = gsl_vector_get(pose, 2);
  
  gsl_vector* path_theta = gsl_vector_alloc(path->size2);
  gsl_matrix_get_row(path_theta, path, 2);

  gsl_vector_add_constant(path_theta, -1.0*theta);
  
  gsl_vector* th_normalized = tklib_normalize_theta_array(path_theta);
  
  //determine if the value is in between end_ang and st_ang
  gsl_vector* thleq = tklib_vector_leq(th_normalized, end_ang);
  gsl_vector* thgeq = tklib_vector_geq(th_normalized, st_ang);
  gsl_vector* thint = gsl_vector_alloc(path->size2);
  tklib_vector_intersect(thleq, thgeq, thint);
  
  //get the count of the elements that are non-zero
  double count = tklib_vector_sum(thint);

  gsl_vector_free(path_theta);
  gsl_vector_free(th_normalized);
  gsl_vector_free(thleq);
  gsl_vector_free(thgeq);
  gsl_vector_free(thint);
  
  return count/(1.0*path->size2);
}

//paths are assumed to have two rows one for x and another for  y
gsl_vector* spatial_features_distance_path_to_landmark(gsl_matrix* figure_xy, gsl_matrix* landmark_xy){
  gsl_vector* ret_vec = gsl_vector_alloc(distance_path_to_landmark_features_count);
  if(figure_xy == NULL || landmark_xy == NULL){
    gsl_vector_add_constant(ret_vec, GSL_NAN);
    return ret_vec;
  }
  
  //out["distFigureStartToLandmarkCentroid"] = distanceFeature(l_centroid, figure[0], scale);
  ///out["distFigureStartToLandmark"] = distanceFeature(math2d.closestPointOnPolygon(landmark, figure[0]), 
  //figure[0], scale);
  gsl_vector_view f_xy_st =  gsl_matrix_column(figure_xy, 0);
  gsl_vector* f_xy_mean =  tklib_mean(figure_xy, 0);
  gsl_vector_view f_xy_end =  gsl_matrix_column(figure_xy, figure_xy->size2-1);

  //tklib_mean(landmark_xy, 0);
  gsl_vector* l_xy_centroid = math2d_centroid(landmark_xy);

  gsl_vector_set(ret_vec, F_distFigureStartToLandmarkCentroid, 
                 math2d_dist(&f_xy_st.vector, l_xy_centroid));
  gsl_vector_set(ret_vec, F_distFigureCenterOfMassToLandmarkCentroid,
                 math2d_dist(f_xy_mean, l_xy_centroid));
  
  //distFigureEndToLandmarkCentroid
  gsl_vector_set(ret_vec, F_distFigureEndToLandmarkCentroid, 
                 math2d_dist(&f_xy_end.vector, l_xy_centroid));
  
  
  {
  /* get the distance to the closest point to the first point on the figure */

    if(math2d_is_interior_point(&f_xy_st.vector, landmark_xy)) {
      gsl_vector_set(ret_vec, F_distFigureStartToLandmark, 0.0);
    } else {
      gsl_vector* cpt = math2d_closest_point_on_polygon(landmark_xy, &f_xy_st.vector);
      gsl_vector_set(ret_vec, F_distFigureStartToLandmark, 
                     math2d_dist(cpt, &f_xy_st.vector));    
      gsl_vector_free(cpt);
    }

  }

  /* get the distance to the closest point on the landmark to the last point on the figure */
  //distFigureEndToLandmark
  {

    if(math2d_is_interior_point(&f_xy_end.vector, landmark_xy)){
      gsl_vector_set(ret_vec, F_distFigureEndToLandmark, 0.0);
    }
    else {
      gsl_vector* cpt = math2d_closest_point_on_polygon(landmark_xy, &f_xy_end.vector);
      gsl_vector_set(ret_vec, F_distFigureEndToLandmark, 
                     math2d_dist(cpt, &f_xy_end.vector));
      gsl_vector_free(cpt);
    }

  }
  
  {
    /* get the distance to the closest point on the landmark to the mean point on the figure */
    gsl_vector* cpt = math2d_closest_point_on_polygon(landmark_xy, f_xy_mean);
    gsl_vector_set(ret_vec, F_distFigureCenterOfMassToLandmark, 
                   math2d_dist(cpt, f_xy_mean));
    gsl_vector_free(cpt);
  }
  
  gsl_vector_free(f_xy_mean);
  gsl_vector_free(l_xy_centroid);

  return ret_vec;
}


gsl_vector* spatial_features_boundary(gsl_matrix* f_xy, gsl_matrix* l_xy)
{
    gsl_vector* ret_vec = gsl_vector_alloc(boundary_features_count);
    gsl_vector_add_constant(ret_vec, GSL_NAN);
    
    if (f_xy == NULL || l_xy == NULL) {
      return ret_vec;
    }
    gsl_vector_view f_start_xy = gsl_matrix_column(f_xy, 0);
    gsl_vector_view f_end_xy = gsl_matrix_column(f_xy, f_xy->size2 - 1);
    gsl_matrix * boundary_line = math2d_compute_boundary_line(l_xy, f_xy);
    gsl_vector * b_st = &gsl_matrix_column(boundary_line, 0).vector;
    gsl_vector * b_end = &gsl_matrix_column(boundary_line, 
					   boundary_line->size2 - 1).vector;
    gsl_vector * closest_b_to_f_start = 
      math2d_closest_point_on_line(boundary_line, &f_start_xy.vector);

    gsl_vector * closest_b_to_f_end = 
      math2d_closest_point_on_line(boundary_line, &f_end_xy.vector);

    double dist_to_start = math2d_dist(closest_b_to_f_start, 
                                       &f_start_xy.vector);

    double dist_to_end = math2d_dist(closest_b_to_f_end, 
                                     &f_end_xy.vector);

    gsl_vector_set(ret_vec, F_distStartLandmarkBoundary, dist_to_start);
    gsl_vector_set(ret_vec, F_distEndLandmarkBoundary, dist_to_end);

    gsl_vector_set(ret_vec, F_averageDistStartEndLandmarkBoundary, 
                   (dist_to_start + dist_to_end)/2.0);

    gsl_vector_set(ret_vec, F_figureStartToEnd, 
                   math2d_dist(&f_start_xy.vector, &f_end_xy.vector));


    gsl_matrix * trimmed_f = math2d_trim_line(f_xy, b_st, b_end);

    double figure_length = math2d_line_length(trimmed_f);
    gsl_matrix * f_points = 
      math2d_step_along_line(trimmed_f, figure_length / 100.0);
    

    gsl_vector * all_distances = gsl_vector_alloc(f_points->size2);
    for (size_t i = 0; i < f_points->size2; i++) {
      gsl_vector *  f_p = & gsl_matrix_column(f_points, i).vector;
      gsl_vector * closest_point = math2d_closest_point_on_line(boundary_line, 
								f_p);
      gsl_vector_set(all_distances, i, math2d_dist(closest_point, f_p));
      gsl_vector_free(closest_point);
    }
    struct math2d_range window = math2d_smallest_window(all_distances, 
							(int) (all_distances->size * 0.75));

    if(window.end_i - window.start_i == window.start_i){
      return ret_vec;
    }
    
    gsl_vector * distances = &gsl_vector_subvector(all_distances, 
						   window.start_i,
						   window.end_i - window.start_i).vector;

    int max_dist_idx = tklib_vector_argmax(distances);
    double peak_dist = gsl_vector_get(distances, max_dist_idx);
    gsl_vector_set(ret_vec, F_peakDistToAxes, peak_dist);
    
    gsl_vector * bbox = math2d_bbox(trimmed_f);
    double scale = math2d_get_scale(bbox);
    if (scale == 0) {
      gsl_vector * lbbox = math2d_bbox(l_xy);
      scale = math2d_get_scale(lbbox);
      gsl_vector_free(lbbox);
    }
    if (scale == 0) {
      scale == 1.0;
    }

    gsl_vector_scale(distances, 1.0/scale);
    gsl_vector_set(ret_vec, F_stdDevToAxes, tklib_vector_stddev(distances));

    gsl_vector_set(ret_vec, F_averageDistToAxes, tklib_vector_mean(distances));
    

    {
      gsl_vector * origin = math2d_point(0, 0);
      struct fit_line_result f_line_result = math2d_fit_line(f_xy);
      struct fit_line_result l_line_result = math2d_fit_line(l_xy);
      gsl_vector * fpoint = math2d_point(0, 0);
      gsl_vector * lpoint = math2d_point(0, 0);
      if (isnan(f_line_result.slope)) {
        math2d_set_point(fpoint, 0, 1);
      } else {
        math2d_set_point(fpoint, 1, f_line_result.slope);
      }
      if (isnan(l_line_result.slope)) {
        math2d_set_point(lpoint, 0, 1);
      } else {
        math2d_set_point(lpoint, 1, l_line_result.slope);
      }

      gsl_vector_set(ret_vec, F_angleBtwnLinearizedObjects, 
                     math2d_angle_between_segments(origin, fpoint,
                                                   origin, lpoint));
      gsl_vector_free(fpoint);
      gsl_vector_free(lpoint);
      gsl_vector_free(origin);
    }
      
    
    gsl_matrix_free(trimmed_f);
    gsl_vector_free(closest_b_to_f_start);
    gsl_vector_free(closest_b_to_f_end);
    gsl_vector_free(bbox);
    gsl_matrix_free(boundary_line);
    gsl_matrix_free(f_points);
    gsl_vector_free(all_distances);
    return ret_vec;
}

gsl_vector* spatial_features_bounding_box(gsl_matrix* f_xy, gsl_matrix* l_xy)
{
    gsl_vector* ret_vec = gsl_vector_alloc(bounding_box_features_count);
    if (f_xy == NULL || l_xy == NULL) {
      gsl_vector_add_constant(ret_vec, GSL_NAN);
      return ret_vec;
    }

    double figure_length = math2d_line_length(f_xy);
    if(figure_length < 10e-3){
      gsl_vector_add_constant(ret_vec, GSL_NAN);
      return ret_vec;
    }
    
    gsl_vector_view f_start_xy = gsl_matrix_column(f_xy, 0);
    gsl_vector_view f_end_xy = gsl_matrix_column(f_xy, f_xy->size2 - 1);

    gsl_vector* l_bbox = math2d_bbox(l_xy);
    double scale = math2d_get_scale(l_bbox) * 0.1;
    // grow the box slightly.
    gsl_vector_set(l_bbox, 0, gsl_vector_get(l_bbox, 0) - scale);
    gsl_vector_set(l_bbox, 1, gsl_vector_get(l_bbox, 1) - scale);
    gsl_vector_set(l_bbox, 2, gsl_vector_get(l_bbox, 2) + scale);
    gsl_vector_set(l_bbox, 3, gsl_vector_get(l_bbox, 3) + scale);
    
    gsl_matrix * polygon = math2d_bbox_to_polygon(l_bbox);
    gsl_matrix * figure_steps = math2d_step_along_line(f_xy, 
						       figure_length / 100.0);
    
    int end_points_in_landmark_bb = 0;
    for (size_t i = 90; i < figure_steps->size2; i++) {
      gsl_vector_view p = gsl_matrix_column(figure_steps, i);
      if (math2d_is_interior_point(&p.vector, polygon)) {
        end_points_in_landmark_bb++;
      }
    }
    gsl_vector_set(ret_vec, F_endPointsInLandmarkBoundingBox, 
		   end_points_in_landmark_bb);

    int start_points_in_landmark_bb = 0;
    for (size_t i = 0; i < 10; i++) {
      gsl_vector_view p = gsl_matrix_column(figure_steps, i);
      if (math2d_is_interior_point(&p.vector, polygon)) {
        start_points_in_landmark_bb++;
      }
    }
    gsl_vector_set(ret_vec, F_startPointsInLandmarkBoundingBox, start_points_in_landmark_bb);


    gsl_matrix_free(figure_steps);
    gsl_matrix_free(polygon);
    gsl_vector_free(l_bbox);

    return ret_vec;
}


gsl_vector* spatial_features_past_axes(gsl_matrix* f_xy, gsl_matrix* l_xy)
{
  gsl_vector* ret_vec = gsl_vector_alloc(past_axes_features_count);
  if (f_xy == NULL || l_xy == NULL) {
    gsl_vector_add_constant(ret_vec, GSL_NAN);
    return ret_vec;
  }

  gsl_vector_view f_start_xy = gsl_matrix_column(f_xy, 0);
  gsl_vector_view f_end_xy = gsl_matrix_column(f_xy, f_xy->size2 - 1);

  double figure_length = math2d_line_length(f_xy);

  
  gsl_matrix * f_points = math2d_step_along_line(f_xy, figure_length / 100.0);


  gsl_vector * distances = gsl_vector_alloc(f_points->size2);
  for (size_t i = 0; i < f_points->size2; i++) {
    gsl_vector_view f_p = gsl_matrix_column(f_points, i);
    gsl_vector * closest_point = math2d_closest_point_on_polygon(l_xy, &f_p.vector);
    gsl_vector_set(distances, i, math2d_dist(closest_point, &f_p.vector));
    gsl_vector_free(closest_point);
  }
  
  int min_idx = tklib_vector_argmin(distances);
  
  gsl_vector * f_point = gsl_vector_alloc(2);
  gsl_vector_memcpy(f_point, &(gsl_matrix_column(f_points, min_idx).vector));
  
  gsl_vector * g_point = math2d_closest_point_on_polygon(l_xy, f_point);

  gsl_vector_set(ret_vec, F_angleFigureToPastAxes, 
                 math2d_angle_between_segments(f_point, g_point,
                                               &f_start_xy.vector, &f_end_xy.vector));

  gsl_vector_set(ret_vec, F_pastAxesLength, 
		 math2d_dist(f_point, g_point));

  
  
  gsl_vector_free(f_point);
  gsl_vector_free(g_point);
  gsl_matrix_free(f_points);
  gsl_vector_free(distances);

  return ret_vec;

}


double spatial_features_overlap_feature(double t1_st, double t1_end, 
					double t2_st, double t2_end){

  double f_val = 0.0;
  double t1_min = GSL_MIN(GSL_MAX(t1_st, t2_st), t1_end);
  double t1_max = GSL_MAX(GSL_MIN(t1_end, t2_end), t1_st);

  if(t1_end != t1_st)
    f_val = (t1_max-t1_min)/(1.0*t1_end-t1_st);
  else{
    if(t1_max == t1_end)
      f_val = 1.0;
    else
      f_val = 0.0;
  }

  return f_val;
}

//still needs to be scaled
double spatial_features_displacement_feature(gsl_matrix* figure_xy, gsl_matrix* landmark_xy){
  //gsl_vector* bbox = tklib_combined_bounding_box(figure, landmark);
  //gsl_matrix* combined_xy = tklib_combined_matrix(figure_xy, landmark_xy);
  //gsl_vector* bbox = tklib_bounding_box(combined_xy);  

  /* get the scale */
  //double scale = tklib_get_scale(bbox); 
  
  /* get the centroid of the landmark */
  gsl_vector* l_centroid = math2d_centroid(landmark_xy); 
  //tklib_mean(landmark_xy, 0); 

  /* get the start location and end location of the figure */
  gsl_vector_view xy_st = gsl_matrix_column(figure_xy, 0);
  gsl_vector_view xy_end = gsl_matrix_column(figure_xy, figure_xy->size2-1);
  
  /* get the relevant distances */
  double dFigureStartToLandmark = math2d_dist(l_centroid, &xy_st.vector);
  double dFigureEndToLandmark = math2d_dist(l_centroid, &xy_end.vector);

  gsl_vector_free(l_centroid);
  //gsl_vector_free(bbox);
  //gsl_matrix_free(combined_xy);
  //return (dFigureEndToLandmark - dFigureStartToLandmark)/scale;
  return (dFigureEndToLandmark - dFigureStartToLandmark);
}

//["centroidToAxesOrigin", "figureCenterOfMassToAxesOrigin", "figureCenterOfMassToLandmarkCentroid",
// axesStartToLandmark, "axesEndToLandmark", 'axesToLandmarkSum', 
// "axesStartToFigureStart", "axesEndToFigureEnd", 'axesToFigureSum', 
// 'ratioFigureToAxes', 'ratioLengthFigureToAxes']
//still needs to be scaled except for the last two elements
gsl_vector* spatial_features_axes(gsl_matrix* figure_xy, gsl_matrix* landmark_xy){
  gsl_vector* ret_vec = gsl_vector_calloc(axes_features_count);

  if(figure_xy == NULL || landmark_xy == NULL){
    gsl_vector_add_constant(ret_vec, GSL_NAN);
    return ret_vec;
  }

  struct axes axes = math2d_compute_axes(landmark_xy, figure_xy);

  if(axes.minor_st == NULL){
    gsl_vector_add_constant(ret_vec, GSL_NAN);
    return ret_vec;
  }


  gsl_vector* origin = math2d_intersect_segments(axes.minor_st, axes.minor_end, 
                                                 axes.major_st, axes.major_end, 
                                                 true);

  /* get the start and end location of the figure */
  gsl_vector_view fig_st = gsl_matrix_column(figure_xy, 0);
  gsl_vector_view fig_end = gsl_matrix_column(figure_xy, figure_xy->size2-1);

  double figure_length = math2d_line_length(figure_xy);
  gsl_matrix * f_points = math2d_step_along_line(figure_xy, figure_length / 100.0);


  double myd1 = (math2d_dist(axes.minor_st, &fig_st.vector)  + 
                 math2d_dist(axes.minor_end, &fig_end.vector));
  double myd2 = (math2d_dist(axes.minor_st, &fig_end.vector) + 
                 math2d_dist(axes.minor_end, &fig_st.vector));
  if (myd1 > myd2 && (fabs(myd1 - myd2) > 0.00000000001)) {
    fig_st = gsl_matrix_column(figure_xy, figure_xy->size2-1);
    fig_end = gsl_matrix_column(figure_xy, 0);
  }

  //#in terms of landmark-only
  /* this was originally sampled */
  //gsl_vector* f_com = tklib_mean(figure_xy, 0);
  gsl_vector* f_com = math2d_center_of_mass(f_points);
  gsl_vector* l_centroid = math2d_centroid(landmark_xy);


  if (origin == NULL) {
    gsl_vector_set(ret_vec, F_centroidToAxesOrigin, GSL_NAN);
    
    //figureCenterOfMassToAxesOrigin
    gsl_vector_set(ret_vec, F_figureCenterOfMassToAxesOrigin, GSL_NAN);
  } else {
    //#returned features that depend on both
    gsl_vector_set(ret_vec, F_centroidToAxesOrigin, 
		   math2d_dist(l_centroid, origin));
    //figureCenterOfMassToAxesOrigin
    gsl_vector_set(ret_vec, F_figureCenterOfMassToAxesOrigin, 
		   math2d_dist(f_com, origin));
    gsl_vector_free(origin);
  }
  
  
  gsl_vector_set(ret_vec, F_figureCenterOfMassToLandmarkCentroid, 
                 math2d_dist(f_com, l_centroid));
  
  gsl_matrix* gnd_comb_xy = math2d_combined_matrix(landmark_xy, &gsl_matrix_submatrix(landmark_xy, 0, 0, landmark_xy->size1, 1).matrix);
  gsl_vector* pt1 = math2d_closest_point_on_line(gnd_comb_xy, axes.minor_st);
  gsl_vector_set(ret_vec, F_axesStartToLandmark, 
                 math2d_dist(pt1, axes.minor_st));
  gsl_vector_free(pt1);

  gsl_vector* pt2 = math2d_closest_point_on_line(gnd_comb_xy, axes.minor_end);
  gsl_vector_set(ret_vec, F_axesEndToLandmark, 
                 math2d_dist(pt2, axes.minor_end));
  gsl_vector_free(pt2);
  gsl_matrix_free(gnd_comb_xy);

  //map['axesEndToLandmark'] + map['axesStartToLandmark'];
  gsl_vector_set(ret_vec, F_axesToLandmarkSum, 
                 gsl_vector_get(ret_vec, 3)+gsl_vector_get(ret_vec, 4));
  
  //axesStartToFigureStart
  gsl_vector_set(ret_vec, F_axesStartToFigureStart, 
                 math2d_dist(axes.minor_st, &fig_st.vector));

  gsl_vector_set(ret_vec, F_axesEndToFigureEnd, 
                 math2d_dist(axes.minor_end, &fig_end.vector));

  
  //  map['axesToFigureSum'] = map['axesEndToFigureEnd'] + map['axesStartToFigureStart'];
  gsl_vector_set(ret_vec, F_axesToFigureSum, 
                 gsl_vector_get(ret_vec, 6)+gsl_vector_get(ret_vec, 7));



  /* DOES NOT NEED TO BE SCALED */
  double minor_len = math2d_dist(axes.minor_st, axes.minor_end);  
  gsl_vector_set(ret_vec, F_ratioFigureToAxes, 
                 math2d_dist(&fig_st.vector, &fig_end.vector) / minor_len);
  gsl_vector_set(ret_vec, F_ratioLengthFigureToAxes, 
                 math2d_line_length(figure_xy) / minor_len);


  gsl_vector_set(ret_vec, F_distAlongLandmarkBtwnAxes,
                 math2d_dist_between_points_along_polygon(landmark_xy, 
                                                          axes.minor_st, axes.minor_end) / math2d_perimeter(landmark_xy));

  struct axes eigen_axes = math2d_eigen_axes(landmark_xy);
  double ratio = (math2d_dist(eigen_axes.minor_st, eigen_axes.minor_end) / 
                  math2d_dist(eigen_axes.major_st, eigen_axes.major_end));
  double one_over_ratio = 1.0/ratio;
  if (one_over_ratio > ratio) {
    ratio = one_over_ratio;
  }
  gsl_vector_set(ret_vec, F_eigenAxesRatio, ratio);

  gsl_vector_free(l_centroid);
  gsl_vector_free(f_com);
  gsl_matrix_free(f_points);

  math2d_axes_free(axes);
  math2d_axes_free(eigen_axes);

  return ret_vec;
}
  

gsl_vector* spatial_features_distance_polygon_polygon(gsl_matrix* figure_xy, 
                                                      gsl_matrix* landmark_xy)
{
  gsl_vector* ret_vec = gsl_vector_alloc(distance_polygon_polygon_features_count);
  
  gsl_vector * f_centroid = math2d_centroid(figure_xy);
  gsl_vector * l_centroid = math2d_centroid(landmark_xy);

  gsl_vector_set(ret_vec, F_distBtwnCentroids,
                 math2d_dist(f_centroid, l_centroid));
  gsl_vector_free(f_centroid);
  gsl_vector_free(l_centroid);
  return ret_vec;
} 

vector<string> spatial_features_names_avs_polygon_polygon()
{   
  char buffer[255];  
  vector<string> ret_names;
  for (size_t i = 0; i < AVS_DIRECTION_COUNT; i++) {
    for (size_t j = 0; j < avs_base_features_count; j++) {
      sprintf(buffer, "%s_%d_%d", avs_base_features_names[j],
              (int) avs_directions[i][0],
              (int) avs_directions[i][1]);
      ret_names.push_back(buffer);
    }
  }
  return ret_names;
}

gsl_vector * spatial_features_avs_polygon_polygon(gsl_matrix * figure,
                                                  gsl_matrix * landmark,
                                                  double direction_theta)
{
  gsl_vector* ret_vec = gsl_vector_alloc(avs_base_features_count * AVS_DIRECTION_COUNT);
  
  gsl_vector * figure_pt = math2d_centroid(figure);

  // parameters from the paper. 
  // Shouldn't matter too much, if the components are used as features.
  double highgain = 0.131;
  double lambda = 1.0;
  double slope = -1/M_PI; 
  double y_intercept = 1;
  double scale;
  {
    gsl_matrix * combined = math2d_combined_matrix(figure, landmark);
    gsl_vector * bbox = math2d_bbox(combined);
    scale = math2d_get_scale(bbox);
    gsl_vector_free(bbox);
    gsl_matrix_free(combined);
  }

  
  for (size_t i = 0; i < AVS_DIRECTION_COUNT; i++) {

    gsl_vector * rotate_direction = math2d_point(avs_directions[i][0],
                                                 avs_directions[i][1]);

    gsl_vector * direction = math2d_rotate(rotate_direction, direction_theta);
    
    struct avs_result r = avs_avs(landmark, figure_pt, direction, 
                                  highgain, lambda, slope, y_intercept);
    int start_i = AVS_DIRECTION_COUNT * i;
    
    gsl_vector_set(ret_vec, start_i + F_avsResult, r.result);
    gsl_vector_set(ret_vec, start_i + F_avsHeightExp, r.height_exp);
    gsl_vector_set(ret_vec, start_i + F_avsHeight, r.height / scale);
    gsl_vector_set(ret_vec, start_i + F_avsg, r.avsg);
    gsl_vector_free(direction);
    avs_free(r);
  }
  gsl_vector_free(figure_pt);
  return ret_vec;
}


gsl_vector * spatial_features_prism_prism(math3d_prism_t figure,
                                          math3d_prism_t landmark)
{
  gsl_vector* ret_vec = gsl_vector_alloc(prism_features_count);
  gsl_vector_set(ret_vec, F_3dEndsHigherThanFigureLandmark, 
                 math3d_higher_than(figure, landmark));

  gsl_vector_set(ret_vec, F_3dEndsHigherThanLandmarkFigure, 
                 math3d_higher_than(landmark, figure));


  gsl_vector_set(ret_vec, F_3dStartsHigherThanFigureLandmark, 
                 math3d_starts_higher_than(figure, landmark));

  gsl_vector_set(ret_vec, F_3dStartsHigherThanLandmarkFigure, 
                 math3d_starts_higher_than(landmark, figure));

  gsl_vector_set(ret_vec, F_3dSupportsFigureLandmark, 
                 math3d_supports(figure, landmark));

  gsl_vector_set(ret_vec, F_3dSupportsLandmarkFigure, 
                 math3d_supports(landmark, figure));

  gsl_vector_set(ret_vec, F_3dIntersectsFigureLandmark, 
                 math3d_intersect_prisms(figure, landmark));

  return ret_vec;
}

gsl_vector * spatial_features_three_polygons(gsl_matrix * figure,
                                             gsl_matrix * l1,
                                             gsl_matrix * l2)
{
  gsl_vector* ret_vec = gsl_vector_alloc(between_features_count);
  gsl_vector * fcentroid = math2d_centroid(figure);
  gsl_vector * centroid1 = math2d_centroid(l1);
  gsl_vector * centroid2 = math2d_centroid(l2);

  
  gsl_vector * axes_origin = math2d_midpoint_segment(centroid1, centroid2);
  gsl_vector_set(ret_vec, F_distFigureCentroidAxes, 
                 math2d_dist(fcentroid, axes_origin));

  gsl_vector_free(fcentroid);
  gsl_vector_free(centroid1);
  gsl_vector_free(centroid2);
  gsl_vector_free(axes_origin);
  return ret_vec;
}


static void sprintf_float(char * result, double value) 
{
  // copied from python format
  if (fabs(value) >= 1e50) {
    sprintf(result, "%.2g", value);    
  } else {
    sprintf(result, "%.2f", value);
  }
}


char * flu_binarize_feature_uniform(char * name, double value, double min_val, 
                                    double max_val, int num_units)
{

  char * str = (char *) calloc(255, sizeof(char));  

  int length = 0;
  if (isnan(value) || isnan(min_val) || isnan(max_val)) {
    length += sprintf(str + length, "%s", name);
    length += sprintf(str + length, "%s", "_nan");
    return str;
  }
  gsl_vector * discrete = NULL;
  if (isinf(min_val)) {
    discrete = tklib_vector_linspace(-100-0.1, max_val+0.1, num_units);
  } else if (isinf(max_val)) {
    discrete = tklib_vector_linspace(min_val-0.1, 100+0.1, num_units);
  } else {
    discrete = tklib_vector_linspace(min_val-0.1, max_val+0.1, num_units);
  }
  //printf("discrete\n");
  //math2d_vector_printf(discrete);
  unsigned int i = tklib_vector_bisect(discrete, value);

  //printf("i: %d\n", i);
  
  length += sprintf(str + length, "%s", name);

  //printf("size: %d\n", discrete->size);
  //printf("value: %.3f\n", value);

  char * tmp = (char *) calloc(sizeof(char), 255);
  if (i <= discrete->size - 1 && i > 0) {
    sprintf_float(tmp, gsl_vector_get(discrete, i - 1));
    length += sprintf(str + length, "_%s", tmp);
    sprintf_float(tmp, gsl_vector_get(discrete, i));
    length += sprintf(str + length, "_%s", tmp);
  } else if (i == 0) {
    sprintf_float(tmp, gsl_vector_get(discrete, 0));
    length += sprintf(str + length, "_lt_%s", tmp);
  } else if (i == discrete->size) {
    sprintf_float(tmp, gsl_vector_get(discrete, discrete->size - 1));
    length += sprintf(str + length, "_gt_%s", tmp);
  }
  gsl_vector_free(discrete);
  free(tmp);
  return str;
}




