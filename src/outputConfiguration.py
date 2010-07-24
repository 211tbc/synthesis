#!/usr/bin/env python

# Adding a vendor.  Simply append a record by following the format below.

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
        }
}

