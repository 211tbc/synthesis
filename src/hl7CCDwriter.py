from interpretpicklist import Interpretpicklist
#import dateutils
#from datetime import datetime
import xmlutilities
#from exceptions import SoftwareCompatibilityError, DataFormatError
import logger
#from sys import version
import dbobjects
from writer import Writer
from zope.interface import implementer

from sqlalchemy import or_, between#, and_
from conf import settings
from lxml import etree as ET

@implementer(Writer)
class hl7CCDwriter():   # Health Level 7 Continuity of Care Document
    #implements(Writer) # Writer Interface

    def __init__(self, poutDirectory, processingOptions, debugMessages=None):
        print "==== %s Class Initialized" % self.__class__  # JCS-Doesn't have a __name__

        if settings.DEBUG:
            print "XML File to be dumped to: %s" % poutDirectory
            self.log = logger.Logger(configFile=settings.LOGGING_INI, loglevel=40)

        self.outDirectory = poutDirectory
        self.pickList = Interpretpicklist()
        self.options = processingOptions	# Passed in by nodebuilder from QueryObject.getOptions()
        self.errorMsgs = [] # SBB20070628 adding a buffer for errors to be displayed at the end of the process.

        self.db = dbobjects.DB()            # JCS 10/05/11
        self.db.Base.metadata.create_all()
        self.hl7dateform = "%Y%m%d%H%M%S%z"
        
        self.referredToProviderID = ""
        
    def write(self):        # Called from nodebuilder.run() one time.
        return self.makeHL7Docs("disk")

    def get(self):
        return self.makeHL7Docs("string")

    def makeHL7Docs(self,mode):
        self.session = self.db.Session()    # This starts a Transaction
        if settings.DEBUG:
            print '==== Self:', self
        # Database traversal:
        # Step through Exports. For each Export,
        # Step through Persons. For each person,
        # Step through ServiceEvent. For each Service Event, begin a new document, then
        # Step through Entrys
        # Step through ServiceEventNotes - and all note_text 
        exports = self.session.query(dbobjects.Export)
        hl7_output = []
        for oneExport in exports:
            selink = self.session.query(dbobjects.SourceExportLink).filter(
                                        dbobjects.SourceExportLink.export_index_id == oneExport.id).one()
            #print '==== Selink.id:', selink.id
            oneSource = self.session.query(dbobjects.Source).filter(dbobjects.Source.id == selink.source_index_id).one()
            #print '==== Source.id:', source.id
            #self.configRec = self.session.query(dbobjects.SystemConfiguration).filter(and_(dbobjects.SystemConfiguration.source_id
            #                     == source.source_id, dbobjects.SystemConfiguration.processing_mode == settings.MODE)).one()
            #print '==== sys config.id', self.configRec.id
            Persons = self.session.query(dbobjects.Person).filter(dbobjects.Person.export_index_id == oneExport.id)
            # More filtering for options
            if self.options.reported == True:
                Persons = Persons.filter(dbobjects.Person.reported == True)
            elif self.options.unreported == True:
                Persons = Persons.filter(or_(dbobjects.Person.reported == False, dbobjects.Person.reported == None))
            elif self.options.reported == None:
                pass
            # Now apply the dates to the result set.
            if self.options.alldates == None:
                Persons = Persons.filter(between(dbobjects.Person.person_id_date_collected,
                                             self.options.startDate, self.options.endDate))
            for onePerson in Persons:
                # update the reported field here instead of at the end of the loop
                # in case an exception is thrown by processXML. Even if there is an
                # error, the offending record in the Person's table is deactivated hiding it
                # from future queries
                self.updateReported(onePerson)
                self.session.commit()       # This is only for updateReported()
                ServEvts = self.session.query(dbobjects.ServiceEvent).filter(dbobjects.ServiceEvent.person_index_id == onePerson.id)
                for oneServEvt in ServEvts: # One document per event???
                    #print "person is: ", self.person
                    self.processXML(oneExport, onePerson, oneServEvt, oneSource)       # Create one document
                    xmlutilities.indent(self.root_element)  #self.prettify()
                    # Next wraps self.root_element in an ElementTree and writes it to disk
                    if mode=="disk":
                        xmlutilities.writeOutXML(self, xml_declaration=True, encoding="UTF-8")	# JCS - enc. defaults to ASCII w/decl.
                    else:
                        # here return the ccd document along with it's referral ID
                        hl7_output.append((xmlutilities.printOutXML(self, encoding="UTF-8", method="xml"), self.referredToProviderID))

        if mode=="disk":
            return True     # Now nodebuilder.run() will find all output files and validate them.
        else:
            return hl7_output

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
                                   onePerson.person_legal_suffix_unhashed)      # TODO Done?  ?LegalMiddleName.Unhashed
        self.addGender(patient, onePerson.person_gender_unhashed)
        birthTime = ET.SubElement(patient,"birthTime")
        try:
            birthTime.attrib["value"] = onePerson.person_date_of_birth_unhashed.strftime(self.hl7dateform) #"19770701" # TODO Done?
        except:
            pass
        self.races = onePerson.fk_person_to_races
        self.addRace(patient, self.races)  #.race_unhashed)
        self.addEthnicity(patient, onePerson.person_ethnicity_unhashed)
        providOrg = ET.SubElement(patientRole,"providerOrganization")
        self.addGroupId(providOrg, oneSource.source_id_id_str, oneSource.source_name)

        auth = ET.SubElement(self.root_element,"author")                        # Root 2
        authTime = ET.SubElement(auth,"time")
        authTime.attrib["value"] = "20000407130000+0500"
        asgdAuth = ET.SubElement(auth,"assignedAuthor")
        authId = ET.SubElement(asgdAuth,"id")
        authId.attrib["root"] = "20cf14fb-b65c-4c8c-a54d-b0cca834c18c"
        asgdPerson = ET.SubElement(asgdAuth,"assignedPerson")
        self.addAName(asgdPerson, "Dr.", "Robert", "Dolin", None)   # TODO
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
        leAsName.text = "Edward Perry"                              # TODO
        leRepOrg = ET.SubElement(legalEnt,"representedOrganization")
        self.addGroupId(leRepOrg, "11", "2-1-1 Tampa Bay Cares")

        #participant = ET.SubElement(self.root_element,"participant")            # Root 6
        #participant.attrib["typeCode"] = "IND"
        #assocEnt = ET.SubElement(participant,"associatedEntity")
        #assocEnt.attrib["classCode"] = "GUAR"
        #aeId = ET.SubElement(assocEnt,"id")
        #aeId.attrib["root"] = "4ff51570-83a9-47b7-91f2-93ba30373141"
        #self.addAnAddress(assocEnt, "12 Verde Rd.", "Saint Petersburg", "Florida", "33710")
        #aeTel = ET.SubElement(assocEnt,"telecom")
        #aeTel.attrib["value"] = "tel:(727)111-2222"                 # TODO
        #aePers = ET.SubElement(assocEnt,"associatedPerson")
        #self.addAName(aePers, "", "Jim", "Snow", "")                # TODO
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
        self.addAName(seePers, "", "Robert", "Dolin", "")           # TODO
        seeRep = ET.SubElement(seeEnt,"representedOrganization")
        self.addGroupId(seeRep, oneSource.source_id_id_str, oneSource.source_name)

        compon = ET.SubElement(self.root_element,"component")                   # Root 8
        struBod = ET.SubElement(compon,"structuredBody")
        componB = ET.SubElement(struBod,"component")
        section = ET.SubElement(componB,"section")
        self.addTemplateId(section, ".13")
        self.addCodeSys(section, "48764-5", ".6.1", "")
        secTitle = ET.SubElement(section,"title")
        secTitle.text = "Referral for client services from 2-1-1 Tampa Bay Cares"
        # Extensions?
        self.addExtension(section, onePerson, oneServEvt)

        #temp = ""
        #seNotes = self.session.query(dbobjects.ServiceEventNotes).filter(dbobjects.ServiceEventNotes.service_event_index_id
        #                         == oneServEvt.id)
        #for note in seNotes:
        #    if note.note_text != "":
        #        temp = "\n".join([temp, note.note_text])
        #ET.SubElement(section,"text").text = temp.lstrip()  # multi node fails...

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

    def addExtension(self,parent, onePerson, oneServEvt):
        self.extMap = {"ex" : "http://xsd.alexandriaconsulting.com/repos/trunk/HL7_Informal_Extension.xsd",
                      "tbc" : "http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd",
                     "hmis" : "http://www.hmis.info/schema/3_0/HUD_HMIS.xsd",
                     "airs" : "http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd" }  #     ex:version="3.0 ???
        refsNode = ET.SubElement(parent,"{"+self.extMap["ex"]+"}Referrals", nsmap=self.extMap)

        #referrals = self.session.query(dbobjects.Referral).filter(dbobjects.Referral.service_event_index_id == oneServEvt.id)
        referrals = self.session.query(dbobjects.Referral).filter(dbobjects.Referral.person_index_id == onePerson.id)
        for oneRef in referrals:
            taxoRec = self.session.query(dbobjects.Taxonomy).filter(dbobjects.Taxonomy.need_index_id == oneRef.need_index_id).one()
            refNode = ET.SubElement(refsNode,"{"+self.extMap["ex"]+"}Referral") # can be many referral elements inside a 'Referrals'
            tbcRefID = ET.SubElement(refNode,"{"+self.extMap["tbc"]+"}ReferralID")
            ET.SubElement(tbcRefID,"{"+self.extMap["hmis"]+"}IDNum").text=oneRef.referral_idid_num
            hmisTaxo = ET.SubElement(refNode,"{"+self.extMap["hmis"]+"}Taxonomy")
            ET.SubElement(hmisTaxo,"{"+self.extMap["airs"]+"}Code").text=taxoRec.code   # TODO Done?
            # id | export_index_id | site_service_index_id | need_index_id |  code   
            tbcSENotes = ET.SubElement(refNode,"{"+self.extMap["tbc"]+"}ServiceEventNotes")
            hmisNote = ET.SubElement(tbcSENotes,"{"+self.extMap["hmis"]+"}note")
            self.referredToProviderID = oneRef.referral_agency_referred_to_idid_num
            seNotes = self.session.query(dbobjects.ServiceEventNotes).filter(dbobjects.ServiceEventNotes.service_event_index_id
                                 == oneServEvt.id)
            for note in seNotes:
                noteID = ET.SubElement(hmisNote,"{"+self.extMap["hmis"]+"}NoteID")
                ET.SubElement(noteID,"{"+self.extMap["hmis"]+"}IDNum").text=note.note_id_id_num
                ET.SubElement(hmisNote,"{"+self.extMap["hmis"]+"}NoteText",
                               attrib={"{"+self.extMap["hmis"]+"}dateCollected":note.note_text_date_collected.strftime(self.hl7dateform),
                                       "{"+self.extMap["hmis"]+"}dateEffective":note.note_text_date_effective.strftime(self.hl7dateform)}
                             ).text=note.note_text

    def createDoc(self):
        # What about:  <?xml-stylesheet type="text/xsl" href="CDASchemas\cda\Schemas\CCD.xsl"?>
        # targetNamespace="urn:hl7-org:v3" xmlns:mif="urn:hl7-org:v3/mif"
        self.mymap = { None  : "urn:hl7-org:v3",
                  "voc" : "urn:hl7-org:v3/voc",
                  "xsi" : "http://www.w3.org/2001/XMLSchema-instance"}
        root_element = ET.Element("ClinicalDocument", nsmap=self.mymap)
        root_element.attrib["{"+self.mymap["xsi"]+"}schemaLocation"] = "urn:hl7-org:v3 infrastructure/cda/CDA.xsd"
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

    def addRace(self, patient, races):
        if len(races) <  1:
            return
        race_parm = races[0].race_unhashed
        if race_parm in [6, 7] or race_parm > 9:
            return
        raceCode = ET.SubElement(patient,"raceCode")
        if race_parm == 1:
            raceCode.attrib["code"] = "1002-5" 
        elif race_parm == 2:
            raceCode.attrib["code"] = "2028-9" 
        elif race_parm == 3:
            raceCode.attrib["code"] = "2060-2" 
        elif race_parm == 4:
            raceCode.attrib["code"] = "2076-8" 
        elif race_parm == 5:
            raceCode.attrib["code"] = "2106-3" 
        elif race_parm in [8, 9]:
            raceCode.attrib["nullFlavor"] = "ASKU"
        raceCode.attrib["codeSystem"] = "2.16.840.1.113883.6.238" 
        raceCode.attrib["codeSystemName"] = "CDC Race and Ethnicity"

    def addGender(self, patient, hmis_gender):
        if hmis_gender in [5, 6, 7]:
            return
        gendCode = ET.SubElement(patient,"administrativeGenderCode")    # All
        if hmis_gender in [0, 2]:
            gendCode.attrib["code"] = "F"
            if hmis_gender == 0:
                gendCode.attrib["displayName"] = "Female"
            else:
                gendCode.attrib["displayName"] = "Transgendered Male to Female"
        elif hmis_gender in [1, 3]:
            gendCode.attrib["code"] = "M"
            if hmis_gender == 1:
                gendCode.attrib["displayName"] = "Male"
            else:
                gendCode.attrib["displayName"] = "Transgendered Female to Male"
        elif hmis_gender == 4:
            gendCode.attrib["code"] = "UN"
        elif hmis_gender in [8, 9]:
            gendCode.attrib["nullFlavor"] = "ASKU"
        gendCode.attrib["codeSystem"] = "2.16.840.1.113883.5.1"         # All
        gendCode.attrib["codeSystemName"] = "AdministrativeGenderCode"  # All

    def addEthnicity(self, patient, eth_parm):    # int 2
        if eth_parm in [2, 3, 4, 5, 6, 7] or eth_parm > 9:
            return
        ethCode = ET.SubElement(patient,"ethnicGroupCode")
        if eth_parm == 0:           # non-hispanic/non-latino (hud)
            ethCode.attrib["code"] = "2186-5"
        elif eth_parm == 1:         # hispanic/latino (hud)
            ethCode.attrib["code"] = "2135-2" 
        elif eth_parm in [8, 9]:    # 8:don't know (hud)  9:refused (hud)
            ethCode.attrib["nullFlavor"] = "ASKU"
        ethCode.attrib["codeSystem"] = "2.16.840.1.113883.5.50" 
        ethCode.attrib["codeSystemName"] = "Race and Ethnicity Code Sets"

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
	
    def updateReported(self, currentObject):
        # update the reported field of the currentObject being passed in.  These should all exist.
        try:
            if settings.DEBUG:
                print 'Updating reporting for object: %s' % currentObject.__class__
            currentObject.reported = True
            #self.commitTransaction()
        except:
            print "Exception occurred during update the 'reported' flag"
            pass

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
            ET.dump(node)
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
