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


class ParametersTestCaseMixin:
    Parameters = None
    FS_HORIZONTAL_PLUS = None
    FS_VERTICAL_MINUS = None

    def _test_considerations(self, p: Parameters, consider_aid: bool, consider_sid: bool, consider_psd: bool):
        self.assertEqual(p.consider_app_input_data, consider_aid)
        self.assertEqual(p.consider_system_input_data, consider_sid)
        self.assertEqual(p.consider_physical_screen_data, consider_psd)

    def _test_parameters(self, p: Parameters):
        self.assertEqual(p.screen_aspect_ratio, Fraction(1, 2))
        self.assertEqual(p.fov_scaling, self.FS_HORIZONTAL_PLUS)
        self.assertAlmostEqual(p.radians_per_count, 3.1, 5)
        self.assertAlmostEqual(p.counts_per_unit, 4.1, 5)
        self.assertAlmostEqual(p.screen_length, 5.1, 5)
        self._test_considerations(p, True, True, True)

    def test_parameters(self):
        p = self.Parameters(screen_aspect_ratio=Fraction(1, 2), fov_scaling=self.FS_HORIZONTAL_PLUS,
                            radians_per_count=3.1, counts_per_unit=4.1, screen_length=5.1, consider_app_input_data=True,
                            consider_system_input_data=True, consider_physical_screen_data=True)
        self._test_parameters(p)

    def test_parameters2(self):
        p = self.Parameters(screen_aspect_ratio=Fraction(1, 2), fov_scaling=self.FS_VERTICAL_MINUS)
        self.assertEqual(p.screen_aspect_ratio, Fraction(1, 2))
        self.assertEqual(p.fov_scaling, self.FS_VERTICAL_MINUS)
        self.assertAlmostEqual(p.radians_per_count, .0, 5)
        self.assertAlmostEqual(p.counts_per_unit, .0, 5)
        self.assertAlmostEqual(p.screen_length, .0, 5)
        self._test_considerations(p, False, False, False)

    def test_parameters3(self):
        p = self.Parameters(screen_aspect_ratio=Fraction(1, 2), fov_scaling=self.FS_VERTICAL_MINUS, radians_per_count=3,
                            consider_app_input_data=True)
        self.assertEqual(p.screen_aspect_ratio, Fraction(1, 2))
        self.assertEqual(p.fov_scaling, self.FS_VERTICAL_MINUS)
        self._test_considerations(p, True, False, False)

    def test_parameters4(self):
        p = self.Parameters(screen_aspect_ratio=Fraction(1, 2), fov_scaling=self.FS_VERTICAL_MINUS, counts_per_unit=4,
                            consider_system_input_data=True)
        self.assertEqual(p.screen_aspect_ratio, Fraction(1, 2))
        self.assertEqual(p.fov_scaling, self.FS_VERTICAL_MINUS)
        self._test_considerations(p, False, True, False)

    def test_parameters5(self):
        p = self.Parameters(screen_aspect_ratio=Fraction(1, 2), fov_scaling=self.FS_HORIZONTAL_PLUS, screen_length=4,
                            consider_physical_screen_data=True)
        self.assertEqual(p.screen_aspect_ratio, Fraction(1, 2))
        self.assertEqual(p.fov_scaling, self.FS_HORIZONTAL_PLUS)
        self._test_considerations(p, False, False, True)

    def test_parameters6(self):
        p = self.Parameters(Fraction(1, 2), self.FS_HORIZONTAL_PLUS, 3.1, 4.1, 5.1, True, True, True)
        self._test_parameters(p)


class FOVDataTestCaseMixin:
    FOVData = None

    def test_fov_data(self):
        fd = self.FOVData(fov_horizontal=1.1, fov_vertical=2.1)
        self.assertAlmostEqual(fd.fov_horizontal, 1.1)
        self.assertAlmostEqual(fd.fov_vertical, 2.1)

    def test_fov_data2(self):
        fd = self.FOVData(1.1, 2.1)
        self.assertAlmostEqual(fd.fov_horizontal, 1.1)
        self.assertAlmostEqual(fd.fov_vertical, 2.1)


class StateTestCaseMixin:
    State = None

    def test_state(self):
        s = self.State(linear_to_rotary_measure=1.1, fov=2.1)
        self.assertAlmostEqual(s.linear_to_rotary_measure, 1.1)
        self.assertAlmostEqual(s.fov, 2.1)

    def test_state2(self):
        s = self.State(1.1, 2.1)
        self.assertAlmostEqual(s.linear_to_rotary_measure, 1.1)
        self.assertAlmostEqual(s.fov, 2.1)


class ConstantTestCaseMixin:
    FS_HORIZONTAL_PLUS = None
    FS_VERTICAL_MINUS = None
    FT_HORIZONTAL = None
    FT_VERTICAL = None
    RT_AZIMUTHAL = None
    RT_POLAR = None

    def test_constants(self):
        self.assertEqual(self.FS_HORIZONTAL_PLUS, 0)
        self.assertEqual(self.FS_VERTICAL_MINUS, 1)
        self.assertEqual(self.FT_HORIZONTAL, 0)
        self.assertEqual(self.FT_VERTICAL, 1)
        self.assertEqual(self.RT_AZIMUTHAL, 0)
        self.assertEqual(self.RT_POLAR, 1)
