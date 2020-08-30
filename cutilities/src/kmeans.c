#include "kmeans.h"


gsl_matrix* kmeans_get_distances(gsl_matrix* X, gsl_matrix* pts){
  //distances = zeros([len(pts[0]), len(X[0])])*1.0;
  gsl_matrix* distances = gsl_matrix_calloc(pts->size2, X->size2);

  //for i in range(len(pts[0])):
  size_t i;
  for(i=0; i< pts->size2; i++){

    //intended code
    //curr_mean = transpose([pts[:,i]])
    //dist_i = sqrt(sum((X-transpose([pts[:,i]]))**2))
    //distances[i,:] = dist_i

    gsl_vector_view curr_mean = gsl_matrix_column(pts, i);

    gsl_vector* dist_i = tklib_get_distance(X, &curr_mean.vector);
    gsl_matrix_set_row(distances, i, dist_i);
    
    gsl_vector_free(dist_i);
  }

  return distances;
}

int select_initial_cluster(gsl_matrix *X, gsl_matrix* init_clusters){
  //dists = get_distances(X, init_clusters)
  gsl_matrix* dists = kmeans_get_distances(X, init_clusters);
  gsl_vector* probs = tklib_matrix_min(dists, 0);
  
  //double maxval = gsl_vector_max(probs);
  //if(maxval == 0.0){
  //gsl_vector_add_constant(probs, 0.000000000000000000001);
  //}
  
  double Z = tklib_vector_sum(probs);
  gsl_vector_scale(probs, 1.0/Z);

  gsl_vector* indexes = tklib_sample_discrete(probs, 1);

  int ret_ind = (int)gsl_vector_get(indexes, 0);  
  gsl_vector_free(probs);
  gsl_matrix_free(dists);
  gsl_vector_free(indexes);
  
  return ret_ind;
}

gsl_matrix* get_initial_clusters(gsl_matrix *X, int num_clusters){
  //printf("kmeans: s1: %d , s2: %d \n", X->size1, num_clusters);
  gsl_matrix* init_means = gsl_matrix_calloc(X->size1, num_clusters);
  //int curr_number_of_means = 1;
  size_t index = tklib_randint(0, X->size2-1);
  
  //set the first value of the init_means
  gsl_vector* mean_col = gsl_vector_calloc(X->size1);
  gsl_matrix_get_col(mean_col, X, index);
  gsl_matrix_set_col(init_means, 0, mean_col);
  
  size_t i;
  for(i=1;(int)i<num_clusters;i++){
    gsl_matrix_view curr_means = gsl_matrix_submatrix(init_means, 0, 0, X->size1, i);
    index = select_initial_cluster(X, &curr_means.matrix);

    gsl_matrix_get_col(mean_col, X, index);
    gsl_matrix_set_col(init_means, i, mean_col);
  }
  
  //  printf("init_means\n");
  //tklib_matrix_printf(init_means);
  gsl_vector_free(mean_col);
  return init_means;
}


gsl_matrix* kmeans_compute_mean(gsl_matrix* X, gsl_vector* labels){
  gsl_matrix* means = gsl_matrix_calloc(X->size1, (int)gsl_vector_max(labels)+1);
  gsl_vector* count_mean_members = gsl_vector_calloc((int)gsl_vector_max(labels)+1);
  
  //fprintf(stderr, "x length kmeans %d\n", (int)gsl_vector_max(labels)+1);
  size_t i;
  double val;
  
  //intended meaning
  //for i in range(len(labels)):
  //  means[:,labels[i]] = means[:,labels[i]]+ X[:,i]
  //  count_mean_members[labels[i]] += 1
  //

  for(i=0;i<labels->size;i++){
    //get the current column
    gsl_vector_view mean_col = gsl_matrix_column(means, (int)gsl_vector_get(labels, i));
    gsl_vector_view pt_col = gsl_matrix_column(X, i);
    gsl_vector_add(&mean_col.vector, &pt_col.vector);
      
    //add 1 to the value of the count
    //printf("mean_col: %d\n", (int)gsl_vector_get(labels, i));
    //tklib_vector_printf(&mean_col.vector);
      
    val = gsl_vector_get(count_mean_members, (int)gsl_vector_get(labels, i));
    gsl_vector_set(count_mean_members, (int)gsl_vector_get(labels, i),  val+1);
  }


  //printf("means\n");
  //  tklib_matrix_printf(means);
  //indended meaning
  //for i in range(len(means)):
  //    means[:,i] = means[:,i]/count_mean_members[i]
  
  for(i=0;i<means->size2;i++){ 
    //scale the mean columns
    gsl_vector_view mean_col = gsl_matrix_column(means, i);
    gsl_vector_scale(&mean_col.vector, 1.0/gsl_vector_get(count_mean_members, i));
  }

  gsl_vector_free(count_mean_members);

  return means;
}

