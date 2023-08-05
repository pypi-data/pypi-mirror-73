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

#ifndef _EPHYRA_FORMULA_H
#define _EPHYRA_FORMULA_H

#include <Python.h>

#include "data.h"

typedef int (*_ephyra_ltr_coefficient_transformation_formula)(double, _ephyra_fov_data *, _ephyra_fov_data *, _EphyraParameters *, double *);

extern PyObject *_ephyra_ltr_formula_wrapper(PyObject *self, PyObject *args, PyObject *kwargs, _ephyra_ltr_coefficient_transformation_formula f);

extern _ephyra_screen_length_data _ephyra_calculate_screen_width_height(_ephyra_aspect_ratio_data *ar, double diagonal);

extern PyObject *_ephyra_calculate_screen_width_height_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern int _ephyra_calculate_fov(double fov, _ephyra_aspect_ratio_data *ar, long fov_type, _ephyra_fov_data *store_at);

extern PyObject *_ephyra_calculate_fov_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern int _ephyra_convert_fov_to_aspect_ratio(_ephyra_fov_data *fov, long fov_scaling, _ephyra_aspect_ratio_data *ar, _ephyra_fov_data *store_at);

extern PyObject *_ephyra_convert_fov_to_aspect_ratio_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern double _ephyra_radians_per_unit_measure(_EphyraState *state, _EphyraParameters *params);

extern PyObject *_ephyra_radians_per_unit_measure_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern double _ephyra_rotation_ltr_measure(_EphyraState *state, _EphyraParameters *params);

extern PyObject *_ephyra_rotation_ltr_measure_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern double _ephyra_radians_for_ratio_from_center(double ratio, _EphyraState *state);

extern PyObject *_ephyra_radians_for_ratio_from_center_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern double _ephyra_screen_ratio_ltr_measure(double ratio, _EphyraState *state, _EphyraParameters *params);

extern PyObject *_ephyra_screen_ratio_ltr_measure_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern double _ephyra_radians_for_distance_from_center(double distance, _EphyraState *state, _EphyraParameters *params);

extern PyObject *_ephyra_radians_for_distance_from_center_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern double _ephyra_screen_distance_ltr_measure(double distance, _EphyraState *state, _EphyraParameters *params);

extern PyObject *_ephyra_screen_distance_ltr_measure_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern int _ephyra_horizontal_4_to_3_fov_coefficient(double b, _ephyra_fov_data *c, _ephyra_fov_data *z, _EphyraParameters *params, double *store_at);

extern PyObject *_ephyra_horizontal_4_to_3_fov_coefficient_py(PyObject *self, PyObject *args, PyObject *kwargs);

extern int _ephyra_horizontal_fov_to_80_coefficient(double b, _ephyra_fov_data *c, _ephyra_fov_data *z, _EphyraParameters *params, double *store_at);

extern PyObject *_ephyra_horizontal_fov_to_80_coefficient_py(PyObject *self, PyObject *args, PyObject *kwargs);


#endif //_EPHYRA_FORMULA_H
