from interpretpicklist import Interpretpicklist
import dateutils
from datetime import datetime
import xmlutilities
from exceptions import SoftwareCompatibilityError, DataFormatError
import logger
from sys import version
import dbobjects
from writer import Writer
from zope.interface import implements
from sqlalchemy import or_, and_, between
from conf import settings
# py 2.5 support
# dynamic import of modules
thisVersion = version[0:3]
if float(settings.MINPYVERSION) < float(version[0:3]):
    try:
        import xml.etree.cElementTree as ET
        from xml.etree.ElementTree import dump
    except ImportError:
        import xml.etree.ElementTree as ET
        from xml.etree.ElementTree import dump
elif thisVersion == '2.4':
    try:    # Try to use the much faster C-based ET.
        import cElementTree as ET
        from elementtree.ElementTree import dump
    except ImportError:    # Fall back on the pure python one.
        import elementtree.ElementTree as ET
else:
    print 'Sorry, please see the minimum requirements to run this Application'
    theError = (1100, 'This application requires Python 2.4 or higher.  You are current using version: %s' % (thisVersion), 'import Error XMLDumper.py')
    raise SoftwareCompatibilityError, theError

class hl7CCDwriter():   # Health Level 7 Continuity of Care Document
    implements (Writer) # Writer Interface

    def __init__(self, poutDirectory, processingOptions, debugMessages=None):
        print "==== %s Class Initialized" % self.__class__  # JCS-Doesn't have a __name__

        if settings.DEBUG:
            print "XML File to be dumped to: %s" % poutDirectory
            self.log = logger.Logger(configFile=settings.LOGGING_INI, loglevel=40)

        self.outDirectory = poutDirectory
        self.pickList = Interpretpicklist()
        self.options = processingOptions
        self.errorMsgs = [] # SBB20070628 adding a buffer for errors to be displayed at the end of the process.

        self.db = dbobjects.DB()            # JCS 10/05/11
        self.db.Base.metadata.create_all()
        self.hl7dateform = "%Y%m%d%H%M%S%z"
	
    def write(self):    # Called from nodebuilder.run() one time.
        self.session = self.db.Session()
        #self.startTransaction()    # This is only for updateReported()
        if settings.DEBUG:
            print '==== Self:', self
        # Database traversal:
        # Step through Exports. For each Export,
        # Step through Persons. For each person,
        # Step through ServiceEvent. For each Service Event, begin a new document, then
        # Step through Entrys
        # Step through ServiceEventNotes - concat all note_text into one. 
        exports = self.session.query(dbobjects.Export)
        for oneExport in exports:
            selink = self.session.query(dbobjects.SourceExportLink).filter(
                                        dbobjects.SourceExportLink.export_index_id == oneExport.id).one()
            #print '==== Selink.id:', selink.id
            oneSource = self.session.query(dbobjects.Source).filter(dbobjects.Source.id == selink.source_index_id).one()
            #print '==== Source.id:', source.id
            #self.configRec = self.session.query(dbobjects.SystemConfiguration).filter(and_(dbobjects.SystemConfiguration.source_id
            #                     == source.source_id, dbobjects.SystemConfiguration.processing_mode == settings.MODE)).one()
            #print '==== sys config.id', self.configRec.id
            persons = oneExport.fk_export_to_person  # = relationship('Person', backref='fk_person_to_export')

            for onePerson in persons:

               #ServEvts = self.session.query(dbobjects.ServiceEvent).filter(dbobjects.ServiceEvent.export_index_id == oneExport.id)
                ServEvts = self.session.query(dbobjects.ServiceEvent).filter(dbobjects.ServiceEvent.person_index_id == onePerson.id)
                for oneServEvt in ServEvts: # One document per event???
                    #print "person is: ", self.person
                    self.processXML(oneExport, onePerson, oneServEvt, oneSource)       # Create one document
                    xmlutilities.indent(self.root_element)  #self.prettify()
                    # Next wraps self.root_element in an ElementTree and writes it to disk
                    xmlutilities.writeOutXML(self, xml_declaration=True, encoding="UTF-8")	# JCS - no declaration w/o encoding

        #self.session.commit()       # This is only for updateReported()
        return True     # Now nodebuilder.run() will find all output files and validate them.

    def newSubNode(self, parent, nodeName):
        newNode = ET.SubElement(parent, nodeName)
        return newNode

    def processXML(self, oneExport, onePerson, oneServEvt, oneSource):
        if settings.DEBUG:
            print "==== Starting hl7CCDwriter.processXML"
        # That which everything else will live inside of
        self.root_element = self.createDoc() # makes root element (not elementTree) with XML header attributes
        print '==== root created'
        # Required elements
        typeId = ET.SubElement(self.root_element, "typeId")
        typeId.attrib["extension"] = "POCD_HD000040"
        typeId.attrib["root"] = "2.16.840.1.113883.1.3"
        self.addTemplateId(self.root_element, "")
        cdid = ET.SubElement(self.root_element, "id")
        cdid.attrib["extension"] = oneExport.export_id_id_num # TODO Done?"1"  # ExportID.IDNum  ..or.. ServiceEventID.IDNum .or. 
                                                    # ReferralID.IDNum *I think this will just be an extension
        cdid.attrib["root"] = "db734647-fc99-424c-a864-7e3cda82e703"

        self.addCodeSys(self.root_element, "34133-9", ".6.1", "Summarization of episode note")
        title = ET.SubElement(self.root_element,"title")
        title.text = "2-1-1 Tampa Bay Cares Continuity of Care Document"
        effTime = ET.SubElement(self.root_element, "effectiveTime")
        effTime.attrib["value"] = oneExport.export_date.strftime(self.hl7dateform) #TODO Done? "+0500"#"20000407130000+0500"# ExportDate
        confiCode = ET.SubElement(self.root_element,"confidentialityCode")
        confiCode.attrib["code"] = "Y"
        confiCode.attrib["codeSystem"] = "2.16.840.1.113883.5.25"
        langCode = ET.SubElement(self.root_element,"languageCode")
        langCode.attrib["code"] = "en-US"

        recTarget = ET.SubElement(self.root_element,"recordTarget")             # Root 1
        patientRole = ET.SubElement(recTarget,"patientRole")
        prId = ET.SubElement(patientRole,"id")
        prId.attrib["extension"] = onePerson.person_id_id_num #"996756A495"     # TODO Done? PersonID.IDNum>2090888539 
        prId.attrib["root"] = "2.16.840.1.113883.19.5"
        patient = ET.SubElement(patientRole,"patient")
        self.addAName(patient, '', onePerson.person_legal_first_name_unhashed,
                                   onePerson.person_legal_last_name_unhashed,
                                   onePerson.person_legal_suffix_unhashed)    # TODO Done?  ?LegalMiddleName.Unhashed
        gendCode = ET.SubElement(patient,"administrativeGenderCode")
        gendCode.attrib["code"] = "M" #str(onePerson.person_gender_unhashed)  # TODO ??? Gender.Unhashed>2   ,Not Mappable,
        gendCode.attrib["codeSystem"] = "2.16.840.1.113883.5.1"
        gendCode.attrib["codeSystemName"] = "AdministrativeGenderCode"
        birthTime = ET.SubElement(patient,"birthTime")
        birthTime.attrib["value"] = onePerson.person_date_of_birth_unhashed.strftime(self.hl7dateform) #"19770701" # TODO Done?
        self.races = onePerson.fk_person_to_races
        raceCode = ET.SubElement(patient,"raceCode")
        raceCode.attrib["code"] = "1002-5"          # TODO Need code map?  races.race_unhashed Somewhere in here??? > 2 

        raceCode.attrib["codeSystem"] = "2.16.840.1.113883.6.238" 
        raceCode.attrib["codeSystemName"] = "CDC Race and Ethnicity"
        ethCode = ET.SubElement(patient,"ethnicGroupCode")
        ethCode.attrib["code"] = "2186-5"                 # TODO Need code map?  onePerson.person_ethnicity_unhashed >1 
        ethCode.attrib["codeSystem"] = "2.16.840.1.113883.5.50" 
        ethCode.attrib["codeSystemName"] = "Race and Ethnicity Code Sets"
        providOrg = ET.SubElement(patientRole,"providerOrganization")
        self.addGroupId(providOrg, oneSource.source_id_id_str, oneSource.source_name)	# TODO Done parm2 parm3

        auth = ET.SubElement(self.root_element,"author")                        # Root 2
        authTime = ET.SubElement(auth,"time")
        authTime.attrib["value"] = "20000407130000+0500"
        asgdAuth = ET.SubElement(auth,"assignedAuthor")
        authId = ET.SubElement(asgdAuth,"id")
        authId.attrib["root"] = "20cf14fb-b65c-4c8c-a54d-b0cca834c18c"
        asgdPerson = ET.SubElement(asgdAuth,"assignedPerson")
        self.addAName(asgdPerson, "Dr.", "Robert", "Dolin", None)
        repOrg = ET.SubElement(asgdAuth,"representedOrganization")
        self.addGroupId(repOrg, "", "2-1-1 Tampa Bay Cares")

        custodian = ET.SubElement(self.root_element,"custodian")                # Root 3
        assigned  = ET.SubElement(custodian,"assignedCustodian")
        custodOrg = ET.SubElement(assigned,"representedCustodianOrganization")
        self.addGroupId(custodOrg, "", "2-1-1 Tampa Bay Cares")

        infoRec  = ET.SubElement(self.root_element,"informationRecipient")      # Root 4
        intended = ET.SubElement(infoRec,"intendedRecipient")
        intendId = ET.SubElement(intended,"id")
        intendId.attrib["root"] = "2.16.840.1.113883.19.5"
        self.addAnAddress(intended, "Suncoast Center address here", "Saint Petersburg", "Florida", "33710")
        IntendTel = ET.SubElement(intended,"telecom")
        IntendTel.attrib["value"] = "tel:(727)333-4444"

        legalAuth = ET.SubElement(self.root_element,"legalAuthenticator")       # Root 5
        legalTime = ET.SubElement(legalAuth,"time")
        legalTime.attrib["value"] = "20111223130000+0500"
        sigCode = ET.SubElement(legalAuth,"signatureCode")
        sigCode.attrib["code"] = "S"
        legalEnt = ET.SubElement(legalAuth,"assignedEntity")
        leId = ET.SubElement(legalEnt,"id")
        leId.attrib["nullFlavor"] = "NI"
        leAsPer = ET.SubElement(legalEnt,"assignedPerson")
        leAsName = ET.SubElement(leAsPer,"name")
        leAsName.text = "Edward Perry"
        leRepOrg = ET.SubElement(legalEnt,"representedOrganization")
        self.addGroupId(leRepOrg, "11", "2-1-1 Tampa Bay Cares")

        participant = ET.SubElement(self.root_element,"participant")            # Root 6
        participant.attrib["typeCode"] = "IND"
        assocEnt = ET.SubElement(participant,"associatedEntity")
        assocEnt.attrib["classCode"] = "GUAR"
        aeId = ET.SubElement(assocEnt,"id")
        aeId.attrib["root"] = "4ff51570-83a9-47b7-91f2-93ba30373141"
        self.addAnAddress(assocEnt, "12 Verde Rd.", "Saint Petersburg", "Florida", "33710")
        aeTel = ET.SubElement(assocEnt,"telecom")
        aeTel.attrib["value"] = "tel:(727)111-2222"
        aePers = ET.SubElement(assocEnt,"associatedPerson")
        self.addAName(aePers, "", "Jim", "Snow", "")
        #           TODO Should be telecom node here? under aePers? PersonPhoneNumber>2346543210 

        docuOf = ET.SubElement(self.root_element,"documentationOf")             # Root 7
        srvEvent = ET.SubElement(docuOf,"serviceEvent")
        srvEvent.attrib["classCode"] = "PCPR"
        seeTime = ET.SubElement(srvEvent,"effectiveTime")
        ET.SubElement(seeTime,"low").attrib["value"] = oneServEvt.service_event_provision_date.strftime(self.hl7dateform) # TODO Done?
        ET.SubElement(seeTime,"high").attrib["value"] = "20000407"
        seePerf = ET.SubElement(srvEvent,"performer")
        seePerf.attrib["typeCode"] = "PRF"
        seeFunc = ET.SubElement(seePerf,"functionCode")
        seeFunc.attrib["code"] = "PCP"
        seeFunc.attrib["codeSystem"] = "2.16.840.1.113883.5.88"
        #<!--<time>	<low value="1990"/>	<high value='20000407'/>	</time>-->
        seeEnt = ET.SubElement(seePerf,"assignedEntity")
        seeEntId = ET.SubElement(seeEnt,"id")
        seeEntId.attrib["extension"] = oneServEvt.site_service_id #"211"# TODO Need. OR? ServiceEvent.SiteServiceID<->1766  What is:
                                                    # ClinicalDocument . documentationOf . serviceEvent @ classCode to 'PCPR'
        seeEntId.attrib["root"] = "20cf14fb-b65c-4c8c-a54d-b0cca834c18c"
        seePers = ET.SubElement(seeEnt,"assignedPerson")
        self.addAName(seePers, "", "Robert", "Dolin", "")
        seeRep = ET.SubElement(seeEnt,"representedOrganization")
        self.addGroupId(seeRep, oneSource.source_id_id_str, oneSource.source_name) # TODO Done? parm 2, 3 

        compon = ET.SubElement(self.root_element,"component")                   # Root 8
        struBod = ET.SubElement(compon,"structuredBody")
        componB = ET.SubElement(struBod,"component")
        section = ET.SubElement(componB,"section")
        self.addTemplateId(section, ".13")
        self.addCodeSys(section, "48764-5", ".6.1", "")
        secTitle = ET.SubElement(section,"title")
        secTitle.text = "Referral for client services from 2-1-1 Tampa Bay Cares"
        temp = ""
        seNotes = self.session.query(dbobjects.ServiceEventNotes).filter(dbobjects.ServiceEventNotes.service_event_index_id
                                 == oneServEvt.id)
        for note in seNotes:
            if note.note_text != "":
                temp = "\n".join([temp, note.note_text])    # TODO ServiceEventNotes.note.NoteText> multi?
        ET.SubElement(section,"text").text = temp.lstrip()  # multi node fails...

        entry = ET.SubElement(section,"entry")   # Can be multi...?
        entry.attrib["typeCode"] = "DRIV"
        entAct = ET.SubElement(entry,"act")
        entAct.attrib["classCode"] = "ACT"
        entAct.attrib["moodCode"] = "RQO"
        self.addTemplateId(entAct, ".30")
        self.addCodeSys(entAct, "23745001", ".6.96", "Documentation procedure")
        ET.SubElement(entAct,"statusCode").attrib["code"] = "completed"

        entRel = ET.SubElement(entAct,"entryRelationship")
        entRel.attrib["typeCode"] = "RSON"
        subAct = ET.SubElement(entRel,"act")
        subAct.attrib["classCode"] = "ACT"
        subAct.attrib["moodCode"] = "EVN"
        self.addCodeSys(subAct, "308292007", ".6.96", "Transfer of care")
        ET.SubElement(subAct,"statusCode").attrib["code"] = "completed"

        entry2 = ET.SubElement(section,"entry")   # Can be multi...
        entEnc = ET.SubElement(entry2,"encounter") #, attributes={"classCode":"ACT","moodCode":"EVN"})
        entEnc.attrib["classCode"] = "ACT"
        entEnc.attrib["moodCode"] = "EVN"
        return          # End of ProcessXML()		

    def createDoc(self):
        # What about:  # targetNamespace="urn:hl7-org:v3" xmlns:mif="urn:hl7-org:v3/mif" xmlns="urn:hl7-org:v3"
        root_element = ET.Element("ClinicalDocument")
        root_element.attrib["xmlns"] = "urn:hl7-org:v3"
        root_element.attrib["xmlns:voc"] = "urn:hl7-org:v3/voc"
        #root_element.attrib["xmlns:mif"] = "urn:hl7-org:v3/mif"
        root_element.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        root_element.attrib["xsi:schemaLocation"] = "urn:hl7-org:v3 infrastructure/cda/CDA.xsd"
        #root_element.text = "\n"
        return root_element

    def addCodeSys(self, parentNode, theCode, sysMore, dispName):
        code = ET.SubElement(parentNode, "code")
        code.attrib["code"] = theCode
        code.attrib["codeSystem"] = "2.16.840.1.113883" + sysMore
        if not isNullOrMT(dispName):
            code.attrib["displayName"] = dispName

    def addTemplateId(self, parentNode, sysMore):    # Never has sub-nodes??
        templateId = ET.SubElement(parentNode, "templateId")
        templateId.attrib["root"] = "2.16.840.1.113883.10.20.1" + sysMore

    def addAName(self, parentNode, pr, fi, la, su):
        name = ET.SubElement(parentNode, "name")
        if not isNullOrMT(pr):
            namPr = ET.SubElement(name,"prefix")
            namPr.text = pr
        if not isNullOrMT(fi):
            namFi = ET.SubElement(name,"given")
            namFi.text = fi
        if not isNullOrMT(la):
            namLa = ET.SubElement(name,"family")
            namLa.text = la
        if not isNullOrMT(su):
            namSu = ET.SubElement(name,"suffix")
            namSu.text = su

    def addGroupId(self, parentNode, extension, groupNameText):
        groupId = ET.SubElement(parentNode, "id")
        groupId.attrib["root"] = "2.16.840.1.113883.19.5"
        if not isNullOrMT(extension):
            groupId.attrib["extension"] = extension
        if not isNullOrMT(groupNameText):
            groupName = ET.SubElement(parentNode,"name")
            groupName.text = groupNameText

    def addAnAddress(self, parentNode, street, city, state, postalCode ):
        address = ET.SubElement(parentNode,"addr")
        if not isNullOrMT(street):
            addStr = ET.SubElement(address,"streetAddressLine")
            addStr.text = street
        if not isNullOrMT(city):
            addCty = ET.SubElement(address,"city")
            addCty.text = city
        if not isNullOrMT(state):
            addSta = ET.SubElement(address,"state")
            addSta.text = state
        if not isNullOrMT(postalCode):
            addZip = ET.SubElement(address,"postalCode")
            addZip.text = postalCode
	
#    def updateReported(self, currentObject):
#        # update the reported field of the currentObject being passed in.  These should all exist.
#        try:
#            if settings.DEBUG:
#                print 'Updating reporting for object: %s' % currentObject.__class__
#            currentObject.reported = True
#            #self.commitTransaction()
#        except:
#            print "Exception occurred during update the 'reported' flag"
#            pass

    def dumpErrors(self):
        print "Error Reporting"
        print "-" * 80
        for row in range(len(self.errorMsgs)):
            print "%s %s" % (row, self.errorMsgs[row])

    def current_picture(self, node):
        ''' Internal function.  Debugging aid for the export module.'''
        if settings.DEBUG:
            print "Current XML Picture is"
            print "======================\n" * 2
            dump(node)
            print "======================\n" * 2

def isNullOrMT(test):   # Expand for numeric?
    if test == None:
        return True
    if test == "":
        return True
    return False

#if __name__ == "__main__":
#   vld = hl7CCDwriter(".")
#   vld.write()
