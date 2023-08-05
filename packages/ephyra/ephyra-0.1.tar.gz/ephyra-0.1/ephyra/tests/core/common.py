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
from math import radians

from ephyra.data import FS_HORIZONTAL_PLUS, FS_VERTICAL_MINUS, FT_VERTICAL, RT_AZIMUTHAL, RT_POLAR
from ..helper import dh_sys_app1_factory, dh_sys_app1_p_factory, dh_app1, dh_sys_app1, dh_app2, dh_sys_app2, \
    params_collection, state


class DataHelperTestCaseMixin:
    data_helper = None

    def _test1(self, p, sp, s1, sl, fs, f1):
        # parameters
        self.assertEqual(p.screen_aspect_ratio, Fraction(16, 10))
        self.assertAlmostEqual(p.screen_length, sl, 5)
        self.assertTrue(p.consider_physical_screen_data)
        self.assertAlmostEqual(p.counts_per_unit, 800, 5)
        self.assertTrue(p.consider_system_input_data)
        self.assertAlmostEqual(p.radians_per_count, .0003839724354387525, 8)
        self.assertTrue(p.consider_app_input_data)
        self.assertEqual(p.fov_scaling, FS_HORIZONTAL_PLUS)
        # primary state
        self.assertAlmostEqual(sp.linear_to_rotary_measure, 1, 5)
        self.assertAlmostEqual(sp.fov, fs, 5)
        # state
        self.assertAlmostEqual(s1.linear_to_rotary_measure, .25, 5)
        self.assertAlmostEqual(s1.fov, f1, 5)

    def _test2(self, p, sp, s1, fs, f1):
        # parameters
        self.assertEqual(p.screen_aspect_ratio, Fraction(16, 10))
        self.assertAlmostEqual(p.screen_length, .0, 5)
        self.assertFalse(p.consider_physical_screen_data)
        self.assertAlmostEqual(p.counts_per_unit, .0, 5)
        self.assertFalse(p.consider_system_input_data)
        self.assertAlmostEqual(p.radians_per_count, .0, 5)
        self.assertFalse(p.consider_app_input_data)
        self.assertEqual(p.fov_scaling, FS_VERTICAL_MINUS)
        # primary state
        self.assertAlmostEqual(sp.linear_to_rotary_measure, 0.9, 5)
        self.assertAlmostEqual(sp.fov, fs, 5)
        # state
        self.assertAlmostEqual(s1.linear_to_rotary_measure, 1, 5)
        self.assertAlmostEqual(s1.fov, f1, 5)

    def test_azimuthal_rotation_data(self):
        dh_sys_app = dh_sys_app1_factory(self.data_helper)
        s1 = dh_sys_app.get_state_for_fov(radians(52.8605), fov_aspect_ratio=Fraction(16, 10),
                                          ltr_coefficient=0.5)
        self._test1(dh_sys_app.parameters, dh_sys_app.primary_state, s1, 20.35195929612211,
                    radians(100.3888578154696), radians(52.8605))

    def test_azimuthal_rotation_data2(self):
        dh = self.data_helper(Fraction(16, 10), radians(73.74), Fraction(16, 9), FT_VERTICAL, FS_VERTICAL_MINUS,
                              RT_AZIMUTHAL, ltr_coefficient=0.9, fov_transformation_formula=lambda f, df, pr: f * 1.2)
        s1 = dh.get_state_for_fov(radians(35), Fraction(4, 3), FT_VERTICAL)
        self._test2(dh.parameters, dh.primary_state, s1, radians(119.98340377498069), radians(54.20843241712849))

    def test_polar_rotation_data(self):
        dh_sys_app1_p = dh_sys_app1_p_factory(self.data_helper)
        s1 = dh_sys_app1_p.get_state_for_fov(radians(52.8605), fov_aspect_ratio=Fraction(16, 10),
                                             ltr_coefficient=0.5)
        self._test1(dh_sys_app1_p.parameters, dh_sys_app1_p.primary_state, s1, 12.71997456007632,
                    radians(73.73979529168803), radians(34.51628653564565))

    def test_polar_rotation_data2(self):
        dh = self.data_helper(Fraction(16, 10), radians(73.74), Fraction(16, 9), FT_VERTICAL, FS_VERTICAL_MINUS,
                              RT_POLAR, ltr_coefficient=0.9, fov_transformation_formula=lambda f, df, pr: f * 1.2)
        s1 = dh.get_state_for_fov(radians(35), Fraction(4, 3), FT_VERTICAL)
        self._test2(dh.parameters, dh.primary_state, s1, radians(94.51984219934904), radians(35.477565197940905))

    def test_invalid_rotation_type(self):
        with self.assertRaises(ValueError):
            self.data_helper(Fraction(16, 10), radians(73.74), Fraction(16, 9), FT_VERTICAL, FS_VERTICAL_MINUS,
                             -5, ltr_coefficient=0.9, fov_transformation_formula=lambda f, df, pr: f * 1.2)


class _ParametersConsistencyMixin:
    calc_factory = None

    def test_data_consistency(self):
        for p1 in params_collection:
            for p2 in params_collection:
                with self.subTest(p1=p1, p2=p2):
                    if not hasattr(self, 'data_consistency_assumption') or self.data_consistency_assumption(p1):
                        if p1.consider_physical_screen_data == p2.consider_physical_screen_data \
                                and p1.consider_system_input_data == p2.consider_system_input_data \
                                and p1.consider_app_input_data == p2.consider_app_input_data:
                            self.calc_factory(p1, p2)
                        else:
                            with self.assertRaises(ValueError):
                                self.calc_factory(p1, p2)


