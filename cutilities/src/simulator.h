#ifndef SIMULATOR1_H
#define SIMULATOR1_H

#ifdef __cplusplus
extern "C" {
#endif
#include "hurdle_extractor.h"
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <math.h>
#include "gsl_utilities.h"
#include "noise_models.h"
#include "tklib_log_gridmap.h"
  //#include "gridmapping.h"

class simulator2D{
 private:
  //private variables

  //true and corrupted poses of the robot
  gsl_vector* true_pose;
  gsl_vector* corrupted_pose;

  //motion noise model and observation std
  motion_noise_model_slip nm;
  double laser_std;

  //hurdles that have been seen by the robot
  gsl_vector* seen_hurdles;
  
 public:
  //variables
  tklib_log_gridmap map;

  //functions
  /*constructors: when init_pose is not specified, the
   initial robot pose is automatically selected by obtaining
   a random initial open pose.*/
  
  /*simulator2D(gsl_vector* init_pose, motion_noise_model_slip* mnm, 
	      observation_noise_model* onm, char* map_filename_in);

  simulator2D(motion_noise_model_slip* mnm, 
  observation_noise_model* onm, char* map_filename_in);*/

  simulator2D(motion_noise_model_slip* mnm_in, 
	      double laser_noise_std,  char* map_filename_in);
	      

  //simulator2D(gsl_vector* start_pose,motion_noise_model_slip* mnm_in, 
  //double laser_noise_std,char* map_filename_in);
	      
  ~simulator2D();

  gsl_matrix_float *get_map();
  gsl_vector *get_true_pose();
  gsl_vector* get_pose();  
  void reset_pose(gsl_vector* new_pose);
  int no_obstacle(void);

  //get free location
  gsl_vector* get_random_open_location(double radius);
  gsl_vector* get_random_open_location_from_pt(gsl_vector* pt, double distance, double box_radius);

  //simulating measurements 
  gsl_vector* simulate_measurements(void);
  gsl_vector* simulate_measurements_pose(gsl_vector* curr_pose);

  //simulating motion
  void simulate_motion(double tv, double rv, double dt);

  //regarding hurdles
  gsl_matrix* get_hurdles_true();
  void add_hurdles(double hurdle_width, double pole_size, int num_hurdles);
  void hurdles_visible_update();
  gsl_vector* hurdles_visible_get();

  
  //simulate the hurdles from real readings
  gsl_matrix* simulate_extracted_hurdles();
  
  //
  double min_range();
};

#ifdef __cplusplus
}
#endif

#endif


