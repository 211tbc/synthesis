#!/usr/bin/env/python
# -*- coding: utf-8 -*-
HAS_CONF = True
HAS_ENCRYPTION = True
POST_TO_LOCAL_SERVER = True
PRINT_HTTP_POST = True

if POST_TO_LOCAL_SERVER:
    # LOCAL TEST SERVER URLS
    OCC_POST_URL = "http://127.0.0.1:5000/docs"
    TBC_POST_URL = "http://127.0.0.1:5000/docs"
else:
    # REMOTE TEST SERVER URLS
    OCC_POST_URL = "https://pix.penguix.net:8023/docs"
    TBC_POST_URL = "https://pix.penguix.net:8024/docs"

import base64
try:
    from conf import outputConfiguration
except:
    HAS_CONF = False
try:
    from Encryption import *
except:
    HAS_ENCRYPTION = False
import urllib2
import uuid

class REST():

    def __init__(self, source_id, post_url=None):
        self._encryption_type = outputConfiguration.Configuration[source_id]['encryption']
        if post_url == None and HAS_CONF:
            self._url = outputConfiguration.Configuration[source_id]['destinationURL']
        else:
            self._url = post_url

    def post(self, filename, ccd_data, use_base64=False):
        """ filename   : The name of the file attachment
            ccd_data   : The xml to post (send)
            use_base64 : If true, encode the encrypted XML as base64. Maybe necessary for 3DES
        """
        attachments = ""
        payload = """--%s
Content-Disposition: attachment; name="%s"; filename="%s.xml"
Content-Type: text/xml

%s"""

        payload_uuid = str(uuid.uuid4())
        try:
            for data in ccd_data:
                if len(attachments) > 0:
                    attachments += "\r\n\r\n"
                if use_base64:
                    attachments += payload % (payload_uuid, filename, filename, base64.b64encode(data))
                else:
                    attachments += payload % (payload_uuid, filename, filename, data)
            #import pdb; pdb.set_trace()
            if self._url.find("https") == 0:
                https = urllib2.HTTPSHandler(debuglevel=1)
                opener = urllib2.build_opener(https)
                urllib2.install_opener(opener)
                request = urllib2.Request(self._url)
                request.add_header("Content-Type", "multipart/form-data; boundary=%s" % payload_uuid)
                request.add_header("User-Agent", "synthesis")
                request.add_data(attachments)
                if PRINT_HTTP_POST:
                    print request.header_items()
                    print request.get_data()
                    print request.get_method()
                    print request.get_host()
                    return (True, "True")
                response = urllib2.urlopen(request).read()
            else:
                print "**** POSTING TO LOCAL SERVER ****" 
                request = urllib2.Request(self._url)
                request.add_header("Content-Type", "multipart/form-data; boundary=%s" % payload_uuid)
                request.add_header("User-Agent", "synthesis")
                request.add_data(attachments)
                if PRINT_HTTP_POST:
                    print request.header_items()
                    print request.get_data()
                    print request.get_method()
                    print request.get_host()
                    return (True, "True")
                response = urllib2.urlopen(request).read()

            # check for some sign of success within the response
            if response[0:4] == "202:":
                return (True, response)
            else:
                return (False, response)
        except Exception, err:
            return (False, "An error occurred while performing an HTTP-POST or receiving the response: (%s)" % str(err))

    def test_post_local(self, filename, ccd_data, use_base64=False):
        """ filename   : The name of the file attachment
            ccd_data   : The xml to post (send)
            use_base64 : If true, encode the encrypted XML as base64. Maybe necessary for 3DES
        """
        attachments = ""
        payload = """--%s
Content-Disposition: attachment; name="%s"; filename="%s.xml"
Content-Type: text/xml

%s"""

        payload_uuid = str(uuid.uuid4())
        #try:
        for data in ccd_data:
            if len(attachments) > 0:
                attachments += "\r\n\r\n"
            if use_base64:
                attachments += payload % (payload_uuid, filename, filename, base64.b64encode(data))
            else:
                attachments += payload % (payload_uuid, filename, filename, data)
        http = urllib2.HTTPHandler(debuglevel=1)
        opener = urllib2.build_opener(http)
        urllib2.install_opener(opener)
        request = urllib2.Request(self._url)
        request.add_header("Content-Type", "multipart/form-data; boundary=%s" % payload_uuid)
        request.add_header("User-Agent", "synthesis")
        request.add_data(attachments)
        response = urllib2.urlopen(request).read()

        # check for some sign of success within the response
        if response[0:4] == "202:":
            return (True, response)
        else:
            return (False, response)
        #except Exception, err:
        #    return (False, "An error occurred while performing an HTTP-POST or receiving the response: (%s)" % str(err))

