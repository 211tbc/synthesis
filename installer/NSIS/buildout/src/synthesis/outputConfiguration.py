#!/usr/bin/env python

# Adding a vendor.  Simply append a record by following the format below.

Configuration = \
{
    '1234':
        {
            'vendor': 'Orlando Shelter Society',
            'outputFormat': 'svcpoint',
            'destinationURL': 'user@domain.us',
            'transportConfiguration': 'email'
        },
    '5678':
        {
            'vendor': 'Pinellas',
            'outputFormat': 'svcpoint',
            'destinationURL': 'crusty.penguix.net',
            'transportConfiguration': 'sftp',
            'username': 'user',
            'password': 'password#'
        },
    '91011':
        {
            'vendor': 'Cleveland Housing Authority',
            'outputFormat': 'svcpoint',
            'destinationURL': '192.168.0.208',
            'transportConfiguration': 'sftp',
            'username': 'user',
            'password': 'password#'
        }
}

