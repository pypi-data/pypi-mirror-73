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

#include "core.h"
#include "formula.h"
#include "util.h"

static PyObject *_EphyraDataHelper_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraDataHelper *self = (_EphyraDataHelper *) subtype->tp_alloc(subtype, 0);
    if (self) {
        self->fov_aspect_ratio.numerator = DEFAULT_LONG;
        self->fov_aspect_ratio.denominator = DEFAULT_LONG;
        self->fov_type = DEFAULT_ENUM;
        self->parameters = NULL;
        self->fov_transformation_formula = NULL;
        self->ltr_coefficient_transformation_formula = NULL;
        self->rotation_type = DEFAULT_ENUM;
        self->primary_state = NULL;
        self->primary_fov_data = NULL;
    }
    return (PyObject *) self;
}

static int _ephyra_create_state_and_fov_data(PyObject *fov_transformation_formula, double fov, PyObject *primary_fov_data,
        _EphyraParameters *parameters, _ephyra_aspect_ratio_data *fov_aspect_ratio, long fov_type, long rotation_type,
        PyObject *ltr_coefficient_transformation_formula, double ltr_coefficient,
        _EphyraState **state_out, _EphyraFOVData **fov_data_out) {
    double transformed_fov;
    if (fov_transformation_formula != NULL) {
        PyObject *res = PyObject_CallFunction(fov_transformation_formula, "dOO", fov, primary_fov_data, parameters);
        if (!res) {
            return FAILURE;
        }
        transformed_fov = PyFloat_AsDouble(res);
        if (PyErr_Occurred()) {
            return FAILURE;
        }
    } else {
        transformed_fov = fov;
    }
    // primary fov data
    _EphyraFOVData *fov_data = PyObject_New(_EphyraFOVData, &_EphyraFOVDataType);
    if (!fov_data) {
        return FAILURE;
    }
    if (_ephyra_calculate_fov(transformed_fov, fov_aspect_ratio, fov_type, &fov_data->d) < SUCCESS) {
        Py_DECREF(fov_data);
        return FAILURE;
    }
    if (!_ephyra_aspect_ratios_equal(fov_aspect_ratio, &parameters->screen_aspect_ratio)) {
        _ephyra_fov_data source = fov_data->d;
        if (_ephyra_convert_fov_to_aspect_ratio(&source, parameters->fov_scaling, &parameters->screen_aspect_ratio, &fov_data->d) < SUCCESS) {
            Py_DECREF(fov_data);
            return FAILURE;
        }
    }
    // primary state: fov
    _EphyraState *state = PyObject_New(_EphyraState, &_EphyraStateType);
    if (!state) {
        Py_DECREF(fov_data);
        return FAILURE;
    }
    for_rotation_type(rotation_type, state->fov, fov_data->d.horizontal,
                      fov_data->d.vertical, Py_DECREF(fov_data); Py_DECREF(state))
    // primary state: ltr_coefficient
    if (ltr_coefficient_transformation_formula != NULL) {
        PyObject *res = PyObject_CallFunction(ltr_coefficient_transformation_formula, "dOOO", ltr_coefficient, fov_data, primary_fov_data, parameters);
        if (!res) {
            return FAILURE;
        }
        state->linear_to_rotary_measure = PyFloat_AsDouble(res);
        if (PyErr_Occurred()) {
            Py_DECREF(fov_data);
            Py_DECREF(state);
            return FAILURE;
        }
    } else {
        state->linear_to_rotary_measure = ltr_coefficient;
    }
    *fov_data_out = fov_data;
    *state_out = state;
    return SUCCESS;
}

