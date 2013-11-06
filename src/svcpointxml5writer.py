from interpretpicklist import Interpretpicklist
import dateutils
from datetime import datetime
import xmlutilities
from synthesis.exceptions import DataFormatError#, SoftwareCompatibilityError
import logger
#from sys import version
import dbobjects
from writer import Writer
from zope.interface import implements
from sqlalchemy import or_, and_, between
from conf import settings
from lxml import etree as ET


def buildWorkhistoryAttributes(element):
    element.attrib['date_added'] = datetime.now().isoformat()
    element.attrib['date_effective'] = datetime.now().isoformat()

class SvcPointXML5Writer():
    # Writer Interface
    implements(Writer)

    hmis_namespace = "http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd" 
    airs_namespace = "http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd"
    nsmap = {"hmis" : hmis_namespace, "airs" : airs_namespace}

    svcpt_version = '5.00'

    def __init__(self, poutDirectory, processingOptions, debugMessages=None):
        #print "%s Class Initialized" % self.__name__

        if settings.DEBUG:
            print "XML File to be dumped to: %s" % poutDirectory
            self.log = logger.Logger(configFile=settings.LOGGING_INI, loglevel=40)    # JCS 10/3/11

        self.outDirectory = poutDirectory
        self.pickList = Interpretpicklist()
        # SBB20070626 Adding the declaration for outcomes list
        self.options = processingOptions

        # SBB20070628 adding a buffer for errors to be displayed at the end of the process.
        self.errorMsgs = []

        self.db = dbobjects.DB()            # JCS 10/05/11
        self.db.Base.metadata.create_all()
            
    def write(self):
        self.startTransaction()
        self.processXML()
        self.prettify()
        print '==== Self:', self
        xmlutilities.writeOutXML(self, xml_declaration=True, encoding="UTF-8")    # JCS, 1 Sep 2012
        #self.commitTransaction()
        return True

    def updateReported(self, currentObject):
        # update the reported field of the currentObject being passed in.  These should all exist.
        try:
            if settings.DEBUG:
                print 'Updating reporting for object: %s' % currentObject.__class__
            currentObject.reported = True
            #currentObject.update()
            self.commitTransaction()
        except:
            print "Exception occurred during update the 'reported' flag"
            pass

    def prettify(self):
        xmlutilities.indent(self.root_element)

    def dumpErrors(self):
        print "Error Reporting"
        print "-" * 80
        for row in range(len(self.errorMsgs)):
            print "%s %s" % (row, self.errorMsgs[row])

    def setSysID(self, pSysID):
        self.sysID = pSysID

    def commitTransaction(self):
        self.session.commit()

    def startTransaction(self):
        self.session = self.db.Session()

    def pullConfiguration(self, pExportID):
        # need to use both ExportID and Processing Mode (Test or Prod)
        export = self.session.query(dbobjects.Export).filter(dbobjects.Export.export_id == pExportID).one()
        if settings.DEBUG:
            print "trying to do pullConfiguration"
            #print "export is:", export, "pExportID is", pExportID
            #print "export.export_id is: ", export.export_id
            #print "dbobjects.SystemConfiguration.source_id is ", dbobjects.SystemConfiguration.source_id

        selink = self.session.query(dbobjects.SourceExportLink).filter(dbobjects.SourceExportLink.export_index_id == export.id).one()
        #print '==== Selink.id:', selink.id
        source = self.session.query(dbobjects.Source).filter(dbobjects.Source.id == selink.source_index_id).one()
        #print '==== Source.id:', source.id
        self.configurationRec = self.session.query(dbobjects.SystemConfiguration).filter(and_(dbobjects.SystemConfiguration.source_id == source.source_id, dbobjects.SystemConfiguration.processing_mode == settings.MODE)).one()
        #print '==== sys config.id', self.configurationRec.id
    
    def processXML(self): # records represents whatever element you're tacking more onto, like entry_exits or clients
        if settings.DEBUG:
            print "processXML: Appending XML to Base Record"
        self.root_element = self.createDoc() #makes root element with XML header attributes
        #print '==== root created'
        clients = self.createClients(self.root_element) # JCS - tag is <clientRecords> Only node under clients is <Client>
        print '==== clientRecords created'
        
        if self.options.reported == True:
            Persons = self.session.query(dbobjects.Person).filter(dbobjects.Person.reported == True)
        elif self.options.unreported == True:
            Persons = self.session.query(dbobjects.Person).filter(or_(dbobjects.Person.reported == False, dbobjects.Person.reported == None))
        elif self.options.reported == None:
            Persons = self.session.query(dbobjects.Person)
        # Now apply the dates to the result set.
        if self.options.alldates == None:
            Persons = Persons.filter(between(dbobjects.Person.person_id_date_collected, self.options.startDate, self.options.endDate))
        
        pulledConfigID = 0    # JCS Only pull it if it has changed
        for self.person in Persons:
            #print "person is: ", self.person

            export = self.person.fk_person_to_export    # this is a single record because:
            # person has: export_index_id = Column(Integer, ForeignKey('export.id'))
            # export has: fk_export_to_person = relationship('Person', backref='fk_person_to_export')
            # Therefore there are multiple persons to one export - but only one export to a person

            #print "==== export before pullconfig:", export.id, export  # JCS
            if pulledConfigID != export.id:
                self.pullConfiguration(export.export_id)
                pulledConfigID = export.id
            
            self.ph = self.person.fk_person_to_person_historical    # JCS This is a list of records
            self.race = self.person.fk_person_to_races
            self.site_service_part = self.person.site_service_participations    # JCS

            #information_releases = self.person.fk_person_to_release_of_information    # JCS a set
            #self.service_event = self.person.fk_person_to_service_event
            # Instead of generating a number (above), use the client number that is already provided in the legacy system
            # or
            # self.iDG.initializeSystemID(self.person.id)
            self.sysID = self.person.id        # JCS beware set self.sysID
            #if settings.DEBUG:
                #print "self.person is:", self.person 
            if self.person: # and not self.person.person_legal_first_name_unhashed+self.person.person_legal_last_name_unhashed == None:
                self.client = self.createClient(clients) # JCS - no clients in svc5? yes as clientRecords
                # Sub can be: active, anonymous, firstName, suffix, unnamedClient, alias, middleName, childEntryExit,
                # childReleaseOfInfo, childGoal
                self.customizeClient(self.client)    
                self.customizeClientPersonalIdentifiers(self.client, self.person)
                self.assessment_data = self.createAssessmentData(self.client) # JCS New - self?
                self.customizeAssessmentData(self.assessment_data)
                if self.site_service_part:      # JCS 21 Dec 2012
                    self.child_entry_exit = self.createChildEntryExit(self.client)
                    for ssp in self.site_service_part:
                        self.createEntryExit(self.child_entry_exit, ssp)
            # update the reported flag for person (This needs to be applied to all objects that we are getting data from)
            self.updateReported(self.person)

        # Query Mechanism for Site Service Participation (Entry Exits) same as for Person?
