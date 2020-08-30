

#ifndef GAUSSIAN_H
#define GAUSSIAN_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_cblas.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_sf_log.h>
#include <math.h>
#include "gsl_utilities.h"
#include "probability.h"
#ifdef __cplusplus
extern "C" {
#endif
gsl_vector* gaussian_normal_sample(gsl_matrix *cov, gsl_vector *u);
gsl_vector* gaussian_log_prob(gsl_matrix* X, gsl_vector* u, gsl_matrix* cov);
#ifdef __cplusplus
}
#endif


#endif
