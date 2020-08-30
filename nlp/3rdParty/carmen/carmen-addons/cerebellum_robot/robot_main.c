/*********************************************************
 *
 * This source code is part of the Carnegie Mellon Robot
 * Navigation Toolkit (CARMEN)
 *
 * CARMEN Copyright (c) 2002 Michael Montemerlo, Nicholas
 * Roy, and Sebastian Thrun
 *
 * CARMEN is free software; you can redistribute it and/or 
 * modify it under the terms of the GNU General Public 
 * License as published by the Free Software Foundation; 
 * either version 2 of the License, or (at your option)
 * any later version.
 *
 * CARMEN is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied 
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more 
 * details.
 *
 * You should have received a copy of the GNU General 
 * Public License along with CARMEN; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place, 
 * Suite 330, Boston, MA  02111-1307 USA
 *
 ********************************************************/

#include <carmen/carmen.h>

#include "robot_laser.h"
#include "robot_sonar.h"

#include "robot.h"

carmen_robot_config_t carmen_robot_config;
char *carmen_robot_host;
carmen_base_odometry_message carmen_robot_latest_odometry;
carmen_base_odometry_message carmen_robot_odometry[MAX_READINGS];

int carmen_robot_converge = 1;
double carmen_robot_collision_avoidance_frequency = 1;
double carmen_robot_laser_bearing_skip_rate = 0;
double turn_before_driving_if_heading_bigger_than = M_PI/2;

static double current_time;

static double odometry_local_timestamp[MAX_READINGS];

static int use_sonar = 1;
static int use_laser = 1;

static int collision_avoidance = 1;

// Don't change; 3d controller isn't ready for main distribution yet - Jared Glover
static int use_3d_control = 0;
static double control_lookahead = 1000.0;
static double control_lookahead_approach_dist = 5.0;

static double theta_gain;
static double theta_d_gain;
static double disp_gain;
static double robot_timeout;
static double command_tv = 0, command_rv = 0;
static double time_of_last_command;

static carmen_traj_point_t start_position;
static carmen_traj_point_t goal;
static double vector_distance;
static double vector_angle;
static int following_vector = 0;
static int following_trajectory = 0;

static void publish_vector_status(double distance, double angle);

inline double 
carmen_robot_get_odometry_skew(void)
{
  if(strcmp(carmen_robot_host, carmen_robot_latest_odometry.host) == 0)
    return 0;  
  else 
    return carmen_running_average_report(ODOMETRY_AVERAGE);
}

double 
carmen_robot_interpolate_heading(double head1, double head2, double fraction)
{
  double result;

  if(head1 > 0 && head2 < 0 && head1 - head2 > M_PI) 
    {
      head2 += 2 * M_PI;
      result = head1 + fraction * (head2 - head1);
      if(result > M_PI)
	result -= 2 * M_PI;
      return result;
    }
  else if(head1 < 0 && head2 > 0 && head2 - head1 > M_PI) 
    {
      head1 += 2 * M_PI;
      result = head1 + fraction * (head2 - head1);
      if(result > M_PI)
	result -= 2 * M_PI;
      return result;
    }
  else
    return head1 + fraction * (head2 - head1);
}

void 
carmen_robot_send_base_velocity_command(void)
{
  IPC_RETURN_TYPE err;
  char *host;
  static carmen_base_velocity_message v;
  static int first = 1;

  if(first) {
    host = carmen_get_tenchar_host_name();
    strcpy(v.host, host);
    first = 0;
  }

  v.tv = carmen_clamp(-carmen_robot_config.max_t_vel, command_tv, 
		      carmen_robot_config.max_t_vel);
  v.rv = carmen_clamp(-carmen_robot_config.max_r_vel, command_rv,
		      carmen_robot_config.max_r_vel);
  
  v.timestamp = carmen_get_time_ms();
  
  err = IPC_publishData(CARMEN_BASE_VELOCITY_NAME, &v);
  carmen_test_ipc(err, "Could not publish", CARMEN_BASE_VELOCITY_NAME);  
}

