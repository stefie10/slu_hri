/* File : pyTklib.i */
%module(directors="1") pyTklib
%{

#include "EKF2D.h"
#include "procrustes.h"
#include "kmeans.h"
#include "hurdle_extractor.h"
#include <carmen/carmen.h>
#include "carmen_util.h"
#include "tklib_log_gridmap.h"
#include "gridmapping.h"
#include "noise_models.h"
#include "simulator.h"
#include "carmen_util.h"
#include "spline.h"
#include "carmen_subscribe.h"
#include "carmen_publish.h"
#include "python_swig_utils.h"
#include "gsl_utilities.h"
  %}


%newobject flu_binarize_feature_uniform;
%typemap(newfree) char * "free($1);";


%include "../../pytools/gsl_utilities/swig/typemaps.i"

%typemap(out) carmen_gridmapping_map_message*{
	PyObject* pymap = PyList_New(0);

	if($1 == NULL)
	    return pymap;
	
	int i, j;
	for(i=0; i<$1->size1; i++){
	  PyObject* row = PyList_New(0);
	  for(j=0;j<$1->size2;j++){
		  PyObject* pt = PyFloat_FromDouble($1->map[i*$1->size1+j]);
		  PyList_Append(row, pt);
		  Py_DECREF(pt);
          }
          PyList_Append(pymap, row);
	  Py_DECREF(row);
	}
	
	//have mat and pyvec add to hash
	PyObject *retdict = PyDict_New();

	PyObject *x_origin = PyFloat_FromDouble($1->x_origin);	
	PyObject *y_origin = PyFloat_FromDouble($1->y_origin);	
	PyObject *resolution = PyFloat_FromDouble($1->resolution);	
	PyObject *timestamp = PyFloat_FromDouble($1->timestamp);	
	PyObject *host_name = PyString_FromString($1->host);


	PyDict_SetItemString(retdict, "map", pymap);
	PyDict_SetItemString(retdict, "x_origin", x_origin);	
	PyDict_SetItemString(retdict, "y_origin", y_origin);	
	PyDict_SetItemString(retdict, "resolution", resolution);	
	PyDict_SetItemString(retdict, "timestamp", timestamp);	
	PyDict_SetItemString(retdict, "host_name", host_name);	

	Py_DECREF(pymap);
	Py_DECREF(x_origin);
	Py_DECREF(y_origin);
	Py_DECREF(resolution);
	Py_DECREF(timestamp);
	Py_DECREF(host_name);	
	
	$result = retdict;
	//free(map);
}



%typemap(out) carmen_ekf_message*{
	
	PyObject* pycov = PyList_New(0);

	if($1 == NULL)
	    return pycov;

	double*  cov = $1->covariance;
	int i, j;
	for(i=0; i<$1->size_mean; i++){
	  PyObject* row = PyList_New(0);
	  for(j=0;j<$1->size_mean;j++){
		  PyObject* pt = PyFloat_FromDouble(cov[i*$1->size_mean + j]);
		  PyList_Append(row, pt);
		  Py_DECREF(pt);
          }
          PyList_Append(pycov, row);
	  Py_DECREF(row);
	}
	

	PyObject* pymean = PyList_New(0);
	double* mean = $1->mean;
	for(i=0; i<$1->size_mean; i++){
	  PyObject* pt = PyFloat_FromDouble(mean[i]);
	  PyList_Append(pymean, pt);
	  Py_DECREF(pt);
	}
	

	//have mat and pyvec add to hash
	PyObject *retdict = PyDict_New();
	PyObject *timestamp = PyFloat_FromDouble($1->timestamp);	
	PyObject *host_name = PyString_FromString($1->host);

	PyDict_SetItemString(retdict, "cov", pycov);
	PyDict_SetItemString(retdict, "mean", pymean);	
	PyDict_SetItemString(retdict, "timestamp", timestamp);	
	PyDict_SetItemString(retdict, "host_name", host_name);	

	Py_DECREF(pycov);
	Py_DECREF(pymean);
	Py_DECREF(timestamp);
	Py_DECREF(host_name);	


	$result = retdict;
}

