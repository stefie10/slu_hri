#ifndef CARMEN_SUBSCRIBE1_H
#define CARMEN_SUBSCRIBE1_H

#ifdef __cplusplus
extern "C" {
#endif

#include <carmen/carmen.h>
#include "carmen_messages.h"
#include "spline.h"

/*typedef struct {
  double x;
  double y;
  double theta;
  double timestamp;
  char *host;
} garmen_gridmapping_pose_message;
  
#define CARMEN_GRIDMAPPING_POSE_NAME "carmen_gridmapping_pose"
#define CARMEN_GRIDMAPPING_POSE_NAME "{double, double, double, double, string}"*/


class pyTklibHandler {
 private:
  carmen_spline_free_request_message the_latest_spline_free_request;
  carmen_spline_free_response_message the_latest_spline_free_response;
  carmen_ekf_message the_latest_ekf_message;  
  carmen_gridmapping_pose_message the_latest_gridmapping_pose_message;
  carmen_gridmapping_ray_trace_message the_latest_gridmapping_ray_trace_message;
  carmen_gridmapping_map_message the_latest_gridmapping_map_message;
  carmen_trajopt_destinations_config_message the_latest_trajopt_config;
  carmen_trajopt_set_destinations_message the_latest_trajopt_destinations;
  carmen_trajopt_go_message the_latest_go_msg;
  carmen_trajopt_stop_message the_latest_stop_msg;
  carmen_trajopt_curr_spline_message the_current_spline;
 public:
  pyTklibHandler(){
  }
  virtual ~pyTklibHandler() 
    {}
  virtual void run_cb(char* type, char* msg)
  {type=type; msg=msg;}
  
  //request message
  void set_spline_free_request_message(carmen_spline_free_request_message *msg);
  SplineC* spline_free_request_message();
  
  //response message
  void set_spline_free_response_message(carmen_spline_free_response_message *msg);
  carmen_spline_free_response_message* spline_free_response_message();
  
  //ekf message
  void set_ekf_message(carmen_ekf_message *msg);
  carmen_ekf_message* get_carmen_ekf_message();

  //ekf message
  void set_gridmapping_pose_message(carmen_gridmapping_pose_message *msg);
  carmen_gridmapping_pose_message* get_gridmapping_pose_message();

  void set_gridmapping_ray_trace_message(carmen_gridmapping_ray_trace_message *msg);
  carmen_gridmapping_ray_trace_message* get_gridmapping_ray_trace_message();

  void set_gridmapping_map_message(carmen_gridmapping_map_message *msg);
  carmen_gridmapping_map_message* get_gridmapping_map_message();

  //trajopt config message
  void set_trajopt_config_message(carmen_trajopt_destinations_config_message *msg);
  carmen_trajopt_destinations_config_message* get_trajopt_config_message();

  //trajopt set destinations message
  void set_trajopt_destinations_message(carmen_trajopt_set_destinations_message *msg);
  gsl_matrix* get_trajopt_destinations_message();

  //trajopt set go message
  void set_trajopt_go_message(carmen_trajopt_go_message *msg);
  carmen_trajopt_go_message* get_trajopt_go_message();

  //trajopt set stop message
  void set_trajopt_stop_message(carmen_trajopt_stop_message *msg);
  carmen_trajopt_stop_message* get_trajopt_stop_message();
  
  void set_curr_spline_message(carmen_trajopt_curr_spline_message *msg);
  SplineC* get_curr_spline_message();
};



class subscribe_spline_free_request_message{
 public:
  subscribe_spline_free_request_message(pyTklibHandler *cb);
  static void my_handler(carmen_spline_free_request_message *msg);
};

class subscribe_spline_free_response_message{
 public:
  subscribe_spline_free_response_message(pyTklibHandler *cb);
  static void my_handler(carmen_spline_free_response_message *msg);
};

class subscribe_ekf_message{
 public:
  subscribe_ekf_message(pyTklibHandler *cb);
  static void my_handler(carmen_ekf_message *msg);
};

class subscribe_gridmapping_pose_message{
 public:
  subscribe_gridmapping_pose_message(pyTklibHandler *cb);
  static void my_handler(carmen_gridmapping_pose_message *msg);
};

class subscribe_gridmapping_ray_trace_message{
 public:
  subscribe_gridmapping_ray_trace_message(pyTklibHandler *cb);
  static void my_handler(carmen_gridmapping_ray_trace_message *msg);
};

class subscribe_gridmapping_map_message{
 public:
  subscribe_gridmapping_map_message(pyTklibHandler *cb);
  static void my_handler(carmen_gridmapping_map_message *msg);
};

class subscribe_trajopt_config_message{
 public:
  subscribe_trajopt_config_message(pyTklibHandler *cb);
  static void my_handler(carmen_trajopt_destinations_config_message *msg);
};

class subscribe_trajopt_destinations_message{
 public:
  subscribe_trajopt_destinations_message(pyTklibHandler *cb);
  static void my_handler(carmen_trajopt_set_destinations_message *msg);
};

class subscribe_trajopt_go_message{
 public:
  subscribe_trajopt_go_message(pyTklibHandler *cb);
  static void my_handler(carmen_trajopt_go_message *msg);
};

class subscribe_trajopt_stop_message{
 public:
  subscribe_trajopt_stop_message(pyTklibHandler *cb);
  static void my_handler(carmen_trajopt_stop_message *msg);
};

class subscribe_trajopt_curr_spline_message{
 public:
  subscribe_trajopt_curr_spline_message(pyTklibHandler *cb);
  static void my_handler(carmen_trajopt_curr_spline_message *msg);
};

#ifdef __cplusplus
}
#endif


#endif
