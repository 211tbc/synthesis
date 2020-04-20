'''Reads a a set of HMIS CSV files into memory, parses their contents, and stores 
their informaton into a postgresql database.  This is a log database, so it holds 
everything and doesn't worry about deduplication.  The only thing it enforces 
are exportids, which must be unique.'''

#import sys, os
from .reader import Reader
from zope.interface import implementer
#from lxml import etree
#from sqlalchemy.exc import IntegrityError
#import dateutil.parser
#import logging
#from conf import settings
#import clsExceptions
from . import dbobjects
#from fileUtils import fileUtilities
#from errcatalog import catalog

@implementer(Reader)
class HmisCsv30Reader(dbobjects.DB):
    '''Implements reader interface.'''
    #implements (Reader) 
    
    hmis_namespace = None 
    airs_namespace = None
    nsmap = None
    #global FILEUTIL
    #FILEUTIL = fileUtilities(settings.DEBUG, None)

    def __init__(self, dir_name):
        pass
        
# if __name__ == "__main__":
#     sys.exit(main()) 
