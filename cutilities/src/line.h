#ifndef LINE1_H
#define LINE1_H

#ifdef __cplusplus
extern "C" {
#endif
#include <gsl/gsl_vector.h>
#include <math.h>
#include "gsl_utilities.h"
double line_perpendicular_distance(gsl_vector* pt, double m, double b);
void get_line_parameters_m_pt(double m, gsl_vector* pt, 
			      double* m_ret, double* b_ret);
void get_line_parameters_m_b(gsl_vector* pt1, gsl_vector* pt2, 
			     double* m_ret, double* b_ret);
#ifdef __cplusplus
}
#endif

#endif



