#include "line.h"

double line_perpendicular_distance(gsl_vector* pt, double m, double b){
  double m2;
  if(m == 0)
    m2 = 10000000.0;
  else
    m2 = -1.0*(1.0/m);
  
  double b2 = gsl_vector_get(pt, 1) - (m2 * gsl_vector_get(pt, 0));
  double x = (b2 - b)/(m - m2);
  double y = m*x + b;
  gsl_vector* intercept = gsl_vector_alloc(2);
  gsl_vector_set(intercept, 0, x);
  gsl_vector_set(intercept, 1, y);
  
  double dist = tklib_euclidean_distance(intercept, pt);
  gsl_vector_free(intercept);
  return dist;
}


void get_line_parameters_m_pt(double m, gsl_vector* pt, 
			      double* m_ret, double* b_ret){
  double b = -m*gsl_vector_get(pt, 0) + gsl_vector_get(pt,1);
  *m_ret = m;
  *b_ret = b;
}

void get_line_parameters_m_b(gsl_vector* pt1, gsl_vector* pt2, 
			     double* m_ret, double* b_ret){
  double num = (gsl_vector_get(pt1, 1)-gsl_vector_get(pt2, 1));
  double den = (gsl_vector_get(pt1,0)-gsl_vector_get(pt2, 0));
  if(den == 0)
    den += 0.000001;
  double m = num/den;
  double b = gsl_vector_get(pt1, 1) - gsl_vector_get(pt1, 0)*m;
  
  *m_ret = m;
  *b_ret = b;
}
