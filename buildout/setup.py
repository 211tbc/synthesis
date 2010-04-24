#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'synthesis',
    version = '1.0',
    license = 'MIT',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)