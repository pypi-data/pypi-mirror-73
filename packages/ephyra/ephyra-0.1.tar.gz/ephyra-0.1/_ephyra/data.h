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

#ifndef _EPHYRA_DATA_H
#define _EPHYRA_DATA_H

#include <Python.h>
#include <stdbool.h>
#include <structmember.h>

#define FT_HORIZONTAL 0L
extern PyObject *_EPHYRA_FT_HORIZONTAL;
#define FT_VERTICAL 1L
extern PyObject *_EPHYRA_FT_VERTICAL;

#define FS_HORIZONTAL_PLUS 0L
extern PyObject *_EPHYRA_FS_HORIZONTAL_PLUS;
#define FS_VERTICAL_MINUS 1L
extern PyObject *_EPHYRA_FS_VERTICAL_MINUS;

#define RT_AZIMUTHAL 0L
extern PyObject *_EPHYRA_RT_AZIMUTHAL;
#define RT_POLAR 1L
extern PyObject *_EPHYRA_RT_POLAR;

extern int _Ephyra_data_init();

#define DEFAULT_DOUBLE .0
#define DEFAULT_LONG 0L
#define DEFAULT_BOOL false
#define DEFAULT_ENUM -1L

typedef struct {
    long numerator;
    long denominator;
} _ephyra_aspect_ratio_data;

typedef struct {
    double horizontal;
    double vertical;
} _ephyra_fov_data, _ephyra_screen_length_data;

typedef struct {
    PyObject_HEAD
    _ephyra_aspect_ratio_data screen_aspect_ratio;
    long fov_scaling;
    double radians_per_count;
    double counts_per_unit;
    double screen_length;
    char consider_app_input_data;
    char consider_system_input_data;
    char consider_physical_screen_data;
} _EphyraParameters;

extern PyTypeObject _EphyraParametersType;

typedef struct {
    PyObject_HEAD
    _ephyra_fov_data d;
} _EphyraFOVData;

extern PyTypeObject _EphyraFOVDataType;

typedef struct {
    PyObject_HEAD
    double linear_to_rotary_measure;
    double fov;
} _EphyraState;

extern PyTypeObject _EphyraStateType;

#endif //_EPHYRA_DATA_H
