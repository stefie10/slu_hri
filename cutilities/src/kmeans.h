
#ifndef KMEANS_H
#define KMEANS_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include "probability.h"
#include "gsl_utilities.h"
#include "gaussian.h"

#ifdef __cplusplus
extern "C" {
#endif
gsl_matrix* kmeans(gsl_matrix *X, int iterations, gsl_matrix* init_means);
gsl_matrix* kmeans_autoinit(gsl_matrix *X, int iterations, int num_clusters);
gsl_vector* kmeans_get_labels(gsl_matrix* X, gsl_matrix* means);
gsl_matrix* kmeans_get_distances(gsl_matrix* X, gsl_matrix* pts);
gsl_matrix* kmeans_compute_mean(gsl_matrix* X, gsl_vector* labels);
gsl_vector* kmeans_get_log_likelihood(gsl_matrix* X, gsl_matrix* u, 
				      gsl_vector* labels, double std);



  int select_initial_cluster(gsl_matrix *X, gsl_matrix* init_clusters);
#ifdef __cplusplus
}
#endif


#endif
