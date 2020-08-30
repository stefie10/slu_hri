%module cMath2d
%{
#define SWIG_FILE_WITH_INIT
#include "math2d.h"
%}

%include "numpy.i"
%init %{
import_array();
%}


%typemap(in) (line l1, line l2, double * out, int dim) {
  
}

%typemap(in) point(point temp) {
  PyObject * v1 = PySequence_GetItem($input, 0);
  PyObject * v2 = PySequence_GetItem($input, 1);
  temp.x = PyFloat_AsDouble(v1);
  temp.y = PyFloat_AsDouble(v2);

  Py_DECREF(v1);
  Py_DECREF(v2);
  $1 = temp;
}

%typemap(in) pose(pose temp) {
  PyObject * v1 = PySequence_GetItem($input, 0);
  PyObject * v2 = PySequence_GetItem($input, 1);
  PyObject * v3 = PySequence_GetItem($input, 2);
  temp.x = PyFloat_AsDouble(v1);
  temp.y = PyFloat_AsDouble(v2);
  temp.theta = PyFloat_AsDouble(v3);

  Py_DECREF(v1);
  Py_DECREF(v2);
  Py_DECREF(v3);
  $1 = temp;
}

%typemap(out) boolean { 
  return PyBool_FromLong(result);	     
}

%typemap(out) double[] { 
  return PyBool_FromLong(result);	     
}

%typemap(out) point {
  PyObject * out = PyTuple_New(2);
  PyTuple_SET_ITEM(out, 0, PyFloat_FromDouble(result.x));
  PyTuple_SET_ITEM(out, 1, PyFloat_FromDouble(result.y));
  $result = out;
}


%typemap(out) pose {
  PyObject * out = PyTuple_New(3);
  PyTuple_SET_ITEM(out, 0, PyFloat_FromDouble(result.x));
  PyTuple_SET_ITEM(out, 1, PyFloat_FromDouble(result.y));
  PyTuple_SET_ITEM(out, 2				, PyFloat_FromDouble(result.theta));
  $result = out;
}

%typemap(out) line {
  PyObject * out = PyList_New(result.length);
  int i;
  for (i = 0; i < result.length; i++) {
    PyObject * pt = PyTuple_New(2);
    
    PyTuple_SET_ITEM(pt, 0, PyFloat_FromDouble(result.points[i].x));
    PyTuple_SET_ITEM(pt, 1, PyFloat_FromDouble(result.points[i].y));    
    PyList_SET_ITEM(out, i, pt);
  }
  free(result.points);
  result.points = NULL;
  $result = out;
}

%typemap(in) segment(segment temp) {
  if (PySequence_Length($input) != 2) {
    PyErr_SetString(PyExc_ValueError, "Segment must contain two points.");
    return NULL;
  }
  {
    PyObject * v1 = PySequence_GetItem($input, 0);
    PyObject * w1 = PySequence_GetItem(v1, 0);
    PyObject * w2 = PySequence_GetItem(v1, 1);

    temp.start.x = PyFloat_AsDouble(w1);
    temp.start.y = PyFloat_AsDouble(w2);
    Py_DECREF(v1);
    Py_DECREF(w1);
    Py_DECREF(w2);
  }

  {
    PyObject * v1 = PySequence_GetItem($input, 1);
    PyObject * w1 = PySequence_GetItem(v1, 0);
    PyObject * w2 = PySequence_GetItem(v1, 1);
  
    temp.end.x = PyFloat_AsDouble(w1);
    temp.end.y = PyFloat_AsDouble(w2);
    Py_DECREF(v1);
    Py_DECREF(w1);
    Py_DECREF(w2);
  }

  $1 = temp;
}


%typemap(in) line(line temp) {
  temp.length = PySequence_Length($input);
  temp.points = (point *) malloc(sizeof(point) * temp.length);
  int i;
  for (i = 0; i < temp.length; i++) {
    PyObject * v1 = PySequence_GetItem($input, i);
    PyObject * w1 = PySequence_GetItem(v1, 0);
    PyObject * w2 = PySequence_GetItem(v1, 1);  
    temp.points[i].x = PyFloat_AsDouble(w1);
    temp.points[i].y = PyFloat_AsDouble(w2);
    Py_DECREF(v1);
    Py_DECREF(w1);
    Py_DECREF(w2);
  }
  $1 = temp;
}

// This cleans up the char ** array we malloc'd before the function call
%typemap(freearg) line {
  if ($1.points != NULL) {
    free((point *) $1.points);
  }
}


%ignore squareDistances;
%inline %{
PyObject * numpySquareDistances(line l1, line l2) {
  assert(l1.length == l2.length);
  npy_intp dims = l1.length;
  PyObject *array = PyArray_SimpleNew(1, &dims, NPY_DOUBLE);
  assert(array != NULL);
  double * aData = (double *) (((PyArrayObject *)array)->data);
  squareDistances(l1, l2, aData, l1.length);
  return array;
}
%}

%include math2d.h	