# This is only if we want to create an EE summary at the end for all Clients
#        if self.options.reported == True:
#            site_service_part = self.session.query(dbobjects.SiteServiceParticipation).filter(dbobjects.SiteServiceParticipation.reported == True)
#        elif self.options.unreported == True:
#            site_service_part = self.session.query(dbobjects.SiteServiceParticipation).filter(or_(dbobjects.SiteServiceParticipation.reported == False, dbobjects.SiteServiceParticipation.reported == None))
#        elif self.options.reported == None:
#            site_service_part = self.session.query(dbobjects.SiteServiceParticipation)
#        else:
#            pass
#        
#        # setup the date filter also
#        site_service_part = site_service_part.filter(between(dbobjects.SiteServiceParticipation.site_service_participation_idid_num_date_collected, self.options.startDate, self.options.endDate))
#
#        entry_exits = self.createEntryExits(self.root_element)
#        for EE in site_service_part:
#            # SBB20100405 do this to pull the configuration record
#            person = EE.fk_participation_to_person
#            export = person.fk_person_to_export
#            self.pullConfiguration(export.export_id)
#            self.updateReported(EE)        # Reporting Update
#            self.sysID = EE.id            # JCS beware set self.sysID
#            self.createEntryExit(entry_exits, EE)


        # End of ProcessXML()        

    def createDoc(self):

        # From hl7
        #self.mymap = { None  : "urn:hl7-org:v3",
        #          "voc" : "urn:hl7-org:v3/voc",
        #          "xsi" : "http://www.w3.org/2001/XMLSchema-instance"}
        #root_element = ET.Element("ClinicalDocument", nsmap=self.mymap)
        #root_element.attrib["{"+self.mymap["xsi"]+"}schemaLocation"] = "urn:hl7-org:v3 infrastructure/cda/CDA.xsd"
        # From hl7 end

        #sp5_instance looks like this
        # <records xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        #       xsi:noNamespaceSchemaLocation="file:/home/eric/workspace/servicepoint_schema/sp5/sp5.xsd" 
        #       odb_identifier="qwo7Wsoi"      
        #       import_identifier="v7:1bl.e">

        self.mymap = {"xsi" : "http://www.w3.org/2001/XMLSchema-instance"}  # Yes lxml

        #root_element = ET.Element("records")       # Non-lxml
        root_element = ET.Element("records", nsmap=self.mymap)  # Yes lxml

        #root_element.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"    # Non-lxml
        
        #root_element.attrib["xsi:noNamespaceSchemaLocation"] = "sp5.xsd"     # Non-lxml
        root_element.attrib["{"+self.mymap["xsi"]+"}noNamespaceSchemaLocation"] = "sp5.xsd"  # Yes lxml

        # Added by JCS 1 Sep 2012
        root_element.attrib["odb_identifier"] = "qwo7Wsoi"      # Yes lxml
        root_element.attrib["import_identifier"] = "v7:1bl.e"   # Yes lxml

        #root_element.attrib["schema_revision"] = "300_108"    # JCS Not in Schema
        #root_element.text = "\n"
        return root_element

    def createClients(self, root_element):
        clients = ET.SubElement(root_element, "clientRecords")
        return clients

    def createClient(self, clients):
        client = ET.SubElement(clients, "Client")    #  Cap 'C' in svc5
        return client

    def createChildEntryExit(self,client):
        child_entry_exit = ET.SubElement(client, "childEntryExit") # JCS new - sub-client
        return child_entry_exit
        
    def createEntryExits(self,root_element):
        entry_exits = ET.SubElement(root_element, "entryExitRecords") # JCS - not in SVP5?
        return entry_exits
        
    def customizeClient(self, client):

        #print "==== Customize Client:", self.configurationRec.odbid, self.person.person_id_id_num
        client.attrib["record_id"] = "CL-" + str(self.person.id) 
        #client.attrib["external_id"] = self.person.person_id_id_num    # JCS -this item is optional
        client.attrib["system_id"] = self.person.person_id_id_num        # JCS just a guess ????
        client.attrib["date_added"] = dateutils.fixDate(datetime.now())
        client.attrib["date_updated"] = dateutils.fixDate(datetime.now())

        # SBB20070702 check if self.intakes has none, this is a daily census that is alone
    def customizeClientPersonalIdentifiers(self,client,recordset):    # params are: self.client, self.person
    
        if recordset.person_legal_first_name_unhashed <> "" and recordset.person_legal_first_name_unhashed <> None:
            first_name = ET.SubElement(client, "firstName")
            first_name.text = recordset.person_legal_first_name_unhashed

        if recordset.person_legal_last_name_unhashed <> "" and recordset.person_legal_last_name_unhashed <> None:
            last_name = ET.SubElement(client, "lastName")
            last_name.text = recordset.person_legal_last_name_unhashed

        #we don't have the following elements for daily_census only clients, but SvcPt requires them:
        # I simulated this w/my datasets.  Column names are as in the program
        if recordset.person_legal_middle_name_unhashed <> "" and recordset.person_legal_middle_name_unhashed <> None:
            mi_initial = ET.SubElement(client, "mi_initial")
            mi_initial.text = self.fixMiddleInitial(recordset.person_legal_middle_name_unhashed)
            
        # SBB20070831 incoming SSN's are 123456789 and need to be 123-45-6789
        fixedSSN = self.fixSSN(recordset.person_social_security_number_unhashed) # JCS  .person_SSN_unhashed)
                    
        if fixedSSN <> "" and fixedSSN <> None:        #ECJ20071111 Omit SSN if it's blank
            soc_sec_no = ET.SubElement(client, "socSecNoDashed")
            soc_sec_no.text = fixedSSN
            ssn_data_quality = ET.SubElement(client, "ssnDataQualityValue")
            ssn_data_quality.text = "full ssn reported (hud)"

    def createEntryExit(self, entry_exits, EE):    # Outer Node, one EntryExit(ssp)

        entry_exit = ET.SubElement(entry_exits, "EntryExit")

        entry_exit.attrib["record_id"] = "EE-"+str(EE.id)
        # ssp-idid-num looks like it ought to be unique, but isn't in sample input data, so append client id????
        entry_exit.attrib["system_id"] = EE.site_service_participation_idid_num+"-"+EE.person.person_id_id_num
        # person.site_service_participations = relationship("SiteServiceParticipation", backref="person")
        entry_exit.attrib["date_added"] = dateutils.fixDate(datetime.now())
        entry_exit.attrib["date_updated"] = dateutils.fixDate(datetime.now())

        self.customizeEntryExit(entry_exit, EE)
        return entry_exit

    def customizeEntryExit(self, entry_exit, EE):
        # Schema expects one of ( active, typeEntryExit, client, exitDate, reasonLeavingValue, reasonLeavingOther,
        #    destinationValue, destinationOther, notes, group )
        # There is no type in our input XML, nor a field in ssp. Schema needs {'basic', 'basic center program entry/exit',
        #   'hprp', 'hud', 'path', 'quick call', 'standard', 'transitional living program entry/exit'}
        type1 = ET.SubElement(entry_exit, "typeEntryExit")    # JCS  this is a fudge to pass validation
        type1.text = "basic"    # "hud-40118"

        provider_id = ET.SubElement(entry_exit, "provider")
        provider_id.text = '%s' % self.configurationRec.providerid

        if EE.participation_dates_start_date <> "" and EE.participation_dates_start_date <> None:
            entry_date = ET.SubElement(entry_exit, "entryDate")
            entry_date.text = dateutils.fixDate(EE.participation_dates_start_date)

            if EE.participation_dates_end_date <> "" and EE.participation_dates_end_date <> None:
                exit_date = ET.SubElement(entry_exit, "exitDate")
                exit_date.text = dateutils.fixDate(EE.participation_dates_end_date)
        return

    def createAssessmentData(self, client):        # dynamic content type
        assessment_data = ET.SubElement(client, "assessmentData")
        return assessment_data

    def customizeAssessmentData(self, assessment_data):

        if self.person.person_gender_unhashed <> "" and self.person.person_gender_unhashed <> None:
            persGender = ET.SubElement(assessment_data, "svpprofgender" ) #"gender")
            persGender.attrib["date_added"] = dateutils.fixDate(self.person.person_gender_unhashed_date_collected)
            persGender.attrib["date_effective"] = dateutils.fixDate(self.person.person_gender_unhashed_date_effective)
            persGender.text = str(self.person.person_gender_unhashed)

        # dob (Date of Birth)    lots of:SVPPROFDOB    a few:DATEOFBIRTH
        if self.person.person_date_of_birth_unhashed <> "" and self.person.person_date_of_birth_unhashed <> None:
            dob = ET.SubElement(assessment_data, "svpprofdob")
            dob.attrib["date_added"] = dateutils.fixDate(self.person.person_date_of_birth_unhashed_date_collected)
            dob.attrib["date_effective"] = dateutils.fixDate(datetime.now())    # No date effect. in Person
            dob.text = dateutils.fixDate(self.person.person_date_of_birth_unhashed)

        # Ethnicity           lots of:SVPPROFETH    a few:Ethnicity     uses:ETHNICITYPickOption
        if self.person.person_ethnicity_unhashed <> "" and self.person.person_ethnicity_unhashed <> None:
            # Our Interpretpicklist basically has 2 options. The schema has 23
            ethText = self.pickList.getValue("EthnicityPick",str(self.person.person_ethnicity_unhashed))
            eth = ET.SubElement(assessment_data, "svpprofeth")
            eth.attrib["date_added"] = dateutils.fixDate(self.person.person_ethnicity_unhashed_date_collected)
            eth.attrib["date_effective"] = dateutils.fixDate(datetime.now())    # No date effect. in Person
            eth.text = ethText  # str(self.person.person_ethnicity_unhashed)
    
        # Race    more than one?? JCS
        for race in self.race:
            # JCS schema has 'RACEPickOption' - using existing RacePick for now
            raceText = self.pickList.getValue("RacePick",str(race.race_unhashed))
            # print '==== race:', race.race_unhashed, raceText
            if raceText <> None:
                raceNode = ET.SubElement(assessment_data, "svpprofrace")    # JCS "primaryrace" or "svpprofrace"?
                raceNode.attrib["date_added"] = dateutils.fixDate(race.race_date_collected)
                raceNode.attrib["date_effective"] = dateutils.fixDate(race.race_date_effective)
                raceNode.text = raceText

        for ph in self.ph:
            #print '==== ph person id:', ph.person_index_id #, ph.__dict__
            # JCS - Fails if none - seen in going from tbc to here - but don't know if that ever happens
            hs = self.session.query(dbobjects.HousingStatus).filter(dbobjects.HousingStatus.person_historical_index_id == ph.id).one()
            hsText = self.pickList.getValue("HOUSINGSTATUSPickOption",hs.housing_status)
            #print '==== hs:', hsText
            if hsText <> None:
                housingStatus = ET.SubElement(assessment_data, "svp_hud_housingstatus")    # JCS
                housingStatus.attrib["date_added"] = dateutils.fixDate(hs.housing_status_date_collected)
                housingStatus.attrib["date_effective"] = dateutils.fixDate(hs.housing_status_date_effective)
                housingStatus.text = hsText

            foster = self.session.query(dbobjects.FosterChildEver).filter(dbobjects.FosterChildEver.person_historical_index_id == ph.id).one()
            fosterText = self.pickList.getValue("ENHANCEDYESNOPickOption",str(foster.foster_child_ever))
            if fosterText <> None:
                fosterEver = ET.SubElement(assessment_data, "x20wereyoueverafoster")    # JCS
                fosterEver.attrib["date_added"] = dateutils.fixDate(foster.foster_child_ever_date_collected)
                fosterEver.attrib["date_effective"] = dateutils.fixDate(foster.foster_child_ever_date_effective)
                fosterEver.text = fosterText

        # length of stay at prior residence
        losapr = self.session.query(dbobjects.LengthOfStayAtPriorResidence).filter(dbobjects.LengthOfStayAtPriorResidence.person_historical_index_id == ph.id).one()
        losaprText = self.pickList.getValue("LENGTHOFTHESTAYPickOption",losapr.length_of_stay_at_prior_residence)
        #print '==== losapr:', losaprText
        if losaprText <> None:
            lengthOfStay = ET.SubElement(assessment_data, "hud_lengthofstay")    # JCS
            lengthOfStay.attrib["date_added"] = dateutils.fixDate(losapr.length_of_stay_at_prior_residence_date_collected)
            lengthOfStay.attrib["date_effective"] = dateutils.fixDate(losapr.length_of_stay_at_prior_residence_date_effective)
            lengthOfStay.text = losaprText

        # "Prior Residence" becomes "typeoflivingsituation"
        tols = self.session.query(dbobjects.PriorResidence).filter(dbobjects.PriorResidence.person_historical_index_id == ph.id).one()
        tolsText = self.pickList.getValue("LIVINGSITTYPESPickOption",tols.prior_residence_code)
        #print '==== (prior) tols:', tolsText
        if tolsText <> None:
            priorLiving = ET.SubElement(assessment_data, "typeoflivingsituation")    # JCS
            priorLiving.attrib["date_added"] = dateutils.fixDate(tols.prior_residence_code_date_collected)
            priorLiving.attrib["date_effective"] = dateutils.fixDate(tols.prior_residence_code_date_effective)
            priorLiving.text = tolsText
        # There's also a  prior_residence_id_id_num populated with a 13 digit number as string  JCS

        # Physical Disability - Boolean
        pdyn = self.session.query(dbobjects.PhysicalDisability).filter(dbobjects.PhysicalDisability.person_historical_index_id == ph.id).one()
        pdynText = pdyn.has_physical_disability
        #print '==== pdyn:', pdynText
        if pdynText <> None:
            physDisabYN = ET.SubElement(assessment_data, "svpphysicaldisabilit")    # JCS
            physDisabYN.attrib["date_added"] = dateutils.fixDate(pdyn.has_physical_disability_date_collected)
            # This is required, but input is usually blank - something plugs in now()
            physDisabYN.attrib["date_effective"] = dateutils.fixDate(pdyn.has_physical_disability_date_effective)
            physDisabYN.text = pdynText
        # There is also a complex type "disabilities_1"

        # Veteran Status - Uses "ENHANCEDYESNOPickOption" which is a union, and allows anything
        vvs = self.session.query(dbobjects.VeteranVeteranStatus).filter(dbobjects.VeteranVeteranStatus.person_historical_index_id == ph.id).one()
        vvsText = vvs.veteran_status
        #print '==== vvs:', vvsText
        if vvsText <> None:
            vetStat = ET.SubElement(assessment_data, "veteran")    # JCS
            vetStat.attrib["date_added"] = dateutils.fixDate(vvs.veteran_status_date_collected)
            vetStat.attrib["date_effective"] = dateutils.fixDate(vvs.veteran_status_date_effective)
            vetStat.text = vvsText

