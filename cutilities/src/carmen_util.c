#include "carmen_util.h"

carmen_vascocore_param_t carmen_util_vasco_parameters;

//type is "sick" or "samsung"
void carmen_util_init_vasco(char *laser_type){
  vascocore_get_default_params(&carmen_util_vasco_parameters, laser_type);
  vascocore_init_no_ipc(&carmen_util_vasco_parameters);
}


gsl_vector* carmen_util_vasco_scan_match(gsl_vector* curr_pose, 
					 gsl_vector_float* range, 
					 gsl_vector_float* angle, int first){
  carmen_point_t start_pt;
  gsl_vector* retpt = gsl_vector_alloc(3);
  
  start_pt.x = gsl_vector_get(curr_pose,0);
  start_pt.y = gsl_vector_get(curr_pose,1);
  start_pt.theta = gsl_vector_get(curr_pose,2);
  
  carmen_point_t pt = vascocore_scan_match_general(range->size, range->data, 
						   angle->data,  M_PI,
						   start_pt, first);
  gsl_vector_set(retpt, 0, pt.x);
  gsl_vector_set(retpt, 1, pt.y);
  gsl_vector_set(retpt, 2, pt.theta);
  
  return retpt;
}



carmen_map_p carmen_util_read_gridmap(char* filename){
  //  config->map_name = (char *)calloc(strlen(filename) + 1, sizeof(char));
  carmen_map_p map = (carmen_map_p)calloc(1, sizeof(carmen_map_t));
  int error = carmen_map_read_gridmap_chunk(filename, map);
  error=error;
  
  return map;
}


int carmen_util_write_gridmap(char* filename, gsl_matrix_float* probability, double resolution){
  //  printf("opening file\n");
  carmen_FILE *fp = carmen_fopen(filename, "w");
  if(fp == NULL)
    return 0;
  
  if (carmen_map_write_id(fp) < 0)
    carmen_die_syserror("Couldn't write map id to %s", filename);

  float** map_data = (float**)calloc(probability->size1, sizeof(float*));
  
  size_t i;
  for(i=0;i<probability->size1;i++){
    map_data[i] = &probability->data[i*probability->size2];
  }

  int loaded =  carmen_map_write_gridmap_chunk(fp, map_data, 
					       probability->size1, probability->size2, resolution);
  
  carmen_fclose(fp);
  free(map_data);
  
  if(loaded<0)
    return 0;
  return 1;
}


//gsl_matrix* carmen_util_reading_to_xy(gsl_vector* mypose, gsl_vector* myreading){
gsl_matrix* carmen_util_reading_to_xy(gsl_vector* mypose, gsl_vector* myreading, 
				      double rel_start_angle, double rel_end_angle){
  gsl_matrix *ret_matrix = gsl_matrix_alloc(2, myreading->size);

  double th_inc = fabs(rel_end_angle-rel_start_angle)/myreading->size;
  gsl_vector* theta = tklib_range(rel_start_angle, rel_end_angle, th_inc);
  
  //printf("thetas %d\n", theta->size);
  //printf("myreading %d\n", myreading->size);
  //tklib_vector_printf(theta);

  gsl_vector_add_constant(theta, gsl_vector_get(mypose, 2));
  
  //compute X, Y
  gsl_vector *X = tklib_cos(theta);
  gsl_vector *Y = tklib_sin(theta);


  
  gsl_vector_mul(X, myreading);
  gsl_vector_mul(Y, myreading);

  //add the translation
  gsl_vector_add_constant(X, gsl_vector_get(mypose, 0));
  gsl_vector_add_constant(Y, gsl_vector_get(mypose, 1));
  
  gsl_matrix_set_row(ret_matrix, 0, X);
  gsl_matrix_set_row(ret_matrix, 1, Y);
  
  gsl_vector_free(X);
  gsl_vector_free(Y);
  gsl_vector_free(theta);
  return ret_matrix;
}


