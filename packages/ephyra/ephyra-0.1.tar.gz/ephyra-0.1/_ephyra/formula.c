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

#include <math.h>

#include "formula.h"
#include "util.h"

static const double _RAD_80 = 80 * Py_MATH_PI / 180;

// TODO: investigate possibility of cython-based implementation of the wrappers <AP>

_ephyra_screen_length_data _ephyra_calculate_screen_width_height(_ephyra_aspect_ratio_data *ar, double diagonal) {
    double unit_length = sqrt(pow(diagonal, 2) / (pow(ar->numerator, 2) + pow(ar->denominator, 2)));
    return (_ephyra_screen_length_data) {unit_length * ar->numerator, unit_length * ar->denominator};
}

PyObject *_ephyra_calculate_screen_width_height_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"aspect_ratio", "diagonal", NULL};
    PyObject *ar;
    double diagonal;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Od", kwds, &ar, &diagonal)) {
        return NULL;
    }
    _ephyra_aspect_ratio_data ar_data;
    if (_ephyra_deconstruct_fraction(ar, &ar_data) < SUCCESS) {
        return NULL;
    }
    _ephyra_screen_length_data res = _ephyra_calculate_screen_width_height(&ar_data, diagonal);
    return Py_BuildValue("dd", res.horizontal, res.vertical);
}

static double _horizontal_fov(double fov_v, _ephyra_aspect_ratio_data *ar) {
    return 2 * atan(tan(fov_v / 2) * ((double) ar->numerator / ar->denominator));
}

static double _vertical_fov(double fov_h, _ephyra_aspect_ratio_data *ar) {
    return 2 * atan(tan(fov_h / 2) * ((double) ar->denominator / ar->numerator));
}

int _ephyra_calculate_fov(double fov, _ephyra_aspect_ratio_data *ar, long fov_type, _ephyra_fov_data *store_at) {
    switch(fov_type) {
        case FT_HORIZONTAL:
            store_at->horizontal = fov;
            store_at->vertical = _vertical_fov(fov, ar);
            break;
        case FT_VERTICAL:
            store_at->vertical = fov;
            store_at->horizontal = _horizontal_fov(fov, ar);
            break;
        default:
            PyErr_Format(PyExc_ValueError, "unknown fov type %d", fov_type);
            return FAILURE;
    }
    return SUCCESS;
}

PyObject *_ephyra_calculate_fov_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"fov", "aspect_ratio", "fov_type", NULL};
    double fov;
    PyObject *ar;
    long fov_type;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dOl", kwds, &fov, &ar, &fov_type)) {
        return NULL;
    }
    _ephyra_aspect_ratio_data ar_data;
    if (_ephyra_deconstruct_fraction(ar, &ar_data) < SUCCESS) {
        return NULL;
    }
    _EphyraFOVData *ret = PyObject_New(_EphyraFOVData,&_EphyraFOVDataType);
    if (!ret) {
        return NULL;
    }
    if (_ephyra_calculate_fov(fov, &ar_data, fov_type, &ret->d) < SUCCESS) {
        Py_DECREF(ret);
        return NULL;
    }
    return (PyObject *) ret;
}

int _ephyra_convert_fov_to_aspect_ratio(_ephyra_fov_data *fov, long fov_scaling, _ephyra_aspect_ratio_data *ar, _ephyra_fov_data *store_at) {
    switch (fov_scaling) {
        case FS_HORIZONTAL_PLUS:
            store_at->vertical = fov->vertical;
            store_at->horizontal = _horizontal_fov(fov->vertical, ar);
            break;
        case FS_VERTICAL_MINUS:
            store_at->horizontal = fov->horizontal;
            store_at->vertical = _vertical_fov(fov->horizontal, ar);
            break;
        default:
            PyErr_Format(PyExc_ValueError, "unknown scaling type %d", fov_scaling);
            return FAILURE;
    }
    return SUCCESS;
}

PyObject *_ephyra_convert_fov_to_aspect_ratio_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"fov", "fov_scaling", "aspect_ratio", NULL};
    _EphyraFOVData *fov_data;
    long fov_scaling;
    PyObject *ar;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!lO", kwds, &_EphyraFOVDataType, &fov_data, &fov_scaling, &ar)) {
        return NULL;
    }
    _ephyra_aspect_ratio_data ar_data;
    if (_ephyra_deconstruct_fraction(ar, &ar_data) < SUCCESS) {
        return NULL;
    }
    _EphyraFOVData *ret = PyObject_New(_EphyraFOVData, &_EphyraFOVDataType);
    if (!ret) {
        return NULL;
    }
    if (_ephyra_convert_fov_to_aspect_ratio(&fov_data->d, fov_scaling, &ar_data, &ret->d) < SUCCESS) {
        Py_DECREF(ret);
        return NULL;
    }
    return (PyObject *) ret;
}

double _ephyra_radians_per_unit_measure(_EphyraState *state, _EphyraParameters *params) {
    double v = state->linear_to_rotary_measure;
    if (params->consider_app_input_data) {
        v *= params->radians_per_count;
    }
    if (params->consider_system_input_data) {
        v *= params->counts_per_unit;
    }
    return v;
}

PyObject *_ephyra_radians_per_unit_measure_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"state", "parameters", NULL};
    _EphyraState *state;
    _EphyraParameters *parameters;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!", kwds, &_EphyraStateType, &state, &_EphyraParametersType, &parameters)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_radians_per_unit_measure(state, parameters));
}