static int _EphyraDataHelper_init(_EphyraDataHelper *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"screen_aspect_ratio", "fov", "fov_aspect_ratio", "fov_type", "fov_scaling", "rt",
                           "ltr_coefficient", "fov_transformation_formula", "ltr_coefficient_transformation_formula",
                           "radians_per_count", "counts_per_unit", "screen_diagonal", NULL};
    static char *kwt = "OdOlll|$dOOOOO";
    PyObject *screen_aspect_ratio, *fov_aspect_ratio;
    PyObject *fov_transformation_formula = NULL, *ltr_coefficient_transformation_formula = NULL;
    PyObject *radians_per_count = NULL, *counts_per_unit = NULL, *screen_diagonal = NULL;
    double fov, ltr_coefficient = 1;
    _EphyraParameters *parameters = PyObject_New(_EphyraParameters, &_EphyraParametersType);
    if (!parameters) {
        return FAILURE;
    }
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, kwt, kwds, &screen_aspect_ratio, &fov, &fov_aspect_ratio,
            &self->fov_type, &parameters->fov_scaling, &self->rotation_type, &ltr_coefficient, &fov_transformation_formula,
            &ltr_coefficient_transformation_formula, &radians_per_count, &counts_per_unit, &screen_diagonal)) {
        Py_DECREF(parameters);
        return FAILURE;
    }
    // DataHelper field values requiring special treatment
    if (fov_transformation_formula) {
        init_counted_ref(fov_transformation_formula, self->fov_transformation_formula)
    }
    if (ltr_coefficient_transformation_formula) {
        init_counted_ref(ltr_coefficient_transformation_formula, self->ltr_coefficient_transformation_formula)
    }
    if (_ephyra_deconstruct_fraction(fov_aspect_ratio, &self->fov_aspect_ratio) < SUCCESS) {
        Py_DECREF(parameters);
        return FAILURE;
    }
    // remaining Parameters field values
    if (_ephyra_deconstruct_fraction(screen_aspect_ratio, &parameters->screen_aspect_ratio) < SUCCESS) {
        Py_DECREF(parameters);
        return FAILURE;
    }
    init_optional_double(radians_per_count, parameters->radians_per_count,
                         parameters->consider_app_input_data, Py_DECREF(parameters))
    init_optional_double(counts_per_unit, parameters->counts_per_unit,
                         parameters->consider_system_input_data, Py_DECREF(parameters))
    if (screen_diagonal != Py_None && screen_diagonal != NULL) {
        double d;
        extract_double(screen_diagonal, d, Py_DECREF(parameters))
        _ephyra_screen_length_data len_d = _ephyra_calculate_screen_width_height(&parameters->screen_aspect_ratio, d);
        for_rotation_type(self->rotation_type, parameters->screen_length,
                len_d.horizontal, len_d.vertical, Py_DECREF(parameters))
        parameters->consider_physical_screen_data = true;
    } else {
        parameters->screen_length = DEFAULT_DOUBLE;
        parameters->consider_physical_screen_data = false;
    }
    _EphyraFOVData *fov_data = NULL;
    _EphyraState *state = NULL;
    if (_ephyra_create_state_and_fov_data(fov_transformation_formula, fov, Py_None, parameters, &self->fov_aspect_ratio,
            self->fov_type, self->rotation_type, ltr_coefficient_transformation_formula, ltr_coefficient, &state,
            &fov_data) < SUCCESS) {
        Py_DECREF(parameters);
        return FAILURE;
    }
    self->parameters = parameters;
    self->primary_state = state;
    self->primary_fov_data = fov_data;
    return SUCCESS;
}

static int _EphyraDataHelper_traverse(_EphyraDataHelper *self, visitproc visit, void *arg) {
    Py_VISIT(self->fov_transformation_formula);
    Py_VISIT(self->ltr_coefficient_transformation_formula);
    return SUCCESS;
}

static void _EphyraDataHelper_dealloc(_EphyraDataHelper *self) {
    PyObject_GC_UnTrack(self);
    Py_XDECREF(self->parameters);
    Py_XDECREF(self->fov_transformation_formula);
    Py_XDECREF(self->ltr_coefficient_transformation_formula);
    Py_XDECREF(self->primary_state);
    Py_XDECREF(self->primary_fov_data);
    Py_TYPE(self)->tp_free(self);
}

PyMemberDef _EphyraDataHelper_members[] = {
        {"parameters", T_OBJECT_EX, offsetof(_EphyraDataHelper, parameters), READONLY, NULL},
        {"primary_state", T_OBJECT_EX, offsetof(_EphyraDataHelper, primary_state), READONLY, NULL},
        {NULL}};