# test functions
def occtest():
    rest = REST("occtest", OCC_POST_URL)

    occ_xml = """<?xml version="1.0" encoding="UTF-8"?>
<ext:Sources
    xmlns:airs="http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd" 
    xmlns:ext="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/OCC_Extend_HUD_HMIS.xsd" 
    xmlns:hmis="http://www.hmis.info/schema/3_0/HUD_HMIS.xsd" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/OCC_Extend_HUD_HMIS.xsd http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/OCC_Extend_HUD_HMIS.xsd"
    ext:version="3.0">
    <ext:Source>
        <ext:SourceID>
                <hmis:IDStr>occtest</hmis:IDStr>
        </ext:SourceID>
        <ext:SoftwareVendor>OCC</ext:SoftwareVendor>
        <ext:SoftwareVersion>0.1</ext:SoftwareVersion>
        <ext:SourceContactEmail>i@occ.gov</ext:SourceContactEmail>
        <ext:SourceContactExtension>103</ext:SourceContactExtension>
        <ext:SourceContactFirst>Ike</ext:SourceContactFirst>
        <ext:SourceContactLast>Ross</ext:SourceContactLast>
        <ext:SourceContactPhone>2112111111</ext:SourceContactPhone>
        <ext:SourceName>Orange County Corrections</ext:SourceName>
        <ext:Export>
            <ext:ExportID>
                <!-- Since this is the first export, it's "1".  The second will be "2". -->
                    <hmis:IDNum>7</hmis:IDNum>
            </ext:ExportID>
            <ext:ExportDate>2010-06-23T18:51:58</ext:ExportDate>
            <ext:ExportPeriod>
                <!-- This is an example for the month of June. -->                
                <hmis:StartDate>2010-06-01T00:00:00</hmis:StartDate>
                <hmis:EndDate>2010-06-30T23:59:59</hmis:EndDate>
            </ext:ExportPeriod>
            <ext:Person>
                <ext:PersonID>
                    <hmis:IDNum>2090888539</hmis:IDNum>
                </ext:PersonID>
                <ext:DateOfBirth>
                        <hmis:Unhashed hmis:dateCollected="2011-05-27T18:51:58">2010-04-21</hmis:Unhashed>
                    <hmis:DateOfBirthType hmis:dateCollected="2010-11-05T18:51:58">8</hmis:DateOfBirthType>
                </ext:DateOfBirth>
                <ext:Ethnicity>
                    <hmis:Unhashed hmis:dateCollected="2011-06-25T18:51:58">8</hmis:Unhashed>
                </ext:Ethnicity>
                <ext:Gender>
                    <hmis:Unhashed hmis:dateCollected="2010-06-05T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">2</hmis:Unhashed>
                </ext:Gender>
                <ext:LegalFirstName>
                    <hmis:Unhashed hmis:dateCollected="2011-01-27T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">Harold</hmis:Unhashed>
                </ext:LegalFirstName>
                <ext:LegalLastName>
                    <hmis:Unhashed hmis:dateCollected="2011-03-05T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">Smith</hmis:Unhashed>
                </ext:LegalLastName>
                <ext:PersonHistorical>
                    <hmis:PersonHistoricalID>
                        <hmis:IDStr>1234</hmis:IDStr>
                    </hmis:PersonHistoricalID>
                    <hmis:SiteServiceID>123</hmis:SiteServiceID>
                    <hmis:HousingStatus hmis:dateCollected="2011-03-05T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">1</hmis:HousingStatus>
                    <hmis:LengthOfStayAtPriorResidence hmis:dateCollected="2011-03-05T18:51:58">2</hmis:LengthOfStayAtPriorResidence>
                    <hmis:PhysicalDisability>
                        <hmis:HasPhysicalDisability hmis:dateCollected="2011-03-05T18:51:58">0</hmis:HasPhysicalDisability>
                    </hmis:PhysicalDisability>
                    <hmis:PriorResidence>
                        <hmis:PriorResidenceID>
                            <hmis:IDNum>232</hmis:IDNum>
                        </hmis:PriorResidenceID>
                        <hmis:PriorResidenceCode hmis:dateCollected="2011-06-02T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">1</hmis:PriorResidenceCode>
                    </hmis:PriorResidence>
                    <hmis:Veteran>
                        <hmis:VeteranStatus hmis:dateCollected="2010-01-12T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">1</hmis:VeteranStatus>
                    </hmis:Veteran>
                    <ext:FosterChildEver hmis:dateCollected="2011-03-05T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">1</ext:FosterChildEver>
                </ext:PersonHistorical>
                <ext:Race>
                    <hmis:Unhashed hmis:dateCollected="2009-11-30T18:51:58">2</hmis:Unhashed>
                </ext:Race>           
                <ext:SocialSecurityNumber>
                        <hmis:Unhashed hmis:dateCollected="2011-09-15T18:51:58">111111111</hmis:Unhashed>
                    <hmis:SocialSecNumberQualityCode hmis:dateCollected="2011-04-29T18:51:58" >2</hmis:SocialSecNumberQualityCode>
                </ext:SocialSecurityNumber>
            </ext:Person>
        </ext:Export>
    </ext:Source>
</ext:Sources>"""
    
    # test results
    if HAS_ENCRYPTION:
        keyiv = get_incoming_3des_key_iv()
        des3 = DES3()
        encrypted_data = des3.encrypt(occ_xml, keyiv['key'], iv=keyiv['iv'])
        #print encrypted_data
        print "Result of OCC test (encrypted): ", rest.test_post_local("occtest", [encrypted_data,], use_base64=True)
    else:
        print "Result of OCC test (unencrypted): ", rest.test_post_local("occtest", [occ_xml,], use_base64=False)

