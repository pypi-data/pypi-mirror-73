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

from __future__ import annotations

from abc import ABC, abstractmethod
from fractions import Fraction
from math import pi
from typing import TYPE_CHECKING

from ..data import State, Parameters
from ..formula import calculate_fov, convert_fov_to_aspect_ratio, screen_ratio_ltr_measure, \
    screen_distance_ltr_measure, radians_per_unit_measure, radians_for_distance_from_center, \
    radians_for_ratio_from_center, calculate_screen_width_height, rotation_ltr_measure
from ..util import for_rotation_type, parameters_consistent

if TYPE_CHECKING:
    from typing import Tuple, Callable

    from ..data import RotationType, FOVScaling, FOVType, FOVData

    FOVTransformationFormula = Callable[[float, FOVData, Parameters], float]
    LTRCoefficientTransformationFormula = Callable[[float, FOVData, FOVData, Parameters], float]


class DataHelper:

    def _create_state(self, fov: float, fov_aspect_ratio: Fraction, fov_type: FOVType, ltr_coefficient: float) \
            -> Tuple[State, FOVData]:
        if self._fov_t_f is not None:
            fov = self._fov_t_f(fov, self._st_ex, self._p)
        fov_d = calculate_fov(fov, fov_aspect_ratio, fov_type)
        if fov_aspect_ratio != self._p.screen_aspect_ratio:
            fov_d = convert_fov_to_aspect_ratio(fov_d, self._p.fov_scaling, self._p.screen_aspect_ratio)
        if self._ltr_c_f is not None:
            ltr_coefficient = self._ltr_c_f(ltr_coefficient, fov_d, self._st_ex, self._p)
        return State(ltr_coefficient, for_rotation_type(self._rt, fov_d.fov_horizontal, fov_d.fov_vertical)), fov_d

    def __init__(self, screen_aspect_ratio: Fraction, fov: float, fov_aspect_ratio: Fraction, fov_type: FOVType,
                 fov_scaling: FOVScaling, rt: RotationType, *, ltr_coefficient: float = 1,
                 fov_transformation_formula: FOVTransformationFormula = None,
                 ltr_coefficient_transformation_formula: LTRCoefficientTransformationFormula = None,
                 radians_per_count: float = None, counts_per_unit: float = None, screen_diagonal: float = None):
        self._def_fov_ar = fov_aspect_ratio
        self._def_fov_t = fov_type
        opt = {}
        if radians_per_count is not None:
            opt['consider_app_input_data'] = True
            opt['radians_per_count'] = radians_per_count
        if counts_per_unit is not None:
            opt['consider_system_input_data'] = True
            opt['counts_per_unit'] = counts_per_unit
        if screen_diagonal is not None:
            sw, sh = calculate_screen_width_height(screen_aspect_ratio, screen_diagonal)
            opt['consider_physical_screen_data'] = True
            opt['screen_length'] = for_rotation_type(rt, sw, sh)
        self._p = Parameters(screen_aspect_ratio, fov_scaling, **opt)
        self._fov_t_f = fov_transformation_formula
        self._ltr_c_f = ltr_coefficient_transformation_formula
        self._rt = rt
        self._st_ex = None
        # dangerous, pay attention to the initialized fields
        self._st, self._st_ex = self._create_state(fov, fov_aspect_ratio, fov_type, ltr_coefficient)

    @property
    def primary_state(self) -> State:
        return self._st

    @property
    def parameters(self) -> Parameters:
        return self._p

    def get_state_for_fov(self, fov: float, fov_aspect_ratio: Fraction = None, fov_type: FOVType = None,
                          ltr_coefficient: float = 1):
        if fov_aspect_ratio is None:
            fov_aspect_ratio = self._def_fov_ar
        if fov_type is None:
            fov_type = self._def_fov_t
        state, _ = self._create_state(fov, fov_aspect_ratio, fov_type, ltr_coefficient)
        return state


class _AbstractCalculator(ABC):

    def __init__(self, s1: State, p1: Parameters, p2: Parameters = None, val1: float = None, val2: float = None):
        if p2 is None:
            p2 = p1
        else:
            if not parameters_consistent(p1, p2):
                raise ValueError('p1 and p2 are inconsistent')
        self._p2 = p2
        if val2 is None:
            val2 = val1
        self._rm = self.measure_formula(val1, s1, p1)
        self._val2 = val2

    @staticmethod
    @abstractmethod
    def measure_formula(param: float, s: State, p: Parameters):
        pass

    def coefficient_for(self, s2: State) -> float:
        return self.measure_formula(self._val2, s2, self._p2) / self._rm

    def sensitivity_for(self, s1_sens: float, s2: State) -> Tuple[float, float]:
        c = self.coefficient_for(s2)
        return c, s1_sens * c


class FullRotationCalculator(_AbstractCalculator):

    def __init__(self, s1: State, p1: Parameters, p2: Parameters = None):
        super().__init__(s1, p1, p2, None, None)

    @staticmethod
    def measure_formula(_: float, s: State, p: Parameters):
        return rotation_ltr_measure(s, p)


class ScreenRatioCalculator(_AbstractCalculator):

    def __init__(self, ratio1: float, s1: State, p1: Parameters, p2: Parameters = None, ratio2: float = None):
        super().__init__(s1, p1, p2, ratio1, ratio2)

    @staticmethod
    def measure_formula(param: float, s: State, p: Parameters):
        return screen_ratio_ltr_measure(param, s, p)


class ScreenDistanceCalculator(_AbstractCalculator):

    def __init__(self, distance1: float, s1: State, p1: Parameters, p2: Parameters = None, distance2: float = None):
        if not p1.consider_physical_screen_data:
            raise ValueError('p1 lacks physical screen data')
        super().__init__(s1, p1, p2, distance1, distance2)

    @staticmethod
    def measure_formula(param: float, s: State, p: Parameters):
        return screen_distance_ltr_measure(param, s, p)


class DetailsCalculator:

    def __init__(self, s: State, p: Parameters):
        if not (p.consider_app_input_data and p.consider_system_input_data and p.consider_physical_screen_data):
            raise ValueError('p lacks data')
        self._s = s
        self._p = p
        self._rpu = radians_per_unit_measure(s, p)

    def full_rotation_units(self, sens: float) -> float:
        return 2 * pi / (self._rpu * sens)

    def screen_ratio_units(self, ratio: float, sens: float) -> float:
        return radians_for_ratio_from_center(ratio, self._s) / (self._rpu * sens)

    def screen_distance_units(self, distance: float, sens: float) -> float:
        return radians_for_distance_from_center(distance, self._s, self._p) / (self._rpu * sens)
