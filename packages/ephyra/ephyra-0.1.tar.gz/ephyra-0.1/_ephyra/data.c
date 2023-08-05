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

#include "data.h"
#include "util.h"

// constants

PyObject *_EPHYRA_FT_HORIZONTAL;
PyObject *_EPHYRA_FT_VERTICAL;

PyObject *_EPHYRA_FS_HORIZONTAL_PLUS;
PyObject *_EPHYRA_FS_VERTICAL_MINUS;

PyObject *_EPHYRA_RT_AZIMUTHAL;
PyObject *_EPHYRA_RT_POLAR;

// imports

static PyObject *fractions;
static PyObject* Fraction;

// handle initialization

int _Ephyra_data_init() {
    fractions = PyImport_ImportModule("fractions");
    if (!fractions) {
        return FAILURE;
    }
    Py_INCREF(fractions);
    Fraction = PyObject_GetAttrString(fractions, "Fraction");
    if (!Fraction) {
        Py_DECREF(fractions);
        return FAILURE;
    }
    Py_INCREF(Fraction);
    return SUCCESS;
}

// DTOs

static PyMemberDef _EphyraParameters_members[] = {
        {"fov_scaling", T_LONG, offsetof(_EphyraParameters, fov_scaling), READONLY, NULL},
        {"radians_per_count", T_DOUBLE, offsetof(_EphyraParameters, radians_per_count), READONLY, NULL},
        {"counts_per_unit", T_DOUBLE, offsetof(_EphyraParameters, counts_per_unit), READONLY, NULL},
        {"screen_length", T_DOUBLE, offsetof(_EphyraParameters, screen_length), READONLY, NULL},
        {"consider_app_input_data", T_BOOL, offsetof(_EphyraParameters, consider_app_input_data), READONLY, NULL},
        {"consider_system_input_data", T_BOOL, offsetof(_EphyraParameters, consider_system_input_data), READONLY, NULL},
        {"consider_physical_screen_data", T_BOOL, offsetof(_EphyraParameters, consider_physical_screen_data), READONLY, NULL},
        {NULL}};

static PyObject *_EphyraParameters_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraParameters *self = (_EphyraParameters *) subtype->tp_alloc(subtype, 0);
    if (self) {
        self->screen_aspect_ratio.numerator = DEFAULT_LONG;
        self->screen_aspect_ratio.denominator = DEFAULT_LONG;
        self->fov_scaling = DEFAULT_ENUM;
        self->radians_per_count = DEFAULT_DOUBLE;
        self->counts_per_unit = DEFAULT_DOUBLE;
        self->screen_length = DEFAULT_DOUBLE;
        self->consider_app_input_data = DEFAULT_BOOL;
        self->consider_system_input_data = DEFAULT_BOOL;
        self->consider_physical_screen_data = DEFAULT_BOOL;
    }
    return (PyObject *) self;
}

static int _EphyraParameters_init(_EphyraParameters *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"screen_aspect_ratio", "fov_scaling", "radians_per_count", "counts_per_unit",
                           "screen_length", "consider_app_input_data", "consider_system_input_data",
                           "consider_physical_screen_data", NULL};
    PyObject *screen_ar;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Ol|dddppp", kwds, &screen_ar, &self->fov_scaling,
                                     &self->radians_per_count, &self->counts_per_unit, &self->screen_length,
                                     &self->consider_app_input_data, &self->consider_system_input_data,
                                     &self->consider_physical_screen_data)) {
        return FAILURE;
    }
    if (_ephyra_deconstruct_fraction(screen_ar, &self->screen_aspect_ratio) < SUCCESS) {
        return FAILURE;
    }
    return SUCCESS;
}

static PyObject *_Ephyra_screen_aspect_ratio_getter(_EphyraParameters *self, void *closure) {
    return PyObject_CallFunction(Fraction, "ll", self->screen_aspect_ratio.numerator, self->screen_aspect_ratio.denominator);
}

static PyGetSetDef _EphyraParameters_getset[] = {
        {"screen_aspect_ratio", (getter) &_Ephyra_screen_aspect_ratio_getter, NULL, NULL, NULL},
        {NULL}};

PyTypeObject _EphyraParametersType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_ephyra.Parameters",
        .tp_basicsize = sizeof(_EphyraParameters),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_members = _EphyraParameters_members,
        .tp_getset = _EphyraParameters_getset,
        .tp_init = (initproc) _EphyraParameters_init,
        .tp_new = (newfunc) _EphyraParameters_new
};

static PyMemberDef _EphyraFOVData_members[] = {
        {"fov_horizontal", T_DOUBLE, offsetof(_EphyraFOVData,d.horizontal), READONLY, NULL},
        {"fov_vertical", T_DOUBLE, offsetof(_EphyraFOVData,d.vertical), READONLY, NULL},
        {NULL}};

static PyObject *_EphyraFOVData_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraFOVData *self = (_EphyraFOVData *) subtype->tp_alloc(subtype, 0);
    if (self) {
        self->d.horizontal = DEFAULT_DOUBLE;
        self->d.vertical = DEFAULT_DOUBLE;
    }
    return (PyObject *) self;
}

static int _EphyraFOVData_init(_EphyraFOVData *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"fov_horizontal", "fov_vertical", NULL};
    if (PyArg_ParseTupleAndKeywords(args, kwargs, "dd", kwds, &self->d.horizontal, &self->d.vertical) < SUCCESS) {
        return FAILURE;
    }
    return SUCCESS;
}

PyTypeObject _EphyraFOVDataType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_ephyra.FOVData",
        .tp_basicsize = sizeof(_EphyraFOVData),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_members = _EphyraFOVData_members,
        .tp_init = (initproc) _EphyraFOVData_init,
        .tp_new = _EphyraFOVData_new
};

static PyMemberDef _EphyraState_members[] = {
        {"linear_to_rotary_measure", T_DOUBLE, offsetof(_EphyraState, linear_to_rotary_measure), READONLY, NULL},
        {"fov", T_DOUBLE, offsetof(_EphyraState, fov), READONLY, NULL},
        {NULL}};

static PyObject *_EphyraState_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraState *self = (_EphyraState *) subtype->tp_alloc(subtype, 0);
    if (self) {
        self->linear_to_rotary_measure = DEFAULT_DOUBLE;
        self->fov = DEFAULT_DOUBLE;
    }
    return (PyObject *) self;
}

static int _EphyraState_init(_EphyraState *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"linear_to_rotary_measure", "fov", NULL};
    if (PyArg_ParseTupleAndKeywords(args, kwargs, "dd", kwds, &self->linear_to_rotary_measure, &self->fov) < SUCCESS) {
        return FAILURE;
    }
    return SUCCESS;
}

PyTypeObject _EphyraStateType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_ephyra.State",
        .tp_basicsize = sizeof(_EphyraState),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_members = _EphyraState_members,
        .tp_init = (initproc) _EphyraState_init,
        .tp_new = _EphyraState_new
};