gsl_vector* kmeans_get_labels(gsl_matrix* X, gsl_matrix* means){
  gsl_matrix* distances = kmeans_get_distances(X, means);
  gsl_vector* labels = tklib_matrix_argmin(distances, 0);
  //printf("means_lables\n");  
  //tklib_matrix_printf(means);

  //printf("labels\n");
  //tklib_vector_printf(labels);
  gsl_matrix_free(distances);
  return labels;
}

gsl_matrix* kmeans(gsl_matrix *X, int iterations, gsl_matrix* init_means){
  gsl_matrix* means = gsl_matrix_alloc(init_means->size1, init_means->size2);
  gsl_matrix_memcpy(means, init_means);
  gsl_vector* labels;

  int i;
  for(i=0;i<iterations;i++){
    //printf("in kmeans\n");
    labels =  kmeans_get_labels(X, means);
    //distances = kmeans_get_distances(X, means);
    //labels = tklib_matrix_argmin(distances, 1);
    
    //free means and then get it again
    //printf("means1\n");
    //tklib_matrix_printf(means);    
    gsl_matrix_free(means);
    means = kmeans_compute_mean(X, labels);
    //printf("means2\n");
    //tklib_matrix_printf(means);
    
    gsl_vector_free(labels);
  }

  return means;

}


gsl_matrix* kmeans_autoinit(gsl_matrix *X, int iterations, int num_clusters){
  gsl_matrix* init_means = get_initial_clusters(X, num_clusters);
  gsl_matrix* curr_means = kmeans(X, iterations, init_means);
  gsl_matrix_free(init_means);
  return curr_means;
}


gsl_vector* kmeans_get_log_likelihood(gsl_matrix* X, gsl_matrix* u, 
				   gsl_vector* labels, double std){
  //initialize the probabilities
  gsl_matrix* probs = gsl_matrix_calloc(u->size2, X->size2);
  gsl_vector* probs_with_assignments = gsl_vector_calloc((int)gsl_vector_max(labels)+1);
  
  //initialize the covariance matrix
  gsl_vector* cov_vec = gsl_vector_alloc(u->size1);
  gsl_vector_set_all(cov_vec, std*std);
  gsl_matrix* cov_mat = tklib_diag(cov_vec);
  
  size_t i;
  for(i=0;i<u->size2;i++){
    gsl_vector_view u_i = gsl_matrix_column(u, i);
    gsl_vector* prob_i = gaussian_log_prob(X, &u_i.vector, cov_mat);

    gsl_matrix_set_row(probs, i, prob_i);
    gsl_vector_free(prob_i);
  }
  
  double p_cum, p_new;
  
  for(i=0;i<labels->size;i++){
    //supposed to be
    //probs_with_assignments[labels[i]] += probs[labels[i],i]

    p_cum = gsl_vector_get(probs_with_assignments, (int)gsl_vector_get(labels, i));
    p_new = gsl_matrix_get(probs, (int)gsl_vector_get(labels, i), i);
    gsl_vector_set(probs_with_assignments, (int)gsl_vector_get(labels,i), p_cum + p_new);
  }
  
  gsl_matrix_free(probs);
  gsl_vector_free(cov_vec);
  gsl_matrix_free(cov_mat);
  return probs_with_assignments;
}
