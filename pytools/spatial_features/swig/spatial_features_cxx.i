%module(directors="1") spatial_features_cxx
%{
#include "math2d.h"
#include "math3d.h"
#include "avs.h"
#include "spatial_features.h"
#include "spatial_feature_extractor.h"
#include "python_swig_utils.h"
%}



%typemap(in) math3d_prism_t {
  math3d_prism_t prism = math3d_prism_init();
  {
    PyObject * zStart = PyObject_GetAttrString($input, "zStart");
    if (zStart == NULL) {
      PyErr_SetString(PyExc_ValueError,"Couldn't get zStart.");
      return NULL;
    }

    prism.z_start = PyFloat_AsDouble(zStart);
    Py_DECREF(zStart);
  }
  {
    PyObject * zEnd = PyObject_GetAttrString($input, "zEnd");
    if (zEnd == NULL) {
      PyErr_SetString(PyExc_ValueError,"Couldn't get zEnd.");
      return NULL;
    }

    prism.z_end = PyFloat_AsDouble(zEnd);
    Py_DECREF(zEnd);
  }
  {
    PyObject * points_xy = PyObject_GetAttrString($input, "points_xy");
    prism.points_xy = psu_python_to_matrix(points_xy);
    Py_DECREF(points_xy);
  }      
  $1 = prism;
 }

%typemap(freearg) math3d_prism_t {
  if ($1.initialized == 1) {
    math3d_prism_free($1);
  }
}


%include "std_string.i"
%include "std_vector.i"

%include "typemaps.i"
%include "carrays.i"
%include "../../gsl_utilities/swig/typemaps.i"

%array_class(double, doubleArray);
%array_class(float, floatArray);


namespace std{
    %template(vectori) vector<int>;
    %template(vectord) vector<double>;
  %template(vectors) vector<string>;
   %typemap(out) vector<string>
      {
        PyObject * obj = PyList_New(0);
        for(size_t i = 0; i < $1.size(); i++) {
          PyObject* st = PyString_FromString($1[i].c_str());
          PyList_Append(obj, st);
          Py_DECREF(st);    
        }
        $result = obj;
}
}
%newobject flu_binarize_feature_uniform;
%typemap(newfree) char * "free($1);";


%include "math2d.h"
%include "math3d.h"
%include "avs.h"
%include "spatial_features.h"
%include "spatial_feature_extractor.h"
