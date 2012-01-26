'''see ./docs/output_configurations.readme for information on setting these configurations'''
#!/usr/bin/env python

import settings

# Adding a vendor.  Simply append a record by following the format below.

Configuration = \
{
    'occtest':#For HUD files in test_files folder
        {
            'vendor': 'OCC',
            'outputFormat': 'svcpoint5',
            'destinationURL': 'https://pix.penguix.net:8023/docs',
            #'destinationURL': 'http://127.0.0.1:5000/docs',
            # transport type can be set to "save" (to directory), "soap", "rest", "ftps", "sftp"
            'transportConfiguration': 'save',
            # encryption type can be set to "none", "openpgp", "3des"
            'encryption': '3des',
            # when transportConfiguration is set to "save", set destination to the absolute path of the save directory
            'destination': settings.BASE_PATH + '/occ_output_files',
            # frequency controls how often nodebuilder runs and can be set to "asap" (later on maybe "daily", "weekly", monthly")
            'frequency': 'asap'
        },
    'tbctest':#For HUD files in test_files folder
        {
            'vendor': 'TBC',
            'outputFormat': 'pseudo',
            'destinationURL': 'https://pix.penguix.net:8024/docs',
            #'destinationURL': 'http://127.0.0.1:5001/docs',
            # transport type can be set to "save" (to directory), "soap", "rest", "ftps", "sftp"
            'transportConfiguration': 'save',
            # encryption type can be set to "none", "openpgp", "3des"
            'encryption': 'none',
            # when transportConfiguration is set to "save", set destination to the absolute path of the save directory
            'destination': settings.BASE_PATH + '/tbc_output_files',
            # frequency controls how often nodebuilder runs and can be set to "asap" (later on maybe "daily", "weekly", monthly")
            'frequency': 'asap'
        },
    '003':#For HUD files in test_files folder
        {
            'vendor': 'Orange County Corrections',
            'outputFormat': 'svcpoint5',
            #'destinationURL': 'https://pix.penguix.net:8024/docs',
            'destinationURL': 'http://fby.homeip.net:8092/docs',
            #'destinationURL': 'http://127.0.0.1:5000/docs',
            # transport type can be set to "save" (to directory), "soap", "rest", "ftps", "sftp"
            'transportConfiguration': 'save',
            # encryption type can be set to "none", "openpgp", "3des"
            'encryption': 'none',
            # when transportConfiguration is set to "save", set destination to the absolute path of the save directory
            'destination': settings.OUTPUTFILES_PATH,
            # frequency controls how often nodebuilder runs and can be set to "asap" (later on maybe "daily", "weekly", monthly")
            'frequency': 'asap'
        },
    '334380997':#For HUD files in test_files folder
        {
            'vendor': 'Vendor Name',
            'outputFormat': 'svcpoint5',
            'destinationURL': 'localhost',
            'transportConfiguration': 'save',
            'encryption': 'none',
            'destination': '',
            'frequency': 'asap'
        },
    'iH9HiPbW40JbS5m_':#For HUD files in test_files folder
        {
            'vendor': 'Vendor Name',
            'outputFormat': 'svcpoint5',
            'destinationURL': 'localhost',
            'transportConfiguration': 'save',
            'encryption': 'none',
            'destination': '',
            'frequency': 'asap'
        },
    '7777':#Project Synthesis Phase 3 for Orlando
        {
            'vendor': 'BIS',
            'outputFormat': 'svcpoint5',#the new servicepoint format
            'destinationURL': 'localhost',
            'transportConfiguration': '', #we're just going to save this outputted XML file to a local drive
            'encryption': 'none', # should be 3DES for production for Orlando OCC
            'destination': settings.OUTPUTFILES_PATH,    # (I get an error if I leave the value blank)
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

