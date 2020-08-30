#include "box_window.h"

gsl_matrix* box_inwindow(gsl_matrix* pts, gsl_vector* x_st, gsl_vector* x_end,
			 double box_height, double box_dw, 
			 double width_line_m, double width_line_b, 
			 double height_line_m, double height_line_b){
  double d_st_end = tklib_euclidean_distance(x_st, x_end);
  gsl_matrix* in_rect_pts = gsl_matrix_alloc(pts->size1, pts->size2);
  
  int pt_count = 0;
  size_t i;
  double d_height, d_width;
  
  //printf("pts:->%d, %d\n", pts->size1, pts->size2);
  //tklib_matrix_printf(pts);
  //printf("x_st -> x_end\n");
  //tklib_vector_printf(x_st);
  //tklib_vector_printf(x_end);
  for(i=0;i<pts->size2;i++){
    gsl_vector_view mypt = gsl_matrix_column(pts, i);
    d_height = line_perpendicular_distance(&mypt.vector, width_line_m, width_line_b);
    d_width = line_perpendicular_distance(&mypt.vector, height_line_m, height_line_b);
    //printf("dh: %f\n", d_height);
    //printf("dw: %f\n", d_width);
    if(d_height < (box_height / 2.0) and d_width < ((d_st_end /2.0) + box_dw) ){
      gsl_matrix_set_col(in_rect_pts, pt_count, &mypt.vector);
      pt_count+=1;
    }
  }
  
  //printf("in_rect_pts:->%d, %d\n", in_rect_pts->size1, pt_count);

  
  gsl_matrix_view rect_pts = gsl_matrix_submatrix(in_rect_pts, 0, 0, 
						  in_rect_pts->size1, pt_count);
  
  gsl_matrix* ret_pts = gsl_matrix_calloc(in_rect_pts->size1, pt_count);
  gsl_matrix_memcpy(ret_pts, &rect_pts.matrix);
  
  gsl_matrix_free(in_rect_pts);
  return ret_pts;
}



gsl_matrix* box_outwindow(gsl_matrix* pts, gsl_vector* x_st, gsl_vector* x_end,
			 double box_height, double box_dw, 
			 double width_line_m, double width_line_b, 
			 double height_line_m, double height_line_b){
  double d_st_end = tklib_euclidean_distance(x_st, x_end);
  gsl_matrix* out_rect_pts = gsl_matrix_alloc(pts->size1, pts->size2);
  
  int pt_count = 0;
  size_t i;
  double d_height, d_width;
  for(i=0;i<pts->size2;i++){
    gsl_vector_view mypt = gsl_matrix_column(pts, i);
    d_height = line_perpendicular_distance(&mypt.vector, width_line_m, width_line_b);
    d_width = line_perpendicular_distance(&mypt.vector, height_line_m, height_line_b);
    
    if(d_height > (box_height / 2.0) or d_width > ((d_st_end /2.0) + box_dw) ){
      gsl_matrix_set_col(out_rect_pts, pt_count, &mypt.vector);
      pt_count+=1;
    }
  }

  
  if(out_rect_pts->size1 <= 0 || pt_count <= 0)
    return NULL;
  
  gsl_matrix_view rect_pts = gsl_matrix_submatrix(out_rect_pts, 0, 0, 
						  out_rect_pts->size1, pt_count);
  
  gsl_matrix* ret_pts = gsl_matrix_calloc(out_rect_pts->size1, pt_count);
  gsl_matrix_memcpy(ret_pts, &rect_pts.matrix);
  
  gsl_matrix_free(out_rect_pts);
  return ret_pts;
}