def tbctest():
    rest = REST("tbctest", TBC_POST_URL)

    tbc_xml = """<?xml version="1.0" encoding="UTF-8"?>
<ext:Sources
    xmlns:airs="http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd" 
    xmlns:ext="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd" 
    xmlns:hmis="http://www.hmis.info/schema/3_0/HUD_HMIS.xsd" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd" 
    ext:version="3.0">
    <ext:Source>
        <ext:SourceID >
                <hmis:IDStr>tbctest</hmis:IDStr>
        </ext:SourceID>
        <ext:SoftwareVendor>Vendor Name Here</ext:SoftwareVendor>
        <ext:SoftwareVersion>7.1</ext:SoftwareVersion>
        <ext:SourceName>Source Name Here</ext:SourceName>
        <ext:Export>
            <ext:ExportID >
                <!-- Since this is the first export, it's "1".  The second will be "2". -->
                    <hmis:IDNum>1010111</hmis:IDNum>
            </ext:ExportID>
            <ext:ExportDate>2011-09-23T18:51:58</ext:ExportDate>
            <ext:ExportPeriod>
                <!-- This is an example for the month of June. -->                
                <hmis:StartDate>2011-09-01T00:00:00</hmis:StartDate>
                <hmis:EndDate>2011-09-02T23:59:59</hmis:EndDate>
            </ext:ExportPeriod>
            <ext:Person>
                <ext:PersonID>
                    <hmis:IDNum>2090888539</hmis:IDNum>
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
                    <hmis:Unhashed hmis:dateCollected="2011-01-27T18:51:58">Harold</hmis:Unhashed>
                </ext:LegalFirstName>
                <ext:LegalLastName>
                    <hmis:Unhashed hmis:dateCollected="2011-03-05T18:51:58">Smith</hmis:Unhashed>
                </ext:LegalLastName>
                <ext:LegalMiddleName>
                    <hmis:Unhashed hmis:dateCollected="2011-03-05T18:51:58">Barclay</hmis:Unhashed>
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
                    <hmis:PersonPhoneNumber hmis:dateCollected="2009-11-30T18:51:58">2346543210</hmis:PersonPhoneNumber>
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
                                <hmis:IDNum>11111</hmis:IDNum>
                            </ext:AgencyReferredToID>
                            <!--Extension element -->
                            <ext:AgencyReferredToName hmis:dateCollected="2009-11-30T18:51:58">Suncoast Center, Inc.</ext:AgencyReferredToName>
                            <!--Refers to a standalone need--> 
                            <ext:NeedID>
                                 <hmis:IDNum>345</hmis:IDNum>
                            </ext:NeedID>
                        </ext:Referral>
                        <ext:Referral>
                            <ext:ReferralID>
                                <hmis:IDNum>12346</hmis:IDNum>
                            </ext:ReferralID>
                            <ext:AgencyReferredToID>
                                <hmis:IDNum>11111</hmis:IDNum>
                            </ext:AgencyReferredToID>
                            <ext:AgencyReferredToName hmis:dateCollected="2009-11-30T18:51:58">Suncoast Center, Inc.</ext:AgencyReferredToName>
                            <!--Here is a nested need within a referral (the other way of referring to a need from a referral)-->                
                            <ext:Need>
                                <hmis:NeedID>
                                    <hmis:IDNum>346</hmis:IDNum>
                                </hmis:NeedID>
                                <hmis:SiteServiceID>1766</hmis:SiteServiceID>
                                <hmis:NeedStatus>1</hmis:NeedStatus>
                                <hmis:Taxonomy>
                                    <airs:Code>123.456</airs:Code>
                                </hmis:Taxonomy>
                            </ext:Need>
                        </ext:Referral>
                    </ext:Referrals>
                    <ext:ServiceEventProvisionDate>2011-09-01</ext:ServiceEventProvisionDate>
                    <ext:ServiceEventNotes>
                        <hmis:note>
                            <hmis:NoteID >
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
                        <hmis:Unhashed hmis:dateCollected="2010-09-15T18:51:58">111111111</hmis:Unhashed>
                    <hmis:SocialSecNumberQualityCode hmis:dateCollected="2010-09-15T18:51:58" >2</hmis:SocialSecNumberQualityCode>
                </ext:SocialSecurityNumber>
            </ext:Person>
        </ext:Export>
    </ext:Source>
</ext:Sources>"""
    
    # test results
    if HAS_ENCRYPTION:
        gpg = GPG()
        encrypted_data = gpg.encrypt(tbc_xml)
        #print encrypted_data
        print "Result of TBC test (encrypted): ", rest.test_post_local("tbctest", [encrypted_data,], use_base64=True)
    else:
        print "Result of TBC test (unencrypted): ", rest.test_post_local("tbctest", [tbc_xml,], use_base64=False)

if __name__ == "__main__":
    # testing TBC HTTP-POST
    #tbctest()

    # testing OCC HTTP-POST
    #occtest()

    pass
