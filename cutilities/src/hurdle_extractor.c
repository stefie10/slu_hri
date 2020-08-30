#include "hurdle_extractor.h"

static inline int tklib_max(int a , int b){
  return a>b?a:b;
}

static inline int tklib_min(int a , int b){
  return a<b?a:b;
}

gsl_vector* hurdle_candidates(gsl_vector* pt, gsl_matrix* pts, 
			      double separation, double separation_err){

  gsl_vector* k_dists = tklib_get_distance(pts, pt);
  gsl_permutation* k_ind_perm = NN_all_index(pt, pts);
  gsl_vector* k_ind = tklib_permutation_to_vector(k_ind_perm);

  double min_sep = separation - separation_err;
  double max_sep = separation + separation_err;
    
  PyObject* min_indexes = PyList_New(0);

  size_t i;
  size_t curr_ind;
  for(i=0;i<k_dists->size;i++){
    curr_ind = (size_t)gsl_vector_get(k_ind,i);
    if(gsl_vector_get(k_dists,curr_ind) > min_sep && gsl_vector_get(k_dists, curr_ind)<max_sep){
      //again with the appending
      double val = gsl_vector_get(k_ind, i);
      PyObject* myint = PyFloat_FromDouble(val);
      PyList_Append(min_indexes, myint);
      
      Py_DECREF(myint);
    }

    //there can be no answers over this value
    if(gsl_vector_get(k_dists, curr_ind) > (separation + separation_err))
      break;
  }
  
  
  gsl_vector* ret_vec = pyobject_to_gsl_vector(min_indexes);
  gsl_vector_free(k_dists);
  gsl_permutation_free(k_ind_perm);
  gsl_vector_free(k_ind);

  Py_DECREF(min_indexes);
  
  return ret_vec;
}

gsl_matrix* hurdles_extract(gsl_matrix* pts, double separation, double separation_err, 
			    double window_height, double window_dw, double min_log_likelihood){

  PyObject* fin_hurdles = PyList_New(0);
  
  gsl_matrix* curr_pts = gsl_matrix_calloc(pts->size1, pts->size2);
  gsl_matrix_memcpy(curr_pts, pts);
    
  size_t i = 0;

  double m_width, m_height, b_width, b_height;
  
  while(1){
    if(curr_pts == NULL || i > curr_pts->size2 -1)
      break;
    
    gsl_vector_view st_pt = gsl_matrix_column(curr_pts, i);
    gsl_vector* min_indexes = hurdle_candidates(&st_pt.vector, curr_pts, 
						separation, separation_err);
    
    if(min_indexes == NULL){
      i+=1;
      //gsl_vector_free(min_indexes);
      continue;
    }

    gsl_vector_view end_pt = gsl_matrix_column(curr_pts,
					       (int)gsl_vector_get(min_indexes, 
								   min_indexes->size/2));
    
    //create a window and get the points in this window
    get_line_parameters_m_b(&st_pt.vector, &end_pt.vector, &m_width, &b_width);
    gsl_vector* midpoint = tklib_get_centroid(&st_pt.vector, &end_pt.vector);
    get_line_parameters_m_pt(-1.0/m_width, midpoint, &m_height, &b_height);

    //get the points in the window
    gsl_matrix* rect_pts = box_inwindow(curr_pts, &st_pt.vector, &end_pt.vector, 
					window_height, window_dw, 
					m_width, b_width, m_height, b_height);

    //perform kmeans clustering


    gsl_matrix* curr_means = kmeans_autoinit(rect_pts, 3, 2);
    gsl_vector* labels = kmeans_get_labels(rect_pts, curr_means);
    gsl_vector* probs = kmeans_get_log_likelihood(rect_pts, curr_means, labels, 0.01);
    
    //if this is the case then we have found some poles
    if(labels->size > 1 && gsl_vector_get(probs,0) > min_log_likelihood &&  
       gsl_vector_get(probs,1) > min_log_likelihood){
      //add the final values
      gsl_vector* fin_hurdle = tklib_matrix_sum(curr_means,1);
      gsl_vector_scale(fin_hurdle, 1.0/2.0);
      
      PyObject* py_fin_hurdle = gsl_vector_to_pyobject(fin_hurdle);
      PyList_Append(fin_hurdles, py_fin_hurdle);
      
      gsl_matrix* out_box_pts = box_outwindow(curr_pts, &st_pt.vector, &end_pt.vector, 
					      window_height, window_dw, 
					      m_width, b_width, m_height, b_height);

      gsl_matrix_free(curr_pts);
      //do not free out_box_pts since it is the new curr_pts
      curr_pts = out_box_pts;
      Py_DECREF(py_fin_hurdle);
      gsl_vector_free(fin_hurdle);
    }
    i+=1;
    
    gsl_vector_free(min_indexes);
    gsl_vector_free(midpoint);
    gsl_matrix_free(rect_pts);
    gsl_matrix_free(curr_means);
    gsl_vector_free(labels);
    gsl_vector_free(probs);
  }
  

  gsl_matrix* ret_hurdles_trans = pyobject_to_gsl_matrix(fin_hurdles);
  if(ret_hurdles_trans == NULL){
    return NULL;
  }
  gsl_matrix* ret_hurdles = gsl_matrix_alloc(ret_hurdles_trans->size2, ret_hurdles_trans->size1);
  gsl_matrix_transpose_memcpy(ret_hurdles, ret_hurdles_trans);
  
  Py_DECREF(fin_hurdles);
  if(curr_pts != NULL)
    gsl_matrix_free(curr_pts);
  gsl_matrix_free(ret_hurdles_trans);
  return ret_hurdles;
  
  //return transpose(fin_hurdles);
}


