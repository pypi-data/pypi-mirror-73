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
from unittest import TestCase

from ephyra.data import FT_HORIZONTAL
from ephyra.discovery import find_settings_fov_aspect_ratio


class FOVSettingsDiscoveryTestCase(TestCase):

    def test_fov_aspect_ratio_discovery(self):
        ratio, diff = find_settings_fov_aspect_ratio(radians(70), radians(81), FT_HORIZONTAL, Fraction(16, 10))
        self.assertEqual(ratio, Fraction(4, 3))
        self.assertLessEqual(diff, 0.05)

    # TODO: test with real data for FT_VERTICAL <AP>
