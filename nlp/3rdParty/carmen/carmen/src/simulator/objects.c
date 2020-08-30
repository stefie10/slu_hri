/*********************************************************
 *
 * This source code is part of the Carnegie Mellon Robot
 * Navigation Toolkit (CARMEN)
 *
 * CARMEN Copyright (c) 2002 Michael Montemerlo, Nicholas
 * Roy, Sebastian Thrun, Dirk Haehnel, Cyrill Stachniss,
 * and Jared Glover
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

/****************************************
 * library to create and control random *
 * two-legged people                    *
 ****************************************/

#include <carmen/carmen.h>

#include "simulator.h"
#include "objects.h"

#define MAX_STEP  0.40  //m

static int num_objects = 0;
static int list_capacity = 0;
static carmen_traj_point_t *traj_object_list = NULL;
static carmen_object_t *object_list = NULL;

static double leg_width = .1;
static double min_dist_from_robot = .4;
static double person_speed = .3;

static void update_other_robot(carmen_object_t *object);

static void
check_list_capacity(void)
{
  if (traj_object_list == NULL) 
    {
      list_capacity = 10;
      traj_object_list = (carmen_traj_point_t *)
	calloc(10, sizeof(carmen_traj_point_t));
      carmen_test_alloc(traj_object_list);
      object_list = (carmen_object_t *)
	calloc(10, sizeof(carmen_object_t));
      carmen_test_alloc(object_list);
    } 
  else if (num_objects >= list_capacity) 
    {
      list_capacity += 10;

      traj_object_list = (carmen_traj_point_t *)
	realloc(traj_object_list, sizeof(carmen_traj_point_t)*list_capacity);
      carmen_test_alloc(traj_object_list);

      object_list = (carmen_object_t *)
	realloc(object_list, sizeof(carmen_object_t)*list_capacity);
      carmen_test_alloc(object_list);
    }
}

void
carmen_simulator_create_object(double x, double y, double theta,
			       carmen_simulator_object_t type,
			       double speed)
{
  check_list_capacity();

  if (speed == -1)
    speed = fabs(carmen_gaussian_random(0.0, person_speed/2.0) + 
		 person_speed/2.0);

  object_list[num_objects].type = type;
  object_list[num_objects].is_robot = 0;

  object_list[num_objects].x1 = x+cos(theta+M_PI/2)*MAX_STEP/4;
  object_list[num_objects].y1 = y+sin(theta+M_PI/2)*MAX_STEP/4; 
  object_list[num_objects].x2 = x-cos(theta+M_PI/2)*MAX_STEP/4;
  object_list[num_objects].y2 = y-sin(theta+M_PI/2)*MAX_STEP/4;

  object_list[num_objects].theta = theta;
  object_list[num_objects].width = leg_width;

  object_list[num_objects].tv = speed;
  object_list[num_objects].rv = 0;  

  traj_object_list[num_objects].t_vel = speed;
  traj_object_list[num_objects].r_vel = speed;
  traj_object_list[num_objects].x = x;
  traj_object_list[num_objects].y = y;
  traj_object_list[num_objects].theta = theta;

  num_objects++; 
}

static int
in_map(double x, double y, carmen_map_p map)
{
  int map_x, map_y;
  double occupancy;

  map_x = carmen_trunc(x / map->config.resolution);
  map_y = carmen_trunc(y / map->config.resolution);

  if (map_x < 0 || map_x > map->config.x_size ||
      map_y < 0 || map_y > map->config.y_size) {
    return 0;
  }

  occupancy = map->map[map_x][map_y];
 
  if (occupancy > 0.15 || occupancy < 0) 
    return 0;

  return 1;
}

