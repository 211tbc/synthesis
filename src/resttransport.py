#!/usr/bin/env/python
# -*- coding: utf-8 -*-
from conf import outputConfiguration
import urllib2
import uuid

class REST():

    def __init__(self, source_id):
        self._url = outputConfiguration.Configuration[source_id]['destinationURL']

    def post(self, ccd_data, test=False):
        try:
            payload_uuid = str(uuid.uuid4())
            request = urllib2.Request(self._url)
            request.add_header("Content-Type", "multipart/form-data; boundary=%s" % payload_uuid)
            request.add_header("User-Agent", "synthesis")
            request.add_data(ccd_data % payload_uuid)
            response = urllib2.urlopen(request).read()

            # check for some sign of success within the response
            if response.lower().find("success"):
                return (True, response)
            else:
                return (False, response)
        except Exception, err:
            return (False, "An error occurred while performing an HTTP-POST or receiving the response: (%s)" % str(err))

if __name__ == "__main__":
    rest = REST("test")
    payload = """--%s
Content-Disposition: attachment; name="test"; filename="test.xml"
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8"?>
<ext:Sources
    xmlns:airs="http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd" 
    xmlns:ext="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/OCC_Extend_HUD_HMIS.xsd" 
    xmlns:hmis="http://www.hmis.info/schema/3_0/HUD_HMIS.xsd" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/OCC_Extend_HUD_HMIS.xsd http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/OCC_Extend_HUD_HMIS.xsd"
    ext:version="3.0">
    <ext:Source>
        <ext:SourceID>
                <hmis:IDStr>003</hmis:IDStr>
        </ext:SourceID>
        <ext:SoftwareVendor>Orange County Corrections</ext:SoftwareVendor>
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
                    <hmis:IDNum>1</hmis:IDNum>
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
                    <hmis:Hashed hmis:dateCollected="2011-01-27T18:51:58" hmis:dateEffective="2011-03-05T18:51:58">Harold</hmis:Hashed>
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
    # This test should fail because the XML is invalid
    print rest.post(payload)
