#include "nearest_neighbor.h"
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_eigen.h>
#include <gsl/gsl_sort_vector.h>
#include <math.h>

//v should be of the size of each point
gsl_vector* NN(gsl_vector* pt, gsl_matrix* pts){
  gsl_vector* v = gsl_vector_calloc(pt->size);
  gsl_vector* euc_dist = tklib_get_distance(pts, pt);
  size_t min_index = gsl_vector_min_index(euc_dist);
  
  gsl_matrix_get_col(v, pts, min_index);
  
  gsl_vector_free(euc_dist);
  
  return v;
}

//ret_mat should be the same size of pts
gsl_matrix* NNs(gsl_matrix* pts, gsl_matrix* model_pts){
  size_t i;
  gsl_matrix* ret_mat = gsl_matrix_calloc(pts->size1, pts->size2);
  gsl_vector* curr_col = gsl_vector_calloc(pts->size1);
  gsl_vector* curr_closest; //= gsl_vector_calloc(pts->size1);

  for(i=0; i<pts->size2; i++){
    gsl_matrix_get_col(curr_col, pts, i);
    curr_closest = NN(curr_col, model_pts);
    gsl_matrix_set_col(ret_mat, i, curr_closest);
    gsl_vector_free(curr_closest);
  }
  
  gsl_vector_free(curr_col);
  //gsl_vector_free(curr_closest);
  
  return ret_mat;
}

gsl_vector* NNs_index(gsl_matrix* pts, gsl_matrix* model_pts){
  size_t i;
  gsl_vector* ret_vec = gsl_vector_calloc(pts->size2);
  gsl_vector* curr_col = gsl_vector_calloc(pts->size1);
  gsl_vector* curr_closest; //= gsl_vector_calloc(ptsx->size1);

  //printf("next\n");
  for(i=0; i<pts->size2; i++){
    //printf("starting\n");
    gsl_matrix_get_col(curr_col, pts, i);
    //printf("starting2\n");
    curr_closest = kNN_index(curr_col, model_pts, 1);
    //printf("starting3\n");
    gsl_vector_set(ret_vec, i, gsl_vector_get(curr_closest, 0));
    //printf("starting4\n");
    gsl_vector_free(curr_closest);
  }
  
  gsl_vector_free(curr_col);
  //gsl_vector_free(curr_closest);
  
  return ret_vec;
}


gsl_matrix* kNN(gsl_vector* pt, gsl_matrix* pts, int k){
  gsl_matrix* myNN = NN_all(pt, pts);
  gsl_matrix_view nnview = gsl_matrix_submatrix(myNN, 0, 0, myNN->size1, k);
  
  gsl_matrix* ret_matrix = gsl_matrix_calloc(myNN->size1, k);
  gsl_matrix_memcpy(ret_matrix, &nnview.matrix);

  gsl_matrix_free(myNN);
  return ret_matrix;
}


gsl_vector* kNN_index(gsl_vector* pt, gsl_matrix* pts, int k){
  gsl_permutation* myNN_index = NN_all_index(pt, pts);
  gsl_vector* myNN_index_vec = tklib_permutation_to_vector(myNN_index);  
  
  gsl_vector_view nn_ind_view = gsl_vector_subvector(myNN_index_vec, 0, k);
  
  gsl_vector* ret_vec = gsl_vector_calloc(k);
  gsl_vector_memcpy(ret_vec, &nn_ind_view.vector);

  gsl_permutation_free(myNN_index);
  gsl_vector_free(myNN_index_vec);
  return ret_vec;
}


//pts are assumed to be MxN, where M is the number of
//dimensions of the points and N is the number of points
gsl_permutation* NN_all_index(gsl_vector* pt, gsl_matrix* pts){
  gsl_permutation* euc_dist_ind = gsl_permutation_calloc(pts->size2);

  gsl_vector* euc_dist = tklib_get_distance(pts, pt);
  gsl_sort_vector_index(euc_dist_ind, euc_dist);
  
  gsl_vector_free(euc_dist);
  return euc_dist_ind;
}

//pts are assumed to be MxN, where M is the number of
//dimensions of the points and N is the number of points
gsl_matrix* NN_all(gsl_vector* pt, gsl_matrix* pts){
  gsl_permutation* nn_inds = NN_all_index(pt, pts);
  gsl_matrix* ret_pts = gsl_matrix_calloc(pts->size1, pts->size2);
  
  size_t i;
  size_t myindex;
  gsl_vector* curr_column = gsl_vector_calloc(pts->size1);
  
  for(i=0; i<nn_inds->size; i++){
    myindex = gsl_permutation_get(nn_inds, i);
    
    gsl_matrix_get_col(curr_column, pts, myindex);
    gsl_matrix_set_col(ret_pts, i, curr_column);
  }
  
  gsl_vector_free(curr_column);
  gsl_permutation_free(nn_inds);
  return ret_pts;
}
