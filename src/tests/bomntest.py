import urllib2
import base64
from Encryption import *
import conf.settings

tbc = open('/home/eric/workspace/tbc/synthesis/synthesis/test_files/bowman.xml', 'r')
xml = tbc.read()
tbc.close()

gpg = GPG()
encrypted_xml = gpg.encrypt(xml)
encoded_xml = base64.b64encode(encrypted_xml)

data="""--98f3d0e0-8336-489b-b815-a48da207a689
Content-Disposition: attachment; name="bowmantest"; filename="bowmantest.xml"
Content-Type: text/xml

%s""" % (encoded_xml, )

hs = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(hs)
urllib2.install_opener(opener)
request = urllib2.Request('http://127.0.0.1:5000/docs')
request.add_header("Content-Type", "multipart/form-data; boundary=98f3d0e0-8336-489b-b815-a48da207a689")
request.add_header("User-Agent", "synthesis")
request.add_data(data)
print urllib2.urlopen(request).read()
