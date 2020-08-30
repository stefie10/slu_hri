#include "EKF2D.h"

gsl_vector* EKF2D_getpose(gsl_vector* U){
  gsl_vector* pose = gsl_vector_alloc(3);
  
  gsl_vector_view pose_U = gsl_vector_subvector(U, 0, 3);
  gsl_vector_memcpy(pose, &pose_U.vector);

  return pose;
}

int EKF2D_get_num_features(gsl_vector* U){
  return (U->size-3)/3;
}

int EKF2D_get_feature_index_in_state(int i){
  return (i*3)+3;
}

gsl_vector* EKF2D_getfeature(int i, gsl_vector* U){
  int index_st = EKF2D_get_feature_index_in_state(i);

  //create a vector and return it
  gsl_vector* landmark = gsl_vector_alloc(3);
  gsl_vector_view landmark_U = gsl_vector_subvector(U, index_st, 3);
  gsl_vector_memcpy(landmark, &landmark_U.vector);

  return landmark;
}

gsl_vector_view EKF2D_getfeature_view(int i, gsl_vector* U){
  int index_st = EKF2D_get_feature_index_in_state(i);
  
  //create a vector and return it
  gsl_vector_view landmark_U = gsl_vector_subvector(U, index_st, 3);

  return landmark_U;
}

gsl_vector* EKF2D_addnewfeature_mean(gsl_vector* measurement, gsl_vector* U){
  double measurement_r = gsl_vector_get(measurement, 0);
  double measurement_phi = gsl_vector_get(measurement, 1);
  double measurement_signature = gsl_vector_get(measurement, 2);
  
  gsl_vector *U_new = gsl_vector_alloc(U->size+3);  

  //Utmp[0:U->size]=self.U;
  gsl_vector_view Utmp = gsl_vector_subvector(U_new, 0, U->size);
  gsl_vector_memcpy(&Utmp.vector, U);

  //#add the mean of the new feature to the state
  double x_r = gsl_vector_get(U, 0);
  double y_r = gsl_vector_get(U, 1);
  double theta_r = gsl_vector_get(U, 2);
        
  gsl_vector_set(U_new,U->size, x_r + measurement_r*cos(measurement_phi + theta_r));
  gsl_vector_set(U_new,U->size+1, y_r + measurement_r*sin(measurement_phi + theta_r));
  gsl_vector_set(U_new,U->size+2, measurement_signature);
  
  return U_new;
}

