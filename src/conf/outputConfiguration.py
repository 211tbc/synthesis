'''see ./docs/output_configurations.readme for information on setting these configurations'''
#!/usr/bin/env python
import os
import settings

# 3DES
KEY_PATH = '' # full directory path to the 3DES key file
IV_PATH = '' # full directory path to the 3DES IV file

PROCESSEDFILES_PATH = os.path.join(settings.BASE_PATH, "processed_files")
if not os.path.exists(PROCESSEDFILES_PATH):
    os.mkdir(PROCESSEDFILES_PATH)

# Adding a vendor.  Simply append a record by following the sample format below.

Configuration = \
{
    # Sample Format
    'Source ID (e.g. 001)':
        {
            'vendor': '',
            'outputFormat': '', # Possible values: 
            'destinationURL': '',
            'transportConfiguration': 'save', # Possible values: "save" (to directory), "soap", "rest", "ftps", "sftp"
            'encryption': 'none', # Possible values: "none", "3des", "openpgp"
            # when transportConfiguration is set to "save", set destination to the absolute path of the save directory
            'destination': settings.BASE_PATH + '/output_files',
            # frequency controls how often nodebuilder runs and can be set to "asap" (later on maybe "daily", "weekly", monthly")
            'frequency': 'asap'
        },
    'occtest':#For HUD files in test_files folder
        {
            'vendor': 'OCC',
            'outputFormat': 'svcpoint5',
            'destinationURL': 'https://pix.penguix.net:8023/docs',
            #'destinationURL': 'http://127.0.0.1:5000/docs',
            'transportConfiguration': 'save',
            'encryption': '3des',
            'destination': settings.BASE_PATH + '/occ_output_files',
            'frequency': 'asap'
        },
    'tbctest':#For HUD files in test_files folder
        {
            'vendor': 'TBC',
            'outputFormat': 'pseudo',
            'destinationURL': 'https://pix.penguix.net:8024/docs',
            'transportConfiguration': 'save',
            'encryption': 'none',
            'destination': settings.BASE_PATH + '/tbc_output_files',
            'frequency': 'asap'
        },
    '003':#For HUD files in test_files folder
        {
            'vendor': 'Orange County Corrections',
            'outputFormat': 'svcpoint5',
            'destinationURL': 'http://fby.homeip.net:8092/docs',
            'transportConfiguration': 'save',
            'encryption': 'none',
            'destination': settings.BASE_PATH + '/output_files',
            'frequency': 'asap'
        },
    '334380997':#For HUD files in test_files folder
        {
            'vendor': 'Vendor Name',
            'outputFormat': 'svcpoint5',
            'destinationURL': 'localhost',
            'transportConfiguration': 'save',
            'encryption': 'none',
            'destination': settings.BASE_PATH + '/output_files',
            'frequency': 'asap'
        },
    'iH9HiPbW40JbS5m_':#For HUD files in test_files folder
        {
            'vendor': 'Vendor Name',
            'outputFormat': 'svcpoint5',
            'destinationURL': 'localhost',
            'transportConfiguration': 'save',
            'encryption': 'none',
            'destination': settings.BASE_PATH + '/output_files',
            'frequency': 'asap'
        },
    'hl7CCD':  # Project Health Level 7 Continuity of Care Document
        {
            'vendor': 'HL7',
            'outputFormat': 'hl7ccd',
            'destinationURL': 'localhost',
            'transportConfiguration': 'save',
            'encryption': 'openpgp',
            'destination': settings.BASE_PATH + '/output_files',
            'frequency': 'asap'
        },
    '7777':#Project Synthesis Phase 3 for Orlando
        {
            'vendor': 'BIS',
            'outputFormat': 'svcpoint5',#the new servicepoint format
            'destinationURL': 'localhost',
            'transportConfiguration': '', #we're just going to save this outputted XML file to a local drive
            'encryption': 'none', # should be 3DES for production for Orlando OCC
            'destination': settings.BASE_PATH + '/output_files',    # (I get an error if I leave the value blank)
            'frequency': 'asap'
        },
    '8888':
        {
            'vendor': 'System Operator',
            'outputFormat': 'hmiscsv',
            'destinationURL': 'localhost',
            'transportConfiguration': ''
        },
    '9999':
        {
            'vendor': 'System Operator',
            'outputFormat': 'hmisxml',
            'destinationURL': 'localhost',
            'transportConfiguration': 'sys.stdout'
        },
    '1234':
        {
            'vendor': 'Some Vendor Name',
            'outputFormat': 'svcpoint',
            'destinationURL': 'someone@somewhere.net',
            'transportConfiguration': 'email'
        },
    '5678':
        {
            'vendor': 'Some Vendor Name2',
            'outputFormat': 'svcpoint',
            'destinationURL': 'subdomain.domain.net',
            'transportConfiguration': 'sftp',
            'username': 'someuser',
            'password': 'somepassword'
        },
    '91011':
        {
            'vendor': 'Some Vendor Name3',
            'outputFormat': 'svcpoint',
            'destinationURL': '192.168.0.208',
            'transportConfiguration': 'sftp',
            'username': 'someuser2',
            'password': 'somepassword2'
        }, 
     '1313': 
        { 
             'outputFormat': 'hmiscsv', 
             'destinationURL': 'user@localhost', 
             'transportConfiguration': 'email' 
        },
}

#############################################################
# Testing|Production variables for the soaptrasnport module #
#############################################################
# Uncomment this line if you are testing with Netsmart
# No referrals will actually go to the providers, 
#   which will make them happy during testing
SystemUserId = "69470500-66A2-4841-931A-23D226FBC937"
    
#Uncomment this line if you are communicating with Netsmart Production
#SystemUserId = "2A5B7129-6A70-473B-995F-B0A459A4E5C6"


#old Suncoast Production
#SuncoastReceivingProviderId = "29F2951F-7F47-451D-AED8-5729F29347D5"
#Suncoast Production
#SuncoastReceivingProviderId= "3634CE56-C001-4CF5-9620-A2E3BAC128AF"
#Suncoast Test
SuncoastReceivingProviderId= "8754B0BB-CC45-465E-9F97-1A9D2F5FE058"


#old PEMHS production
#PEMHSReceivingProviderId= "3DDFF107-0AD2-4728-8EC6-6305D0F0479D"
#PEMHS Production
#PEMHSReceivingProviderId= "D76C72B3-8DFA-4240-96CC-328B985BB4EA"
#PEMHS Test
PEMHSReceivingProviderId= "D22D0095-FD2E-4011-BEA4-4479AE92C414"

