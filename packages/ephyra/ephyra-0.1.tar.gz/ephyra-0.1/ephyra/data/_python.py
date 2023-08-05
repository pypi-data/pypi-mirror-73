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

from dataclasses import dataclass
from fractions import Fraction

from ._types import *

FS_HORIZONTAL_PLUS: FOVScaling = 0
FS_VERTICAL_MINUS: FOVScaling = 1

FT_HORIZONTAL: FOVType = 0
FT_VERTICAL: FOVType = 1

RT_AZIMUTHAL: RotationType = 0
RT_POLAR: RotationType = 1


@dataclass(frozen=True, eq=False)
class Parameters:
    screen_aspect_ratio: Fraction
    fov_scaling: FOVScaling
    radians_per_count: float = .0
    counts_per_unit: float = .0
    screen_length: float = .0
    consider_app_input_data: bool = False
    consider_system_input_data: bool = False
    consider_physical_screen_data: bool = False


@dataclass(frozen=True, eq=False)
class FOVData:
    fov_horizontal: float
    fov_vertical: float


@dataclass(frozen=True, eq=False)
class State:
    linear_to_rotary_measure: float
    fov: float
