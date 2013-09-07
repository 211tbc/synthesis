import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import urllib2
import base64
from Encryption import *
import conf.settings
occ = open('test_files/HUD_HMIS_OCC.xml', 'r')
xml = occ.read()
occ.close()
keyiv = get_incoming_3des_key_iv()
dess = DES3()
encrypted_xml = dess.encrypt(xml, keyiv['key'], iv=keyiv['iv'])
encoded_xml = base64.b64encode(encrypted_xml)
xml_payload="""--98f3d0e0-8336-489b-b815-a48da207a689
Content-Disposition: attachment; name="occtest"; filename="occtest.xml"
Content-Type: text/xml

%s""" % (encoded_xml, )
headers = {"Content-Type": "multipart/form-data; boundary=98f3d0e0-8336-489b-b815-a48da207a689", "User-Agent": "synthesis"}
req = urllib2.Request('http://0.0.0.0:6543/docs', xml_payload, headers)
resp = urllib2.urlopen(req)
