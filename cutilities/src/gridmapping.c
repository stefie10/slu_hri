#include "gridmapping.h"
#include <math.h>

occupancy_grid_mapper::occupancy_grid_mapper(double p_occ, double p_free, double p_nought_occ, 
					     double x_size, double y_size,double resolution, 
					     gsl_vector *start_pose, double alpha_in){
  first_reading = 1;
  max_range = 20.0;
  tklib_log_gridmap mapt(x_size, y_size, resolution);
  //copy this
  map.copy(&mapt);
  
  l_occ = log(p_free/(1.0-p_free));
  //printf("l_occ:%f\n", l_occ);
  l_free = log((1.0-p_occ)/(1.0*p_occ));
  //printf("l_free:%f\n", l_free);
  l_nought = log((1.0-p_nought_occ)/(1.0*p_nought_occ));
  //printf("l_nought:%f\n", l_nought);

  curr_pose = gsl_vector_calloc(start_pose->size);
  gsl_vector_memcpy(curr_pose, start_pose);
  alpha = alpha_in;
  
  //rel_start_angle=rel_start_anglei;
  //rel_end_angle=rel_end_anglei;
}
  
occupancy_grid_mapper::~occupancy_grid_mapper(){
  gsl_vector_free(curr_pose);
}

gsl_matrix* occupancy_grid_mapper::nearest_neighbors_map_alloc(gsl_matrix* points){
  gsl_matrix* nn_pts = gsl_matrix_alloc(points->size1, points->size2);
  nearest_neighbors_map(points, nn_pts);
  return nn_pts;
}
  
void occupancy_grid_mapper::nearest_neighbors_map(gsl_matrix* points, gsl_matrix* nn_pts){
  gsl_vector* curr_nn = gsl_vector_alloc(points->size1);
  
  size_t i;    
  for(i=0;i<points->size2;i++){
    gsl_vector_view curr_pt = gsl_matrix_column(points, i);
    nearest_neighbor_map(&curr_pt.vector, curr_nn);
    
    gsl_matrix_set_col(nn_pts, i, curr_nn);
  }
  gsl_vector_free(curr_nn);
}
  

  
void occupancy_grid_mapper::nearest_neighbor_map(gsl_vector* point, gsl_vector *nn_pt){
  double r = 0;
  //setting the center index
  gsl_vector* center_ind = gsl_vector_alloc(point->size);
  map.xy_to_ind(point, center_ind);
  
  //need for below
  size_t i;
  int nn_seen = 0;
  double dist, ix, iy;
  double curr_dist = 10000000000000000.0;
  gsl_vector* xy = gsl_vector_alloc(point->size);
  
  while(1) {   
    gsl_matrix* curr_inds = box_pts(r);
    tklib_matrix_add_vec(curr_inds, center_ind, 1.0, 1.0);
    
    for(i=0;i<curr_inds->size2;i++){
      //get ix, iy
      gsl_vector_view myind = gsl_matrix_column(curr_inds, i);
      ix = gsl_vector_get(&myind.vector, 0); iy = gsl_vector_get(&myind.vector, 1); 
      

      if((int)ix > map.get_map_width()-1 || (int)iy > map.get_map_height()-1 || (int)ix < 0 || (int)iy < 0){
	continue;
      }
      else if(map.get_value((int)ix,(int)iy) < 0.0){
	map.ind_to_xy(&myind.vector, xy);
	dist = tklib_euclidean_distance(point, xy);

	//see if its better than our previous estimate
	if(dist < curr_dist){
	  nn_seen = 1;
	  curr_dist = dist;
	  gsl_vector_memcpy(nn_pt,xy);
	}
      }
    }
    gsl_matrix_free(curr_inds);  
    //return the closest point if we found
    if(nn_seen){
      //printf("breaking\n");
      break;
    }
    
    r+=1;
    //exit if we've gone outside the grid
    if(r > fmax(map.x_size/map.resolution,map.y_size/map.resolution))
      break;
  }
  

  //free up the space
  gsl_vector_free(center_ind);
  gsl_vector_free(xy);    
}

  
void occupancy_grid_mapper::update_ray_trace(double startx, double starty, 
					     double start_theta, double distance){
  double x_step = cos(start_theta)*map.resolution;
  double y_step = sin(start_theta)*map.resolution;
  
  //#iterate through all of the boxes here
  int j=0; double ix, iy;
  double curr_dist=0;
  gsl_vector *xy = gsl_vector_calloc(2);
  gsl_vector *ind = gsl_vector_calloc(2);
  while(curr_dist <= distance + alpha){
    gsl_vector_set(xy, 0, startx+j*x_step);
    gsl_vector_set(xy, 1, starty+j*y_step);
    map.xy_to_ind(xy, ind);
    
    ix = gsl_vector_get(ind, 0);
    iy = gsl_vector_get(ind, 1);
    //get a grid cell and update with
    // anp observation

    if((int)ix > map.get_map_width()-1 || (int)iy > map.get_map_height()-1 || (int)ix < 0 || (int)iy < 0){
      
    }
    else if(fabs(distance - curr_dist) < alpha){
      map.set_value((int)ix, (int)iy, 
		    map.get_value((int)ix,(int)iy) + l_occ - l_nought);
    }
    //get the grid cell and update it
    //with an unobserved grid cell
    else{
      map.set_value((int)ix, (int)iy, 
		    map.get_value((int)ix, (int)iy) + l_free - l_nought);
    }
    curr_dist = sqrt(pow(j*x_step, 2) + pow(j*y_step, 2));
    j+=1;
  }

  gsl_vector_free(xy);
  gsl_vector_free(ind);
}
  