%typemap(out) carmen_gridmapping_ray_trace_message*{
	if($1 == NULL)
	    return PyList_New(0);

	PyObject* thetas = PyList_New(0);
	PyObject* readings = PyList_New(0);

	int i;
	for(i=0; i<$1->num_readings; i++){
		PyObject* pt = PyFloat_FromDouble($1->thetas[i]);
		PyList_Append(thetas, pt);
		PyObject* pt2 = PyFloat_FromDouble($1->readings[i]);
		PyList_Append(readings, pt2);
		Py_DECREF(pt);
		Py_DECREF(pt2);
        }


	PyObject *retdict = PyDict_New();
	PyObject* robot_pose = PyList_New(0);
	
	PyObject* x = PyFloat_FromDouble($1->x);
	PyObject* y = PyFloat_FromDouble($1->y);
	PyObject* theta = PyFloat_FromDouble($1->theta);
	PyList_Append(robot_pose, x);
	PyList_Append(robot_pose, y);
	PyList_Append(robot_pose, theta);

	PyDict_SetItemString(retdict, "robot_pose", robot_pose);
	PyDict_SetItemString(retdict, "thetas", thetas);
	PyDict_SetItemString(retdict, "readings", readings);	
	Py_DECREF(robot_pose);
	Py_DECREF(x);
	Py_DECREF(y);
	Py_DECREF(theta);	
	Py_DECREF(thetas);	
	Py_DECREF(readings);	

	$result = retdict;
}

%typemap(out) carmen_map_p{
	PyObject* pymap = PyList_New(0);
	//fprintf(stderr, "here0\n");
	if($1 == NULL)
	    return pymap;

	float** themap = $1->map;
	int i, j;
	for(i=0; i<$1->config.x_size; i++){
	  PyObject* row = PyList_New(0);
	  for(j=0;j<$1->config.y_size;j++){
		  PyObject* pt = PyFloat_FromDouble(themap[i][j]);
		  PyList_Append(row, pt);
		  Py_DECREF(pt);
          }
          PyList_Append(pymap, row);
	  Py_DECREF(row);
	}

	//have mat and pyvec add to hash
	PyObject *retdict = PyDict_New();
	//fprintf(stderr, "here1\n");	
	PyObject *x_size = PyFloat_FromDouble($1->config.x_size);	
	PyObject *y_size = PyFloat_FromDouble($1->config.y_size);	
	PyObject *resolution = PyFloat_FromDouble($1->config.resolution);	
	PyObject *map_name = PyString_FromString($1->config.map_name);
	
		
	PyDict_SetItemString(retdict, "map", pymap);
	PyDict_SetItemString(retdict, "x_size", x_size);	
	PyDict_SetItemString(retdict, "y_size", y_size);	
	PyDict_SetItemString(retdict, "resolution", resolution);	
	PyDict_SetItemString(retdict, "map_name", map_name);	
	//fprintf(stderr, "here3\n");	
	Py_DECREF(pymap);
	Py_DECREF(x_size);
	Py_DECREF(y_size);
	Py_DECREF(resolution);	
	Py_DECREF(map_name);
	//fprintf(stderr, "here3\n");	
	$result = retdict;
        carmen_map_destroy(&$1);
}