class _ParametersSufficiencyMixin:
    calc_factory = None

    def test_data_sufficiency(self):
        for p in params_collection:
            with self.subTest(p=p):
                if self.data_consistency_assumption(p):
                    self.calc_factory(p, p)
                else:
                    with self.assertRaises(ValueError):
                        self.calc_factory(p, p)


class FullRotationCalculatorTestCaseMixin(_ParametersConsistencyMixin):
    FullRotationCalculator = None

    def test_full_rotation_coefficient(self):
        s2 = dh_app1.get_state_for_fov(radians(45))
        c = self.FullRotationCalculator(dh_app1.primary_state, dh_app1.parameters)
        self.assertAlmostEqual(c.coefficient_for(s2), 2, 5)

    def test_full_rotation_sens(self):
        s2 = dh_app2.primary_state
        c = self.FullRotationCalculator(dh_app1.primary_state, dh_app1.parameters, dh_app2.parameters)
        cf, sens = c.sensitivity_for(2, s2)
        self.assertAlmostEqual(cf, .007899999999999999, 5)
        self.assertAlmostEqual(sens, .0158, 5)

    def calc_factory(self, p1, p2):
        return self.FullRotationCalculator(state, p1, p2)


class ScreenRatioCalculatorTestCaseMixin(_ParametersConsistencyMixin):
    ScreenRatioCalculator = None

    def test_screen_ratio_coefficient(self):
        s2 = dh_app1.get_state_for_fov(radians(45))
        c = self.ScreenRatioCalculator(.3755782578608322, dh_app1.primary_state, dh_app1.parameters)
        self.assertAlmostEqual(c.coefficient_for(s2), .8717319501838238, 5)

    def test_screen_ratio_coefficient2(self):
        s2 = dh_app2.primary_state
        c = self.ScreenRatioCalculator(.3755782578608322, dh_app1.primary_state, dh_app1.parameters, dh_app2.parameters,
                                       .1877891289304161)
        self.assertAlmostEqual(c.coefficient_for(s2), .004107746005894921, 5)

    def test_screen_ratio_sens(self):
        s2 = dh_app2.get_state_for_fov(radians(40))
        c = self.ScreenRatioCalculator(.3755782578608322, dh_app2.primary_state, dh_app2.parameters)
        cf, sens = c.sensitivity_for(.0158, s2)
        self.assertAlmostEqual(cf, .8070339035709131, 5)
        self.assertAlmostEqual(sens, .01275113567642043, 5)

    def calc_factory(self, p1, p2):
        return self.ScreenRatioCalculator(1, state, p1, p2, 2)


class ScreenDistanceCalculatorTestCaseMixin(_ParametersConsistencyMixin, _ParametersSufficiencyMixin):
    ScreenDistanceCalculator = None

    def test_screen_distance_coefficient(self):
        s2 = dh_sys_app1.get_state_for_fov(radians(45))
        c = self.ScreenDistanceCalculator(3.93700787, dh_sys_app1.primary_state, dh_sys_app1.parameters)
        self.assertAlmostEqual(c.coefficient_for(s2), .8741948552471518, 5)

    def test_screen_distance_coefficient2(self):
        s2 = dh_sys_app2.primary_state
        c = self.ScreenDistanceCalculator(3.93700787, dh_sys_app1.primary_state, dh_sys_app1.parameters,
                                          dh_sys_app2.parameters, 3.93700787 / 2)
        self.assertAlmostEqual(c.coefficient_for(s2), .004118163897214368, 5)

    def test_screen_distance_sens(self):
        s2 = dh_sys_app2.get_state_for_fov(radians(40))
        c = self.ScreenDistanceCalculator(3.93700787, dh_sys_app2.primary_state, dh_sys_app2.parameters)
        cf, sens = c.sensitivity_for(.0158, s2)
        self.assertAlmostEqual(cf, .8095353430632674, 5)
        self.assertAlmostEqual(sens, .012790658420399625, 5)

    def calc_factory(self, p1, p2):
        return self.ScreenDistanceCalculator(1, state, p1, p2, 2)

    @staticmethod
    def data_consistency_assumption(p):
        return p.consider_physical_screen_data


class _ParametersSufficiencyMixin:
    calc_factory = None

    def test_data_sufficiency(self):
        for p in params_collection:
            with self.subTest(p=p):
                if self.data_consistency_assumption(p):
                    self.calc_factory(p, p)
                else:
                    with self.assertRaises(ValueError):
                        self.calc_factory(p, p)


class DetailsCalculatorTestCaseMixin(_ParametersSufficiencyMixin):
    DetailsCalculator = None

    def test_full_rotation_units(self):
        d = self.DetailsCalculator(dh_sys_app1.primary_state, dh_sys_app1.parameters)
        self.assertAlmostEqual(d.full_rotation_units(2), 10.227272727272728, 5)

    def test_screen_ratio_units(self):
        d = self.DetailsCalculator(dh_sys_app1.primary_state, dh_sys_app1.parameters)
        self.assertAlmostEqual(d.screen_ratio_units(.3755782578608322, 2), .6892272609337514, 5)

    def test_screen_distance_units(self):
        d = self.DetailsCalculator(dh_sys_app1.primary_state, dh_sys_app1.parameters)
        self.assertAlmostEqual(d.screen_distance_units(10, 2), 1.411991816731347, 5)

    def calc_factory(self, p1, _):
        return self.DetailsCalculator(state, p1)

    @staticmethod
    def data_consistency_assumption(p):
        return p.consider_physical_screen_data and p.consider_system_input_data and p.consider_app_input_data
