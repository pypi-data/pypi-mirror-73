/*
* SPDX-License-Identifier: Apache-2.0
*
* Copyright 2020 Andrey Pleshakov
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

#ifndef _EPHYRA_UTIL_H
#define _EPHYRA_UTIL_H

#include <stdbool.h>

#include <Python.h>

#include "data.h"

#define FAILURE -1
#define SUCCESS 0

#define init_counted_ref(local_var, storage) \
    { \
        void *tmp = storage; \
        Py_INCREF(local_var); \
        storage = local_var; \
        Py_XDECREF(tmp); \
    }

#define extract_double(local_var, storage, cleanup) \
    storage = PyFloat_AsDouble(local_var); \
    if (PyErr_Occurred()) { \
        cleanup; \
        return FAILURE; \
    }

#define init_optional_double(local_var, storage, flag, cleanup) \
    if (local_var != Py_None && local_var != NULL) { \
        extract_double(local_var, storage, cleanup) \
        flag = true; \
    } else { \
        storage = DEFAULT_DOUBLE; \
        flag = false;\
    }

#define for_rotation_type(rt, store, azimuthal_value, polar_value, cleanup) \
    switch (rt) { \
        case RT_AZIMUTHAL: \
            store = azimuthal_value; \
            break; \
        case RT_POLAR: \
            store = polar_value; \
            break; \
        default: \
            PyErr_Format(PyExc_ValueError, "unknown rotation type %d", rt); \
            cleanup; \
            return FAILURE; \
    }

extern int _ephyra_extract_long_attribute(PyObject *obj, char *attr_name, long *store_at);

extern int _ephyra_deconstruct_fraction(PyObject *obj, _ephyra_aspect_ratio_data *store_at);

extern bool _ephyra_aspect_ratios_equal(_ephyra_aspect_ratio_data *ar1, _ephyra_aspect_ratio_data *ar2);

extern bool _ephyra_parameters_consistent(_EphyraParameters *p1, _EphyraParameters *p2);

#endif //_EPHYRA_UTIL_H
