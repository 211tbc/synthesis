import urllib2
import base64
from Encryption import *
import conf.settings

tbc = open('test_files/bad_bowman6.xml', 'r')
xml = tbc.read()
tbc.close()
gpg = GPG()
encrypted_xml = gpg.encrypt(xml)
encoded_xml = base64.b64encode(encrypted_xml)

data="""--98f3d0e0-8336-489b-b815-a48da207a689
Content-Disposition: attachment; name="tbctest"; filename="tbctest.xml"
Content-Type: text/xml

%s""" % (encoded_xml, )
hs = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(hs)
urllib2.install_opener(opener)
#request = urllib2.Request('https://pix.penguix.net:8025/docs')
request = urllib2.Request('http://127.0.0.1:5001/docs')
request.add_header("Content-Type", "multipart/form-data; boundary=98f3d0e0-8336-489b-b815-a48da207a689")
request.add_header("User-Agent", "synthesis")
request.add_data(data)
print urllib2.urlopen(request).read()