/* randomly updates the person's position based on its velocity */
static void 
update_random_object(int i, 
		     carmen_simulator_config_t *simulator_config)
{
  carmen_object_t new;
  double vx, vy;
  double separation;
  double dist;

  double mean_x, mean_y, delta_x, delta_y;

  new = object_list[i];
  if (!new.is_robot) 
    {
      separation = hypot(new.x1 - new.x2, new.y1 - new.y2);
      if(separation > MAX_STEP)
	{      
	  mean_x = (new.x1+new.x2)/2;
	  mean_y = (new.y1+new.y2)/2;
	  
	  delta_x = fabs((new.x1 - new.x2)/2);
	  delta_y = fabs((new.y1 - new.y2)/2);
	  
	  new.x1 = carmen_gaussian_random(mean_x, delta_x);
	  new.x2 = carmen_gaussian_random(mean_x, delta_x);
	  new.y1 = carmen_gaussian_random(mean_y, delta_y);
	  new.y2 = carmen_gaussian_random(mean_y, delta_y);
	}
      else
	{
	  vx = new.tv * cos(new.theta) * simulator_config->delta_t;
	  vy = new.tv * sin(new.theta) * simulator_config->delta_t; 
	  new.x1 += carmen_gaussian_random(vx, vx/10.0);
	  new.x2 += carmen_gaussian_random(vx, vx/10.0);
	  new.y1 += carmen_gaussian_random(vy, vy/10.0);
	  new.y2 += carmen_gaussian_random(vy, vy/10.0);
	  
	}
      
      dist = hypot((new.x1+new.x2)/2.0-simulator_config->true_pose.x, 
		   (new.y1+new.y2)/2.0-simulator_config->true_pose.y);
      
      if (!in_map(new.x1, new.y1, &(simulator_config->map)) || 
	  !in_map(new.x2, new.y2, &(simulator_config->map)) || 
	  dist < min_dist_from_robot ||
	  carmen_simulator_object_too_close(new.x1, new.y1, i) ||
	  carmen_simulator_object_too_close(new.x2, new.y2, i))
	{      
	  object_list[i].theta = carmen_normalize_theta
	    (carmen_gaussian_random(M_PI+object_list[i].theta, M_PI/4));
	  return;
	}
    }
  else
    {
      vx = new.tv * cos(new.theta) * simulator_config->delta_t;
      vy = new.tv * sin(new.theta) * simulator_config->delta_t; 
      new.x1 += carmen_gaussian_random(vx, vx/10.0);
      new.y1 += carmen_gaussian_random(vy, vy/10.0);

      dist = hypot(new.x1-simulator_config->true_pose.x, 
		   new.y1-simulator_config->true_pose.y);

      if (!in_map(new.x1, new.y1, &(simulator_config->map)) || 
	  dist < min_dist_from_robot ||
	  carmen_simulator_object_too_close(new.x1, new.y1, i))
	{      
	  object_list[i].theta = carmen_normalize_theta
	    (carmen_gaussian_random(M_PI+object_list[i].theta, M_PI/4));
	  
	  return;
	}
    }
  object_list[i] = new;
  object_list[i].time_of_last_update = carmen_get_time();
}

static void 
update_line_follower(carmen_object_t * object, 
		     carmen_simulator_config_t *simulator_config)
{
  carmen_object_t new;
  double vx, vy;
  double separation;
  double dist = 0;

  double mean_x, mean_y, delta_x, delta_y;

  new = *object;

  if (!object->is_robot) 
    {
      separation = hypot(new.x1 - new.x2, new.y1 - new.y2);
      
      if(separation > MAX_STEP)
	{      
	  mean_x = (new.x1+new.x2)/2;
	  mean_y = (new.y1+new.y2)/2;
	  
	  delta_x = fabs((new.x1 - new.x2)/2);
	  delta_y = fabs((new.y1 - new.y2)/2);
	  
	  new.x1 = carmen_gaussian_random(mean_x, delta_x);
	  new.x2 = carmen_gaussian_random(mean_x, delta_x);
	  new.y1 = carmen_gaussian_random(mean_y, delta_y);
	  new.y2 = carmen_gaussian_random(mean_y, delta_y);
	}
      else
	{
	  vx = new.tv * cos(new.theta) * simulator_config->delta_t;
	  vy = new.tv * sin(new.theta) * simulator_config->delta_t; 
	  new.x1 += carmen_gaussian_random(vx, vx/10.0);
	  new.x2 += carmen_gaussian_random(vx, vx/10.0);
	  new.y1 += carmen_gaussian_random(vy, vy/10.0);
	  new.y2 += carmen_gaussian_random(vy, vy/10.0);
	  
	}
      
      dist = hypot((object->x1+object->x2)/2.0-simulator_config->true_pose.x, 
		   (object->y1+object->y2)/2.0-simulator_config->true_pose.y);
      
      if (!in_map(new.x1, new.y1, &(simulator_config->map)) || 
	  !in_map(new.x2, new.y2, &(simulator_config->map)) || 
	  dist < min_dist_from_robot)
	{      
	  return;
	}
    }
  else
    {
      vx = new.tv * cos(new.theta) * simulator_config->delta_t;
      vy = new.tv * sin(new.theta) * simulator_config->delta_t; 
      new.x1 += carmen_gaussian_random(vx, vx/10.0);
      new.y1 += carmen_gaussian_random(vy, vy/10.0);

      dist = hypot(object->x1-simulator_config->true_pose.x, 
		   object->y1-simulator_config->true_pose.y);
      
      if (!in_map(new.x1, new.y1, &(simulator_config->map)) || 
	  dist < min_dist_from_robot)
	{      
	  return;
	}
    }
  *object = new;
  object->time_of_last_update = carmen_get_time();
}