gsl_matrix* EKF2D_addnewfeature_cov(gsl_vector* measurement, gsl_matrix* measurement_covariance,
				    gsl_vector* U, gsl_matrix* SIGMA){

  //measurement_r, measurement_phi, measurement_signature = measurement[:,0]
  double measurement_r = gsl_vector_get(measurement, 0);
  double measurement_phi = gsl_vector_get(measurement, 1);
  //double measurement_signature = gsl_vector_get(measurement, 2);
  
  size_t curr_size = U->size;

  //make some new matrices and copy the old ones over
  /*printf("u_size:%d\n", U->size);
    printf("curr_size:%d\n", curr_size);*/
  //printf("sig_size:%d\n", SIGMA->size1);
  gsl_matrix *SIGMA_new = gsl_matrix_alloc(curr_size+3, curr_size+3);
  
  //SIGtmp[0:curr_size,0:curr_size] = self.SIGMA;
  //printf("curr_size:%d\n", curr_size);
  gsl_matrix_view SIGMAtmp = gsl_matrix_submatrix(SIGMA_new, 0, 0, curr_size, curr_size);
  //printf("SIGtmp:%d -- SIGMA:%d\n", (&SIGMAtmp.matrix)->size1, SIGMA->size1);
  gsl_matrix_memcpy(&SIGMAtmp.matrix, SIGMA);
  
  double theta_r = gsl_vector_get(U, 2);
  
  //#get the Jacobian wrt the state
  //zeros([3,curr_size])*1.0;
  gsl_matrix *Gx = gsl_matrix_calloc(3, curr_size);
  gsl_matrix_set(Gx,0,0,1.0);
  gsl_matrix_set(Gx,0,2,-measurement_r*sin(measurement_phi + theta_r));
  gsl_matrix_set(Gx,1,1,1.0);
  gsl_matrix_set(Gx,1,2,measurement_r*cos(measurement_phi + theta_r));


  //#get the Jacobian wrt the measurement
  //Gy = zeros([3,3])*1.0
  gsl_matrix *Gy = gsl_matrix_calloc(3, 3);
  gsl_matrix_set(Gy,0,0,cos(measurement_phi + theta_r));
  gsl_matrix_set(Gy,0,1,-measurement_r*sin(measurement_phi + theta_r));
  gsl_matrix_set(Gy,1,0,sin(measurement_phi+theta_r));
  gsl_matrix_set(Gy,1,1,measurement_r*cos(measurement_phi + theta_r));
  gsl_matrix_set(Gy,2,2,1.0);


  //#compute the new values for the covariance matrix
  gsl_matrix* W = measurement_covariance;

  
  //A = matrixmultiply(matrixmultiply(Gx, self.SIGMA), transpose(Gx)) 
  //           + matrixmultiply(matrixmultiply(Gy, W), transpose(Gy));
  gsl_matrix* A = gsl_matrix_alloc(3, 3);
  gsl_matrix* B = gsl_matrix_alloc(3, curr_size);
  gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, Gx, SIGMA, 0.0, B);
  gsl_blas_dgemm(CblasNoTrans, CblasTrans, 1.0, B, Gx, 0.0, A);


  gsl_matrix* A2 = gsl_matrix_alloc(3, 3);
  gsl_matrix* A2_1 = gsl_matrix_alloc(3, 3);
  gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, Gy, W, 0.0, A2);
  gsl_blas_dgemm(CblasNoTrans, CblasTrans, 1.0, A2, Gy, 0.0, A2_1);



  gsl_matrix_add(A, A2_1);

  //SIGtmp[curr_size:curr_size+3,curr_size:curr_size+3] = A;
  gsl_matrix_view A_view = gsl_matrix_submatrix(SIGMA_new, curr_size, curr_size, 3, 3);
  gsl_matrix_memcpy(&A_view.matrix, A);

  //SIGtmp[curr_size:curr_size+3,0:curr_size] = B;
  gsl_matrix_view B_view = gsl_matrix_submatrix(SIGMA_new, curr_size, 0, 3, curr_size);
  gsl_matrix_memcpy(&B_view.matrix, B);
  

  //SIGtmp[0:curr_size,curr_size:curr_size+3] = transpose(B);
  gsl_matrix *B_transpose = gsl_matrix_alloc(curr_size, 3);
  gsl_matrix_transpose_memcpy(B_transpose, B);
  gsl_matrix_view B_trans_view = gsl_matrix_submatrix(SIGMA_new, 0, curr_size, curr_size, 3);
  gsl_matrix_memcpy(&B_trans_view.matrix, B_transpose);


  //#add the initial values to the covariance matrix
  //printf("SIGnew:%d\n", SIGMA_new->size1);

  gsl_matrix_free(Gx);
  gsl_matrix_free(Gy);
  gsl_matrix_free(A);
  gsl_matrix_free(B);
  gsl_matrix_free(A2);
  gsl_matrix_free(A2_1);
  gsl_matrix_free(B_transpose);
  return SIGMA_new;
  //self.SIGMA = SIGMA_new;
  //  self.U = U_new;
}


