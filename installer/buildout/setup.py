#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

version = '1.0'

install_requires = [
    'setuptools',
]

if sys.platform.startswith("linux"):
    install_requires.append("pyinotify==0.8.8")

setup(
    name = 'synthesis',
    version = version,
    license = 'MIT',
    namespace_packages=[],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    install_requires = install_requires,
)