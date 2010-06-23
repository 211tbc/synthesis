#!/usr/bin/env python
import os
#import sys

# Settings for synthesis.py

MODE = 'PROD'                               # This is the switch that runs the program in Test Mode.

# DB settings:
DB_DATABASE = "synthesis"
DB_USER = "postgres"
DB_PASSWD = "mypassword"
DB_HOST = "localhost"
DB_PORT = 5432

# uses current working directory, uncomment the line if the output path needs to be elsewhere.
BASE_PATH = os.getcwd()

PATH_TO_GPG = os.path.join(BASE_PATH, 'gpg.exe')
PGPHOMEDIR = os.path.join(BASE_PATH, 'gpghome')
PASSPHRASE = 'mypassword'

# Input files Processing path
# New 'Customers' input file path must be put into this 'list'.  Add it to the list mechanism.  
INPUTFILES_PATH = [
            os.path.join(BASE_PATH, "InputFiles")
            ]

# subfolder 
XSD_PATH = "xsd"

# file path subdirectories
OUTPUTFILES_PATH = os.path.join(BASE_PATH, "OutputFiles")
if not os.path.exists(OUTPUTFILES_PATH):
    os.mkdir(OUTPUTFILES_PATH)
    
USEDFILES = os.path.join(BASE_PATH, "UsedFiles")
if not os.path.exists(USEDFILES):
    os.mkdir(USEDFILES)
    
FAILEDFILES = os.path.join(BASE_PATH, "FailedFiles")
if not os.path.exists(FAILEDFILES ):
    os.mkdir(FAILEDFILES )
    
LOGS = os.path.join(BASE_PATH, "logs")
if not os.path.exists(LOGS):
    os.mkdir(LOGS)

PROCESSED_PATH = ""

SCHEMA_DOCS = {'hud_hmis_2_8_xml':os.path.join(BASE_PATH, XSD_PATH, 'HUD_HMIS_2_8.xsd'),
                'jfcs_service_xml':os.path.join(BASE_PATH, XSD_PATH, 'JFCS_SERVICE.xsd'),
                'jfcs_client_xml':os.path.join(BASE_PATH, XSD_PATH, 'JFCS_CLIENT.xsd'),
                'operation_par_xml':os.path.join(BASE_PATH, XSD_PATH, 'Operation_PAR_Extend_HUD_HMIS_2_8.xsd')
               }

DEBUG = False                                    # Debug the application layer
DEBUG_ALCHEMY = False                            # Debug the ORM Layer
DEBUG_DB = False                                # Debug the DB layer of the application

# This mechanism provides an override to the settings above.  create a file called local_settings.py and simply
# override the values like BASE_PATH='/home/mypath'.  Then import like this: from conf import settings
# this will bring in all of settings.py's values and have the overriddin values of local_settings.py

# email configuration
SMTPSERVER = '10.37.129.4'
SMTPPORT = 25
SMTPSENDER = 'joe@t3ch.com'
SMTPSENDERPWD = ''

# SMTP Mail recipients is a dictionary that must be defined for each source of input files
SMTPRECIPIENTS = \
    {
    os.path.join(BASE_PATH, "InputFiles"):
        {
        'SMTPTOADDRESS': ['joe+dev.synthesis.1@t3ch.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        }
    }

try:
    from local_settings import *
except ImportError:
    pass