void 
carmen_robot_stop_robot(int how)
{
  command_tv = 0.0;
  if (how == ALL_STOP)
    command_rv = 0.0;
  if (following_vector || following_trajectory)
    command_rv = 0.0;
  following_vector = 0;
  following_trajectory = 0;
  publish_vector_status(0, 0);

  printf("STOP ROBOT!!!\n");

  carmen_robot_send_base_velocity_command();
}

static void 
base_odometry_handler(void)
{
  int i;

  for(i = 0; i < MAX_READINGS - 1; i++) {
    carmen_robot_odometry[i] = carmen_robot_odometry[i + 1];
    odometry_local_timestamp[i] = odometry_local_timestamp[i + 1];
  }
  carmen_robot_odometry[MAX_READINGS - 1] = carmen_robot_latest_odometry;
  odometry_local_timestamp[MAX_READINGS - 1] = carmen_get_time_ms();

  carmen_running_average_add(ODOMETRY_AVERAGE, 
			     odometry_local_timestamp[MAX_READINGS - 1]- 
			     carmen_robot_latest_odometry.timestamp);

  if (collision_avoidance) 
    {
      if (carmen_robot_latest_odometry.tv > 0 &&
	  carmen_robot_laser_max_front_velocity() < 
	  carmen_robot_latest_odometry.tv &&
	  command_tv > carmen_robot_laser_max_front_velocity())
	{
	  if (carmen_robot_laser_max_front_velocity() <= 0.0)
	    {
	      command_tv = 0;
	      fprintf(stderr, "S");
	      carmen_robot_stop_robot(ALLOW_ROTATE);
	    }
	  else 
	    {
	      command_tv = carmen_robot_laser_max_front_velocity();
	      carmen_robot_send_base_velocity_command();
	    }
	} 
      else if (carmen_robot_latest_odometry.tv < 0 &&
	       carmen_robot_laser_min_rear_velocity() >
	       carmen_robot_latest_odometry.tv &&
	       command_tv < carmen_robot_laser_min_rear_velocity())
	{
	  if (carmen_robot_laser_min_rear_velocity() >= 0.0)
	    {
	      fprintf(stderr, "S");
	      command_tv = 0;
	      carmen_robot_stop_robot(ALLOW_ROTATE);
	    }
	  else 
	    {
	      command_tv = carmen_robot_laser_min_rear_velocity();
	      carmen_robot_send_base_velocity_command();
	    }
	} 
    } // End of if (collision_avoidance)

  if (use_laser)
    carmen_robot_correct_laser_and_publish();
  if (use_sonar)
    carmen_robot_correct_sonar_and_publish();
}

static void
publish_vector_status(double distance, double angle)
{
  static carmen_robot_vector_status_message msg;
  static int first = 1;
  int err;

  if (first) {
    strcpy(msg.host, carmen_get_tenchar_host_name());
    first = 0;
  }
  msg.timestamp = carmen_get_time_ms();
  msg.vector_distance = distance;
  msg.vector_angle = angle;

  err = IPC_publishData(CARMEN_ROBOT_VECTOR_STATUS_NAME, &msg);
  carmen_test_ipc(err, "Could not publish", CARMEN_ROBOT_VECTOR_STATUS_NAME);  
}

