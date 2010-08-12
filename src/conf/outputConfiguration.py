#!/usr/bin/env python

# Adding a vendor.  Simply append a record by following the format below.

'''
Here is sample of the fields that need to be defined for each particular transport method

Email:

    'outputFormat': 'svcpoint',
    'destinationURL': 'user@somehost.com',
    'transportConfiguration': 'email'

SFTP:

    'outputFormat': 'svcpoint',
    'destinationURL': 'subdomain.domain.suffix',
    'transportConfiguration': 'sftp',
    'username': 'someuser',
    'password': 'somepassword',
    'outputpath': 'outputted/xml/path',
    'owner': '',
    'chmod': '',
    'group': ''

VPNFTP


VPNCP


    
'''

Configuration = \
{
    '8888':
        {
            'vendor': 'System Operator',
            'outputFormat': 'svcpoint',
            'destinationURL': 'localhost',
            'transportConfiguration': ''
        },
    '9999':
        {
            'vendor': 'System Operator',
            'outputFormat': 'svcpoint',
            'destinationURL': 'localhost',
            'transportConfiguration': 'sys.stdout'
        },
    '1234':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': 'user@host.com',
            'transportConfiguration': 'email'
        },
    '5678':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': '192.168.0.208',
            'transportConfiguration': 'sftp',
            'username': 'someuser',
            'password': 'somepassword',
            'outputpath': 'xmlFiles',
            'owner': '',
            'chmod': '',
            'group': ''
        },
    '3':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': 'subdomain.domain.suffix',
            'transportConfiguration': 'vpnftp',
            'username': '',
            'password': '',
            'outputpath': 'xmlFiles',
            'owner': '',
            'chmod': '',
            'group': ''
        }

}

