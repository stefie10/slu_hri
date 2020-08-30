#include "carmen_publish.h"

void carmen_publish_define_messages(void){

  //current spline message
  IPC_RETURN_TYPE err = IPC_defineMsg(CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_NAME,
				      IPC_VARIABLE_LENGTH, 
				      CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_NAME);



  //spline request message
  err = IPC_defineMsg(CARMEN_SPLINE_FREE_REQUEST_MESSAGE_NAME,
				      IPC_VARIABLE_LENGTH, 
				      CARMEN_SPLINE_FREE_REQUEST_MESSAGE_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_SPLINE_FREE_REQUEST_MESSAGE_NAME);

  
  

  //spline response message
  err = IPC_defineMsg(CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_NAME,
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_NAME);


  //spline response message
  err = IPC_defineMsg(CARMEN_EKF_MESSAGE_NAME,
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_EKF_MESSAGE_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_EKF_MESSAGE_NAME);


  //gridmapping pose
  err = IPC_defineMsg(CARMEN_GRIDMAPPING_POSE_NAME,
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_GRIDMAPPING_POSE_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_GRIDMAPPING_POSE_NAME);

  //gridmapping ray trace message
  err = IPC_defineMsg(CARMEN_GRIDMAPPING_RAY_TRACE_NAME,
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_GRIDMAPPING_RAY_TRACE_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_GRIDMAPPING_RAY_TRACE_NAME);

  //gridmapping ray trace message
  err = IPC_defineMsg(CARMEN_GRIDMAPPING_MAP_NAME,
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_GRIDMAPPING_MAP_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_GRIDMAPPING_MAP_NAME);

  //trajopt config message
  err = IPC_defineMsg(CARMEN_TRAJOPT_DESTINATIONS_CONFIG_NAME, 
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_TRAJOPT_DESTINATIONS_CONFIG_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_TRAJOPT_DESTINATIONS_CONFIG_NAME);


  //trajopt set destinations
  err = IPC_defineMsg(CARMEN_TRAJOPT_SET_DESTINATIONS_NAME, 
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_TRAJOPT_SET_DESTINATIONS_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_TRAJOPT_SET_DESTINATIONS_NAME);


  //GO MESSAGE
  err = IPC_defineMsg(CARMEN_TRAJOPT_GO_NAME, 
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_TRAJOPT_GO_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_TRAJOPT_GO_NAME);

  //STOP MESSAGE
  err = IPC_defineMsg(CARMEN_TRAJOPT_STOP_NAME, 
		      IPC_VARIABLE_LENGTH, 
		      CARMEN_TRAJOPT_STOP_FMT);

  carmen_test_ipc_exit(err, "Could not define message", 
		       CARMEN_TRAJOPT_STOP_NAME);

}


void carmen_publish_current_spline_message(SplineC* curr_spline){
  carmen_spline_free_request_message mymsg;
  gsl_vector* start_vec = curr_spline->get_start_pose();
  mymsg.x0 = gsl_vector_get(start_vec, 0);
  mymsg.y0 = gsl_vector_get(start_vec, 1);
  mymsg.start_theta = gsl_vector_get(start_vec, 2);

  gsl_vector* end_vec = curr_spline->get_end_pose();
  mymsg.x1 = gsl_vector_get(end_vec, 0);
  mymsg.y1 = gsl_vector_get(end_vec, 1);
  mymsg.end_theta = gsl_vector_get(end_vec, 2);

  mymsg.start_magnitude = curr_spline->get_start_magnitude();
  mymsg.end_magnitude = curr_spline->get_end_magnitude();
  
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_NAME);

  gsl_vector_free(start_vec);
  gsl_vector_free(end_vec);
}

void carmen_publish_spline_free_request_message(SplineC* curr_spline){
  carmen_spline_free_request_message mymsg;
  gsl_vector* start_vec = curr_spline->get_start_pose();
  mymsg.x0 = gsl_vector_get(start_vec, 0);
  mymsg.y0 = gsl_vector_get(start_vec, 1);
  mymsg.start_theta = gsl_vector_get(start_vec, 2);

  gsl_vector* end_vec = curr_spline->get_end_pose();
  mymsg.x1 = gsl_vector_get(end_vec, 0);
  mymsg.y1 = gsl_vector_get(end_vec, 1);
  mymsg.end_theta = gsl_vector_get(end_vec, 2);

  mymsg.start_magnitude = curr_spline->get_start_magnitude();
  mymsg.end_magnitude = curr_spline->get_end_magnitude();
  
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_SPLINE_FREE_REQUEST_MESSAGE_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_SPLINE_FREE_REQUEST_MESSAGE_NAME);

  gsl_vector_free(start_vec);
  gsl_vector_free(end_vec);
}


