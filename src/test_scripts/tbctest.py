import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import urllib2
#import base64
#from Encryption import *
import conf.settings
tbc = open('test_files/bowman_test_3.xml', 'r')
xml = tbc.read()
tbc.close()
#gpg = GPG()
#encrypted_xml = gpg.encrypt(xml)
#encoded_xml = base64.b64encode(encrypted_xml)
xml_payload="""--98f3d0e0-8336-489b-b815-a48da207a689
Content-Disposition: attachment; name="003"; filename="tbctest.xml"
Content-Type: text/xml

%s""" % (xml, )
headers = {"Content-Type": "multipart/form-data; boundary=98f3d0e0-8336-489b-b815-a48da207a689", "User-Agent": "synthesis"}
req = urllib2.Request('http://0.0.0.0:5001/docs', xml_payload, headers)
resp = urllib2.urlopen(req)
import pprint
pprint.pprint([(attr, value) for attr, value in resp.__dict__.iteritems()])
