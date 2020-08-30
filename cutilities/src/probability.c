#include "probability.h"
#include <assert.h>

//long myseed;
int rng_is_initialized=0;
const gsl_rng_type *T;
gsl_rng *r;


void tklib_initialize_rng(){
  time_t seed = time(NULL);
  
  gsl_rng_env_setup();
  T = gsl_rng_default;
  r = gsl_rng_alloc(T);
  gsl_rng_set(r, seed);
}

void tklib_init_rng(int seed){
  gsl_rng_env_setup();
  T = gsl_rng_default;
  r = gsl_rng_alloc(T);
  gsl_rng_set(r, seed);
  rng_is_initialized = 1;
}


gsl_vector* tklib_vector_random(int number){
  gsl_vector* rand_vec = gsl_vector_calloc(number);
  if(!rng_is_initialized){
    tklib_initialize_rng();
    rng_is_initialized=1;
  }

  int i;
  for(i = 0; i < number; i++){
    gsl_vector_set(rand_vec, i, gsl_rng_uniform(r));
  }

  return rand_vec;
}

gsl_vector* tklib_vector_randint(int number, int start, int end){
  gsl_vector* rand_vec = gsl_vector_calloc(number);
  if(!rng_is_initialized){
    tklib_initialize_rng();
    rng_is_initialized=1;
  }

  int i;
  for(i = 0; i < number; i++){
    gsl_vector_set(rand_vec, i, tklib_randint(start, end));
  }

  return rand_vec;
}

double tklib_random(){
  if(!rng_is_initialized){
    tklib_initialize_rng();
    rng_is_initialized=1;
  }

  double u = gsl_rng_uniform(r);
  return u;
}


double tklib_randn(){
  if(!rng_is_initialized){
    tklib_initialize_rng();
    rng_is_initialized=1;
  }

  double u = gsl_ran_gaussian(r, 1.0);
  return u;
}

gsl_vector* tklib_vector_randn(double mean, double std, int n){
  if(!rng_is_initialized){
    tklib_initialize_rng();
    rng_is_initialized=1;
  }
  
  //allocate the return vector
  gsl_vector* ret_vec = gsl_vector_alloc(n);
  
  //sample the values
  size_t i;
  for(i=0;i<(size_t)n;i++)
    gsl_vector_set(ret_vec, i, gsl_ran_gaussian(r, std));


  //set the mean
  gsl_vector_add_constant(ret_vec, mean);

  return ret_vec;
}


/*gsl_vector *tklib_vector_randn(int n){
  if(!rng_is_initialized){
    tklib_initialize_rng();
    rng_is_initialized=1;
  }

  size_t i;
  gsl_vector* ret_vec = gsl_vector_alloc(n);
  for(i=0;i<(size_t)n;i++)
    gsl_vector_set(ret_vec, i, gsl_ran_gaussian(r, 1.0));

  return ret_vec;
  }*/


int tklib_randint(int start, int end){
  double r = tklib_random();
  double span = (end-start)+1;
  int r_int = (int)floor(r*span) + start;
  
  return r_int;
}

gsl_vector* tklib_sample_discrete(gsl_vector* P, int number_of_samples){
  gsl_vector* indexes = gsl_vector_calloc(number_of_samples);

  //take care of the off by one units error
  //this could be optimized
  gsl_vector* cdf = gsl_vector_calloc(P->size + 1);
  gsl_vector_set(cdf, 0, -100000.0);
		 
  size_t i;
  double cum_prob = 0.0;
  for(i=0; i<P->size; i++){
    cum_prob += gsl_vector_get(P, i);
    gsl_vector_set(cdf, i+1, cum_prob);
  }

  //sample from it
  //fprintf(stderr, "random=%f\n", tklib_random());
  double u0 = tklib_random()*(1.0/number_of_samples);
  double uj = 0.0;
  i = 1;

  int j;
  
  //printf("cdf:\n");
  //tklib_vector_printf(cdf);
  for(j=1;j<number_of_samples+1;j++){

    uj = u0 + (1.0/number_of_samples)*(j-1);
    
    while(uj > gsl_vector_get(cdf, i)){
      i+=1;
    }
    
    //fprintf(stderr, "j=%d\n", j);
    gsl_vector_set(indexes, j-1, i-1);
  }

  gsl_vector_free(cdf);
  return indexes;
}

