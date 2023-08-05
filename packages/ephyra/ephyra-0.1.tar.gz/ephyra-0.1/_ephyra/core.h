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

#ifndef _EPHYRA_CORE_H
#define _EPHYRA_CORE_H

#include <Python.h>
#include "data.h"

typedef struct {
    PyObject_HEAD
    _ephyra_aspect_ratio_data fov_aspect_ratio;
    long fov_type;
    _EphyraParameters *parameters;
    PyObject *fov_transformation_formula;
    PyObject *ltr_coefficient_transformation_formula;
    long rotation_type;
    _EphyraState *primary_state;
    _EphyraFOVData *primary_fov_data;
} _EphyraDataHelper;

extern PyTypeObject _EphyraDataHelperType;

typedef double (*measure_formula)(double, _EphyraState*, _EphyraParameters*);

typedef struct {
    PyObject_HEAD
    measure_formula mf;
    _EphyraParameters *p2;
    double rm;
    double v2;
} _EphyraAbstractCalculator;

extern PyTypeObject _EphyraAbstractCalculatorType;

extern PyTypeObject _EphyraFullRotationCalculatorType;

extern PyTypeObject _EphyraScreenRatioCalculatorType;

extern PyTypeObject _EphyraScreenDistanceCalculatorType;

typedef struct {
    PyObject_HEAD
    _EphyraState *s;
    _EphyraParameters *p;
    double rpu;
} _EphyraDetailsCalculator;

extern PyTypeObject _EphyraDetailsCalculatorType;

#endif //_EPHYRA_CORE_H