static void
update_traj_object(int index)
{
  if (object_list[index].type == CARMEN_SIMULATOR_OTHER_ROBOT) 
    {
      traj_object_list[index].x = object_list[index].x1;
      traj_object_list[index].y = object_list[index].y1;
      traj_object_list[index].theta = object_list[index].theta;
      traj_object_list[index].t_vel = object_list[index].tv;
      traj_object_list[index].r_vel = object_list[index].rv;
    }
  else
    {
      traj_object_list[index].x = 
	(object_list[index].x1+object_list[index].x2)/2.0;
      traj_object_list[index].y = 
	(object_list[index].y1+object_list[index].y2)/2.0;
      traj_object_list[index].theta = object_list[index].theta;
      traj_object_list[index].t_vel = object_list[index].tv;
    }
}

/* updates all objects */
void 
carmen_simulator_update_objects(carmen_simulator_config_t *simulator_config)
{
  int index;

  for (index = 0; index < num_objects; index++) 
    {
      if (object_list[index].type == CARMEN_SIMULATOR_RANDOM_OBJECT) 
	update_random_object(index, simulator_config);
      else if (object_list[index].type == CARMEN_SIMULATOR_LINE_FOLLOWER) 
	update_line_follower(object_list+index, simulator_config);
      else if (object_list[index].type == CARMEN_SIMULATOR_OTHER_ROBOT)
	update_other_robot(object_list+index);
      update_traj_object(index);
    }
  return;

}

static void
add_object_to_laser(double object_x, double object_y, double width,
		    carmen_laser_laser_message *laser,
		    carmen_simulator_config_t *simulator_config, int is_rear)
{
  double phi, angle_diff;
  int index, i;
  //double separation = M_PI/laser->num_readings;
  double separation;
  double lwidth;
  double dist;
  carmen_point_t robot;
  carmen_simulator_laser_config_t *laser_config;

  robot = simulator_config->true_pose;


  if (is_rear) {
    laser_config = &(simulator_config->rear_laser_config);
  } 
  else  {
    laser_config = &(simulator_config->front_laser_config);
  }

  robot.x = simulator_config->true_pose.x 
    + laser_config->offset *  cos(simulator_config->true_pose.theta) 
    - laser_config->side_offset *  sin(simulator_config->true_pose.theta) ;

  robot.y = simulator_config->true_pose.y 
    + laser_config->offset * sin(simulator_config->true_pose.theta)
    + laser_config->side_offset * cos(simulator_config->true_pose.theta);

  robot.theta = carmen_normalize_theta(simulator_config->true_pose.theta +
				       laser_config->angular_offset);


  separation = laser_config->fov/laser->num_readings;
  phi = atan2(object_y - robot.y, object_x - robot.x);
  angle_diff = carmen_normalize_theta(phi - robot.theta);

  if (fabs(angle_diff) >=  0.5*laser_config->fov)
    return;

  //index = carmen_normalize_theta(angle_diff+M_PI/2) / separation;
  index = carmen_normalize_theta(angle_diff+laser_config->fov/2) / separation;
  dist = hypot(object_x - robot.x, object_y - robot.y);
			
  if (dist >= laser_config->max_range)
    return;	

  //lwidth = width / (double)(dist) / M_PI * laser->num_readings/2;
  lwidth = width / (double)(dist) / laser_config->fov * laser->num_readings/2;
  i = carmen_fmax(index - lwidth, 0);

  for(; i < index + lwidth && i < laser->num_readings; i++)
    {
      if(laser->range[i] > dist)
	laser->range[i] = dist;
    }
} 
 