gsl_matrix* tklib_get_transition_matrix_maxprob(gsl_matrix* M, int num_steps){
  gsl_matrix* M_max = gsl_matrix_calloc(M->size1, M->size2);
  gsl_matrix_memcpy(M_max, M);

  if(num_steps == 0 || num_steps == 1)
    return M_max;

  gsl_matrix* M_conn = gsl_matrix_calloc(M->size1, M->size2);
  gsl_matrix_memcpy(M_conn, M);
  
  gsl_matrix* M_max_prev = gsl_matrix_calloc(M->size1, M->size2);
  gsl_matrix_memcpy(M_max_prev, M);

  size_t d = 0; size_t i = 0; size_t j = 0; size_t k = 0;
  for(d=0; d< (size_t)num_steps-1; d++){
    for(i=0; i<M->size1; i++){
      for(j=0; j< M->size2; j++){
	for(k=0; k< M->size2; k++){
	  double new_val = gsl_matrix_get(M_conn,i,j)*gsl_matrix_get(M,j,k);
	  
	  if(new_val > gsl_matrix_get(M_conn,i,k))
	    gsl_matrix_set(M_conn,i,k,new_val);
	  
	  if(new_val > 0){
	    //printf("index %d %d on path %d %d %d and max of %f and %f and %f\n", i,k, i,j,k, gsl_matrix_get(M_max_prev,i,k), gsl_matrix_get(M,j,k), gsl_matrix_get(M_max_prev,i,j));
	    double m_max = GSL_MAX(gsl_matrix_get(M_max_prev,i,j), gsl_matrix_get(M,j,k));
	    m_max = GSL_MAX(gsl_matrix_get(M_max_prev,i,k), m_max);
	    gsl_matrix_set(M_max,i,k,m_max);
	  }
	}
      }
    }
  }
  gsl_matrix_free(M_conn);
  gsl_matrix_free(M_max_prev);
  return M_max;
}




gsl_vector* tklib_du_get_path(gsl_matrix* parents, int state_idx, int time_idx) {
  if(parents == NULL)
    return NULL;
  if((size_t)state_idx >= parents->size1)
    return NULL;
  if((size_t)time_idx >= parents->size2)
    return NULL;
  
  
  //#get the final best index after applying the last
  //# transition 
  gsl_vector* curr_best_path = gsl_vector_calloc(time_idx+2);
  gsl_vector_set(curr_best_path, time_idx+1, state_idx);
  
  int i;
  for(i=time_idx; i >=0; i--){
    if(gsl_matrix_get(parents, gsl_vector_get(curr_best_path, i+1), i) <= -99) {
      gsl_vector_free(curr_best_path);
      return NULL;
    }
    
    int new_idx = gsl_matrix_get(parents, gsl_vector_get(curr_best_path, i+1), i);
    gsl_vector_set(curr_best_path, i, new_idx);
  }
  
  return curr_best_path;
}


gsl_vector* tklib_du_get_path_topN(gsl_matrix* parents_prev, gsl_matrix* parents_iN, int state_idx, int time_idx, int iN_idx, int N) {
  int i;
  int pos;
  
/*  tklib_matrix_printf(parents_prev);*/
/*  tklib_matrix_printf(parents_iN);*/
  
	//TODO must take in account the different structure of parents for topN
  if(parents_prev == NULL || parents_iN == NULL){
    printf("ERROR:parents_prev or parents_iN are NULL\n");
    return NULL;
  }
  if((size_t)state_idx >= parents_prev->size1){
    printf("ERROR:more state indexes than parents can hold\n");
    return NULL;  
  }

  if((size_t)time_idx >= (parents_prev->size2)/N){
    printf("ERROR:time index is bigger than parent_prev\n");
    return NULL;  
  }

  if(iN_idx >= N){
    printf("ERROR: iN_idx is %d >= N which is %d\n",iN_idx,N);
    return NULL;  
  }

  
  //#get the final best index after applying the last
  //# transition 
  gsl_vector* curr_best_path = gsl_vector_calloc(time_idx+2);

  gsl_vector_set(curr_best_path, time_idx+1, state_idx);

  pos=iN_idx;
  

  for(i=time_idx; i >=0; i--){
    if(pos<0 || gsl_matrix_get(parents_prev, gsl_vector_get(curr_best_path, i+1), i*N+pos) <= -99) {
      gsl_vector_free(curr_best_path);
/*      if(pos<0) printf("negative position\n");*/
/*      else printf("parent < -99\n");*/
      return NULL;
    }
      
    int new_idx = gsl_matrix_get(parents_prev, gsl_vector_get(curr_best_path, i+1), i*N+pos);
    int new_pos = gsl_matrix_get(parents_iN, gsl_vector_get(curr_best_path, i+1), i*N+pos); 
    pos = new_pos;
    gsl_vector_set(curr_best_path, i, new_idx);
  }
  
  return curr_best_path;
}

gsl_vector* tklib_du_get_mask(int vp1_i, int vp2_i, 
			      gsl_matrix* topo_i_to_location_mask, 
			      gsl_vector* vp_i_to_topo_i){
  gsl_vector* ret_vec = gsl_vector_calloc(topo_i_to_location_mask->size2);
  gsl_vector_view mymask = gsl_matrix_row(topo_i_to_location_mask, 
					  gsl_vector_get(vp_i_to_topo_i, vp1_i));
  
  gsl_vector_memcpy(ret_vec, &mymask.vector);
  gsl_vector_view mymask2 = gsl_matrix_row(topo_i_to_location_mask, 
					   gsl_vector_get(vp_i_to_topo_i, vp2_i));

  size_t i;
  for(i=0; i < (&mymask2.vector)->size; i++){
    double v = gsl_vector_get(&mymask2.vector, i);
    if(v > 0)
      gsl_vector_set(ret_vec, i, v);
  }

  return ret_vec;
}

