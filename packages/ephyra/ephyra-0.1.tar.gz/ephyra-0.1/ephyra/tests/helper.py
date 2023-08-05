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
from math import radians
from typing import TYPE_CHECKING

from ephyra.core import DataHelper
from ephyra.data import FT_HORIZONTAL, FS_HORIZONTAL_PLUS, RT_AZIMUTHAL, FS_VERTICAL_MINUS, Parameters, State, RT_POLAR
from ephyra.formula import horizontal_4_to_3_fov_coefficient, horizontal_fov_to_80_coefficient

if TYPE_CHECKING:
    from typing import Type, TypeVar

    HT = TypeVar('HT', bound=DataHelper)

dh_app1 = DataHelper(Fraction(16, 10), radians(90), Fraction(4, 3), FT_HORIZONTAL, FS_HORIZONTAL_PLUS,
                     RT_AZIMUTHAL, ltr_coefficient_transformation_formula=horizontal_4_to_3_fov_coefficient,
                     radians_per_count=radians(0.022))


def dh_sys_app1_factory(dh: Type[HT]) -> HT:
    return dh(Fraction(16, 10), radians(90), Fraction(4, 3), FT_HORIZONTAL, FS_HORIZONTAL_PLUS, RT_AZIMUTHAL,
              ltr_coefficient_transformation_formula=horizontal_4_to_3_fov_coefficient,
              radians_per_count=radians(0.022), counts_per_unit=800, screen_diagonal=24)


dh_sys_app1 = dh_sys_app1_factory(DataHelper)


def dh_sys_app1_p_factory(dh: Type[HT]) -> HT:
    return dh(Fraction(16, 10), radians(90), Fraction(4, 3), FT_HORIZONTAL, FS_HORIZONTAL_PLUS, RT_POLAR,
              ltr_coefficient_transformation_formula=horizontal_4_to_3_fov_coefficient,
              radians_per_count=radians(0.022), counts_per_unit=800, screen_diagonal=24)


dh_sys_app1_p = dh_sys_app1_p_factory(DataHelper)

dh_app2 = DataHelper(Fraction(16, 10), radians(100), Fraction(16, 10), FT_HORIZONTAL, FS_VERTICAL_MINUS,
                     RT_AZIMUTHAL, ltr_coefficient_transformation_formula=horizontal_fov_to_80_coefficient,
                     radians_per_count=radians(2.2278481012658227))

dh_sys_app2 = DataHelper(Fraction(16, 10), radians(100), Fraction(16, 10), FT_HORIZONTAL, FS_VERTICAL_MINUS,
                         RT_AZIMUTHAL, ltr_coefficient_transformation_formula=horizontal_fov_to_80_coefficient,
                         radians_per_count=radians(2.2278481012658227), counts_per_unit=800, screen_diagonal=24)

# TODO: investigate Hypothesis library for exhaustive discrete strategies <AP>

state = State(1., 1.)

params_collection = []

for rpc in (False, True):
    for cpu in (False, True):
        for sl in (False, True):
            params_collection.append(Parameters(Fraction(1, 1), FS_HORIZONTAL_PLUS, radians_per_count=1.,
                                                consider_app_input_data=rpc, counts_per_unit=1.,
                                                consider_system_input_data=cpu, screen_length=1.,
                                                consider_physical_screen_data=sl))
