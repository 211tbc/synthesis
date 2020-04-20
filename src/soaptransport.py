#!/usr/bin/env/python
# -*- coding: utf-8 -*-
from .conf import settings, hl7settings
from .conf import outputConfiguration
from .Encryption import *  # @UnusedWildImport
import urllib.request
import http.client
from sys import version
from lxml import etree
import urllib.parse
import uuid
import base64
import time
from synthesis.exceptions import SoftwareCompatibilityError
#import dbobjects

# py 2.5 support
# dynamic import of modules
thisVersion = version[0:3]
if True:
    from lxml import etree as ET  # @UnusedImport

else:
    print('Sorry, please see the minimum requirements to run this Application')
    theError = (1100, 'This application requires Python 2.4 or higher.  You are current using version: %s' % (thisVersion), 'import Error XMLDumper.py')
    raise SoftwareCompatibilityError(theError)

PRINT_SOAP_REQUEST = settings.DEBUG


def ascii_only(text):
    # If parameter is a string, return only ascii character by replacing non-ascii
    # characters with whitespace (i.e. ' ')
    if type(text) == str:
        temp = ''.join([i if ord(i) < 128 else ' ' for i in text])
        return temp.encode('ascii', 'ignore')
    else:
        return text

class HTTPSClientAuthHandler(urllib.request.HTTPSHandler):  
    def __init__(self, key, cert):  
        urllib.request.HTTPSHandler.__init__(self, debuglevel=1)  
        #urllib.request.HTTPSHandler.__init__(self)  
        self.key = key  
        self.cert = cert  
    def https_open(self, req):  
        #Rather than pass in a reference to a connection class, we pass in  
        # a reference to a function which, for all intents and purposes,  
        # will behave as a constructor  
        return self.do_open(self.getConnection, req)  
    def getConnection(self, host, timeout=300):  
        return http.client.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)  

