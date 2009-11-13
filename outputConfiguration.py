#!/usr/bin/env python

# Adding a vendor.  Simply append a record by following the format below.

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
            'destinationURL': 'crusty.penguix.net',
            'transportConfiguration': 'sftp',
            'username': 'scottben',
            'password': 'nx9353#'
        }

}

