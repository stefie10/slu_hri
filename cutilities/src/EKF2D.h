#ifndef EKF2D_H
#define EKF2D_H

#ifdef __cplusplus
extern "C" {
#endif
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <math.h>
#include <gsl/gsl_cblas.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_linalg.h>
#include "gsl_utilities.h"

  typedef struct {
    gsl_vector *U;
    gsl_matrix *SIGMA;
    gsl_vector *associations;
  } EKF2D_filter_state;
  

EKF2D_filter_state* EKF2D_measurement_update(gsl_matrix* measurements, 
					     gsl_matrix* measurement_covariance, 
					     double alpha, gsl_vector* U, gsl_matrix* SIGMA);



gsl_matrix * EKF2D_get_transfer_function(gsl_matrix* measurements,
					 gsl_matrix* measurement_noise, 
					 gsl_matrix* motion_jacobian,
                                         gsl_matrix* motion_noise, 
					 gsl_matrix* motion_jacobian_zero,
					 gsl_matrix* motion_noise_zero, 
					 double alpha, gsl_vector* U, gsl_matrix* SIGMA);

#ifdef __cplusplus
}
#endif

#endif


