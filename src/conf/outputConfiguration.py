#!/usr/bin/env python

# Adding a vendor.  Simply append a record by following the format below.

'''
Here is sample of the fields that need to be defined for each particular transport method

Email:

    'outputFormat': 'svcpoint',
    'destinationURL': 'scott@benninghoff.us',
    'transportConfiguration': 'email'

SFTP:

    'outputFormat': 'svcpoint',
    'destinationURL': 'crusty.penguix.net',
    'transportConfiguration': 'sftp',
    'username': 'scottben',
    'password': 'nx9353#',
    'outputpath': 'xmlpath',
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
            'destinationURL': 'scott@benninghoff.us',
            'transportConfiguration': 'email'
        },
    '5678':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': '192.168.0.208',
            'transportConfiguration': 'sftp',
            'username': 'scottben',
            'password': 'nx9353',
            'outputpath': 'xmlFiles',
            'owner': '',
            'chmod': '',
            'group': ''
        },
    '3':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': 'baisix.servicept.com',
            'transportConfiguration': 'vpnftp',
            'username': '',
            'password': '',
            'outputpath': 'xmlFiles',
            'owner': '',
            'chmod': '',
            'group': ''
        }

}