static void 
velocity_handler(MSG_INSTANCE msgRef, BYTE_ARRAY callData,
		 void *clientData __attribute__ ((unused)))
{
  carmen_robot_velocity_message v;
  FORMATTER_PTR formatter;
  IPC_RETURN_TYPE err;

  formatter = IPC_msgInstanceFormatter(msgRef);
  err = IPC_unmarshallData(formatter, callData, &v,
			   sizeof(carmen_robot_velocity_message));  
  IPC_freeByteArray(callData);

  carmen_test_ipc_return(err, "Could not unmarshall", 
			 IPC_msgInstanceName(msgRef));

  time_of_last_command = carmen_get_time_ms();

  command_rv = v.rv;
  command_tv = v.tv;

  if (collision_avoidance) 
    {
      if (use_laser)
	command_tv = carmen_clamp(carmen_robot_laser_min_rear_velocity(), 
				  command_tv,
				  carmen_robot_laser_max_front_velocity());
      if (use_sonar)
	command_tv = carmen_clamp(carmen_robot_sonar_min_rear_velocity(), 
				  command_tv,
				  carmen_robot_sonar_max_front_velocity());
    }

  if (!carmen_robot_config.allow_rear_motion && command_tv < 0)
    command_tv = 0.0;

  following_vector = following_trajectory = 0;
  printf("velocity handler\n");
  carmen_robot_send_base_velocity_command();
  publish_vector_status(0, 0);
}

static void
follow_vector(void)
{
  double true_angle_difference, angle_difference, displacement;
  double dt = .1;
  /*double radius;*/
  /*int backwards = 0;*/

  true_angle_difference = angle_difference = vector_angle;
  displacement = vector_distance;

  /*   double angle_change =  */
  /*     carmen_normalize_theta(carmen_robot_latest_odometry.theta -  */
  /* 			   start_position.theta); */
  /*   double distance_change =  */
  /*     hypot(carmen_robot_latest_odometry.x-start_position.x, */
  /* 	  carmen_robot_latest_odometry.y-start_position.y); */

  /*   angle_difference = carmen_normalize_theta(vector_angle-angle_change);	 */

  /*   carmen_verbose("angle: o %f s %f : v %f d: %f\n",  */
  /* 		 carmen_robot_latest_odometry.theta, */
  /* 		 start_position.theta, vector_angle, angle_difference); */

  /*   if (fabs(vector_distance) > 0.0) */
  /*     displacement = vector_distance-distance_change; */
  /*   else */
  /*     displacement = 0.0; */

  /*   if (fabs(angle_difference) < carmen_degrees_to_radians(5.0) && */
  /*       fabs(displacement) < carmen_robot_config.approach_dist)  */
  /*     { */
  /*       command_tv = 0; */
  /*       command_rv = 0; */
  /*       following_vector = 0;		 */
  /*       carmen_robot_stop_robot(ALL_STOP); */
  /*       publish_vector_status(0, 0); */
  /*       printf("stopping: dest\n"); */
  /*       return; */
  /*     } */

  /*   true_angle_difference = angle_difference; */

  /*   if (carmen_robot_config.allow_rear_motion &&  */
  /*       (angle_difference > M_PI/2 || angle_difference < -M_PI/2))  */
  /*     { */
  /*       if (!collision_avoidance ||  */
  /* 	  carmen_robot_laser_min_rear_velocity() < 0.0) { */
  /* 	backwards = 1; */
  /* 	true_angle_difference = angle_difference; */
  /* 	if (angle_difference < 0)  */
  /* 	  angle_difference += M_PI ;  */
  /* 	else */
  /* 	  angle_difference -= M_PI;  */
  /*       } */
  /*     } */

  command_rv = theta_gain*dt*angle_difference + 
    (1-theta_d_gain*dt)*carmen_robot_latest_odometry.rv;
  /*   command_rv = carmen_clamp(-carmen_robot_config.max_r_vel, command_rv, */
  /* 			    carmen_robot_config.max_r_vel); */
	
  /*   if (fabs(angle_difference) > 0.0 &&  */
  /*       carmen_radians_to_degrees(fabs(angle_difference)) < 15.0) */
  /*     command_rv -= theta_d_gain*carmen_robot_latest_odometry.rv; */
  
  if ((fabs(carmen_robot_latest_odometry.tv) <= 0.001 && 
       fabs(angle_difference) > 0.5 * turn_before_driving_if_heading_bigger_than) || 
      fabs(angle_difference) > turn_before_driving_if_heading_bigger_than)
    {
      command_tv = 0;
    }
  
  /*   else if (fabs(command_rv) > carmen_robot_config.max_r_vel / 4) */
  /*     { */
  /*       radius = fabs(displacement/4 / sin(angle_difference)); */
  /*       command_tv = fabs(radius * command_rv); */
  /*     } */
  else 
    {
      command_tv = carmen_robot_config.max_t_vel;
      /*       if (fabs(displacement) > 0 && fabs(displacement) < 0.15) */
      /* 	command_tv -= carmen_robot_latest_odometry.tv/2; */
    }
  
  /*   if (backwards) */
  /*     command_tv *= -1; */
  
  if (collision_avoidance)
    {
      if (use_laser)
	command_tv = carmen_clamp(carmen_robot_laser_min_rear_velocity(),
				  command_tv, 
				  carmen_robot_laser_max_front_velocity());
    }

  /*   if (!carmen_robot_config.allow_rear_motion && command_tv < 0) */
  /*     command_tv = 0.0; */
  publish_vector_status(displacement, true_angle_difference);
  carmen_robot_send_base_velocity_command();	
}

