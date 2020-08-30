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

#ifndef NAVIGATOR_H
#define NAVIGATOR_H

#include <carmen/localize_messages.h>

#ifdef __cplusplus
extern "C" {
#endif

  typedef struct {
    int num_lasers_to_use;
    int use_fast_laser;
    int max_range;
    int max_collision_range;
    int update_map;
    double replan_frequency;
    int smooth_path;
    double goal_size;
    double goal_theta_tolerance;
    int dont_integrate_odometry;
  } carmen_navigator_config_t;

  void carmen_navigator_goal_triplet(carmen_point_p point);
  void carmen_navigator_goal(double x, double y);
  int carmen_navigator_goal_place(char *name);
  void carmen_navigator_set_max_velocity(double vel);
  carmen_map_placelist_p carmen_navigator_get_places(void);
  int carmen_navigator_autonomous_status(void);

  void carmen_navigator_start_autonomous(void);
  void carmen_navigator_stop_autonomous(void);

  typedef struct {
    double tv;
    double rv;
  } command_t;

#ifdef __cplusplus
}
#endif

#endif
