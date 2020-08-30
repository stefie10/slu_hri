#include "tklib_log_gridmap.h"

#include <carmen/map_io.h>
#include <assert.h>

tklib_log_gridmap::tklib_log_gridmap(double map_x_size, 
				     double map_y_size, 
				     double map_resolution){
  x_size = map_x_size;
  y_size = map_y_size;
  resolution = map_resolution;
  max_range = 30.0;
  
  double x_width = x_size/resolution;
  double y_width = y_size/resolution;
  
  data = gsl_matrix_float_calloc((int)y_width, (int)x_width);
  //exp_data = to_probability_map();
  
  hurdles = NULL;
}

tklib_log_gridmap::~tklib_log_gridmap(){
  gsl_matrix_float_free(data);
  if(hurdles != NULL)
    gsl_matrix_free(hurdles);
}

double tklib_log_gridmap::get_max_range(){
  return max_range;
}

float tklib_log_gridmap::get_value(int i, int j){
  return gsl_matrix_float_get(data, i, j);
}

/*float tklib_log_gridmap::get_value_probability(int i, int j){
  }*/

//set the value of a map element
void tklib_log_gridmap::set_value(int i, int j, float value){
  gsl_matrix_float_set(data, i, j, value);
}

void tklib_log_gridmap::publish(){
  carmen_publish_gridmapping_map_message(data, 0, 0, resolution);
}

gsl_matrix* tklib_log_gridmap::get_hurdles(){
  gsl_matrix* curr_hurdles = gsl_matrix_alloc(hurdles->size1, hurdles->size2);
  gsl_matrix_memcpy(curr_hurdles, hurdles);

  return curr_hurdles;
}

void  tklib_log_gridmap::copy(tklib_log_gridmap* omap){
  data = omap->get_likelihood_map();//gsl_matrix_float_alloc(omap->data.size1, omap->data.size2);
  gsl_matrix_float_memcpy(data, omap->data);
  resolution = omap->resolution;
  x_size = omap->x_size;
  y_size = omap->y_size;
}




//get the map with allocation
gsl_matrix_float* tklib_log_gridmap::get_likelihood_map(){
  gsl_matrix_float* retdata = gsl_matrix_float_alloc(data->size1, data->size2);
  gsl_matrix_float_memcpy(retdata, data);
  
  return retdata;
}

int tklib_log_gridmap::location_free(gsl_vector* xy){
  gsl_vector* ind = gsl_vector_alloc(2);
  xy_to_ind(xy, ind);
  int isfree = ind_free(ind);
  
  gsl_vector_free(ind);
  return isfree;
}

int tklib_log_gridmap::location_occupied(gsl_vector* xy){
  gsl_vector* ind = gsl_vector_alloc(2);
  xy_to_ind(xy, ind);
  int isoccupied = ind_occupied(ind);

  gsl_vector_free(ind);
  return isoccupied;
}

//index is occupied
 int tklib_log_gridmap::ind_occupied(gsl_vector* ind){
  //is the minimum index less than 0, if so, its not free at all
  double x_ind = gsl_vector_get(ind, 0);   double y_ind = gsl_vector_get(ind, 1);
  
  //see if we are outside the map, if so then return false
  double min_ind = gsl_vector_min(ind);
  if(min_ind < 0 || x_ind >= get_map_width() || y_ind >= get_map_height())
    return 0;

  //is the value of the map less than 0 or equal to it
  //   if so then the map is occupied
  double map_val = get_value_probability((int)x_ind, (int)y_ind);
  
  if(gsl_isnan(map_val))
    return 0;
  if(map_val == 0.5)
    return 0;
  if(map_val > 0.1 && map_val <= 1.0)
    return 1;
  
  //if neither of the above are the case, then the area is unoccupied
  return 0;
}

