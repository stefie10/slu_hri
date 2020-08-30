#ifndef PROBABILITY_H
#define PROBABILITY_H

#ifdef __cplusplus
extern "C" {
#endif
#include <gsl/gsl_vector.h>
#include <gsl/gsl_rng.h>
#include <math.h>
#include "gsl_utilities.h"
#include <gsl/gsl_randist.h>
#include <time.h>
#include <gsl/gsl_math.h>
//sample from a discrete distribution
gsl_vector* tklib_sample_discrete(gsl_vector* P, int number_of_samples);

//random values
void tklib_init_rng(int seed);
double tklib_randn();
double tklib_random();
int tklib_randint(int start, int end);

  //gsl_vector *tklib_vector_randn(int n);
gsl_vector* tklib_vector_randn(double mean, double std, int n);
gsl_vector* tklib_vector_random(int number);
gsl_vector* tklib_vector_randint(int number, int start, int end);

  //gsl_matrix* tklib_viterbi_update(gsl_vector* P_prev, gsl_matrix* T, gsl_vector* O_curr);
gsl_matrix* tklib_get_transition_matrix_maxprob(gsl_matrix* M, int num_steps);

inline gsl_matrix* tklib_viterbi_update(gsl_vector* P_prev, gsl_matrix* T, gsl_vector* O_curr){
  //make the current probability
  gsl_matrix* ret_mat = gsl_matrix_calloc(2, P_prev->size);
  
  gsl_vector_view P_curr = gsl_matrix_row(ret_mat, 0);
  gsl_vector_view parents = gsl_matrix_row(ret_mat, 1);
  
  //#j is the to state
  size_t j;
  for(j=0; j < T->size2; j++){ 
    //p_o = None;    
    double p_o =  gsl_vector_get(O_curr, j);

    //#k is thefrom state
    size_t k;
    for(k=0; k<T->size1; k++){ 
      double p_curr = gsl_vector_get(P_prev,k)*gsl_matrix_get(T,j,k)*p_o;
      
      if(p_curr > gsl_vector_get(&P_curr.vector,j)){
	gsl_vector_set(&P_curr.vector, j, p_curr);
	gsl_vector_set(&parents.vector,j, k);
      }
    }
  }

  return ret_mat;
}




bool compute_already_seen(gsl_vector* curr_path,
			  int vp_i, 
			  gsl_vector* vp_index_to_topo_index);

bool compute_already_seen_topo(gsl_vector* curr_path,
			       int vp_i, 
			       gsl_vector* vp_index_to_topo_index);
			  

gsl_vector* tklib_du_get_path(gsl_matrix* parents, int state_idx, int time_idx);
gsl_vector* tklib_du_get_path_topN(gsl_matrix* parents_prev, gsl_matrix* parents_iN, int state_idx, int time_idx, int iN_idx, int N);

gsl_matrix* tklib_du_update_log(gsl_matrix* P_log_prev,
				gsl_matrix* myparents,
				gsl_matrix* used_epsilons,
				gsl_matrix* T_log_curr,
				gsl_matrix* SR_log_curr,
				gsl_matrix* D_log_curr,
				gsl_vector* L_log_curr,
				gsl_vector* O_log_curr, 
				gsl_vector* vp_index_to_topo_index, 
				gsl_matrix* topo_i_to_location_mask,
				gsl_matrix* path_lengths,
				int num_topologies,
				bool allow_multiple_sdcs_per_transition,
				bool sdc_is_epsilon,
				bool allow_backtracking,
				int max_epsilon_transitions
				);

double tklib_du_lp_obs(int vp1_i, int vp2_i,
		       gsl_vector* vp_index_to_topo_index,
		       gsl_matrix* T_log_curr,
		       gsl_matrix* D_log_curr,
		       gsl_matrix* SR_log_curr, 
		       gsl_vector* L_log_curr, 
		       gsl_vector* O_log_curr,
		       int num_topologies);
  
gsl_matrix * tklib_du_lp_obs_array(size_t num_viewpoints,
				   gsl_vector* vp_index_to_topo_index,
				   gsl_matrix* T_log_curr,
				   gsl_matrix* D_log_curr,
				   gsl_matrix* SR_log_curr, 
				   gsl_vector* L_log_curr, 
				   gsl_vector* O_log_curr,
				   gsl_matrix* topo_i_to_location_mask,
				   int num_topologies);

double tklib_du_lp_sr(int vp1_i, int vp2_i,
		      gsl_vector* vp_index_to_topo_index,
		      gsl_matrix* SR_log_curr, 
		      gsl_vector* L_log_curr, 
		      gsl_vector* O_log_curr,
		      int num_topologies);

gsl_matrix * tklib_du_lp_sr_array(size_t num_viewpoints,
				  gsl_vector* vp_i_to_topo_i,
				  gsl_matrix* SR_log_curr, 
				  gsl_vector* L_log_curr, 
				  gsl_vector* O_log_curr,
				  int num_topologies);
  

gsl_vector* tklib_du_marginalize_log(gsl_vector* prev_message,
				     gsl_matrix* T_log_curr,
				     gsl_matrix* SR_log_curr,
				     gsl_matrix* D_log_curr,
				     gsl_vector* L_log_curr,
				     gsl_vector* O_log_curr, 
				     gsl_vector* vp_i_to_topo_i, 
				     int num_topologies);
				 
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
						    );				

#ifdef __cplusplus
}
#endif

#endif


