#!/usr/bin/env python

# Alchemy Libraries
from zope.interface import implements
import dbobjects
from writer import Writer

class HMISCSV27Writer(dbobjects.DB):

    # Writer Interface
    implements (Writer)

    def __init__(self):
        pass

