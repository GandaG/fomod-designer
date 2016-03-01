#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2016 Daniel Nunes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages
from setuptools import setup


setup(
    name='fomod-editor',
    version='0.0.0',
    license='MIT',
    description="",
    author='Daniel Nunes',
    author_email='gandaganza@gmail.com',
    url='https://github.com/GandaG/fomod-editor',
    packages=find_packages(''),
    package_dir={''},
    py_modules=[splitext(basename(path))[0] for path in glob('fomod/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'fomod=fomod.cli:main',
        ]
    },
)