gsl_matrix* hurdles_extract_optimized(gsl_matrix* pts, double separation, 
				      double separation_err, double window_height, 
				      double window_dw, double min_log_likelihood, 
				      int searchahead){
  PyObject* fin_hurdles = PyList_New(0);
  gsl_matrix* curr_pts = gsl_matrix_calloc(pts->size1, pts->size2);
  gsl_matrix_memcpy(curr_pts, pts);
  
  size_t i = 0;

  double m_width, m_height, b_width, b_height;

  gsl_vector* st_pt = gsl_vector_calloc(pts->size1);
  gsl_vector* end_pt = gsl_vector_calloc(pts->size1);
  while(1){
    if(curr_pts==NULL || i > curr_pts->size2 -1){
      break;
    }

    gsl_matrix_get_col(st_pt, curr_pts, i);
    
    int sa_min_i = tklib_max(i-searchahead, 0);
    int sa_max_i = tklib_min(i+searchahead, curr_pts->size2-1);
    
    gsl_matrix_view curr_pts_view = gsl_matrix_submatrix(curr_pts, 0, sa_min_i, 
							 curr_pts->size1, sa_max_i - sa_min_i);

    gsl_vector* min_indexes = hurdle_candidates(st_pt,&curr_pts_view.matrix,  
						separation, separation_err);
    
    if(min_indexes == NULL){
      i+=1;
      continue;
    }
    
    gsl_matrix_get_col(end_pt, &curr_pts_view.matrix, 
		       (int)gsl_vector_get(min_indexes, min_indexes->size/2));
    
    //create a window and get the points in this window
    get_line_parameters_m_b(st_pt, end_pt, &m_width, &b_width);
    gsl_vector* midpoint = tklib_get_centroid(st_pt, end_pt);
    get_line_parameters_m_pt(-1.0/m_width, midpoint, &m_height, &b_height);

    //get the points in the window
    gsl_matrix* rect_pts = box_inwindow(&curr_pts_view.matrix, st_pt, end_pt, 
					window_height, window_dw, 
					m_width, b_width, m_height, b_height);
    
    //perform kmeans clustering
    gsl_matrix* curr_means = kmeans_autoinit(rect_pts, 3, 2);
    gsl_vector* labels = kmeans_get_labels(rect_pts, curr_means);
    gsl_vector* probs = kmeans_get_log_likelihood(rect_pts, curr_means, labels, 0.01);
    
    //if this is the case then we have found some poles
    if(labels->size > 1 && gsl_vector_get(probs,0) > min_log_likelihood &&  gsl_vector_get(probs,1) > min_log_likelihood){
      //add the final values
      gsl_vector* fin_hurdle = tklib_matrix_sum(curr_means,1);
      gsl_vector_scale(fin_hurdle, 1.0/2.0);

      PyObject* py_fin_hurdle = gsl_vector_to_pyobject(fin_hurdle);
      PyList_Append(fin_hurdles, py_fin_hurdle);
      
      gsl_matrix* out_box_pts = box_outwindow(curr_pts, st_pt, end_pt, 
					      window_height, window_dw, 
					      m_width, b_width, m_height, b_height);
      
      if(curr_pts != NULL)
	gsl_matrix_free(curr_pts);
      //do not free out_box_pts since it is the new curr_pts
      curr_pts = out_box_pts;
      Py_DECREF(py_fin_hurdle);
      gsl_vector_free(fin_hurdle);
    }
    i+=1;
    
    gsl_vector_free(min_indexes);
    gsl_vector_free(midpoint);
    gsl_matrix_free(rect_pts);
    gsl_matrix_free(curr_means);
    gsl_vector_free(labels);
    gsl_vector_free(probs);
  }
  
  gsl_matrix* ret_hurdles_trans = pyobject_to_gsl_matrix(fin_hurdles);
  if(curr_pts != NULL)
    gsl_matrix_free(curr_pts);
  gsl_vector_free(st_pt);
  gsl_vector_free(end_pt);
  Py_DECREF(fin_hurdles);
  
  if(ret_hurdles_trans == NULL){
    return NULL;
  }
  gsl_matrix* ret_hurdles = gsl_matrix_alloc(ret_hurdles_trans->size2, ret_hurdles_trans->size1);
  gsl_matrix_transpose_memcpy(ret_hurdles, ret_hurdles_trans);
  gsl_matrix_free(ret_hurdles_trans);
  return ret_hurdles;
}




