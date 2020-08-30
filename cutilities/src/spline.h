#ifndef SPLINE1_H
#define SPLINE1_H

#ifdef __cplusplus
extern "C" {
#endif
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <math.h>
#include "gsl_utilities.h"

class SplineC{
 private:
  double x0, y0, x1, y1;
  double Dx0, Dx1, Dy0, Dy1;
  double start_theta, end_theta;
  double start_magnitude, end_magnitude;

  double cPr(double t);
  gsl_vector* getCoef(double y0, double y1, double Dy0, double Dy1);
  gsl_vector* getY(double y0, double y1, double Dy0, double Dy1, gsl_vector* time);
  gsl_vector* getDerivativeNormalized(double theta);
  

  //desireable to add these at some point
  //double al;
  //void setArcLength(void);
  //double arc_length();  
 public:
  SplineC(gsl_vector* start_pose, gsl_vector* end_pose, 
	  double start_magnitude, double end_magnitude);
  
  int at_destination(gsl_vector* curr_pt, double epsilon);

  gsl_vector* get_start_pose(void);
  gsl_vector* get_end_pose(void);
  gsl_vector* get_start_derivative(void);
  gsl_vector* get_end_derivative(void);
  double get_start_magnitude(void){return start_magnitude;}
  double get_end_magnitude(void){return end_magnitude;}

  gsl_matrix* value(gsl_vector* t);  

  //    #gets the arc length of the spline
  gsl_vector* getCoefX(void);
  gsl_vector* getCoefY(void);  
};


#ifdef __cplusplus
}
#endif

#endif