//index is free
 int tklib_log_gridmap::ind_free(gsl_vector* ind){
  //is the minimum index less than 0, if so, its not free
  //     at all
  double x_ind = gsl_vector_get(ind, 0);   double y_ind = gsl_vector_get(ind, 1);
  
  //see if we are outside the map, if so then return false
  double min_ind = gsl_vector_min(ind);
  if(min_ind < 0 || x_ind >= get_map_width() || y_ind >= get_map_height())
    return 0;
  
  //is the value of the map less than 0 or equal to it
  //   if so then the map is occupied
  double map_val = get_value_probability((int)x_ind, (int)y_ind);
  if(gsl_isnan(map_val)){
    //printf("isnan\n");
    return 0;
  }
  if(map_val > 0.1)
    return 0;
  
  //if neither of the above are the case, then the area is unoccupied
  return 1;
}




 double tklib_log_gridmap::min_range(gsl_vector *from_pt){
  double x = gsl_vector_get(from_pt, 0);
  double y = gsl_vector_get(from_pt, 1);

  gsl_vector* theta = tklib_range(0, 2*M_PI, M_PI/180.0);
  gsl_vector* range = ray_trace(x, y, theta);

  double mymin = gsl_vector_min(range);
  
  gsl_vector_free(theta);
  gsl_vector_free(range);
  return mymin;
}

gsl_matrix* tklib_log_gridmap::get_random_open_locations(int num_samples, double radius){
  gsl_matrix* pts = gsl_matrix_calloc(2, num_samples);
  
  for(size_t i=0; i<pts->size2; i++){
    gsl_vector* pt = get_random_open_location(radius);
    gsl_matrix_set_col(pts, i, pt);
    gsl_vector_free(pt);
  }
  
  return pts;
}


gsl_vector* tklib_log_gridmap::get_random_open_location(double radius){
  int done = 0;
  gsl_vector* ind = gsl_vector_alloc(2);
  gsl_vector* xy = gsl_vector_alloc(2);
  
  double x_ind, y_ind;
  while(!done){
    x_ind = tklib_randint(0, get_map_width());
    y_ind = tklib_randint(0, get_map_height());

    //convert to xy coordinates
    gsl_vector_set(ind, 0, x_ind); gsl_vector_set(ind, 1, y_ind);
    ind_to_xy(ind, xy);
    if(radius < 0.1 && location_free(xy)){
      done = 1;
    }
    else if(location_free_radius(xy, radius)){
      done = 1;
    }
  }
  
  gsl_vector_free(ind);
  return xy;
}

//add n random hurdle features to the map
void tklib_log_gridmap::add_hurdles(double hurdle_width, double hurdle_size, int N){
  if(!(hurdles == NULL))
    gsl_matrix_free(hurdles);
  hurdles = gsl_matrix_alloc(3, N);
  
  int i;
  for(i=0; i<N; i++){
    gsl_vector* curr_hurdle = add_hurdle(hurdle_width, hurdle_size);
    
    //set hurdles here
    gsl_matrix_set_col(hurdles, i, curr_hurdle);
    gsl_vector_free(curr_hurdle);
  }
}

//convert to the probability map
gsl_matrix_float* tklib_log_gridmap::to_probability_map(){
  return get_probability_submap(0, 0, data->size1, data->size2);
}

gsl_matrix_float* tklib_log_gridmap::to_probability_map_carmen(){
  gsl_matrix_float* ret_map = get_probability_submap(0, 0, data->size1, data->size2);
  
  size_t i, j;
  
  for(i=0;i<data->size1; i++){
    for(j=0;j<data->size2;j++){
      if(gsl_matrix_float_get(ret_map, i, j) == 0.5){
	gsl_matrix_float_set(ret_map, i, j, -1);
      }
    }
  }

  return ret_map;
}

 gsl_matrix_float* tklib_log_gridmap::get_probability_submap(int start_i, int start_j, 
								   int stride_i, int stride_j){
  gsl_matrix_float_view mydata = gsl_matrix_float_submatrix(data, 
							    start_i, start_j, 
							    stride_i, stride_j);
  
  gsl_matrix_float* ret_mat = gsl_matrix_float_calloc((&mydata.matrix)->size1, (&mydata.matrix)->size2);
  gsl_matrix_float_add_constant(ret_mat, -1.0);

  gsl_matrix_float* denom = tklib_exp_float(&mydata.matrix);
  gsl_matrix_float_add_constant(denom, 1.0);
  
  gsl_matrix_float_div_elements(ret_mat, denom);
  gsl_matrix_float_add_constant(ret_mat, 1);

  size_t i,j;
  for(i=0;i<ret_mat->size1;i++){
    for(j=0;j<ret_mat->size2;j++){
      if(gsl_isnan(gsl_matrix_float_get(ret_mat,i,j))){
	gsl_matrix_float_set(ret_mat, i, j, -1);
      }
    }
  }

  gsl_matrix_float_free(denom); 
  return ret_mat;
}


