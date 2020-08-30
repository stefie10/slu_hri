#include "python_swig_utils.h"


gsl_matrix * psu_python_to_matrix(PyObject * input)
{
  int i, my_len1, my_len2;
  my_len2 = 0;
  if (!PySequence_Check(input)) {
    PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
    return NULL;
  }

  my_len1 = PyObject_Length(input);
  
  if (my_len1 > 0) {
    PyObject *o = PySequence_GetItem(input, 0);
    if (o == NULL) {
      PyErr_SetString(PyExc_TypeError,"First element is null?");
      return NULL;
    }
    my_len2 = PyObject_Length(o);
    Py_DECREF(o);
  }
  
  if(my_len1 == 0 || my_len2 == 0){
    return NULL;
  }
  else{
    //printf("wrap gsl_matrix2 %d\n", my_len2);  
    gsl_matrix* mat = gsl_matrix_calloc(my_len1, my_len2);
    
    for (i =0; i < my_len1; i++) {
      PyObject *o = PySequence_GetItem(input,i);
      int j;
      for(j = 0; j < my_len2; j++){
        PyObject *m = PySequence_GetItem(o,j);
        if (!PyNumber_Check(m)) {
	  gsl_matrix_free(mat);
          PyErr_SetString(PyExc_ValueError,"Expecting a sequence of numbers.");
          return NULL;
        }
        PyObject * flt = PyNumber_Float(m);
        gsl_matrix_set(mat, i, j, PyFloat_AsDouble(flt));
        Py_DECREF(flt);
        Py_DECREF(m);
      }
      Py_DECREF(o);
    }
    return mat;
  }
}


PyObject * psu_vector_to_python(gsl_vector * vector)
{
  PyObject* pyvec = PyList_New(0);
  if (vector == NULL) {
    return pyvec;
  }

  for(size_t i = 0; i < vector->size; i++){
    PyObject* pt = PyFloat_FromDouble(gsl_vector_get(vector, i));
    PyList_Append(pyvec, pt);
    Py_DECREF(pt);
  }
  return pyvec;
}
