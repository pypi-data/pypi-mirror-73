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

from unittest import TestCase

from ephyra.core._python import DataHelper, FullRotationCalculator, ScreenRatioCalculator, ScreenDistanceCalculator, \
    DetailsCalculator
from .common import DataHelperTestCaseMixin, FullRotationCalculatorTestCaseMixin, ScreenRatioCalculatorTestCaseMixin, \
    ScreenDistanceCalculatorTestCaseMixin, DetailsCalculatorTestCaseMixin


class PyDataHelperTestCase(DataHelperTestCaseMixin, TestCase):
    data_helper = DataHelper


class PyFullRotationCalculatorTestCase(FullRotationCalculatorTestCaseMixin, TestCase):
    FullRotationCalculator = FullRotationCalculator


class NScreenRatioCalculatorTestCase(ScreenRatioCalculatorTestCaseMixin, TestCase):
    ScreenRatioCalculator = ScreenRatioCalculator


class NScreenDistanceCalculatorTestCase(ScreenDistanceCalculatorTestCaseMixin, TestCase):
    ScreenDistanceCalculator = ScreenDistanceCalculator


class NDetailsCalculatorTestCase(DetailsCalculatorTestCaseMixin, TestCase):
    DetailsCalculator = DetailsCalculator
