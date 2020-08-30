#include "gaussian.h"


gsl_vector* gaussian_normal_sample(gsl_matrix *cov, gsl_vector *u){
  //return random vector
  gsl_vector* ret_vec = gsl_vector_alloc(u->size);

  //R = linalg.decomp.cholesky(cov);
  gsl_matrix* R = tklib_linalg_cholesky_decomp(cov);
  //printf("choleskyC\n");
  //tklib_matrix_printf(R);
  gsl_vector* x = tklib_vector_randn(0.0, 1.0, u->size);
  
  //myVal = matrixmultiply(R, x)+u;
  gsl_blas_dgemv(CblasNoTrans, 1.0, R , x , 0.0, ret_vec);
  gsl_vector_add(ret_vec, u);
  
  gsl_matrix_free(R);
  gsl_vector_free(x);
  return ret_vec;
}

/*Inspired by the following code:
  N = len(X)
  Z = 1.0/(((2*pi)**(N/2.0))*det(cov)**(1/2.0))
  
  R1 = matrixmultiply(transpose(X-transpose([u])), inv(cov))
  R2 = R1*transpose(X-transpose([u]))
  V = sum(R2, 1)
  
  l_prob = log(Z) + (-1.0/2.0)*V
  return l_prob*/
gsl_vector* gaussian_log_prob(gsl_matrix* X, gsl_vector* u, gsl_matrix* cov){
  
  //get the inverse covariance matrix
  int signum;
  gsl_permutation* p_cov = gsl_permutation_calloc(cov->size1);
  gsl_matrix* LU_cov = gsl_matrix_calloc(cov->size1, cov->size2);
  gsl_matrix_memcpy(LU_cov, cov);
  gsl_linalg_LU_decomp(LU_cov, p_cov, &signum);
  
  //get ints determinant
  double determinant = gsl_linalg_LU_det(LU_cov, signum);
  int N = X->size1;
  double Z = 1.0/(pow(2*M_PI, N/2.0)*sqrt(determinant));
  
  //make a copy of X
  gsl_matrix* X_tmp = gsl_matrix_calloc(X->size1, X->size2);
  gsl_matrix_memcpy(X_tmp, X);
  
  //perform the inverse covariance
  gsl_matrix* inv_cov = gsl_matrix_calloc(cov->size1, cov->size2);
  gsl_permutation* p_inv_cov = gsl_permutation_calloc(cov->size1);
  gsl_linalg_LU_invert(LU_cov, p_inv_cov, inv_cov);

  //subtract out the mean
  tklib_matrix_add_vec(X_tmp, u, 1.0, -1.0);

  //create the results
  gsl_matrix* R1 = gsl_matrix_calloc(X->size2, X->size1);  
  gsl_blas_dgemm(CblasTrans, CblasNoTrans, 1.0, X_tmp , inv_cov , 0.0, R1);
  //gsl_matrix* R1 = matrixmultiply(transpose(X-transpose([u])), inv(cov));

  gsl_matrix* X_tmp_transpose = gsl_matrix_calloc(X_tmp->size2, X_tmp->size1);
  gsl_matrix_transpose_memcpy(X_tmp_transpose, X_tmp);
  gsl_matrix_mul_elements(R1, X_tmp_transpose);
  gsl_vector* V = tklib_matrix_sum(R1, 1);

  gsl_vector_scale(V, (-1.0/2.0));
  gsl_vector_add_constant(V, gsl_sf_log(Z));
  

  gsl_permutation_free(p_cov);
  gsl_permutation_free(p_inv_cov);
  gsl_matrix_free(LU_cov);
  gsl_matrix_free(X_tmp);
  gsl_matrix_free(X_tmp_transpose);
  gsl_matrix_free(inv_cov);
  gsl_matrix_free(R1);
  return V;
}
