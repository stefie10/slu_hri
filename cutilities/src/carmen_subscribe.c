#include "carmen_subscribe.h"

//void set_curr_spline_message(carmen_trajopt_curr_spline_message *msg);
void pyTklibHandler::set_curr_spline_message(carmen_trajopt_curr_spline_message *msg){
  memcpy(&the_current_spline, msg, sizeof(carmen_trajopt_curr_spline_message));
}


//  SplineC* get_curr_spline_message();	
SplineC* pyTklibHandler::get_curr_spline_message() {
  carmen_trajopt_curr_spline_message* myp = &the_current_spline;
  
  gsl_vector* start_pose = gsl_vector_alloc(3);
  gsl_vector_set(start_pose, 0, myp->x0);
  gsl_vector_set(start_pose, 1, myp->y0);
  gsl_vector_set(start_pose, 2, myp->start_theta);
  
  gsl_vector* end_pose = gsl_vector_alloc(3);
  gsl_vector_set(end_pose, 0, myp->x1);
  gsl_vector_set(end_pose, 1, myp->y1);
  gsl_vector_set(end_pose, 2, myp->end_theta);

  SplineC * retspline = new SplineC(start_pose, end_pose, myp->start_magnitude, myp->end_magnitude);
  return retspline;
}


/*********Handler Class***********/
//request message
void pyTklibHandler::set_spline_free_request_message(carmen_spline_free_request_message *msg){
  memcpy(&the_latest_spline_free_request, msg, sizeof(carmen_spline_free_request_message));
}
	
SplineC* pyTklibHandler::spline_free_request_message() {
  carmen_spline_free_request_message* myp = &the_latest_spline_free_request;
  
  gsl_vector* start_pose = gsl_vector_alloc(3);
  gsl_vector_set(start_pose, 0, myp->x0);
  gsl_vector_set(start_pose, 1, myp->y0);
  gsl_vector_set(start_pose, 2, myp->start_theta);
  
  gsl_vector* end_pose = gsl_vector_alloc(3);
  gsl_vector_set(end_pose, 0, myp->x1);
  gsl_vector_set(end_pose, 1, myp->y1);
  gsl_vector_set(end_pose, 2, myp->end_theta);
  
  SplineC * retspline = new SplineC(start_pose, end_pose, myp->start_magnitude, myp->end_magnitude);
  
  return retspline;
}
	
//response message
void pyTklibHandler::set_spline_free_response_message(carmen_spline_free_response_message *msg){
  memcpy(&the_latest_spline_free_response, msg, sizeof(carmen_spline_free_response_message));
}
carmen_spline_free_response_message* pyTklibHandler::spline_free_response_message() {
  return &the_latest_spline_free_response;
}

//ekf message
void pyTklibHandler::set_ekf_message(carmen_ekf_message *msg){
  memcpy(&the_latest_ekf_message, msg, sizeof(carmen_ekf_message));
}
carmen_ekf_message* pyTklibHandler::get_carmen_ekf_message() {return &the_latest_ekf_message;}



//gridmapping pose message
void pyTklibHandler::set_gridmapping_pose_message(carmen_gridmapping_pose_message *msg){
  memcpy(&the_latest_gridmapping_pose_message, msg, sizeof(carmen_gridmapping_pose_message));
}
carmen_gridmapping_pose_message* pyTklibHandler::get_gridmapping_pose_message(){
  return &the_latest_gridmapping_pose_message;
}

void pyTklibHandler::set_gridmapping_ray_trace_message(carmen_gridmapping_ray_trace_message *msg){
  memcpy(&the_latest_gridmapping_ray_trace_message, msg, sizeof(carmen_gridmapping_ray_trace_message));
}
carmen_gridmapping_ray_trace_message* pyTklibHandler::get_gridmapping_ray_trace_message(){
  return &the_latest_gridmapping_ray_trace_message;
}

void pyTklibHandler::set_gridmapping_map_message(carmen_gridmapping_map_message *msg){
  memcpy(&the_latest_gridmapping_map_message, msg, sizeof(carmen_gridmapping_map_message));
}
carmen_gridmapping_map_message* pyTklibHandler::get_gridmapping_map_message(){
  return &the_latest_gridmapping_map_message;
}


//trajopt config message
void pyTklibHandler::set_trajopt_config_message(carmen_trajopt_destinations_config_message *msg){
  memcpy(&the_latest_trajopt_config, msg, sizeof(carmen_trajopt_destinations_config_message));
}
carmen_trajopt_destinations_config_message* pyTklibHandler::get_trajopt_config_message(){
  return &the_latest_trajopt_config;
}


//trajopt set destinations message
void pyTklibHandler::set_trajopt_destinations_message(carmen_trajopt_set_destinations_message *msg){
  memcpy(&the_latest_trajopt_destinations, msg, sizeof(carmen_trajopt_set_destinations_message));
}