static void
add_object_to_sonar(double object_x, double object_y, double width,
		    carmen_base_sonar_message *base_sonar,
		    carmen_simulator_config_t *simulator_config)
{
  double phi, angle_diff;
  int j, i;
  double separation = M_PI/base_sonar->num_sonars;
  double lwidth;
  double dist;
  carmen_point_t robot;

  robot = simulator_config->true_pose;

  phi = atan2(object_y - robot.y, object_x - robot.x);
  angle_diff = carmen_normalize_theta(phi - robot.theta);
  if (fabs(angle_diff) >=M_PI/2)
    return;

  j = carmen_normalize_theta(angle_diff+M_PI/2) / separation;
  dist = hypot(object_x - robot.x, object_y - robot.y);

  lwidth = width / (double)(dist) / M_PI * base_sonar->num_sonars;
  i = carmen_fmax(j - lwidth, 0);
  for(; i < j + lwidth && i < base_sonar->num_sonars; i++)
    {
      if(base_sonar->range[i] > dist)
	base_sonar->range[i] = dist;
    }
}

/* modifies the laser reading to acount for objects near the robot */
void 
carmen_simulator_add_objects_to_laser(carmen_laser_laser_message * laser, 
				      carmen_simulator_config_t 
				      *simulator_config, int is_rear)
{
  int index;
  for (index = 0; index < num_objects; index++)
    {
      add_object_to_laser(object_list[index].x1, object_list[index].y1, 
			  object_list[index].width, laser, simulator_config, 
			  is_rear);
      if (!object_list[index].is_robot)
	add_object_to_laser(object_list[index].x2, object_list[index].y2, 
			    object_list[index].width, laser, simulator_config, 
			    is_rear);
    }
}

void
carmen_simulator_add_objects_to_sonar(carmen_base_sonar_message * base_sonar, 
				      carmen_simulator_config_t 
				      *simulator_config)
{
  double dist;
  int index;
  for (index = 0; index < num_objects; index++)
    {
      dist = hypot((object_list[index].x1+object_list[index].x2)/2.0-
		   simulator_config->true_pose.x,
		   (object_list[index].y1+object_list[index].y2)/2.0-
		   simulator_config->true_pose.y);
      if( dist >= simulator_config->sonar_config.max_range)
	continue;
      add_object_to_sonar(object_list[index].x1, object_list[index].y1,
			  object_list[index].width, base_sonar, 
			  simulator_config);
      add_object_to_sonar(object_list[index].x2, object_list[index].y2, 
			  object_list[index].width, base_sonar, 
			  simulator_config);
    }
}

/* frees all objects */
void 
carmen_simulator_clear_objects(void)
{
  num_objects = 0;
}

/* gets the possitions of all the objects */
void 
carmen_simulator_get_object_poses(int * num, 
				  carmen_traj_point_t ** coordinates)
{
  *num = num_objects;
  *coordinates = traj_object_list;
}

void
carmen_simulator_initialize_object_model(int argc, char *argv[])
{
  carmen_param_t param_list[] = {
    {"simulator", "person_leg_width", CARMEN_PARAM_DOUBLE,
     &leg_width, 1, NULL},
    {"simulator", "person_dist_from_robot", CARMEN_PARAM_DOUBLE,
     &min_dist_from_robot, 1, NULL},
    {"simulator", "person_speed", CARMEN_PARAM_DOUBLE,
     &person_speed, 1, NULL}};

  int num_items = sizeof(param_list)/sizeof(param_list[0]);
  carmen_param_install_params(argc, argv, param_list, num_items);
}

