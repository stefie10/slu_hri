#ifndef BOXWINDOW1_H
#define BOXWINDOW1_H

#ifdef __cplusplus
extern "C" {
#endif
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <math.h>
#include "line.h"
#include "gsl_utilities.h"

gsl_matrix* box_inwindow(gsl_matrix* pts, gsl_vector* x_st, gsl_vector* x_end,
			 double box_height, double box_dw, 
			 double width_line_m, double width_line_b, 
			 double height_line_m, double height_line_b);

gsl_matrix* box_outwindow(gsl_matrix* pts, gsl_vector* x_st, gsl_vector* x_end,
			  double box_height, double box_dw, 
			  double width_line_m, double width_line_b, 
			  double height_line_m, double height_line_b);


#ifdef __cplusplus
}
#endif

#endif