//convert to a likelihood map
 gsl_matrix_float* tklib_log_gridmap::to_likelihood_map(gsl_matrix_float* probability_map){
  //make the numeratior
  gsl_matrix_float* num = gsl_matrix_float_calloc(probability_map->size1, 
						  probability_map->size2);
  gsl_matrix_float_memcpy(num, probability_map);
  
  //make the denominator
  gsl_matrix_float* denom = gsl_matrix_float_calloc(probability_map->size1, 
						    probability_map->size2);
  gsl_matrix_float_memcpy(denom, probability_map);
  gsl_matrix_float_scale(denom, -1.0);
  gsl_matrix_float_add_constant(denom, 1.0);

  //divide the numerator by the denominator
  gsl_matrix_float_div_elements(num, denom);
  gsl_matrix_float* ret_mat = tklib_log_float(num);
  
  gsl_matrix_float_free(num);
  gsl_matrix_float_free(denom); 
  return ret_mat;
}


//convert to a carmen_map
carmen_map_p tklib_log_gridmap::to_carmen_map_noalloc(){
  //fill out the config information
  carmen_map_config_p config = (carmen_map_config_p)calloc(1, sizeof(carmen_map_config_t));
  config->x_size = data->size1;
  config->y_size = data->size2;
  config->resolution = resolution;
  config->map_name = (char*)"tklib_log_gridmap";

  //fill out the map data
  float* map_data = gsl_block_float_data(data->block);
  carmen_map_p ret_map = (carmen_map_p)calloc(1, sizeof(carmen_map_t));
  ret_map->complete_map = map_data;
  
  //allocate the map pointers
  float** map_pnters = (float**)calloc(config->x_size, sizeof(float*));
  int i;
  for(i=0;i<config->x_size;i++){
    map_pnters[i] = &map_data[i*config->x_size];
  }

  // this is roughly right... may crash things :-/
  ret_map->map = map_pnters;

  return ret_map;
}

void tklib_log_gridmap::load_carmen_map(char* filename){
  if(data != NULL)
    gsl_matrix_float_free(data);
  //if(exp_data != NULL)
  //gsl_matrix_float_free(exp_data);
  
  carmen_map_p mymap = carmen_util_read_gridmap(filename);
  
  gsl_block_float* bl = (gsl_block_float*)calloc(1, sizeof(gsl_block_float));
  bl->size = mymap->config.x_size * mymap->config.y_size;
  bl->data = mymap->complete_map;
  
  gsl_matrix_float* mydata = gsl_matrix_float_alloc_from_block(bl, 0, 
							       mymap->config.x_size, 
							       mymap->config.y_size, 
							       mymap->config.y_size);
  mydata->owner = 1;
  
  //gsl_matrix_float_scale(mydata, -1);
  //gsl_matrix_float_add_constant(mydata, 1);

  data = to_likelihood_map(mydata);

  //this is new
  //exp_data = to_probability_map();
  
  resolution = mymap->config.resolution;
  x_size = mymap->config.x_size*mymap->config.resolution;
  y_size = mymap->config.y_size*mymap->config.resolution;


  carmen_global_offset_p global_offset = (carmen_global_offset_p)calloc(1, sizeof(carmen_global_offset_t));
  carmen_map_read_global_offset_chunk(filename, global_offset);
  x_offset = global_offset->x;
  y_offset = global_offset->y;
  theta_offset = global_offset->theta;
  printf("theta: %.3f\n", theta_offset);
  //assert(fabs(theta_offset - 0) < 0.00000001); // we don't rotate yet.
    
  free(&mymap->config);
  mymap = NULL;
  free(global_offset);
  gsl_matrix_float_free(mydata);
}


 int tklib_log_gridmap::path_free(SplineC *thespline){
  gsl_vector* start_pose = thespline->get_start_pose();
  gsl_vector* end_pose = thespline->get_end_pose();
  gsl_vector* times = tklib_range(0, 1+0.0000001, resolution/2.0);
  gsl_matrix* spline_pts = thespline->value(times);

  int outside_map = 0;
  int hit_obstacle = 0;
  int hit_unknown = 0;


  gsl_vector* ind = gsl_vector_alloc(spline_pts->size1);
  double ix, iy;
  float map_val;

  
  size_t i;
  for(i=0;i<times->size;i++){
    gsl_vector_view v = gsl_matrix_column(spline_pts, i);
    xy_to_ind(&v.vector, ind);

    ix = gsl_vector_get(ind, 0);
    iy = gsl_vector_get(ind, 1);
    
    
    if((int)ix > get_map_width()-1 || (int)iy > get_map_height()-1 || (int)ix < 0 || (int)iy < 0){
      outside_map = 1;
      break;
    }
    
    map_val = get_value((int)ix, (int)iy);

    if(map_val == 0){
      hit_unknown =1;
      break;
    }
    else if(map_val < 0){
      hit_obstacle = 1;
      break;
    }
  }

  gsl_vector_free(ind);
  gsl_matrix_free(spline_pts);
  gsl_vector_free(start_pose);
  gsl_vector_free(end_pose);
  gsl_vector_free(times);

  //error if hit obstacle or otherwise
  if(hit_obstacle)
    return 0;
  else if(outside_map)
    return -1;
  else if(hit_unknown)
    return -2;
  
  return 1;
}