#    def customizeDisabilities_1(self, disabilities_1, ph):
#        #if self.intakes['DisabilityDiscription'] <> "":
#        noteondisability = ET.SubElement(disabilities_1,'noteondisability')
#        noteondisability.attrib["date_added"] = dateutils.fixDate(datetime.now())
#        noteondisability.attrib["date_effective"] = dateutils.fixDate(ph.physical_disability_date_collected)
#        noteondisability.text = ph.physical_disability

    def current_picture(self, node):
        ''' Internal function.  Debugging aid for the export module.'''
        if settings.DEBUG:
            print "Current XML Picture is"
            print "======================\n" * 2
            ET.dump(node)
            print "======================\n" * 2

    def calcHourlyWage(self, monthlyWage):
        if monthlyWage <> "":
            if monthlyWage.strip().isdigit():
                if float(monthlyWage) > 5000.00:
                    hourlyWage = float(monthlyWage) / 160.00#IGNORE:@UnusedVariable
            else:
                hourlyWage = float(monthlyWage)#IGNORE:@UnusedVariable
        else:
            hourlyWage = 0.00
        return str(round(hourlyWage,2))

    def fixMiddleInitial(self, middle_initial):
        fixed_middle_initial = middle_initial[0].upper().lstrip()
        return fixed_middle_initial

    def fixSSN(self, incomingSSN):
        originalSSN = incomingSSN
        if incomingSSN == "" or incomingSSN == None:
            return incomingSSN

        dashCount = incomingSSN.count('-') 
        if dashCount > 0:
            if dashCount == 2:
            # already has the dashes, return the string
                if settings.DEBUG:
                    self.debugMessages.log("incoming SSN is correctly formatted: %s\n" % (incomingSSN))

                return incomingSSN
            else:       # incoming SSN has 1 dash but not 2.  This is an error
            # fix this data
                incomingSSN = incomingSSN.replace( '-', '')
                if len(incomingSSN) < 9:
                    # reformat the string and return
                    theError = (1020, 'Data format error discovered in trying to cleanup incoming SSN: %s, original SSN: %s' % (incomingSSN, originalSSN))
                    if settings.DEBUG:
                        self.debugMessages.log(">>>> Incoming SSN is INcorrectly formatted.  Original SSN from input file is: %s and Attempted cleaned up SSN is: %s\n" % (originalSSN, incomingSSN))
                    raise DataFormatError, theError

        # If we are here, we can simply reformat the string into dashes
        if settings.DEBUG:
            pass    # JCS
        #   self.debugMessages.log("incoming SSN is INcorrectly formatted: %s.  Reformatting to: %s\n" % (incomingSSN, '%s-%s-%s' % (incomingSSN[0:3], incomingSSN[3:5], incomingSSN[5:10])))
        return '%s-%s-%s' % (incomingSSN[0:3], incomingSSN[3:5], incomingSSN[5:10])

#if __name__ == "__main__":
#   vld = SVCPOINTXMLWriter(".")
#   vld.write()
