#!/usr/bin/env python

# Alchemy Libraries
from zope.interface import implementer
from . import dbobjects
from .writer import Writer

@implementer(Writer)
class HMISCSV27Writer(dbobjects.DB):
    # Writer Interface
    # implements (Writer)

    def __init__(self):
        pass

