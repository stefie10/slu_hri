#include "simulator.h"

simulator2D::simulator2D(motion_noise_model_slip* mnm_in, 
			 double laser_noise_std,
			 char* map_filename_in){

  //set the standard deviation of the laser noise
  laser_std = laser_noise_std;

  //load the map
  map.load_carmen_map(map_filename_in);

  //initialize the state variables
  gsl_vector* start_pt = get_random_open_location(0.3);
  double theta = tklib_normalize_theta(tklib_random()*2*M_PI);
  
  //set the start pose
  gsl_vector* start_pose = gsl_vector_alloc(3);
  gsl_vector_set(start_pose, 0, gsl_vector_get(start_pt, 0));
  gsl_vector_set(start_pose, 1, gsl_vector_get(start_pt, 1));
  gsl_vector_set(start_pose, 2, theta);
  
  true_pose = gsl_vector_alloc(start_pose->size);
  corrupted_pose = gsl_vector_alloc(start_pose->size);
  gsl_vector_memcpy(true_pose, start_pose);
  gsl_vector_memcpy(corrupted_pose, start_pose);
  
  //copy the noise models
  nm.copy(mnm_in);
  
  //seen hurdles
  seen_hurdles = NULL;
  
  //free the extra variables
  gsl_vector_free(start_pose);
  gsl_vector_free(start_pt);
}

/*simulator2D::simulator2D(gsl_vector* start_pose, 
			 motion_noise_model_slip* mnm_in, 
			 double laser_noise_std,
			 char* map_filename_in){
  //set the standard deviation of the laser noise
  laser_std = laser_noise_std;

  //load the map
  map.load_carmen_map(map_filename_in);

  //initialize the state variables
  true_pose = gsl_vector_alloc(start_pose->size);
  corrupted_pose = gsl_vector_alloc(start_pose->size);
  gsl_vector_memcpy(true_pose, start_pose);
  gsl_vector_memcpy(corrupted_pose, start_pose);
  
  //copy the noise models
  nm.copy(mnm_in);
  //onm.copy(onm_in);

  //seen hurdles
  seen_hurdles = NULL;

  //free extra variables
  gsl_vector_free(start_pose);
  }*/

simulator2D::~simulator2D(){
  gsl_vector_free(true_pose);
  gsl_vector_free(corrupted_pose);
  if(seen_hurdles != NULL)
    gsl_vector_free(seen_hurdles);
}

void simulator2D::add_hurdles(double hurdle_width, double pole_size, int num_hurdles){
  seen_hurdles = gsl_vector_calloc(num_hurdles);
  map.add_hurdles(hurdle_width, pole_size, num_hurdles);
}

gsl_vector* simulator2D::get_true_pose(){
    gsl_vector* ret_pose =gsl_vector_alloc(true_pose->size);
    gsl_vector_memcpy(ret_pose, true_pose);
    return ret_pose;
}

gsl_vector* simulator2D::get_pose(){
    gsl_vector* ret_pose =gsl_vector_alloc(corrupted_pose->size);
    gsl_vector_memcpy(ret_pose, corrupted_pose);
    return ret_pose;
}

void simulator2D::reset_pose(gsl_vector* new_pose){
  gsl_vector_memcpy(true_pose, new_pose);
  gsl_vector_memcpy(corrupted_pose, new_pose);
}


gsl_matrix_float* simulator2D::get_map(){
  return map.to_probability_map();
}

gsl_matrix* simulator2D::get_hurdles_true(){
  return map.get_hurdles();
}

gsl_vector* simulator2D::get_random_open_location(double radius){
  return map.get_random_open_location(radius);
}


gsl_vector* simulator2D::get_random_open_location_from_pt(gsl_vector* pt, 
							  double distance, 
							  double box_radius){
  return map.get_random_open_location_from_pt(pt, distance, box_radius);
}