gsl_matrix * tklib_du_lp_sr_array(size_t num_viewpoints,
				   gsl_vector* vp_i_to_topo_i,
				   gsl_matrix* SR_log_curr, 
				   gsl_vector* L_log_curr, 
				   gsl_vector* O_log_curr,
				   int num_topologies) {
  gsl_matrix* ret_mat = gsl_matrix_calloc(num_viewpoints, num_viewpoints);
  unsigned int vp1_i;
  for(vp1_i=0; vp1_i<num_viewpoints; vp1_i++){ 
    for(size_t vp2_i = 0; vp2_i<num_viewpoints; vp2_i++){ 
      double lp_sr =  tklib_du_lp_sr(vp1_i, vp2_i,
				     vp_i_to_topo_i,
				     SR_log_curr, 
				     L_log_curr, 
				     O_log_curr,
				     num_topologies);
      gsl_matrix_set(ret_mat, vp1_i, vp2_i, lp_sr);
    }
  }
  return ret_mat;
}

double tklib_du_lp_sr(int vp1_i, int vp2_i,
		      gsl_vector* vp_i_to_topo_i,
		      gsl_matrix* SR_log_curr, 
		      gsl_vector* L_log_curr, 
		      gsl_vector* O_log_curr,
		      int num_topologies) {
  if(O_log_curr == NULL)
    return log(1.0);
  else if(SR_log_curr == NULL || L_log_curr == NULL){
    return gsl_vector_get(O_log_curr, vp2_i);  
  }
  
  //get the index from the viewpoint to the topology index
  size_t topo1  = gsl_vector_get(vp_i_to_topo_i, vp1_i);
  size_t topo2  = gsl_vector_get(vp_i_to_topo_i, vp2_i);
  
  //get the spatial relation matrix (which was compressed to two dimensions)
  gsl_vector_view sr_view = gsl_matrix_row(SR_log_curr, topo1*num_topologies + topo2);
  
  gsl_vector * sr_vec = gsl_vector_calloc(sr_view.vector.size);
  gsl_vector_memcpy(sr_vec, &sr_view.vector);
  //in case there is exactly no option, give an option for staying put

  //this is probably good to do, but I'm not doing it because of the log probabilities
  //gsl_vector_add_constant(sr_vec, log(10e-6));
  
  //create the temporary vector
  gsl_vector* ret_vec = gsl_vector_calloc(SR_log_curr->size2);
  
  //do the relevant multiplication and summation and return
  gsl_vector_add(ret_vec, L_log_curr);

  //this is to allow the spatial relations to self transition
  gsl_vector_add(ret_vec, sr_vec);
  

  gsl_vector* ret_exp = tklib_vector_exp(ret_vec);

  int argmax = tklib_vector_argmax(ret_exp);
  //printf("modified lp sr\n");
  double lp_sr = log(gsl_vector_get(ret_exp, argmax));
  //double lp_sr = log(tklib_vector_sum(ret_exp));
  //int max_idx = tklib_vector_argmax(ret_exp);
  //lp_sr = log(gsl_vector_get(ret_exp, max_idx));
  lp_sr = lp_sr + gsl_vector_get(O_log_curr, vp2_i);

  gsl_vector_free(ret_exp);
  gsl_vector_free(ret_vec);
  gsl_vector_free(sr_vec);

  return lp_sr;
}


double tklib_du_lp_obs(int vp1_i, int vp2_i,
		       gsl_vector* vp_i_to_topo_i,
		       gsl_matrix* T_log_curr,
		       gsl_matrix* D_log_curr,
		       gsl_matrix* SR_log_curr, 
		       gsl_vector* L_log_curr, 
		       gsl_vector* O_log_curr,
		       int num_topologies) {

  double lp_obs = tklib_du_lp_sr(vp1_i, vp2_i, vp_i_to_topo_i, 
				 SR_log_curr, L_log_curr, O_log_curr,
				 num_topologies);

  if(T_log_curr != NULL) {
    lp_obs = lp_obs+gsl_matrix_get(T_log_curr,vp2_i,vp1_i);
  }

  if(D_log_curr != NULL) {
    lp_obs = lp_obs+gsl_matrix_get(D_log_curr, vp1_i, vp2_i);
  }
  
  return lp_obs;
}

double compute_p_path(gsl_vector* curr_path,
		      int vp2_i, int vp3_i,
		      gsl_vector* vp_i_to_topo_i,
		      gsl_matrix* path_lengths)
{

  if (curr_path == NULL || path_lengths == NULL) {
    return 1.0;
  }
  size_t p_i;
  double actual_path_length = 0;


  size_t first_vp_i = gsl_vector_get(curr_path, 0);

  size_t first_topo_i = gsl_vector_get(vp_i_to_topo_i,
				      first_vp_i);
  size_t last_vp_i = first_vp_i;
  size_t last_topo_i = first_topo_i;
  bool print;
  if (vp3_i == 160) {

    print = 1;
  } else {
    print = 0;
  }

  for(p_i = 1; p_i < curr_path->size; p_i++){
    size_t this_vp_i = gsl_vector_get(curr_path,p_i);
    size_t this_topo_i = gsl_vector_get(vp_i_to_topo_i, 
				       this_vp_i);

    actual_path_length += gsl_matrix_get(path_lengths, last_topo_i, this_topo_i);
    
    last_topo_i = this_topo_i;
    last_vp_i = this_vp_i;
  }

  size_t vp2_topo_i = gsl_vector_get(vp_i_to_topo_i, vp2_i);
  size_t vp3_topo_i = gsl_vector_get(vp_i_to_topo_i, vp3_i);


  actual_path_length += gsl_matrix_get(path_lengths, last_topo_i, vp2_topo_i);
  actual_path_length += gsl_matrix_get(path_lengths, vp2_topo_i, vp3_topo_i);


  double shortest_path_length = gsl_matrix_get(path_lengths, 
					       first_topo_i,
					       vp3_topo_i);

  // 8 to 40
  double p_path;
  if (actual_path_length - shortest_path_length > 5) {
    p_path = 1e-20;
  } else {
    p_path = 1;
  }


  return p_path;
}

