#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

version = '1.0'

install_requires = [
    'setuptools',
]

#ECJ20100920 needed to remove this hard-coded dependency condition, since pyinotify 0.8.8 isn't installing, whilst 0.9.0 seems to work fine
#if sys.platform.startswith("linux"):
#    install_requires.append("pyinotify==0.8.8")

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