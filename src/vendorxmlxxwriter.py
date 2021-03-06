#!/usr/bin/env python
import os.path
from . import interpretpicklist
from datetime import timedelta, date, datetime
from time import strptime, time
from .xmlutilities import IDGeneration

# Alchemy Libraries
from sqlalchemy import create_engine, Table, Column, Numeric, Integer, String, Boolean, MetaData, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, mapper, backref, relation, clear_mappers
from sqlalchemy.types import DateTime, Date

from sys import version
from .conf import settings
from . import exceptions
from . import dbobjects
from .writer import Writer

from zope.interface import implementer

@implementer(Writer)
class VendorXMLXXWriter(dbobjects.DB):

    # Writer Interface

    def __init__(self):
        pass
    
    
