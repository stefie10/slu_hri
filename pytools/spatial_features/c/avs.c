#include "avs.h"
#include "math2d.h"

avs_result avs_avs(gsl_matrix * landmark, gsl_vector * figure_pt, 
                   gsl_vector * direction, 
                   double highgain,
                   double lam, double slope, double y_intercept)
{
  struct avs_result result;

  result.vsum = avs_vector_sum(landmark, figure_pt, direction, lam);
  result.height_exp = avs_height(landmark,
                                 figure_pt,
                                 direction, highgain, &result);
  result.avsg = avs_g(result.vsum, direction, slope, y_intercept);
  result.result = result.avsg * result.height_exp;
  return result;
}

double avs_sig(double x, double gain)
{
  return 1.0 / (1 + exp(gain * - x));
}

gsl_vector * avs_vector_sum(gsl_matrix * landmark, gsl_vector * figure_pt, 
                            gsl_vector * direction, double lam) 
{
  gsl_matrix * top = math2d_top(landmark, direction);
  double perimeter = math2d_perimeter(landmark);
  
  gsl_matrix * p_steps = math2d_step_along_polygon(landmark, perimeter/10);
  gsl_vector * focus_point = math2d_closest_point_on_line(top, figure_pt);
  double sigma = math2d_dist(figure_pt, focus_point);

  gsl_matrix * C_i = gsl_matrix_alloc(2, p_steps->size2);
  
  for (size_t i = 0; i < p_steps->size2; i++) {
    gsl_vector * p = &(gsl_matrix_column(p_steps, i).vector);
    double a_i = exp(-math2d_dist(p, focus_point) / (lam*sigma));
    gsl_vector * c_i = &(gsl_matrix_column(C_i, i).vector);
    gsl_vector_memcpy(c_i, figure_pt);
    gsl_vector_sub(c_i, p);
    gsl_vector_scale(c_i, 1.0/math2d_point_length(c_i));
    gsl_vector_scale(c_i, a_i);
  }
  gsl_vector * vector_sum = tklib_matrix_sum(C_i, 1);
  gsl_matrix_free(top);
  gsl_matrix_free(p_steps);
  gsl_vector_free(focus_point);
  gsl_matrix_free(C_i);
  return vector_sum;
}

double avs_height(gsl_matrix * landmark, gsl_vector * figure_pt, 
                  gsl_vector * direction, double highgain, avs_result * r)
{
  gsl_matrix * top = math2d_top(landmark, direction);
  gsl_vector * hightop = math2d_highest_point(top, direction);
  gsl_vector * lowtop = math2d_lowest_point(top, direction);
  double f_height = math2d_height_in_direction(figure_pt, direction);
  double hightop_height = math2d_height_in_direction(hightop, direction);
  double lowtop_height = math2d_height_in_direction(lowtop, direction);
  gsl_vector_free(hightop);
  gsl_vector_free(lowtop);
  gsl_matrix_free(top);
  double height_exp = (avs_sig(f_height - hightop_height, highgain) + 
                      avs_sig(f_height - lowtop_height, 1)) / 2.0;
  if (r != NULL) {
    r->hightop_height = hightop_height;
    r->lowtop_height = lowtop_height;
    r->height = 0.5 * (hightop_height + lowtop_height);

    r->height_exp = height_exp;
  }
  return height_exp;
}


double avs_g(gsl_vector * vector, gsl_vector * direction,
             double slope, double y_intercept)
{


  if (gsl_vector_get(vector, 0) == 0 &&
      gsl_vector_get(vector, 1) == 0) {
    return 0;
  } else {
    double theta = fabs(math2d_angle_between_points(vector, direction));
    return theta * slope + y_intercept;
  }
}


void avs_free(struct avs_result result)
{
  gsl_vector_free(result.vsum);
}