class SoapEnv():

    def __init__(self, source_id):
        self._soap_server = outputConfiguration.Configuration[source_id]['destinationURL']
        self._encryption_type = outputConfiguration.Configuration[source_id]['encryption']
        self._host = urllib.parse.urlparse(self._soap_server).netloc
        #self._post = urlparse.urlparse(self._soap_server).path

        # define the soap envelope template

        self._ENVELOPE_TEMPLATE = """


%(XML_UUID)s
Content-Type: application/xop+xml; charset=UTF-8; type="application/soap+xml"; action="DocumentRepository_ProvideAndRegisterDocumentSet-b"
Content-Transfer-Encoding: 8bit
Content-ID: %(START_UUID)s

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:ihe:iti:xds-b:2007" xmlns:urn1="urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0" xmlns:urn2="urn:oasis:names:tc:ebxml-regrep:xsd:rs:3.0" xmlns:urn3="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0" xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:direct="urn:direct:addressing">
   <soap:Header>
      <a:MessageID>%(MESSAGE_ID_UUID)s</a:MessageID>
      <a:Action soap:mustUnderstand="1">urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b</a:Action>
      <direct:addressBlock a:IsReferenceParameter="true" a:relay="true" a:role="urn:direct:addressing:destination">
         <direct:from>%(DIRECT_FROM)s</direct:from>
         <direct:to>%(DIRECT_TO)s</direct:to>
         <direct:metadata-level>XDS</direct:metadata-level>
      </direct:addressBlock>
   </soap:Header>
   <soap:Body>
      <urn:ProvideAndRegisterDocumentSetRequest>
         <urn1:SubmitObjectsRequest id="%(OBJECT_ID_UUID)s">
            <!--Optional:-->
            <urn3:RegistryObjectList>
               <urn1:ExtrinsicObject id="%(DOCUMENT_OBJECT)s" mimeType="text/xml" objectType="urn:uuid:%(EXTRINSIC_OBJECT_UUID)s">
                  <!--Zero or more repetitions:-->
                  <urn3:Identifiable id="%(IDENTITY_ID_UUID)s">
                     <!--Zero or more repetitions:-->
                     <urn3:Slot name="creationTime">
                        <urn3:ValueList>
                           <urn3:Value>%(CREATION_TIME)s</urn3:Value>
                        </urn3:ValueList>
                     </urn3:Slot>
                     <urn3:Slot name="languageCode">
                        <urn3:ValueList>
                           <urn3:Value>%(LANGUAGE_CODE)s</urn3:Value>
                        </urn3:ValueList>
                     </urn3:Slot>
                  </urn3:Identifiable>
               </urn1:ExtrinsicObject>
            </urn3:RegistryObjectList>
         </urn1:SubmitObjectsRequest>
         <!--1 or more repetitions of Document-->
         <Document id="%(DOCUMENT_OBJECT)s">
            <xop:Include href="cid:CCD_%(UNIQUE_ID)s.xml" xmlns:xop="http://www.w3.org/2004/08/xop/include"/>
         </Document>
      </urn:ProvideAndRegisterDocumentSetRequest>
   </soap:Body>
</soap:Envelope>%(MIME_BORDER_SECTION)s""".replace("\t","")

    def send_soap_envelope(self, ccd_data, referredToProviderID, source_id):
        
        SystemUserId = ""
        ReceivingProviderId = ""
        if settings.SEND_REFERRALS_TO_PRODUCTION:
            SystemUserId = outputConfiguration.Configuration[source_id]['Production_SystemUserId']
        else:
            SystemUserId = outputConfiguration.Configuration[source_id]['Testing_SystemUserId']

        import copy
        soap_transport_properties = copy.deepcopy(hl7settings.SOAP_TRANSPORT_PROPERTIES)

        ccd = ET.fromstring(ccd_data)

        #
        # construct the message and header
        #

        # document id
        soap_transport_properties["DOCUMENT_OBJECT"] = ccd.find("{urn:hl7-org:v3}id").attrib.get("extension")

        # extrinsic author person
        soap_transport_properties["EXTRINSIC_AUTHOR_PERSON"] = "^Left^Right^^^"

        # registry author person
        soap_transport_properties["REGISTRY_AUTHOR_PERSON"] = "^First^Last^^^"

        # Language Code
        soap_transport_properties["LANGUAGE_CODE"] = ccd.find("{urn:hl7-org:v3}languageCode").attrib.get("code")

        # Source Patient ID
        patient_role = ccd.find("{urn:hl7-org:v3}recordTarget/{urn:hl7-org:v3}patientRole")
        source_patient_id = patient_role.find("{urn:hl7-org:v3}id").attrib.get("extension")
        soap_transport_properties["SOURCE_PATIENT_ID"] = "%s^^^&amp;3.4.5&amp;ISO" % source_patient_id
        
        # submissionTime -- Where does it come from? Is this module responsible for generating it?
        t = time.gmtime()
        snapshot = str(t[0])+str(t[1]).zfill(2)+str(t[2]).zfill(2)+str(t[3]).zfill(2)+str(t[4]).zfill(2)+str(t[5]).zfill(2)
        soap_transport_properties["SUBMISSION_TIME"] = snapshot

        # creationTime -- Where does it come from? Is this module responsible for generating it?
        t = time.gmtime()
        #snapshot = str(t[0])+str(t[1]).zfill(2)+str(t[2]).zfill(2)
        snapshot = "%s-%s-%sT%s:%s:%s"%(str(t[0]), str(t[1]).zfill(2), str(t[2]).zfill(2), str(t[3]).zfill(2), str(t[4]).zfill(2), str(t[5]).zfill(2))
        soap_transport_properties["CREATION_TIME"] = snapshot

        # Patient ID <== Where does this come from?
        soap_transport_properties["PATIENT_ID"] = "ef77eeda67dd4a2^^^&amp;1.3.6.1.4.1.21367.2005.3.7&amp;ISO"

        # Source ID <== Where does this come from?
        soap_transport_properties["SOURCE_ID"] = "1.3.6.1.4.1.21367.2009.1.2.1"

        #03/17/2013 ECJ adding referring provider id to differentiate originating source
        # for Suncoast Center
        if str(referredToProviderID) in ['885','12047','12048','12049','12052','12054','12055','12060','15333','15392','15399','15400','15402','15403','15404','15405','15407','15408','15409','15410','15411','15413','15414','15416','15434','15436','15437','15438','15442','15443','15444','15445','15446','15447','15484','15485','15487','15488','15489','15490','15492','15493','15494','15495','15496','15500','15501','15502','15503','15505','15506','15507','15508','15509','15510','15511','15513','15514','15515','15516','15517','15518','15519','15520','15521','15522','15523','15524','15525','15526','15527','15529','15530','15531','15532','15533','15534','15535','15536','15537','15538']:
            if settings.SEND_REFERRALS_TO_PRODUCTION:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['Suncoast_production_ReceivingProviderId']
            else:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['Suncoast_test_ReceivingProviderId']
            if settings.USE_TESTING_REFERRAL_EMAIL:
                soap_transport_properties['DIRECT_TO'] = 'Suncoast@uat.direct.ntst.com'
            else:
                #soap_transport_properties['DIRECT_TO'] = 'Suncoast@direct.ntst.com'
                soap_transport_properties['DIRECT_TO'] = 'SuncoastCenter@suncoast.netsmartdirect.net'

        # for PEMHS    
        elif str(referredToProviderID) in ['8169', '15346', '3546', '12605', '15368', '14109','15356','11031','14086','2222','15749','11034','15400']:
            if settings.SEND_REFERRALS_TO_PRODUCTION:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['PEMHS_production_ReceivingProviderId']
            else:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['PEMHS_test_ReceivingProviderId']
            if settings.USE_TESTING_REFERRAL_EMAIL:
                soap_transport_properties['DIRECT_TO'] = 'PEMHS@uat.direct.ntst.com'
            else:
                soap_transport_properties['DIRECT_TO'] = 'PEMHS@direct.ntst.com'

        # for Boley
        elif str(referredToProviderID) in ['9082', '16537', '15772', '16536', '13686', '15114', '15889', '16327', '15026', '13626', '14337', '13629', '13630', '13632', '13631', '15973', '944', '15432', '9084', '14339', '13708', '14338', '13711', '16535', '13709', '13710', '16283', '16333', '13712', '13687', '14079', '14775', '15254', '15253', '1429', '16375', '9085', '14340', '13707', '14363', '9086', '9087']:
            if settings.SEND_REFERRALS_TO_PRODUCTION:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['Boley_production_ReceivingProviderId']
            else:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['Boley_test_ReceivingProviderId']
            if settings.USE_TESTING_REFERRAL_EMAIL:
                soap_transport_properties['DIRECT_TO'] = 'BoleyCenter@uat.direct.ntst.com'
            else:
                soap_transport_properties['DIRECT_TO'] = 'BoleyCenter@direct.ntst.com'

        # for Directions for Living
        elif str(referredToProviderID) in ['9757', '9754', '9755', '9756', '16427', '16425', '16424', '16426', '15364', '9758', '15262', '9759', '16421', '16420', '16419', '15693', '16092', '7651', '14810', '14809', '16555', '13016', '16422', '16423', '15367']:
            if settings.SEND_REFERRALS_TO_PRODUCTION:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['DFL_production_ReceivingProviderId']
            else:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['DFL_test_ReceivingProviderId']
            if settings.USE_TESTING_REFERRAL_EMAIL:
                soap_transport_properties['DIRECT_TO'] = 'DirectionsForLiving@uat.direct.ntst.com'
            else:
                soap_transport_properties['DIRECT_TO'] = 'DirectionsForLiving@direct.ntst.com'

        # for GCJFCS
        elif str(referredToProviderID) in ['10180', '10183', '15482', '10186', '10182', '10190', '10194', '10195', '15464', '7854']:
            if settings.SEND_REFERRALS_TO_PRODUCTION:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['GCJFCS_production_ReceivingProviderId']
            else:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['GCJFCS_test_ReceivingProviderId']
            if settings.USE_TESTING_REFERRAL_EMAIL:
                soap_transport_properties['DIRECT_TO'] = 'GulfCoast@uat.direct.ntst.com'
            else:
                soap_transport_properties['DIRECT_TO'] = 'GulfCoast@direct.ntst.com'

        # for Operation PAR
        elif str(referredToProviderID) in ['10940', '10919', '15588', '10954', '10939', '15579', '10921', '10937', '10943', '15581', '8133', '10935', '14921', '15589', '15582', '10933', '15590', '10936', '16064', '15702', '13294', '15563', '4766', '10945', '10949', '15755', '15587', '12567', '14102']:
            if settings.SEND_REFERRALS_TO_PRODUCTION:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['OPAR_production_ReceivingProviderId']
            else:
                ReceivingProviderId = outputConfiguration.Configuration[source_id]['OPAR_test_ReceivingProviderId']
            if settings.USE_TESTING_REFERRAL_EMAIL:
                soap_transport_properties['DIRECT_TO'] = 'OperationPar@uat.direct.ntst.com'
            else:
                soap_transport_properties['DIRECT_TO'] = 'OperationPar@direct.ntst.com'

        else:
            # Provider IDs not filtered above are unmapped here.
            if referredToProviderID == '15473':
                # Sent document to Netsmart test endpoint.
                self._soap_server = 'https://labsdev.netsmartcloud.com:444/CareConnectXDR'
                self._host = urllib.parse.urlparse(self._soap_server).netloc
            else:
                # Log that the Provider ID is unmapped.
                ReceivingProviderId = ""
                soap_transport_properties['DIRECT_TO'] = ""
                # The provider ID  could not be mapped so log receipt as such
                return (True, "Referral ID %s is unmapped!" % str(referredToProviderID))

        soap_transport_properties["UNIQUE_ID"] = str(uuid.uuid4()).replace("-", "").upper()

        # Random UUIDs
        soap_transport_properties["START_UUID"] = str(uuid.uuid4()).replace("-", "").upper()
        soap_transport_properties["XML_UUID"] = '------=_Part_0_581382233.1586371463133'
        #soap_transport_properties["XML_UUID"] = '--MIMEBoundaryurn_uuid_%s' % str(uuid.uuid4()).replace("-", "").upper()

        soap_transport_properties["MESSAGE_ID_UUID"] = str(uuid.uuid4()).replace("-", "").upper()
        soap_transport_properties["OBJECT_ID_UUID"] = str(uuid.uuid4()).replace("-", "").upper()
        soap_transport_properties["IDENTITY_ID_UUID"] = str(uuid.uuid4()).replace("-", "").upper()
        soap_transport_properties["AUTHOR_UUID"] = str(uuid.uuid4())
        
        #
        # BEGIN OPTIONAL TAGS
        #

        test = lambda s: s if len(s.strip()) > 0 else ""
        
        # Store original properties values by "testing" each property using the lambda function defined above
        orig_EXTRINSIC_NAME_TAG = test(soap_transport_properties["EXTRINSIC_NAME_TAG"])
        orig_EXTRINSIC_DESCRIPTION_TAG = test(soap_transport_properties["EXTRINSIC_DESCRIPTION_TAG"])
        orig_EXTRINSIC_AUTHOR_INSTITUTION_SLOT = test(soap_transport_properties["EXTRINSIC_AUTHOR_INSTITUTION_SLOT"])
        orig_EXTRINSIC_AUTHOR_ROLE_SLOT = test(soap_transport_properties["EXTRINSIC_AUTHOR_ROLE_SLOT"])
        orig_EXTRINSIC_AUTHOR_SPECIALTY_SLOT = test(soap_transport_properties["EXTRINSIC_AUTHOR_SPECIALTY_SLOT"])
        orig_REGISTRY_PACKAGE_NAME_TAG = test(soap_transport_properties["REGISTRY_PACKAGE_NAME_TAG"])
        orig_REGISTRY_PACKAGE_DESCRIPTION_TAG = test(soap_transport_properties["REGISTRY_PACKAGE_DESCRIPTION_TAG"])
        orig_REGISTRY_AUTHOR_INSTITUTION_SLOT = test(soap_transport_properties["REGISTRY_AUTHOR_INSTITUTION_SLOT"])
        orig_REGISTRY_AUTHOR_ROLE_SLOT = test(soap_transport_properties["REGISTRY_AUTHOR_ROLE_SLOT"])
        orig_REGISTRY_AUTHOR_SPECIALTY_SLOT = test(soap_transport_properties["REGISTRY_AUTHOR_SPECIALTY_SLOT"])
        orig_SERVICE_START_TIME = test(soap_transport_properties["SERVICE_START_TIME"])
        orig_SERVICE_STOP_TIME = test(soap_transport_properties["SERVICE_STOP_TIME"])

        # if Extrinsic has a name attribute ...
        if len(orig_EXTRINSIC_NAME_TAG) > 0:
            soap_transport_properties["EXTRINSIC_NAME_TAG"] = """<rim:Name><rim:LocalizedString value="%s"/></rim:Name>""" % orig_EXTRINSIC_NAME_TAG
        else:
            soap_transport_properties["EXTRINSIC_NAME_TAG"] = "<rim:Name/>"

        # if Extrinsic has a description attribute ... 
        if len(orig_EXTRINSIC_DESCRIPTION_TAG) > 0:
            soap_transport_properties["EXTRINSIC_DESCRIPTION_TAG"] = """<rim:Description><rim:LocalizedString value="%s"/></rim:Description>""" % orig_EXTRINSIC_DESCRIPTION_TAG
        else:
            soap_transport_properties["EXTRINSIC_DESCRIPTION_TAG"] = "<rim:Description/>"

        # if there is an authorInstitution slot for Extrinsic ...
        if len(orig_EXTRINSIC_AUTHOR_INSTITUTION_SLOT) > 0:
            soap_transport_properties["EXTRINSIC_AUTHOR_INSTITUTION_SLOT"] = """<rim:Slot name="authorInstitution">
                            <rim:ValueList>
                                <rim:Value>%s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>""" % orig_EXTRINSIC_AUTHOR_INSTITUTION_SLOT

        # if there is an authorRole slot for Extrinsic ...
        if len(orig_EXTRINSIC_AUTHOR_ROLE_SLOT) > 0:
            soap_transport_properties["EXTRINSIC_AUTHOR_ROLE_SLOT"] = """<rim:Slot name="authorRole">
                            <rim:ValueList>
                                <rim:Value>%s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>""" % orig_EXTRINSIC_AUTHOR_ROLE_SLOT

        # if there is an authorSpecialty slot for Extrinsic ...
        if len(orig_EXTRINSIC_AUTHOR_SPECIALTY_SLOT) > 0:
            soap_transport_properties["EXTRINSIC_AUTHOR_SPECIALTY_SLOT"] = """<rim:Slot name="authorSpecialty">
                            <rim:ValueList>
                                <rim:Value>%s</rim:Value>
                                <!-- Add more value tags as needed -->
                            </rim:ValueList>
                        </rim:Slot>""" % orig_EXTRINSIC_AUTHOR_SPECIALTY_SLOT

        ## if RegistryPackage has a name attribute ...
        #if len(orig_REGISTRY_PACKAGE_NAME_TAG) > 0:
        #    soap_transport_properties["REGISTRY_PACKAGE_NAME_TAG"] = """<rim:Name><rim:LocalizedString value="%s"/></rim:Name>""" % orig_REGISTRY_PACKAGE_NAME_TAG
        #else:
        #    soap_transport_properties["REGISTRY_PACKAGE_NAME_TAG"] = "<rim:Name/>"

        ## if RegistryPackage has a description attribute ... 
        #if len(orig_REGISTRY_PACKAGE_DESCRIPTION_TAG) > 0:
        #    soap_transport_properties["REGISTRY_PACKAGE_DESCRIPTION_TAG"] = """<rim:Description><rim:LocalizedString value="%s"/></rim:Description>""" % orig_REGISTRY_PACKAGE_DESCRIPTION_TAG
        #else:
        #    soap_transport_properties["REGISTRY_PACKAGE_DESCRIPTION_TAG"] = "<rim:Description/>"

        # if there is an authorInstitution slot for RegistryPackage ...
        if len(orig_REGISTRY_AUTHOR_INSTITUTION_SLOT) > 0:
            soap_transport_properties["REGISTRY_AUTHOR_INSTITUTION_SLOT"] = """<rim:Slot name="authorInstitution">
                            <rim:ValueList>
                                <rim:Value>%s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>""" % orig_REGISTRY_AUTHOR_INSTITUTION_SLOT

        # if there is an authorRole slot for RegistryPackage ...
        if len(orig_REGISTRY_AUTHOR_ROLE_SLOT) > 0:
            soap_transport_properties["REGISTRY_AUTHOR_ROLE_SLOT"] = """<rim:Slot name="authorRole">
                            <rim:ValueList>
                                <rim:Value>%s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>""" % orig_REGISTRY_AUTHOR_ROLE_SLOT

        # if there is an authorSpecialty slot for RegistryPackage ...
        if len(orig_REGISTRY_AUTHOR_SPECIALTY_SLOT) > 0:
            soap_transport_properties["REGISTRY_AUTHOR_SPECIALTY_SLOT"] = """<rim:Slot name="authorSpecialty">
                            <rim:ValueList>
                                <rim:Value>%s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>""" % orig_REGISTRY_AUTHOR_SPECIALTY_SLOT

        # if there is a serviceStartTime ...
        if len(orig_SERVICE_START_TIME) > 0:
            soap_transport_properties["SERVICE_START_TIME"] = """<rim:Slot name="serviceStartTime">
                                <rim:ValueList>
                                    <rim:Value>%s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>""" % orig_SERVICE_START_TIME

        # if there is a serviceStopTime ...
        if len(orig_SERVICE_STOP_TIME) > 0:
            soap_transport_properties["SERVICE_STOP_TIME"] = """<rim:Slot name="serviceStopTime">
                                <rim:ValueList>
                                    <rim:Value>%s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>""" % orig_SERVICE_STOP_TIME
        
        # if there is a sourcePatientInfo ...
        #soap_transport_properties["SOURCE_PATIENT_INFO"] = """
        #                <rim:Slot name="sourcePatientInfo">
        #                    <rim:ValueList>
        #                        <rim:Value>PID-3|89765a87b^^^&amp;3.4.5&amp;ISO</rim:Value>
        #                        <rim:Value>PID-5|Doe^John^^^</rim:Value>
        #                        <rim:Value>PID-7|19560527</rim:Value>
        #                        <rim:Value>PID-8|M</rim:Value>
        #                        <rim:Value>PID-11|100 Main St^^Metropolis^Il^44130^USA</rim:Value>
        #                    </rim:ValueList>
        #                </rim:Slot>"""

        #
        # END OPTIONAL TAGS
        #

        # Taxonomy Code
        try:
            taxonomy_codes = ' '.join([c.text for c in ccd.iter('{http://www.hudhdx.info/Resources/Vendors/3_0/AIRS_3_0_mod.xsd}Code')])
        except:
            taxonomy_codes = ''

        # Note Text
        try:
            referal_notes = ' '.join([c.text for c in ccd.iter('{http://www.hudhdx.info/Resources/Vendors/3_0/HUD_HMIS.xsd}NoteText')])
        except:
            referal_notes = ''
            
        # FBY New 2017-03-12 : NeedNotes text
        try:
            need_notes = ' '.join([c.text for c in ccd.iter('{https://raw.githubusercontent.com/211tbc/synthesis/master/src/xsd/TBC_Extend_HUD_HMIS.xsd}NeedNotes')])
        except:
            need_notes = ''

        # FBY New 2017-04-18 : AIRS Code text
        try:
            airs_code = ' '.join([c.text for c in ccd.iter('{https://raw.githubusercontent.com/211tbc/synthesis/master/src/xsd/TBC_Extend_HUD_HMIS.xsd}TempAirsCode')])
        except:
            airs_code = ''

        # FBY New 2017-03-12 : Combine notes and codes
        soap_transport_properties["REGISTRY_PACKAGE_NAME_TAG"] = """<rim:Name><rim:LocalizedString xml:lang="en-us" charset="UTF-8" value="Need Note - %s  Need AIRS Code: %s %s  Referral Notes - %s" /></rim:Name>""" % (need_notes, taxonomy_codes, airs_code, referal_notes)
        soap_transport_properties["REGISTRY_PACKAGE_DESCRIPTION_TAG"] = """<rim:Description />"""
        
        # FBY New 2017-03-12 : Strip NeedNotes from XML
        if need_notes != '':
            for tag in ccd.iter('{https://raw.githubusercontent.com/211tbc/synthesis/master/src/xsd/TBC_Extend_HUD_HMIS.xsd}NeedNotes'):
                tag.getparent().remove(tag)

        # FBY New 2017-04-18 : Strip AirsCode and ServiceEvent from XML
        if airs_code != '':
            for tag in ccd.iter('{https://raw.githubusercontent.com/211tbc/synthesis/master/src/xsd/TBC_Extend_HUD_HMIS.xsd}TempAirsCode'):
                tag.getparent().remove(tag)
            for tag in ccd.iter('{https://raw.githubusercontent.com/211tbc/synthesis/master/src/xsd/TBC_Extend_HUD_HMIS.xsd}TempServiceEvent'):
                tag.getparent().remove(tag)

        # SOAP Attachment
        payload_uuid = str(uuid.uuid4()).replace("-", "").upper()

        ccd_id = ccd.find("{urn:hl7-org:v3}id").attrib.get("extension")
        soap_transport_properties["ASSOCIATION_SECTION"] += """<rim:Association
                    associationType="urn:oasis:names:tc:ebxml-regrep:AssociationType:HasMember"
                    sourceObject="%s" targetObject="%s" id="%s"
                    objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Association">
                    <rim:Slot name="SubmissionSetStatus">
                        <rim:ValueList>
                            <rim:Value>%s</rim:Value>
                        </rim:ValueList>
                    </rim:Slot>
                </rim:Association>""" % (soap_transport_properties["SOURCE_OBJECT"], \
                                         ccd_id, \
                                         soap_transport_properties["ASSOCIATION_ID"], \
                                         soap_transport_properties["ASSOCIATION_VALUE"])
        soap_transport_properties["ATTACHMENT_SECTION"] += """<xdsb:Document id="%s">
            <xop:Include href="cid:1.urn:uuid:%s@apache.org" xmlns:xop="http://www.w3.org/2004/08/xop/include"/>
        </xdsb:Document>""" % (soap_transport_properties["DOCUMENT_OBJECT"], payload_uuid)
        attachment = etree.tostring(ccd, encoding='utf8', method='xml', pretty_print=True)

        if self._encryption_type != "none":
            if self._encryption_type == "3des":
                keyiv = get_incoming_3des_key_iv()
                des3 = DES3()
                attachment = base64.b64encode(des3.encrypt(ccd_data, keyiv['key'], iv=keyiv['iv']))
            if self._encryption_type == "openpgp":
                gpg = GPG()
                attachment = base64.b64encode(gpg.encrypt(ccd_data))