gsl_matrix* hurdles_extract_optimized_search(gsl_matrix* pts, double separation, 
					     double separation_err, double window_height, 
					     double window_dw, double min_log_likelihood, 
					     int searchahead){
  PyObject* fin_hurdles = PyList_New(0);
  
  gsl_matrix* curr_pts = gsl_matrix_calloc(pts->size1, pts->size2);
  gsl_matrix_memcpy(curr_pts, pts);
  
  size_t i = 0;

  double m_width, m_height, b_width, b_height;

  gsl_vector* st_pt = gsl_vector_calloc(pts->size1);
  gsl_vector* end_pt = gsl_vector_calloc(pts->size1);
  while(1){
    if(curr_pts == NULL || i > curr_pts->size2 -1)
      break;
    
    gsl_matrix_get_col(st_pt, curr_pts, i);
    
    int sa_min_i = tklib_max(i-searchahead, 0);
    int sa_max_i = tklib_min(i+searchahead, curr_pts->size2-1);
    
    gsl_matrix_view curr_pts_view = gsl_matrix_submatrix(curr_pts, 0, sa_min_i, 
							 curr_pts->size1, sa_max_i - sa_min_i);
    
    //tklib_matrix_printf(&curr_pts_view.matrix);
    gsl_vector* min_indexes = hurdle_candidates(st_pt,&curr_pts_view.matrix,  //&curr_pts_view.matrix
						separation, separation_err);
    
    if(min_indexes == NULL){
      i+=1;
      continue;
    }
    
    
    size_t j;
    gsl_matrix* fin_means=NULL;
    gsl_vector* fin_probs=NULL;
    double max_sum=-1000000000.0;
    //find the best model and then pass it along out of all possibilities
    for(j=0; j<min_indexes->size;j++){
      gsl_matrix_get_col(end_pt, &curr_pts_view.matrix, (int)gsl_vector_get(min_indexes, j));
    
      //create a window and get the points in this window
      get_line_parameters_m_b(st_pt, end_pt, &m_width, &b_width);
      gsl_vector* midpoint = tklib_get_centroid(st_pt, end_pt);
      get_line_parameters_m_pt(-1.0/m_width, midpoint, &m_height, &b_height);
      
      //get the points in the window
      gsl_matrix* rect_pts = box_inwindow(&curr_pts_view.matrix, st_pt, end_pt, 
					  window_height, window_dw, 
					  m_width, b_width, m_height, b_height);
       
      //perform kmeans clustering
      gsl_matrix* curr_means = kmeans_autoinit(rect_pts, 3, 2);
      gsl_vector* labels = kmeans_get_labels(rect_pts, curr_means);
      gsl_vector* probs = kmeans_get_log_likelihood(rect_pts, curr_means, labels, 0.01);
      //double tklib_vector_sum(gsl_vector* vec);
      if(tklib_vector_sum(probs) > max_sum){
	max_sum = tklib_vector_sum(probs);
	if(fin_means != NULL){
	  gsl_matrix_free(fin_means);
	  gsl_vector_free(fin_probs);
	}
	fin_means = curr_means;
	fin_probs = probs;
      }
      else{
	gsl_vector_free(probs);
	gsl_matrix_free(curr_means);
      }

      gsl_vector_free(labels);
      gsl_vector_free(midpoint);
      gsl_matrix_free(rect_pts);
    }
    
    //if this is the case then we have found some poles
    if(fin_probs != NULL && fin_probs->size > 1 &&
       gsl_vector_get(fin_probs,0) > min_log_likelihood &&  
       gsl_vector_get(fin_probs,1) > min_log_likelihood){
      
      //add the final values
      gsl_vector* fin_hurdle = tklib_matrix_sum(fin_means,1);
      gsl_vector_scale(fin_hurdle, 1.0/2.0);
	
      PyObject* py_fin_hurdle = gsl_vector_to_pyobject(fin_hurdle);
      PyList_Append(fin_hurdles, py_fin_hurdle);
      
      gsl_matrix* out_box_pts = box_outwindow(curr_pts, st_pt, end_pt, 
					      window_height, window_dw, 
					      m_width, b_width, m_height, b_height);
      
      if(curr_pts != NULL)
	gsl_matrix_free(curr_pts);
      //do not free out_box_pts since it is the new curr_pts
      curr_pts = out_box_pts;
      Py_DECREF(py_fin_hurdle);
      gsl_vector_free(fin_hurdle);
      gsl_matrix_free(fin_means);
      gsl_vector_free(fin_probs);
    }
    i+=1;
    
    gsl_vector_free(min_indexes);
  }
  
  


  gsl_matrix* ret_hurdles_trans = pyobject_to_gsl_matrix(fin_hurdles);

  if(ret_hurdles_trans == NULL){
    //fprintf(stderr, "NULL pointer\n"); 
    return NULL;
  }
  gsl_matrix* ret_hurdles = gsl_matrix_alloc(ret_hurdles_trans->size2, ret_hurdles_trans->size1);
  gsl_matrix_transpose_memcpy(ret_hurdles, ret_hurdles_trans);
  
  /*Py_DECREF(fin_hurdles);
  gsl_matrix_free(curr_pts);
  gsl_matrix_free(ret_hurdles_trans);
  gsl_vector_free(st_pt);
  gsl_vector_free(end_pt);*/
  Py_DECREF(fin_hurdles);
  return ret_hurdles;
  
  //return transpose(fin_hurdles);
}
