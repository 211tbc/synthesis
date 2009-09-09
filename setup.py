#!/usr/bin/env python

from setuptools import setup # this is new

setup(name='synthesis',
version='1.0',
py_modules=['clsExceptions'
,'DBObjects'
,'DBObjects_unit_test'
,'emailProcessor'
,'fileinput_unit_test_file_exists'
,'fileinput_unit_test_no_file'
,'fileinputwatcher'
,'fileRouter'
,'fileUtils'
,'hmiscsv27writer'
,'hmisxml28reader'
,'hmisxml28writer'
,'interpretPicklist'
,'local_settings'
,'MainProcessor'
,'nodebuilder'
,'optimized_al'
,'postgresutils'
,'reader'
,'selector'
,'selector_unit_test'
,'smtpLibrary'
,'svcpointxml20writer'
,'synthesisINI'
,'testCase_settings'
,'translator'
,'validate_unit_test'
,'vendorxmlxxwriter'
,'writer'
'XMLUtilities'],
packages=['conf','errcatalog','xsd','InputFiles','Used',]
)