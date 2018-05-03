
#include <Python.h>

#include "foo.h"

static
PyObject* call_foo(PyObject *junk)
{
    return PyLong_FromLong(foo());
}

static struct PyMethodDef dtest_methods[] = {
    {"foo", (PyCFunction)call_foo, METH_NOARGS,
     "foo() -> long\n"
     "call foo"},
    {NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef dtestymodule = {
  PyModuleDef_HEAD_INIT,
    "dtest",
    NULL,
    -1,
    dtest_methods,
};
#endif

#if PY_MAJOR_VERSION >= 3
#  define PyMOD(NAME) PyObject* PyInit_##NAME (void)
#else
#  define PyMOD(NAME) void init##NAME (void)
#endif

PyMOD(dtest)
{
#if PY_MAJOR_VERSION >= 3
        PyObject *mod = PyModule_Create(&dtestymodule));
#else
        PyObject *mod = Py_InitModule("dtest", dtest_methods);
#endif
        if(mod) {
        }
#if PY_MAJOR_VERSION >= 3
    return mod;
#else
    (void)mod;
#endif
}
