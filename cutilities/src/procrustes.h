#include <gsl/gsl_matrix.h>
#include "nearest_neighbor.h"
#include "gsl_utilities.h"
#include "quaternion.h"

#ifndef PROCRUSTES_H
#define PROCRUSTES_H


#ifdef __cplusplus
extern "C" {
#endif
  class procrustes{
  private:
    gsl_matrix* rotated_pts;
    gsl_matrix* R;
    gsl_vector* t;
  public:
    double sse;
    
    procrustes(){
      rotated_pts = NULL;
      R = NULL;
      t = NULL;
    }
    
    double run(gsl_matrix* measured_pts, gsl_matrix* model_pts);
    
    gsl_vector* get_translation(){
      gsl_vector* tret = gsl_vector_alloc(t->size);
      gsl_vector_memcpy(tret, t);
      return tret;
    }  
    
    gsl_matrix* get_rotation(){
      gsl_matrix* Rret = gsl_matrix_alloc(R->size1, R->size2);
      gsl_matrix_memcpy(Rret, R);
      return Rret;
    }
    
    gsl_matrix* get_rotated_points(){
      gsl_matrix* rotated_ret = gsl_matrix_alloc(rotated_pts->size1, rotated_pts->size2);
      gsl_matrix_memcpy(rotated_ret, rotated_pts);
      return rotated_ret;
    }
  };
  

  
  double procrustesSVD(gsl_matrix* model_pts, gsl_matrix* pts, 
		       gsl_matrix* rotated_pts, gsl_matrix* R, gsl_vector* t);

  //double procrustes_quaternion(gsl_matrix* model_pts, gsl_matrix* pts, 
  //			     gsl_matrix* rotated_pts, gsl_matrix* R, gsl_matrix* t);

  //gsl_matrix* icp(gsl_matrix* measured_points, gsl_matrix* model_points, double tau, double maxsse);
#ifdef __cplusplus
}
#endif


#endif
