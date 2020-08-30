#ifndef HURDLE_EXTRACTOR_H
#define HURDLE_EXTRACTOR_H

#ifdef __cplusplus
extern "C" {
#endif
#include "Python.h"
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_math.h>
#include "gsl_utilities.h"
#include "kmeans.h"
#include "nearest_neighbor.h"
#include "gsl_python.h"
#include "line.h"
#include "box_window.h"

gsl_matrix* hurdles_extract(gsl_matrix* pts, double separation, double separation_err, 
			    double window_height, double window_dw, double min_log_likelihood);

gsl_matrix* hurdles_extract_optimized(gsl_matrix* pts, double separation, 
				      double separation_err, double window_height, 
				      double window_dw, double min_log_likelihood, 
				      int searchahead);

gsl_matrix* hurdles_extract_optimized_search(gsl_matrix* pts, double separation, 
					     double separation_err, double window_height, 
					     double window_dw, double min_log_likelihood, 
					     int searchahead);
#ifdef __cplusplus
}
#endif

#endif


