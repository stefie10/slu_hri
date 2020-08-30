#include <gsl/gsl_matrix.h>
#include "nearest_neighbor.h"
#include "gsl_utilities.h"
#include <math.h>

#ifndef QUATERNION_H
#define QUATERNION_H

#ifdef __cplusplus
extern "C" {
#endif
void quat2rot(gsl_vector* q, gsl_matrix* R);

#ifdef __cplusplus
}
#endif


#endif



