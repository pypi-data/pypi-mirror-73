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

from setuptools import setup, Extension, find_packages

_ephyra = Extension('_ephyra', sources=['_ephyra/_ephyramodule.c', '_ephyra/data.c', '_ephyra/formula.c',
                                        '_ephyra/util.c', '_ephyra/core.c'])

setup(name='ephyra', version='0.1',
      ext_modules=[_ephyra], python_requires='>=3.8.1',
      packages=find_packages(exclude=['ephyra.tests', 'ephyra.tests.*']),
      description='Library to help with mouse input configuration',
      url='https://github.com/apleshakov/ephyra',
      author='Andrey Pleshakov',
      author_email='aplshkv@gmail.com',
      long_description_content_type='text/x-rst',
      license='Apache-2.0',
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3.8',
                   'Topic :: Software Development :: Libraries'])
