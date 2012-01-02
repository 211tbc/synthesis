#!/usr/bin/python
# -*- coding: utf-8 -*-
import httplib
import sys
import urlparse
import uuid
#from conf inport settings

# these constants will be moved to conf/settings.py
SOAP_SERVER = "http://www.netsmart.com/recipientserver/ProvideAndRegisterDocumentSetRequest"
AUTHOR_PERSON = "John Doe"
AUTHOR_INSTITUTION = "ACME"
AUTHOR_ROLE = "Wise Man"
AUTHOR_SPECIALTY = "Mediation"
NODE_REPRESENTATION = "Not Available"
CODING_SCHEME = "LOINC"
LOCALIZED_STRING = "Not Available"

class SoapEnv():

    def __init__(self):
        self._host = urlparse.urlparse(SOAP_SERVER).netloc
        self._post = urlparse.urlparse(SOAP_SERVER).path
        self._transport_properties = {
            "CCD"                       : "",
            "PAYLOADUUID"               : str(uuid.uuid4()).replace("-", "").upper(),
            "STARTUUID"                 : str(uuid.uuid4()).replace("-", "").upper(),
            "XMLUUID"                   : str(uuid.uuid4()).replace("-", "").upper(),
            "MESSAGEIDUUID"             : str(uuid.uuid4()).replace("-", "").upper(),
            "EXTRINSICOBJECTUUID"       : str(uuid.uuid4()),
            "CLASSIFICATIONSCHEME1UUID" : str(uuid.uuid4()),
            "CLASSIFICATIONSCHEME2UUID" : str(uuid.uuid4()),
            "ACTIONURI"                 : SOAP_SERVER,
            "ASSOCIATION_ID"            : "ID_00000000_0",
            "AUTHORPERSON"              : AUTHOR_PERSON,
            "AUTHORINSTITUTION"         : AUTHOR_INSTITUTION,
            "AUTHORROLE"                : AUTHOR_ROLE,
            "AUTHORSPECIALTY"           : AUTHOR_SPECIALTY,
            "NODEREPRESENTATION"        : NODE_REPRESENTATION,
            "CODINGSCHEME"              : CODING_SCHEME,
            "LOCALIZEDSTRING"           : LOCALIZED_STRING
        }
        
        # define the soap envelope template

        self._ENVELOPE_TEMPLATE = """--MIMEBoundaryurn_uuid_%(XMLUUID)s
Content-Type: application/xop+xml; charset=UTF-8; type="application/soap+xml"
Content-Transfer-Encoding: binary
Content-ID: <0.urn:uuid:%(STARTUUID)s@apache.org>
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing">
    <soapenv:Header>
        <wsa:MessageID>urn:uuid:%(MESSAGEIDUUID)s</wsa:MessageID>
        <wsa:Action>%(ACTIONURI)s</wsa:Action>
    </soapenv:Header>
    <soapenv:Body>
        <xdsb:ProvideAndRegisterDocumentSetRequest xmlns:xdsb="urn:ihe:iti:xds-b:2007">
            <lcm:SubmitObjectsRequest xmlns:lcm="urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0">
                <rim:RegistryObjectList xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
                    <rim:Association
                        associationType="urn:oasis:names:tc:ebxml-regrep:AssociationType:HasMember"
                        sourceObject="SubmissionSet01" targetObject="Document01" id="%(ASSOCIATION_ID)s"
                        objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Association">
                        <rim:Slot name="SubmissionSetStatus">
                            <rim:ValueList>
                                <rim:Value>Original</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                    </rim:Association>
                    <rim:Classification
                        classificationScheme="urn:uuid:%(CLASSIFICATIONSCHEME1UUID)s"
                        classifiedObject="Document01" nodeRepresentation=""
                        objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                        id="id_1">
                        <rim:Slot name="authorPerson">
                            <rim:ValueList>
                                <rim:Value>%(AUTHORPERSON)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        <rim:Slot name="authorInstitution">
                            <rim:ValueList>
                                <rim:Value>%(AUTHORINSTITUTION)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        <rim:Slot name="authorRole">
                            <rim:ValueList>
                                <rim:Value>%(AUTHORROLE)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        <rim:Slot name="authorSpecialty">
                            <rim:ValueList>
                                <rim:Value>%(AUTHORSPECIALTY)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                    </rim:Classification>
                    <rim:Classification
                        classificationScheme="urn:uuid:%(CLASSIFICATIONSCHEME2UUID)s"
                        classifiedObject="Document01" nodeRepresentation="%(NODEREPRESENTATION)s"
                        objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"
                        id="id_2">
                        <rim:Slot name="codingScheme">
                            <rim:ValueList>
                                <rim:Value>%(CODINGSCHEME)s</rim:Value>
                            </rim:ValueList>
                        </rim:Slot>
                        <rim:Name>
                            <rim:LocalizedString value="%(LOCALIZEDSTRING)s"/>
                        </rim:Name>
                    </rim:Classification>
                    <rim:Description />
                    <rim:ExtrinsicObject id="Document01" mimeType="text/plain" objectType="urn:uuid:%(EXTRINSICOBJECTUUID)s">
                    </rim:ExtrinsicObject>
                    <rim:RegistryPackage id="SubmissionSet01"
                        objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:RegistryPackage">
                    </rim:RegistryPackage>
                </rim:RegistryObjectList>
            </lcm:SubmitObjectsRequest>
            <xdsb:Document id="Document01">
                <xop:Include href="cid:1.urn:uuid:%(PAYLOADUUID)s@apache.org" xmlns:xop="http://www.w3.org/2004/08/xop/include"/>
            </xdsb:Document>
        </xdsb:ProvideAndRegisterDocumentSetRequest>
    </soapenv:Body>
</soapenv:Envelope>

--MIMEBoundaryurn_uuid_%(XMLUUID)s
Content-Type: text/xml
Content-Transfer-Encoding: binary
Content-ID: <1.urn:uuid:%(PAYLOADUUID)s@apache.org>

%(CCD)s
--MIMEBoundaryurn_uuid_%(XMLUUID)s""".replace("\t","")

    def send_soap_envelope(self, ccd_data):
        # construct the message and header
        self._transport_properties["CCD"] = ccd_data
        soap_env = self._ENVELOPE_TEMPLATE % self._transport_properties
        if len(soap_env) > 0: # delete this if block        
            print soap_env
            return
        ws = httplib.HTTP(self._host)
        ws.putrequest("POST", self._post)
        ws.putheader("Host", self._host)
        ws.putheader("User-Agent", "synthesis")
        #ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        ws.putheader("Content-type", "multipart/related") # most likely not right
        ws.putheader("boundary", "MIMEBoundaryurn_uuid_{XMLUUID}" % self._transport_properties)
        ws.putheader("type", "application/xop+xml") #  <== don't know if this is needed
        ws.putheader("start", "0.urn:uuid:{STARTUUID}@apache.org" % self._transport_properties) # <== don't know if this is needed and if so then its most likely not right
        ws.putheader("start-info", "application/soap+xml") # <== don't know if this is needed
        ws.putheader("Content-length", "%d" % len(soap_env))
        ws.putheader("SOAPAction", self._host + "/ProvideAndRegisterDocumentSet-b")
        ws.endheaders()

        # send the SOAP envelope
        ws.send(soap_env)

        # check for some sign of success within the response
        status_code, status_message, header = ws.getreply()
        print "Response: ", status_code, status_message
        print "headers: ", header
        response = ws.getfile().read()
        #if response.find("ResponseStatusType:Success"):
        #    return True
        #else:
        #    return False

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

    soap = SoapEnv()
    soap.send_soap_envelope(ccd_data)
