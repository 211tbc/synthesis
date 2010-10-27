'''see ./docs/output_configurations.readme for information on setting these configurations'''
#!/usr/bin/env python

# Adding a vendor.  Simply append a record by following the format below.

Configuration = \
{
    '8888':
        {
            'vendor': 'System Operator',
            'outputFormat': 'hmisxml30',
            'destinationURL': 'localhost',
            'transportConfiguration': ''
        },
    '9999':
        {
            'vendor': 'System Operator',
            'outputFormat': 'hmiscsv30',
            'destinationURL': 'localhost',
            'transportConfiguration': 'sys.stdout'
        },
    '7777':
        {
            'vendor': 'System Operator',
            'outputFormat': 'hmisxml28',
            'destinationURL': 'localhost',
            'transportConfiguration': 'sys.stdout'
        },
    '1234':
        {
            'vendor': 'Some Vendor Name',
            'outputFormat': 'svcpoint406',
            'destinationURL': 'someone@somewhere.net',
            'transportConfiguration': 'email'
        },
    '5678':
        {
            'vendor': 'Some Vendor Name2',
            'outputFormat': 'svcpoint20',
            'destinationURL': 'subdomain.domain.net',
            'transportConfiguration': 'sftp',
            'username': 'someuser',
            'password': 'somepassword'
        },
    '91011':
        {
            'vendor': 'Some Vendor Name3',
            'outputFormat': 'svcpoint406',
            'destinationURL': '192.168.0.208',
            'transportConfiguration': 'sftp',
            'username': 'someuser2',
            'password': 'somepassword2'
        }, 
     '1313': 
        { 
             'outputFormat': 'hmiscsv30', 
             'destinationURL': 'user@localhost', 
             'transportConfiguration': 'email' 
        },
}

