#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_eigen.h>
#include <gsl/gsl_sort_vector.h>
#include <math.h>
#include "procrustes.h"

double procrustes::run(gsl_matrix* measured_pts, gsl_matrix* model_pts){
  
  if(R != NULL){
    gsl_vector_free(t);
    gsl_matrix_free(R);
    gsl_matrix_free(rotated_pts);
  }
  
  R = gsl_matrix_alloc(measured_pts->size1, measured_pts->size1);
  t = gsl_vector_calloc(measured_pts->size1);
  rotated_pts = gsl_matrix_alloc(measured_pts->size1, measured_pts->size2);
  sse = procrustesSVD(measured_pts, model_pts, rotated_pts, R, t);

  return sse;
}



double procrustesSVD(gsl_matrix* measured_pts, gsl_matrix* model_pts, 
		     gsl_matrix* rotated_pts, gsl_matrix* R, gsl_vector* t){
  
  gsl_matrix* measured_pts_norm = tklib_subtract_mean(measured_pts);
  gsl_matrix* model_pts_norm = tklib_subtract_mean(model_pts);

  //get the covariance
  gsl_matrix* covariance_pts_model_pts = gsl_matrix_calloc(model_pts->size1, measured_pts->size1);
  gsl_blas_dgemm(CblasNoTrans, CblasTrans, 1.0/model_pts->size2, model_pts_norm,
		 measured_pts_norm, 0.0, covariance_pts_model_pts);  
  
  //allocate the things for SVD
  gsl_vector *myworkspace = gsl_vector_alloc(covariance_pts_model_pts->size1);
  gsl_matrix* V = gsl_matrix_calloc(covariance_pts_model_pts->size1, covariance_pts_model_pts->size2); 
  gsl_vector* S = gsl_vector_calloc(covariance_pts_model_pts->size1);

  //  U, D, V = svd(matrixmultiply(model-u_model, transpose(measured-u_measured))/len(measured[0]));

  gsl_linalg_SV_decomp(covariance_pts_model_pts, V, S, myworkspace);
  gsl_matrix* U = covariance_pts_model_pts;
  

  //fix up the reflection matrix problem
  double det_V = tklib_linalg_det(V);
  double det_U = tklib_linalg_det(U);
  gsl_vector* Spr_v = gsl_vector_calloc(U->size2);
  gsl_vector_add_constant(Spr_v, 1.0);
  gsl_matrix *Spr = tklib_diag(Spr_v);
  if(round(det_U*det_V) == 1.0){
  }
  else if(round(det_U*det_V) == -1.0){
    gsl_matrix_set(Spr, Spr->size2-1, Spr->size2 -1, -1.0);
  }
  else
    return -1;

  //get the rotation matrix
  //R = dot(dot(U, S), V);
  gsl_matrix* US = gsl_matrix_alloc(U->size1, Spr->size2);
  gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, U, Spr, 0.0, US);  
  gsl_blas_dgemm(CblasNoTrans, CblasTrans, 1.0, US, V, 0.0, R);  
  
  //allocate the necessary quantities for the translation vector
  gsl_vector* u_measured = tklib_mean(measured_pts, 0);
  gsl_vector* u_model = tklib_mean(model_pts, 0);
  gsl_vector* t_tmp = gsl_vector_calloc(u_measured->size);

  //get the translation vector
  //t = u_model - dot(R, u_measured);
  gsl_vector_memcpy(t, u_model);
  gsl_blas_dgemv(CblasNoTrans, 1.0, R, u_measured, 0.0, t_tmp); 
  
  //subtract the two
  gsl_vector_sub(t, t_tmp);
  
  //get the rotated points
  gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, R, measured_pts, 0.0, rotated_pts); 
  tklib_matrix_add_vec(rotated_pts, t, 1.0, 1.0);
  
  //get the sum squared error
  double sse = tklib_sse(rotated_pts, model_pts);

  //free the used space
  gsl_matrix_free(measured_pts_norm);
  gsl_matrix_free(model_pts_norm);
  gsl_matrix_free(covariance_pts_model_pts);
  gsl_vector_free(myworkspace);
  gsl_matrix_free(V);
  gsl_vector_free(S);  
  gsl_matrix_free(Spr);
  gsl_vector_free(Spr_v);
  gsl_matrix_free(US);
  gsl_vector_free(u_measured);
  gsl_vector_free(u_model);
  gsl_vector_free(t_tmp);
  
  return sse;
}


