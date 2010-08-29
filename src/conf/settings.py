#!/usr/bin/env python
import os
# Settings for synthesis.py

# current Min Python version is 2.4
MINPYVERSION = '2.4'

MODE = 'TEST'                               # This is the switch that runs the program in 'TEST' or 'PROD' Mode. 

#The GUI setting determines in Filehandler() will use a GUI controller to start and stop the service.  
#In practical terms, this is determined by whether Windows is running or Unix, since the GUI was built for Windows 
#However, the gui is cross-platform, so the GUI setting should be actually independent of the platform
GUI = False  
# DB settings:
DB_DATABASE = "synthesis"
DB_USER = "user_name_here"
DB_PASSWD = "password"
DB_PORT = 5432
DB_HOST = "localhost"

# Which SvcPt version is this site using, if any?  This version number pulls the xsd schema in and configures the plug in as well.
SVCPT_VERSION = '406'                    # this is 4.06
# uses current working directory, uncomment the line if the output path needs to be elsewhere.
BASE_PATH = os.getcwd()
#BASE_PATH = ""

PATH_TO_GPG = '/usr/bin/gpg'
PGPHOMEDIR = ''
PASSPHRASE = ''

# Input files Processing path
# New 'Customers' input file path must be put into this 'list'.  Add it to the list mechanism.  
INPUTFILES_PATH = [
            "/home/user_name_here/workspace/synthesis/installer/build/InputFiles"
            ,
            ]

# subfolder 
XSD_PATH = "xsd"

# file path subdirectories
OUTPUTFILES_PATH = os.path.join(BASE_PATH, "OutputFiles")
if not os.path.exists(OUTPUTFILES_PATH):
    os.mkdir(OUTPUTFILES_PATH)
    
USEDFILES_PATH = os.path.join(BASE_PATH, "UsedFiles")
if not os.path.exists(USEDFILES_PATH):
    os.mkdir(USEDFILES_PATH)
    
FAILEDFILES_PATH = os.path.join(BASE_PATH, "FailedFiles")
if not os.path.exists(FAILEDFILES_PATH):
    os.mkdir(FAILEDFILES_PATH)
    
LOGS = os.path.join(BASE_PATH, "logs")
if not os.path.exists(LOGS):
    os.mkdir(LOGS)

PROCESSED_PATH = ""

#ECJ20100829 using the HMISXML_version setting is deprecated, because selector.py now can tell between 2.8 and 3.0 through validation tests.  ServicePoint XML should work the same in the future
SCHEMA_DOCS = {
'hud_hmis_xml_2_8':os.path.join(BASE_PATH, XSD_PATH, 'versions','HMISXML','28','HUD_HMIS.xsd'),               
'hud_hmis_xml_3_0':os.path.join(BASE_PATH, XSD_PATH, 'versions','HMISXML','30','HUD_HMIS.xsd'),
'svcpoint_2_0_xml':os.path.join(BASE_PATH, XSD_PATH, 'versions','SVCPT', SVCPT_VERSION, 'sp.xsd'),    # Service Point current version (output)
'jfcs_service_xml':os.path.join(BASE_PATH, XSD_PATH, 'JFCS_SERVICE.xsd'),
'jfcs_client_xml':os.path.join(BASE_PATH, XSD_PATH, 'JFCS_CLIENT.xsd'),
'operation_par_xml':os.path.join(BASE_PATH, XSD_PATH, 'Operation_PAR_Extend_HUD_HMIS_2_8.xsd')
               }

DEBUG = True									# Debug the application layer
DEBUG_ALCHEMY = False							# Debug the ORM Layer
DEBUG_DB = False								# Debug the DB layer of the applicHMIation

# This mechanism provides an override to the settings above.  create a file called local_settings.py and simply
# override the values like BASE_PATH='/home/mypath'.  Then import like this: from conf import settings
# this will bring in all of settings.py's values and have the overriddin values of local_settings.py

# email configuration
SMTPSERVER = 'localhost'
SMTPPORT = 25
SMTPSENDER = 'me@localhost'
SMTPSENDERPWD = 'mysecret'

# SMTP Mail recipients is a dictionary that must be defined for each source of input files
SMTPRECIPIENTS =	{
     "/home/user_name_here/workspace/synthesis/installer/build/InputFiles":
		{
        'VENDOR_NAME': 'SomeVendor',
		'SMTPTOADDRESS': ['someone@somedomain.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': [],
		'FINGERPRINT':'',
		'USES_ENCRYPTION':False
		}
	,"~/workspace/synthesis/installer/build/InputFiles2":
		{
        'VENDOR_NAME': 'SomeVendor2',
		'SMTPTOADDRESS': ['admin@superhost.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': [],
		'FINGERPRINT':'',
		'USES_ENCRYPTION':True
		}
	,"~/workspace/synthesis/installer/build/InputFiles3":
		{
		'VENDOR_NAME': '',
        'SMTPTOADDRESS': ['sammy.davis@jr.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': [],
		'FINGERPRINT':'',
		'USES_ENCRYPTION':False
		}
# output processing
    ,"~/workspace/synthesis/installer/build/OutputFiles":
		{
		'VENDOR_NAME': '',
        'SMTPTOADDRESS': ['user@host.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': [],
		'FINGERPRINT':'',
		'USES_ENCRYPTION':False
		}
    ,"~/workspace/synthesis/installer/build/OutputFiles2":
		{
		'VENDOR_NAME': '',
        'SMTPTOADDRESS': ['admin@somehost.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': [],
		'FINGERPRINT':'',
		'USES_ENCRYPTION':True
		}
	}

try:
	from local_settings import *
except ImportError:
	pass


