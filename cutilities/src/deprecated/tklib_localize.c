#include "tklib_localize.h"

  
tklib_localize::tklib_localize(){
  //initialize the filter
  filter_params = get_default_parameters();
  filter = carmen_localize_particle_filter_new(filter_params);
}


tklib_localize::~tklib_localize(){
  free(filter_params->motion_model);
  free(filter_params);
}


void tklib_localize::update(gsl_vector* robot_pose, 
			    gsl_vector* readings, double offset, int backwards){
  robot_pose = robot_pose;
  readings = readings;
  offset = offset;
  backwards = backwards;
  
  //gsl_matrix* themap = gridmap.to_carmen_map();
  
  //carmen_localize_run(filter, themap, readings, offset, backwards);
}



carmen_localize_param_p tklib_localize::get_default_parameters(){
  carmen_localize_param_p default_params;
  default_params = (carmen_localize_param_p)calloc(1, sizeof(carmen_localize_param_t));
  
  default_params->front_laser_offset = 0.0;  
  default_params->rear_laser_offset = 0.0;  
  default_params->num_particles = 1000;
  default_params->max_range = 30.0;
  default_params->min_wall_prob			= 0.25;
  default_params->outlier_fraction		= 0.90;
  default_params->update_distance		= 0.20;
  //## integrate a beam each n rads (new version of laser_skip)

  default_params->integrate_angle		= 0.052359;   //## 3 degrees
  default_params->do_scanmatching		= 0;
  default_params->constrain_to_map		= 0;
  default_params->occupied_prob	                = 0.5;
  default_params->lmap_std			= 0.3;
  default_params->global_lmap_std		= 0.6;
  default_params->global_evidence_weight		= 0.01;
  default_params->global_distance_threshold	= 2.0;
  default_params->global_test_samples		= 100000;
  default_params->use_sensor			= 1;

  //not in any config file
  default_params->laser_skip = 1;
  default_params->use_rear_laser = 0;

  //make the motion model
  carmen_localize_motion_model_t* motion_model;
  motion_model = (carmen_localize_motion_model_t*)calloc(1, sizeof(carmen_localize_motion_model_t));
  motion_model->mean_c_d = -0.0123;
  motion_model->mean_c_t = -0.1065;
  motion_model->std_dev_c_d =0.1380;
  motion_model->std_dev_c_t =0.2347;

  motion_model->mean_d_d = 1.0055;
  motion_model->mean_d_t = 0.0025;
  motion_model->std_dev_d_d = 0.1925;
  motion_model->std_dev_d_t = 0.3982;

  motion_model->mean_t_d = -0.0025;
  motion_model->mean_t_t = 0.9638;
  motion_model->std_dev_t_d = 0.0110;
  motion_model->std_dev_t_t = 0.3300;
  
  default_params->motion_model = motion_model;  
  return default_params;
}