static void follow_trajectory_3d(void) 
{

  /* gain matrix: by rows, [ga gb, gc gd] */
  double ga, gb, gc, gd;
  double x, y, theta, cos_theta, sin_theta;
  double ahead_x, ahead_y, pursuit_x, pursuit_y, dx, dy;

  theta = carmen_normalize_theta(carmen_robot_latest_odometry.theta - start_position.theta);
  cos_theta = cos(theta);
  sin_theta = sin(theta);

  ga = cos_theta;
  gb = sin_theta;
  gc = -sin_theta / control_lookahead;
  gd = cos_theta / control_lookahead;

  x = carmen_robot_latest_odometry.x - start_position.x;
  y = carmen_robot_latest_odometry.y - start_position.y;
  ahead_x = x + cos_theta * control_lookahead;
  ahead_y = y + sin_theta * control_lookahead;

  //dbug
  pursuit_x = goal.x + /*cos(goal.theta) * */ control_lookahead;
  pursuit_y = goal.y /* + sin(goal.theta) * control_lookahead */ ;

  dx = pursuit_x - ahead_x;
  dy = pursuit_y - ahead_y;

  if (sqrt(dx*dx + dy*dy) < control_lookahead_approach_dist) {
    command_tv = 0;
    command_rv = 0;
    following_trajectory = 0;		
    carmen_robot_stop_robot(ALL_STOP);
    publish_vector_status(0, 0);
    return;
  }

  command_tv = disp_gain * (ga * dx + gb * dy);
  command_rv = disp_gain * (gc * dx + gd * dy);

  //carmen_robot_send_base_velocity_command();
}

static void 
vector_move_handler(MSG_INSTANCE msgRef, BYTE_ARRAY callData,
		    void *clientData __attribute__ ((unused)))
{
  carmen_robot_vector_move_message msg;
  FORMATTER_PTR formatter;
  IPC_RETURN_TYPE err;

  formatter = IPC_msgInstanceFormatter(msgRef);
  err = IPC_unmarshallData(formatter, callData, &msg,
			   sizeof(carmen_robot_vector_move_message));  
  IPC_freeByteArray(callData);

  carmen_test_ipc_return
    (err, "Could not unmarshall", IPC_msgInstanceName(msgRef));

  time_of_last_command = carmen_get_time_ms();

  following_vector = 1;
  if (following_trajectory)
    following_trajectory = 0;

  start_position.x = carmen_robot_latest_odometry.x;
  start_position.y = carmen_robot_latest_odometry.y;
  start_position.theta = carmen_robot_latest_odometry.theta;
  start_position.t_vel = carmen_robot_latest_odometry.tv;
  start_position.r_vel = carmen_robot_latest_odometry.rv;
  
  vector_angle = msg.theta;
  vector_distance = msg.distance;
  
  follow_vector();
}

