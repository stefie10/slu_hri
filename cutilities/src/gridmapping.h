#ifndef GRIDMAPPING_H
#define GRIDMAPPING_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_block_float.h>
#include "gsl_utilities.h"
#include "probability.h"
#include "gsl_utilities.h"
#include "carmen_util.h"
#include "procrustes.h"
#include "noise_models.h"
#include "spline.h"
#include "tklib_log_gridmap.h"
//#include <math.h>

#ifdef __cplusplus
extern "C" {
#endif

class occupancy_grid_mapper{
 private:
  //variables
  //double rel_start_angle, rel_end_angle;
  double l_occ, l_free, l_nought, alpha;
  double max_range;
  int first_reading;
  gsl_vector *curr_pose;



  //functions
  gsl_matrix* box_pts(double r);
  void nearest_neighbors_map(gsl_matrix* points, gsl_matrix* nn_pts);
  void nearest_neighbor_map(gsl_vector* point, gsl_vector *nn_pt);
  gsl_matrix* get_non_max_range_readings(gsl_vector* range,
					 gsl_matrix* curr_pts, 
					 double max_range);


  //will perform a ray trace on the map from
  //startx, starty, start_theta for length distance
  void update_ray_trace(double startx, double starty, 
			double start_theta, double distance);
  
  //calling update_reading will simply trace out the map from
  //the given robot pose and the measurments in xy coordinates
  void update_ray_trace_xy(gsl_vector* pose, 
			   gsl_matrix* new_measurements_xy);

  gsl_matrix* nearest_neighbors_map_alloc(gsl_matrix* points);
  
 public:
  tklib_log_gridmap map;
  
  occupancy_grid_mapper(double p_occ, double p_free, double p_nought_occ, 
			double x_size, double y_size,double resolution, 
			gsl_vector *start_pose, double alpha_in);
  //double rel_start_anglei, double rel_end_anglei);
  ~occupancy_grid_mapper();

  gsl_vector* get_pose(){
    gsl_vector* ret_pose =gsl_vector_alloc(curr_pose->size);
    gsl_vector_memcpy(ret_pose, curr_pose);
    return ret_pose;
  }

  //performs iterative closest point on the map for measured_points
  //tau is the change in the error from one timestep to the next
  //maxsse is the maximum sum squared error tolerated
  //gsl_matrix* icp_map(gsl_matrix* measured_points, int num_iters);


  //calling update will try to infer the robot pose from an initial
  //robot pose and a set of readings
  void update(gsl_vector* from_pose,  gsl_vector *reading, 
	      double rel_start_angle, double rel_end_angle);

  //update using icp
  //void update_icp(gsl_vector* from_pose,  gsl_vector *reading, int num_iters);

  //do the ray_tracing  
  //gsl_vector* ray_trace(double startx, double starty, gsl_vector* thetas);

};
#ifdef __cplusplus
}
#endif


#endif