bool compute_already_seen(gsl_vector* curr_path,
			  int vp_i, 
			  gsl_vector* vp_i_to_topo_i)
{
  if(curr_path !=NULL){
    //check if we've already seen a particular element
    size_t p_i;
    float topo1 = gsl_vector_get(vp_i_to_topo_i, vp_i);

    bool first_repetition_allowance_on = true;
    for(p_i = 0; p_i < curr_path->size; p_i++){
      float topo2 = gsl_vector_get(vp_i_to_topo_i, 
				   gsl_vector_get(curr_path,p_i));

      //allow repetition as long as it was only the same at the end
      if(topo1 != topo2 && first_repetition_allowance_on)
	first_repetition_allowance_on = false;
      
      //if the two topologies are the same and they weren't at the end of the
      //    path, then say we've already seen them
      if(topo1 == topo2 && !first_repetition_allowance_on)
	return true;
    }
  }
  return false;
}


/* This method checks the last 3 elements in the current path for
   repeated topological regions*/
bool compute_already_seen_topo(gsl_vector* curr_path,
			       int vp_i, 
			       gsl_vector* vp_i_to_topo_i)
{
  bool already_seen = false;
  if(curr_path !=NULL){
    gsl_vector * topo_path = gsl_vector_calloc(curr_path->size);
    size_t topo_path_i = 0;
    size_t path_i;


    //this gets the unique topologies from the full viewpoint path
    for(path_i = 0; path_i < curr_path->size; path_i++){
      //get the topological locations in the path
      float p_topo_i = gsl_vector_get(vp_i_to_topo_i, 
				      gsl_vector_get(curr_path, path_i));

      if (topo_path_i > 0) {
	float last_topo_i = gsl_vector_get(topo_path, topo_path_i - 1);
	if (last_topo_i != p_topo_i) {
	  gsl_vector_set(topo_path, topo_path_i, p_topo_i);
	  topo_path_i += 1;
	}
      } 
      else { 
	assert(topo_path_i == 0);
	gsl_vector_set(topo_path, topo_path_i, p_topo_i);
	topo_path_i += 1;
      }
    }

    //get the index of the relevant topology
    float topo1 = gsl_vector_get(vp_i_to_topo_i, vp_i);

    //this starts 3 from the end and prevents backtracking on these regions
    int backtrack_start = topo_path_i - 2;
    if (backtrack_start  < 0) {
      backtrack_start = 0;
    }

    //checks the last 3 elements for repeats
    for(path_i = backtrack_start; path_i < topo_path_i; path_i++) {
      float topo2 = gsl_vector_get(topo_path, path_i);
      if (topo1 == topo2) {
	already_seen = true;
      }
    }
    gsl_vector_free(topo_path);
  }
  return already_seen;

}
			  
			  