double _ephyra_rotation_ltr_measure(_EphyraState *state, _EphyraParameters *params) {
    return 1 / _ephyra_radians_per_unit_measure(state, params);
}

PyObject *_ephyra_rotation_ltr_measure_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"state", "parameters", NULL};
    _EphyraState *state;
    _EphyraParameters *parameters;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!", kwds, &_EphyraStateType, &state, &_EphyraParametersType, &parameters)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_rotation_ltr_measure(state, parameters));
}

double _ephyra_radians_for_ratio_from_center(double ratio, _EphyraState *state) {
    return atan(ratio * tan(state->fov / 2));
}

PyObject *_ephyra_radians_for_ratio_from_center_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"ratio", "state", NULL};
    double ratio;
    _EphyraState *state;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!", kwds, &ratio, &_EphyraStateType, &state)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_radians_for_ratio_from_center(ratio, state));
}

double _ephyra_screen_ratio_ltr_measure(double ratio, _EphyraState *state, _EphyraParameters *params) {
    return _ephyra_radians_for_ratio_from_center(ratio, state) / _ephyra_radians_per_unit_measure(state, params);
}

PyObject *_ephyra_screen_ratio_ltr_measure_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"ratio", "state", "parameters", NULL};
    double ratio;
    _EphyraState *state;
    _EphyraParameters *parameters;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!O!", kwds, &ratio, &_EphyraStateType, &state, &_EphyraParametersType, &parameters)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_screen_ratio_ltr_measure(ratio, state, parameters));
}

double _ephyra_radians_for_distance_from_center(double distance, _EphyraState *state, _EphyraParameters *params) {
    return atan(2 * distance * tan(state->fov / 2) / params->screen_length);
}

PyObject *_ephyra_radians_for_distance_from_center_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"distance", "state", "parameters", NULL};
    double distance;
    _EphyraState *state;
    _EphyraParameters *parameters;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!O!", kwds, &distance, &_EphyraStateType, &state, &_EphyraParametersType, &parameters)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_radians_for_distance_from_center(distance, state, parameters));
}

double _ephyra_screen_distance_ltr_measure(double distance, _EphyraState *state, _EphyraParameters *params) {
    return _ephyra_radians_for_distance_from_center(distance, state, params) / _ephyra_radians_per_unit_measure(state, params);
}

PyObject *_ephyra_screen_distance_ltr_measure_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"distance", "state", "parameters", NULL};
    double distance;
    _EphyraState *state;
    _EphyraParameters *parameters;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!O!", kwds, &distance, &_EphyraStateType, &state, &_EphyraParametersType, &parameters)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_screen_distance_ltr_measure(distance, state, parameters));
}

int _ephyra_horizontal_4_to_3_fov_coefficient(double b, _ephyra_fov_data *c, _ephyra_fov_data *z, _EphyraParameters *params, double *store_at) {
    if (z != NULL) {
        _ephyra_aspect_ratio_data ar = {4, 3};
        _ephyra_fov_data c_fov;
        if (_ephyra_convert_fov_to_aspect_ratio(c, params->fov_scaling, &ar, &c_fov) < SUCCESS) {
            return FAILURE;
        }
        _ephyra_fov_data z_fov;
        if (_ephyra_convert_fov_to_aspect_ratio(z, params->fov_scaling, &ar, &z_fov) < SUCCESS) {
            return FAILURE;
        }
        *store_at = b * c_fov.horizontal / z_fov.horizontal;
    } else {
        *store_at = b;
    }
    return SUCCESS;
}

PyObject *_ephyra_ltr_formula_wrapper(PyObject *self, PyObject *args, PyObject *kwargs, _ephyra_ltr_coefficient_transformation_formula f) {
    static char *kwds[] = {"b", "c", "z", "p", NULL};
    double b;
    _EphyraFOVData *c;
    PyObject *z;
    _EphyraParameters *p;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!OO!", kwds, &b, &_EphyraFOVDataType, &c, &z, &_EphyraParametersType, &p)) {
        return NULL;
    }
    _ephyra_fov_data *z_fov = NULL;
    if (Py_TYPE(z) == &_EphyraFOVDataType) {
        z_fov = &((_EphyraFOVData *) z)->d;
    } else {
        if (z != Py_None) {
            PyErr_Format(PyExc_TypeError, "expected type %s (got %s)", _EphyraFOVDataType.tp_name, Py_TYPE(z)->tp_name);
            return NULL;
        }
    }
    double res;
    if (f(b, &c->d, z_fov, p, &res) < SUCCESS) {
        return NULL;
    }
    return PyFloat_FromDouble(res);
}

PyObject *_ephyra_horizontal_4_to_3_fov_coefficient_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    return _ephyra_ltr_formula_wrapper(self, args, kwargs, _ephyra_horizontal_4_to_3_fov_coefficient);
}

int _ephyra_horizontal_fov_to_80_coefficient(double b, _ephyra_fov_data *c, _ephyra_fov_data *z, _EphyraParameters *params, double *store_at) {
    *store_at = b * c->horizontal / _RAD_80;
    return SUCCESS;
}

PyObject *_ephyra_horizontal_fov_to_80_coefficient_py(PyObject *self, PyObject *args, PyObject *kwargs) {
    return _ephyra_ltr_formula_wrapper(self, args, kwargs, _ephyra_horizontal_fov_to_80_coefficient);
}