//determine whether an x, y location is free 
//     for some box around this location
 int tklib_log_gridmap::location_free_radius(gsl_vector* xy, double radius){
  gsl_vector* max_xy = gsl_vector_calloc(2);   gsl_vector_memcpy(max_xy, xy);
  gsl_vector* min_xy = gsl_vector_calloc(2);   gsl_vector_memcpy(min_xy, xy);
  gsl_vector* min_ind = gsl_vector_calloc(2);  

  //get the minimum and maximum points of the square
  gsl_vector_add_constant(max_xy, radius);
  gsl_vector_add_constant(min_xy, -1.0*radius);
  xy_to_ind(min_xy, min_ind);
  double x_ind = gsl_vector_get(min_ind, 0); double y_ind = gsl_vector_get(min_ind, 1);
  
  int is_free =  0;
  if(location_free(min_xy) && location_free(max_xy)){
    //get the submatrix and just get the submatrix corresponding to that
    //     radius
    //gsl_matrix_float_view curr_submatrix = gsl_matrix_float_submatrix(data, 
    //								      (int)x_ind, (int)y_ind, 
    //								      (int)(2*(radius/resolution)), 
    //								      (int)(2*(radius/resolution)));
    
    gsl_matrix_float* curr_submatrix = get_probability_submap((int)x_ind, (int)y_ind, 
							      (int)(2*(radius/resolution)),
							      (int)(2*(radius/resolution)));

    //get the minimum value in this matrix and see if its less than 0
    double map_min_value = gsl_matrix_float_min(curr_submatrix); 
    double map_max_value = gsl_matrix_float_max(curr_submatrix); 
    
    if(map_min_value < 0)
      is_free = 0;
    else if(map_max_value > 0.1)
      is_free = 0;
    else
      is_free = 1;
    
    gsl_matrix_float_free(curr_submatrix);
  }
  else
    is_free = 0;

  gsl_vector_free(max_xy);
  gsl_vector_free(min_xy);
  gsl_vector_free(min_ind);
  return is_free;
}