#        soap_transport_properties["MIME_BORDER_SECTION"] += """
#--MIMEBoundaryurn_uuid_%s
#Content-Type: text/xml; charset=us-ascii; name=CCD.xml
#Content-Transfer-Encoding: 7bit
#Content-ID: <CCD.xml>
#Content-Disposition: attachment; name="CCD.xml"; filename="CCD.xml"
#
#%s
#
#--MIMEBoundaryurn_uuid_%s--""" % (soap_transport_properties["XML_UUID"], attachment, soap_transport_properties["XML_UUID"])
        
        #ncrypted_xml = gpg.encrypt(xml)
        #ncoded_xml = base64.b64encode(encrypted_xml.encode())

        soap_transport_properties["MIME_BORDER_SECTION"] += """
%s
Content-Type: text/xml; charset=us-ascii; name=CCD_%s.xml
Content-Transfer-Encoding: 7bit
Content-ID: <CCD_%s.xml>
Content-Disposition: attachment; name="CCD_%s.xml"; filename="CCD_%s.xml"

%s

%s--""" % (soap_transport_properties["XML_UUID"], soap_transport_properties["UNIQUE_ID"], soap_transport_properties["UNIQUE_ID"], soap_transport_properties["UNIQUE_ID"], soap_transport_properties["UNIQUE_ID"], attachment, soap_transport_properties["XML_UUID"])
        
        # generate the SOAP envelope
        for key in soap_transport_properties.keys():
            # For each property, sanitize the text.
            #soap_transport_properties[key] = ascii_only(soap_transport_properties[key]).decode().replace('\\n', '')
            soap_transport_properties[key] = ascii_only(soap_transport_properties[key]).decode()
        
        soap_env = self._ENVELOPE_TEMPLATE % soap_transport_properties
        soap_env = soap_env.replace("\\n", "\n")
        soap_env = soap_env.replace("\n\nb\'", "\n\n")
        soap_env = soap_env.replace("\\\'", "\'")
        soap_env = soap_env.replace("\n\'", "")
        
        #print(soap_env)
        
        #while '\\\\' in soap_env:
        #    soap_env = soap_env.replace('\\\\', '\\')

        #soap_env = test_soap_env

        print('Sending SOAP document to "%s"' % self._soap_server)
        #import pdb; pdb.set_trace()

        # create header
        headers = {
            "Host"              : self._host,
            "User-Agent"        : "synthesis",
            "Accept-Encoding"   : "gzip,deflate",
            "Connection"        : "Keep-Alive",
            "MIME-Version"      : "1.0",
            "SystemUserId"    : SystemUserId,
            "ReceivingProviderId" : ReceivingProviderId,
            "Content-type"      : "multipart/related; type=\"application/xop+xml\"; start=\"%s\"; start-info=\"application/soap+xml\"; boundary=\"%s\"; action=\"urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b\"" % (soap_transport_properties["START_UUID"], soap_transport_properties["XML_UUID"][2:]),
            #"Content-type"      : "multipart/related; type=\"application/xop+xml\"; start=\"<rootpart@soapui.org>\"; start-info=\"application/soap+xml\"; boundary=\"----=_Part_0_581382233.1586371463133\"; action=\"urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b\"",
            "Content-length"    : "%d" % len(soap_env),
            }

        #if PRINT_SOAP_REQUEST: # delete this if block
        #    import pprint as pp
        #    pp.pprint(headers)
        #    #print soap_env
        #    #import pdb; pdb.set_trace()
        #    #fo = open('soap_envelope.txt', 'w')
        #    #fo.write("\n".join(["%s : %s" % (key, headers[key]) for key in headers.keys()]))
        #    #fo.write(soap_env)
        #    #fo.flush()
        #    #fo.close()
        #    #return (True, "True")

        # send the SOAP envelope
        
        #import requests
        #
        #import logging
        #try:
        #    import http.client as http_client
        #except ImportError:
        #    # Python 2
        #    import httplib as http_client
        #http.client.HTTPConnection.debuglevel = 1

        ## You must initialize logging, otherwise you'll not see debug output.
        #logging.basicConfig()
        #logging.getLogger().setLevel(logging.DEBUG)
        #requests_log = logging.getLogger("requests.packages.urllib3")
        #requests_log.setLevel(logging.DEBUG)
        #requests_log.propagate = True
        #import pdb; pdb.set_trace()
        #r = requests.request('POST', self._soap_server, data=soap_env, headers=headers, cert=(settings.SSL_CERTIFICATE_FILE, settings.SSL_CERTIFICATE_KEY_FILE))
        #print(r.text)

        try:
            if len(settings.SSL_CERTIFICATE_FILE.strip()) > 0 and len(settings.SSL_CERTIFICATE_KEY_FILE.strip()) > 0:
                opener = urllib.request.build_opener(HTTPSClientAuthHandler(settings.SSL_CERTIFICATE_KEY_FILE, settings.SSL_CERTIFICATE_FILE))
                urllib.request.install_opener(opener)
                request = urllib.request.Request(self._soap_server, soap_env.encode(), headers)
                res = urllib.request.urlopen(request, timeout=60)
                response = res.read()
                #print(response)
                if str(response).find("ResponseStatusType:Success") != -1:
                    return (True, response)
                else:
                    return (False, response)
            else:
                print("*****************************")
                print("*    BEGIN urllib debug    *")
                print("*****************************")
                opener = urllib.request.build_opener(urllib.request.HTTPSHandler(debuglevel=1))
                urllib.request.install_opener(opener)
                request = urllib.request.Request(self._soap_server, soap_env.encode(), headers)
                import pprint
                #import pdb; pdb.set_trace()
                print(['%s\n%s'%(key, request.__dict__[key]) for key in request.__dict__.keys()])
                pprint.pprint(request.__dict__)
                res = urllib.request.urlopen(request)
                response = res.read()
                print("*****************************")
                print("*     END urllib debug     *")
                print("*****************************")
                if response.find("ResponseStatusType:Success") != -1:
                    return (True, response)
                else:
                    return (False, response)
        except Exception as e:
            print(e)
            print(e)
            return (False, "An error occurred while sending the SOAP request or receiving the SOAP response")