gsl_matrix* pyTklibHandler::get_trajopt_destinations_message(){
  gsl_vector* myX = tklib_double_to_gsl_vector(the_latest_trajopt_destinations.x, 
					       the_latest_trajopt_destinations.num_destinations);
  gsl_vector* myY = tklib_double_to_gsl_vector(the_latest_trajopt_destinations.y, 
					       the_latest_trajopt_destinations.num_destinations);
  
  gsl_matrix* destinations = gsl_matrix_alloc(2, the_latest_trajopt_destinations.num_destinations);
  gsl_matrix_set_row(destinations, 0, myX);
  gsl_matrix_set_row(destinations, 1, myY);

  return destinations;
}


//trajopt set go message
void pyTklibHandler::set_trajopt_go_message(carmen_trajopt_go_message *msg){
  memcpy(&the_latest_go_msg, msg, sizeof(carmen_trajopt_go_message));
}
carmen_trajopt_go_message* pyTklibHandler::get_trajopt_go_message(){
  return &the_latest_go_msg;
}

//trajopt set stop message
void pyTklibHandler::set_trajopt_stop_message(carmen_trajopt_stop_message *msg){
  memcpy(&the_latest_stop_msg, msg, sizeof(carmen_trajopt_stop_message));
}
carmen_trajopt_stop_message* pyTklibHandler::get_trajopt_stop_message(){
  return &the_latest_stop_msg;
}




/******************************************/
/********  Callback Handlers      ********/
/******************************************/

//spline free request
static pyTklibHandler *_spline_free_callback;


void subscribe_spline_free_request_message::my_handler(carmen_spline_free_request_message *msg) 
{
  _spline_free_callback->set_spline_free_request_message(msg);
  if (_spline_free_callback) _spline_free_callback->run_cb((char*)"spline_free_request", (char*)"spline_free_request_message()");
}