static carmen_object_t *
find_object(IPC_CONTEXT_PTR context)
{
  int i;

  for (i = 0; i < num_objects; i++) 
    {
      if (object_list[i].type == CARMEN_SIMULATOR_OTHER_ROBOT &&
	  object_list[i].context == context)
	return object_list+i;
    }
  return NULL;
}

static void
globalpos_handler(carmen_localize_globalpos_message *msg) 
{
  IPC_CONTEXT_PTR context;
  carmen_object_t *object;

  context = IPC_getContext();
  object = find_object(context);
  if (object == NULL)
    return;
  if (carmen_get_time() - object->time_of_last_update > 10) 
    {
      object->x1 = msg->globalpos.x;
      object->y1 = msg->globalpos.y;
      object->theta = msg->globalpos.theta;
      object->time_of_last_update = carmen_get_time();
    }
}

static void 
simulator_handler(MSG_INSTANCE msgRef, BYTE_ARRAY callData,
		  void *clientData __attribute__ ((unused)))
{
  IPC_RETURN_TYPE err = IPC_OK;
  FORMATTER_PTR formatter;
  carmen_simulator_truepos_message msg;
  IPC_CONTEXT_PTR context;
  carmen_object_t *object;

  formatter = IPC_msgInstanceFormatter(msgRef);
  err = IPC_unmarshallData(formatter, callData, &msg, 
			   sizeof(carmen_simulator_truepos_message));
  IPC_freeByteArray(callData);

  carmen_test_ipc_return(err, "Could not unmarshall", 
			 IPC_msgInstanceName(msgRef));

  context = IPC_getContext();
  object = find_object(context);
  if (object == NULL)
    return;

  object->x1 = msg.truepose.x;
  object->y1 = msg.truepose.y;
  object->theta = msg.truepose.theta;
  object->time_of_last_update = carmen_get_time();
}

void 
carmen_simulator_add_robot(char *program_name, char *robot_central)
{
  char buffer[1024];
  IPC_CONTEXT_PTR current_context;

  current_context = IPC_getContext();

  check_list_capacity();

  sprintf(buffer, "%s_%d", program_name, getpid());
  IPC_connectModule(program_name, robot_central);

  object_list[num_objects].context = IPC_getContext();

  if (IPC_isMsgDefined(CARMEN_SIMULATOR_TRUEPOS_NAME)) 
    {
      IPC_subscribe(CARMEN_SIMULATOR_TRUEPOS_NAME, simulator_handler, NULL);
      IPC_setMsgQueueLength(CARMEN_SIMULATOR_TRUEPOS_NAME, 1);
    }
  else
    carmen_localize_subscribe_globalpos_message
      (NULL, (carmen_handler_t)globalpos_handler, CARMEN_SUBSCRIBE_LATEST);
  carmen_param_set_module(NULL);
  carmen_param_get_double("robot_width", &(object_list[num_objects].width), NULL);

  object_list[num_objects].type = CARMEN_SIMULATOR_OTHER_ROBOT;
  object_list[num_objects].is_robot = 1;

  num_objects++; 

  IPC_setContext(current_context);
}

static void
update_other_robot(carmen_object_t *object)
{
  IPC_CONTEXT_PTR current_context;

  current_context = IPC_getContext();
  IPC_setContext(object->context);
 
  IPC_listenClear(0);
  IPC_setContext(current_context);  
}

int
carmen_simulator_object_too_close(double x, double y, int skip)
{
  int i;

  for (i = 0; i < num_objects; i++) 
    {
      if (i == skip)
	continue;
      if (hypot(x - object_list[i].x1,
		y - object_list[i].y1) < min_dist_from_robot) {
	return 1;
      }
      if (!object_list[i].is_robot) 
	{
	  if (hypot(x - object_list[i].x2,
		    y - object_list[i].y2) < min_dist_from_robot) {
	    return 1;
	  }
	}
    }

  return 0;
}
