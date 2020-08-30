#ifndef PYTHON_SWIG_UTILS_H
#define PYTHON_SWIG_UTILS_H
#include <Python.h>
#include <gsl/gsl_matrix.h>

gsl_matrix * psu_python_to_matrix(PyObject * input);

PyObject * psu_vector_to_python(gsl_vector * vector);

#endif

