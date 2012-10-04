#!/usr/bin/env/python
# -*- coding: utf-8 -*-
from conf import settings
from conf import outputConfiguration
from Encryption import *
import urllib2
import httplib
from sys import version
import urlparse
import uuid
import base64
import time
from exceptions import SoftwareCompatibilityError
# py 2.5 support
# dynamic import of modules
thisVersion = version[0:3]
if True:
    from lxml import etree as ET
else:
    if float(settings.MINPYVERSION) < float(version[0:3]):
        try:
            # FIXME ( remove this once done debugging namespace issue )
            #import xml.etree.cElementTree as ET
            import xml.etree.ElementTree as ET
            from xml.etree.ElementTree import Element, SubElement, dump
        except ImportError:
            import xml.etree.ElementTree as ET
            from xml.etree.ElementTree import Element, SubElement
    elif thisVersion == '2.4':
        try:
        # Try to use the much faster C-based ET.
            import cElementTree as ET
            from elementtree.ElementTree import Element, SubElement, dump
        except ImportError:
        # Fall back on the pure python one.
            import elementtree.ElementTree as ET
            from elementtree.ElementTree import Element, SubElement
    else:
        print 'Sorry, please see the minimum requirements to run this Application'
        theError = (1100, 'This application requires Python 2.4 or higher.  You are current using version: %s' % (thisVersion), 'import Error XMLDumper.py')
        raise SoftwareCompatibilityError, theError

PRINT_SOAP_REQUEST = True

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):  
    def __init__(self, key, cert):  
        urllib2.HTTPSHandler.__init__(self)  
        self.key = key  
        self.cert = cert  
    def https_open(self, req):  
        #Rather than pass in a reference to a connection class, we pass in  
        # a reference to a function which, for all intents and purposes,  
        # will behave as a constructor  
        return self.do_open(self.getConnection, req)  
    def getConnection(self, host, timeout=300):  
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)  

