#!/usr/bin/env python
import os.path
from interpretPicklist import interpretPickList
from datetime import timedelta, date, datetime
from time import strptime, time
from XMLUtilities import XMLUtilities

# Alchemy Libraries
from sqlalchemy import create_engine, Table, Column, Numeric, Integer, String, Boolean, MetaData, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, mapper, backref, relation, clear_mappers
from sqlalchemy.types import DateTime, Date

from sys import version
from conf import settings
import clsExceptions
import DBObjects
from writer import Writer

from zope.interface import implements


class VendorXMLXXWriter(DBObjects.databaseObjects):

    # Writer Interface
    implements (Writer)

    def __init__(self):
        pass
    
    