PyObject *_EphyraDataHelper_get_state_for_fov(_EphyraDataHelper *self, PyObject * args, PyObject *kwargs) {
    static char *kwds[] = {"fov", "fov_aspect_ratio", "fov_type", "ltr_coefficient", NULL};
    double fov, ltr_coefficient = 1;
    PyObject *fov_type = NULL, *fov_aspect_ratio = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "d|OOd", kwds, &fov, &fov_aspect_ratio, &fov_type, &ltr_coefficient)) {
        return NULL;
    }
    _ephyra_aspect_ratio_data ar_data;
    if (fov_aspect_ratio != NULL && fov_aspect_ratio != Py_None) {
        if (_ephyra_deconstruct_fraction(fov_aspect_ratio, &ar_data) < SUCCESS) {
            return NULL;
        }
    } else {
        ar_data = self->fov_aspect_ratio;
    }
    long ft_data;
    if (fov_type != NULL && fov_type != Py_None) {
        ft_data = PyLong_AsLong(fov_type);
        if (PyErr_Occurred()) {
            return NULL;
        }
    } else {
        ft_data = self->fov_type;
    }
    _EphyraFOVData *fov_data;
    _EphyraState *state;
    _ephyra_create_state_and_fov_data(self->fov_transformation_formula, fov, (PyObject *) self->primary_fov_data,
            self->parameters, &ar_data, ft_data, self->rotation_type, self->ltr_coefficient_transformation_formula,
            ltr_coefficient, &state, &fov_data);
    Py_DECREF(fov_data);
    return (PyObject *) state;
}

PyMethodDef _EphyraDataHelper_methods[] = {
        {"get_state_for_fov", (PyCFunction) _EphyraDataHelper_get_state_for_fov, METH_VARARGS | METH_KEYWORDS},
        {NULL}
};

PyTypeObject _EphyraDataHelperType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_ephyra.DataHelper",
        .tp_basicsize = sizeof(_EphyraDataHelper),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
        .tp_new = _EphyraDataHelper_new,
        .tp_traverse = (traverseproc) _EphyraDataHelper_traverse,
        .tp_dealloc = (destructor) _EphyraDataHelper_dealloc,
        .tp_init = (initproc) _EphyraDataHelper_init,
        .tp_members = _EphyraDataHelper_members,
        .tp_methods = _EphyraDataHelper_methods
};

static void _EphyraAbstractCalculator_dealloc(_EphyraAbstractCalculator *self) {
    Py_XDECREF(self->p2);
    Py_TYPE(self)->tp_free(self);
}

static PyObject *_EphyraAbstractCalculator_coefficient_for(_EphyraAbstractCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"s2", NULL};
    _EphyraState *state = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", kwds, &_EphyraStateType, &state)) {
        return NULL;
    }
    return PyFloat_FromDouble(self->mf(self->v2, state, self->p2) / self->rm);
}

static PyObject *_EphyraAbstractCalculator_sensitivity_for(_EphyraAbstractCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"s1_sens", "s2", NULL};
    _EphyraState *state = NULL;
    double s1_sens;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!", kwds, &s1_sens, &_EphyraStateType, &state)) {
        return NULL;
    }
    double c = self->mf(self->v2, state, self->p2) / self->rm;
    return Py_BuildValue("dd", c, c * s1_sens);
}

PyMethodDef _EphyraAbstractCalculator_methods[] = {
        {"coefficient_for", (PyCFunction) _EphyraAbstractCalculator_coefficient_for, METH_VARARGS | METH_KEYWORDS},
        {"sensitivity_for", (PyCFunction) _EphyraAbstractCalculator_sensitivity_for, METH_VARARGS | METH_KEYWORDS},
        {NULL}};

PyTypeObject _EphyraAbstractCalculatorType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_ephyra._AbstractCalculator",
    .tp_basicsize = sizeof(_EphyraAbstractCalculator),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = NULL,
    .tp_dealloc = (destructor) _EphyraAbstractCalculator_dealloc,
    .tp_methods = _EphyraAbstractCalculator_methods
};

static _EphyraAbstractCalculator *_ephyra_abstract_calculator_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraAbstractCalculator *self = (_EphyraAbstractCalculator *) subtype->tp_alloc(subtype, 0);
    if (self) {
        self->p2 = NULL;
        self->rm = DEFAULT_DOUBLE;
        self->v2 = DEFAULT_DOUBLE;
    }
    return self;
}

