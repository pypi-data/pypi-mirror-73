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

from fractions import Fraction
from math import atan, tan, sqrt, radians
from typing import TYPE_CHECKING

from ..data import Parameters, FT_HORIZONTAL, FT_VERTICAL, FS_HORIZONTAL_PLUS, FS_VERTICAL_MINUS, FOVData

if TYPE_CHECKING:
    from typing import Tuple

    from ..data import FOVScaling, FOVType, State


# core


def _fov_h(fov_v: float, aspect_ratio: Fraction) -> float:
    return 2 * atan(tan(fov_v / 2) * (aspect_ratio.numerator / aspect_ratio.denominator))


def _fov_v(fov_h: float, aspect_ratio: Fraction) -> float:
    return 2 * atan(tan(fov_h / 2) * (aspect_ratio.denominator / aspect_ratio.numerator))


def calculate_screen_width_height(aspect_ratio: Fraction, diagonal: float) -> Tuple[float, float]:
    unit_length = sqrt(diagonal ** 2 / (aspect_ratio.numerator ** 2 + aspect_ratio.denominator ** 2))
    return aspect_ratio.numerator * unit_length, aspect_ratio.denominator * unit_length


# TODO: Type/Value error consistency with native implementation <AP>

def calculate_fov(fov: float, aspect_ratio: Fraction, fov_type: FOVType) -> FOVData:
    if fov_type == FT_HORIZONTAL:
        specified_horizontal_fov = fov
        specified_vertical_fov = _fov_v(specified_horizontal_fov, aspect_ratio)
    elif fov_type == FT_VERTICAL:
        specified_vertical_fov = fov
        specified_horizontal_fov = _fov_h(specified_vertical_fov, aspect_ratio)
    else:
        raise ValueError(f'unknown fov type {fov_type}')
    return FOVData(specified_horizontal_fov, specified_vertical_fov)


def convert_fov_to_aspect_ratio(fov: FOVData, fov_scaling: FOVScaling,
                                aspect_ratio: Fraction) -> FOVData:
    if fov_scaling == FS_HORIZONTAL_PLUS:
        actual_vertical_fov = fov.fov_vertical
        actual_horizontal_fov = _fov_h(fov.fov_vertical, aspect_ratio)
    elif fov_scaling == FS_VERTICAL_MINUS:
        actual_horizontal_fov = fov.fov_horizontal
        actual_vertical_fov = _fov_v(fov.fov_horizontal, aspect_ratio)
    else:
        raise ValueError(f'unknown fov scaling {fov_scaling}')
    return FOVData(actual_horizontal_fov, actual_vertical_fov)


def radians_per_unit_measure(s: State, p: Parameters) -> float:
    v = s.linear_to_rotary_measure
    if p.consider_app_input_data:
        v *= p.radians_per_count
    if p.consider_system_input_data:
        v *= p.counts_per_unit
    return v


def rotation_ltr_measure(s: State, p: Parameters) -> float:
    return 1 / radians_per_unit_measure(s, p)


def radians_for_ratio_from_center(ratio: float, s: State) -> float:
    return atan(ratio * tan(s.fov / 2))


def screen_ratio_ltr_measure(ratio: float, s: State, p: Parameters) -> float:
    return radians_for_ratio_from_center(ratio, s) / radians_per_unit_measure(s, p)


def radians_for_distance_from_center(distance: float, s: State, p: Parameters) -> float:
    return atan(2 * distance * tan(s.fov / 2) / p.screen_length)


def screen_distance_ltr_measure(distance: float, s: State, p: Parameters):
    return radians_for_distance_from_center(distance, s, p) / radians_per_unit_measure(s, p)


# LtR Coefficients

_RAD_80 = radians(80)


def horizontal_4_to_3_fov_coefficient(b: float, c: FOVData, z: FOVData, p: Parameters) -> float:
    if z:
        c_fov = convert_fov_to_aspect_ratio(c, p.fov_scaling, Fraction(4, 3))
        z_fov = convert_fov_to_aspect_ratio(z, p.fov_scaling, Fraction(4, 3))
        return b * c_fov.fov_horizontal / z_fov.fov_horizontal
    else:
        return b


def horizontal_fov_to_80_coefficient(b: float, c: FOVData, _: FOVData, _2: Parameters) -> float:
    return b * c.fov_horizontal / _RAD_80
