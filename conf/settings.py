#!/usr/bin/env python
import os
# Settings for synthesis.py

MODE = 'PROD'                               # This is the switch that runs the program in Test Mode.

# DB settings:
DB_DATABASE = ""
DB_USER = ""
DB_PASSWD = ""
DB_PORT = 5432

# uses current working directory, uncomment the line if the output path needs to be elsewhere.
BASE_PATH = os.getcwd()
#BASE_PATH = ""

PATH_TO_GPG = '/usr/bin/gpg'
PGPHOMEDIR = ''
PASSPHRASE = ''

# Input files Processing path
# New 'Customers' input file path must be put into this 'list'.  Add it to the list mechanism.  
INPUTFILES_PATH = [
            "/home/path/goes/here"
            ,"/usr/inputfiles"
            ,"/dir/encryptedpath/here"
            ]

# subfolder 
XSD_PATH = "xsd"

# file path subdirectories
OUTPUTFILES_PATH = "OutputFiles"
USEDFILES = os.path.join(BASE_PATH, "Used")
FAILEDFILES = os.path.join(BASE_PATH, "Failed")
LOGS = os.path.join(BASE_PATH, "logs")

PROCESSED_PATH = ""

SCHEMA_DOCS = {'hud_hmis_2_8_xml':os.path.join(BASE_PATH, XSD_PATH, 'HUD_HMIS_2_8.xsd')}

DEBUG = False									# Debug the application layer
DEBUG_ALCHEMY = False							# Debug the ORM Layer
DEBUG_DB = False								# Debug the DB layer of the application

# This mechanism provides an override to the settings above.  create a file called local_settings.py and simply
# override the values like BASE_PATH='/home/mypath'.  Then import like this: from conf import settings
# this will bring in all of settings.py's values and have the overriddin values of local_settings.py

# email configuration
SMTPSERVER = 'localhost'
SMTPPORT = 25
SMTPSENDER = 'me@localhost'
SMTPSENDERPWD = 'mysecret'

# SMTP Mail recipients is a dictionary that must be defined for each source of input files
SMTPRECIPIENTS = \
	{
	"/home/scottben/Documents/Development/AlexandriaConsulting/repos/trunk/synthesis/InputFiles":
		{
		'SMTPTOADDRESS': ['email@domain.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': [],
		'FINGERPRINT':'',
		'USES_ENCRYPTION':True
		}
	,"/home/scottben/Documents/Development/AlexandriaConsulting/repos/trunk/synthesis/InputFiles2":
		{
		'SMTPTOADDRESS': ['admin@superhost.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': [],
		'FINGERPRINT':'',
		'USES_ENCRYPTION':True
		}
	,"/home/scottben/Documents/Development/AlexandriaConsulting/repos/trunk/synthesis/InputFiles3":
		{
		'SMTPTOADDRESS': ['sammy.davis@jr.com',],
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