gsl_matrix* occupancy_grid_mapper::get_non_max_range_readings(gsl_vector* range,
							      gsl_matrix* curr_pts, 
							      double max_range){
  
  //allocate the index vector
  gsl_vector* I = gsl_vector_alloc(range->size);
  
  //figure out which ones are less than max_range
  size_t i; 
  int curr_ind=0;
  for(i=0;i<curr_pts->size2;i++){
    if(gsl_vector_get(range, i) < max_range){
      gsl_vector_set(I, curr_ind, i);
      curr_ind+=1;
    }
  }
  
  //get the subvector of the actual indicies and then the relevant points
  gsl_vector_view Ipr = gsl_vector_subvector(I, 0, curr_ind);
  gsl_matrix* ret_pts =  tklib_matrix_get_columns(curr_pts, &Ipr.vector);
  
  //free the space and return the points
  gsl_vector_free(I);
  return ret_pts;
}


void occupancy_grid_mapper::update(gsl_vector* from_pose,  gsl_vector *reading, 
				   double rel_start_angle, double rel_end_angle){
  gsl_matrix* curr_pts = carmen_util_reading_to_xy(from_pose, reading, 
						   rel_start_angle, rel_end_angle);
  
  gsl_matrix* tmp_pts = get_non_max_range_readings(reading, curr_pts, max_range);
  
  //do the ray tracing
  update_ray_trace_xy(from_pose, tmp_pts);
  

  gsl_matrix_free(curr_pts);
  gsl_matrix_free(tmp_pts);

}


void occupancy_grid_mapper::update_ray_trace_xy(gsl_vector* pose, gsl_matrix* new_measurements){
  //startx = pose.x; starty=pose.y;
  size_t i;
  gsl_vector *v = gsl_vector_calloc(2);
  gsl_vector *r_xy = gsl_vector_calloc(2);
  gsl_vector_memcpy(r_xy, &gsl_vector_subvector(pose, 0, 2).vector);
  double d, curr_theta;
  
  for(i=0;i<new_measurements->size2;i++){
    //#update the map according to the scan matching algorithm
    //v = new_measurements[:,i] - array([pose.x, pose.y]);
    gsl_vector_view curr_measurement = gsl_matrix_column(new_measurements, i);
    gsl_vector_memcpy(v, &curr_measurement.vector);
    gsl_vector_sub(v, r_xy);
    
    //#get the distance to the current reading
    curr_theta = atan2(gsl_vector_get(v,1),gsl_vector_get(v,0));
    d = tklib_euclidean_distance(&curr_measurement.vector, r_xy);
    
    update_ray_trace(gsl_vector_get(r_xy, 0), gsl_vector_get(r_xy, 1), curr_theta, d);
  }
  gsl_vector_free(r_xy);
  gsl_vector_free(v);
}