static void 
follow_trajectory_handler(MSG_INSTANCE msgRef, BYTE_ARRAY callData,
			  void *clientData __attribute__ ((unused)))
{
  carmen_robot_follow_trajectory_message msg;
  FORMATTER_PTR formatter;
  IPC_RETURN_TYPE err;  

  formatter = IPC_msgInstanceFormatter(msgRef);
  err = IPC_unmarshallData(formatter, callData, &msg,
			   sizeof(carmen_robot_follow_trajectory_message));  
  IPC_freeByteArray(callData);

  carmen_test_ipc_return
    (err, "Could not unmarshall", IPC_msgInstanceName(msgRef));

  time_of_last_command = carmen_get_time_ms();

  if (msg.trajectory_length == 0)
    return;

  start_position.x = carmen_robot_latest_odometry.x;
  start_position.y = carmen_robot_latest_odometry.y;
  start_position.theta = carmen_robot_latest_odometry.theta;
  start_position.t_vel = carmen_robot_latest_odometry.tv;
  start_position.r_vel = carmen_robot_latest_odometry.rv;

  if (use_3d_control)
    {
      following_vector = 0;
      following_trajectory = 1;
      goal = msg.trajectory[0];
      follow_trajectory_3d();
    }
  else
    {
      following_vector = 1;
      following_trajectory = 0;

      goal = msg.trajectory[0];
      goal.x -= msg.robot_position.x;
      goal.y -= msg.robot_position.y;
      
      vector_distance = hypot(goal.x, goal.y);

      if (vector_distance < carmen_robot_config.approach_dist)
	{
	  vector_angle = carmen_normalize_theta(goal.theta);
	  vector_angle = carmen_normalize_theta(vector_angle - msg.robot_position.theta);
	}
      else
	{
	  vector_angle = carmen_normalize_theta(atan2(goal.y, goal.x));
	  vector_angle = carmen_normalize_theta(vector_angle - msg.robot_position.theta);
	}

      follow_vector();      
    }
  free(msg.trajectory);
}

