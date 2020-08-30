#ifndef TKLIB_LOG_GRIDMAP_H
#define TKLIB_LOG_GRIDMAP_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_block_float.h>
#include <gsl/gsl_math.h>
//#include "gsl_utilities.h"
#include "probability.h"
//#include "gsl_utilities.h"
#include "carmen_util.h"
//#include "procrustes.h"
//#include "noise_models.h"
#include "spline.h"
#include "carmen_publish.h"


#ifdef __cplusplus
extern "C" {
#endif

class tklib_log_gridmap{
 private:
  double max_range;
  gsl_matrix_float* data;
  //gsl_matrix_float* exp_data;
  gsl_matrix* hurdles;
  
  void draw_post(gsl_vector* loc, double width);
  gsl_matrix* get_connected_frontiers(gsl_vector* loc_i);
 public:
  //variables
  double x_size, y_size, resolution;

  double x_offset, y_offset, theta_offset;
  
  //constructor
  tklib_log_gridmap(){data=NULL; hurdles=NULL; max_range=30.0;}
  // exp_data=NULL; max_range = 30.0;}
  tklib_log_gridmap(double map_x_size, double map_y_size, double map_resolution);
  ~tklib_log_gridmap();

  //return the max range of the sensor
  double get_max_range();

  //get the x and y size of the map
  double get_x_size(){return y_size;}
  double get_y_size(){return x_size;}
  
  //get the width and height of the map
  int get_map_width(){return data->size1;}
  int get_map_height(){return data->size2;}
  
  //get the values of the map
  float get_value(int i, int j);
  
  inline float get_value_probability(int i, int j){
    float val = get_value(i, j);
    val = 1.0-(1.0/(1.0+exp(val)));
    
    return val;
  }
  void  set_value(int i, int j, float value);

  //convert between indicies and xy locations
  //void  xy_to_ind(gsl_vector* xy, gsl_vector* ind);
  //void  ind_to_xy(gsl_vector *ind, gsl_vector *xy);


  inline gsl_vector* to_xy(gsl_vector *ind){
    gsl_vector* xy = gsl_vector_alloc(2);
    ind_to_xy(ind, xy);
    
    return xy;
  }

  inline gsl_vector* to_index(gsl_vector *xy){
    gsl_vector* ind = gsl_vector_alloc(2);
    xy_to_ind(xy, ind);

    return ind;
  }

  gsl_matrix_float* downsample_map(int ds);
  
  //convert the xy position to an index, pass the memory in
  inline void xy_to_ind(gsl_vector* xy, gsl_vector* ind){
    double ix = round((gsl_vector_get(xy,0) - x_offset) / resolution);
    double iy = round((gsl_vector_get(xy,1) - y_offset) / resolution);
    
    gsl_vector_set(ind, 0, ix);
    gsl_vector_set(ind, 1, iy);
  }
  
  //convert the index to xy values, pass the memory in
  inline void ind_to_xy(gsl_vector *ind, gsl_vector *xy){
    gsl_vector_memcpy(xy, ind);
    gsl_vector_scale(xy, resolution);
    gsl_vector_set(xy, 0, gsl_vector_get(xy, 0) + x_offset);
    gsl_vector_set(xy, 1, gsl_vector_get(xy, 1) + y_offset);
  }

  void downsize_and_save_map(char* tofilename, int ds);

  //add carmen functionality 
  void  load_carmen_map(char* filename);
  int   save_carmen_map(char* filename);
  carmen_map_p to_carmen_map_noalloc();

  //convert between different formats
  gsl_matrix_float* to_probability_map();
  gsl_matrix_float* to_probability_map_carmen();
  gsl_matrix_float* get_probability_submap(int start_i, int start_j, 
					   int stride_i, int stride_j);
  
  gsl_matrix_float* get_likelihood_map();
  gsl_matrix_float* to_likelihood_map(gsl_matrix_float* probability_map);
  
  void  copy(tklib_log_gridmap* omap);
  void publish();
  
  //determine whether a spline is free or not
  int path_free(SplineC *thespline);
  
  //determine whether a particular index is free;
  int ind_free(gsl_vector* ind);
  int ind_occupied(gsl_vector* ind);

  //determine whether an x, y location is free or occupied
  int location_free(gsl_vector* xy);
  int location_free_radius(gsl_vector* xy, double radius);
  int location_occupied(gsl_vector* xy);
  
  //returns the free locations of the map
  gsl_matrix* get_free_locations();
  gsl_matrix* get_free_inds();
  
  //returns the occupied locations in the map
  gsl_matrix* get_occupied_locations();
  gsl_matrix* get_occupied_inds();

  //get a random location in the map that has the radius free
  gsl_vector* get_random_open_location(double radius);
  gsl_vector* get_random_open_location_from_pt(gsl_vector* pt, 
					       double distance, double box_radius);
  gsl_matrix* get_random_open_locations(int num_samples, double radius);
  
  //ray trace the map
  gsl_vector* ray_trace(double startx, double starty, gsl_vector* thetas);
  bool is_visible(gsl_vector* pt1, gsl_vector* pt2);

  //minimum range to any obstacle from the particular point
  double min_range(gsl_vector *from_pt);

  //add n random hurdle features to the map
  gsl_matrix* get_hurdles();
  gsl_vector* add_hurdle(double hurdle_width, double hurdle_size);
  void add_hurdles(double hurdle_width, double hurdle_size, int N);
  
  gsl_matrix* get_frontiers();
};

#ifdef __cplusplus
}
#endif


#endif
