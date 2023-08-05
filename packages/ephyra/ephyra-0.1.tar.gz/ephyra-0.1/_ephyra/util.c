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

#include "util.h"

int _ephyra_extract_long_attribute(PyObject *obj, char *attr_name, long *store_at) {
    PyObject *val = PyObject_GetAttrString(obj, attr_name);
    if (!val) {
        return FAILURE;
    }
    long l_val = PyLong_AsLong(val);
    if (PyErr_Occurred()) {
        return FAILURE;
    }
    *store_at = l_val;
    return SUCCESS;
}

int _ephyra_deconstruct_fraction(PyObject *obj, _ephyra_aspect_ratio_data *store_at) {
    if (_ephyra_extract_long_attribute(obj, "numerator", &store_at->numerator) < SUCCESS) {
        return FAILURE;
    }
    if (_ephyra_extract_long_attribute(obj, "denominator", &store_at->denominator) < SUCCESS) {
        return FAILURE;
    }
    return SUCCESS;
}

bool _ephyra_aspect_ratios_equal(_ephyra_aspect_ratio_data *ar1, _ephyra_aspect_ratio_data *ar2) {
    return (ar1->numerator == ar2->numerator) && (ar1->denominator == ar2->denominator);
}

bool _ephyra_parameters_consistent(_EphyraParameters *p1, _EphyraParameters *p2) {
    return (p1->consider_app_input_data == p2->consider_app_input_data)
           && (p1->consider_system_input_data == p2->consider_system_input_data)
           && (p1->consider_physical_screen_data == p2->consider_physical_screen_data);
}