subscribe_spline_free_request_message::subscribe_spline_free_request_message(pyTklibHandler *cb)
{
  _spline_free_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_SPLINE_FREE_REQUEST_MESSAGE_NAME,
			   (char*)CARMEN_SPLINE_FREE_REQUEST_MESSAGE_FMT,
			   NULL, sizeof(carmen_spline_free_request_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}


//spline_free result
static pyTklibHandler *_spline_free_res_callback;
void subscribe_spline_free_response_message::my_handler(carmen_spline_free_response_message *msg) 
{
  _spline_free_res_callback->set_spline_free_response_message(msg);
  if (_spline_free_res_callback) _spline_free_res_callback->run_cb((char*)"spline_free_response", (char*)"spline_free_response_message()");
}

subscribe_spline_free_response_message::subscribe_spline_free_response_message(pyTklibHandler *cb)
{
  _spline_free_res_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_NAME,
			   (char*)CARMEN_SPLINE_FREE_RESPONSE_MESSAGE_FMT,
			   NULL, sizeof(carmen_spline_free_response_message), 
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}



//ekf message
static pyTklibHandler *_ekf_callback;
void subscribe_ekf_message::my_handler(carmen_ekf_message *msg) 
{
  _ekf_callback->set_ekf_message(msg);
  if (_ekf_callback) _ekf_callback->run_cb((char*)"ekf_message", (char*)"get_carmen_ekf_message()");
}

subscribe_ekf_message::subscribe_ekf_message(pyTklibHandler *cb)
{
  _ekf_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_EKF_MESSAGE_NAME,
			   (char*)CARMEN_EKF_MESSAGE_FMT,
			   NULL, sizeof(carmen_ekf_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
  
}


//gridmapping pose message
static pyTklibHandler *_gridmapping_pose_callback;
subscribe_gridmapping_pose_message::subscribe_gridmapping_pose_message(pyTklibHandler *cb){
  _gridmapping_pose_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_GRIDMAPPING_POSE_NAME, 
			   (char*)CARMEN_GRIDMAPPING_POSE_FMT, 
			   NULL, sizeof(carmen_gridmapping_pose_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}

void subscribe_gridmapping_pose_message::my_handler(carmen_gridmapping_pose_message *msg){
  _gridmapping_pose_callback->set_gridmapping_pose_message(msg);
  if (_gridmapping_pose_callback) _gridmapping_pose_callback->run_cb((char*)"gridmapping_pose_message", 
								     (char*)"get_gridmapping_pose_message()");
}

static pyTklibHandler *_gridmapping_ray_trace_callback;
subscribe_gridmapping_ray_trace_message::subscribe_gridmapping_ray_trace_message(pyTklibHandler *cb){
  _gridmapping_ray_trace_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_GRIDMAPPING_RAY_TRACE_NAME, 
			   (char*)CARMEN_GRIDMAPPING_RAY_TRACE_FMT, 
			   NULL, sizeof(carmen_gridmapping_ray_trace_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}
void subscribe_gridmapping_ray_trace_message::my_handler(carmen_gridmapping_ray_trace_message *msg){
    _gridmapping_ray_trace_callback->set_gridmapping_ray_trace_message(msg);
    if (_gridmapping_ray_trace_callback) _gridmapping_ray_trace_callback->run_cb((char*)"gridmapping_ray_trace_message", 
										 (char*)"get_gridmapping_ray_trace_message()");
}


static pyTklibHandler *_gridmapping_map_callback;
subscribe_gridmapping_map_message::subscribe_gridmapping_map_message(pyTklibHandler *cb){
  _gridmapping_map_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_GRIDMAPPING_MAP_NAME, 
			   (char*)CARMEN_GRIDMAPPING_MAP_FMT, 
			   NULL, sizeof(carmen_gridmapping_map_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}
void subscribe_gridmapping_map_message::my_handler(carmen_gridmapping_map_message *msg){
    _gridmapping_map_callback->set_gridmapping_map_message(msg);
    if (_gridmapping_map_callback) _gridmapping_map_callback->run_cb((char*)"gridmapping_map_message", 
								     (char*)"get_gridmapping_map_message()");
}



//trajopt configuration parameters... only one for now
static pyTklibHandler *_trajopt_config_callback;
subscribe_trajopt_config_message::subscribe_trajopt_config_message(pyTklibHandler *cb){
  _trajopt_config_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_TRAJOPT_DESTINATIONS_CONFIG_NAME,
			   (char*)CARMEN_TRAJOPT_DESTINATIONS_CONFIG_FMT,
			   NULL, sizeof(carmen_trajopt_destinations_config_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}
void subscribe_trajopt_config_message::my_handler(carmen_trajopt_destinations_config_message *msg){
  _trajopt_config_callback->set_trajopt_config_message(msg);
  if (_trajopt_config_callback) _trajopt_config_callback->run_cb((char*)"trajopt_config_message", 
								 (char*)"get_trajopt_config_message()");
}


//trajopt destinations to move to
static pyTklibHandler *_trajopt_destinations_callback;
subscribe_trajopt_destinations_message::subscribe_trajopt_destinations_message(pyTklibHandler *cb){
  _trajopt_destinations_callback = cb;

  carmen_subscribe_message((char*)CARMEN_TRAJOPT_SET_DESTINATIONS_NAME,
			   (char*)CARMEN_TRAJOPT_SET_DESTINATIONS_FMT,
			   NULL, sizeof(carmen_trajopt_set_destinations_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}

void subscribe_trajopt_destinations_message::my_handler(carmen_trajopt_set_destinations_message *msg){
  _trajopt_destinations_callback->set_trajopt_destinations_message(msg);
  if (_trajopt_destinations_callback) _trajopt_destinations_callback->run_cb((char*)"trajopt_destinations_message", 
									     (char*)"get_trajopt_destinations_message()");
}

//trajopt go message
static pyTklibHandler *_trajopt_go_callback;
//trajopt go message
subscribe_trajopt_go_message::subscribe_trajopt_go_message(pyTklibHandler *cb){
  _trajopt_go_callback = cb;
  carmen_subscribe_message((char*)CARMEN_TRAJOPT_GO_NAME,
			   (char*)CARMEN_TRAJOPT_GO_FMT, 
			   NULL, sizeof(carmen_trajopt_go_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}
void subscribe_trajopt_go_message::my_handler(carmen_trajopt_go_message *msg){
  _trajopt_go_callback->set_trajopt_go_message(msg);
  if (_trajopt_go_callback) _trajopt_go_callback->run_cb((char*)"trajopt_go_message", 
							 (char*)"get_trajopt_go_message()");
}

//trajopt stop message
static pyTklibHandler *_trajopt_stop_callback;
//trajopt stop message
subscribe_trajopt_stop_message::subscribe_trajopt_stop_message(pyTklibHandler *cb){
  _trajopt_stop_callback = cb;
  carmen_subscribe_message((char*)CARMEN_TRAJOPT_STOP_NAME,
			   (char*)CARMEN_TRAJOPT_STOP_FMT, 
			   NULL, sizeof(carmen_trajopt_stop_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);

}
void subscribe_trajopt_stop_message::my_handler(carmen_trajopt_stop_message *msg){
  _trajopt_stop_callback->set_trajopt_stop_message(msg);
  if (_trajopt_stop_callback) _trajopt_stop_callback->run_cb((char*)"trajopt_stop_message", 
							     (char*)"get_trajopt_stop_message()");
}


//spline free request
static pyTklibHandler *_curr_spline_callback;
void subscribe_trajopt_curr_spline_message::my_handler(carmen_trajopt_curr_spline_message *msg) 
{
  _curr_spline_callback->set_curr_spline_message(msg);
  if (_curr_spline_callback) _curr_spline_callback->run_cb((char*)"curr_spline", (char*)"get_curr_spline_message()");
}

subscribe_trajopt_curr_spline_message::subscribe_trajopt_curr_spline_message(pyTklibHandler *cb)
{
  _curr_spline_callback = cb;
  
  carmen_subscribe_message((char*)CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_NAME,
			   (char*)CARMEN_TRAJOPT_CURR_SPLINE_MESSAGE_FMT,
			   NULL, sizeof(carmen_trajopt_curr_spline_message),
			   (carmen_handler_t)my_handler, CARMEN_SUBSCRIBE_LATEST);
}
