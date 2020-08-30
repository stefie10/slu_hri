#ifndef AVS_H
#define AVS_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
struct avs_result
{
  gsl_vector * vsum;
  double height_exp;
  double height;
  double hightop_height;
  double lowtop_height;
  double avsg;
  double result;
};

void avs_free(struct avs_result result);

avs_result avs_avs(gsl_matrix * landmark, gsl_vector * figure_pt, 
                   gsl_vector * direction, 
                   double highgain,
                   double lam, double slope, double y_intercept);


double avs_sig(double x, double gain);
double avs_height(gsl_matrix * landmark, gsl_vector * figure_pt, 
                  gsl_vector * direction, double highgain, avs_result * r);
gsl_vector * avs_vector_sum(gsl_matrix * landmark, gsl_vector * figure_pt, 
                            gsl_vector * direction, double lam);
double avs_g(gsl_vector * vector, gsl_vector * direction,
             double slope, double y_intercept);



#endif
