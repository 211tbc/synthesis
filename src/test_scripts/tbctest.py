import pprint
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import urllib.request
import base64
from Encryption import *
import conf.settings
tbc = open('test_files/unitest.xml', 'r')
xml = tbc.read()
tbc.close()
gpg = GPG()
encrypted_xml = gpg.encrypt(xml)
encoded_xml = base64.b64encode(encrypted_xml.encode())
xml_payload=b"""--98f3d0e0-8336-489b-b815-a48da207a689
Content-Disposition: attachment; name="003"; filename="newtest.xml"
Content-Type: text/xml

%s""" % (encoded_xml, )

headers = {"Content-Type": "multipart/form-data; boundary=98f3d0e0-8336-489b-b815-a48da207a689", "User-Agent": "synthesis"}
req = urllib.request.Request('http://0.0.0.0:6543/docs', xml_payload, headers)
resp = urllib.request.urlopen(req)
pprint.pprint(resp.__dict__)