EKF2D_filter_state * EKF2D_measurement_update(gsl_matrix* measurements, 
					      gsl_matrix* measurement_covariance, 
					      double alpha, gsl_vector* U, gsl_matrix* SIGMA){
  //noise_model = self.sensor_error_model 
  //Q = noise_model.getvariance()

  EKF2D_filter_state *ret_state = (EKF2D_filter_state *)calloc(1, sizeof(EKF2D_filter_state));  
  
  //if there is no state, don't update it
  if(U == NULL || SIGMA == NULL)
    return NULL;

  gsl_vector* U_new = gsl_vector_alloc(U->size);
  gsl_matrix* SIGMA_new = gsl_matrix_alloc(U->size, U->size);
  
  //if there are no measurements just return the previous value
  if(measurements == NULL){
    gsl_vector_memcpy(U_new, U);
    gsl_matrix_memcpy(SIGMA_new, SIGMA);
    ret_state->U = U_new;
    ret_state->SIGMA = SIGMA_new;
    ret_state->associations = NULL;
    return ret_state;
  }
  
  gsl_matrix* Q = measurement_covariance;

  size_t i, k;
  int myindex;

  gsl_matrix_memcpy(SIGMA_new, SIGMA);
  gsl_vector_memcpy(U_new, U);
  
  
  gsl_vector *associations = gsl_vector_calloc(measurements->size2);

  //other intermediate structs
  gsl_vector *z_hat = gsl_vector_alloc(3);  
  gsl_matrix* J = gsl_matrix_calloc(3, 6);
  gsl_vector* gain = gsl_vector_alloc(3);
  gsl_matrix* psi_k = gsl_matrix_alloc(3, 3);
  
  //decide the association
  gsl_vector* min_gain = gsl_vector_calloc(3);
  gsl_matrix* min_inv_psi_k = gsl_matrix_alloc(3, 3);
  
  //for the inverse bit
  
  gsl_matrix* LU_cov = gsl_matrix_calloc(3, 3);
  gsl_matrix* psi_k_inv = gsl_matrix_calloc(3, 3);
  gsl_vector* mah_tmp = gsl_vector_alloc(3);  
  
  double measurement_r, measurement_phi, measurement_signature;
  double delta_kx, delta_ky, q_k;
  for(i=0;i<measurements->size2;i++){
    //printf("---------ver C---------\n");
    int num_landmarks = EKF2D_get_num_features(U_new);
    gsl_vector* curr_pose = EKF2D_getpose(U_new);

    double curr_pose_x = gsl_vector_get(curr_pose, 0);
    double curr_pose_y = gsl_vector_get(curr_pose, 1);
    double curr_pose_theta = gsl_vector_get(curr_pose, 2);


    gsl_matrix* H = gsl_matrix_calloc(3, U_new->size);
    gsl_matrix* HSIG_tmp = gsl_matrix_calloc(3, U_new->size);  
    gsl_matrix* min_H_k = gsl_matrix_calloc(3, U_new->size);
    
    //kalman gain
    gsl_matrix *K = gsl_matrix_alloc(U_new->size, 3);
    gsl_matrix *K_tmp = gsl_matrix_alloc(U_new->size, 3);
    
    //I
    gsl_matrix *I = tklib_eye(U_new->size, U_new->size);
    gsl_matrix *Innovation = gsl_matrix_alloc(U_new->size, U_new->size);
    gsl_matrix* SIGMA_new_tmp = gsl_matrix_alloc(U_new->size, U_new->size);
    gsl_vector *U_update = gsl_vector_alloc(U_new->size);
    int min_association = -1;
    double min_association_value = alpha;

    //z = transpose([measurements[:,i]]) 
    gsl_vector_view z = gsl_matrix_column(measurements, i);
    measurement_r = gsl_vector_get(&z.vector, 0);
    measurement_phi = gsl_vector_get(&z.vector, 1);
    measurement_signature = gsl_vector_get(&z.vector, 2);

    //assoc = [];
    //invcov = [];

    //printf("mav: %f ", min_association_value);
    for(k=0;k<(size_t)num_landmarks;k++){
      gsl_matrix* F = gsl_matrix_calloc(6, U_new->size);
      gsl_vector_view feat = EKF2D_getfeature_view(k, U_new);
      
      delta_kx = gsl_vector_get(&feat.vector,0)-curr_pose_x;
      delta_ky = gsl_vector_get(&feat.vector,1)-curr_pose_y;
      q_k = delta_kx*delta_kx + delta_ky*delta_ky;
      
      //printf("d_kx %f, d_ky %f, q_k %f\n", delta_kx, delta_ky, q_k);
      gsl_vector_set(z_hat, 0, sqrt(q_k));
      gsl_vector_set(z_hat, 1, tklib_normalize_theta(atan2(delta_ky, delta_kx)-curr_pose_theta));
      gsl_vector_set(z_hat, 2, gsl_vector_get(&feat.vector, 2));
      
      //J  = zeros([3, 6])*1.0;
      //First row
      gsl_matrix_set(J,0,0, -sqrt(q_k)*delta_kx);
      gsl_matrix_set(J,0,1, -sqrt(q_k)*delta_ky);
      gsl_matrix_set(J,0,3, sqrt(q_k)*delta_kx);
      gsl_matrix_set(J,0,4, sqrt(q_k)*delta_ky);
      //Second row
      gsl_matrix_set(J,1,0, delta_ky);
      gsl_matrix_set(J,1,1, -delta_kx);
      gsl_matrix_set(J,1,2, -q_k);
      gsl_matrix_set(J,1,3, -delta_ky);
      gsl_matrix_set(J,1,4, delta_kx);
      //Third row
      gsl_matrix_set(J,2,5, q_k);
      
      //printf("J\n");
      //tklib_matrix_printf(J);
      //create F
      //F = zeros([6, len(self.U)])*1.0;
      gsl_matrix_set_zero(F);
      gsl_matrix_set(F,0,0, 1.0);
      gsl_matrix_set(F,1,1, 1.0);
      gsl_matrix_set(F,2,2, 1.0);
      myindex = EKF2D_get_feature_index_in_state(k);
      gsl_matrix_set(F,3,myindex, 1.0);
      gsl_matrix_set(F,4,myindex+1, 1.0);
      gsl_matrix_set(F,5,myindex+2, 1.0);

      //H = (1.0/q_k) *matrixmultiply(J, F);
      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, J, F, 0.0, H);
      gsl_matrix_scale(H, 1.0/q_k);
      
      //psi_k = matrixmultiply(matrixmultiply(H, self.SIGMA), transpose(H)) + Q;
      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, H, SIGMA_new, 0.0, HSIG_tmp);
      gsl_blas_dgemm(CblasNoTrans, CblasTrans, 1.0, HSIG_tmp, H, 0.0, psi_k);
      gsl_matrix_add(psi_k, Q);

      //gain = z - z_hat;
      gsl_vector_memcpy(gain, &z.vector);
      gsl_vector_sub(gain, z_hat);
      
      //gain[1][0] = normalize_theta(gain[1][0]);      
      gsl_vector_set(gain, 1, tklib_normalize_theta(gsl_vector_get(gain, 1)));
      

      //psi_k_inv = inv(psi_k);
      //get the inverse covariance matrix
      int signum;
      gsl_permutation* p_cov = gsl_permutation_calloc(3);
      
      gsl_matrix_memcpy(LU_cov, psi_k);
      gsl_linalg_LU_decomp(LU_cov, p_cov, &signum);
      
      //perform the inverse covariance
      gsl_linalg_LU_invert(LU_cov, p_cov, psi_k_inv);
      
      double pi_k;
      //pi_k = squeeze(matrixmultiply(matrixmultiply(transpose(gain), psi_k_inv), gain));
      gsl_blas_dgemv(CblasNoTrans, 1.0, psi_k_inv, gain, 0.0, mah_tmp);
      gsl_blas_ddot(mah_tmp, gain, &pi_k);

      ///*assoc.append(alpha);
      //j = argmin(assoc);
      //printf("v%d %f ", k, pi_k);

      if(pi_k < min_association_value){
	min_association = k;
	min_association_value = pi_k;
	//gsl_vector_memcpy(min_z_k, &z.vector);
	gsl_vector_memcpy(min_gain, gain);
	gsl_matrix_memcpy(min_H_k, H);
	gsl_matrix_memcpy(min_inv_psi_k, psi_k_inv);
      }
      gsl_matrix_free(F);
      gsl_permutation_free(p_cov);
    }

    //printf(" Cma:%d", min_association);
    
    if(min_association < 0){
      //printf("6666666ADDING Feature666666666\n");
      //memory leak here
      //gsl_matrix_free(U_new);
      //gsl_matrix_free(SIGMA_new);
      //printf("********************************\n");
      gsl_vector* U_new_tmp = EKF2D_addnewfeature_mean(&z.vector, U_new);
      
      //EKF_2D_addnewfeature(z, noise_model);
      gsl_matrix* SIGMA_new2 = EKF2D_addnewfeature_cov(&z.vector, Q, U_new, SIGMA_new);

      gsl_vector_free(U_new);
      gsl_matrix_free(SIGMA_new);
      

      U_new = U_new_tmp;
      SIGMA_new = SIGMA_new2;
    }
    else{
      //printf("6666666Updating Feature666666666\n");
      //H_k, psi_k_inv, z_k = invcov[j];
      //K = matrixmultiply(matrixmultiply(self.SIGMA, transpose(H_k)), psi_k_inv);
      gsl_blas_dgemm(CblasNoTrans, CblasTrans, 1.0, SIGMA_new, min_H_k, 0.0, K_tmp);
      //gsl_matrix_memcpy(min_inv_psi_k, psi_k_inv);
      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, K_tmp, min_inv_psi_k, 0.0, K);

      //self.U = self.U + squeeze(matrixmultiply(K, gain));

      gsl_blas_dgemv(CblasNoTrans, 1.0, K, min_gain, 0.0, U_update);
      gsl_vector_add(U_new, U_update);
      
      //self.SIGMA = matrixmultiply(eye(len(self.U))*1.0 - matrixmultiply(K, H_k), self.SIGMA);
      
      /*printf("K %d %d \n", K->size1, K->size2);
      printf("minH_k %d %d \n", min_H_k->size1, min_H_k->size2);
      printf("Innovation %d %d \n", Innovation->size1, Innovation->size2);*/
      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, K, min_H_k, 0.0, Innovation);
      gsl_matrix_sub(I, Innovation);
      /*printf("I %d %d \n", I->size1, I->size2);
      printf("SIGMA_new %d %d \n", SIGMA_new->size1, SIGMA_new->size2);
      printf("SIGMA_new_tmp %d %d \n", SIGMA_new_tmp->size1, SIGMA_new_tmp->size2);*/
      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, I, SIGMA_new, 0.0, SIGMA_new_tmp);
            
      //swap the pointers
      gsl_matrix* tmp = SIGMA_new;


      SIGMA_new = SIGMA_new_tmp;
      SIGMA_new_tmp = tmp;


    }
    gsl_vector_set(associations, i, min_association);
    gsl_vector_free(U_update);
    gsl_vector_free(curr_pose);    

    gsl_matrix_free(H);
    gsl_matrix_free(HSIG_tmp);
    gsl_matrix_free(min_H_k);
    gsl_matrix_free(K);
    gsl_matrix_free(K_tmp);
    gsl_matrix_free(I);
    gsl_matrix_free(Innovation);
    gsl_matrix_free(SIGMA_new_tmp);
  }
  //printf("\n");
  gsl_matrix_free(LU_cov);
  gsl_vector_free(z_hat);
  gsl_matrix_free(J);
  gsl_vector_free(gain);
  gsl_matrix_free(psi_k);
  gsl_matrix_free(psi_k_inv);
  
  //decide the association
  gsl_vector_free(min_gain);
  gsl_matrix_free(min_inv_psi_k);

  gsl_vector_free(mah_tmp);

  ret_state->U = U_new;
  ret_state->SIGMA = SIGMA_new;
  ret_state->associations = associations;
  //printf("SIGMA:");
  //tklib_matrix_printf(ret_state->SIGMA);
  return ret_state;
  //return SIGMA_new_tmp
}