class SoapEnv():

    def __init__(self, source_id):
        self._soap_server = outputConfiguration.Configuration[source_id]['destinationURL']
        self._encryption_type = outputConfiguration.Configuration[source_id]['encryption']
        self._host = urlparse.urlparse(self._soap_server).netloc
        #self._post = urlparse.urlparse(self._soap_server).path

        # define the soap envelope template

        self._ENVELOPE_TEMPLATE = """--MIMEBoundaryurn_uuid_%(XML_UUID)s
Content-Type: application/xop+xml; charset=UTF-8; type="application/soap+xml"
Content-Transfer-Encoding: binary
Content-ID: <0.urn:uuid:%(START_UUID)s@apache.org>
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing">    
    <soapenv:Header>
        <wsa:MessageID>urn:uuid:%(MESSAGE_ID_UUID)s</wsa:MessageID>
        <wsa:Action soapenv:mustUnderstand="1">urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b</wsa:Action>
        <wsa:To>http://localhost:2647/XdsService/IHEXDSRepository.svc</wsa:To>
        <wsa:ReplyTo soapenv:mustUnderstand="1">
            <wsa:Address>https://pix.penguix.net:8024/docs</wsa:Address>
        </wsa:ReplyTo>
    </soapenv:Header>
    <soapenv:Body>
        <xdsb:ProvideAndRegisterDocumentSetRequest xmlns:xdsb="urn:ihe:iti:xds-b:2007">
            <lcm:SubmitObjectsRequest xmlns:lcm="urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0">
                <rim:RegistryObjectList xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
                    <rim:ExtrinsicObject id="%(DOCUMENT_OBJECT)s" mimeType="text/plain" objectType="urn:uuid:%(EXTRINSIC_OBJECT_UUID)s">
                        <rim:Slot name="creationTime">
                            <rim:ValueList>
                                <rim:Value>%(CREATION_TIME)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        <rim:Slot name="languageCode">
                            <rim:ValueList>
                                <rim:Value>%(LANGUAGE_CODE)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        %(SERVICE_START_TIME)s
                        %(SERVICE_STOP_TIME)s
                        <rim:Slot name="sourcePatientId">
                            <rim:ValueList>
                                <rim:Value>%(SOURCE_PATIENT_ID)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        %(SOURCE_PATIENT_INFO)s
                        %(EXTRINSIC_NAME_TAG)s
                        %(EXTRINSIC_DESCRIPTION_TAG)s
                        <rim:Classification
                            classificationScheme="urn:uuid:%(EXTRINSIC_UUID)s"
                            classifiedObject="%(DOCUMENT_OBJECT)s" nodeRepresentation=""
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_1">
                            <rim:Slot name="authorPerson">
                                <rim:ValueList>
                                    <rim:Value>%(EXTRINSIC_AUTHOR_PERSON)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            %(EXTRINSIC_AUTHOR_INSTITUTION_SLOT)s
                            %(EXTRINSIC_AUTHOR_ROLE_SLOT)s
                            %(EXTRINSIC_AUTHOR_SPECIALTY_SLOT)s
                        </rim:Classification>
                        <rim:Classification
                            classificationScheme="urn:uuid:%(CLASS_CODE_UUID)s"
                            classifiedObject="%(DOCUMENT_OBJECT)s" nodeRepresentation="%(CLASS_CODE_NODE_REPRESENTATION)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_3">
                            <rim:Slot name="codingScheme">
                                <rim:ValueList>
                                    <rim:Value>%(CLASS_CODE_VALUE)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            <rim:Name>
                                <rim:LocalizedString value="%(CLASS_CODE_NAME)s"/>
                            </rim:Name>
                        </rim:Classification>
                        <rim:Classification
                            classificationScheme="urn:uuid:%(CONFIDENTIALITY_CODE_UUID)s"
                            classifiedObject="%(DOCUMENT_OBJECT)s" nodeRepresentation="%(CONFIDENTIALITY_CODE_NODE_REPRESENTATION)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_4">
                            <rim:Slot name="codingScheme">
                                <rim:ValueList>
                                    <rim:Value>%(CONFIDENTIALITY_CODE_VALUE)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            <rim:Name>
                                <rim:LocalizedString value="%(CONFIDENTIALITY_CODE_NAME)s"/>
                            </rim:Name>
                        </rim:Classification>
                        <rim:Classification
                            classificationScheme="urn:uuid:%(FORMAT_CODE_UUID)s"
                            classifiedObject="%(DOCUMENT_OBJECT)s" nodeRepresentation="%(FORMAT_CODE_NODE_REPRESENTATION)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_5">
                            <rim:Slot name="codingScheme">
                                <rim:ValueList>
                                    <rim:Value>%(FORMAT_CODE_VALUE)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            <rim:Name>
                                <rim:LocalizedString value="%(FORMAT_CODE_NAME)s"/>
                            </rim:Name>
                        </rim:Classification>
                        <rim:Classification
                            classificationScheme="urn:uuid:%(HEALTHCARE_FACILITY_TYPE_CODE_UUID)s"
                            classifiedObject="%(DOCUMENT_OBJECT)s" nodeRepresentation="%(HEALTHCARE_FACILITY_TYPE_CODE_NODE_REPRESENTATION)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_6">
                            <rim:Slot name="codingScheme">
                                <rim:ValueList>
                                    <rim:Value>%(HEALTHCARE_FACILITY_TYPE_CODE_VALUE)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            <rim:Name>
                                <rim:LocalizedString value="%(HEALTHCARE_FACILITY_TYPE_CODE_NAME)s"/>
                            </rim:Name>
                        </rim:Classification>
                        <rim:Classification
                            classificationScheme="urn:uuid:%(PRACTICE_SETTING_CODE_UUID)s"
                            classifiedObject="%(DOCUMENT_OBJECT)s" nodeRepresentation="%(PRACTICE_SETTING_CODE_NODE_REPRESENTATION)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_7">
                            <rim:Slot name="codingScheme">
                                <rim:ValueList>
                                    <rim:Value>%(PRACTICE_SETTING_CODE_VALUE)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            <rim:Name>
                                <rim:LocalizedString value="%(PRACTICE_SETTING_CODE_NAME)s"/>
                            </rim:Name>
                        </rim:Classification>
                        <rim:Classification
                            classificationScheme="urn:uuid:%(TYPE_CODE_UUID)s"
                            classifiedObject="%(DOCUMENT_OBJECT)s" nodeRepresentation="%(TYPE_CODE_NODE_REPRESENTATION)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_8">
                            <rim:Slot name="codingScheme">
                                <rim:ValueList>
                                    <rim:Value>%(TYPE_CODE_VALUE)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            <rim:Name>
                                <rim:LocalizedString value="%(TYPE_CODE_NAME)s"/>
                            </rim:Name>
                        </rim:Classification>
                        <rim:ExternalIdentifier
                            identificationScheme="urn:uuid:%(DOCUMENT_ENTRY_PATIENTID_UUID)s"
                            value="%(PATIENT_ID)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier"
                            id="id_9" registryObject="%(DOCUMENT_OBJECT)s">
                            <rim:Name>
                                <rim:LocalizedString value="XDSDocumentEntry.patientId"/>
                            </rim:Name>
                        </rim:ExternalIdentifier>
                        <rim:ExternalIdentifier
                            identificationScheme="urn:uuid:%(DOCUMENT_ENTRY_UNIQUEID_UUID)s"
                            value="%(UNIQUE_ID)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier"
                            id="id_10" registryObject="%(DOCUMENT_OBJECT)s">
                            <rim:Name>
                                <rim:LocalizedString value="XDSDocumentEntry.uniqueId"/>
                            </rim:Name>
                        </rim:ExternalIdentifier>
                    </rim:ExtrinsicObject>
                    <rim:RegistryPackage id="%(SOURCE_OBJECT)s"
                        objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:RegistryPackage">
                        <rim:Slot name="submissionTime">
                            <rim:ValueList>
                                <rim:Value>%(SUBMISSION_TIME)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        %(REGISTRY_PACKAGE_NAME_TAG)s
                        %(REGISTRY_PACKAGE_DESCRIPTION_TAG)s
                        <rim:Classification
                            classificationScheme="urn:uuid:%(REGISTRY_UUID)s"
                            classifiedObject="%(SOURCE_OBJECT)s" nodeRepresentation=""
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_11">
                            <rim:Slot name="authorPerson">
                                <rim:ValueList>
                                    <rim:Value>%(REGISTRY_AUTHOR_PERSON)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            %(REGISTRY_AUTHOR_INSTITUTION_SLOT)s
                            %(REGISTRY_AUTHOR_ROLE_SLOT)s
                            %(REGISTRY_AUTHOR_SPECIALTY_SLOT)s
                        </rim:Classification>
                        <rim:Classification
                            classificationScheme="urn:uuid:%(CONTENT_TYPE_CODE_UUID)s"
                            classifiedObject="%(SOURCE_OBJECT)s" nodeRepresentation="%(CONTENT_TYPE_CODE_NODE_REPRESENTATION)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                            id="id_2">
                            <rim:Slot name="codingScheme">
                                <rim:ValueList>
                                    <rim:Value>%(CONTENT_TYPE_CODE_CODING_SCHEME)s</rim:Value>
                                </rim:ValueList>
                            </rim:Slot>
                            <rim:Name>
                                <rim:LocalizedString value="%(CONTENT_TYPE_CODE_LOCALIZED_STRING)s"/>
                            </rim:Name>
                        </rim:Classification>
                        <rim:ExternalIdentifier
                            identificationScheme="urn:uuid:%(REGISTRY_PACKAGE_UNIQUE_ID_UUID)s"
                            value="%(UNIQUE_ID)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier"
                            id="id_13" registryObject="%(SOURCE_OBJECT)s">
                            <rim:Name>
                                <rim:LocalizedString value="XDSSubmissionSet.uniqueId"/>
                            </rim:Name>
                        </rim:ExternalIdentifier>
                        <rim:ExternalIdentifier
                            identificationScheme="urn:uuid:%(REGISTRY_PACKAGE_SOURCE_ID_UUID)s"
                            value="%(SOURCE_ID)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier"
                            id="id_14" registryObject="%(SOURCE_OBJECT)s">
                            <rim:Name>
                                <rim:LocalizedString value="XDSSubmissionSet.sourceId"/>
                            </rim:Name>
                        </rim:ExternalIdentifier>
                        <rim:ExternalIdentifier
                            identificationScheme="urn:uuid:%(REGISTRY_PACKAGE_PATIENT_ID_UUID)s"
                            value="%(PATIENT_ID)s"
                            objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:ExternalIdentifier"
                            id="id_15" registryObject="%(SOURCE_OBJECT)s">
                            <rim:Name>
                                <rim:LocalizedString value="XDSSubmissionSet.patientId"/>
                            </rim:Name>
                        </rim:ExternalIdentifier>
                    </rim:RegistryPackage>
                    <rim:Classification classifiedObject="SubmissionSet01"
                        classificationNode="urn:uuid:%(SUBMISSION_SET_UUID)s" id="%(SUBMISSION_SET_ID)s"
                        objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"/>
                    %(ASSOCIATION_SECTION)s
                </rim:RegistryObjectList>
            </lcm:SubmitObjectsRequest>
            %(ATTACHMENT_SECTION)s
        </xdsb:ProvideAndRegisterDocumentSetRequest>
    </soapenv:Body>
</soapenv:Envelope>%(MIME_BORDER_SECTION)s""".replace("\t","")

    def send_soap_envelope(self, ccd_data):
        
        print "soaptransport generating soap"

        soap_transport_properties = settings.SOAP_TRANSPORT_PROPERTIES

        #
        # FBY: TODO: I'm not sure what the SOAP envelope should look like if ccd_data
        #            contains multiple documents. For now, I'm only ever interested in
        #            ccd_data[0]

        ccd = ET.fromstring(ccd_data[0])

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
        snapshot = str(t[0])+str(t[1]).zfill(2)+str(t[2]).zfill(2)
        soap_transport_properties["CREATION_TIME"] = snapshot

        # Patient ID <== Where does this come from?
        soap_transport_properties["PATIENT_ID"] = "ef77eeda67dd4a2^^^&amp;1.3.6.1.4.1.21367.2005.3.7&amp;ISO"

        # Source ID <== Where does this come from?
        soap_transport_properties["SOURCE_ID"] = "1.3.6.1.4.1.21367.2009.1.2.1"

        # Unique ID <== Where does this come from?
        soap_transport_properties["UNIQUE_ID"] = "1.2009.0827.08.33.5017"

        # Random UUIDs
        soap_transport_properties["START_UUID"] = str(uuid.uuid4()).replace("-", "").upper()
        soap_transport_properties["XML_UUID"] = str(uuid.uuid4()).replace("-", "").upper()
        soap_transport_properties["MESSAGE_ID_UUID"] = str(uuid.uuid4()).replace("-", "").upper()
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

        # if RegistryPackage has a name attribute ...
        if len(orig_REGISTRY_PACKAGE_NAME_TAG) > 0:
            soap_transport_properties["REGISTRY_PACKAGE_NAME_TAG"] = """<rim:Name><rim:LocalizedString value="%s"/></rim:Name>""" % orig_REGISTRY_PACKAGE_NAME_TAG
        else:
            soap_transport_properties["REGISTRY_PACKAGE_NAME_TAG"] = "<rim:Name/>"

        # if RegistryPackage has a description attribute ... 
        if len(orig_REGISTRY_PACKAGE_DESCRIPTION_TAG) > 0:
            soap_transport_properties["REGISTRY_PACKAGE_DESCRIPTION_TAG"] = """<rim:Description><rim:LocalizedString value="%s"/></rim:Description>""" % orig_REGISTRY_PACKAGE_DESCRIPTION_TAG
        else:
            soap_transport_properties["REGISTRY_PACKAGE_DESCRIPTION_TAG"] = "<rim:Description/>"

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

        # Attachments
        for data in ccd_data:
            payload_uuid = str(uuid.uuid4()).replace("-", "").upper()
            ccd = ET.fromstring(data)
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
            attachment = data
            if self._encryption_type != "none":
                if self._encryption_type == "3des":
                    keyiv = get_incoming_3des_key_iv()
                    des3 = DES3()
                    attachment = base64.b64encode(des3.encrypt(data, keyiv['key'], iv=keyiv['iv']))
                if self._encryption_type == "openpgp":
                    gpg = GPG()
                    attachment = base64.b64encode(gpg.encrypt(data))
            soap_transport_properties["MIME_BORDER_SECTION"] += """

--MIMEBoundaryurn_uuid_%s
Content-Type: text/xml; charset=us-ascii
Content-Transfer-Encoding: 7bit
Content-ID: <1.urn:uuid:%s@apache.org>
Content-Disposition: attachment; name="uuid_%s.xml"

%s
--MIMEBoundaryurn_uuid_%s""" % (soap_transport_properties["XML_UUID"], payload_uuid, payload_uuid, attachment, soap_transport_properties["XML_UUID"])

        # generate the SOAP envelope
        soap_env = self._ENVELOPE_TEMPLATE % soap_transport_properties

        # create header
        headers = {
            "Host"              : self._host,
            "User-Agent"        : "synthesis",
            "Accept-Encoding"   : "gzip,deflate",
            "Connection"        : "Keep-Alive",
            "MIME-Version"      : "1.0",
            "Content-type"      : "multipart/related",
            "boundary"          : "MIMEBoundaryurn_uuid_%(XML_UUID)s" % soap_transport_properties,
            "type"              : "application/xop+xml",
            "start"             : "0.urn:uuid:%(START_UUID)s@apache.org" % soap_transport_properties,
            "start-info"        : "application/soap+xml",
            "Content-length"    : "%d" % len(soap_env),
            "action"            : "urn:ihe:iti:xds-b:2007:ProvideAndRegisterDocumentSet-b",
            }

        if PRINT_SOAP_REQUEST: # delete this if block
            import pprint as pp
            pp.pprint(headers)
            print soap_env
            #fo = open('soap_envelope.txt', 'w')
            #fo.write(soap_env)
            #fo.flush()
            #fo.close()
            #return (True, "True")

        # send the SOAP envelope
        try:
            if len(settings.SSL_CERTIFICATE_FILE.strip()) > 0 and len(settings.SSL_CERTIFICATE_KEY_FILE.strip()) > 0:
                opener = urllib2.build_opener(HTTPSClientAuthHandler(settings.SSL_CERTIFICATE_KEY_FILE, settings.SSL_CERTIFICATE_FILE))
                urllib2.install_opener(opener)
                request = urllib2.Request(self._soap_server, soap_env, headers)
                res = urllib2.urlopen(request)
                response = res.read()
                if response.find("ResponseStatusType:Success") != -1:
                    return (True, response)
                else:
                    return (False, response)
            else:
                opener = urllib2.build_opener(urllib2.HTTPSHandler(debuglevel=1))
                urllib2.install_opener(opener)
                request = urllib2.Request(self._soap_server, soap_env, headers)
                res = urllib2.urlopen(request)
                response = res.read()
                if response.find("ResponseStatusType:Success") != -1:
                    return (True, response)
                else:
                    return (False, response)                
        except Exception as e:
            print e
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
	<code code="34133-9" codeSystem="2.16.840.1.113883.6.1" displayName="Summarization of episode note"/> <!-- The value for “ClinicalDocument / code” SHALL be “34133-9” “Summarization of episode note” 2.16.840.1.113883.6.1 LOINC STATIC. -->
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
			<id root="20cf14fb-b65c-4c8c-a54d-b0cca834c18c"/> <!-- If author has an associated representedOrganization with no assignedPerson or assignedAuthoringDevice, then the value for “ClinicalDocument / author /	assignedAuthor / id / @NullFlavor” SHALL be “NA” “Not applicable” 2.16.840.1.113883.5.1008 NullFlavor STATIC.	-->
			<assignedPerson>
				<name><prefix>Dr.</prefix><given>Robert</given><family>Dolin</family></name>
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
    </informationRecipient>
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
		<serviceEvent classCode="PCPR"> <!--A CCD SHALL contain exactly one ClinicalDocument / documentationOf / serviceEvent.  The value for “ClinicalDocument / documentationOf / serviceEvent / @classCode” SHALL be “PCPR” “Care provision” 2.16.840.1.113883.5.6 ActClass STATIC.	-->
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
						<name><prefix>Dr.</prefix><given>Robert</given><family>Dolin</family></name>
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
					<code code="48764-5" codeSystem="2.16.840.1.113883.6.1"/> <!-- The purpose section SHALL contain Section / code.  The value for “Section / code” SHALL be “48764-5” “Summary purpose” 2.16.840.1.113883.6.1 LOINC STATIC. -->
					<title>Referral for client services from 2-1-1 Tampa Bay Cares</title> <!-- The purpose section SHALL contain Section / title. Section / title SHOULD be valued with a case-insensitive language-insensitive text string containing “purpose”.	-->						
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
    soap.send_soap_envelope(ccd_data)