%typemap(out) EKF2D_filter_state*{
	PyObject* pyvec = PyList_New(0);

	if($1 == NULL)
	    return pyvec;

	gsl_vector * Uswig = $1->U;
	gsl_matrix* SIGMAswig = $1->SIGMA;
	gsl_vector * assoc_swig = $1->associations;
        int i;
	for(i=0; i<Uswig->size; i++){
	  PyObject* pt = PyFloat_FromDouble(gsl_vector_get(Uswig, i));
	  PyList_Append(pyvec, pt);
	  Py_DECREF(pt);
	}

	/*save the associations*/
	PyObject* pyvec2 = PyList_New(0);
	if(assoc_swig != NULL){
		for(i=0; i<assoc_swig->size; i++){
		  PyObject* pt = PyFloat_FromDouble(gsl_vector_get(assoc_swig, i));
		  PyList_Append(pyvec2, pt);
		  Py_DECREF(pt);
		}
	}

	PyObject* mat = PyList_New(0);

	if(SIGMAswig == NULL)
	    return mat;

	for(i=0; i<SIGMAswig->size1; i++){
	  PyObject* row = PyList_New(0);	
	  int j;
	  for(j=0;j<SIGMAswig->size2;j++){
		  PyObject* pt = PyFloat_FromDouble(gsl_matrix_get(SIGMAswig, i, j));
		  PyList_Append(row, pt);
		  Py_DECREF(pt);
          }
         PyList_Append(mat, row);
	 Py_DECREF(row);
	}

	//have mat and pyvec add to hash
	PyObject *retdict = PyDict_New();
	PyDict_SetItemString(retdict, "U", pyvec);
	PyDict_SetItemString(retdict, "associations", pyvec2);
	PyDict_SetItemString(retdict, "SIGMA", mat);
		
	Py_DECREF(mat);
	Py_DECREF(pyvec);
	Py_DECREF(pyvec2);
		
	$result = retdict;

	gsl_matrix_free($1->SIGMA);
	gsl_vector_free($1->U);
	if($1->associations != NULL)
		gsl_vector_free($1->associations);
        free((EKF2D_filter_state *) $1);
	
}





%typemap(in) marray* {
  //printf("converting marray\n");
  if (!PySequence_Check($input)) {
      PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
      return NULL;
  }
  else{
      //printf("wrap gsl_matrix2 %d\n", my_len2);  

      bool done = false;
      int rank = 0;  
      PyObject *o = $input;
      while(!done){
          if (PyList_Check(o)) {
	    o = PyList_GetItem(o,0);
	    rank+=1;
	  }
	  else
	      done=true;
	  
      }

      size_t i = 0;
      done = false;
      size_t mat_size[rank];
      o = $input;
      while(!done){
          if (PyList_Check(o)){
	      mat_size[i] = PyList_Size(o);
	      //printf("size: %d, %d ", i, mat_size[i]);
	      o = PyList_GetItem(o,0);
	      i+=1;
	  }
	  else
	      done=true;
      }
      
      //printf("\n");
      
      marray* mat = marray_calloc(rank, mat_size);
      
      size_t curr_index[rank];
      for(size_t i=0; i<rank; i++){
          curr_index[i] = 0;
      }
      
      done = false;
      while(!done){
          //printf("in loop\n");
          PyObject *o = $input;
	  //PyObject *o_new;
	  	  	  	  
          for(size_t k=0; k<rank; k++){
	     o = PyList_GetItem(o,curr_index[k]);
          }
	  marray_set(mat, curr_index, PyFloat_AsDouble(o));
	    	  
	  curr_index[0]+=1;
	  
          for(size_t i=0; i<rank; i++){
	      if(curr_index[i] == mat_size[i]){
	      
	          if(i+1 < rank){
	              curr_index[i+1]+=1;
		      curr_index[i]=0;
                  }
		  else{
		      done = true;
		      break;
		  }
              }
	      else
	          break;
	  }
      }
           
      $1 = mat;
    }
}



%feature("director") pyTklibHandler;

%include "carmen_messages.h"

%include "procrustes.h"
%include "kmeans.h"
%include "probability.h"
%include "nearest_neighbor.h"
%include "line.h"
%include "box_window.h"
%include "gsl_python.h"
%include "hurdle_extractor.h"
%include "gaussian.h"
%include "EKF2D.h"
%include "tklib_log_gridmap.h"
%include "gridmapping.h"
%include "noise_models.h"
%include "simulator.h"
%include "carmen_util.h"
%include "spline.h"
%include "carmen_subscribe.h"
%include "carmen_publish.h"
%include "gsl_utilities.h"

/* turn on director wrapping Callback */
#define __attribute__(x)





%include <carmen/ipc_wrapper.h>





