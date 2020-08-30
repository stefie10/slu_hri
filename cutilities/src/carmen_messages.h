#ifndef CARMEN_MESSAGES1_H
#define CARMEN_MESSAGES1_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  double x0, y0, x1, y1;
  double start_magnitude, end_magnitude;
  double start_theta, end_theta;
  double signature;
  double timestamp;
  char *host;
} carmen_spline_free_request_message;  
  
#define CARMEN_SPLINE_FREE_REQUEST_MESSAGE_NAME "carmen_spline_free_request_message"
#define CARMEN_SPLINE_FREE_REQUEST_MESSAGE_FMT  "{double, double, double, double, double, double, double, double, double, double, string}"

typedef struct {
  double x0, y0, x1, y1;
  double start_magnitude, end_magnitude;
  double start_theta, end_theta;
  double signature;
  double timestamp;
  char *host;
} carmen_trajopt_curr_spline_message;  
  
#define CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_NAME "carmen_trajopt_current_spline"
#define CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_FMT  "{double, double, double, double, double, double, double, double, double, double, string}"

typedef struct {
  int state;
  int signature;
  double timestamp;
  char *host;
} carmen_spline_free_response_message;  

#define CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_NAME "carmen_spline_free_response_message"
#define CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_FMT  "{int, int, double, string}"


typedef struct {
  int size_mean;
  int size_covariance;
  double* mean;
  double* covariance;
  double timestamp;
  char *host;
} carmen_ekf_message;
  
#define CARMEN_EKF_MESSAGE_NAME "carmen_ekf_message"
#define CARMEN_EKF_MESSAGE_FMT  "{int, int, <double:1>, <double:2>, double, string}"


typedef struct {
  double x;
  double y;
  double theta;
  double timestamp;
  char *host;
} carmen_gridmapping_pose_message;
  
#define CARMEN_GRIDMAPPING_POSE_NAME "carmen_gridmapping_pose"
#define CARMEN_GRIDMAPPING_POSE_FMT "{double, double, double, double, string}"


typedef struct {
  //robot pose
  double x;
  double y;
  double theta;
  
  //the readings from the current position
  int num_readings;
  double* thetas;
  double* readings;
  
  //rest of the message
  double timestamp;
  char *host;
} carmen_gridmapping_ray_trace_message;

#define CARMEN_GRIDMAPPING_RAY_TRACE_NAME "carmen_gridmapping_ray_trace"
#define CARMEN_GRIDMAPPING_RAY_TRACE_FMT "{double, double, double, int, <double:4>, <double:4>, double, string}"

typedef struct {
  //these are for ipc
  int map_length;
  float* map;
  
  //these are for the actual size of the map
  int size1;
  int size2;

  //these are the parameters for the map
  double resolution;  
  double x_origin;
  double y_origin;

  //rest of the message
  double timestamp;
  char *host;
} carmen_gridmapping_map_message;
  
#define CARMEN_GRIDMAPPING_MAP_NAME "carmen_gridmapping_map"
#define CARMEN_GRIDMAPPING_MAP_FMT "{int, <float:1>, int, int, double, double, double, double, string}"


typedef struct {
  int num_destinations;
  double* x;
  double* y;
  double timestamp;
  char *host;
} carmen_trajopt_set_destinations_message;
  
#define CARMEN_TRAJOPT_SET_DESTINATIONS_NAME "carmen_trajopt_set_destinations"
#define CARMEN_TRAJOPT_SET_DESTINATIONS_FMT "{int, <double:1>, <double:1>, double, string}"

typedef struct {
  int num_destinations;
  double timestamp;
  char *host;
} carmen_trajopt_destinations_config_message;

#define CARMEN_TRAJOPT_DESTINATIONS_CONFIG_NAME "carmen_trajopt_destinations_config"
#define CARMEN_TRAJOPT_DESTINATIONS_CONFIG_FMT "{int, double, string}"

typedef struct {
  double timestamp;
  char *host;
} carmen_trajopt_go_message;

#define CARMEN_TRAJOPT_GO_NAME "carmen_trajopt_go"
#define CARMEN_TRAJOPT_GO_FMT "{double, string}"

typedef struct {
  double timestamp;
  char *host;
} carmen_trajopt_stop_message;

#define CARMEN_TRAJOPT_STOP_NAME "carmen_trajopt_STOP"
#define CARMEN_TRAJOPT_STOP_FMT "{double, string}"

#ifdef __cplusplus
}
#endif

#endif