//add n random hurdle features to the map
gsl_vector* tklib_log_gridmap::add_hurdle(double hurdle_width, double hurdle_size){
  gsl_vector* ret_loc = gsl_vector_alloc(3);
  
  //get an open location with a bit more than the width of the hurdle
  double hurdle_theta = tklib_random()*2.0*M_PI;
  gsl_vector* hurdle_loc = get_random_open_location(hurdle_width*2.0);
  gsl_vector* post1 = gsl_vector_calloc(2);
  gsl_vector* post2 = gsl_vector_calloc(2);
  

  //get the precise location of the first post
  double post1_theta = hurdle_theta - M_PI/2.0;
  gsl_vector_set(post1, 0, (hurdle_width/2.0)*cos(post1_theta));
  gsl_vector_set(post1, 1, (hurdle_width/2.0)*sin(post1_theta));
  gsl_vector_add(post1, hurdle_loc);

  //get the precise location of the first post
  double post2_theta = hurdle_theta + M_PI/2.0;
  gsl_vector_set(post2, 0, (hurdle_width/2.0)*cos(post2_theta));
  gsl_vector_set(post2, 1, (hurdle_width/2.0)*sin(post2_theta));
  gsl_vector_add(post2, hurdle_loc);
  
  draw_post(post1, hurdle_size);
  draw_post(post2, hurdle_size);
  
  gsl_vector_set(ret_loc, 0, gsl_vector_get(hurdle_loc, 0));
  gsl_vector_set(ret_loc, 1, gsl_vector_get(hurdle_loc, 1));
  gsl_vector_set(ret_loc, 2, hurdle_theta);
  
  
  gsl_vector_free(hurdle_loc);
  gsl_vector_free(post1);
  gsl_vector_free(post2);
  return ret_loc;
} 

void tklib_log_gridmap::draw_post(gsl_vector* loc, double post_width){
  gsl_vector* min_loc = gsl_vector_alloc(2);
  gsl_vector* min_loc_ind = gsl_vector_alloc(2);

  gsl_vector_memcpy(min_loc, loc);
  gsl_vector_add_constant(min_loc, -post_width/2.0);

  xy_to_ind(min_loc, min_loc_ind);

  double x_ind = gsl_vector_get(min_loc_ind, 0);
  double y_ind = gsl_vector_get(min_loc_ind, 1);
  
  gsl_matrix_float_view post_view = gsl_matrix_float_submatrix(data, (int)x_ind, (int)y_ind, 
							       (int)(post_width/resolution)+1, 
							       (int)(post_width/resolution)+1);
  
  gsl_matrix_float_set_all(&post_view.matrix, -1.0);
  gsl_vector_free(min_loc);
  gsl_vector_free(min_loc_ind);
}




//  gsl_matrix* get_occupied_locations();
 gsl_matrix* tklib_log_gridmap::get_occupied_locations(){
  gsl_matrix* free_locations = gsl_matrix_calloc(2, data->size1*data->size2);
  gsl_vector* xy = gsl_vector_alloc(2);
  gsl_vector* ind = gsl_vector_alloc(2);
  
  size_t i, j;
  size_t n = 0;
  for(i=0;i<data->size1;i++){
    for(j=0;j<data->size2;j++){
      //set the indicies
      //convert index to xy
      gsl_vector_set(ind, 0, i);
      gsl_vector_set(ind, 1, j);
      ind_to_xy(ind, xy);

      //check whether it is free
      if(location_occupied(xy)){
	gsl_matrix_set(free_locations,0,n,gsl_vector_get(xy,0));
	gsl_matrix_set(free_locations,1,n,gsl_vector_get(xy,1));
	n+=1;
      }
    }
  }

  gsl_matrix* ret_vals = gsl_matrix_alloc(2, n);
  gsl_matrix_view free_loc_tmp = gsl_matrix_submatrix(free_locations, 0, 0, 2, n);
  gsl_matrix_memcpy(ret_vals, &free_loc_tmp.matrix);
  gsl_vector_free(ind);
  gsl_vector_free(xy);
  gsl_matrix_free(free_locations);
  return ret_vals;
}

 gsl_matrix* tklib_log_gridmap::get_occupied_inds(){
  gsl_matrix* free_locations = gsl_matrix_calloc(2, data->size1*data->size2);
  gsl_vector* ind = gsl_vector_alloc(2);
  
  size_t i, j;
  size_t n = 0;
  for(i=0;i<data->size1;i++){
    for(j=0;j<data->size2;j++){
      //set the indicies
      //convert index to xy
      gsl_vector_set(ind, 0, i);
      gsl_vector_set(ind, 1, j);
      
      //check whether it is free
      if(ind_occupied(ind)){
	gsl_matrix_set(free_locations,0,n,gsl_vector_get(ind,0));
	gsl_matrix_set(free_locations,1,n,gsl_vector_get(ind,1));
	n+=1;
      }
    }
  }
  
  gsl_matrix* ret_vals = gsl_matrix_alloc(2, n);
  gsl_matrix_view free_loc_tmp = gsl_matrix_submatrix(free_locations, 0, 0, 2, n);
  gsl_matrix_memcpy(ret_vals, &free_loc_tmp.matrix);
  gsl_vector_free(ind);
  gsl_matrix_free(free_locations);
  return ret_vals;
}

 gsl_matrix* tklib_log_gridmap::get_free_locations(){
   gsl_matrix* free_locations = gsl_matrix_calloc(2, data->size1*data->size2);
   gsl_vector* xy = gsl_vector_alloc(2);
   gsl_vector* ind = gsl_vector_alloc(2);
  
   size_t i, j;
   size_t n = 0;
   for(i=0;i<data->size1;i++){
     for(j=0;j<data->size2;j++){
       //set the indicies
       //convert index to xy
       gsl_vector_set(ind, 0, i);
       gsl_vector_set(ind, 1, j);
       ind_to_xy(ind, xy);
      
       //check whether it is free
       if(location_free(xy)){
	 gsl_matrix_set(free_locations,0,n,gsl_vector_get(xy,0));
	 gsl_matrix_set(free_locations,1,n,gsl_vector_get(xy,1));
	 n+=1;
       }
     }
   }

  gsl_matrix* ret_vals = gsl_matrix_alloc(2, n);
  gsl_matrix_view free_loc_tmp = gsl_matrix_submatrix(free_locations, 0, 0, 2, n);
  gsl_matrix_memcpy(ret_vals, &free_loc_tmp.matrix);
  gsl_vector_free(ind);
  gsl_vector_free(xy);
  gsl_matrix_free(free_locations);
  return ret_vals;
}