static int 
initialize_robot_ipc(void)
{
  IPC_RETURN_TYPE err;

  /* define messages created by this module */
  err = IPC_defineMsg(CARMEN_ROBOT_FRONTLASER_NAME,
                      IPC_VARIABLE_LENGTH,
                      CARMEN_ROBOT_FRONTLASER_FMT);
  carmen_test_ipc_exit(err, "Could not define", CARMEN_ROBOT_FRONTLASER_NAME);

  err = IPC_defineMsg(CARMEN_ROBOT_REARLASER_NAME,
                      IPC_VARIABLE_LENGTH,
                      CARMEN_ROBOT_REARLASER_FMT);
  carmen_test_ipc_exit(err, "Could not define", CARMEN_ROBOT_REARLASER_NAME);

  err = IPC_defineMsg(CARMEN_ROBOT_SONAR_NAME,
		      IPC_VARIABLE_LENGTH,
		      CARMEN_ROBOT_SONAR_FMT);
  carmen_test_ipc_exit(err, "Could not define", CARMEN_ROBOT_SONAR_NAME);

  err = IPC_defineMsg(CARMEN_ROBOT_VELOCITY_NAME,
                      IPC_VARIABLE_LENGTH,
                      CARMEN_ROBOT_VELOCITY_FMT);
  carmen_test_ipc_exit(err, "Could not define", CARMEN_ROBOT_VELOCITY_NAME);

  err = IPC_defineMsg(CARMEN_ROBOT_VECTOR_MOVE_NAME, IPC_VARIABLE_LENGTH,
                      CARMEN_ROBOT_VECTOR_MOVE_FMT);
  carmen_test_ipc_exit(err, "Could not define", CARMEN_ROBOT_VECTOR_MOVE_NAME);

  err = IPC_defineMsg(CARMEN_ROBOT_FOLLOW_TRAJECTORY_NAME, IPC_VARIABLE_LENGTH,
                      CARMEN_ROBOT_FOLLOW_TRAJECTORY_FMT);
  carmen_test_ipc_exit(err, "Could not define", CARMEN_ROBOT_FOLLOW_TRAJECTORY_NAME);

  err = IPC_defineMsg(CARMEN_ROBOT_VECTOR_STATUS_NAME, IPC_VARIABLE_LENGTH,
                      CARMEN_ROBOT_VECTOR_STATUS_FMT);
  carmen_test_ipc_exit(err, "Could not define", 
		       CARMEN_ROBOT_VECTOR_STATUS_NAME);

  /* setup incoming message handlers */
  err = IPC_subscribe(CARMEN_ROBOT_VELOCITY_NAME, velocity_handler, NULL);
  carmen_test_ipc_exit(err, "Could not subscribe", CARMEN_ROBOT_VELOCITY_NAME);
  IPC_setMsgQueueLength(CARMEN_ROBOT_VELOCITY_NAME, 1);

  err = IPC_subscribe(CARMEN_ROBOT_VECTOR_MOVE_NAME, vector_move_handler, 
		      NULL);
  carmen_test_ipc_exit(err, "Could not subscribe", 
		       CARMEN_ROBOT_VECTOR_MOVE_NAME);
  IPC_setMsgQueueLength(CARMEN_ROBOT_VECTOR_MOVE_NAME, 1);
 
  err = IPC_subscribe(CARMEN_ROBOT_FOLLOW_TRAJECTORY_NAME, follow_trajectory_handler, 
		      NULL);

  carmen_test_ipc_exit(err, "Could not subscribe", 
		       CARMEN_ROBOT_FOLLOW_TRAJECTORY_NAME);
  IPC_setMsgQueueLength(CARMEN_ROBOT_FOLLOW_TRAJECTORY_NAME, 1);

  return 0;
}

void 
carmen_robot_shutdown(int x __attribute__ ((unused)))
{
  carmen_robot_stop_robot(ALL_STOP);
}

void 
carmen_robot_usage(char *progname, char *fmt, ...) 
{
  va_list args;

  if (fmt != NULL)
    {
      fprintf(stderr, "\n[31;1m");
      va_start(args, fmt);
      vfprintf(stderr, fmt, args);
      va_end(args);
      fprintf(stderr, "[0m\n\n");
    }
  else
    {
      fprintf(stderr, "\n");
    }

  if (strrchr(progname, '/') != NULL)
    {
      progname = strrchr(progname, '/');
      progname++;
    }

  fprintf(stderr, "Usage: %s <args> \n", progname);
  fprintf(stderr, 
	  "\t-laser {on|off}   - turn laser use on and off (default on).\n");
  fprintf(stderr, 
	  "\t-sonar {on|off}   - turn sonar use on and off (unsupported).\n");
  fprintf(stderr, 
	  "\t-converge {on|off} - turn waiting for convergence on and off.\n");
  exit(-1);
}

