import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import urllib2
import base64
from Encryption import *
import conf.settings


tbc = open('/home/synthesis/py3_tbc/synthesis/synthesis/ws_input_files/received_data_2020-05-09_21:59:09.570788_encrypted.xml', 'r')
    

#tbc = open('tmp/wellsky.xml', 'r')
xml = tbc.read()
tbc.close()

gpg = GPG()
encrypted_xml = xml
#xml = base64.b64encode(encrypted_xml)
xml = encrypted_xml
xml_payload="""--98f3d0e0-8336-489b-b815-a48da207a689
Content-Disposition: attachment; name="003"; filename="newtest.xml"
Content-Type: text/xml

%s""" % (xml, )

use_apache = False

headers = {"Content-Type": "multipart/form-data; boundary=98f3d0e0-8336-489b-b815-a48da207a689", "User-Agent": "synthesis"}

if use_apache:
    req = urllib2.Request('https://50.116.39.44:8023/docs', xml_payload, headers)
    import ssl
    context = hasattr(ssl,'_create_unverified_context') and ssl._create_unverified_context() or None
    #import pdb; pdb.set_trace()
    resp = urllib2.urlopen(req, context=context)
else:
    req = urllib2.Request('http://0.0.0.0:5001/docs', xml_payload, headers)
    #import pdb; pdb.set_trace()
    resp = urllib2.urlopen(req)

import pprint
pprint.pprint([(attr, value) for attr, value in resp.__dict__.iteritems()])
