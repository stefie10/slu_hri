#include "gsl_python.h"

PyObject* gsl_matrix_to_pyobject(gsl_matrix* matrix_in){
  PyObject* mylist = PyList_New(0);
  
  size_t i, j;
  for(i=0;i<matrix_in->size1;i++){
    PyObject* tmp_list = PyList_New(0);
    for(j=0;j<matrix_in->size2;j++){
      PyObject* myfloat = PyFloat_FromDouble(gsl_matrix_get(matrix_in , i, j));
      
      PyList_Append(tmp_list, myfloat);
      Py_DECREF(myfloat);
    }

    PyList_Append(mylist, tmp_list);
    Py_DECREF(tmp_list);
  }
  
  return mylist;
}

PyObject* gsl_vector_to_pyobject(gsl_vector* vector_in){
  PyObject* mylist = PyList_New(0);
  
  size_t i;
  for(i=0;i<vector_in->size;i++){
    PyObject* myfloat = PyFloat_FromDouble(gsl_vector_get(vector_in , i));
      
    PyList_Append(mylist, myfloat);
    Py_DECREF(myfloat);
  }
  
  return mylist;
}


gsl_matrix* pyobject_to_gsl_matrix(PyObject* list){
  int y_size = PyList_Size(list);
  
  if(y_size <= 0){
    //fprintf(stderr, "NULL pointer matrix\n");
    //gsl_matrix* ret_mat = gsl_matrix_calloc(1, 1);
    //gsl_matrix_set(ret_mat,0,0, MATRIX_IS_EMPTY);
    return NULL;
  }
  
  int x_size = PyList_Size(PyList_GetItem(list, 0));
  gsl_matrix* ret_mat = gsl_matrix_calloc(y_size, x_size);

  int i, j;
  for(i=0;i<y_size;i++){
    PyObject* row = PyList_GetItem(list, i);
    
    for(j=0;j<x_size;j++){
      PyObject* elt = PyList_GetItem(row, j);
      
      double double_elt = PyFloat_AsDouble(elt);
      gsl_matrix_set(ret_mat, i, j, double_elt);
      Py_DECREF(elt);
    }
    Py_DECREF(row);
  }
  
  return ret_mat;
}



gsl_vector* pyobject_to_gsl_vector(PyObject* list){
  int y_size = PyList_Size(list);
  
  if(y_size <= 0){
    //fprintf(stderr, "NULL pointer vector\n");
    return NULL;
  }
  //fprintf(stderr, "y_size%d\n", y_size);
  gsl_vector* ret_vec= gsl_vector_calloc(y_size);
  
  int i;
  for(i=0;i<y_size;i++){
    PyObject* elt = PyList_GetItem(list, i);
    
    double double_elt = PyFloat_AsDouble(elt);
    gsl_vector_set(ret_vec, i, double_elt);
    Py_DECREF(elt);
  }
  
  return ret_vec;
}
