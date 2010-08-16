#!/usr/bin/env python
import os
# Settings for synthesis.py

MODE = 'TEST'                               # This is the switch that runs the program in Test Mode.

# DB settings:
DB_DATABASE = "synthesis"
DB_USER = "postgres"
DB_PASSWD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

# uses current working directory, uncomment the line if the output path needs to be elsewhere.
BASE_PATH = os.getcwd()
#BASE_PATH = ""

PATH_TO_GPG = '/usr/bin/gpg'
PGPHOMEDIR = ''
PASSPHRASE = ''

# Input files Processing path
# New 'Customers' input file path must be put into this 'list'.  Add it to the list mechanism.  
INPUTFILES_PATH = \
[
    os.path.join(BASE_PATH, "InputFiles/1"),
    os.path.join(BASE_PATH, "InputFiles/2"),
    os.path.join(BASE_PATH, "InputFiles/3")
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
               'hud_hmis_3_0_xml':os.path.join(BASE_PATH, XSD_PATH, 'HUD_HMIS_3_0.xsd'),
               'jfcs_service_xml':os.path.join(BASE_PATH, XSD_PATH, 'JFCS_SERVICE.xsd'),
               'jfcs_client_xml':os.path.join(BASE_PATH, XSD_PATH, 'JFCS_CLIENT.xsd'),
               'operation_par_xml':os.path.join(BASE_PATH, XSD_PATH, 'Operation_PAR_Extend_HUD_HMIS_2_8.xsd')
              }

DEBUG = True                                    # Debug the application layer
DEBUG_ALCHEMY = True                            # Debug the ORM Layer
DEBUG_DB = True                                # Debug the DB layer of the application

# This mechanism provides an override to the settings above.  create a file called local_settings.py and simply
# override the values like BASE_PATH='/home/mypath'.  Then import like this: from conf import settings
# this will bring in all of settings.py's values and have the overriddin values of local_settings.py

# email configuration
SMTPSERVER = 'localhost'
SMTPPORT = 25
SMTPSENDER = 'usert@localhost'
SMTPSENDERPWD = ''

# SMTP Mail recipients is a dictionary that must be defined for each source of input files
SMTPRECIPIENTS = \
    {
        os.path.join(BASE_PATH, "InputFiles/1"):
        {
        'SMTPTOADDRESS': ['usert@localhost',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        },
        
        os.path.join(BASE_PATH, "InputFiles/2"):
        {
        'SMTPTOADDRESS': ['usert@localhost',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':True
        },
        
        os.path.join(BASE_PATH, "InputFiles/3"):
        {
        'SMTPTOADDRESS': ['usert@localhost',],
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


