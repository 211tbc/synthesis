#!/usr/bin/env python

import os

# Alchemy Libraries
from sqlalchemy import create_engine, Table, Column, Numeric, Integer, String, \
                       Boolean, MetaData, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, mapper, backref, relation, clear_mappers
from sqlalchemy.types import DateTime, Date
from sqlalchemy import or_, and_, between
from zope.interface import implements

import csv

from conf import settings
import clsExceptions
import DBObjects
from writer import Writer


class HmisCsv30Writer(DBObjects.databaseObjects):

    # Writer Interface
    implements (Writer)

    files = \
    {
        "export"         : "Export.csv",
        "agency"         : "Agency_Program.csv",
        "siteInfo"       : "Site_Information.csv",
        "regions"        : "Regions.csv",
        "inventory"      : "Bed_Inventory.csv",
        "client"         : "Client.csv",
        "historical"     : "ClientHistorical.csv",
        "participation"  : "Program_Participation.csv",
        "serviceEvent"   : "Service_Event.csv",
        "incomeBenefits" : "Income_Benefits.csv"
    }


    exportHeader = \
    [
        "ExportIDStr", "SourceID", "SourceName", "SourceContactFirst",
        "SourceContactLast", "SourceContactPhone", "SourceContactExtension",
        "SourceContactEmail", "ExportDate", "ExportPeriodBegin",
        "ExportPeriodEnd", "ExportHashing", "SoftwareVendor",
        "SoftwareVersion", "AgencyFile", "BedInventoryFile",
        "ClientFile", "ClientHistoricalFile", "IncomeBenefitsFile",
        "OutcomeMeasuresFile", "RegionsFile", "Program_Participation",
        "ServiceEventFile", "SiteInformationFile", "Delta or Refresh"
    ]

    agencyHeader = \
    [
        "OrganizationID", "OrganizationName", "ProgramID", "ProgramName",
        "DirectServiceCode", "SiteID", "ProgramTypeCode", "TargetPopulationA",
        "TargetPopulationB", "TrackingMethod", "GranteeIdentifier",
        "ReceivesMcKinneyFunding", "DateCreated", "DateUpdated", "ExportIDStr"
    ]

    siteInfoHeader = \
    [
        "OrganizationID", "Setup Site ID", "Address", "City", "State",
        "Zip Code", "GeographicCode", "SiteServiceType", "HousingType",
        "DateUpdated", "ExportIDStr"
    ]

    regionsHeader = \
    [
        "OrganizationID", "SiteID", "RegionType", "RegionID",
        "RegionDescription", "DateUpdated", "ExportIDStr"
    ]

    inventoryHeader = \
    [
        "OrganizationID", "ProgramID", "SiteID", "AssetListID", "AssetListName",
        "HouseholdType", "BedType", "Availability", "BedInventory",
        "CHBedInventory", "UnitInventory", "InventoryStartDate",
        "InventoryEndDate", "HMISParticipatingBeds", "HMISParticipationStartDate",
        "HMISParticipationEndDate", "DateUpdated", "ExportIDStr"
    ]

    clientHeader = \
    [
        "OrganizationID", "PersonalIdentificationNumber", "LegalFirstName",
        "LegalMiddleName", "LegalLastName", "LegalSuffix", "SocialSecurityNumber",
        "SocialSecNumberQualityCode", "DateOfBirth", "DateOfBirthQualityCode",
        "PrimaryRace", "SecondaryRace", "Ethnicity", "Gender", "DateAdded",
        "DateUpdated", "UpdateOrDelete", "IdentityVerification",
        "ReleaseOfInformation", "ExportIDStr"
    ]

    historicalHeader = \
    [
        "PersonalIdentificationNumber", "OrganizationID", "ProgramID",
        "SiteID", "AssessmentDate", "DateUpdated", "IncomeTotalMonthly",
        "IncomeLast30Days", "NonCashBenefitsLast30Days", "PhysicalDisability",
        "ReceivePhysicalDisabilityServices", "HasDevelopmentalDisability",
        "ReceiveDevelopmentalDisabilityServices", "HasChronicHealthCondition",
        "ReceiveChronicHealthServices", "HasHIVAIDS", "ReceiveHIVAIDSServices",
        "HasMentalHealthProblem", "MentalHealthIndefinite",
        "ReceiveMentalHealthServices", "HasSubstanceAbuseProblem",
        "SubstanceAbuseIndefinite", "ReceiveSubstanceAbuseServices",
        "DomesticViolenceSurvivor", "DVOccurred", "CurrentlyEmployed",
        "HoursWorkedLastWeek", "EmploymentTenure", "LookingForWork",
        "CurrentlyInSchool", "VocationalTraining", "HighestSchoolLevel",
        "Degree", "HealthStatus", "PregnancyStatus", "DueDate", "ServiceEra",
        "MilitaryServiceDuration", "ServedInWarZone", "WarZone",
        "MonthsInWarZone", "ReceivedFire", "MilitaryBranch", "DischargeStatus",
        "ChildCurrentlyEnrolledInSchool", "ChildSchoolName",
        "ChildMcKinneyVentoLiaison", "ChildSchoolType",
        "ChildSchoolLastEnrolledDate", "ChildEnrollmentBarrier", "ExportIDStr"
    ]

    participationHeader = \
    [
        "PersonalIdentificationNumber", "OrganizationID", "ProgramID", "SiteID",
        "EntryDate", "ExitDate", "DateUpdated", "VeteranStatus",
        "DisablingCondition", "PriorResidence", "LengthOfStayAtPriorResidence",
        "ZIPCode", "ZIPQualityCode", "HousingStatusAtEntry", "HousingStatusAtExit",
        "HouseholdIdentificationNumber", "Destination", "ReasonForLeaving",
        "RelationshipToHeadOfHousehold", "HUDChronicHomeless", "ExportIDStr"

    ]

    serviceEventHeader = \
    [
        "PersonalIdentificationNumber", "OrganizationID", "ProgramID", "SiteID",
        "ServiceEventType", "ServiceEventStartDate", "ServiceEventEndDate",
        "ServiceCode", "ServiceAIRSCode", "IsReferral?", "Quantity/Frequency",
        "FinancialAssistanceAmount", "FundingCategory", "GrantIDNumber",
        "IsRecurring", "Period/Interval", "Advance/Arrears", "ContactTime",
        "ContactSite", "ClientEngaged", "AssetListID", "AssetID", "DomainIDCode",
        "DateUpdated", "ExportIDStr"

    ]

    incomeBenefitsHeader = \
    [
        "PersonalIdentificationNumber", "OrganizationID", "ProgramID", "SiteID",
        "AssessmentDate", "DateUpdated", "IncomeBenefitType", "SourceCode",
        "SourceOther", "MonthlyAmount", "ExportIDStr"
    ]


    def __init__(self, outDirectory, processingOptions, debug=False, debugMessages=None):
        if settings.DEBUG:
            print "CSV Files to be created in: %s" % outDirectory

        self.outDirectory = outDirectory
        #self.pickList = interpretPickList()
        self.errorMsgs = []
        self.debug = debug

        print "Setting up DBObjects..."
        import time
        startReal = time.time()
        self.mappedObjects = DBObjects.databaseObjects()
        endReal = time.time()
        print "DBObjects setup finished after %0.2f real seconds." % (endReal - startReal)


        if debug == True:
            print "Debug switch is: %s" % debug
            self.debugMessages = debugMessages

        self.options = processingOptions

        self.openFiles = []


    def startTransaction(self):
        self.session = self.mappedObjects.session(echo_uow=True)
        print "Starting transaction..."


    def commitTransaction(self):
        self.session.commit()
        print "Transaction committed."


    def openFile(self, fileName):
        try:
            filePath = os.path.join(self.outDirectory, fileName)
            print "Opening CSV output file %s for writing... " % filePath,
            file = open(filePath, "wt+")
            print "opened."
            return file

        except:
            print "Unable to open CSV output file %s for writing!" % filePath
            raise


    def closeCsvFiles(self):
        print "Closing CSV output files... ",
        for file in self.openFiles:
            try:
                file.close()

            except:
                print "Unable to close CSV output file"
                raise

        print "all closed."

    
    ##########################################
    # Database Column-level Access Functions #
    ##########################################

    def getRacesData(self, personIndex):
        races = self.session.query(DBObjects.Races)\
                    .filter(DBObjects.Races.person_index_id == personIndex)

        # TBD: Do we care about which two races get output?

        primaryRace = None
        secondaryRace = None
                
        try:
            primaryRace = races[0].race_unhashed
            secondaryRace = races[1].race_unhashed

        except:
            pass

        return (primaryRace, secondaryRace)


    def getFundingSourceData(self, serviceIndex):
        fundingSources = self.session.query(DBObjects.FundingSource)\
            .filter(DBObjects.FundingSource.service_index_id == serviceIndex).first()
        
        try:
            receivesMcKinneyFunding = fundingSources.receives_mcKinney_funding

        except:
            receivesMcKinneyFunding = None

        return receivesMcKinneyFunding


    #######################################
    # Database Row-level Access Functions #
    #######################################

    def getPersonData(self, exportId):
        persons = self.session.query(DBObjects.Person)\
                      .filter(DBObjects.Person.export_id == exportId)

        # TBD: Figure out if/how to correctly handle reported:
        """
        if self.options.reported:
            persons = persons.filter(DBObjects.Person.reported == True)
        elif self.options.unreported:
            persons = persons.filter(DBObjects.Person.reported != True)
        """
        
        if not persons.count():
            print "Warning: there's no data in person table for export %s." \
                  % exportId
            return
        
        else:
            self.clientFile = self.openFile(HmisCsv30Writer.files["client"])
            self.openFiles.append(self.clientFile)
            self.clientWriter = csv.writer(self.clientFile, quoting=csv.QUOTE_NONNUMERIC)
            self.clientWriter.writerow(HmisCsv30Writer.clientHeader)
            
        for person in persons:
            try:
                if self.debug:
                    print "\n* person=", person

                yield person
                
            except:
                print "Unable to obtain data from person table!"
                raise


    def getInventoryData(self, siteServiceIndex):
        inventories = self.session.query(DBObjects.Inventory)\
            .filter(DBObjects.Inventory.site_service_index_id == siteServiceIndex)

        if not inventories.count():
            print "Warning: no data in inventory for site_service_id %s." \
                  % siteServiceIndex
            return
        
        else:
            self.inventoryFile = self.openFile(HmisCsv30Writer.files["inventory"])
            self.openFiles.append(self.inventoryFile)
            self.inventoryWriter = csv.writer(self.inventoryFile, quoting=csv.QUOTE_NONNUMERIC)
            self.inventoryWriter.writerow(HmisCsv30Writer.inventoryHeader)

        for inventory in inventories:
            try:
                if self.debug:
                    print "\n* inventory=", inventory
                    
                yield inventory

            except:
                print "Unable to obtain data from inventory table!"
                raise


    def getRegionData(self, siteServiceId):
        pass
    

    def getSiteServiceData(self, siteIndex):
        siteServices \
            = self.session.query(DBObjects.SiteService)\
                  .filter(DBObjects.SiteService.site_index_id == siteIndex)

        if not siteServices.count():
            print "Warning: no data in site_service for site index %s." \
                  % siteIndex
            return
        
        else:
            self.siteInfoFile = self.openFile(HmisCsv30Writer.files["siteInfo"])
            self.openFiles.append(self.siteInfoFile)
            self.siteInfoWriter = csv.writer(self.siteInfoFile, quoting=csv.QUOTE_NONNUMERIC)
            self.siteInfoWriter.writerow(HmisCsv30Writer.siteInfoHeader)

        for siteService in siteServices:
            try:
                if self.debug:
                    print "\n* site_service=", siteService
                    
                yield siteService

            except:
                print "Unable to obtain data from siteService table!"
                raise


    def getAgencyProgramData(self, exportIndex):
        self.orgId = None
        
        agencyPrograms \
            = self.session.query(DBObjects.Agency, DBObjects.Service, DBObjects.Site)\
                  .filter(and_(DBObjects.Agency.export_index_id == exportIndex,
                               DBObjects.Service.export_index_id == exportIndex,
                               DBObjects.Site.export_index_id == exportIndex,
                               DBObjects.Agency.id == DBObjects.Service.agency_index_id,
                               DBObjects.Agency.id == DBObjects.Site.agency_index_id))

        if not agencyPrograms.count():
            print "Warning: no data in (agency x service x site) for export %s." \
                  % self.exportId
            return
        
        else:
            self.agencyFile = self.openFile(HmisCsv30Writer.files["agency"])
            self.openFiles.append(self.agencyFile)
            self.agencyWriter = csv.writer(self.agencyFile, quoting=csv.QUOTE_NONNUMERIC)
            self.agencyWriter.writerow(HmisCsv30Writer.agencyHeader)

        for agency, service, site in agencyPrograms:
            try:
                if self.debug:
                    print "\n* agency=", agency
                    print "\n* service=", service
                    print "\n* site=", site
                    
                yield (agency, service, site)

            except:
                print "Unable to obtain data from agency, service, site tables!"
                raise


    def getSourceData(self, exportId):
        sources = self.session.query(DBObjects.Source)\
                      .filter(DBObjects.Source.export_id == exportId).first()
                      
        if not sources:
            print "Warning: there's no data in source table for export %s." \
                  % exportId
            return None

        try:
            if self.debug:
                print "\n* source=", sources

            return sources
                        
        except:
           print "Unable to obtain data from source table!"
           raise


    def getExportData(self):
        exports = self.session.query(DBObjects.Export)

        if not exports.count():
            print "Warning: there's no data in export table."
            return
        
        else:
            self.exportFile = self.openFile(HmisCsv30Writer.files["export"])
            self.openFiles.append(self.exportFile)
            self.exportWriter = csv.writer(self.exportFile, quoting=csv.QUOTE_NONNUMERIC)
            self.exportWriter.writerow(HmisCsv30Writer.exportHeader)

        for export in exports:
            try:
                if self.debug:
                    print "\n* export=", export
                yield export

            except:
                print "Unable to obtain data from export table!"
                raise


    ################################
    # CSV Record Creator Functions #
    ################################

    def createParticipationRecs(self, personIndex, personId):
        """
        for participation in self.getParticipationData(personIndex, personId):
            try:
                # Get the fields in site_service_participation table:
                entryDate = participation.participation_dates_start_date
                exitDate = participation.participation_dates_end_date
                vetStatus = participation.veteran_status
                disablingCond = participation.disabling_condition
                householdId = participation.household_idid_num
                dest = participation.destination

            except:
                print "Unable to interpret data from site_service_participation table!"
                raise

            # TBD: Other fields to implement:
            programId = None
            siteId = None
            
            dateUpdated = None
            priorResidence = None
            lengthPriorRes = None
            zipCode = None
            zipQual = None
            housingEntry = None
            housingExit = None
            reasonForLeaving = None
            relationshipToHead = None
            chronicHomeless = None

            # Build data row list:
            dataRow = \
            [
                personId, self.orgId, programId, siteId, entryDate, exitDate,
                dateUpdated, vetStatus, disablingCond, priorResidence,
                lengthPriorRes, zipCode, zipQual, housingEntry, housingExit,
                householdId, dest, reasonForLeaving, relationshipToHead,
                chronicHomeless, self.exportId
            ]

            try:
                print "\n* DataRow (ProgramParticipation)= ", dataRow
                self.participationWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["participation"]
                raise
        """
        pass
    
            
    def createClientRecs(self, exportId):
        for person in self.getPersonData(exportId):
            try:
                # Get the person index id to be used to get related data:
                personIndex = person.id

                # Get the fields in person table:
                personId = person.person_id_unhashed
                firstName = person.person_legal_first_name_unhashed
                middleName = person.person_legal_middle_name_unhashed
                lastName = person.person_legal_last_name_unhashed
                nameSuffix = person.person_legal_suffix_unhashed
                ssn = person.person_social_security_number_unhashed
                ssnQual = person.person_social_sec_number_quality_code
                dob = person.person_date_of_birth_unhashed
                ethnicity = person.person_ethnicity_unhashed
                gender = person.person_gender_unhashed

            except:
                print "Unable to interpret data from person table!"
                raise

            (primaryRace, secondaryRace) = self.getRacesData(personIndex)

            # TBD: Other fields to implement:
            dobQual = None
            dateAdded = None
            dateUpdated = None
            updateOrDelete = None
            idVerification = None
            releaseOfInfo = None

            # Build data row list:
            dataRow = \
            [
                self.orgId, personId, firstName, middleName, lastName, nameSuffix,
                ssn, ssnQual, dob, dobQual, primaryRace, secondaryRace, ethnicity,
                gender, dateAdded, dateUpdated, updateOrDelete, idVerification,
                releaseOfInfo, exportId
            ]

            try:
                if self.debug:
                    print "\n* DataRow (Client)= ", dataRow
                self.clientWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["client"]
                raise


    def createBedInventoryRecs(self, siteService):
        for inventory in self.getInventoryData(siteService.id):
            try:
                # Get the fields in site_service table:
                programId = siteService.service_id
                siteId = siteService.site_id
                
                # Get the fields in inventory table:
                householdType = inventory.household_type
                bedType = inventory.bed_type
                bedAvail = inventory.bed_availability
                #TBD: need bed_inventory added to table:
                bedInv = None   #inventory.bed_inventory
                chInv = inventory.chronic_homeless_bed
                unitInv = inventory.unit_inventory
                invStart = inventory.inventory_effective_period_start_date
                invEnd = inventory.inventory_effective_period_end_date
                hmisPartBeds = inventory.hmis_participating_beds
                hmisStart = inventory.hmis_participation_period_start_date
                hmisEnd = inventory.hmis_participation_period_end_date

                # TBD: Other fields to implement:
                assetListId = None
                assetListName = None
                dateUpdated = None
                
            except:
                print "Unable to interpret data from inventory tables!"
                raise

            # Build data row list:
            dataRow = \
            [
                self.orgID, programId, siteId, assetListId, assetListName, 
                householdType, bedType, bedAvail, bedInv, chInv, unitInv, invStart, 
                invEnd, hmisPartBeds, hmisStart, hmisEnd, dateUpdated, self.exportId
            ]

            try:
                if self.debug:
                    print "\n* DataRow (Inventory)= ", dataRow
                self.inventoryWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["inventory"]
                raise


    def createRegionsRecs(self, siteService):
        pass


    def createSiteInformationRecs(self, site):
        for siteService in self.getSiteServiceData(site.id):
            try:
                # Get the fields in site table:
                siteId = site.airs_key
                address = site.physical_address_line_1
                city = site.physical_address_city
                state =  site.physical_address_state
                zipCode = site.physical_address_zip_code
                
                # Get the fields in site_service table:
                geoCode = siteService.geographic_code
                siteServiceType = siteService.site_service_type
                housingType = siteService.housing_type 
                
                # TBD: Other fields to implement:
                dateUpdated = None

            except:
                print "Unable to interpret data from site, site_service tables!"
                raise

            # Build data row list:
            dataRow = \
            [
                self.orgID, siteId, address, city, state, zipCode, 
                geoCode, siteServiceType, housingType, dateUpdated, self.exportId
            ]

            try:
                if self.debug:
                    print "\n* DataRow (SiteInfo)= ", dataRow
                self.siteInfoWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["siteInfo"]
                raise

            self.createRegionsRecs(siteService)
            self.createBedInventoryRecs(siteService)


    def createAgencyProgramRecs(self, exportIndex):
        self.orgId = None

        for agency, service, site in self.getAgencyProgramData(exportIndex):
            try:
                # Get the fields in agency table:
                #agencyIndex = agency.id
                
                self.orgID = agency.airs_key
                orgName = agency.airs_name

                # Get the fields in service table:
                serviceIndex = service.id
                programId = service.airs_key
                programName = service.airs_name
                directServiceCode = service.direct_service_code
                programTypeCode = service.service_type
                targetPopulationA = service.target_population_a
                targetPopulationB = service.target_population_b
                trackingMethod = service.residential_tracking_method
                granteeIdentifier = service.grantee_identifier

                # Get the fields in site table:
                siteID = site.airs_key

                # Get the fields in related funding_source table:
                receivesMcKFunding = self.getFundingSourceData(serviceIndex)

                # TBD: Other fields to implement:
                dateCreated = None
                dateUpdated = None

            except:
                print "Unable to interpret data from agency, service, and/or site tables!"
                raise

            # Build data row list:
            dataRow = \
            [
                self.orgID, orgName, programId, programName, directServiceCode,
                siteID, programTypeCode, targetPopulationA, targetPopulationB,
                trackingMethod, granteeIdentifier, receivesMcKFunding, dateCreated,
                dateUpdated, self.exportId
            ]

            try:
                if self.debug:
                    print "\n* DataRow (AgencyProgram)= ", dataRow
                self.agencyWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["agency"]
                raise

            self.createSiteInformationRecs(site)


    def createExportRecs(self):
        self.exportid = None
        
        for export in self.getExportData():
            try:
                exportIndex = export.export_id
                
                self.exportId = export.export_id
                expDate = export.export_date.strftime("%m/%d/%Y")
                perStart = export.export_period_start_date.strftime("%m/%d/%Y")
                perEnd = export.export_period_end_date.strftime("%m/%d/%Y")

                # TBD: These moved to source for 3.0:
                #swVendor = export.export_software_vendor
                #swVersion = export.export_software_version

            except:
                print "Unable to interpret data from export table!"
                raise

            
            source = self.getSourceData(self.exportId)
    
            try:
                sourceId = getattr(source, "source_id", None)
                sourceName = getattr(source, "source_name", None)
                contactFirst = getattr(source, "source_contact_first", None)
                contactLast = getattr(source, "source_contact_last", None)
                contactPhone = getattr(source, "source_contact_phone", None)
                contactExt = getattr(source, "source_contact_extension", None)
                contactEmail = getattr(source, "source_email", None)

                # TBD: These are moved from export for 3.0:
                swVendor = getattr(source, "software_vendor_2010", None)
                swVersion = getattr(source, "software_version_2010", None)
                    
            except:
                    print "Unable to interpret data from source table!"
                    raise

            # TBD: Other fields to implement:
            self.exportHashing = None
            deltaRefresh = None

            # Build data row list:
            dataRow = \
            [
                 self.exportId, sourceId, sourceName, contactFirst, contactLast,
                 contactPhone, contactExt, contactEmail, expDate, perStart, perEnd,
                 self.exportHashing, swVendor, swVersion,
                 HmisCsv30Writer.files["agency"],
                 HmisCsv30Writer.files["inventory"],
                 HmisCsv30Writer.files["client"],
                 HmisCsv30Writer.files["historical"],
                 HmisCsv30Writer.files["incomeBenefits"],
                 # Outcome_measures file was removed from 3.0:
                 None,
                 HmisCsv30Writer.files["regions"],
                 HmisCsv30Writer.files["participation"],
                 HmisCsv30Writer.files["serviceEvent"],
                 HmisCsv30Writer.files["siteInfo"], deltaRefresh
            ]

            try:
                if self.debug:
                    print "\n* DataRow (Export)= ", dataRow
                self.exportWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["export"]
                raise

            self.createAgencyProgramRecs(exportIndex)
            self.createClientRecs(self.exportId)


    def createCsvFiles(self):
        self.createExportRecs();


    def write(self):
        self.startTransaction()
        self.createCsvFiles()
        self.closeCsvFiles()
        self.commitTransaction()
        print "Export finished."

        return True
