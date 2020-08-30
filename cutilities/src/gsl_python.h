#ifndef GSL_PYTHON_H
#define GSL_PYTHON_H

#ifdef __cplusplus
extern "C" {
#endif
#include "Python.h"
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>


gsl_vector* pyobject_to_gsl_vector(PyObject* list);
gsl_matrix* pyobject_to_gsl_matrix(PyObject* list);

PyObject* gsl_matrix_to_pyobject(gsl_matrix* matrix_in);
PyObject* gsl_vector_to_pyobject(gsl_vector* vector_in);


#ifdef __cplusplus
}
#endif

#endif