//model_pts is a 3xN set of points
//pts is a 3xN set of points
//return the sse
/*double procrustes_quaternion(gsl_matrix* pts, gsl_matrix* model_pts, 
			     gsl_matrix* rotated_pts, gsl_matrix* R, gsl_matrix* t){
  const gsl_matrix* pts_norm = tklib_subtract_mean(pts);
  const gsl_matrix* model_pts_norm = tklib_subtract_mean(model_pts);
  
  gsl_matrix* covariance_pts_and_model_pts = gsl_matrix_calloc(3, 3);

  //this will probably crash
  //printf("pts_norm\n");
  //tklib_const_matrix_printf(pts_norm);
  //printf("model_pts_norm\n");
  //tklib_const_matrix_printf(model_pts_norm);
  gsl_blas_dgemm(CblasNoTrans, CblasTrans, 1.0/model_pts->size2, pts_norm, model_pts_norm, 0.0, covariance_pts_and_model_pts);
  //printf("covariance:\n");
  //tklib_matrix_printf(covariance_pts_and_model_pts);  
  //take the transpose
  //double covtrace = trace(covariance_pts_and_model_pts);
  gsl_matrix* covariance_pts_and_model_pts_transpose = gsl_matrix_calloc(3, 3);

  //gsl_matrix* K = gsl_matrix_alloc(covariance_pts_and_model_pts->size1, covariance_pts_and_model_pts->size2 );
  gsl_matrix* K= gsl_matrix_calloc(covariance_pts_and_model_pts->size1, covariance_pts_and_model_pts->size2 );
  gsl_matrix_memcpy(K, covariance_pts_and_model_pts);
  gsl_matrix_transpose_memcpy(K, covariance_pts_and_model_pts);

  //sub irreversibly modifies the first value
  gsl_matrix_sub(covariance_pts_and_model_pts, covariance_pts_and_model_pts_transpose);
  gsl_matrix* Q = gsl_matrix_calloc(4, 4);
  gsl_matrix_set(Q, 0, 0, tklib_trace(covariance_pts_and_model_pts));
  //K = cov_ptsmodel - transpose(1.0*cov_ptsmodel)  
  gsl_matrix_set(Q, 0, 1, gsl_matrix_get(K, 1, 2)); 
  gsl_matrix_set(Q, 1, 0, gsl_matrix_get(K, 1, 2));
  gsl_matrix_set(Q, 0, 2, gsl_matrix_get(K, 2, 0));
  gsl_matrix_set(Q, 2, 0, gsl_matrix_get(K, 2, 0));
  gsl_matrix_set(Q, 0, 3, gsl_matrix_get(K, 0, 1));
  gsl_matrix_set(Q, 3, 0, gsl_matrix_get(K, 0, 1));

  gsl_matrix* J = gsl_matrix_calloc(3,3);
  gsl_matrix_memcpy(J, covariance_pts_and_model_pts);
  gsl_matrix_add(J, covariance_pts_and_model_pts_transpose);
  gsl_matrix *I = tklib_eye(3,3);
  gsl_matrix_sub(J, I);

  int i;
  for(i=1; i<4; i++){
    int j;
    for(j=1;j<4;j++){
      gsl_matrix_set(Q, i, j, gsl_matrix_get(J, i-1, j-1));
    }
  }
  
  gsl_vector* eval = gsl_vector_calloc(4);
  gsl_matrix* evec = gsl_matrix_calloc(4, 4);
  
  gsl_eigen_symmv_workspace* ewrk = gsl_eigen_symmv_alloc(4);
  gsl_eigen_symmv(Q, eval, evec, ewrk);
  gsl_eigen_symmv_sort(eval, evec, GSL_EIGEN_SORT_VAL_DESC);
  
  gsl_vector_view q = gsl_matrix_row(evec, 0);
  quat2rot(&q.vector, R);

  gsl_vector* u_pts = tklib_mean(pts, 0);
  gsl_vector* u_model = tklib_mean(model_pts, 0);
  
  //get the rotation and translation
  gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, R, u_pts, 0.0, t);
  printf("pts\n");
  tklib_matrix_printf(pts);
  printf("model_pts\n");
  tklib_matrix_printf(model_pts);
  printf("u_pts\n");
  tklib_matrix_printf(u_pts);
  printf("u_model\n");
  tklib_matrix_printf(u_model);
  printf("translation vector1\n");
  tklib_matrix_printf(t);
  tklib_matrix_add_vec_M(t, u_model, -1.0, 1.0);
  
  printf("translation vector2\n");
  tklib_matrix_printf(t);
  //rotated_pts = gsl_matrix_calloc(pts->size1, pts->size2);
  gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, R, pts, 0.0, rotated_pts);
  printf("rotated pts\n");
  tklib_matrix_printf(rotated_pts);
  tklib_matrix_add_vec_M(rotated_pts, t, 1.0, 1.0);
  
  printf("rotated and translated pts\n");
  tklib_matrix_printf(rotated_pts);

  printf("R\n");
  tklib_matrix_printf(R);

  double mysse = tklib_sse(model_pts, rotated_pts);
  //printf("end model_pts\n");
  //  tklib_const_matrix_printf(model_pts);
  //printf("end rot_pts\n");
  //tklib_const_matrix_printf(rotated_pts);  

  gsl_matrix_free(u_pts);
  gsl_matrix_free(u_model);
  gsl_vector_free(eval);
  gsl_matrix_free(evec);
  gsl_matrix_free(J);  
  gsl_matrix_free(Q);  
  gsl_matrix_free(K);  
  gsl_matrix_free(covariance_pts_and_model_pts);  
  gsl_matrix_free(covariance_pts_and_model_pts_transpose);    
  gsl_eigen_symmv_free(ewrk);
  gsl_matrix_free((gsl_matrix*)pts_norm);
  gsl_matrix_free((gsl_matrix*)model_pts_norm);
  gsl_matrix_free(I);
  return mysse;
}*/