gsl_matrix* occupancy_grid_mapper::box_pts(double r){
  if(r == 0){
    gsl_matrix* retval = gsl_matrix_calloc(2, 1);
    return retval;
  }

  gsl_vector* ext = tklib_range(-r, r, 1);
  gsl_vector* fix = gsl_vector_calloc(ext->size);
  gsl_vector_scale(fix, r);
  
  gsl_matrix* box_pts = gsl_matrix_alloc(2, 4*ext->size);
  
  //box_pts[:,0:len(ext)]=array([fix, ext]);
  gsl_matrix_view mv = gsl_matrix_submatrix(box_pts, 0, 0, 2, ext->size);
  gsl_matrix_set_row(&mv.matrix, 0, fix);
  gsl_matrix_set_row(&mv.matrix, 1, ext);


  //box_pts[:,2*len(ext):3*len(ext)]=array([ext, fix]);
  mv = gsl_matrix_submatrix(box_pts, 0, ext->size, 2, ext->size);
  gsl_matrix_set_row(&mv.matrix, 0, ext);
  gsl_matrix_set_row(&mv.matrix, 1, fix);


  gsl_vector_scale(fix, -1.0);
  //box_pts[:,len(ext):2*len(ext)]=array([-1.0*fix, ext]);
  mv = gsl_matrix_submatrix(box_pts, 0, 2*ext->size, 2, ext->size);
  gsl_matrix_set_row(&mv.matrix, 0, fix);
  gsl_matrix_set_row(&mv.matrix, 1, ext);


  //box_pts[:,3*len(ext):4*len(ext)]=array([ext, -1.0*fix]);
  mv = gsl_matrix_submatrix(box_pts, 0, 3*ext->size, 2, ext->size);
  gsl_matrix_set_row(&mv.matrix, 0, ext);
  gsl_matrix_set_row(&mv.matrix, 1, fix);
  
  
  gsl_vector_free(ext);
  gsl_vector_free(fix);
  
  return box_pts;
}

/*gsl_vector* occupancy_grid_mapper::ray_trace(double startx, double starty, gsl_vector* thetas){
  gsl_vector* ret_distances = gsl_vector_calloc(thetas->size);
  gsl_vector *stpt = gsl_vector_calloc(2);
  gsl_vector *endpt = gsl_vector_calloc(2);
  gsl_vector *xy = gsl_vector_calloc(2);
  gsl_vector *ind = gsl_vector_calloc(2);  
  
  double x_step, y_step, start_theta, d; 
  double ix, iy;   size_t i, j;
  for(i=0;i<thetas->size;i++){
    start_theta = gsl_vector_get(thetas, i);
    x_step = cos(start_theta)*map.resolution;
    y_step = sin(start_theta)*map.resolution;
    
    j=0;
    while(1){
      gsl_vector_set(xy, 0, startx+j*x_step);
      gsl_vector_set(xy, 1, starty+j*y_step);
      map.xy_to_ind(xy, ind);
      
      ix = gsl_vector_get(ind, 0);
      iy = gsl_vector_get(ind, 1);
      
      if(ix < 0 || iy < 0){
	gsl_vector_set(ret_distances, i, max_range);
	break;
      }
      
      if(ix >= map.x_size/(1.0*map.resolution) || iy >= map.y_size/(1.0*map.resolution)){
	gsl_vector_set(ret_distances, i, max_range);
	break;
      }
      
      //if we actually hit something
      if(map.get_value((int)ix, (int)iy) <= 0){
	gsl_vector_set(stpt, 0, startx);
	gsl_vector_set(stpt, 1, starty);
	  
	gsl_vector_set(endpt, 0,startx+j*x_step);
	gsl_vector_set(endpt, 1, starty+j*y_step);
	
	d = tklib_euclidean_distance(stpt, endpt);
	
	gsl_vector_set(ret_distances, i, d);
	break;
      }
      //this is for the case where we hit unoccupied territory
      //else if(map.get_value((int)ix, (int)iy) == 0){
      //gsl_vector_set(ret_distances, i, max_range);
      //	break;
      //} 
      j+=1;
    } 
  }


  gsl_vector_free(stpt);
  gsl_vector_free(endpt);
  gsl_vector_free(xy);
  gsl_vector_free(ind);
  return ret_distances;
}
*/

