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
    '9101112':
        {
            'outputFormat': 'svcpoint',
            'destinationURL': 'crusty.penguix.net',
            'transportConfiguration': 'vpnftp',
            'username': 'scottben',
            'password': 'nx9353#',
            'outputpath': 'xmlFiles',
            'owner': '',
            'chmod': '',
            'group': ''
        }

}

