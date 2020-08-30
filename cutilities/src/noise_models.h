#ifndef NOISE_MODELS_H
#define NOISE_MODELS_H

#ifdef __cplusplus
extern "C" {
#endif
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include "gsl_utilities.h"
#include "gaussian.h"

//base class to define a noise model for the motion noise
//  in the r, slip and theta directions
class noise_model2D{
 private:
  double mu_tv, mu_rv, std_tv, std_rv;
 public:
  noise_model2D(){}
  noise_model2D(double mu_tv_in, double mu_rv_in, double std_tv_in, double std_rv_in){
    mu_tv = mu_tv_in;
    mu_rv = mu_rv_in;
    std_tv = std_tv_in;
    std_rv = std_rv_in;
  }
  double getmean(double tv, double rv){return mu_tv*tv + mu_rv*rv;}
  double getvar(double tv, double rv){return pow(std_tv*tv,2.0) + pow(std_rv*rv,2.0);}
  double getstd(double tv, double rv){return sqrt(pow(std_tv*tv,2.0) + pow(std_rv*rv,2.0));}
  void copy(noise_model2D* other_noise_model);
};


//this is the motion model noise model 
//  and includes a noise term for slip
class motion_noise_model_slip{
 private:
  noise_model2D radius_noise_model;
  noise_model2D angular_noise_model;

 public:
  noise_model2D slip_noise_model;

  motion_noise_model_slip(){}
  motion_noise_model_slip(noise_model2D *radius_noise_model_in, 
			  noise_model2D *angular_noise_model_in, 
			  noise_model2D *slip_noise_model_in);
  
  void copy(motion_noise_model_slip *onm);
  gsl_vector* getmean(double dr, double dth);
  gsl_matrix* getvariance(double dr, double dth);
  gsl_matrix* getstd(double dr, double dth);


  //update the current pose with these particular
  //    values for dr, dth, and ds
  void update(gsl_vector* curr_pose, 
	      double dr, double dth, double ds);

  //update the pose with the mean from the given noise models
  //   and the parr motion model
  void update_mean(gsl_vector* curr_pose, 
		   double dr, double dth);

  //update the pose with the mean and return the result
  gsl_vector* update_mean_copy(gsl_vector* curr_pose, 
			       double dr, double dth);

  //update by sampling errors in each of the variables, 
  //  updates the values in place, does not return a value
  void update_sample(gsl_vector* curr_pose, 
		     double dr, double dth);
  
  //update and return a copy
  gsl_vector* update_sample_copy(gsl_vector* curr_pose, 
				 double dr, double dth);

};


//this is the observation noise model for use in gaussian point
//    features
class point_feature_model{
 private:
  double std_r, std_phi, std_signature;
 public:
  point_feature_model(double std_r_in, double std_phi_in, double std_signature_in);
  //point_feature_model(){};
  gsl_matrix* getvariance();
  gsl_matrix* getstd();
  void copy(point_feature_model *onm);
};

#ifdef __cplusplus
}
#endif

#endif
