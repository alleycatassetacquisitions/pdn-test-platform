#!/usr/bin/env python3
"""
Setup script for the Serial Log Testing Platform.
"""

from setuptools import setup, find_packages
import os

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if not line.startswith('#') and line.strip()]

# Read the version from src/__init__.py
with open(os.path.join('src', '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'\"")
            break

setup(
    name="serial-log-testing-platform",
    version=version,
    description="Platform for testing and analyzing serial log data from embedded devices",
    author="PDN Test Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'log-platform=src.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
) 