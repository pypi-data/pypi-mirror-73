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

from ephyra.formula._python import calculate_screen_width_height, calculate_fov, convert_fov_to_aspect_ratio, \
    radians_per_unit_measure, rotation_ltr_measure, radians_for_ratio_from_center, screen_ratio_ltr_measure, \
    radians_for_distance_from_center, screen_distance_ltr_measure, horizontal_4_to_3_fov_coefficient, \
    horizontal_fov_to_80_coefficient
from .common import ScreenCalculationsTestCaseMixin, FOVManipulationTestCaseMixin, CalculatorFormulaTestCaseMixin, \
    LtRCoefficientTransformationFormulaTestCaseMixin


class PyScreenCalculationsTestCase(ScreenCalculationsTestCaseMixin, TestCase):
    calculate_screen_width_height = staticmethod(calculate_screen_width_height)


class PyFOVManipulationTestCase(FOVManipulationTestCaseMixin, TestCase):
    calculate_fov = staticmethod(calculate_fov)
    convert_fov_to_aspect_ratio = staticmethod(convert_fov_to_aspect_ratio)


class PyCalculatorFormulaTestCase(CalculatorFormulaTestCaseMixin, TestCase):
    radians_per_unit_measure = staticmethod(radians_per_unit_measure)
    rotation_ltr_measure = staticmethod(rotation_ltr_measure)
    radians_for_ratio_from_center = staticmethod(radians_for_ratio_from_center)
    screen_ratio_ltr_measure = staticmethod(screen_ratio_ltr_measure)
    radians_for_distance_from_center = staticmethod(radians_for_distance_from_center)
    screen_distance_ltr_measure = staticmethod(screen_distance_ltr_measure)


class PyLtRCoefficientTransformationFormulaTestCase(LtRCoefficientTransformationFormulaTestCaseMixin, TestCase):
    horizontal_4_to_3_fov_coefficient = staticmethod(horizontal_4_to_3_fov_coefficient)
    horizontal_fov_to_80_coefficient = staticmethod(horizontal_fov_to_80_coefficient)