gsl_matrix* tklib_du_update_log(gsl_matrix* P_log_prev,
				gsl_matrix* myparents,
				gsl_matrix* used_epsilons,
				gsl_matrix* T_log_curr,
				gsl_matrix* SR_log_curr,
				gsl_matrix* D_log_curr,
				gsl_vector* L_log_curr,
				gsl_vector* O_log_curr, 
				gsl_vector* vp_i_to_topo_i, 
				gsl_matrix* topo_i_to_location_mask,
				gsl_matrix* path_lengths,
				int num_topologies,
				bool allow_multiple_sdcs_per_transition,
				bool sdc_is_epsilon,
				bool allow_backtracking,
				int max_epsilon_transitions
				) {
  
  gsl_matrix* ret_mat = gsl_matrix_calloc(P_log_prev->size1*2+1, P_log_prev->size2);
  gsl_matrix_view P_log_curr = gsl_matrix_submatrix(ret_mat, 0, 0, P_log_prev->size1, P_log_prev->size2);
  
  //copy over negative infinities
  gsl_matrix* log_P = tklib_log(&P_log_curr.matrix);
  gsl_matrix_memcpy(&P_log_curr.matrix, log_P);
  gsl_matrix_free(log_P);

  //keep track of the epsilons used
  gsl_matrix_view epsilons = gsl_matrix_submatrix(ret_mat, P_log_prev->size1, 0,
						  P_log_prev->size1, P_log_prev->size2);

  gsl_vector_view parents = gsl_matrix_row(ret_mat, P_log_prev->size1*2);
  gsl_vector_add_constant(&parents.vector, -100.0);

  gsl_vector* L_log_reduced = NULL;
  if(L_log_curr != NULL)
    L_log_reduced = gsl_vector_calloc(L_log_curr->size);


  size_t num_viewpoints = vp_i_to_topo_i->size;
  size_t vp1_i;

  for(vp1_i=0; vp1_i<num_viewpoints; vp1_i++){ 
    size_t vp2_i;
    gsl_vector* curr_path =  NULL;
    if(myparents != NULL)
      curr_path = tklib_du_get_path(myparents, vp1_i, myparents->size2-1);
    
    for(vp2_i = 0; vp2_i<num_viewpoints; vp2_i++){  
      size_t vp3_i;
      for(vp3_i=0; vp3_i<num_viewpoints; vp3_i++){ 
	if((T_log_curr != NULL and gsl_matrix_get(T_log_curr,vp3_i,vp2_i) == GSL_NEGINF) ||
	   gsl_matrix_get(P_log_prev,vp1_i,vp2_i) == GSL_NEGINF || 
	   (D_log_curr != NULL and gsl_matrix_get(D_log_curr,vp2_i,vp3_i) == GSL_NEGINF))
	  continue;
	
	//reduce the possible ground object locations when filtering by 
	//    the topo_to_location mask
	if (L_log_curr != NULL) {
	  gsl_vector_memcpy(L_log_reduced, L_log_curr);

          if (topo_i_to_location_mask != NULL) {
            
            gsl_vector_view v2mask = gsl_matrix_row(topo_i_to_location_mask, 
                                                    gsl_vector_get(vp_i_to_topo_i, vp2_i));
            
            gsl_vector_view v3mask = gsl_matrix_row(topo_i_to_location_mask, 
                                                    gsl_vector_get(vp_i_to_topo_i, vp3_i));
            gsl_vector * mask = gsl_vector_calloc(v2mask.vector.size);
            tklib_vector_union(&v2mask.vector, &v3mask.vector, mask);
            tklib_apply_mask_lp(mask, L_log_reduced, L_log_reduced);
            gsl_vector_free(mask);
          }
	}
	//compute the observation probability using things in the future
	double lp_obs = tklib_du_lp_obs(vp2_i, vp3_i, 
					vp_i_to_topo_i, 
					T_log_curr, D_log_curr,
					SR_log_curr, L_log_reduced, 
					O_log_curr, num_topologies);
	
	//double p_path = compute_p_path(curr_path, vp2_i, vp3_i, vp_i_to_topo_i, path_lengths);
	//p_obs += log(p_path);


	//apply the transition matrix only if it is not null


	if (max_epsilon_transitions != -1) {
	  int vpb_i = vp2_i;
	  size_t p_i;
	  int epsilon_count = 0;

	  if (used_epsilons != NULL && curr_path != NULL) {
	    for(p_i = 0; p_i < curr_path->size; p_i++){
	      int vpa_i = gsl_vector_get(curr_path, curr_path->size - p_i - 1);

	      //int time = curr_path->size - p_i;
	      int idx1 = p_i *num_viewpoints + vpa_i;
	      int idx2 = vpb_i;
	      bool uses_epsilon = gsl_matrix_get(used_epsilons, idx1, idx2);
	      if (uses_epsilon) {
		epsilon_count += 1;
	      }
	      vpb_i = vpa_i;
	    }
	  }
	  if (epsilon_count > max_epsilon_transitions) {
	    if (sdc_is_epsilon && vp2_i != vp3_i) {
 	      lp_obs = log(10e-30);
 	    }
 	  }
	}

	// if the sdc applies better in the recent past, then do a self transition. 
	if (vp2_i == vp3_i && curr_path != NULL && allow_multiple_sdcs_per_transition) {
	  int vpb_i = vp2_i;
	  size_t p_i;
          for(p_i = 0; p_i < curr_path->size; p_i++){
            int vpa_i = gsl_vector_get(curr_path, curr_path->size - p_i - 1);
	    double last_lp_obs = tklib_du_lp_obs(vpa_i, vpb_i, 
						 vp_i_to_topo_i, 
						 T_log_curr, D_log_curr,
						 SR_log_curr, L_log_reduced, 
						 O_log_curr, num_topologies);

	    if (last_lp_obs >= lp_obs) {
	      lp_obs = last_lp_obs;
	    }
	    vpb_i = vpa_i;
	    if (p_i >= 2) {
	      break;
	    }
	  }
	}
	
	//printf("p before addition:%f\n", p_obs);
	double lp_new = gsl_matrix_get(P_log_prev,vp1_i,vp2_i)+lp_obs;
	
	//bool already_seen = compute_already_seen_topo(curr_path, vp2_i, vp_i_to_topo_i);
	bool already_seen = compute_already_seen(curr_path, vp2_i, vp_i_to_topo_i);

	// allow self transitions
	if (vp1_i == vp2_i) {
	  already_seen = false;
	}



	/*float topo1 = gsl_vector_get(vp_i_to_topo_i, vp2_i);
	float topo2 = gsl_vector_get(vp_i_to_topo_i, vp1_i);
	if(topo1 == topo2)
	already_seen = false;*/
	
	if (allow_backtracking) {
	  already_seen = false;
	}
	//if(already_seen == true)
	//  printf("already seen == true\n");
	//double p_trans = gsl_matrix_get(T_curr, vp3_i, vp2_i);

	
	if(lp_new > gsl_matrix_get(&P_log_curr.matrix,vp2_i,vp3_i) && !already_seen){
	  gsl_matrix_set(&P_log_curr.matrix, vp2_i, vp3_i, lp_new);
	  gsl_vector_set(&parents.vector, vp2_i, vp1_i);
	  
	  if (sdc_is_epsilon) {
	    if (vp2_i == vp3_i) {
	      gsl_matrix_set(&epsilons.matrix, vp2_i, vp3_i, false);
	    } else {
	      gsl_matrix_set(&epsilons.matrix, vp2_i, vp3_i, true);
	    }
	  } else {
	    gsl_matrix_set(&epsilons.matrix, vp2_i, vp3_i, false);
	  }
	}
      }
    }
    if(curr_path != NULL)
      gsl_vector_free(curr_path);
  }
  
  if(L_log_reduced != NULL)
    gsl_vector_free(L_log_reduced);
  
  return ret_mat;
}

