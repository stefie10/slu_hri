#ifndef NNeihbor_H
#define NNeihbor_H

#ifdef __cplusplus
extern "C" {
#endif
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_permutation.h>
#include "gsl_utilities.h"
gsl_matrix* NN_all(gsl_vector* pt, gsl_matrix* pts);
gsl_permutation* NN_all_index(gsl_vector* pt, gsl_matrix* pts);

gsl_matrix* kNN(gsl_vector* pt, gsl_matrix* pts, int k);
gsl_vector* kNN_index(gsl_vector* pt, gsl_matrix* pts, int k);

gsl_vector* NN(gsl_vector* pt, gsl_matrix* pts);
gsl_matrix* NNs(gsl_matrix* pts, gsl_matrix* model_pts);
gsl_vector* NNs_index(gsl_matrix* pts, gsl_matrix* model_pts);

#ifdef __cplusplus
}
#endif

#endif