gsl_matrix* tklib_log_gridmap::get_free_inds(){
  gsl_matrix* free_locations = gsl_matrix_calloc(2, data->size1*data->size2);
  gsl_vector* ind = gsl_vector_alloc(2);
  
  size_t i, j;
  size_t n = 0;
  for(i=0;i<data->size1;i++){
    for(j=0;j<data->size2;j++){
      //set the indicies
      gsl_vector_set(ind, 0, i);
      gsl_vector_set(ind, 1, j);
      
      //check whether it is free
      if(ind_free(ind)){
	gsl_matrix_set(free_locations,0,n,i);
	gsl_matrix_set(free_locations,1,n,j);
	n+=1;
      }
    }
  }

  gsl_matrix* ret_vals = gsl_matrix_alloc(2, n);
  gsl_matrix_view free_loc_tmp = gsl_matrix_submatrix(free_locations, 0, 0, 2, n);
  gsl_matrix_memcpy(ret_vals, &free_loc_tmp.matrix);
  gsl_vector_free(ind);
  gsl_matrix_free(free_locations);
  return ret_vals;
}


void tklib_log_gridmap::downsize_and_save_map(char* tofilename, int ds){
  tklib_log_gridmap* mymap =   (tklib_log_gridmap *)calloc(1, sizeof(tklib_log_gridmap));
  
  //printf("downsampling map\n");
  mymap->data = downsample_map(ds);
  mymap->resolution = resolution*(1.0*ds);
  mymap->x_size = x_size;
  mymap->y_size = y_size;
  
  //printf("saving map\n");
  mymap->save_carmen_map(tofilename);
  
  //printf("freeing stuff\n");
  gsl_matrix_float_free(mymap->data);
  //printf("freeing map\n");
  free(mymap);
  //printf("done\n");
}

gsl_matrix_float* tklib_log_gridmap::downsample_map(int ds){
  gsl_matrix_float* themap = data; //to_probability_map();
  gsl_vector* x_range = tklib_range(0, themap->size2-1, ds);
  gsl_vector* y_range = tklib_range(0, themap->size1-1, ds);
  
  gsl_matrix_float* without_X = tklib_matrix_float_get_columns(themap, x_range);
  gsl_matrix_float* without_Y = tklib_matrix_float_get_rows(without_X, y_range);
  
  //gsl_matrix_float_free(themap);
  gsl_matrix_float_free(without_X);
  gsl_vector_free(y_range);
  gsl_vector_free(x_range);
  return without_Y;
}


