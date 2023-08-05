#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import setup, find_packages
import sys

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    reqs = f.read()

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fever-drqa',
    author='James Thorne',
    author_email='james@jamesthorne.co.uk',
    url='https://jamesthorne.co.uk',
    version='1.0.13',
    description='Adapted version of Facebooks Reading Wikipedia to Answer Open-Domain Questions',
    long_description="This is an adapted version of the DrQA facebook library for use in FEVER",
    license=license,
    python_requires='>=3.5',
    packages=find_packages(exclude=('data')),
    install_requires=reqs.strip().split('\n'),
)