static double _ephyra_full_rotation_measure_formula(double val, _EphyraState *state, _EphyraParameters *parameters) {
    return _ephyra_rotation_ltr_measure(state, parameters);
}

static PyObject *_EphyraFullRotationCalculator_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraAbstractCalculator *self = _ephyra_abstract_calculator_new(subtype, args, kwargs);
    if (self) {
        self->mf = _ephyra_full_rotation_measure_formula;
    }
    return (PyObject *) self;
}

#define init_p2(p1, p2, self) \
    if (p2 == NULL) { \
        p2 = p1; \
    } else { \
        if (!_ephyra_parameters_consistent(p1, p2)) { \
            PyErr_SetString(PyExc_ValueError, "p1 and p2 are inconsistent"); \
            return FAILURE; \
        } \
    } \
    init_counted_ref(p2, self->p2)

#define init_mf(val, state, parameters, self) \
    self->rm = self->mf(val, state, parameters);

static int _EphyraFullRotationCalculator_init(_EphyraAbstractCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"s1", "p1", "p2", NULL};
    _EphyraState *state = NULL;
    _EphyraParameters *p1 = NULL, *p2 = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!|O!", kwds, &_EphyraStateType, &state, &_EphyraParametersType, &p1, &_EphyraParametersType, &p2)) {
        return FAILURE;
    }
    init_p2(p1, p2, self)
    init_mf(DEFAULT_DOUBLE, state, p1, self)
    return SUCCESS;
}

PyTypeObject _EphyraFullRotationCalculatorType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_ephyra.FullRotationCalculator",
        .tp_base = &_EphyraAbstractCalculatorType,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_new = _EphyraFullRotationCalculator_new,
        .tp_init = (initproc) _EphyraFullRotationCalculator_init,
};

static double _ephyra_screen_ratio_measure_formula(double val, _EphyraState *state, _EphyraParameters *parameters) {
    return _ephyra_screen_ratio_ltr_measure(val, state, parameters);
}

static PyObject *_EphyraScreenRatioCalculator_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraAbstractCalculator *self = _ephyra_abstract_calculator_new(subtype, args, kwargs);
    if (self) {
        self->mf = _ephyra_screen_ratio_measure_formula;
    }
    return (PyObject *) self;
}

#define init_v2(v1, v2_object, self) \
    if (v2_object) { \
        extract_double(v2_object, self->v2,) \
    } else {\
        self->v2 = v1; \
    } \

static int _EphyraScreenRatioCalculator_init(_EphyraAbstractCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"ratio1", "s1", "p1", "p2", "ratio2", NULL};
    _EphyraState *state = NULL;
    _EphyraParameters *p1 = NULL, *p2 = NULL;
    double ratio1;
    PyObject *ratio2 = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!O!|O!O", kwds, &ratio1, &_EphyraStateType, &state, &_EphyraParametersType, &p1, &_EphyraParametersType, &p2, &ratio2)) {
        return FAILURE;
    }
    init_p2(p1, p2, self)
    init_v2(ratio1, ratio2, self)
    init_mf(ratio1, state, p1, self)
    return SUCCESS;
}

PyTypeObject _EphyraScreenRatioCalculatorType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_ephyra.ScreenRatioCalculator",
        .tp_base = &_EphyraAbstractCalculatorType,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_new = _EphyraScreenRatioCalculator_new,
        .tp_init = (initproc) _EphyraScreenRatioCalculator_init,
};

static double _ephyra_screen_distance_measure_formula(double val, _EphyraState *state, _EphyraParameters *parameters) {
    return _ephyra_screen_distance_ltr_measure(val, state, parameters);
}

static PyObject *_EphyraScreenDistanceCalculator_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraAbstractCalculator *self = _ephyra_abstract_calculator_new(subtype, args, kwargs);
    if (self) {
        self->mf = _ephyra_screen_distance_measure_formula;
    }
    return (PyObject *) self;
}

