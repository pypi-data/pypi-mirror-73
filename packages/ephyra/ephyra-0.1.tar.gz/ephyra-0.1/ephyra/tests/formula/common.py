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

from fractions import Fraction
from math import radians, degrees

from ephyra.data import FT_HORIZONTAL, FT_VERTICAL, FS_VERTICAL_MINUS, FS_HORIZONTAL_PLUS, FOVData, State, Parameters
from ..helper import dh_app1, dh_sys_app1


class ScreenCalculationsTestCaseMixin:
    calculate_screen_width_height = None

    def test_screen_width_height_calculations(self):
        w, h = self.calculate_screen_width_height(Fraction(16, 10), 24)
        self.assertAlmostEqual(w, 20.35195929612211, 5)
        self.assertAlmostEqual(h, 12.71997456007632, 5)


class FOVManipulationTestCaseMixin:
    calculate_fov = None
    convert_fov_to_aspect_ratio = None

    def test_fov_calculation(self):
        fov = self.calculate_fov(radians(100), Fraction(16, 10), FT_HORIZONTAL)
        self.assertAlmostEqual(degrees(fov.fov_horizontal), 100, 2)
        self.assertAlmostEqual(degrees(fov.fov_vertical), 73.36, 2)

    def test_fov_calculation2(self):
        fov = self.calculate_fov(radians(74), Fraction(4, 3), FT_VERTICAL)
        self.assertAlmostEqual(degrees(fov.fov_horizontal), 90.27, 2)
        self.assertAlmostEqual(degrees(fov.fov_vertical), 74, 2)

    def test_fov_calculation3(self):
        with self.assertRaises(ValueError):
            self.calculate_fov(1, Fraction(2, 3), -1)

    def test_fov_aspect_ratio_conversion(self):
        fov_p = self.calculate_fov(radians(70), Fraction(4, 3), FT_HORIZONTAL)
        fov_desired = self.calculate_fov(radians(80), Fraction(16, 10), FT_HORIZONTAL)
        fov_converted = self.convert_fov_to_aspect_ratio(fov_p, FS_HORIZONTAL_PLUS, Fraction(16, 10))
        self.assertAlmostEqual(fov_converted.fov_horizontal, fov_desired.fov_horizontal, 2)
        self.assertAlmostEqual(fov_converted.fov_vertical, fov_desired.fov_vertical, 2)

    def test_fov_aspect_ratio_conversion2(self):
        fov_p = self.calculate_fov(radians(70), Fraction(4, 3), FT_HORIZONTAL)
        fov_desired = self.calculate_fov(radians(70), Fraction(16, 10), FT_HORIZONTAL)
        fov_converted = self.convert_fov_to_aspect_ratio(fov_p, FS_VERTICAL_MINUS, Fraction(16, 10))
        self.assertAlmostEqual(fov_converted.fov_horizontal, fov_desired.fov_horizontal, 2)
        self.assertAlmostEqual(fov_converted.fov_vertical, fov_desired.fov_vertical, 2)

    def test_fov_aspect_ratio_conversion3(self):
        with self.assertRaises(ValueError):
            self.convert_fov_to_aspect_ratio(FOVData(1.2, 3.4), -1, Fraction(3, 4))


class CalculatorFormulaTestCaseMixin:
    radians_per_unit_measure = None
    rotation_ltr_measure = None
    radians_for_ratio_from_center = None
    radians_for_distance_from_center = None
    screen_ratio_ltr_measure = None
    screen_distance_ltr_measure = None

    def test_radians_per_unit_measure(self):
        p = Parameters(Fraction(1, 2), FS_HORIZONTAL_PLUS, 0.5, 4, consider_app_input_data=True,
                       consider_system_input_data=True)
        s = State(3, 1)
        self.assertAlmostEqual(self.radians_per_unit_measure(s, p), 6, 5)

    def test_rotation_ltr_measure(self):
        p = Parameters(Fraction(1, 2), FS_HORIZONTAL_PLUS, 0.5, 4, consider_app_input_data=True,
                       consider_system_input_data=True)
        s = State(3, 1)
        self.assertAlmostEqual(self.rotation_ltr_measure(s, p), 1 / 6, 5)

    def test_radians_for_ratio_from_center(self):
        self.assertAlmostEqual(self.radians_for_ratio_from_center(.3755782578608322, dh_app1.primary_state),
                               .4234308319224209, 5)

    def test_radians_for_distance_from_center(self):
        self.assertAlmostEqual(self.radians_for_distance_from_center(3.93700787, dh_sys_app1.primary_state,
                                                                     dh_sys_app1.parameters), .43465788352661283, 5)

    def test_screen_ratio_ltr_measure(self):
        self.assertAlmostEqual(self.screen_ratio_ltr_measure(.3755782578608322, dh_app1.primary_state,
                                                             dh_app1.parameters), 1102.7636174940023, 5)

    def test_screen_distance_ltr_measure(self):
        self.assertAlmostEqual(self.screen_distance_ltr_measure(3.93700787, dh_sys_app1.primary_state,
                                                                dh_sys_app1.parameters), 1.415003537395672, 5)


class LtRCoefficientTransformationFormulaTestCaseMixin:
    horizontal_4_to_3_fov_coefficient = None
    horizontal_fov_to_80_coefficient = None

    def test_horizontal_4_to_3_fov_coefficient(self):
        self.assertAlmostEqual(self.horizontal_4_to_3_fov_coefficient(1, FOVData(radians(2), radians(3)), None,
                                                                      dh_app1.parameters), 1, 5)

    def test_horizontal_4_to_3_fov_coefficient2(self):
        p = Parameters(Fraction(16, 10), FS_VERTICAL_MINUS)
        self.assertAlmostEqual(self.horizontal_4_to_3_fov_coefficient(1, FOVData(radians(100), radians(50)),
                                                                      FOVData(radians(50), radians(25)), p), 2, 5)

    def test_horizontal_fov_to_80_coefficient(self):
        self.assertAlmostEqual(self.horizontal_fov_to_80_coefficient(1, FOVData(radians(160), radians(-5)), None,
                                                                     dh_app1.parameters), 2, 5)