//Dimitar: P_log_prev will become a matrix N times bigger than before
gsl_matrix* tklib_du_update_log_topN(gsl_matrix* P_log_prev,
						    gsl_matrix* myparents_prev,
						    gsl_matrix* myparents_iN,				    
						    gsl_matrix* used_epsilons,
						    gsl_matrix* T_log_curr,
						    gsl_matrix* SR_log_curr,
						    gsl_matrix* D_log_curr,
						    gsl_vector* L_log_curr,
						    gsl_vector* O_log_curr, 
						    gsl_vector* vp_index_to_topo_index, 
						    gsl_matrix* topo_i_to_location_mask,
						    int num_topologies,
						    bool allow_multiple_sdcs_per_transition,
						    bool sdc_is_epsilon,
						    bool allow_backtracking,
						    int max_epsilon_transitions,
						    int N
						    ){

  int num_states = P_log_prev->size2;
  
  //bigger ret_mat !
  gsl_matrix* ret_mat = gsl_matrix_calloc(P_log_prev->size1 + num_states + 2*N, num_states);
  // assuming N<50
  // assuming P_log_prev->size1 is N times bigger than size2
  gsl_matrix_view P_log_curr[50];
  int iN;
  for(iN=0;iN<N;iN++){
  	P_log_curr[iN] = gsl_matrix_submatrix(ret_mat, 0+iN*num_states, 0, num_states, num_states);
  }
  
  //copy over negative infinities
  for(iN=0;iN<N;iN++){
  	gsl_matrix* log_P = tklib_log(&P_log_curr[iN].matrix);
	  gsl_matrix_memcpy(&P_log_curr[iN].matrix, log_P);
	  gsl_matrix_free(log_P);
  }
  
  //keep track of the epsilons used
  gsl_matrix_view epsilons = gsl_matrix_submatrix(ret_mat, P_log_prev->size1, 0,
						  num_states, num_states);


  //make parents into a matrix, last N rows of ret_mat
  gsl_matrix_view parents_prev = gsl_matrix_submatrix(ret_mat, P_log_prev->size1+num_states, 0, N, num_states);
  gsl_matrix_view parents_iN = gsl_matrix_submatrix(ret_mat, P_log_prev->size1+num_states+N, 0, N, num_states);
  gsl_matrix_add_constant(&parents_prev.matrix, -100.0);
  gsl_matrix_add_constant(&parents_iN.matrix, -1.0);

  gsl_vector* L_log_reduced = NULL;
  if(L_log_curr != NULL)
    L_log_reduced = gsl_vector_calloc(L_log_curr->size);
    
  size_t num_viewpoints = vp_index_to_topo_index->size;

  size_t vp1_i;
  for(vp1_i = 0; vp1_i<num_viewpoints; vp1_i++){   
  	  	
    //for i = 1 to N
    int N_i;
    for(N_i=0; N_i<N; N_i++){
      gsl_vector* curr_path =  NULL;
      if(myparents_prev != NULL && myparents_iN != NULL){
        curr_path = tklib_du_get_path_topN(myparents_prev, myparents_iN, 
					   vp1_i, (int)(myparents_prev->size2/N)-1, N_i, N);
	if(curr_path == NULL) continue;
      }
        
      size_t vp2_i;
      for(vp2_i = 0; vp2_i<num_viewpoints; vp2_i++){  
        
        size_t vp3_i;
        for(vp3_i = 0; vp3_i<num_viewpoints; vp3_i++){
            
        //Check if variables are defined and good.
		    if((T_log_curr != NULL and gsl_matrix_get(T_log_curr,vp3_i,vp2_i) == GSL_NEGINF) ||
		       gsl_matrix_get(P_log_prev,vp1_i+N_i*num_states,vp2_i) == GSL_NEGINF || 
		       (D_log_curr != NULL and gsl_matrix_get(D_log_curr,vp2_i,vp3_i) == GSL_NEGINF))
		      continue;
		    //reduce the possible ground object locations when filtering by 
		    //    the topo_to_location mask
		    if(L_log_reduced != NULL && topo_i_to_location_mask != NULL){      
		      gsl_vector_memcpy(L_log_reduced, L_log_curr);
		      gsl_vector_view v2mask = gsl_matrix_row(topo_i_to_location_mask, 
							      gsl_vector_get(vp_index_to_topo_index, vp2_i));
		      gsl_vector_view v3mask = gsl_matrix_row(topo_i_to_location_mask, 
							      gsl_vector_get(vp_index_to_topo_index, vp3_i));
		      gsl_vector * mask = gsl_vector_calloc(v2mask.vector.size);
		      tklib_vector_union(&v2mask.vector, &v3mask.vector, mask);
		      gsl_vector_mul(L_log_reduced, mask);
		      gsl_vector_free(mask);
		    }
		    //compute the observation probability using things in the future
		    double p_obs = tklib_du_lp_obs(vp2_i, vp3_i, 
					           vp_index_to_topo_index, 
					           T_log_curr, D_log_curr,
					           SR_log_curr, L_log_reduced, 
					           O_log_curr, num_topologies);
		    //topN doesn't use epsilons
		    if (max_epsilon_transitions != -1) {
		      int vpb_i = vp2_i;
		      size_t p_i;
		      int epsilon_count = 0;

		      if (used_epsilons != NULL && curr_path != NULL) {
			    for(p_i = 0; p_i < curr_path->size; p_i++){
			      int vpa_i = gsl_vector_get(curr_path, curr_path->size - p_i - 1);

			      //int time = curr_path->size - p_i;
			      int idx1 = p_i *num_viewpoints + vpa_i;
			      int idx2 = vpb_i;
			      bool uses_epsilon = gsl_matrix_get(used_epsilons, idx1, idx2);
			      if (uses_epsilon) {
			    epsilon_count += 1;
			      }
			      vpb_i = vpa_i;
			    }
		      }
		      if (epsilon_count > max_epsilon_transitions) {
			    if (sdc_is_epsilon && vp2_i != vp3_i) {
	     	      p_obs = log(10e-30);
	     	    }
	     	  }
		    }

        //topN doesnt allow multiple sdcs_per_transition
		    // if the sdc applies better in the recent past, then do a self transition. 
		    if (vp2_i == vp3_i && curr_path != NULL && allow_multiple_sdcs_per_transition) {
		      int vpb_i = vp2_i;
		      size_t p_i;
	          for(p_i = 0; p_i < curr_path->size; p_i++){
	            int vpa_i = gsl_vector_get(curr_path, curr_path->size - p_i - 1);
			    double last_p_obs = tklib_du_lp_obs(vpa_i, vpb_i, 
							        vp_index_to_topo_index, 
							        T_log_curr, D_log_curr,
							        SR_log_curr, L_log_reduced, 
							        O_log_curr, num_topologies);
			    if (last_p_obs >= p_obs) {
			      p_obs = last_p_obs;
			    }
			    vpb_i = vpa_i;
			    if (p_i >= 2) {
			      break;
			    }
		      }
		    }
	
	      
		    double p_new = gsl_matrix_get(P_log_prev,vp1_i+N_i*num_states,vp2_i)+p_obs;
		    bool already_seen = compute_already_seen_topo(curr_path, vp2_i, vp_index_to_topo_index);
		
		    // allow self transitions
		    if (vp1_i == vp2_i) {
		      already_seen = false;
		    }
	
		    if (allow_backtracking) {
		      already_seen = false;
		    }
		    //if(already_seen == true)
		    //double p_trans = gsl_matrix_get(T_curr, vp3_i, vp2_i);
		    //p_new is the new probability
		    // check where in the N it should be.
		    int topN_idx;
		    double prob_to_insert=p_new; 
		    int curr_parent = vp1_i;
		    int curr_parent_iN = N_i;	    
		    if(!already_seen){
		      //EXPERIMENTAL: if there is no path that is going there do not add it. 
/*		      if(curr_path==NULL) continue;*/
		      if(myparents_prev != NULL && myparents_iN != NULL){
            curr_path = tklib_du_get_path_topN(myparents_prev, myparents_iN, 
                                            vp1_i, (int)(myparents_prev->size2/N)-1, N_i, N);
            if(curr_path==NULL) continue;                            
            }
		      for(topN_idx=0; topN_idx<N; topN_idx++){
		          if(prob_to_insert > gsl_matrix_get(&P_log_curr[topN_idx].matrix,vp2_i,vp3_i)){
		            double buffer= prob_to_insert;
		            prob_to_insert= gsl_matrix_get(&P_log_curr[topN_idx].matrix,vp2_i,vp3_i);
		            gsl_matrix_set(&P_log_curr[topN_idx].matrix, vp2_i, vp3_i, buffer);
		            int cpprev_buffer = curr_parent;
		            int cpin_buffer = curr_parent_iN;
		            curr_parent = gsl_matrix_get(&parents_prev.matrix,topN_idx,vp2_i); 
		            curr_parent_iN = gsl_matrix_get(&parents_iN.matrix,topN_idx,vp2_i); 
		            gsl_matrix_set(&parents_prev.matrix,topN_idx,vp2_i,cpprev_buffer);
		            gsl_matrix_set(&parents_iN.matrix,topN_idx,vp2_i,cpin_buffer);
		          }	 
		                   
              if(prob_to_insert==GSL_NEGINF) break;
                  
              //topN doesn't use epsilons		      		          
		          if (sdc_is_epsilon) {
			          if (vp2_i == vp3_i) {
			            gsl_matrix_set(&epsilons.matrix, vp2_i, vp3_i, false);
			          } else {
			            gsl_matrix_set(&epsilons.matrix, vp2_i, vp3_i, true);
			          }
		          } else {
			        gsl_matrix_set(&epsilons.matrix, vp2_i, vp3_i, false);
		          }
		          
		      }
		    }

		    
          }
        }    
        if(curr_path != NULL)
          gsl_vector_free(curr_path);
    }
    
  } 
  
  if(L_log_reduced != NULL)
    gsl_vector_free(L_log_reduced);
    
  return ret_mat;
	
}





