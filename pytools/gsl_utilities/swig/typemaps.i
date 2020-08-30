
%typemap(out) gsl_vector * {
  PyObject * obj = psu_vector_to_python($1);
  if($1 != NULL){
    gsl_vector_free($1);
  }
  $result = obj;
}

%typemap(in, numinputs=0) gsl_vector * result(gsl_vector * temp) {
  $1 = gsl_vector_alloc(2);
 }
%typemap(argout) gsl_vector * result {
  PyObject * o = psu_vector_to_python($1);
  $result = o;
 }


%typemap(out) gsl_permutation*{
	PyObject* pyvec = PyList_New(0);

	if($1 == NULL)
	    return pyvec;

	gsl_vector * gsl_vec = tklib_permutation_to_vector($1);

        int i;
	for(i=0; i<gsl_vec->size; i++){
	  PyObject* pt = PyInt_FromLong((long)gsl_vector_get(gsl_vec, i));
	  PyList_Append(pyvec, pt);
	  Py_DECREF(pt);
	}
	
   	
	gsl_vector_free(gsl_vec);
	gsl_permutation_free($1);
	$result = pyvec;
}


%typemap(out) gsl_matrix*{
	PyObject* mat = PyList_New(0);

	if($1 == NULL)
	    return mat;

        int i;
	for(i=0; i<$1->size1; i++){
	  PyObject* row = PyList_New(0);	
	  int j;
	  for(j=0;j<$1->size2;j++){
		  PyObject* pt = PyFloat_FromDouble(gsl_matrix_get($1, i, j));
		  PyList_Append(row, pt);
		  Py_DECREF(pt);
          }
         PyList_Append(mat, row);
	 Py_DECREF(row);
	}

	gsl_matrix_free($1);
	$result = mat;
}


%typemap(out) gsl_matrix_float*{
	PyObject* mat = PyList_New(0);

	if($1 == NULL)
	    return mat;

        int i;
	for(i=0; i<$1->size1; i++){
	  PyObject* row = PyList_New(0);	
	  int j;
	  for(j=0;j<$1->size2;j++){
		  PyObject* pt = PyFloat_FromDouble((double)gsl_matrix_float_get($1, i, j));
		  PyList_Append(row, pt);
		  Py_DECREF(pt);
          }
         PyList_Append(mat, row);
	 Py_DECREF(row);
	}

	gsl_matrix_float_free($1);
	$result = mat;
}


%typemap(in) gsl_vector * {
  int i, my_len;
  if (!PySequence_Check($input)) {
      PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
      return NULL;
  }

  my_len = PyObject_Length($input);

  if(my_len == 0){
    $1=NULL;
  }
  else{
      gsl_vector * vec = gsl_vector_calloc(my_len);

      for (i =0; i < my_len; i++) {
          PyObject *o = PySequence_GetItem($input,i);
          if (!PyFloat_Check(o) && !PyInt_Check(o)) {
             PyErr_SetString(PyExc_ValueError,"Expecting a sequence of doubles");
             return NULL;
          }
          gsl_vector_set(vec, i, PyFloat_AsDouble(o));
	  Py_DECREF(o);
      }
      $1 = vec;
    }
}



%typemap(in) gsl_vector_float* {
  int i, my_len;
  if (!PySequence_Check($input)) {
      PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
      return NULL;
  }

  my_len = PyObject_Length($input);

  if(my_len == 0){
    $1=NULL;
  }
  else{
      gsl_vector_float* vec = gsl_vector_float_calloc(my_len);

      for (i =0; i < my_len; i++) {
          PyObject *o = PySequence_GetItem($input,i);
          if (!PyFloat_Check(o) && !PyInt_Check(o)) {
             PyErr_SetString(PyExc_ValueError,"Expecting a sequence of doubles");
             return NULL;
          }
          gsl_vector_float_set(vec, i, (float)PyFloat_AsDouble(o));
	  Py_DECREF(o);
      }
      $1 = vec;
    }
}

%typemap(freearg) gsl_vector * {

  if($1 != NULL)
      gsl_vector_free($1);
}

%typemap(freearg) gsl_vector_float * {

  if($1 != NULL)
      gsl_vector_float_free($1);
}


%typemap(freearg) gsl_matrix * {
  if($1 != NULL)
      gsl_matrix_free($1);
}

%typemap(freearg) gsl_matrix_float * {
  if($1 != NULL)
      gsl_matrix_float_free($1);
}

%typemap(in) gsl_matrix* {
  $1 = psu_python_to_matrix($input);
}


//// Map a Python sequence into any sized C double array
%typemap(in) double* {
  int i, my_len;
  if (!PySequence_Check($input)) {
      PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
      return NULL;
  }

  my_len = PyObject_Length($input);
  double *temp = (double*)calloc(my_len,sizeof(double));
  for (i =0; i < my_len; i++) {
      PyObject *o = PySequence_GetItem($input,i);
      if (!PyFloat_Check(o) && !PyInt_Check(o)) {
         PyErr_SetString(PyExc_ValueError,"Expecting a sequence of doubles");
         return NULL;
      }
      temp[i] = PyFloat_AsDouble(o);
      Py_DECREF(o);
  }
  $1 = temp;
}


//// Map a Python sequence into any sized C int array
%typemap(in) int* {
  int i, my_len;
  if (!PySequence_Check($input)) {
      PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
      return NULL;
  }

  my_len = PyObject_Length($input);
  int *temp = (int*)calloc(my_len,sizeof(int));
  for (i =0; i < my_len; i++) {
      PyObject *o = PySequence_GetItem($input,i);
      if (!PyFloat_Check(o) && !PyInt_Check(o)) {
         PyErr_SetString(PyExc_ValueError,"Expecting a sequence of doubles");
         return NULL;
      }
      temp[i] = (int)PyFloat_AsDouble(o);
      Py_DECREF(O);
  }
  $1 = temp;
}




//// Map a Python sequence into any sized C double array
%typemap(in) float* {
  int i, my_len;
  if (!PySequence_Check($input)) {
      PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
      return NULL;
  }

  my_len = PyObject_Length($input);
  float *temp = (float*)calloc(my_len,sizeof(float));
  for (i =0; i < my_len; i++) {
      PyObject *o = PySequence_GetItem($input,i);
      if (!PyFloat_Check(o) && !PyInt_Check(o)) {
         PyErr_SetString(PyExc_ValueError,"Expecting a sequence of doubles");
         return NULL;
      }
      temp[i] = (float)PyFloat_AsDouble(o);
      Py_DECREF(o);
  }
  $1 = temp;
}


// This tells SWIG to treat char ** as a special case
%typemap(in) char ** {
  /* Check if is a list */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (char **) malloc((size+1)*sizeof(char *));
    for (i = 0; i < size; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyString_Check(o))
	$1[i] = PyString_AsString(PyList_GetItem($input,i));
      else {
	PyErr_SetString(PyExc_TypeError,"list must contain strings");
	free($1);
	return NULL;
      }
    }
    $1[i] = 0;
  } else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}



