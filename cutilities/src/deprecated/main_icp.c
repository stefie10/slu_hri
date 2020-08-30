//#include "quat2ang.h"
#include <gsl/gsl_matrix.h>
#include <gsl_utilities.h>
#include <procrustes.h>

void test1(){
  while(1){
  gsl_matrix* pts = gsl_matrix_alloc(3,4);
  gsl_matrix* modelpts = gsl_matrix_alloc(3,4);
  
  //pt 1
  gsl_matrix_set(pts, 0,0, 0.0);
  gsl_matrix_set(pts, 1,0, 0.0);
  gsl_matrix_set(pts, 2,0, 0.0);

  //pt 2
  gsl_matrix_set(pts, 0,1, 1.0);
  gsl_matrix_set(pts, 1,1, 0.0);
  gsl_matrix_set(pts, 2,1, 0.0);

  //pt 3
  gsl_matrix_set(pts, 0,2, 1.0);
  gsl_matrix_set(pts, 1,2, 1.0);
  gsl_matrix_set(pts, 2,2, 0.0);
  
  //pt 4
  gsl_matrix_set(pts, 0,3, 0.0);
  gsl_matrix_set(pts, 1,3, 1.0);
  gsl_matrix_set(pts, 2,3, 0.0);
  
  //pt 1
  gsl_matrix_set(modelpts, 0,0, 0.0);
  gsl_matrix_set(modelpts, 1,0, 0.0);
  gsl_matrix_set(modelpts, 2,0, 0.0);

  //pt 2
  gsl_matrix_set(modelpts, 0,1, 0.0);
  gsl_matrix_set(modelpts, 1,1, -0.9);
  gsl_matrix_set(modelpts, 2,1, 0.0);

  //pt 3
  gsl_matrix_set(modelpts, 0,2, 0.9);
  gsl_matrix_set(modelpts, 1,2, -0.9);
  gsl_matrix_set(modelpts, 2,2, 0.0);
  
  //pt 4
  gsl_matrix_set(modelpts, 0,3, 0.9);
  gsl_matrix_set(modelpts, 1,3, 0.0);
  gsl_matrix_set(modelpts, 2,3, 0.0);

  double sse;
  /*gsl_matrix* rotated_pts = gsl_matrix_calloc(pts->size1, pts->size2);
  gsl_matrix* R = gsl_matrix_calloc(3,3);
  gsl_matrix* t = gsl_matrix_calloc(3,1);*/
  
  printf("initial point sets\nstart points-->\n");
  tklib_matrix_printf(pts);
  printf("model points >>>>\n");
  tklib_matrix_printf(modelpts);
  printf("starting procrustes\n");

  gsl_matrix* rotated_pts = icp(pts, modelpts, 0.01, 0.1);
  //sse = procrustes_quaternion(modelpts, pts, rotated_pts, R, t);
  
  printf("**************\n");
  printf("rotated pts\n");
  tklib_matrix_printf(rotated_pts);
  /*printf("R\n");
  tklib_matrix_printf(R);
  printf("t\n");
  tklib_matrix_printf(t);
  printf("sse %f\n", sse);*/
  gsl_matrix_free(modelpts);
  gsl_matrix_free(pts);
  gsl_matrix_free(rotated_pts);
  
  }
}


void test2(){
  gsl_matrix* pts = gsl_matrix_alloc(3,4);
  gsl_matrix* modelpts = gsl_matrix_alloc(3,4);
  
  //pt 1
  
  gsl_matrix_set(pts, 0,0, 0.0);
  gsl_matrix_set(pts, 1,0, 0.0);
  gsl_matrix_set(pts, 2,0, 0.0);

  //pt 2
  gsl_matrix_set(pts, 0,1, 1.0);
  gsl_matrix_set(pts, 1,1, 0.0);
  gsl_matrix_set(pts, 2,1, 0.0);

  //pt 3
  gsl_matrix_set(pts, 0,2, 1.0);
  gsl_matrix_set(pts, 1,2, 1.0);
  gsl_matrix_set(pts, 2,2, 0.0);
  
  //pt 4
  gsl_matrix_set(pts, 0,3, 0.0);
  gsl_matrix_set(pts, 1,3, 1.0);
  gsl_matrix_set(pts, 2,3, 0.0);
  
  //pt 1
  gsl_matrix_set(modelpts, 0,0, 0.0);
  gsl_matrix_set(modelpts, 1,0, 0.0);
  gsl_matrix_set(modelpts, 2,0, 0.0);

  //pt 2
  gsl_matrix_set(modelpts, 0,1, 0.0);
  gsl_matrix_set(modelpts, 1,1, -0.9);
  gsl_matrix_set(modelpts, 2,1, 0.0);

  //pt 3
  gsl_matrix_set(modelpts, 0,2, 0.9);
  gsl_matrix_set(modelpts, 1,2, -0.9);
  gsl_matrix_set(modelpts, 2,2, 0.0);
  
  //pt 4
  gsl_matrix_set(modelpts, 0,3, 0.9);
  gsl_matrix_set(modelpts, 1,3, 0.0);
  gsl_matrix_set(modelpts, 2,3, 0.0);

  double sse;
  /*gsl_matrix* rotated_pts = gsl_matrix_calloc(pts->size1, pts->size2);
  gsl_matrix* R = gsl_matrix_calloc(3,3);
  gsl_matrix* t = gsl_matrix_calloc(3,1);*/
  
  printf("initial point sets\nstart points-->\n");
  tklib_matrix_printf(pts);
  printf("model points >>>>\n");
  tklib_matrix_printf(modelpts);
  printf("starting procrustes\n");

  gsl_matrix* rotated_pts = icp(modelpts, pts, 0.01, 0.1);
  //sse = procrustes_quaternion(modelpts, pts, rotated_pts, R, t);
  
  printf("**************\n");
  printf("rotated pts\n");
  tklib_matrix_printf(rotated_pts);
  /*printf("R\n");
  tklib_matrix_printf(R);
  printf("t\n");
  tklib_matrix_printf(t);
  printf("sse %f\n", sse);*/
  
}


