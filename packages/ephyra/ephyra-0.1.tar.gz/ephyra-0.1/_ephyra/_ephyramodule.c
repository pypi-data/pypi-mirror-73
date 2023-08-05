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

#include <Python.h>

#include "data.h"
#include "formula.h"
#include "core.h"
#include "util.h"

#define init_const(var, holder, char_name, module) \
    holder = PyLong_FromLong(var); \
    if (!holder) { \
        Py_DECREF(module); \
        return NULL; \
    } \
    Py_INCREF(holder); \
    if (PyModule_AddObject(module, char_name, holder) < SUCCESS) { \
        Py_DECREF(module); \
        Py_DECREF(holder); \
        return NULL; \
    }

#define init_type(type, attr_name, module) \
    if (PyType_Ready(&type) < SUCCESS) { \
        Py_DECREF(module); \
        return NULL; \
    } \
    Py_INCREF(&type); \
    if (PyModule_AddObject(module, attr_name, (PyObject *) &type) < SUCCESS) { \
        Py_DECREF(module); \
        Py_DECREF(&type); \
        return NULL; \
    }

PyMethodDef _ephyra_methods[] = {
            {"calculate_screen_width_height", (PyCFunction) _ephyra_calculate_screen_width_height_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"calculate_fov", (PyCFunction) _ephyra_calculate_fov_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"convert_fov_to_aspect_ratio", (PyCFunction) _ephyra_convert_fov_to_aspect_ratio_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"radians_per_unit_measure", (PyCFunction) _ephyra_radians_per_unit_measure_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"rotation_ltr_measure", (PyCFunction) _ephyra_rotation_ltr_measure_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"radians_for_ratio_from_center", (PyCFunction) _ephyra_radians_for_ratio_from_center_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"screen_ratio_ltr_measure", (PyCFunction) _ephyra_screen_ratio_ltr_measure_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"radians_for_distance_from_center", (PyCFunction) _ephyra_radians_for_distance_from_center_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"screen_distance_ltr_measure", (PyCFunction) _ephyra_screen_distance_ltr_measure_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"horizontal_4_to_3_fov_coefficient", (PyCFunction) _ephyra_horizontal_4_to_3_fov_coefficient_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {"horizontal_fov_to_80_coefficient", (PyCFunction) _ephyra_horizontal_fov_to_80_coefficient_py,  METH_VARARGS | METH_KEYWORDS, NULL},
            {NULL}};

static struct PyModuleDef _ephyramodule = {
        PyModuleDef_HEAD_INIT,
        .m_name = "_ephyra",
        .m_size = -1,
        .m_methods = _ephyra_methods
};

PyMODINIT_FUNC PyInit__ephyra(void) {
    PyObject *module = PyModule_Create(&_ephyramodule);
    if (module == NULL) {
        return NULL;
    }
    if (_Ephyra_data_init() < SUCCESS) {
        Py_DECREF(module);
        return NULL;
    }
    // constant objects
    init_const(FT_HORIZONTAL, _EPHYRA_FT_HORIZONTAL, "FT_HORIZONTAL", module)
    init_const(FT_VERTICAL, _EPHYRA_FT_VERTICAL, "FT_VERTICAL", module)
    init_const(FS_HORIZONTAL_PLUS, _EPHYRA_FS_HORIZONTAL_PLUS, "FS_HORIZONTAL_PLUS", module)
    init_const(FS_VERTICAL_MINUS, _EPHYRA_FS_VERTICAL_MINUS, "FS_VERTICAL_MINUS", module)
    init_const(RT_AZIMUTHAL, _EPHYRA_RT_AZIMUTHAL, "RT_AZIMUTHAL", module)
    init_const(RT_POLAR, _EPHYRA_RT_POLAR, "RT_POLAR", module)
    // DTOs
    init_type(_EphyraParametersType,"Parameters", module)
    init_type(_EphyraFOVDataType,"FOVData", module)
    init_type(_EphyraStateType,"State", module)
    // core types
    init_type(_EphyraDataHelperType, "DataHelper", module)
    init_type(_EphyraAbstractCalculatorType, "_AbstractCalculator", module)
    init_type(_EphyraFullRotationCalculatorType, "FullRotationCalculator", module)
    init_type(_EphyraScreenRatioCalculatorType, "ScreenRatioCalculator", module)
    init_type(_EphyraScreenDistanceCalculatorType, "ScreenDistanceCalculator", module)
    init_type(_EphyraDetailsCalculatorType, "DetailsCalculator", module)
    return module;
}