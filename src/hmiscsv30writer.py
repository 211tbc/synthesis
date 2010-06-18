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

    ########################
    # Constant Definitions #
    ########################

    files = \
    {
        "export" : "Export.csv",
        "agency" : "AgencyProgram.csv",
        "siteInfo" : "SiteInformation.csv",
        "regions" : "Regions.csv",
        "inventory" : "BedInventory.csv",
        "client" : "Client.csv",
        "historical" : "ClientHistorical.csv",
        "participation" : "ProgramParticipation.csv",
        "serviceEvent" : "ServiceEvent.csv",
        "incBens" : "IncomeBenefits.csv"
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

    incBensHeader = \
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


    ###################################
    # Miscellaneous Utility Functions #
    ###################################

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


    def extractDate(self, tsStr):
        try:
            dateStr = tsStr.strftime("%m/%d/%Y")
           
        except:
            dateStr = None

        return dateStr
                  
    ##########################################
    # Database Column-level Access Functions #
    ##########################################

    def getHistoryRelatedColumnData(self, phIndex, table, *columns):

        query = "self.session.query(DBObjects.%s)" % table\
              + ".filter(DBObjects.%s.person_historical_index_id == phIndex)" % table\
              +".first()"
        row = eval(query)
            
        # TBD: Do we care which row record gets returned?
        
        if self.debug:
            print "\n* %s = %s" % (table, row)

        retVal = []
        for column in columns:
            if not row:
                retVal.append(None)
                continue
            
            try:
                retVal.append(eval("row.%s" % column))
                 
            except:
                retVal.append(None)

        if len(retVal) == 1:
            return retVal[0]
        
        else:        
            return tuple(retVal)
        

    def getSchoolBarrier(self, cesIndex):
        barrier = self.session.query(DBObjects.ChildEnrollmentStatusBarrier)\
            .filter(DBObjects.ChildEnrollmentStatusBarrier.\
                    child_enrollment_status_index_id == cesIndex).first()
        # TBD: Do we care which zipCode_status record gets returned?

        if not barrier:
            return None
        
        if self.debug:
            print "\n* barrier = ", barrier
            
        try:
            barrierCd = barrier.barrier_code
             
        except:
            barrierCd = None

        return barrierCd


    def getPriorZipCodeData(self, phIndex):
        address = self.session.query(DBObjects.PersonAddress)\
            .filter(and_(DBObjects.PersonAddress.person_historical_index_id == phIndex,
                         DBObjects.PersonAddress.is_last_permanent_zip == 1)).first()
        # TBD: Do we care which zipCode_status record gets returned?

        if not address:
            return (None, None)
        
        if self.debug:
            print "\n* person_address = ", address
            
        zipCode = None
        zipQual = None
        
        try:
            zipCode = address.zipcode
            zipQual = address.zip_quality_code
             
        except:
            pass

        return (zipCode, zipQual)


    def getReasonForLeavingData(self, sspIndex):
        reason = self.session.query(DBObjects.ReasonsForLeaving)\
            .filter(DBObjects.ReasonsForLeaving.site_service_participation_index_id 
                    == sspIndex)\
            .first()
        # TBD: Do we care which reason_status record gets returned?
        
        if not reason:
            return None
        
        if self.debug:
            print "\n* reasons_for_leaving=", reason
            
        try:
            reasonCd = reason.reason_for_leaving
             
        except ZeroDivisionError:
            reasonCd = None

        return reasonCd


    def getPersonHistoricalIndexData(self, sspIndex):
        historical = self.session.query(DBObjects.PersonHistorical)\
            .filter(DBObjects.PersonHistorical.site_service_index_id == sspIndex).first()
        
        # TBD: Do we care which person historical record's index gets returned?

        if not historical:
            return None
        
        if self.debug:
            print "\n* person_historical=", historical
            
        try:
            phIndex = historical.id
             
        except:
            phIndex = None

        return phIndex


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


    def getReceivesMcKinneyFundingData(self, serviceIndex):
        funding = self.session.query(DBObjects.FundingSource)\
            .filter(DBObjects.FundingSource.service_index_id == serviceIndex).first()

        if not funding:
            return None
        
        try:
            receivesMcKinneyFunding = funding.receives_mcKinney_funding

        except:
            receivesMcKinneyFunding = None

        return receivesMcKinneyFunding


    def getFundingSourceData(self, seIndex):
        funding = self.session.query(DBObjects.FundingSource)\
            .filter(DBObjects.FundingSource.service_event_index_id == seIndex).first()

        if not funding:
            return None
        
        faAmt = None
        grantId = None
        advArrears = None
        
        try:
            faAmt = funding.financial_assistance_amount
            grantId = funding.federal_cfda_number
            advArrears = funding.advance_or_arrears

        except:
            pass

        return (faAmt, grantId, advArrears)



    #######################################
    # Database Row-level Access Functions #
    #######################################

    def getNonCashBenefitsData(self, phIndex):
        print "in gncbd"
        nonCashBens = self.session.query(DBObjects.NonCashBenefits)\
            .filter(DBObjects.NonCashBenefits.person_historical_index_id == phIndex)

        if not nonCashBens.count():
            return
        
        for nonCashBen in nonCashBens:
            try:
                if self.debug:
                    print "\n* non_cash_benefits=", nonCashBen

                yield nonCashBen
                
            except:
                print "Unable to obtain data from non_cash_benefits table!"
                raise


    def getIncomeAndSourcesData(self, phIndex):
        print "in gisd"
        incomes = self.session.query(DBObjects.IncomeAndSources)\
            .filter(DBObjects.IncomeAndSources.person_historical_index_id == phIndex)

        if not incomes.count():
            return
        
        for income in incomes:
            try:
                if self.debug:
                    print "\n* income_and_sources=", income

                yield income
                
            except:
                print "Unable to obtain data from income_and_sources table!"
                raise


    def getPersonHistoricalData(self, personIndex, personId):
        historicals = self.session.query(DBObjects.PersonHistorical)\
            .filter(DBObjects.PersonHistorical.person_index_id == personIndex)

        if not historicals.count():
            print "Warning: no data in person_historical table for person %s." \
                  % personId
            return
        
        else:
            self.historicalFile = self.openFile(HmisCsv30Writer.files["historical"])
            self.openFiles.append(self.historicalFile)
            self.historicalWriter = csv.writer(self.historicalFile,
                                               quoting=csv.QUOTE_NONNUMERIC)
            self.historicalWriter.writerow(HmisCsv30Writer.historicalHeader)

        for historical in historicals:
            try:
                if self.debug:
                    print "\n* person_historical=", historical

                yield historical
                
            except:
                print "Unable to obtain data from person_historical table!"
                raise


    def getServiceEventData(self, personIndex, personId):
        serviceEvents = self.session.query(DBObjects.ServiceEvent)\
            .filter(DBObjects.ServiceEvent.person_index_id_2010 == personIndex)

        if not serviceEvents.count():
            print "Warning: no data in service_event table for person %s." % personId
            return
        
        else:
            self.serviceEventFile = self.openFile(HmisCsv30Writer.files["serviceEvent"])
            self.openFiles.append(self.serviceEventFile)
            self.serviceEventWriter = csv.writer(self.serviceEventFile,
                                                  quoting=csv.QUOTE_NONNUMERIC)
            self.serviceEventWriter.writerow(HmisCsv30Writer.serviceEventHeader)

        for serviceEvent in serviceEvents:
            try:
                if self.debug:
                    print "\n* service_event=", serviceEvent

                yield serviceEvent
                
            except:
                print "Unable to obtain data from service_event table!"
                raise


    def getParticipationData(self, personIndex, personId):
        participations = self.session.query(DBObjects.SiteServiceParticipation)\
            .filter(DBObjects.SiteServiceParticipation.person_index_id == personIndex)

        if not participations.count():
            print "Warning: no data in site_service_participation table for person %s." \
                  % personId
            return
        
        else:
            self.participationFile = self.openFile(HmisCsv30Writer.files["participation"])
            self.openFiles.append(self.participationFile)
            self.participationWriter = csv.writer(self.participationFile,
                                                  quoting=csv.QUOTE_NONNUMERIC)
            self.participationWriter.writerow(HmisCsv30Writer.participationHeader)

        for participation in participations:
            try:
                if self.debug:
                    print "\n* site_service_participation=", participation

                yield participation
                
            except:
                print "Unable to obtain data from site_service_participation table!"
                raise


    def getPersonData(self, exportId):
        persons = self.session.query(DBObjects.Person)\
                      .filter(DBObjects.Person.export_id == exportId)

        if exportId == None:
            print "listen, bub, you cant select on null export id"
            
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
        regions = self.session.query(DBObjects.Region)\
                      .filter(DBObjects.Region.site_service_id == siteServiceId)

        if not regions.count():
            print "Warning: no data in region for site_service_id %s." % siteServiceId
            return
        
        else:
            self.regionsFile = self.openFile(HmisCsv30Writer.files["regions"])
            self.openFiles.append(self.regionsFile)
            self.regionsWriter = csv.writer(self.regionsFile, quoting=csv.QUOTE_NONNUMERIC)
            self.regionsWriter.writerow(HmisCsv30Writer.regionsHeader)

        for region in regions:
            try:
                if self.debug:
                    print "\n* region=", region
                    
                yield region

            except:
                print "Unable to obtain data from region table!"
                raise


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
        agencyPrograms \
            = self.session.query(DBObjects.Agency, DBObjects.Service, DBObjects.Site)\
                  .filter(and_(DBObjects.Agency.export_index_id == exportIndex,
                               DBObjects.Service.export_index_id == exportIndex,
                               DBObjects.Site.export_index_id == exportIndex,
                               DBObjects.Agency.airs_key == DBObjects.Service.airs_key,
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


    ####################################################
    # Database Concatenated Row-level Access Functions #
    ####################################################

    def getIncomeAndNonCashBenefitsData(self, phIndex):
        
        IB_TYPE_INCOME = '1'
        IB_TYPE_NON_CASH = '2'
        
        for ias in self.getIncomeAndSourcesData(phIndex):            
            # Return (IncomeBenefitType, SourceCode, SourceOther, MonthlyAmount):
            yield (IB_TYPE_INCOME, ias.income_source_code, 
                   ias.income_source_other, ias.amount)
            
        for ncb in self.getNonCashBenefitsData(phIndex):        
            # Return (non_cashBenefitType, SourceCode, SourceOther, MonthlyAmount):
            yield (IB_TYPE_NON_CASH, ncb.non_cash_source_code, 
                   ncb.non_cash_source_other, None)


    ################################
    # CSV Record Creator Functions #
    ################################

    def createServiceEventRecs(self, personIndex, personId):
         for serviceEvent in self.getServiceEventData(personIndex, personId):
            try:
                # Get the fields in service_event table:
                seIndex = serviceEvent.site_service_index_id
                seType = serviceEvent.type_of_service
                seStartDt = self.extractDate(serviceEvent.service_period_start_date) 
                seEndDt  = self.extractDate(serviceEvent.service_period_end_date)
                serviceAirsCd = serviceEvent.service_airs_code
                isReferral = serviceEvent.is_referral
                quantFreq = serviceEvent.quantity_of_service

                (faAmt, grantId, advArrears) = self.getFundingSourceData(seIndex)

            except:
                print "Unable to interpret data from service_event table!"
                raise

            # TBD: Other fields to implement:
            orgId = None
            programId = None
            siteId = None
            serviceCd = None
            fundcat = None
            isRecurring = None
            periodInt = None
            contTime = None
            contSite = None
            clientEngaged = None
            assetListId = None
            assetId = None
            domainIdCd = None
            dateUpdated = self.extractDate(None)

            # Build data row list:
            dataRow = \
            [
                personId, orgId, programId, siteId, seType, seStartDt, seEndDt, 
                serviceCd, serviceAirsCd, isReferral, quantFreq, faAmt, fundcat, 
                grantId, isRecurring, periodInt, advArrears, contTime, contSite,
                clientEngaged, assetListId, assetId, domainIdCd, dateUpdated,   
                self.exportId
            ]

            try:
                print "\n* DataRow (ServiceEvent)= ", dataRow
                self.serviceEventWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["serviceEvent"]
                raise


    def createIncomeBenefitsRecs(self, phIndex, personId):
        for (ibType, srcCode, srcOther, monthlyAmt)\
            in self.getIncomeAndNonCashBenefitsData(phIndex):
            
            # TBD: Other fields to implement:
            orgId = None
            programId = None
            siteId = None
            
            assessDate = self.extractDate(None)
            dateUpdated = self.extractDate(None)
            
            # Build data row list:
            dataRow = \
            [
                personId, orgId, programId, siteId, assessDate, dateUpdated, 
                ibType, monthlyAmt, srcCode, srcOther, monthlyAmt, 
                self.exportId
            ]

            try:
                if not getattr(self, "incBensFile", None):
                    self.incBensFile = self.openFile(HmisCsv30Writer.files["incBens"])
                    self.openFiles.append(self.incBensFile)
                    self.incBensWriter = csv.writer(self.incBensFile,
                                                    quoting=csv.QUOTE_NONNUMERIC)
                
                print "\n* DataRow (IncomeBenefits)= ", dataRow
                self.incBensWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["incBens"]
                raise


    def createParticipationRecs(self, personIndex, personId):
         for participation in self.getParticipationData(personIndex, personId):
            try:
                # Get the fields in site_service_participation table:
                sspIndex = participation.id
                entryDate = self.extractDate(participation.participation_dates_start_date)
                exitDate = self.extractDate(participation.participation_dates_end_date)

                # Get fields related to site_service_participation table:
                phIndex = self.getPersonHistoricalIndexData(sspIndex)
                reasonForLeaving = self.getReasonForLeavingData(sspIndex)

                # Get fields from subtables simply related to person_historical table:                
                vetStatus = self.getHistoryRelatedColumnData(phIndex,
                    "VeteranVeteranStatus", "veteran_status")                
                disCond = self.getHistoryRelatedColumnData(phIndex,
                    "DisablingCondition", "disabling_condition") 
                priorRes = self.getHistoryRelatedColumnData(phIndex,
                    "PriorResidence", "prior_residence_code")
                lengthPriorStay = self.getHistoryRelatedColumnData(phIndex,
                    "LengthOfStayAtPriorResidence", "length_of_stay_at_prior_residence") 
                dest = self.getHistoryRelatedColumnData(phIndex,
                    "Destinations", "destination_code")
                chronicHomeless = self.getHistoryRelatedColumnData(phIndex,
                    "HudChronicHomeless", "hud_chronic_homeless")

                # Get fields from subtables non-simply related to person_historical table:                
                zipCode, zipQual = self.getPriorZipCodeData(phIndex) 

            except:
                print "Unable to interpret data from site_service_participation table!"
                raise

            # TBD: Other fields to implement:
            orgId = None
            programId = None
            siteId = None
            
            dateUpdated = self.extractDate(None)
            housingEntry = None
            housingExit = None
            householdId = None
            relationshipToHead = None

            # Build data row list:
            dataRow = \
            [
                personId, orgId, programId, siteId, entryDate, exitDate,
                dateUpdated, vetStatus, disCond, priorRes, lengthPriorStay, zipCode, 
                zipQual, housingEntry, housingExit, householdId, dest, reasonForLeaving, 
                relationshipToHead, chronicHomeless, self.exportId
            ]

            try:
                print "\n* DataRow (ProgramParticipation)= ", dataRow
                self.participationWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["participation"]
                raise

            self.createServiceEventRecs(personIndex, personId)
     

    def createClientHistoricalRecs(self, personIndex, personId):
         for historical in self.getPersonHistoricalData(personIndex, personId):
            try:
                # Get the fields in site_service_participation table:
                phIndex = historical.id

                # Get fields from subtables simply related to person_historical table:                
                monthlyIncome = self.getHistoryRelatedColumnData(phIndex,
                    "IncomeTotalMonthly", "income_total_monthly")
                income30 =  self.getHistoryRelatedColumnData(phIndex,
                    "IncomeLast30Days", "income_last_30_days")
                noncash30 = self.getHistoryRelatedColumnData(phIndex,
                    "NonCashBenefitsLast30Days", "income_last_30_days")                
                physDis, recvPhysDis = self.getHistoryRelatedColumnData(phIndex,
                    "PhysicalDisability", 
                    "has_physical_disability", "receive_physical_disability_services")                                            
                devDis, recvDevDis = self.getHistoryRelatedColumnData(phIndex,
                    "DevelopmentalDisability", 
                    "has_developmental_disability", "receive_developmental_disability")                
                chronicCond, recvChronic = self.getHistoryRelatedColumnData(phIndex,
                    "ChronicHealthCondition", 
                    "has_chronic_health_condition", "receive_chronic_health_services")                
                hivAids, recvHivAids = self.getHistoryRelatedColumnData(phIndex,
                    "HivAidsStatus", "has_hiv_aids", "receive_hiv_aids_services")
                mental, mentalIndef,recvMental = self.getHistoryRelatedColumnData(phIndex,
                    "MentalHealthProblem", "has_mental_health_problem", 
                    "mental_health_indefinite", "receive_mental_health_services")
                substance, substanceIndef, recvSubstance \
                    = self.getHistoryRelatedColumnData(phIndex,
                    "SubstanceAbuseProblem", "has_substance_abuse_problem", 
                    "substance_abuse_indefinite", "receive_substance_abuse_services")
                violence,violenceOccured = self.getHistoryRelatedColumnData(phIndex,
                    "DomesticViolence", 
                    "domestic_violence_survivor", "dv_occurred")
                employed, hoursLastWk, tenure, looking \
                    = self.getHistoryRelatedColumnData(phIndex, "Employment",
                    "currently_employed", "hours_worked_last_week",
                    "employment_tenure", "looking_for_work")                                                                                         
                inSchool = self.getHistoryRelatedColumnData(phIndex,
                     "CurrentlyInSchool", "currently_in_school")
                vocational = self.getHistoryRelatedColumnData(phIndex,
                    "VocationalTraining", "vocational_training")
                highestSchool = self.getHistoryRelatedColumnData(phIndex,
                    "HighestSchoolLevel", "highest_school_level")
                degree = self.getHistoryRelatedColumnData(phIndex,
                    "Degree", "degree_id_id_num")
                healthStatus = self.getHistoryRelatedColumnData(phIndex,
                    "HealthStatus", "health_status")            
                pregnant, dueDate = self.getHistoryRelatedColumnData(phIndex,
                    "Pregnancy", "pregnancy_status", "due_date")
                dueDate = self.extractDate(dueDate)                
                serviceEra = self.getHistoryRelatedColumnData(phIndex,
                    "VeteranServiceEra", "service_era")
                serviceDur = self.getHistoryRelatedColumnData(phIndex,
                    "VeteranMilitaryServiceDuration", "military_service_duration")
                servedInWz  = self.getHistoryRelatedColumnData(phIndex, 
                    "VeteranServedInWarZone", "served_in_war_zone")
                warZone, wzMonths, wzFire = self.getHistoryRelatedColumnData(phIndex, 
                    "VeteranWarzonesServed", "war_zone_id_id_id_num", 
                    "months_in_war_zone", "received_fire")
                branch, discharge = self.getHistoryRelatedColumnData(phIndex,
                    "VeteranMilitaryBranches", "military_branch", "discharge_status")
                cesIndex, childInSchool, school, mvLiason, schoolType, lastSchoolDt \
                     = self.getHistoryRelatedColumnData(phIndex, "ChildEnrollmentStatus", 
                     "id", "child_currently_enrolled_in_school", 
                     "child_school_name", "child_mckinney_vento_liason", 
                     "child_school_type", "child_last_enrolled_date")
                     
                # Get fields from subtables non-simply related to person_historical table:                                
                schoolBarrier  = self.getSchoolBarrier(cesIndex)
                
            except:
                print "Unable to interpret data from client_historical table!"
                raise

            # TBD: Other fields to implement:
            orgId = None
            programId = None
            siteId = None
            
            assessDate = None
            dateUpdated = self.extractDate(None)
            
            # Build data row list:
            dataRow = \
            [
                personId, orgId, programId, siteId, assessDate, dateUpdated,
                monthlyIncome, income30, noncash30, physDis, recvPhysDis,
                devDis, recvDevDis, chronicCond, recvChronic, hivAids, recvHivAids, 
                mental, mentalIndef, recvMental, substance, substanceIndef, 
                recvSubstance, violence, violenceOccured, employed, hoursLastWk, 
                tenure, looking, inSchool, vocational, highestSchool, degree, 
                healthStatus, pregnant, dueDate, serviceEra, serviceDur, servedInWz, 
                warZone, wzMonths, wzFire, branch, discharge, childInSchool, school, 
                mvLiason, schoolType, lastSchoolDt, schoolBarrier, self.exportId
            ]

            try:
                print "\n* DataRow (ClientHistorical)= ", dataRow
                self.historicalWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["historical"]
                raise

            self.createIncomeBenefitsRecs(phIndex, personId)


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
                dob = self.extractDate(person.person_date_of_birth_unhashed)
                ethnicity = person.person_ethnicity_unhashed
                gender = person.person_gender_unhashed

            except:
                print "Unable to interpret data from person table!"
                raise

            (primaryRace, secondaryRace) = self.getRacesData(personIndex)

            # TBD: Other fields to implement:
            orgId = None
            dobQual = None
            dateAdded = self.extractDate(None)
            dateUpdated = self.extractDate(None)
            updateOrDelete = None
            idVerification = None
            releaseOfInfo = None

            # Build data row list:
            dataRow = \
            [
                orgId, personId, firstName, middleName, lastName, nameSuffix,
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

            self.createClientHistoricalRecs(personIndex, personId)
            self.createParticipationRecs(personIndex, personId)            

    
    def createBedInventoryRecs(self, siteService, orgId):
        for inventory in self.getInventoryData(siteService.id):
            try:
                # Get the fields in site_service table:
                programId = siteService.service_id
                siteId = siteService.site_id
                
                # Get the fields in inventory table:
                householdType = inventory.household_type
                bedType = inventory.bed_type
                bedAvail = inventory.bed_availability
                bedInv = inventory.bed_inventory
                chInv = inventory.chronic_homeless_bed
                unitInv = inventory.unit_inventory
                invStart = self.extractDate(inventory.inventory_effective_period_start_date)
                invEnd = self.extractDate(inventory.inventory_effective_period_end_date)
                hmisPartBeds = inventory.hmis_participating_beds
                hmisStart = self.extractDate(inventory.hmis_participation_period_start_date)
                hmisEnd = self.extractDate(inventory.hmis_participation_period_end_date)

                # TBD: Other fields to implement:
                assetListId = None
                assetListName = None
                dateUpdated = self.extractDate(None)
                
            except:
                print "Unable to interpret data from inventory tables!"
                raise

            # Build data row list:
            dataRow = \
            [
                orgId, programId, siteId, assetListId, assetListName, 
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


    def createRegionsRecs(self, siteService, orgId):
        for region in self.getRegionData(siteService.key):
            try:
                # Get the fields in site_service table:
                siteId = siteService.site_id
                
                # Get the fields in region table:

                #TBD: Which field is ID?
                regionId = region.id
                regionType = region.region_type
                descript = region.region_description
                
                # TBD: Other fields to implement:
                dateUpdated = self.extractDate(None)

            except:
                print "Unable to interpret data from region tables!"
                raise

            # Build data row list:
            dataRow = \
            [
                orgId, siteId, regionId, regionType, 
                descript, dateUpdated, self.exportId
            ]

            try:
                if self.debug:
                    print "\n* DataRow (Regions)= ", dataRow
                self.regionsWriter.writerow(dataRow)
                
            except:
                print "Unable to write record to CSV file %s!" \
                      % HmisCsv30Writer.files["regions"]
                raise


    def createSiteInformationRecs(self, site, orgId):
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
                dateUpdated = self.extractDate(None)

            except:
                print "Unable to interpret data from site, site_service tables!"
                raise

            # Build data row list:
            dataRow = \
            [
                orgId, siteId, address, city, state, zipCode, 
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

            self.createRegionsRecs(siteService, orgId)
            self.createBedInventoryRecs(siteService, orgId)


    def createAgencyProgramRecs(self, exportIndex):
        orgId = None

        for agency, service, site in self.getAgencyProgramData(exportIndex):
            try:
                # Get the fields in agency table:
                #agencyIndex = agency.id
                
                orgId = agency.airs_key
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
                receivesMcKFunding = self.getReceivesMcKinneyFundingData(serviceIndex)

                # TBD: Other fields to implement:
                dateCreated = self.extractDate(None)
                dateUpdated = self.extractDate(None)

            except:
                print "Unable to interpret data from agency, service, and/or site tables!"
                raise

            # Build data row list:
            dataRow = \
            [
                orgId, orgName, programId, programName, directServiceCode,
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

            self.createSiteInformationRecs(site, orgId)


    def createExportRecs(self):
        self.exportid = None
        
        for export in self.getExportData():
            try:
                exportIndex = export.export_id
                
                self.exportId = export.export_id
                expDate = self.extractDate(export.export_date)
                perStart = self.extractDate(export.export_period_start_date)
                perEnd = self.extractDate(export.export_period_end_date)

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
                 HmisCsv30Writer.files["incBens"],
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