void test3(){
  gsl_matrix* pts = gsl_matrix_alloc(3,7);
  
  //pt 1
  gsl_matrix_set(pts, 0,0, 0.0);
  gsl_matrix_set(pts, 1,0, 0.0);
  gsl_matrix_set(pts, 2,0, 0.0);

  //pt 2
  gsl_matrix_set(pts, 0,1, 1.0);
  gsl_matrix_set(pts, 1,1, 0.0);
  gsl_matrix_set(pts, 2,1, 0.0);

  //pt 3
  gsl_matrix_set(pts, 0,2, 1.0);
  gsl_matrix_set(pts, 1,2, 1.0);
  gsl_matrix_set(pts, 2,2, 0.0);
  
  //pt 4
  gsl_matrix_set(pts, 0,3, 0.0);
  gsl_matrix_set(pts, 1,3, 1.0);
  gsl_matrix_set(pts, 2,3, 0.0);
  
  //pt 2
  gsl_matrix_set(pts, 0,4, 0.0);
  gsl_matrix_set(pts, 1,4, -0.9);
  gsl_matrix_set(pts, 2,4, 0.0);

  //pt 3
  gsl_matrix_set(pts, 0,5, 0.9);
  gsl_matrix_set(pts, 1,5, -0.9);
  gsl_matrix_set(pts, 2,5, 0.0);
  
  //pt 4
  gsl_matrix_set(pts, 0,6, 0.9);
  gsl_matrix_set(pts, 1,6, 0.0);
  gsl_matrix_set(pts, 2,6, 0.0);
  
  printf("starting points\n");
  tklib_matrix_printf(pts);

  /*gsl_vector* test_vec = gsl_vector_calloc(3);
  gsl_vector_set(test_vec, 0, 1.0);
  gsl_vector_set(test_vec, 1, -1.0);
  gsl_vector_set(test_vec, 2, 0.0);
  printf("******************\n");
  printf("query vec\n");
  tklib_vector_printf(test_vec);
  int index;
  gsl_vector* ret_vec = gsl_vector_calloc(3);
  NN(test_vec, pts, &index, ret_vec);
  printf("****************\n");
  printf("nearest neighbor index %d\n", index);

  tklib_vector_printf(ret_vec);*/

  gsl_matrix* test_mat = gsl_matrix_calloc(3, 2);
  gsl_matrix_set(test_mat, 0, 0, -0.9);
  gsl_matrix_set(test_mat, 1, 0, -0.9);
  gsl_matrix_set(test_mat, 2, 0, 0.0);

  gsl_matrix_set(test_mat, 0, 1, 0.0);
  gsl_matrix_set(test_mat, 1, 1, 0.0);
  gsl_matrix_set(test_mat, 2, 1, 0.0);
  printf("******************\n");
  tklib_matrix_printf(test_mat);
  int index;
  //gsl_matrix* ret_mat = gsl_matrix_calloc(3, 2);
  gsl_matrix* ret_mat = NNs(test_mat, pts);
  printf("result-->\n");
  tklib_matrix_printf(ret_mat);
  
}


void test4(){
  gsl_matrix* pts = gsl_matrix_alloc(3,4);
  gsl_matrix* modelpts = gsl_matrix_alloc(3,4);
  
  //pt1
  gsl_matrix_set(pts, 0,0, 0.0);
  gsl_matrix_set(pts, 1,0, 0.0);
  gsl_matrix_set(pts, 2,0, 0.0);

  //pt 1
  gsl_matrix_set(modelpts, 0,0, 0.0);
  gsl_matrix_set(modelpts, 1,0, 0.0);
  gsl_matrix_set(modelpts, 2,0, 0.0);

  //pt 2
  gsl_matrix_set(pts, 0,1, 1.0);
  gsl_matrix_set(pts, 1,1, 0.0);
  gsl_matrix_set(pts, 2,1, 0.0);

  //pt 2
  gsl_matrix_set(modelpts, 0,1, 0.0);
  gsl_matrix_set(modelpts, 1,1, -0.9);
  gsl_matrix_set(modelpts, 2,1, 0.0);

  //pt 3
  gsl_matrix_set(pts, 0,2, 1.0);
  gsl_matrix_set(pts, 1,2, 1.0);
  gsl_matrix_set(pts, 2,2, 0.0);
  
  //pt 3
  gsl_matrix_set(modelpts, 0,2, 0.9);
  gsl_matrix_set(modelpts, 1,2, -0.9);
  gsl_matrix_set(modelpts, 2,2, 0.0);

  //pt 4
  gsl_matrix_set(pts, 0,3, 0.0);
  gsl_matrix_set(pts, 1,3, 1.0);
  gsl_matrix_set(pts, 2,3, 0.0);
  
  //pt 4
  gsl_matrix_set(modelpts, 0,3, -0.9);
  gsl_matrix_set(modelpts, 1,3, 0.0);
  gsl_matrix_set(modelpts, 2,3, 0.0);

  double mysse = tklib_sse(pts, modelpts);
  printf("sse-->%f\n", mysse);
}




int main(int argc, char** argv){
  fprintf(stderr, "running test1\n");
  test1();
  //test2();
  //test3();
  //test4();
}
