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

from setuptools import setup, find_packages

setup(name='thespiae', version='0.1',
      python_requires='>=3.8.1',
      install_requires=['antlr4-python3-runtime~=4.7.2', 'pyyaml>=5.1', 'aiohttp>=3.6.2 ', 'tqdm>=4.31.1',
                        'colorama~=0.4.1'],
      packages=find_packages(exclude=['thespiae.tests', 'thespiae.tests.*']),
      entry_points={'console_scripts': ['thespiae=thespiae.core:main']},
      description='Tool to setup Windows-based development environments',
      url='https://github.com/apleshakov/thespiae',
      author='Andrey Pleshakov',
      author_email='aplshkv@gmail.com',
      long_description_content_type='text/x-rst',
      license='Apache-2.0',
      classifiers=['Environment :: Console',
                   'License :: OSI Approved :: Apache Software License',
                   'Natural Language :: English',
                   'Operating System :: Microsoft :: Windows',
                   'Programming Language :: Python :: 3.8',
                   'Topic :: Utilities'])