gsl_matrix* EKF2D_get_measurement_jacobian(int assoc, gsl_vector* U){
					   //gsl_matrix* measurement_noise_covariance){

  //gsl_matrix* Q = measurement_noise_covariance;

  //get the current estimated pose and feature values
  gsl_vector* curr_pose = EKF2D_getpose(U);
  gsl_vector* feat =  EKF2D_getfeature(assoc, U);
  
  //create delta_k
  gsl_vector* delta_k = gsl_vector_alloc(2);
  gsl_vector_set(delta_k, 0, gsl_vector_get(feat,0)-gsl_vector_get(curr_pose, 0));
  gsl_vector_set(delta_k, 1, gsl_vector_get(feat,1)-gsl_vector_get(curr_pose, 1));

  
  double q_k = 0.0; 
  gsl_blas_ddot(delta_k, delta_k, &q_k);
  
  gsl_matrix* J  = gsl_matrix_calloc(3, 6);
  //#First row
  gsl_matrix_set(J, 0, 0, -1.0*sqrt(q_k)*gsl_vector_get(delta_k,0));
  gsl_matrix_set(J, 0, 1, -1.0*sqrt(q_k)*gsl_vector_get(delta_k,1));
  gsl_matrix_set(J, 0, 3, sqrt(q_k)*gsl_vector_get(delta_k,0));
  gsl_matrix_set(J, 0, 4, sqrt(q_k)*gsl_vector_get(delta_k, 1));
  //#Second row
  gsl_matrix_set(J, 1, 0, gsl_vector_get(delta_k, 1));
  gsl_matrix_set(J, 1, 1, -1.0*gsl_vector_get(delta_k,0));
  gsl_matrix_set(J, 1, 2, -1.0*q_k);
  gsl_matrix_set(J, 1, 3, -1.0*gsl_vector_get(delta_k,1));
  gsl_matrix_set(J, 1, 4, gsl_vector_get(delta_k, 0));
  //#Third row
  gsl_matrix_set(J, 2, 5, q_k);
  
  //fprintf(stderr, "J\n");
  //tklib_matrix_printf(J);
  
  //#create F
  gsl_matrix* F = gsl_matrix_calloc(6,U->size);

  //#F = zeros([6, len(self.U)])*1.0;
  gsl_matrix_set(F,0,0,1.0);
  gsl_matrix_set(F,1,1,1.0);
  gsl_matrix_set(F,2,2,1.0);
  int myindex = EKF2D_get_feature_index_in_state(assoc);
  gsl_matrix_set(F,3,myindex,1.0);
  gsl_matrix_set(F,4,myindex+1,1.0);
  gsl_matrix_set(F,5,myindex+2,1.0);

  //fprintf(stderr, "F\n");
  //tklib_matrix_printf(F);

  //fprintf(stderr, "q_k %f\n", q_k);

  if(q_k == 0.0)
    q_k = 0.0001;
  gsl_matrix* H = gsl_matrix_calloc(3, U->size);
  gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0/(q_k*1.0), J, F, 0.0, H);

  gsl_vector_free(curr_pose);
  gsl_vector_free(feat);
  gsl_vector_free(delta_k);
  gsl_matrix_free(J);
  gsl_matrix_free(F);
  return H;
}


