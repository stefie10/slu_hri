%module(directors="1") gsl_utilities
%{
#include "gsl/gsl_matrix.h"
#include "gsl/gsl_vector.h"
#include "gsl/gsl_permutation.h"
#include "gsl_utilities.h"
#include "python_swig_utils.h"

void swig_gsl_error_handler (const char * reason,
				   const char * file,
				   int line, 
				   int gsl_errno) {
  printf("gsl file: %s:%d: %s (errno: %s (%d))\n", file, line, 
	 reason, gsl_strerror(gsl_errno), gsl_errno);
  PyErr_SetString(PyExc_ValueError, reason);

  PyObject * traceback =  PyImport_ImportModule("traceback");
  PyObject * method = PyObject_GetAttrString(traceback, "print_stack");
  PyObject * emptyTuple = PyTuple_New(0);
  PyObject_Call(method, emptyTuple, NULL);
  abort();
}

%}

%init %{

  gsl_set_error_handler(swig_gsl_error_handler);
%}



%include "typemaps.i"

%include "gsl_utilities.h"