/*gsl_matrix* icp(gsl_matrix* measured_points, gsl_matrix* model_points, double tau, double maxsse){
  gsl_matrix* prev_points = gsl_matrix_calloc(measured_points->size1, measured_points->size2);
  gsl_matrix_memcpy(prev_points, measured_points);  
  double prevsse = 200000000000000.0;
  double currsse = -200000000000000.0;
  
  //the parameters for the icp
  gsl_matrix* R = gsl_matrix_calloc(measured_points->size1, measured_points->size1);
  gsl_vector* t = gsl_vector_calloc(measured_points->size1);

  //internal parameter each time
  double mysse;
  gsl_matrix* nn_pts;
  while(prevsse - currsse > tau){
    printf("***************START ITERATION******************\n");
    //get the initial translation to subtract out the means
    // of the points ... this is done internally by procrustes,
    // however, this gives a translation in terms of the model points, so its
    // arguably better, I think
        
    //perform nearest neighbors and set the nearest neighbors
    nn_pts = NNs(prev_points, model_points);
    
    //perform procrustes here
    gsl_matrix* rotated_pts = gsl_matrix_calloc(prev_points->size1, prev_points->size2);
    mysse = procrustesSVD(prev_points, nn_pts, rotated_pts, R, t);

    gsl_matrix_free(prev_points);
    prev_points = rotated_pts;
    
    printf("sse---->: %f\n", mysse);
    if(currsse == -200000000000000.0)
      currsse = mysse;
    else{
      prevsse = currsse;
      currsse = mysse;
    }

    if(currsse < maxsse)
      break;
    
    gsl_matrix_free(nn_pts);
  }
  
  gsl_matrix_free(R);
  gsl_vector_free(t);

  return prev_points;
  }*/
