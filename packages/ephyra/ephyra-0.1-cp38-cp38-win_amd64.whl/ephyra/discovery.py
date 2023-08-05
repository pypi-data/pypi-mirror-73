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
from math import tan, fabs, radians
from typing import TYPE_CHECKING

from .data import FT_HORIZONTAL, FT_VERTICAL

if TYPE_CHECKING:
    from typing import Tuple

    from .core import FOVType

_ASPECT_RATIOS = (
    Fraction(4, 3),
    Fraction(5, 4),
    Fraction(3, 2),
    Fraction(16, 10),
    Fraction(16, 9),
    Fraction(21, 9),
    Fraction(32, 9)
)


def find_settings_fov_aspect_ratio(fov_settings: float, fov_real: float, fov_type: FOVType, real_aspect_ratio: Fraction,
                                   ratios_to_test: Tuple[Fraction, ...] = _ASPECT_RATIOS) -> Tuple[Fraction, float]:
    if fov_type == FT_HORIZONTAL:
        r = tan(radians(fov_real) / 2) / tan(radians(fov_settings) / 2)
    elif fov_type == FT_VERTICAL:
        r = tan(radians(fov_settings) / 2) / tan(radians(fov_real) / 2)
    else:
        raise ValueError(f'unknown fov type {fov_type}')
    settings_ratio = float(real_aspect_ratio) / r
    return min(zip(ratios_to_test, (fabs(float(ar) - settings_ratio) for ar in ratios_to_test)), key=lambda t: t[1])