if __name__ == "__main__":
    ccd_data = """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="CDASchemas\cda\Schemas\CCD.xsl"?>
<ClinicalDocument xmlns="urn:hl7-org:v3" xmlns:voc="urn:hl7-org:v3/voc" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="urn:hl7-org:v3 infrastructure/cda/CDA.xsd">
	<!-- 
********************************************************
CDA Header
********************************************************
-->
	<typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
	<templateId root="2.16.840.1.113883.10.20.1"/> <!-- CCD v1.0 Templates Root --> <!-- CCD SHALL contain one or more ClinicalDocument / templateId. -->
	<id root="db734647-fc99-424c-a864-7e3cda82e703"/>
	<code code="34133-9" codeSystem="2.16.840.1.113883.6.1" displayName="Summarization of episode note"/> <!-- The value for "ClinicalDocument / code" SHALL be "34133-9" "Summarization of episode note" 2.16.840.1.113883.6.1 LOINC STATIC. -->
	<title>2-1-1 Tampa Bay Cares Continuity of Care Document</title>
	<effectiveTime value="20000407130000+0500"/> <!-- ClinicalDocument / effectiveTime SHALL be expressed with precision to include seconds. ClinicalDocument / effectiveTime SHALL include an explicit time zone offset. -->
	<confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
	<languageCode code="en-US"/> <!-- CCD SHALL contain exactly one ClinicalDocument / languageCode. -->
	<recordTarget> <!-- CCD SHALL contain one to two ClinicalDocument / recordTarget -->
		<patientRole>
			<id extension="996-756-495" root="2.16.840.1.113883.19.5"/>
			<patient> <!-- Represents the patient to which the summarization refers. Corresponds to CDA R2 ClinicalDocument / recordTarget. -->
				<name>
					<given>John</given>
					<family>Doe</family>
					<suffix>Sr.</suffix>
				</name>
				<administrativeGenderCode code="M" codeSystem="2.16.840.1.113883.5.1"/>
				<birthTime value="19770701"/>
			</patient>
			<providerOrganization>
				<id root="2.16.840.1.113883.19.5"/>
			    <name>2-1-1 Tampa Bay Cares</name>
			</providerOrganization>
		</patientRole>
	</recordTarget>
	<author> <!-- CCD SHALL contain one or more ClinicalDocument / author / assignedAuthor / assignedPerson and/or ClinicalDocument / author / assignedAuthor / representedOrganization. -->
		<time value="20000407130000+0500"/>
		<assignedAuthor>
			<id root="20cf14fb-b65c-4c8c-a54d-b0cca834c18c"/> <!-- If author has an associated representedOrganization with no assignedPerson or assignedAuthoringDevice, then the value for "ClinicalDocument / author /	assignedAuthor / id / @NullFlavor" SHALL be "NA" "Not applicable" 2.16.840.1.113883.5.1008 NullFlavor STATIC.	-->
			<assignedPerson>
				<name><given>Edward</given><family>Perry</family></name>
			</assignedPerson>
			<representedOrganization>
				<id root="2.16.840.1.113883.19.5"/>
			    <name>2-1-1 Tampa Bay Cares</name>
			</representedOrganization>
		</assignedAuthor>
	</author>
	<!--<informant>
		<assignedEntity>
			<id nullFlavor="NI"/>
			<representedOrganization>
				<id root="2.16.840.1.113883.19.5"/>
			    <name>2-1-1 Tampa Bay Cares</name>
			</representedOrganization>
		</assignedEntity>
	</informant>-->
    <custodian>
		<assignedCustodian>
			<representedCustodianOrganization>
				<id root="2.16.840.1.113883.19.5"/>
			    <name>2-1-1 Tampa Bay Cares</name>
			</representedCustodianOrganization>
		</assignedCustodian>
    </custodian>
	<!-- Commented this section out since we are currently using the HTTP receivingProviderID to designate recipient
	<informationRecipient> <!-- Represents to whom or what the summarization is targeted. Corresponds to the CDA R2 ClinicalDocument / informationRecipient participant. This is optional in both CCR and CDA.  CCD MAY contain one or more ClinicalDocument / informationRecipient. -->
        <intendedRecipient>
            <id root="2.16.840.1.113883.19.5"/>
            <addr>
                <streetAddressLine>Suncoast Center address here</streetAddressLine>
                <city>Saint Petersburg</city>
                <state>Florida</state>
                <postalCode>33710</postalCode>
            </addr>
            <telecom value="tel:(727)333-4444">
            </telecom>
        </intendedRecipient>
    </informationRecipient>-->
	<!--<legalAuthenticator>
		<time value="20000407130000+0500"/>
		<signatureCode code="S"/>
		<assignedEntity>
			<id nullFlavor="NI"/>
			<representedOrganization>
				<id root="2.16.840.1.113883.19.5"/>
			    <name>2-1-1 Tampa Bay Cares</name>
			</representedOrganization>
		</assignedEntity>
	</legalAuthenticator>-->
	<!--<participant typeCode="IND">
		<associatedEntity classCode="GUAR">
			<id root="4ff51570-83a9-47b7-91f2-93ba30373141"/>
			<addr>
				<streetAddressLine>12 Verde Rd.</streetAddressLine>
				<city>Saint Petersburg</city>
				<state>Florida</state>
				<postalCode>33710</postalCode>
			</addr>
			<telecom value="tel:(727)111-2222"/>
			<associatedPerson>
				<name>
					<given>Jim</given>
					<family>Snow</family>
				</name>
			</associatedPerson>
		</associatedEntity>
	</participant>-->
	<documentationOf> 		
		<serviceEvent classCode="PCPR"> <!--A CCD SHALL contain exactly one ClinicalDocument / documentationOf / serviceEvent.  The value for "ClinicalDocument / documentationOf / serviceEvent / @classCode" SHALL be "PCPR" "Care provision" 2.16.840.1.113883.5.6 ActClass STATIC.	-->
			<effectiveTime> <!-- This is where the service event provision period is place (ServiceEvent.StartDate/EndDate) -->
				<low value="19320924"/> <!-- ClinicalDocument / documentationOf / serviceEvent SHALL contain exactly one serviceEvent / effectiveTime / low and exactly one serviveEvent / effectiveTime / high. -->
				<high value="20000407"/>
			</effectiveTime>
			<performer typeCode="PRF">
				<functionCode code="PCP" codeSystem="2.16.840.1.113883.5.88"/> <!-- this specific codeSystem is required -->
				<time><low value="1990"/><high value='20000407'/></time>
				<assignedEntity>
					<id root="20cf14fb-b65c-4c8c-a54d-b0cca834c18c"/>
					<assignedPerson>
						<name><given>Edward</given><family>Perry</family></name>
					</assignedPerson>
					<representedOrganization>
						<id root="2.16.840.1.113883.19.5"/>
					    <name>2-1-1 Tampa Bay Cares</name>
					</representedOrganization>
				</assignedEntity>
			</performer>
		</serviceEvent>
	</documentationOf>
	<!-- Only one Document Body allowed per CCD Doc (see "Purpose" section in CCD docs) -->
	<!-- 
********************************************************
CDA Body
********************************************************
	-->
	<component>
		<structuredBody>
<!--
********************************************************
Purpose section
********************************************************
-->
			<component>
				<section>
					<templateId root='2.16.840.1.113883.10.20.1.13'/> <!-- Purpose section template -->
					<title>Referral for client services from 2-1-1 Tampa Bay Cares</title> <!-- The purpose section SHALL contain Section / title. Section / title SHOULD be valued with a case-insensitive language-insensitive text string containing "purpose".	-->		
					<text>Narrative section.  Referral description, perhaps dynamically generated from call log notes?</text>  <!-- The target of Act / entryRelationship / @typeCode in a purpose activity SHALL be an Act, Encounter, Observation, Procedure, SubstanceAdministration, or Supply. -->
					<entry typeCode="DRIV"> <!-- ECJ: Need to determine which typeCode will be used for a referral. --><!-- The target of Act / entryRelationship / @typeCode in a purpose activity SHALL be an Act, Encounter, Observation, Procedure, SubstanceAdministration, or Supply. -->
						<act classCode="ACT" moodCode="EVN">
							<templateId root='2.16.840.1.113883.10.20.1.30'/> <!-- Purpose activity template -->
							<code code="23745001" codeSystem="2.16.840.1.113883.6.96" displayName="Documentation procedure"/>
							<statusCode code="completed"/>
							<entryRelationship typeCode="RSON">
								<act classCode="ACT" moodCode="EVN">
									<code code="308292007" codeSystem="2.16.840.1.113883.6.96" displayName="Transfer of care"/>
									<statusCode code="completed"/>
								</act>
							</entryRelationship>
						</act>
					</entry>
				</section>
			</component>
		</structuredBody>
    </component>
</ClinicalDocument>"""

    soap = SoapEnv('iH9HiPbW40JbS5m_')
    soap.send_soap_envelope(ccd_data, '885', '003')
