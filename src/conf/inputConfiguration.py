#!/usr/bin/env python
import os
import settings

USE_ENCRYPTION = False
#USE_ENCRYPTION = True

# 3DES
KEY_PATH = '' # full directory path to the 3DES key file
IV_PATH = '' # full directory path to the 3DES IV file

FAILEDFILES_PATH = os.path.join(settings.BASE_PATH, "failed_files")
if not os.path.exists(FAILEDFILES_PATH):
    os.mkdir(FAILEDFILES_PATH)

USEDFILES_PATH = os.path.join(settings.BASE_PATH, "used_files")
if not os.path.exists(USEDFILES_PATH):
    os.mkdir(USEDFILES_PATH)
    
# Input files Processing path
# New 'Customers' input file path must be put into this 'list'.  Add it to the list mechanism.  
INPUTFILES_PATH = [
            settings.BASE_PATH + "/input_files"
            ,
            ]
for input_path in INPUTFILES_PATH:
    if not os.path.exists(input_path):
        os.mkdir(input_path)

WEB_SERVICE_INPUTFILES_PATH = [
            settings.BASE_PATH + "/ws_input_files"
            ,
            ]
for wsinput_path in WEB_SERVICE_INPUTFILES_PATH:
    if not os.path.exists(wsinput_path):
        os.mkdir(wsinput_path)

# SMTP Mail recipients is a dictionary that must be defined for each source of input files
SMTPRECIPIENTS = {    
    # input processing
    "testSource":
        {
        'VENDOR_NAME': 'SomeVendor',
        'SMTPTOADDRESS': ['someone@somedomain.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        }
    # input processing
    ,"/home/your_username_here/myrestservice/synthesis/synthesis/input_files":
        {
        'VENDOR_NAME': 'SomeVendor',
        'SMTPTOADDRESS': ['someone@somedomain.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        }
    ,"/home/your_username_here/synthesis/synthesis/input_files2":
        {
        'VENDOR_NAME': 'SomeVendor2',
        'SMTPTOADDRESS': ['admin@superhost.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        }
    ,"/home/your_username_here/synthesis/synthesis/input_files3":
        {
        'VENDOR_NAME': '',
        'SMTPTOADDRESS': ['sammy.davis@jr.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        }
    # output processing
    ,"/home/your_username_here/synthesis/synthesis/output_files":
        {
        'VENDOR_NAME': '',
        'SMTPTOADDRESS': ['user@host.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        }
    ,"/home/your_username_here/synthesis/synthesis/output_files2":
        {
        'VENDOR_NAME': '',
        'SMTPTOADDRESS': ['admin@somehost.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
        'FINGERPRINT':'',
        'USES_ENCRYPTION':False
        }
    }
