#include "spline.h"


SplineC::SplineC(gsl_vector* start_pose, gsl_vector* end_pose, 
		 double st_magnitude, double en_magnitude){
  x0 = gsl_vector_get(start_pose, 0);
  y0 = gsl_vector_get(start_pose, 1);
  
  x1 = gsl_vector_get(end_pose, 0);
  y1 = gsl_vector_get(end_pose, 1);
  
  start_theta = gsl_vector_get(start_pose, 2);
  end_theta = gsl_vector_get(end_pose, 2);

  start_magnitude = st_magnitude;
  end_magnitude = en_magnitude;
  
  gsl_vector* DX0 = getDerivativeNormalized(start_theta);
  Dx0 = st_magnitude * gsl_vector_get(DX0, 0); 
  Dy0 = st_magnitude * gsl_vector_get(DX0, 1);
  
  gsl_vector* DX1 = getDerivativeNormalized(end_theta);
  Dx1 = en_magnitude * gsl_vector_get(DX1, 0); 
  Dy1 = en_magnitude * gsl_vector_get(DX1, 1);
  
  gsl_vector_free(DX0);
  gsl_vector_free(DX1);
}

gsl_vector* SplineC::get_start_pose(void){
  gsl_vector *ret_vec = gsl_vector_alloc(3);
  gsl_vector_set(ret_vec, 0, x0);
  gsl_vector_set(ret_vec, 1, y0);
  gsl_vector_set(ret_vec, 2, start_theta);

  return ret_vec;
}
gsl_vector* SplineC::get_end_pose(void){
  gsl_vector *ret_vec = gsl_vector_alloc(3);
  gsl_vector_set(ret_vec, 0, x1);
  gsl_vector_set(ret_vec, 1, y1);
  gsl_vector_set(ret_vec, 2, end_theta);

  return ret_vec;
}

gsl_matrix* SplineC::value(gsl_vector* time){
  gsl_vector* X = getY(x0, x1, Dx0, Dx1, time);
  gsl_vector* Y = getY(y0, y1, Dy0, Dy1, time);

  gsl_matrix* retpts = gsl_matrix_alloc(2, X->size);

  gsl_matrix_set_row(retpts, 0, X);
  gsl_matrix_set_row(retpts, 1, Y);

  gsl_vector_free(X);
  gsl_vector_free(Y);
  return retpts;
}



gsl_vector* SplineC::get_start_derivative(void){
  gsl_vector *ret_vec = gsl_vector_alloc(2);

  gsl_vector_set(ret_vec, 0, Dx0);
  gsl_vector_set(ret_vec, 1, Dy0);

  return ret_vec;
}

gsl_vector* SplineC::get_end_derivative(void){
  gsl_vector *ret_vec = gsl_vector_alloc(2);

  gsl_vector_set(ret_vec, 0, Dx1);
  gsl_vector_set(ret_vec, 1, Dy1);

  return ret_vec;
}

//    #gets the arc length of the spline
/*void SplineC::setArcLength(void){
  //self.al = integrate.quad(self.cPr, 0, 1);
  //fixme
  }*/
        
/*double SplineC::arc_length(){
  return al;
  }*/


int SplineC::at_destination(gsl_vector* curr_pt, double epsilon){
  gsl_vector* dest = gsl_vector_alloc(2);
  gsl_vector_set(dest, 0, x1);
  gsl_vector_set(dest, 1, y1);
  
  double dist = tklib_euclidean_distance(curr_pt, dest);
  
  gsl_vector_free(dest);
  if(dist < epsilon)
    return 1;

  return 0;
}



gsl_vector* SplineC::getDerivativeNormalized(double theta){
  //return [cos(theta), sin(theta)];
  gsl_vector* myvec = gsl_vector_alloc(2);
  gsl_vector_set(myvec, 0, cos(theta));
  gsl_vector_set(myvec, 1, sin(theta));
  
  return myvec;
}

gsl_vector* SplineC::getY(double y0, double y1, double Dy0, double Dy1, gsl_vector* t){
  double a0 = y0;
  double b0 = Dy0;
  double c0 = 3*(y1 - y0) - 2*Dy0 - Dy1;
  double d0 = 2*(y0 - y1) + Dy0 + Dy1;
    

  //a0 + b0*t + c0*(t**2) + d0*(t**3);
  gsl_vector* t1 = gsl_vector_calloc(t->size);
  gsl_vector_add_constant(t1, a0);
  
  gsl_vector* t2 = gsl_vector_alloc(t->size);
  gsl_vector_memcpy(t2, t);
  gsl_vector_scale(t2, b0);

  gsl_vector* t3 = gsl_vector_alloc(t->size);
  gsl_vector_memcpy(t3, t);
  gsl_vector_mul(t3, t);
  gsl_vector_scale(t3, c0);

  gsl_vector* t4 = gsl_vector_alloc(t->size);
  gsl_vector_memcpy(t4, t);
  gsl_vector_mul(t4, t);
  gsl_vector_mul(t4, t);
  gsl_vector_scale(t4, d0);

  gsl_vector_add(t1, t2);
  gsl_vector_add(t1, t3);
  gsl_vector_add(t1, t4);

  gsl_vector_free(t2);
  gsl_vector_free(t3);
  gsl_vector_free(t4);
    
  return t1;
}
  
double SplineC::cPr(double t){
  gsl_vector* vX = getCoefX();
  double ax = gsl_vector_get(vX, 0);
  double bx= gsl_vector_get(vX, 1);
  double cx= gsl_vector_get(vX, 2);

  gsl_vector* vY = getCoefY();
  double ay = gsl_vector_get(vY, 0);
  double by= gsl_vector_get(vY, 1);
  double cy= gsl_vector_get(vY, 2);
    
  gsl_vector_free(vX);
  gsl_vector_free(vY);
  return pow(pow(3*ax*(pow(t,2)) + 2*bx*t + cx,2) + pow(3*ay*pow(t,2) + 2*by*t + cy,2), (0.5));
}
  
gsl_vector* SplineC::getCoefX(void){
  return getCoef(x0, x1, Dx0, Dx1);
}
gsl_vector* SplineC::getCoefY(void){
  return getCoef(y0, y1, Dy0, Dy1);
}
  
gsl_vector* SplineC::getCoef(double y0, double y1, double Dy0, double Dy1){
  double a0 = y0;
  double b0 = Dy0;
  double c0 = 3*(y1 - y0) - 2*Dy0 - Dy1;
  double d0 = 2*(y0 - y1) + Dy0 + Dy1;
    
  gsl_vector* retvec = gsl_vector_alloc(4);
  gsl_vector_set(retvec, 0, d0);
  gsl_vector_set(retvec, 1, c0);
  gsl_vector_set(retvec, 2, b0);
  gsl_vector_set(retvec, 3, a0);
    
  return retvec;
}
    