//note that R = VWVt
gsl_matrix * EKF2D_get_transfer_function(gsl_matrix* measurements,
					 gsl_matrix* measurement_noise, 
					 gsl_matrix* motion_jacobian,
                                         gsl_matrix* motion_noise, 
					 gsl_matrix* motion_jacobian_zero,
					 gsl_matrix* motion_noise_zero, 
					 double alpha, gsl_vector* U, gsl_matrix* SIGMA){
  /*fprintf(stderr, "starting function\n");
  measurements = measurements;
  measurement_noise = measurement_noise;
  motion_jacobian = motion_jacobian;

  return NULL;*/

  //#compute the motion update for the true motion
  //#   note here that the measurement updates
  //#   and the motion updates will
  //#   be of different sizes
  //#   all of these variables are now sparse
  gsl_matrix* G = motion_jacobian;
  gsl_matrix* R = motion_noise;
  gsl_matrix* G_inv_tr = tklib_inverse(G);
  gsl_matrix_transpose(G_inv_tr);  
  //gsl_matrix_transpose(G);  

  gsl_matrix* G_zero = motion_jacobian_zero;
  gsl_matrix* R_zero = motion_noise_zero;
  gsl_matrix* G_inv_tr_zero = tklib_inverse(G_zero);
  gsl_matrix_transpose(G_inv_tr_zero);  
  //gsl_matrix_transpose(G_zero);  

  int n = U->size;
  gsl_matrix* t_curr = gsl_matrix_calloc(2*U->size, 2*U->size);
  gsl_matrix* t_curr_tmp = gsl_matrix_calloc(2*U->size, 2*U->size);
  //Hs, Q = myEKF.measurement_updateC(measurement, 30.0);
  // fix me 

  //fprintf(stderr, "starting to get transfer function\n");
  if(measurements == NULL){

    //    fprintf(stderr, "start null\n");
    //retT[0:n,0:n]=G.todense();    
    gsl_matrix_view Tc_1 = gsl_matrix_submatrix(t_curr, 0, 0, n, n);    
    gsl_matrix_memcpy(&Tc_1.matrix, G);

    //fprintf(stderr, "start1");
    //retT[0:n,n:2*n]=dot(R, inv_tr_G).todense();
    gsl_matrix* Tc_2tmp = gsl_matrix_calloc(n, n);
    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, R, G_inv_tr, 0.0, Tc_2tmp);
    gsl_matrix_view Tc_2 = gsl_matrix_submatrix(t_curr, 0, n, n, n);    
    gsl_matrix_memcpy(&Tc_2.matrix, Tc_2tmp);
    
    //fprintf(stderr, "start2");
    //retT[n:2*n,n:2*n]=inv_tr_G.todense();
    gsl_matrix_view Tc_3 = gsl_matrix_submatrix(t_curr, n, n, n, n);
    gsl_matrix_memcpy(&Tc_3.matrix, G_inv_tr);

    //fprintf(stderr, "done");
    gsl_matrix_free(G_inv_tr_zero);
    gsl_matrix_free(G_inv_tr);
    gsl_matrix_free(Tc_2tmp);
    
    return t_curr;
  }
  
  //fprintf(stderr, "there exist %d measurements\n", measurements->size2);
  //fprintf(stderr, "DOING ekf measurement update\n");
  EKF2D_filter_state* ekf_state = EKF2D_measurement_update(measurements, 
							   measurement_noise, 
							   alpha, U, SIGMA);
  //fprintf(stderr, "DONE ekf measurement update\n");
  gsl_vector* associations = ekf_state->associations;

  gsl_matrix* Q = measurement_noise;
  gsl_matrix* Q_inv = tklib_inverse(Q);
  
  //#if we don't get any measurements, then set
  //#    H=0 and return the update below
  
  //instance variables
  gsl_matrix* t_tmp = gsl_matrix_calloc(t_curr->size1, t_curr->size2);
  gsl_matrix* T2_3_tmp = gsl_matrix_calloc(n, n);
  gsl_matrix* T1 = gsl_matrix_calloc(2*n, 2*n);
  gsl_matrix* T2 = gsl_matrix_calloc(2*n, 2*n);  
  gsl_matrix* M = gsl_matrix_calloc(U->size, U->size);
  gsl_matrix* M_im = gsl_matrix_calloc(U->size, 3);


  //setup part of T1
  //T1[0:n, n:2*n] = identity(n)*1.0;
  gsl_matrix_view T1_1 = gsl_matrix_submatrix(T1, 0, n, n, n);
  gsl_matrix_set_identity(&T1_1.matrix);
  
  //T1[n:2*n, 0:n] = identity(n)*1.0;
  gsl_matrix_view T1_2 = gsl_matrix_submatrix(T1, n, 0, n, n);
  gsl_matrix_set_identity(&T1_2.matrix);

  gsl_matrix* G_curr = G;
  gsl_matrix* R_curr = R;
  gsl_matrix* G_inv_tr_curr = G_inv_tr;

  //fprintf(stderr, "creating transfer function\n");
  for(size_t i = 0; i<associations->size; i++){
    //fprintf(stderr, "i=%d\n", i);
    int assoc = (int)gsl_vector_get(associations, i);
    //fprintf(stderr, "get measurement jacobian\n");
    gsl_matrix* H_curr = EKF2D_get_measurement_jacobian(assoc, U);
    //fprintf(stderr, "done get measurement jacobian\n");
    gsl_matrix* H_curr_trans = gsl_matrix_calloc(H_curr->size2, H_curr->size1);  
    
    if(i > 0){
      G_curr = G_zero;
      R_curr = R_zero;
      G_inv_tr_curr = G_inv_tr_zero;
    }
    
    //#compute extra terms
    gsl_matrix_transpose_memcpy(H_curr_trans, H_curr);
    
    //compute M
    //fprintf(stderr, "getting M\n");
    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, H_curr_trans, Q_inv, 0.0, M_im);
    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, M_im, H_curr, 0.0, M);
    
    //#initialize some variables

    //#generate term1 and term2
    //T1[n:2*n, n:2*n] = M.todense();

    //fprintf(stderr, "getting T1\n");
    gsl_matrix_view T1_3 = gsl_matrix_submatrix(T1, n, n, n, n);
    gsl_matrix_memcpy(&T1_3.matrix, M);

    //fprintf(stderr, "getting T2\n");
    //T2[0:n, n:2*n] = inv_tr_G.todense();
    gsl_matrix_view T2_1 = gsl_matrix_submatrix(T2, 0, n, n, n);
    gsl_matrix_memcpy(&T2_1.matrix, G_inv_tr_curr);

    //T2[n:2*n, 0:n] = G.todense();
    gsl_matrix_view T2_2 = gsl_matrix_submatrix(T2, n, 0, n, n);
    gsl_matrix_memcpy(&T2_2.matrix, G_curr);

    //T2[n:2*n, n:2*n] = dot(R, inv_tr_G).todense();
    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, R_curr, G_inv_tr_curr, 0.0, T2_3_tmp);
    gsl_matrix_view T2_3 = gsl_matrix_submatrix(T2, n, n, n, n);
    gsl_matrix_memcpy(&T2_3.matrix, T2_3_tmp);

    //#compute the current term
    //t_curr = dot(sparse.lil_matrix(T1), sparse.lil_matrix(T2));
    //fprintf(stderr, "computing t_curr\n");
    
    //fprintf(stderr, "T1\n");
    //tklib_matrix_printf(T1);
    //fprintf(stderr, "T2\n");
    //tklib_matrix_printf(T2);

    if(i == 0){

      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, T1, T2, 0.0, t_curr);

    }
    //t_curr = dot(dot(sparse.lil_matrix(T1),
    //	       sparse.lil_matrix(T2)), t_curr);
    else{
      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, T1, T2, 0.0, t_tmp);
      gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, t_tmp, t_curr, 0.0, t_curr_tmp);
      gsl_matrix_memcpy(t_curr, t_curr_tmp);
    }
    gsl_matrix_free(H_curr);
    gsl_matrix_free(H_curr_trans);
  }
  
  gsl_matrix_free(ekf_state->SIGMA);
  gsl_vector_free(ekf_state->U);
  gsl_vector_free(ekf_state->associations);
  gsl_matrix_free(Q_inv);
  gsl_matrix_free(t_tmp);
  gsl_matrix_free(T2_3_tmp);
  gsl_matrix_free(T1);
  gsl_matrix_free(T2);
  gsl_matrix_free(M);
  gsl_matrix_free(M_im);
  return t_curr;
}