static int _EphyraScreenDistanceCalculator_init(_EphyraAbstractCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"distance1", "s1", "p1", "p2", "distance2", NULL};
    _EphyraState *state = NULL;
    _EphyraParameters *p1 = NULL, *p2 = NULL;
    double distance1;
    PyObject *distance2 = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dO!O!|O!O", kwds, &distance1, &_EphyraStateType, &state, &_EphyraParametersType, &p1, &_EphyraParametersType, &p2, &distance2)) {
        return FAILURE;
    }
    if (!p1->consider_physical_screen_data) {
        PyErr_SetString(PyExc_ValueError, "p1 lacks physical screen data");
        return FAILURE;
    }
    init_p2(p1, p2, self)
    init_v2(distance1, distance2, self)
    init_mf(distance1, state, p1, self)
    return SUCCESS;
}

PyTypeObject _EphyraScreenDistanceCalculatorType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_ephyra.ScreenDistanceCalculator",
        .tp_base = &_EphyraAbstractCalculatorType,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_new = _EphyraScreenDistanceCalculator_new,
        .tp_init = (initproc) _EphyraScreenDistanceCalculator_init,
};

static PyObject *_EphyraDetailsCalculator_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    _EphyraDetailsCalculator *self = (_EphyraDetailsCalculator *) subtype->tp_alloc(subtype, 0);
    if (self) {
        self->s = NULL;
        self->p = NULL;
        self->rpu = DEFAULT_DOUBLE;
    }
    return (PyObject *) self;
}

static int _EphyraDetailsCalculator_init(_EphyraDetailsCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"s", "p", NULL};
    _EphyraState *state = NULL;
    _EphyraParameters *parameters = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!", kwds, &_EphyraStateType, &state, &_EphyraParametersType, &parameters)) {
        return FAILURE;
    }
    if (!(parameters->consider_app_input_data && parameters->consider_system_input_data && parameters->consider_physical_screen_data)) {
        PyErr_SetString(PyExc_ValueError, "p lacks data");
        return FAILURE;
    }
    init_counted_ref(state,self->s)
    init_counted_ref(parameters, self->p)
    self->rpu = _ephyra_radians_per_unit_measure(self->s, self->p);
    return SUCCESS;
}

static void _EphyraDetailsCalculator_dealloc(_EphyraDetailsCalculator *self) {
    Py_XDECREF(self->s);
    Py_XDECREF(self->p);
    Py_TYPE(self)->tp_free(self);
}

static PyObject *_EphyraDetailsCalculator_full_rotation_units(_EphyraDetailsCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"sens", NULL};
    double sens;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "d", kwds, &sens)) {
        return NULL;
    }
    return PyFloat_FromDouble(2 * Py_MATH_PI / (self->rpu * sens));
}

static PyObject *_EphyraDetailsCalculator_screen_ratio_units(_EphyraDetailsCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"ratio", "sens", NULL};
    double ratio, sens;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", kwds, &ratio, &sens)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_radians_for_ratio_from_center(ratio, self->s) / (self->rpu * sens));
}

static PyObject *_EphyraDetailsCalculator_screen_distance_units(_EphyraDetailsCalculator *self, PyObject *args, PyObject *kwargs) {
    static char *kwds[] = {"distance", "sens", NULL};
    double distance, sens;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", kwds, &distance, &sens)) {
        return NULL;
    }
    return PyFloat_FromDouble(_ephyra_radians_for_distance_from_center(distance, self->s, self->p) / (self->rpu * sens));
}

PyMethodDef _EphyraDetailsCalculator_methods[] = {
        {"full_rotation_units", (PyCFunction) _EphyraDetailsCalculator_full_rotation_units, METH_KEYWORDS | METH_VARARGS},
        {"screen_ratio_units", (PyCFunction) _EphyraDetailsCalculator_screen_ratio_units, METH_KEYWORDS | METH_VARARGS},
        {"screen_distance_units", (PyCFunction) _EphyraDetailsCalculator_screen_distance_units, METH_KEYWORDS | METH_VARARGS},
        {NULL}};

PyTypeObject _EphyraDetailsCalculatorType = {
        .tp_name = "_ephyra.DetailsCalculator",
        .tp_basicsize = sizeof(_EphyraDetailsCalculator),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_new = _EphyraDetailsCalculator_new,
        .tp_init = (initproc) _EphyraDetailsCalculator_init,
        .tp_dealloc = (destructor) _EphyraDetailsCalculator_dealloc,
        .tp_methods = _EphyraDetailsCalculator_methods
};