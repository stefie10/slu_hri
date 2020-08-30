#ifndef CARMEN_UTIL1_H
#define CARMEN_UTIL1_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <carmen/carmen.h>
#include <carmen/map_io.h>
#include "gsl_utilities.h"
#include <carmen/vascocore.h>


#ifdef __cplusplus
extern "C" {
#endif

//load a carmen mapfile into a carmen_map_p
carmen_map_p carmen_util_read_gridmap(char* filename);

gsl_matrix* carmen_util_reading_to_xy(gsl_vector* mypose, gsl_vector* myreading, 
				      double rel_start_angle, double rel_end_angle);

int carmen_util_write_gridmap(char* filename, gsl_matrix_float* probability, double resolution);

//type is "sick" or "samsung"
void carmen_util_init_vasco(char *laser_type);

//perform scan matching and return the matches
gsl_vector* carmen_util_vasco_scan_match(gsl_vector* curr_pose, 
					 gsl_vector_float* range, 
					 gsl_vector_float* angle, int first);
  
#ifdef __cplusplus
}
#endif

#endif

