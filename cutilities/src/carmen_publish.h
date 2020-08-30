#ifndef CARMEN_PUBLISH1_H
#define CARMEN_PUBLISH1_H

#ifdef __cplusplus
extern "C" {
#endif

#include <carmen/carmen.h>
#include "carmen_messages.h"
#include "spline.h"

void carmen_publish_define_messages(void);
void carmen_publish_spline_free_request_message(SplineC* curr_spline);
void carmen_publish_spline_free_response_message(int response, int signature);
void carmen_publish_ekf_message(gsl_vector* mean, gsl_matrix* covariance);
void carmen_publish_gridmapping_pose_message(double x, double y, double theta);
void carmen_publish_gridmapping_ray_trace_message(gsl_vector* robot_pose, 
						  gsl_vector* thetas, gsl_vector* readings);
void carmen_publish_gridmapping_map_message(gsl_matrix_float* themap, 
					    double x_origin, double y_origin, double resolution);

void carmen_publish_current_spline_message(SplineC* curr_spline);
void carmen_publish_trajopt_config_message(int num_destinations);
void carmen_publish_trajopt_set_destinations_message(gsl_matrix* destinations);
void carmen_publish_trajopt_go_message(void);
void carmen_publish_trajopt_stop_message(void);

#ifdef __cplusplus
}
#endif


#endif
