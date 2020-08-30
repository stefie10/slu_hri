#include "noise_models.h"


void noise_model2D::copy(noise_model2D *onm){
  mu_tv=onm->mu_tv;
  mu_rv=onm->mu_rv;
  std_tv=onm->std_tv;
  std_rv=onm->std_rv;
}

motion_noise_model_slip::motion_noise_model_slip(noise_model2D *radius_noise_model_in, 
						 noise_model2D *angular_noise_model_in, 
						 noise_model2D *slip_noise_model_in){
  radius_noise_model.copy(radius_noise_model_in);
  angular_noise_model.copy(angular_noise_model_in);
  slip_noise_model.copy(slip_noise_model_in);
}

void motion_noise_model_slip::copy(motion_noise_model_slip *onm){
  
  radius_noise_model.copy(&onm->radius_noise_model);
  angular_noise_model.copy(&onm->angular_noise_model);
  slip_noise_model.copy(&onm->slip_noise_model);
}

gsl_vector* motion_noise_model_slip::getmean(double dr, double dth){
  gsl_vector* retmean = gsl_vector_alloc(3);
  gsl_vector_set(retmean, 0, radius_noise_model.getmean(dr, dth));
  gsl_vector_set(retmean, 1, angular_noise_model.getmean(dr, dth));
  gsl_vector_set(retmean, 2, slip_noise_model.getmean(dr, dth));
  return retmean;
}

gsl_vector* motion_noise_model_slip::update_sample_copy(gsl_vector* curr_pose, 
						      double dr, double dth){
  gsl_vector* myvec = gsl_vector_alloc(curr_pose->size);
  update_sample(curr_pose, dr, dth);
  gsl_vector_memcpy(myvec, curr_pose);
  return myvec;
}

gsl_vector* motion_noise_model_slip::update_mean_copy(gsl_vector* curr_pose, 
						      double dr, double dth){
  gsl_vector* myvec = gsl_vector_alloc(curr_pose->size);
  update_mean(curr_pose, dr, dth);
  gsl_vector_memcpy(myvec, curr_pose);
  return myvec;
}

void motion_noise_model_slip::update_sample(gsl_vector* curr_pose, 
					    double dr, double dth){
  //get the actual motion
  gsl_vector* U = getmean(dr, dth/2.0);
  gsl_matrix* N = getvariance(dr, dth/2.0);
  
  //sample and get the true error parameters
  //the world corrupts things
  gsl_vector* nsamp = gaussian_normal_sample(N, U);
  double dr_true = gsl_vector_get(nsamp, 0);
  double dth_true = gsl_vector_get(nsamp, 1);
  double dslip_true = gsl_vector_get(nsamp, 2);
  
  //printf("update_sample\n");
  update(curr_pose, dr_true, dth_true*2.0, dslip_true);
  //printf("dr_true-->%f\n", dr_true);
  //printf("dth_true-->%f\n", dth_true);
  //printf("dsl_true-->%f\n", dslip_true);
  //tklib_vector_printf(curr_pose);
  
  gsl_vector_free(U);
  gsl_matrix_free(N);
  gsl_vector_free(nsamp);
}

void motion_noise_model_slip::update_mean(gsl_vector* curr_pose, 
					  double dr, double dth){
  //printf("update_mean\n");
   //get the actual motion
  gsl_vector* mymean = getmean(dr, dth/2.0);
  double dr_true = gsl_vector_get(mymean, 0);
  double dth_true = gsl_vector_get(mymean, 1);
  double dsl_true = gsl_vector_get(mymean, 2);

  //printf("dr_true-->%f\n", dr_true);
  //printf("dth_true-->%f\n", dth_true);
  //printf("dsl_true-->%f\n", dsl_true);
  //printf("before\n");
  //  tklib_vector_printf(curr_pose);
  update(curr_pose, dr_true, dth_true*2.0, dsl_true);
  //printf("after\n");
  //tklib_vector_printf(curr_pose);
  gsl_vector_free(mymean);
}


void motion_noise_model_slip::update(gsl_vector* curr_pose, 
				     double dr, double dth, double ds){
  //get the values in the current pose
  double x = gsl_vector_get(curr_pose, 0);
  double y = gsl_vector_get(curr_pose, 1);
  double th = gsl_vector_get(curr_pose, 2);

  //compute the updated motion values given the expected motion
  
  //double test_res =  dr*cos(th + dth/2.0);
  //double test_res2 = ds*cos(th + dth/2.0 + M_PI/2.0);
  //printf("test me--> res1=%f , res2=%f\n", test_res, test_res2);

  double x_pr = x + (dr)*cos(th + dth/2.0) + ds*cos(th + dth/2.0 + M_PI/2.0);
  double y_pr = y + (dr)*sin(th + dth/2.0) + ds*sin(th + dth/2.0 + M_PI/2.0);
  double th_pr = tklib_normalize_theta(th + dth);
  
  //copy it into a return value
  gsl_vector_set(curr_pose, 0, x_pr);
  gsl_vector_set(curr_pose, 1, y_pr);
  gsl_vector_set(curr_pose, 2, th_pr);
}

gsl_matrix* motion_noise_model_slip::getvariance(double dr, double dth){
  gsl_vector* retvar = gsl_vector_alloc(3);
  gsl_vector_set(retvar, 0, radius_noise_model.getvar(dr, dth));
  gsl_vector_set(retvar, 1, angular_noise_model.getvar(dr, dth));
  gsl_vector_set(retvar, 2, slip_noise_model.getvar(dr, dth));
  
  gsl_matrix* retmat =  tklib_diag(retvar);
  gsl_vector_free(retvar);
  
  return retmat;
}

gsl_matrix* motion_noise_model_slip::getstd(double dr, double dth){
  gsl_vector* retvar = gsl_vector_alloc(3);
  gsl_vector_set(retvar, 0, sqrt(radius_noise_model.getvar(dr, dth)));
  gsl_vector_set(retvar, 1, sqrt(angular_noise_model.getvar(dr, dth)));
  gsl_vector_set(retvar, 2, sqrt(slip_noise_model.getvar(dr, dth)));
  
  gsl_matrix* retmat =  tklib_diag(retvar);
  gsl_vector_free(retvar);
  
  return retmat;
}



point_feature_model::point_feature_model(double std_r_in, double std_phi_in, double std_signature_in){
  std_r = std_r_in;
  std_phi = std_phi_in;
  std_signature = std_signature_in;
}


gsl_matrix* point_feature_model::getvariance(){
  gsl_vector* var = gsl_vector_alloc(3);
  gsl_vector_set(var, 0, pow(std_r,2));
  gsl_vector_set(var, 1, pow(std_phi,2));
  gsl_vector_set(var, 2, pow(std_signature,2));
  
  gsl_matrix* retvar = tklib_diag(var);
  gsl_vector_free(var);
  return retvar;
}

gsl_matrix* point_feature_model::getstd(){
  gsl_vector* var = gsl_vector_alloc(3);
  gsl_vector_set(var, 0, std_r);
  gsl_vector_set(var, 1, std_phi);
  gsl_vector_set(var, 2, std_signature);
  
  gsl_matrix* retvar = tklib_diag(var);
  gsl_vector_free(var);
  return retvar;
}

void point_feature_model::copy(point_feature_model *onm){
  std_r = onm->std_r;
  std_phi = onm->std_phi;
  std_signature = onm->std_signature;
}