int  tklib_log_gridmap::save_carmen_map(char* filename){
  gsl_matrix_float* mydata = to_probability_map();
  int success = carmen_util_write_gridmap(filename, mydata, resolution);
  
  gsl_matrix_float_free(mydata);
  return success;
}

 gsl_vector* tklib_log_gridmap::ray_trace(double startx, double starty, gsl_vector* thetas){
  gsl_vector* ret_distances = gsl_vector_calloc(thetas->size);
  gsl_vector *stpt = gsl_vector_calloc(2);
  gsl_vector *endpt = gsl_vector_calloc(2);
  gsl_vector *xy = gsl_vector_calloc(2);
  gsl_vector *ind = gsl_vector_calloc(2);  
  
  double x_step, y_step, start_theta, d; 
  double ix, iy; 
  size_t i, j;
  
  for(i=0;i<thetas->size;i++){
    start_theta = gsl_vector_get(thetas, i);
    x_step = cos(start_theta)*resolution;
    y_step = sin(start_theta)*resolution;
    
    j=0;
    
    //printf("*******************\n");
    //printf("theta=%f\n", start_theta);
    
    while(1){
      gsl_vector_set(xy, 0, startx+j*x_step);
      gsl_vector_set(xy, 1, starty+j*y_step);

      //printf("location:");
      //tklib_vector_printf(xy);
      
      xy_to_ind(xy, ind);
      
      ix = gsl_vector_get(ind, 0);
      iy = gsl_vector_get(ind, 1);
      
      gsl_vector_set(ret_distances, i, max_range);
      if(ix < 0 || iy < 0){
	break;
      }
      else if(ix >= x_size/(1.0*resolution) || iy >= y_size/(1.0*resolution)){
	break;
      }
      //if we actually hit something
      //if(get_value_probability((int)ix, (int)iy) >= tklib_random()){

      //this is for the case where we hit unoccupied territory
      //if(get_value_probability((int)ix, (int)iy) == 0.5){
      //printf("Got maximum uncertainty pixel.");
      //gsl_vector_set(ret_distances, i, max_range);
      //break;
      //} 
      //else 
      else if(get_value_probability((int)ix, (int)iy) >= 0.09 ||
	      gsl_isnan(get_value_probability((int)ix, (int)iy))){
	
	//printf("prob %f\n", get_value_probability((int)ix, (int)iy));
	
	gsl_vector_set(stpt, 0, startx);
	gsl_vector_set(stpt, 1, starty);
	  
	gsl_vector_set(endpt, 0,startx+j*x_step);
	gsl_vector_set(endpt, 1, starty+j*y_step);
	
	d = tklib_euclidean_distance(stpt, endpt);
	
	gsl_vector_set(ret_distances, i, d);
	break;
      }

      j+=1;
    } 
  }


  gsl_vector_free(stpt);
  gsl_vector_free(endpt);
  gsl_vector_free(xy);
  gsl_vector_free(ind);
  return ret_distances;
}




 gsl_vector* tklib_log_gridmap::get_random_open_location_from_pt(gsl_vector* pt, 
							    double distance, double box_radius){
  //initialize done to be whether or not the current point is
  //occupied
  int done = !location_free(pt); 

  if(done){
    printf("Error: simulator.c the initial location was not free\n");
    exit(1);
  }
  
  //initialize the destination variables
  double dest_x, dest_y, dest_theta;

  //the robot pose 
  double rx = gsl_vector_get(pt, 0);
  double ry = gsl_vector_get(pt, 1);
  gsl_vector* destination = gsl_vector_alloc(2);
  gsl_vector* dest_theta_vec = gsl_vector_alloc(1);
  
  //try to find another location
  while(!done){
    dest_theta = tklib_random()*M_PI*2.0;

    dest_x = distance*cos(dest_theta) + rx;
    dest_y = distance*sin(dest_theta) + ry;

    gsl_vector_set(destination, 0, dest_x);
    gsl_vector_set(destination, 1, dest_y);
    
    done = location_free_radius(destination, box_radius);

    //ray trace the direction as well and make sure the
    //    whole path is clear... if not, then we're fucked
    gsl_vector_set(dest_theta_vec, 0, dest_theta);
    gsl_vector* curr_dist = ray_trace(rx, ry, dest_theta_vec);
    if(gsl_vector_get(curr_dist, 0) < distance)
      done = 0;
    
    //free some memory
    gsl_vector_free(curr_dist);
  }
  
  return destination;
  }