gsl_matrix* simulator2D::simulate_extracted_hurdles(){
  gsl_vector* sim_meas = simulate_measurements();

  if(sim_meas == NULL)
    return NULL;
  
  gsl_matrix* XY = tklib_rtheta_to_xy(true_pose, sim_meas);
  gsl_matrix* features = hurdles_extract_optimized(XY, 0.2413, 0.03, 1.2, 1.2, 7.0, 15);
  
  gsl_vector_free(sim_meas);
  gsl_matrix_free(XY);
  if(features == NULL)
    return NULL;

  //convert to R, theta
  gsl_matrix* R_theta = tklib_xy_to_rtheta(true_pose, features);
  gsl_matrix_free(features);  
  return R_theta;
}



void simulator2D::simulate_motion(double tv, double rv, double dt){
  double dth = rv*dt;
  double dr = tv*dt;
  
  nm.update_sample(true_pose, dr, dth);
  nm.update_mean(corrupted_pose, dr, dth);
}

int simulator2D::no_obstacle(void){
  return map.location_free(true_pose);
}

gsl_vector* simulator2D::simulate_measurements(void){
  return simulate_measurements_pose(true_pose);
}

gsl_vector* simulator2D::simulate_measurements_pose(gsl_vector* curr_pose){
  if(!map.location_free(curr_pose)){
    return NULL;
  }

  gsl_vector* angles = tklib_range(-M_PI/2.0, M_PI/2.0+(M_PI/180.0), M_PI/180.0);
  
  double x = gsl_vector_get(curr_pose, 0);
  double y = gsl_vector_get(curr_pose, 1);
  double theta = gsl_vector_get(curr_pose, 2);
  
  gsl_vector_add_constant(angles, theta);

  //ray trace the relevant parts of the map
  gsl_vector* readings = map.ray_trace(x, y, angles);
  
  //add noise to the readings
  gsl_vector* noise_term = tklib_vector_randn(0.0, laser_std, angles->size);  
  gsl_vector_add(readings, noise_term);
  
  //free the memory
  gsl_vector_free(noise_term);
  gsl_vector_free(angles);
  
  return readings;
}


gsl_vector* simulator2D::hurdles_visible_get(){
  gsl_vector* ret_seen = gsl_vector_calloc(seen_hurdles->size);
  gsl_vector_memcpy(ret_seen, seen_hurdles);
  
  return ret_seen;
}

void simulator2D::hurdles_visible_update(){
  //get the hurdles and the true location of the robot
  gsl_matrix* the_hurdles = map.get_hurdles();
  gsl_matrix_view myhurdles = gsl_matrix_submatrix(the_hurdles, 0, 0, 2, the_hurdles->size2);
  gsl_vector_view true_pt = gsl_vector_subvector(true_pose, 0, 2);
  
  //get the distances to each of the hurdles
  gsl_vector* distances = tklib_get_distance(&myhurdles.matrix, &true_pt.vector);

  //subtract the pose of the robot from the landmarks
  tklib_matrix_add_vec(&myhurdles.matrix, &true_pt.vector, 1.0, -1.0);
  gsl_vector_view X = gsl_matrix_row(&myhurdles.matrix, 0);
  gsl_vector_view Y = gsl_matrix_row(&myhurdles.matrix, 1);
  
  //get the thetas
  gsl_vector* angles = tklib_arctan2(&Y.vector, &X.vector);
  gsl_vector* readings = map.ray_trace(gsl_vector_get(true_pose,0), 
				       gsl_vector_get(true_pose,1), angles);
  
  size_t i;
  double d_h; double d_r;
  for(i=0; i<distances->size;i++){
    d_h = gsl_vector_get(distances, i);
    d_r = gsl_vector_get(readings, i);
    
    if(d_r >= map.get_max_range()-0.0001){}
    else if(d_r >= d_h)
      gsl_vector_set(seen_hurdles, i, 1.0);
  }

  gsl_vector_free(distances);
  gsl_vector_free(readings);
  gsl_vector_free(angles);
  gsl_matrix_free(the_hurdles);
}


double simulator2D::min_range(){
  return map.min_range(true_pose);
}