/*gsl_matrix* occupancy_grid_mapper::icp_map(gsl_matrix* measured_points, int num_iters){
  //#match against the currently built map... take the nearest 
  //  #point which is filled
  gsl_matrix* prev_points = gsl_matrix_calloc(measured_points->size1, measured_points->size2);
  gsl_matrix_memcpy(prev_points, measured_points);

  double sse;
  gsl_matrix* nns=gsl_matrix_alloc(measured_points->size1, measured_points->size2);
  gsl_matrix* curr_R = gsl_matrix_alloc(measured_points->size1, measured_points->size1);
  gsl_matrix* curr_rotated_pts = gsl_matrix_calloc(prev_points->size1, prev_points->size2);
  gsl_vector* curr_trans = gsl_vector_calloc(measured_points->size1);
  
  int i;
  for(i=0; i<num_iters; i++){
    nearest_neighbors_map(prev_points, nns);
    //sse, R, t = procrustesSVD(prev_points, nns);
    sse = procrustesSVD(prev_points, nns, curr_rotated_pts, curr_R, curr_trans);
    gsl_matrix_memcpy(prev_points, curr_rotated_pts);
  }
  

  gsl_matrix_free(nns);  
  gsl_matrix_free(curr_R);
  gsl_matrix_free(curr_rotated_pts);
  gsl_vector_free(curr_trans);

  return prev_points;
  }*/


/*void occupancy_grid_mapper::update_icp(gsl_vector* from_pose,  gsl_vector *reading, int num_iters){
  gsl_matrix* curr_pts = carmen_util_reading_to_xy(from_pose, reading);



  gsl_matrix* new_meas;
  gsl_matrix* tmp_pts = get_non_max_range_readings(reading, curr_pts, max_range);
  if(first_reading || num_iters <= 0){
    new_meas = gsl_matrix_alloc(tmp_pts->size1, tmp_pts->size2);
    gsl_matrix_memcpy(new_meas, tmp_pts);
    first_reading = 0;
  }
  else{
    new_meas = icp_map(tmp_pts, num_iters);

  }
  
  //recover the pose of the laser
  double dx = gsl_matrix_get(new_meas, 0, new_meas->size2-1) - gsl_matrix_get(new_meas, 0, 0);
  double dy = gsl_matrix_get(new_meas, 1, new_meas->size2-1) - gsl_matrix_get(new_meas, 1, 0);
  double theta_pr = atan2(dy, dx);
  
  //#recover the robot pose
  double x = gsl_matrix_get(new_meas, 0, 0)+gsl_vector_get(reading, 0)*cos(theta_pr);
  double y = gsl_matrix_get(new_meas, 1, 0)+gsl_vector_get(reading, 0)*sin(theta_pr);
  double theta = theta_pr - M_PI/2.0;
  
  //update the local variables
  gsl_vector_set(curr_pose, 0, x);
  gsl_vector_set(curr_pose, 1, y);
  gsl_vector_set(curr_pose, 2, theta);
  
  //do the ray tracing
  ray_trace_xy(curr_pose, new_meas);
  gsl_matrix_free(new_meas);
  gsl_matrix_free(curr_pts);
  gsl_matrix_free(tmp_pts);
  }*/
