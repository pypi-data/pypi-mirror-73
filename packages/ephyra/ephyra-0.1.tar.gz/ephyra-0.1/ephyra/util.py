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

from typing import TYPE_CHECKING

from .data import RT_AZIMUTHAL, RT_POLAR, Parameters

if TYPE_CHECKING:
    from .data import RotationType


def for_rotation_type(rt: RotationType, for_azimuthal, for_polar):
    if rt == RT_AZIMUTHAL:
        return for_azimuthal
    elif rt == RT_POLAR:
        return for_polar
    else:
        raise ValueError(f'unknown rotation type {rt}')


def parameters_consistent(p1: Parameters, p2: Parameters):
    return p1.consider_app_input_data == p2.consider_app_input_data \
           and p1.consider_system_input_data == p2.consider_system_input_data \
           and p1.consider_physical_screen_data == p2.consider_physical_screen_data
