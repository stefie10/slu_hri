#include "quaternion.h"

void quat2rot(gsl_vector* q, gsl_matrix* R){
  //gsl_matrix* R = gsl_matrix_alloc(3,3);
  
  //row 1
  gsl_matrix_set(R, 0, 0, pow(gsl_vector_get(q, 0), 2) + pow(gsl_vector_get(q, 1), 2) - 
		 pow(gsl_vector_get(q, 2), 2) - pow(gsl_vector_get(q, 3), 2));
  gsl_matrix_set(R, 0, 1, 2*(gsl_vector_get(q, 1)*gsl_vector_get(q, 2) -gsl_vector_get(q, 0)* gsl_vector_get(q, 3)));
  gsl_matrix_set(R, 0, 2, 2*(gsl_vector_get(q, 1)*gsl_vector_get(q, 3) + gsl_vector_get(q, 0)* gsl_vector_get(q, 2)));
  
  //row 2
  gsl_matrix_set(R, 1, 0, 2*(gsl_vector_get(q, 1)*gsl_vector_get(q, 2) + gsl_vector_get(q, 0)* gsl_vector_get(q, 3)));
  gsl_matrix_set(R, 1, 1, pow(gsl_vector_get(q, 0), 2) + pow(gsl_vector_get(q, 2), 2) - 
		 pow(gsl_vector_get(q, 1), 2) - pow(gsl_vector_get(q, 3), 2));
  gsl_matrix_set(R, 1, 2, 2*(gsl_vector_get(q, 2)*gsl_vector_get(q, 3) - gsl_vector_get(q, 0)* gsl_vector_get(q, 1)));

  //row 3
  gsl_matrix_set(R, 2, 0, 2*(gsl_vector_get(q, 1)*gsl_vector_get(q, 3) - gsl_vector_get(q, 0)* gsl_vector_get(q, 2)));
  gsl_matrix_set(R, 2, 0, 2*(gsl_vector_get(q, 2)*gsl_vector_get(q, 3) + gsl_vector_get(q, 0)* gsl_vector_get(q, 1)));
  gsl_matrix_set(R, 1, 1, pow(gsl_vector_get(q, 0), 2) + pow(gsl_vector_get(q, 3), 2) - 
		 pow(gsl_vector_get(q, 1), 2) - pow(gsl_vector_get(q, 2), 2));

}

