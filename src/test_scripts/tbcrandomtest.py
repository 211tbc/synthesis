import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import urllib2
import base64
from Encryption import *
import conf.settings
import random
import time

xml_template = """<ext:Sources xmlns:airs="http://www.hudhdx.info/Resources/Vendors/3_0/AIRS_3_0_mod.xsd" xmlns:ext="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd" xmlns:hmis="http://www.hudhdx.info/Resources/Vendors/3_0/HUD_HMIS.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd" ext:version="3.0">
    <ext:Source>
        <ext:SourceID>
                <hmis:IDStr>%s</hmis:IDStr>
        </ext:SourceID>
        <ext:SoftwareVendor>Vendor Name Here</ext:SoftwareVendor>
        <ext:SoftwareVersion>7.1</ext:SoftwareVersion>
        <ext:SourceName>Source Name Here</ext:SourceName>
        <ext:Export>
            <ext:ExportID>
                <!-- For now, this value is computed as str(int(time.time())) which should be enough to guarantee uniqueness. -->
                    <hmis:IDNum>%s</hmis:IDNum>
            </ext:ExportID>
            <ext:ExportDate>2011-09-23T18:51:58</ext:ExportDate>
            <ext:ExportPeriod>
                <!-- This is an example for the month of June. -->                
                <hmis:StartDate>2011-09-01T00:00:00</hmis:StartDate>
                <hmis:EndDate>2011-09-02T23:59:59</hmis:EndDate>
            </ext:ExportPeriod>
            <ext:Person>
                <ext:PersonID>
                    <hmis:IDNum>%s</hmis:IDNum>
                </ext:PersonID>
                <ext:DateOfBirth>
                        <hmis:Unhashed hmis:dateCollected="2011-05-27T18:51:58">1984-04-21</hmis:Unhashed>
                    <hmis:DateOfBirthType hmis:dateCollected="2011-05-27T18:51:58">1</hmis:DateOfBirthType>
                </ext:DateOfBirth>
                <ext:Ethnicity>
                    <hmis:Unhashed hmis:dateCollected="2011-06-25T18:51:58">1</hmis:Unhashed>
                </ext:Ethnicity>
                <ext:Gender>
                    <hmis:Unhashed hmis:dateCollected="2011-06-25T18:51:58">2</hmis:Unhashed>
                </ext:Gender>
                <ext:LegalFirstName>
                    <hmis:Unhashed hmis:dateCollected="2011-01-27T18:51:58">Green</hmis:Unhashed>
                </ext:LegalFirstName>
                <ext:LegalLastName>
                    <hmis:Unhashed hmis:dateCollected="2011-03-05T18:51:58">Test</hmis:Unhashed>
                </ext:LegalLastName>
                <ext:LegalMiddleName>
                    <hmis:Unhashed hmis:dateCollected="2011-03-05T18:51:58">Box</hmis:Unhashed>
                </ext:LegalMiddleName>
                <!--Here is a standalone need referenced by a referral-->                
                <ext:Need>
                    <hmis:NeedID>
                        <hmis:IDNum>345</hmis:IDNum>
                    </hmis:NeedID>
                    <hmis:SiteServiceID>1766</hmis:SiteServiceID>
                    <hmis:NeedStatus>1</hmis:NeedStatus>
                    <hmis:Taxonomy>
                        <airs:Code>789.987</airs:Code>
                    </hmis:Taxonomy>
                </ext:Need>
                <ext:PersonHistorical>
                    <hmis:PersonHistoricalID>
                        <hmis:IDNum>12345</hmis:IDNum>
                    </hmis:PersonHistoricalID>
                    <hmis:PersonPhoneNumber hmis:dateCollected="2009-11-30T18:51:58">%s</hmis:PersonPhoneNumber>
                </ext:PersonHistorical>
                <ext:Race>
                    <hmis:Unhashed hmis:dateCollected="2009-11-30T18:51:58">2</hmis:Unhashed>
                </ext:Race>
                <ext:ServiceEvent>
                    <ext:ServiceEventID>
                        <hmis:IDNum>11111</hmis:IDNum>
                    </ext:ServiceEventID>
                    <ext:SiteServiceID>1766</ext:SiteServiceID>
                    <ext:IsReferral>1</ext:IsReferral>
                    <ext:Referrals>
                        <!--Two referrals to the same agency-->
                        <ext:Referral>
                            <ext:ReferralID>
                                <hmis:IDNum>12345</hmis:IDNum>
                            </ext:ReferralID>
                            <!--Extension element -->
                            <ext:AgencyReferredToID>
                                <hmis:IDNum>8169</hmis:IDNum>
                            </ext:AgencyReferredToID>
                            <!--Extension element -->
                            <ext:AgencyReferredToName hmis:dateCollected="2009-11-30T18:51:58">Suncoast Center, Inc.</ext:AgencyReferredToName>
                            <!--Refers to a standalone need--> 
                            <ext:NeedID>
                                 <hmis:IDNum>345</hmis:IDNum>
                            </ext:NeedID>
                        </ext:Referral>
                    </ext:Referrals>
                    <ext:ServiceEventProvisionDate>2011-09-01</ext:ServiceEventProvisionDate>
                    <ext:ServiceEventNotes>
                        <hmis:note>
                            <hmis:NoteID>
                                <hmis:IDNum>123456</hmis:IDNum>
                            </hmis:NoteID>
                            <hmis:NoteText hmis:dateCollected="2011-09-01T18:51:58" hmis:dateEffective="2011-09-01T18:51:58">Here is some text about the particular service event.</hmis:NoteText>
                        </hmis:note>
                        <hmis:note>
                            <hmis:NoteID>
                                <hmis:IDNum>123457</hmis:IDNum>
                            </hmis:NoteID>
                            <hmis:NoteText hmis:dateCollected="2011-09-01T18:51:58" hmis:dateEffective="2011-09-01T18:51:58">Here is some more text about the same particular service event.</hmis:NoteText>
                        </hmis:note>
                    </ext:ServiceEventNotes>
                </ext:ServiceEvent>
                <ext:SocialSecurityNumber>
                        <hmis:Unhashed hmis:dateCollected="2010-09-15T18:51:58">%s</hmis:Unhashed>
                    <hmis:SocialSecNumberQualityCode hmis:dateCollected="2010-09-15T18:51:58">2</hmis:SocialSecNumberQualityCode>
                </ext:SocialSecurityNumber>
            </ext:Person>
        </ext:Export>
    </ext:Source>
</ext:Sources>
"""
gpg = GPG()
source_ids = ['003', 'tbctest']
sourceId = source_ids[random.randint(0,1)]
exportId = str(int(time.time()))
personId = str(random.randint(1, 999)).zfill(10)
phoneNumber = str(random.randint(2, 9)) + str(random.randint(0, 99)).zfill(2) + \
        str(random.randint(2, 9)) + str(random.randint(0, 99)).zfill(2) + str(random.randint(0, 9999)).zfill(4)
ssn = str(random.randint(2, 9)) + str(random.randint(0, 99)).zfill(2) + \
        str(random.randint(0, 99)).zfill(2) + str(random.randint(0, 9999)).zfill(4)
encrypted_xml = gpg.encrypt(xml_template % (sourceId, exportId, personId, phoneNumber, ssn))
encoded_xml = base64.b64encode(encrypted_xml)
xml_payload="""--98f3d0e0-8336-489b-b815-a48da207a689
Content-Disposition: attachment; name="%s"; filename="%s.xml"
Content-Type: text/xml

%s""" % (sourceId, sourceId, encoded_xml)
headers = {"Content-Type": "multipart/form-data; boundary=98f3d0e0-8336-489b-b815-a48da207a689", "User-Agent": "synthesis"}
req = urllib2.Request('http://127.0.0.1:5001/docs', xml_payload, headers)
resp = urllib2.urlopen(req)
