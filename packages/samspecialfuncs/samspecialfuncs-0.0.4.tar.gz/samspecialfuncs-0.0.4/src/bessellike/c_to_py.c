/* -*- mode: c; c-file-style: "python"; c-basic-offset: 4; -*- */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>
#include <numpy/ndarraytypes.h>
#include <numpy/ufuncobject.h>
#include <numpy/npy_3kcompat.h>
#include "nufuncs.h"

static PyMethodDef NuFuncMethods[] = {
    {NULL, NULL, 0, NULL}
};

/* Define the first Nufunc with double values */
static void double_nu_i1(char **args, npy_intp *dimensions,
			    npy_intp *steps, void *data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *r = args[0], *Pi = args[1], *r0 = args[2];
    char *out = args[3];
    npy_intp r_step = steps[0], Pi_step = steps[1], r0_step = steps[2];
    npy_intp out_step = steps[3];

    for (i = 0; i < n; i++) {
	
	*((double *)out) = nu_i1(*(double*)r,*(double*)Pi,
				    *(double*)r0);

	r += r_step;
	Pi += Pi_step;
	r0 += r0_step;
	out += out_step;

    }

}

/* Define the first Nufunc with long double values */
static void long_double_nu_i1(char **args, npy_intp *dimensions,
				 npy_intp *steps, void *data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *r = args[0], *Pi = args[1], *r0 = args[2];
    char *out = args[3];
    npy_intp r_step = steps[0], Pi_step = steps[1], r0_step = steps[2];
    npy_intp out_step = steps[3];

    for (i = 0; i < n; i++) {

	*((long double *)out) = nu_i1(*(long double*)r,
					 *(long double*)Pi,
					 *(long double*)r0);

	r += r_step;
	Pi += Pi_step;
	r0 += r0_step;
	out += out_step;

    }

}


/* pointer to above function */
PyUFuncGenericFunction func1s[2] = {&double_nu_i1,
				    &long_double_nu_i1};

/* input and return dtypes of above function */
static char type1s[8] = {NPY_DOUBLE, NPY_DOUBLE,
			 NPY_DOUBLE, NPY_DOUBLE,
			 NPY_LONGDOUBLE, NPY_LONGDOUBLE,
			 NPY_LONGDOUBLE, NPY_LONGDOUBLE};

/* no extra args for above function */
static void *data1[2] = {NULL,NULL};


/* second NuFunc with double values */
static void double_nu_k1(char **args, npy_intp *dimensions,
			    npy_intp *steps, void *data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *r = args[0], *Pi = args[1], *r0 = args[2];
    char *out = args[3];
    npy_intp r_step = steps[0], Pi_step = steps[1], r0_step = steps[2];
    npy_intp out_step = steps[3];

    for (i = 0; i < n; i++) {

	*((double *)out) = nu_k1(*(double*)r,*(double*)Pi,
				    *(double*)r0);

	r += r_step;
	Pi += Pi_step;
	r0 += r0_step;
	out += out_step;

    }

}

/* Define the second Nufunc with long double values */

static void long_double_nu_k1(char **args, npy_intp *dimensions,
				 npy_intp *steps, void *data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char *r = args[0], *Pi = args[1], *r0 = args[2];
    char *out = args[3];
    npy_intp r_step = steps[0], Pi_step = steps[1], r0_step = steps[2];
    npy_intp out_step = steps[3];

    for (i = 0; i < n; i++) {

	*((long double *)out) = nu_k1(*(long double*)r,
					 *(long double*)Pi,
					 *(long double*)r0);

	r += r_step;
	Pi += Pi_step;
	r0 += r0_step;
	out += out_step;

    }

}

/* pointer to above function */
PyUFuncGenericFunction func2s[2] = {&double_nu_k1,
				    &long_double_nu_k1};

/* input and return dtypes of above function */
static char type2s[8] = {NPY_DOUBLE, NPY_DOUBLE,
			 NPY_DOUBLE, NPY_DOUBLE,
			 NPY_LONGDOUBLE, NPY_LONGDOUBLE,
			 NPY_LONGDOUBLE, NPY_LONGDOUBLE};

/* no extra args for above function */
static void *data2[2] = {NULL,NULL};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "nufuncs",
    NULL,
    -1,
    NuFuncMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_nufuncs(void)
{
    PyObject *m, *i1, *k1, *d;

    m = PyModule_Create(&moduledef);
    if (!m) {
	return NULL;
    }
    import_array();
    import_umath();

    i1 = PyUFunc_FromFuncAndData(func1s, data1, type1s, 2,
				 3, 1, PyUFunc_None,
				 "nu_i1",
				 "computing\n\n\t"
				 "1/{\\epsilon}*int_{r_0}^{r_in} "
				 "i1(\\sqrt{Pi} u) V'(u) du,\n\n where i1 is "
				 "the modified bessel function of the "
				 "first kind.",0);

    k1 = PyUFunc_FromFuncAndData(func2s, data2, type2s, 2,
				 3, 1, PyUFunc_None,
				 "nu_k1",
				 "computing\n\n\t"
				 "1/{\\epsilon}*int_{r_0}^{r_in} "
				 "k1(\\sqrt{Pi} u) V'(u) du,\n\n where k1 is "
				 "the modified bessel function of the "
				 "second kind.",0);

    d = PyModule_GetDict(m);

    PyDict_SetItemString(d, "nu_i1", i1);
    PyDict_SetItemString(d, "nu_k1", k1);
    Py_DECREF(i1);
    Py_DECREF(k1);

    return m;

}
    
