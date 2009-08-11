#!/usr/bin/env python
import os
# Settings for synthesis.py

# DB settings:
DB_DATABASE = ""
DB_USER = ""
DB_PASSWD = ""

BASE_PATH = ""

# Input files Processing path
INPUTFILES_PATH = "InputFiles"
XSD_PATH = "InputFiles"

PROCESSED_PATH = ""

SCHEMA_DOCS = {'hud_hmis_2_8_xml':os.path.join(XSD_PATH, 'HUD_HMIS_2_8.xsd')}

DEBUG = True									# Debug the application layer
DEBUG_ALCHEMY = False							# Debug the ORM Layer
DEBUG_DB = False								# Debug the DB layer of the application

# This mechanism provides an override to the settings above.  create a file called local_settings.py and simply
# override the values like BASE_PATH='/home/mypath'.  Then import like this: from conf import settings
# this will bring in all of settings.py's values and have the overriddin values of local_settings.py

try:
    from local_settings import *
except ImportError:
    pass
