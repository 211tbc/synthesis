#!/usr/bin/env python
import os
# Settings for synthesis.py

# DB settings:
DB_DATABASE = ""
DB_USER = ""
DB_PASSWD = ""

BASE_PATH = ""

# Input files Processing path
INPUTFILES_PATH = ""
XSD_PATH = ""

PROCESSED_PATH = ""

SCHEMA_DOCS = {'hud_hmis_2_8_xml':os.path.join(XSD_PATH, 'HUD_HMIS_2_8.xsd')}

DEBUG = False									# Debug the application layer
DEBUG_ALCHEMY = False							# Debug the ORM Layer
DEBUG_DB = False								# Debug the DB layer of the application