bool tklib_log_gridmap::is_visible(gsl_vector* pt1, gsl_vector* pt2){
  double x1 = gsl_vector_get(pt1, 0);
  double y1 = gsl_vector_get(pt1, 1);
  double x2 = gsl_vector_get(pt2, 0);
  double y2 = gsl_vector_get(pt2, 1);
  
  double angle = atan2(y2-y1, x2-x1);
  gsl_vector* ang = gsl_vector_calloc(1);
  gsl_vector_set(ang, 0, angle);

  //do the ray trace and get the distance
  gsl_vector* rt = ray_trace(x1, y1, ang);
  double d_ray_trace = gsl_vector_get(rt, 0);
  
  //get the euclidean distance
  double d_euclid = tklib_euclidean_distance(pt1, pt2);

  //fprintf(stderr, "ray trace=%f ;  ray euclid=%f\n", d_ray_trace, d_euclid);
  //if its not a max_range reading and the ray trace is
  //    larger than the euclidean distance, accept
  if(d_ray_trace != max_range
     and d_ray_trace >= d_euclid)
       return true;
  
  return false;
} 

gsl_matrix* tklib_log_gridmap::get_frontiers(){
  gsl_matrix* free_locs = get_free_locations();
  
  int frontier_cnt = 0;
  gsl_matrix* frontier_locations = gsl_matrix_calloc(free_locs->size1, free_locs->size2);
  gsl_vector* curr_xy = gsl_vector_calloc(free_locs->size1);

  for(size_t i=0; i<free_locs->size2; i++){
    gsl_matrix_get_col(curr_xy, free_locs, i);
    
    gsl_vector* ind = to_index(curr_xy);
    gsl_matrix* ffrontier = get_connected_frontiers(ind);
    
    if(ffrontier != NULL){
      gsl_matrix_set_col(frontier_locations, frontier_cnt, curr_xy);
      frontier_cnt+=1;
    }

    gsl_vector_free(ind);

    if(ffrontier != NULL)
      gsl_matrix_free(ffrontier);
  }

  gsl_vector_free(curr_xy);
  if(frontier_cnt > 0){
    gsl_matrix_view f_view = gsl_matrix_submatrix(frontier_locations, 0, 0, 2, frontier_cnt);
    gsl_matrix* ret_mat = gsl_matrix_calloc((&(f_view.matrix))->size1, 
					    (&(f_view.matrix))->size2);
    gsl_matrix_memcpy(ret_mat, &f_view.matrix);
    gsl_matrix_free(free_locs);
    gsl_matrix_free(frontier_locations);

    return ret_mat;
  }
  else{
    gsl_matrix_free(free_locs);
    gsl_matrix_free(frontier_locations);
    return NULL;
  }
}


gsl_matrix* tklib_log_gridmap::get_connected_frontiers(gsl_vector* loc_i){
  
  int x_i = (int)gsl_vector_get(loc_i, 0);
  int y_i = (int)gsl_vector_get(loc_i, 1);

  int f_i = 0; 
  gsl_matrix* frontier_locations = gsl_matrix_calloc(2, 8);

  for(int i=-1; i <=1; i++){
    for(int j=-1; j<=1; j++){
      if(i==0 && j==0)
	continue;
      
      float v = get_value(x_i+i, y_i+j);
      
      if(isnan(v)){
	gsl_vector* curr_loc = gsl_vector_calloc(2);
	gsl_vector_set(curr_loc, 0, x_i);
	gsl_vector_set(curr_loc, 1, y_i);

	gsl_matrix_set_col(frontier_locations, f_i, curr_loc);

	f_i+=1;
	gsl_vector_free(curr_loc);
      }
    }
  }
  
  if(f_i > 0){
    gsl_matrix_view f_view = gsl_matrix_submatrix(frontier_locations, 0, 0, 2, f_i);
    gsl_matrix* ret_mat = gsl_matrix_calloc((&(f_view.matrix))->size1, 
					    (&(f_view.matrix))->size2);
    gsl_matrix_memcpy(ret_mat, &f_view.matrix);
    gsl_matrix_free(frontier_locations);
    return ret_mat;
  }
  else{
    gsl_matrix_free(frontier_locations);
    return NULL;
  }
  
}