//  
// Needs to be fixed to use log probs
// 
gsl_vector* tklib_du_marginalize_log(gsl_vector* prev_message,
				     gsl_matrix* T_log_curr,
				     gsl_matrix* SR_log_curr,
				     gsl_matrix* D_log_curr,
				     gsl_vector* L_log_curr,
				     gsl_vector* O_log_curr, 
				     gsl_vector* vp_i_to_topo_i, 
				     int num_topologies) {
  //copy over the old message
  gsl_vector* ret_msg = gsl_vector_calloc(prev_message->size);

  size_t num_viewpoints = vp_i_to_topo_i->size;

  size_t vp2_i;
  for(vp2_i = 0; vp2_i<num_viewpoints; vp2_i++){  
    double mysum = 0.0;

    size_t vp1_i;
    for(vp1_i=0; vp1_i<num_viewpoints; vp1_i++){ 
      if((T_log_curr != NULL && gsl_matrix_get(T_log_curr,vp2_i,vp1_i) == GSL_NEGINF)) {
       continue;
      }
      
      //compute the observation probability using things in the future
      double lp_obs = tklib_du_lp_obs(vp1_i, vp2_i,
				      vp_i_to_topo_i, 
				      T_log_curr, D_log_curr,
				      SR_log_curr, L_log_curr, O_log_curr, 
				      num_topologies);

      //apply the transition matrix only if it is not null
      mysum +=exp(gsl_vector_get(prev_message, vp1_i) + lp_obs);
    }
    gsl_vector_set(ret_msg, vp2_i, log(mysum));
  }
  
  return ret_msg;
}






 
gsl_matrix * tklib_du_lp_obs_array(size_t num_viewpoints,
				   gsl_vector* vp_i_to_topo_i,
				   gsl_matrix* T_log_curr, 
				   gsl_matrix* D_log_curr, 
				   gsl_matrix* SR_log_curr, 
				   gsl_vector* L_log_curr, 
				   gsl_vector* O_log_curr,
				   gsl_matrix* topo_i_to_location_mask,
				   int num_topologies) {

  gsl_matrix* ret_mat = gsl_matrix_calloc(num_viewpoints, num_viewpoints);
  size_t vp1_i;
  gsl_vector * L_log_reduced = NULL;
  gsl_vector * mask = NULL;
  if (L_log_curr != NULL) {
    L_log_reduced = gsl_vector_calloc(L_log_curr->size);
  }

  for(vp1_i=0; vp1_i<num_viewpoints; vp1_i++){ 
    size_t vp2_i;
    for(vp2_i = 0; vp2_i<num_viewpoints; vp2_i++){ 
      if (L_log_curr != NULL) {
       gsl_vector_memcpy(L_log_reduced, L_log_curr);
       if (topo_i_to_location_mask != NULL) {
    
         gsl_vector_view v1mask = gsl_matrix_row(topo_i_to_location_mask, 
                                                 gsl_vector_get(vp_i_to_topo_i, vp1_i));
         
         gsl_vector_view v2mask = gsl_matrix_row(topo_i_to_location_mask, 
                                                 gsl_vector_get(vp_i_to_topo_i, vp2_i));
         if (mask == NULL) {
           mask = gsl_vector_calloc(v2mask.vector.size);
           
         }
	 //printf("Starting computation\n");
         tklib_vector_union(&v1mask.vector, &v2mask.vector, mask);
	 tklib_apply_mask_lp(mask, L_log_reduced, L_log_reduced);
	 //assert(0);
       } 
      }
      double lp_obs =  tklib_du_lp_obs(vp1_i, vp2_i,
				       vp_i_to_topo_i,
				       T_log_curr, D_log_curr,
				       SR_log_curr, 
				       L_log_reduced, 
				       O_log_curr,
				       num_topologies);
      gsl_matrix_set(ret_mat, vp1_i, vp2_i, lp_obs);
    }
  }
  if (mask != NULL) {
    gsl_vector_free(mask);
  }

  if (L_log_reduced != NULL) {
    gsl_vector_free(L_log_reduced);
  }
  return ret_mat;
}