static int 
read_robot_parameters(int argc, char **argv)
{
  int num_items;

  carmen_param_t param_list[] = {
    {"robot", "max_t_vel", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.max_t_vel, 1, NULL},
    {"robot", "max_r_vel", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.max_r_vel, 1, NULL},
    {"robot", "min_approach_dist", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.approach_dist, 1, NULL},
    {"robot", "min_side_dist", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.side_dist, 1, NULL},
    {"robot", "length", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.length, 0, NULL},
    {"robot", "width", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.width, 0, NULL},
    {"robot", "acceleration", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.acceleration, 1, NULL},
    {"robot", "reaction_time", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.reaction_time, 0, NULL},
    {"robot", "curvature", CARMEN_PARAM_DOUBLE, 
     &carmen_robot_config.curvature, 1, NULL},
    {"robot", "theta_gain", CARMEN_PARAM_DOUBLE, &theta_gain, 1, NULL},
    {"robot", "theta_d_gain", CARMEN_PARAM_DOUBLE, &theta_d_gain, 1, NULL},
    {"robot", "displacement_gain", CARMEN_PARAM_DOUBLE, &disp_gain, 1, NULL},

    /* 3d controller isn't ready for main distribution yet - Jared Glover
     *
     * {"robot", "use_3d_control", CARMEN_PARAM_ONOFF, &use_3d_control, 1, NULL},
     * {"robot", "control_lookahead", CARMEN_PARAM_DOUBLE, &control_lookahead, 1, NULL},
     * {"robot", "control_lookahead_approach_dist", CARMEN_PARAM_DOUBLE,
     * &control_lookahead_approach_dist, 1, NULL},
     */

    {"robot", "allow_rear_motion", CARMEN_PARAM_ONOFF, 
     &carmen_robot_config.allow_rear_motion, 1, NULL},
    {"robot", "converge", CARMEN_PARAM_ONOFF, &carmen_robot_converge, 1, NULL},
    {"robot", "use_laser", CARMEN_PARAM_ONOFF, &use_laser, 1, NULL},
    {"robot", "use_sonar", CARMEN_PARAM_ONOFF, &use_sonar, 1, NULL},
    {"robot", "timeout", CARMEN_PARAM_DOUBLE, &robot_timeout, 1, NULL},
    {"robot", "collision_avoidance", CARMEN_PARAM_ONOFF, 
     &collision_avoidance, 1, NULL},
    {"robot", "collision_avoidance_frequency", CARMEN_PARAM_DOUBLE,
     &carmen_robot_collision_avoidance_frequency, 1, NULL},
    {"robot", "laser_bearing_skip_rate", CARMEN_PARAM_DOUBLE,
     &carmen_robot_laser_bearing_skip_rate, 1, NULL},

    {"robot", "turn_before_driving_if_heading_bigger_than", CARMEN_PARAM_DOUBLE,
     &turn_before_driving_if_heading_bigger_than, 1, NULL}
  };



  num_items = sizeof(param_list)/sizeof(param_list[0]);
  carmen_param_install_params(argc, argv, param_list, num_items);

  if (use_laser)
    carmen_robot_add_laser_parameters(argv[0]);
  if (use_sonar)
    carmen_robot_add_sonar_parameters(argv[0]);

  carmen_robot_config.acceleration = 0.5;
  return 0;
}

int 
carmen_robot_start(int argc, char **argv)
{
  carmen_robot_host = carmen_get_tenchar_host_name();
  
  carmen_running_average_clear(ODOMETRY_AVERAGE);
  
  if (read_robot_parameters(argc, argv) < 0)
    return -1;

  if(initialize_robot_ipc() < 0) 
    {
      carmen_warn("Error: could not connect to IPC Server\n");
      return -1;;
    }

  carmen_base_subscribe_odometry_message
    (&carmen_robot_latest_odometry, (carmen_handler_t)base_odometry_handler,
     CARMEN_SUBSCRIBE_LATEST);

  if (use_laser)
    carmen_robot_add_laser_handlers();
  if (use_sonar)
    carmen_robot_add_sonar_handler();

  return 0;
}

int
carmen_robot_run(void)
{
  current_time = carmen_get_time_ms();
  if (current_time - time_of_last_command > robot_timeout) 
    {
      if (command_tv != 0.0) {
	carmen_warn("Command timed out. Stopping robot.\n");
	carmen_robot_stop_robot(ALL_STOP);
      }
    } 
  else if (following_vector) 
    follow_vector();
  else if (following_trajectory)
    follow_trajectory_3d();

  return 1;
}
