#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2020 Andrey Pleshakov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from unittest import TestCase

from ephyra.data._native import FS_HORIZONTAL_PLUS, FS_VERTICAL_MINUS, FT_VERTICAL, FT_HORIZONTAL, RT_AZIMUTHAL, \
    RT_POLAR, Parameters, FOVData, State
from .common import ConstantTestCaseMixin, ParametersTestCaseMixin, FOVDataTestCaseMixin, StateTestCaseMixin


class NConstantsTestCase(ConstantTestCaseMixin, TestCase):
    FS_HORIZONTAL_PLUS = FS_HORIZONTAL_PLUS
    FS_VERTICAL_MINUS = FS_VERTICAL_MINUS
    FT_HORIZONTAL = FT_HORIZONTAL
    FT_VERTICAL = FT_VERTICAL
    RT_AZIMUTHAL = RT_AZIMUTHAL
    RT_POLAR = RT_POLAR


class NParametersTestCase(ParametersTestCaseMixin, TestCase):
    FS_HORIZONTAL_PLUS = FS_HORIZONTAL_PLUS
    FS_VERTICAL_MINUS = FS_VERTICAL_MINUS
    Parameters = Parameters


class NFOVDataTestCase(FOVDataTestCaseMixin, TestCase):
    FOVData = FOVData


class NStateTestCase(StateTestCaseMixin, TestCase):
    State = State
