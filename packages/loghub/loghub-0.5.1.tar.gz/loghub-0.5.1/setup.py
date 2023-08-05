#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Setup script for loghub."""

# Standard library imports
import ast
import os

# Third party imports
from setuptools import find_packages, setup

# Constants
HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='loghub'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()

    lines = data.split('\n')
    for line in lines:
        if line.startswith('__version__'):
            version = ast.literal_eval(line.split('=')[-1].strip())
            break

    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.md'), 'r') as f:
        data = f.read()
    return data


REQUIREMENTS = [
    'jinja2',
    'requests',
]

setup(
    name='loghub',
    version=get_version(),
    keywords=["github zenhub changelog milestone releases"],
    url='https://github.com/spyder-ide/loghub',
    license='MIT',
    author='Carlos Cordoba',
    author_email='ccordoba12@gmail.com',
    maintainer='Carlos Cordoba',
    maintainer_email='ccordoba12@gmail.com',
    description='Generate changelogs based on Github milestones or tags',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={'loghub.templates': ['*.txt']},
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'loghub = loghub.cli.main:main',
            'loghub-labels = loghub.cli.label_creator:main',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
