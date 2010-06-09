#!/usr/bin/env python

# Adding a vendor.  Simply append a record by following the format below.

'''
Here is sample of the fields that need to be defined for each particular transport method

Email:

    'outputFormat': 'svcpoint',
    'destinationURL': 'scottt@localhost',
    'transportConfiguration': 'email'

SFTP:

    'outputFormat': 'svcpoint',
    'destinationURL': 'scottt@localhost',
    'transportConfiguration': 'sftp',
    'username': 'scottt',
    'password': 'xxxxxx',
    'outputpath': 'xmlpath',
    'owner': '',
    'chmod': '',
    'group': ''

VPNFTP


VPNCP
    
'''

Configuration = \
{
    '1234':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': 'scottt@localhost',
            'transportConfiguration': 'email'
        },
    '1313':
        {
            'outputFormat': 'hmiscsv',
            'destinationURL': 'scottt@localhost',
            'transportConfiguration': 'email'
        },
    '5678':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': 'localhost',
            'transportConfiguration': 'sftp',
            'username': 'scottt',
            'password': 'xxxxxx',
            'outputpath': 'xmlFiles',
            'owner': '',
            'chmod': '',
            'group': ''
        },
    '9101112':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': 'scottt@localhost',
            'transportConfiguration': 'vpnftp',
            'username': 'scottt',
            'password': 'xxxxxx',
            'outputpath': 'xmlFiles',
            'owner': '',
            'chmod': '',
            'group': ''
        }

}