void carmen_publish_spline_free_response_message(int response, int signature){
  carmen_spline_free_response_message mymsg;
  mymsg.state = response;
  mymsg.signature = signature;
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_NAME);
}


void carmen_publish_ekf_message(gsl_vector* mean, gsl_matrix* covariance){
  if(covariance->size1 != covariance->size2){
    fprintf(stderr, "Error, covariance is not square\n");
    exit(1);
  }
  
  if(mean->size != covariance->size1){
    fprintf(stderr, "Error, mean size is not the same as covariance\n");
    exit(1);
  }
  
  carmen_ekf_message mymsg;
  mymsg.mean = mean->data;
  mymsg.size_mean = mean->size;
  mymsg.size_covariance = mean->size*mean->size;
  mymsg.covariance = covariance->data;
  
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();

  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_EKF_MESSAGE_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_EKF_MESSAGE_NAME);
}




void carmen_publish_gridmapping_pose_message(double x, double y, double theta){
  carmen_gridmapping_pose_message mymsg;
  
  mymsg.x = x;
  mymsg.y = y;
  mymsg.theta = theta;
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_GRIDMAPPING_POSE_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_GRIDMAPPING_POSE_NAME);
}

void carmen_publish_gridmapping_ray_trace_message(gsl_vector* robot_pose, 
						  gsl_vector* thetas, gsl_vector* readings){
  carmen_gridmapping_ray_trace_message mymsg;
  
  mymsg.x = gsl_vector_get(robot_pose, 0);
  mymsg.y = gsl_vector_get(robot_pose, 1);
  mymsg.theta = gsl_vector_get(robot_pose, 2);
  
  //printf("x %f , y %f, theta %f \n", mymsg.x, mymsg.y, mymsg.theta);
  if(thetas->size != readings->size){
    fprintf(stderr, "error, gridmapping thetas and readings don't match up\n");
    exit(0);
  }
  
  mymsg.num_readings = thetas->size;
  mymsg.thetas = thetas->data;
  mymsg.readings = readings->data;

  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_GRIDMAPPING_RAY_TRACE_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_GRIDMAPPING_RAY_TRACE_NAME);
}


void carmen_publish_gridmapping_map_message(gsl_matrix_float* themap, 
					    double x_origin, double y_origin, double resolution){
  carmen_gridmapping_map_message mymsg;
  mymsg.map_length = themap->size1*themap->size2;
  mymsg.map = themap->data;
  
  mymsg.size1 = themap->size1;
  mymsg.size2 = themap->size2;
  
  mymsg.x_origin = x_origin;
  mymsg.y_origin = y_origin;
  mymsg.resolution = resolution;

  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_GRIDMAPPING_MAP_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_GRIDMAPPING_MAP_NAME);
}


void carmen_publish_trajopt_config_message(int num_destinations){
  carmen_trajopt_destinations_config_message mymsg;
  mymsg.num_destinations = num_destinations;
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_TRAJOPT_DESTINATIONS_CONFIG_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_TRAJOPT_DESTINATIONS_CONFIG_NAME);
}

void carmen_publish_trajopt_set_destinations_message(gsl_matrix* destinations){
  carmen_trajopt_set_destinations_message mymsg;
  mymsg.num_destinations = destinations->size2;
  
  gsl_vector_view x = gsl_matrix_row(destinations, 0);
  gsl_vector_view y = gsl_matrix_row(destinations, 1);
  mymsg.x = x.vector.data;
  mymsg.y = y.vector.data;
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_TRAJOPT_SET_DESTINATIONS_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_TRAJOPT_SET_DESTINATIONS_NAME);
}

void carmen_publish_trajopt_go_message(void){
  carmen_trajopt_go_message mymsg;
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_TRAJOPT_GO_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_TRAJOPT_GO_NAME);
}

void carmen_publish_trajopt_stop_message(void){
  carmen_trajopt_stop_message mymsg;
  mymsg.timestamp = carmen_get_time();
  mymsg.host = carmen_get_host();
  
  IPC_RETURN_TYPE err;
  err = IPC_publishData(CARMEN_TRAJOPT_STOP_NAME, &mymsg);
  carmen_test_ipc(err, "Could not publish", CARMEN_TRAJOPT_STOP_NAME);
}
