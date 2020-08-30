#ifndef TKLIB_GRIDMAP_H
#define TKLIB_GRIDMAP_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_block_float.h>
#include "gsl_utilities.h"
#include "probability.h"
#include "gsl_utilities.h"
#include "carmen_util.h"
#include "procrustes.h"
#include "noise_models.h"
#include "spline.h"
#include "carmen_publish.h"

#ifdef __cplusplus
extern "C" {
#endif

class tklib_gridmap{
 private:
  //variables
  double max_range;
  
  gsl_matrix_float* data;
  gsl_matrix* hurdles;

  void draw_post(gsl_vector* loc, double width);
 public:
  //variables
  double x_size, y_size, resolution;
  
  //constructor
  tklib_gridmap(){data=NULL; hurdles=NULL;  max_range = 30.0;}
  tklib_gridmap(double map_x_size, double map_y_size, double map_resolution);
  ~tklib_gridmap();

  //functions
  gsl_matrix_float* get_map();
  float get_value(int i, int j);
  void  set_value(int i, int j, float value);
  void  xy_to_ind(gsl_vector* xy, gsl_vector* ind);
  void  ind_to_xy(gsl_vector *ind, gsl_vector *xy);
  void  load_carmen_map(char* filename);
  int   save_carmen_map(char* filename);
  void publish();
  
  carmen_map_p to_carmen_map_noalloc();
  void  copy(tklib_gridmap* omap);
  
  //get the x and y size of the map
  double get_x_size(){return y_size;}
  double get_y_size(){return x_size;}

  //get the width and height of the map
  int get_map_width(){return data->size1;}
  int get_map_height(){return data->size2;}
  
  //determine whether a spline is free or not
  int path_free(SplineC *thespline);

  //returns the free locations of the map
  gsl_matrix* get_free_locations();
  gsl_matrix* get_free_inds();
  
  //returns the occupied locations in the map
  gsl_matrix* get_occupied_locations();
  gsl_matrix* get_occupied_inds();

  //determine whether an x, y location is free 
  int location_free(gsl_vector* xy);
  int location_occupied(gsl_vector* xy);
  
  //determine whether a particular index is free;
  int ind_free(gsl_vector* ind);
  int ind_occupied(gsl_vector* ind);

  //determine whether a box around an xy location is free
  int location_free(gsl_vector* xy, double radius);
  
  //get a random location in the map that has the radius free
  gsl_vector* get_random_open_location(double radius);
  gsl_vector* get_random_open_location_from_pt(gsl_vector* pt, 
					       double distance, double box_radius);

  //add n random hurdle features to the map
  gsl_matrix* get_hurdles();
  gsl_vector* add_hurdle(double hurdle_width, double hurdle_size);
  void add_hurdles(double hurdle_width, double hurdle_size, int N);
    
  //downsample the map by a factor of ds
  gsl_matrix_float* downsample_map(int ds);
  
  //ray trace the map
  gsl_vector* ray_trace(double startx, double starty, gsl_vector* thetas);
  
  //minimum range to any obstacle from the particular point
  double min_range(gsl_vector *from_pt);
  double get_max_range();
};

#ifdef __cplusplus
}
#endif


#endif
