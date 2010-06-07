''' 
    Reads a HUD HMIS XML 3.0 Document into memory and parses its contents storing them into a postgresql database.
    This is a log database, so it holds everything and doesn't worry about deduplication.
    The only thing it enforces are exportids, which must be unique.
'''

import sys, os
from reader import Reader
from zope.interface import implements
from lxml import etree
from sqlalchemy.exceptions import IntegrityError
import dateutil.parser
from conf import settings
import clsExceptions
import DBObjects
from fileUtils import fileUtilities
from errcatalog import catalog

class HMISXML30Reader(DBObjects.databaseObjects):
    ''' Implements reader interface '''
    implements (Reader) 

    ''' Define XML namespaces '''
    hmis_namespace = "http://www.hmis.info/schema/3_0/HUD_HMIS.xsd" 
    airs_namespace = "http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd"
    nsmap = {"hmis" : hmis_namespace, "airs" : airs_namespace}

    ''' Instantiate FileUtilities '''
    global FU
    FU = fileUtilities(settings.DEBUG, None)

    def __init__(self, xml_file):
        ''' Put XML file into local object '''
        self.xml_file = xml_file

        ''' Instantiate database object '''
        dbo = DBObjects.databaseObjects()
        self.session = dbo.session()

    def read(self):
        ''' Takes an XML instance file and reads it into memory as a node tree '''
        #print '** Raw XML:', self.xml_file
        tree = etree.parse(self.xml_file)
        #print '** Node tree:', tree
        #self.xml_file.close()
        return tree

    def process_data(self, tree):
        ''' Shreds the XML document into the database '''
        root_element = tree.getroot()
        self.parse_source(root_element)
        return
        
    ''' Parse each table '''
    def parse_source(self, root_element):
        ''' Loop through all sources and then traverse the tree for each export '''
        ''' There can be multiple sources with multiple exports inside each source '''

        xpSources = '/hmis:Sources/hmis:Source'
        source_list = root_element.xpath(xpSources, namespaces={'hmis': self.hmis_namespace})
        if source_list is not None:
            for item in source_list:
                self.parse_dict = {}

                ''' Element paths '''
                xpSourceVersion = '../@hmis:version'                
                xpSourceIDIDNum = 'hmis:SourceID/hmis:IDNum'
                xpSourceIDIDStr = 'hmis:SourceID/hmis:IDStr'
                xpSourceDelete = 'hmis:SourceID/@hmis:Delete'
                xpSourceDeleteOccurredDate = 'hmis:SourceID/@hmis:DeleteOccurredDate'
                xpSourceDeleteEffective = 'hmis:SourceID/@hmis:DeleteEffective'
                xpSourceSoftwareVendor = 'hmis:SoftwareVendor'
                xpSourceSoftwareVersion = 'hmis:SoftwareVersion'
                xpSourceContactEmail = 'hmis:SourceContactEmail'
                xpSourceContactExtension = 'hmis:SourceContactExtension'
                xpSourceContactFirst = 'hmis:SourceContactFirst'        
                xpSourceContactLast = 'hmis:SourceContactLast'        
                xpSourceContactPhone = 'hmis:SourceContactPhone'
                xpSourceName = 'hmis:SourceName'

                ''' Map elements to database columns '''
                self.existence_test_and_add('attr_version', item.xpath(xpSourceVersion, namespaces={'hmis': self.hmis_namespace}), 'attribute_text')
                self.existence_test_and_add('source_id_id_id_num_2010', item.xpath(xpSourceIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_id_id_id_str_2010', item.xpath(xpSourceIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_id_id_delete_2010', item.xpath(xpSourceDelete, namespaces={'hmis': self.hmis_namespace}), 'attribute_text')
                self.existence_test_and_add('source_id_id_delete_occurred_date_2010', item.xpath(xpSourceDeleteOccurredDate, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('source_id_id_delete_effective_2010', item.xpath(xpSourceDeleteEffective, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('software_vendor_2010', item.xpath(xpSourceSoftwareVendor, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('software_version_2010', item.xpath(xpSourceSoftwareVersion, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_email_2010', item.xpath(xpSourceContactEmail, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_extension', item.xpath(xpSourceContactExtension, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_first', item.xpath(xpSourceContactFirst, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_last', item.xpath(xpSourceContactLast, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_contact_phone', item.xpath(xpSourceContactPhone, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_name', item.xpath(xpSourceName, namespaces={'hmis': self.hmis_namespace}), 'text')

                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Source)

                ''' Parse all exports for this specific source '''
                self.parse_export(item)
        return                

    def parse_export(self, element):
        ''' loop through all exports and traverse the tree '''
        
        ''' Element paths '''
        xpExport = 'hmis:Export'
        xpExportIDIDNum = 'hmis:ExportID/hmis:IDNum'
        xpExportIDIDStr = 'hmis:ExportID/hmis:IDStr'
        xpExportDelete = 'hmis:ExportID/@hmis:Delete'
        xpExportDeleteOccurredDate = 'hmis:ExportID/@hmis:DeleteOccurredDate'
        xpExportDeleteEffective = 'hmis:ExportID/@hmis:DeleteEffective'
        xpExportExportDate = 'hmis:ExportDate'
        xpExportPeriodStartDate = 'hmis:ExportPeriod/hmis:StartDate'
        xpExportPeriodEndDate = 'hmis:ExportPeriod/hmis:EndDate'
        
        itemElements = element.xpath(xpExport, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}

                ''' Map elements to database columns '''
                test = item.xpath(xpExportIDIDNum, namespaces={'hmis': self.hmis_namespace}) 
                if len(test) is 0:
                    test = item.xpath(xpExportIDIDStr, namespaces={'hmis': self.hmis_namespace})
                    self.export_id = test
                    value = self.existence_test_and_add('export_id', test, 'text')
                else:
                    self.export_id = test
                    self.existence_test_and_add('export_id', test, 'text')
                self.existence_test_and_add('export_id_id_id_num_2010', item.xpath(xpExportIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('export_id_id_id_str_2010', item.xpath(xpExportIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('export_id_id_delete_2010', item.xpath(xpExportDelete, namespaces={'hmis': self.hmis_namespace}), 'attribute_text')
                self.existence_test_and_add('export_id_id_delete_occurred_date_2010', item.xpath(xpExportDeleteOccurredDate, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_id_id_delete_effective_2010', item.xpath(xpExportDeleteEffective, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_date', item.xpath(xpExportExportDate, namespaces={'hmis': self.hmis_namespace}), 'element_date') 
                self.existence_test_and_add('export_period_start_date', item.xpath(xpExportPeriodStartDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                self.existence_test_and_add('export_period_end_date', item.xpath(xpExportPeriodEndDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')

                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Export)
                
                ''' Create source to export link '''
                self.record_source_export_link()

                ''' Parse sub-tables '''
                self.parse_household(item)
                self.parse_region(item)
                self.parse_agency(item)
                self.parse_person(item)
                self.parse_service(item)
                self.parse_site(item)
                self.parse_site_service(item)
        return

    def parse_household(self, element):
        ''' Element paths '''
        xpHousehold = 'hmis:Household'
        xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
        xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'
        xpHeadOfHouseholdIDUnhashed = 'hmis:HeadOfHouseholdID/hmis:Unhashed'
        xpHeadOfHouseholdIDHashed = 'hmis:HeadOfHouseholdID/hmis:Hashed'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}

                ''' Map elements to database columns '''
                self.existence_test_and_add('household_id_num', item.xpath(xpHouseholdIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('household_id_str', item.xpath(xpHouseholdIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('head_of_household_id_unhashed', item.xpath(xpHeadOfHouseholdIDUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('head_of_household_id_hashed', item.xpath(xpHeadOfHouseholdIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')

                ''' Foreign Keys '''
                self.existence_test_and_add('export_id', self.export_id, 'text')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Household)
    
                ''' Parse sub-tables '''
                self.parse_members(item)
    
    def parse_members(self, element):
        ''' Element paths '''
        xpMembers = 'hmis:Members'
        xpMember = 'hmis:Member'
        xpPersonIDUnhashed = 'hmis:PersonID/hmis:Unhashed'
        xpPersonIDHashed = 'hmis:PersonID/hmis:Hashed'
        xpRelationshipToHeadOfHousehold = 'hmis:RelationshipToHeadOfHousehold'
        
        test = element.xpath(xpMembers, namespaces={'hmis': self.hmis_namespace})
        if len(test) > 0:
            itemElements = test[0].xpath(xpMember, namespaces={'hmis': self.hmis_namespace})
            if itemElements is not None:
                for item in itemElements:
                    self.parse_dict = {}

                    ''' Map elements to database columns '''
                    self.existence_test_and_add('person_id_unhashed', item.xpath(xpPersonIDUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_id_hashed', item.xpath(xpPersonIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('relationship_to_head_of_household', item.xpath(xpRelationshipToHeadOfHousehold, namespaces={'hmis': self.hmis_namespace}), 'text')
        
                    ''' Foreign Keys '''
                    self.existence_test_and_add('household_index_id', self.household_index_id, 'no_handling')
        
                    ''' Shred to database '''
                    self.shred(self.parse_dict, DBObjects.Members)

    def parse_region(self, element):
        ''' Element paths '''
        xpRegion = 'hmis:Region'
        xpRegionIDIDNum = 'hmis:RegionID/hmis:IDNum'
        xpRegionIDIDStr = 'hmis:RegionID/hmis:IDStr'
        xpSiteServiceID = 'hmis:SiteServiceID'
        xpRegionType = 'hmis:RegionType'
        xpRegionTypeDateCollected = 'hmis:RegionType/@hmis:dateCollected'
        xpRegionTypeDateEffective = 'hmis:RegionType/@hmis:dateEffective'
        xpRegionTypeDataCollectionStage = 'hmis:RegionType/@hmis:dataCollectionStage'
        xpRegionDescription = 'hmis:RegionDescription'
        xpRegionDescriptionDateCollected = 'hmis:RegionDescription/@hmis:dateCollected'
        xpRegionDescriptionDateEffective = 'hmis:RegionDescription/@hmis:dateEffective'
        xpRegionDescriptionDataCollectionStage = 'hmis:RegionDescription/@hmis:dataCollectionStage'
        
        itemElements = element.xpath(xpRegion, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                self.existence_test_and_add('region_id_id_num', item.xpath(xpRegionIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('region_id_id_str', item.xpath(xpRegionIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('site_service_id', item.xpath(xpSiteServiceID, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('region_type', item.xpath(xpRegionType, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('region_type_date_collected', item.xpath(xpRegionTypeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('region_type_date_effective', item.xpath(xpRegionTypeDateEffective, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('region_type_data_collection_stage', item.xpath(xpRegionTypeDataCollectionStage, namespaces={'hmis': self.hmis_namespace}), 'attribute_text')
                self.existence_test_and_add('region_description', item.xpath(xpRegionDescription, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('region_description_date_collected', item.xpath(xpRegionDescriptionDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('region_description_date_effective', item.xpath(xpRegionDescriptionDateEffective, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('region_description_data_collection_stage', item.xpath(xpRegionDescriptionDataCollectionStage, namespaces={'hmis': self.hmis_namespace}), 'attribute_text')

                ''' Foreign Keys '''
                self.existence_test_and_add('export_id', self.export_id, 'text')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Region)
    
    def parse_agency(self, element):
        ''' Element paths '''
        xpAgency = 'hmis:Agency'
        xpAgencyDelete = '@hmis:Delete'
        xpAgencyDeleteOccurredDate = '@hmis:DeleteOccurredDate'
        xpAgencyDeleteEffective = '@hmis:DeleteEffective'
        xpAirsKey = 'airs:Key'
        xpAirsName = 'airs:Name'
        xpAgencyDescription = 'airs:AgencyDescription'
        xpIRSStatus = 'airs:IRSStatus'
        xpSourceOfFunds = 'airs:SourceOfFunds'
        xpRecordOwner = '@hmis:RecordOwner'
        xpFEIN = '@hmis:FEIN'
        xpYearInc = '@hmis:YearInc'
        xpAnnualBudgetTotal = '@hmis:AnnualBudgetTotal'
        xpLegalStatus = '@hmis:LegalStatus'
        xpExcludeFromWebsite = '@hmis:ExcludeFromWebsite'
        xpExcludeFromDirectory = '@hmis:ExcludeFromDirectory'
        
        itemElements = element.xpath(xpAgency, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                self.existence_test_and_add('attr_delete', item.xpath(xpAgencyDelete, namespaces={'hmis': self.hmis_namespace}), 'attribute_text')
                self.existence_test_and_add('attr_delete_occurred_date', item.xpath(xpAgencyDeleteOccurredDate, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('attr_effective', item.xpath(xpAgencyDeleteOccurredDate, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')

                self.existence_test_and_add('airs_key', item.xpath(xpAirsKey, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('airs_name', item.xpath(xpAirsName, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('agency_description', item.xpath(xpAgencyDescription, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('irs_status', item.xpath(xpIRSStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('source_of_funds', item.xpath(xpSourceOfFunds, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('fein', item.xpath(xpFEIN, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('record_owner', item.xpath(xpRecordOwner, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('year_inc', item.xpath(xpYearInc, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('annual_budget_total', item.xpath(xpAnnualBudgetTotal, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_status', item.xpath(xpLegalStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('exclude_from_website', item.xpath(xpExcludeFromWebsite, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('exclude_from_directory', item.xpath(xpExcludeFromDirectory, namespaces={'hmis': self.hmis_namespace}), 'text')

                ''' Foreign Keys '''
                self.existence_test_and_add('export_id', self.export_id, 'text')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Agency)

                #### check for child agency ? or just skip altogether ?
                #self.record_agency_child_link()
    
                ''' Parse sub-tables '''
                self.parse_service_group(item)
                self.parse_license_accreditation(item)
                self.parse_agency_service(item)
                self.parse_url(item)
                self.parse_aka(item)
                self.parse_resource_info(item)
                self.parse_contact(item)      
                self.parse_email(item)      
                self.parse_phone(item)      
                self.parse_site(item)
                      
                
    def parse_person(self, element):
        ''' Element paths '''
        xpPerson = 'hmis:Person'
        xpPersonIDNum = 'hmis:PersonID/hmis:IDNum'
        xpPersonIDStr = 'hmis:PersonID/hmis:IDStr'
        xpPersonDeleteOccurredDate = 'hmis:PersonID/@hmis:DeleteOccurredDate'
        xpPersonDeleteEffective = 'hmis:PersonID/@hmis:DeleteEffective'
        xpPersonDelete = 'hmis:PersonID/@hmis:Delete'
        xpPersonDateOfBirthHashed = 'hmis:DateOfBirth/hmis:Hashed'
        xpPersonDateOfBirthHashedDeleteOccurredDate = 'hmis:DateOfBirth/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonDateOfBirthHashedDeleteEffective = 'hmis:DateOfBirth/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonDateOfBirthHashedDelete = 'hmis:DateOfBirth/hmis:Hashed/@hmis:Delete'
        xpPersonDateOfBirthUnhashed = 'hmis:DateOfBirth/hmis:Unhashed'
        xpPersonDateOfBirthUnhashedDeleteOccurredDate = 'hmis:DateOfBirth/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonDateOfBirthUnhashedDeleteEffective = 'hmis:DateOfBirth/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonDateOfBirthUnhashedDelete = 'hmis:DateOfBirth/hmis:Unhashed/@hmis:Delete'
        xpPersonEthnicityHashed = 'hmis:Ethnicity/hmis:Hashed'
        xpPersonEthnicityHashedDeleteOccurredDate = 'hmis:Ethnicity/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonEthnicityHashedDeleteEffective = 'hmis:Ethnicity/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonEthnicityHashedDelete = 'hmis:Ethnicity/hmis:Hashed/@hmis:Delete'
        xpPersonEthnicityUnhashed = 'hmis:Ethnicity/hmis:Unhashed'
        xpPersonEthnicityUnhashedDeleteOccurredDate = 'hmis:Ethnicity/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonEthnicityUnhashedDeleteEffective = 'hmis:Ethnicity/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonEthnicityUnhashedDelete = 'hmis:Ethnicity/hmis:Unhashed/@hmis:Delete'
        xpPersonGenderHashed = 'hmis:Gender/hmis:Hashed'
        xpPersonGenderHashedDeleteOccurredDate = 'hmis:Gender/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonGenderHashedDeleteEffective = 'hmis:Gender/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonGenderHashedDelete = 'hmis:Gender/hmis:Hashed/@hmis:Delete'
        xpPersonGenderUnhashed = 'hmis:Gender/hmis:Unhashed'
        xpPersonGenderUnhashedDeleteOccurredDate = 'hmis:Gender/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonGenderUnhashedDeleteEffective = 'hmis:Gender/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonGenderUnhashedDelete = 'hmis:Gender/hmis:Unhashed/@hmis:Delete'
        xpPersonLegalFirstNameHashed = 'hmis:LegalFirstName/hmis:Hashed'
        xpPersonLegalFirstNameHashedDeleteOccurredDate = 'hmis:LegalFirstName/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonLegalFirstNameHashedDeleteEffective = 'hmis:LegalFirstName/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonLegalFirstNameHashedDelete = 'hmis:LegalFirstName/hmis:Hashed/@hmis:Delete'
        xpPersonLegalFirstNameUnhashed = 'hmis:LegalFirstName/hmis:Unhashed'
        xpPersonLegalFirstNameUnhashedDeleteOccurredDate = 'hmis:LegalFirstName/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonLegalFirstNameUnhashedDeleteEffective = 'hmis:LegalFirstName/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonLegalFirstNameUnhashedDelete = 'hmis:LegalFirstName/hmis:Unhashed/@hmis:Delete'
        xpPersonLegalLastNameHashed = 'hmis:LegalLastName/hmis:Hashed'
        xpPersonLegalLastNameHashedDeleteOccurredDate = 'hmis:LegalLastName/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonLegalLastNameHashedDeleteEffective = 'hmis:LegalLastName/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonLegalLastNameHashedDelete = 'hmis:LegalLastName/hmis:Hashed/@hmis:Delete'
        xpPersonLegalLastNameUnhashed = 'hmis:LegalLastName/hmis:Unhashed'
        xpPersonLegalLastNameUnhashedDeleteOccurredDate = 'hmis:LegalLastName/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonLegalLastNameUnhashedDeleteEffective = 'hmis:LegalLastName/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonLegalLastNameUnhashedDelete = 'hmis:LegalLastName/hmis:Unhashed/@hmis:Delete'
        xpPersonLegalMiddleNameHashed = 'hmis:LegalMiddleName/hmis:Hashed'
        xpPersonLegalMiddleNameHashedDeleteOccurredDate = 'hmis:LegalMiddleName/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonLegalMiddleNameHashedDeleteEffective = 'hmis:LegalMiddleName/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonLegalMiddleNameHashedDelete = 'hmis:LegalMiddleName/hmis:Hashed/@hmis:Delete'
        xpPersonLegalMiddleNameUnhashed = 'hmis:LegalMiddleName/hmis:Unhashed'
        xpPersonLegalMiddleNameUnhashedDeleteOccurredDate = 'hmis:LegalMiddleName/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonLegalMiddleNameUnhashedDeleteEffective = 'hmis:LegalMiddleName/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonLegalMiddleNameUnhashedDelete = 'hmis:LegalMiddleName/hmis:Unhashed/@hmis:Delete'
        xpPersonLegalSuffixHashed = 'hmis:LegalSuffix/hmis:Hashed'
        xpPersonLegalSuffixHashedDeleteOccurredDate = 'hmis:LegalSuffix/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonLegalSuffixHashedDeleteEffective = 'hmis:LegalSuffix/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonLegalSuffixHashedDelete = 'hmis:LegalSuffix/hmis:Hashed/@hmis:Delete'
        xpPersonLegalSuffixUnhashed = 'hmis:LegalSuffix/hmis:Unhashed'
        xpPersonLegalSuffixUnhashedDeleteOccurredDate = 'hmis:LegalSuffix/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonLegalSuffixUnhashedDeleteEffective = 'hmis:LegalSuffix/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonLegalSuffixUnhashedDelete = 'hmis:LegalSuffix/hmis:Unhashed/@hmis:Delete'
        xpPersonSocialSecurityNumberHashed = 'hmis:SocialSecurityNumber/hmis:Hashed'
        xpPersonSocialSecurityNumberHashedDeleteOccurredDate = 'hmis:SocialSecurityNumber/hmis:Hashed/@hmis:DeleteOccurredDate'
        xpPersonSocialSecurityNumberHashedDeleteEffective = 'hmis:SocialSecurityNumber/hmis:Hashed/@hmis:DeleteEffective'
        xpPersonSocialSecurityNumberHashedDelete = 'hmis:SocialSecurityNumber/hmis:Hashed/@hmis:Delete'
        xpPersonSocialSecurityNumberUnhashed = 'hmis:SocialSecurityNumber/hmis:Unhashed'
        xpPersonSocialSecurityNumberUnhashedDeleteOccurredDate = 'hmis:SocialSecurityNumber/hmis:Unhashed/@hmis:DeleteOccurredDate'
        xpPersonSocialSecurityNumberUnhashedDeleteEffective = 'hmis:SocialSecurityNumber/hmis:Unhashed/@hmis:DeleteEffective'
        xpPersonSocialSecurityNumberUnhashedDelete = 'hmis:SocialSecurityNumber/hmis:Unhashed/@hmis:Delete'
        xpPersonSocialSecNumberQualityCode = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode'
        xpPersonSocialSecNumberQualityCodeDeleteOccurredDate = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode/@hmis:DeleteOccurredDate'
        xpPersonSocialSecNumberQualityCodeDeleteEffective = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode/@hmis:DeleteEffective'
        xpPersonSocialSecNumberQualityCodeDelete = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode/@hmis:Delete'

        itemElements = element.xpath(xpPerson, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                self.existence_test_and_add('person_id_id_num', item.xpath(xpPersonIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('person_id_id_str', item.xpath(xpPersonIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('date_of_birth_unhashed', item.xpath(xpPersonDateOfBirthUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('date_of_birth_hashed', item.xpath(xpPersonDateOfBirthHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('ethnicity_unhashed', item.xpath(xpPersonEthnicityUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('ethnicity_hashed', item.xpath(xpPersonEthnicityHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('gender_unhashed', item.xpath(xpPersonGenderUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('gender_hashed', item.xpath(xpPersonGenderHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_first_name_unhashed', item.xpath(xpPersonLegalFirstNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_first_name_hashed', item.xpath(xpPersonLegalFirstNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_last_name_unhashed', item.xpath(xpPersonLegalLastNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_last_name_hashed', item.xpath(xpPersonLegalLastNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_middle_name_unhashed', item.xpath(xpPersonLegalMiddleNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_middle_name_hashed', item.xpath(xpPersonLegalMiddleNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_suffix_unhashed', item.xpath(xpPersonLegalSuffixUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('legal_suffix_hashed', item.xpath(xpPersonLegalSuffixHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('social_security_number_unhashed', item.xpath(xpPersonSocialSecurityNumberUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('social_security_number_hashed', item.xpath(xpPersonSocialSecurityNumberHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('social_security_number_quality_code', item.xpath(xpPersonSocialSecNumberQualityCode, namespaces={'hmis': self.hmis_namespace}), 'text')

                ''' Foreign Keys '''
                self.existence_test_and_add('export_id', self.export_id, 'text')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Person)
    
                ''' Parse sub-tables '''
                self.parse_site_service_participation(item)
                self.parse_need(item)          
                self.parse_service_event(item)
                self.parse_person_historical(item)
                self.parse_release_of_information(item)
                self.parse_other_names(item)
                self.parse_races(item)

    def parse_service(self, element):
        ''' Element paths '''
        xpService = 'hmis:Service'
        xpServiceDeleteOccurredDate = '@hmis:DeleteOccurredDate'
        xpServiceDeleteEffective = '@hmis:DeleteEffective'
        xpServiceDelete = '@hmis:Delete'
        xpAirsKey = 'airs:Key'
        xpAirsAgencyKey = 'airs:AgencyKey'
        xpAirsName = 'airs:Name'
        xpCOCCode = 'hmis:COCCode'
        xpConfiguration = 'hmis:Configuration'
        xpDirectServiceCode = 'hmis:DirectServiceCode'
        xpGranteeIdentifier = 'hmis:GranteeIdentifier'
        xpIndividualFamilyCode = 'hmis:IndividualFamilyCode'
        xpResidentialTrackingMethod = 'hmis:ResidentialTrackingMethod'
        xpServiceType = 'hmis:ServiceType'
        xpServiceEffectivePeriodStartDate = 'hmis:ServiceEffectivePeriod/hmis:StartDate'
        xpServiceEffectivePeriodEndDate = 'hmis:ServiceEffectivePeriod/hmis:EndDate'
        xpServiceRecordedDate = 'hmis:ServiceRecordedDate'
        xpTargetPopulationA = 'hmis:TargetPopulationA'
        xpTargetPopulationB = 'hmis:TargetPopulationB'

        itemElements = element.xpath(xpService, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                self.existence_test_and_add('residential_tracking_method', item.xpath(xpResidentialTrackingMethod, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('household_id_num_date_collected', item.xpath(xpServiceType, namespaces={'hmis': self.hmis_namespace}), 'text')

                ''' Foreign Keys '''
                self.existence_test_and_add('export_id', self.export_id, 'text')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Service)
    
                ''' Parse sub-tables '''
                self.parse_funding_source(item)
                self.parse_inventory(item)      

    def parse_site(self, element):
        ''' Element paths '''
        xpSite = 'airs:Site'
        xpSiteDeleteOccurredDate = '@airs:DeleteOccurredDate'
        xpSiteDeleteEffective = '@airs:DeleteEffective'
        xpSiteDelete = '@airs:Delete'
        xpKey = 'airs:Key'
        xpName = 'airs:Name'
        xpSiteDescription = 'airs:SiteDescription'
        xpPhysicalAddressPreAddressLine = 'airs:PhysicalAddress/airs:PreAddressLine'
        xpPhysicalAddressLine1 = 'airs:PhysicalAddress/airs:Line1'
        xpPhysicalAddressLine2 = 'airs:PhysicalAddress/airs:Line2'
        xpPhysicalAddressCity = 'airs:PhysicalAddress/airs:City'
        xpPhysicalAddressCounty = 'airs:PhysicalAddress/airs:County'
        xpPhysicalAddressState = 'airs:PhysicalAddress/airs:State'
        xpPhysicalAddressZipCode = 'airs:PhysicalAddress/airs:ZipCode'
        xpPhysicalAddressCountry = 'airs:PhysicalAddress/airs:Country'
        xpPhysicalAddressReasonWithheld = 'airs:PhysicalAddress/airs:ReasonWithheld'
        xpPhysicalAddressConfidential = 'airs:PhysicalAddress/@airs:Confidential'
        xpPhysicalAddressDescription = 'airs:PhysicalAddress/@airs:Description' 
        xpMailingAddressPreAddressLine = 'airs:MailingAddress/airs:PreAddressLine'
        xpMailingAddressLine1 = 'airs:MailingAddress/airs:Line1'
        xpMailingAddressLine2 = 'airs:MailingAddress/airs:Line2'
        xpMailingAddressCity = 'airs:MailingAddress/airs:City'
        xpMailingAddressCounty = 'airs:MailingAddress/airs:County'
        xpMailingAddressState = 'airs:MailingAddress/airs:State'
        xpMailingAddressZipCode = 'airs:MailingAddress/airs:ZipCode'
        xpMailingAddressCountry = 'airs:MailingAddress/airs:Country'
        xpMailingAddressReasonWithheld = 'airs:MailingAddress/airs:ReasonWithheld'
        xpMailingAddressConfidential = 'airs:MailingAddress/@airs:Confidential'
        xpMailingAddressDescription = 'airs:MailingAddress/@airs:Description'       
        xpNoPhysicalAddressDescription = 'airs:NoPhysicalAddress/airs:Description'        
        xpNoPhysicalAddressExplanation = 'airs:NoPhysicalAddress/airs:Explanation'        
        xpDisabilitiesAccess = 'airs:DisabilitiesAccess'
        xpPhysicalLocationDescription = 'airs:PhysicalLocationDescription'
        xpBusServiceAccess = 'airs:BusServiceAccess'
        xpPublicAccessToTransportation = 'airs:PublicAccessToTransportation'
        xpYearInc = 'airs:YearInc'
        xpAnnualBudgetTotal = 'airs:AnnualBudgetTotal'
        xpLegalStatus = 'airs:LegalStatus'
        xpExcludeFromWebsite = 'airs:ExcludeFromWebsite'
        xpExcludeFromDirectory = 'airs:ExcludeFromDirectory'
        xpAgencyKey = 'airs:AgencyKey'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('export_id', self.export_id, 'text')
                except: pass
                try: self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                except: pass
                    
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Site)
    
                ''' Parse sub-tables '''
                self.parse_url(item)
                self.parse_spatial_location(item)
                self.parse_other_address(item)
                self.parse_cross_street(item)
                self.parse_aka(item)
                self.parse_site_service(item)
                self.parse_languages(item)
                self.parse_time_open(item)            
                self.parse_inventory(item)
                self.parse_contact(item)            
                self.parse_email(item)      
                self.parse_phone(item)      
                
    def parse_site_service(self, element):
        ''' Element paths '''
        xpSiteService = 'hmis:SiteService'
        xpSiteServiceDeleteOccurredDate = '@airs:DeleteOccurredDate'
        xpSiteServiceDeleteEffective = '@airs:DeleteEffective'
        xpSiteServiceDelete = '@airs:Delete'
        xpName = 'airs:Name'
        xpKey = 'airs:Key'
        xpDescription = 'airs:Description'
        xpFeeStructure = 'airs:FeeStructure'
        xpGenderRequirements = 'airs:GenderRequirements'
        xpAreaFlexibility = 'airs:AreaFlexibility'
        xpServiceNotAlwaysAvailable = 'airs:ServiceNotAlwaysAvailable'
        xpServiceGroupKey = 'airs:ServiceGroupKey'
        xpServiceID = 'airs:ServiceID'
        xpSiteID = 'airs:SiteID'
        xpGeographicCode = 'airs:GeographicCode'
        xpGeographicCodeDateCollected = 'hmis:GeographicCode/@hmis:dateCollected'
        xpGeographicCodeDateEffective = 'hmis:GeographicCode/@hmis:dateEffective'
        xpGeographicCodeDataCollectionStage = 'hmis:GeographicCode/@hmis:dataCollectionStage'
        xpHousingType = 'airs:HousingType'
        xpHousingTypeDateCollected = 'hmis:HousingType/@hmis:dateCollected'
        xpHousingTypeDateEffective = 'hmis:HousingType/@hmis:dateEffective'
        xpHousingTypeDataCollectionStage = 'hmis:HousingType/@hmis:dataCollectionStage'
        xpPrincipal = 'airs:Principal'
        xpSiteServiceEffectivePeriodStartDate = 'airs:SiteServiceEffectivePeriod/hmis:StartDate'
        xpSiteServiceEffectivePeriodEndDate = 'airs:SiteServiceEffectivePeriod/hmis:EndDate'
        xpSiteServiceRecordedDate = 'airs:SiteServiceRecordedDate'
        xpSiteServiceType = 'airs:SiteServiceType'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('export_id', self.export_id, 'text')
                except: pass
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.SiteService)
    
                ''' Parse sub-tables '''
                self.parse_seasonal(item)
                self.parse_residency_requirements(item)
                self.parse_pit_count_set(item)
                self.parse_other_requirements(item)
                self.parse_languages(item)
                self.parse_time_open(item)            
                self.parse_inventory(item)
                self.parse_income_requirements(item)
                self.parse_hmis_asset(item)
                self.parse_geographic_area_served(item)
                self.parse_documents_required(item)
                self.parse_aid_requirements(item)
                self.parse_age_requirements(item)
                self.parse_application_process(item)
                self.parse_taxonomy(item)
                self.parse_family_requirements(item)
                self.parse_resource_info(item)
                
    def parse_service_group(self, element):
        ''' Element paths '''
        xpServiceGroup = 'airs:ServiceGroup'
        xpAirsKey = 'airs:Key'
        xpAirsName = 'airs:Name'
        xpAirsAgencyKey = 'airs:ProgramName'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ServiceGroup)
    
                ''' Parse sub-tables '''

    def parse_license_accreditation(self, element):
        ''' Element paths '''
        xpLicenseAccreditation = 'airs:LicenseAccreditation'
        xpLicense = 'airs:License'
        xpLicensedBy = 'airs:LicensedBy'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.LicenseAccreditation)
    
                ''' Parse sub-tables '''
                            

    def parse_agency_service(self, element):
        ''' Element paths '''
        xpAgencyService = 'airs:AgencyService'
        xpAirsKey = 'airs:Key'
        xpAgencyKey = 'airs:AgencyKey'
        xpAgencyName = 'airs:Name'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.AgencyService)
    
                ''' Parse sub-tables '''
                            

    def parse_url(self, element):
        ''' Element paths '''
        xpUrl = 'airs:URL'
        xpAddress = 'airs:Address'
        xpNote = 'airs:Note'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Url)
    
                ''' Parse sub-tables '''
                            

    def parse_spatial_location(self, element):
        ''' Element paths '''
        xpSpatialLocation = 'airs:SpatialLocation'
        xpDescription = 'airs:Description'
        xpDatum = 'airs:Datum'
        xpLatitude = 'airs:Latitude'
        xpLongitude = 'airs:Longitude'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.SpatialLocation)
    
                ''' Parse sub-tables '''
                            

    def parse_other_address(self, element):
        ''' Element paths '''
        xpOtherAddress = 'airs:OtherAddress'
        xpPreAddressLine = 'airs:PreAddressLine'
        xpLine1 = 'airs:Line1'
        xpLine2 = 'airs:Line2'
        xpCity = 'airs:City'
        xpCounty = 'airs:County'
        xpState = 'airs:State'
        xpZipCode = 'airs:ZipCode'
        xpCountry = 'airs:Country'
        xpReasonWithheld = 'airs:ReasonWithheld'
        xpConfidential = '@airs:Confidential'
        xpDescription = '@airs:Description'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.OtherAddress)
    
                ''' Parse sub-tables '''
                            

    def parse_cross_street(self, element):
        ''' Element paths '''
        xpCrossStreet = 'airs:CrossStreet'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.CrossStreet)
    
                ''' Parse sub-tables '''
                            

    def parse_aka(self, element):
        ''' Element paths '''
        xpAka = 'airs:AKA'
        xpName = 'airs:Name'
        xpConfidential = 'airs:Confidential'
        xpDescription = 'airs:Description'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Aka)
    
                ''' Parse sub-tables '''
                            

    def parse_seasonal(self, element):
        ''' Element paths '''
        xpSeasonal = 'airs:Seasonal'
        xpDescription = 'airs:Description'
        xpStartDate = 'airs:StartDate'
        xpEndDate = 'airs:EndDate'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Seasonal)
    
                ''' Parse sub-tables '''
                            

    def parse_residency_requirements(self, element):
        ''' Element paths '''
        xpResidencyRequirements = 'airs:ResidencyRequirements'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ResidencyRequirements)
    
                ''' Parse sub-tables '''
                            

    def parse_pit_count_set(self, element):
        ''' Element paths '''
        xpPitCountSet = 'hmis:PITCountSet'
        xpPitCountSetIDNum = 'hmis:PitCountSetID/hmis:IDNum'
        xpPitCountSetIDStr = 'hmis:PitCountSetID/hmis:IDStr'
        xpPitCountSetIDDeleteOccurredDate = 'hmis:PitCountSetID/@hmis:deleteOccurredDate'
        xpPitCountSetIDDeleteEffective = 'hmis:PitCountSetID/@hmis:deleteEffective'
        xpPitCountSetIDDelete = 'hmis:PitCountSetID/@hmis:delete'
        xpHUDWaiverReceived = 'hmis:HUDWaiverReceived'
        xpHUDWaiverDate = 'hmis:HUDWaiverDate'
        xpHUDWaiverEffectivePeriodStartDate = 'hmis:HUDWaiverEffectivePeriod/hmis:StartDate'
        xpHUDWaiverEffectivePeriodEndDate = 'hmis:HUDWaiverEffectivePeriod/hmis:EndDate'
        xpLastPITShelteredCountDate = 'hmis:LastPITShelteredCountDate'
        xpLastPITUnshelteredCountDate = 'hmis:LastPITUnshelteredCountDate'
        
        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.PitCountSet)
    
                ''' Parse sub-tables '''
                self.parse_pit_counts(item)            

    def parse_pit_counts(self, element):
        ''' Element paths '''
        xpPITCountValue = 'hmis:PITCountValue'
        XpPITCountEffectivePeriodStartDate = 'hmis:PITCountEffectivePeriod/hmis:StartDate'
        XpPITCountEffectivePeriodEndDate = 'hmis:PITCountEffectivePeriod/hmis:EndDate'
        xpPITCountRecordedDate = 'hmis:PITCountRecordedDate'
        xpPITHouseholdType = 'hmis:pITHouseholdType'
        
        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('pit_count_set_index_id', self.pit_count_set_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.PitCounts)
    
                ''' Parse sub-tables '''
                            

    def parse_other_requirements(self, element):
        ''' Element paths '''
        xpOtherRequirements = 'airs:OtherRequirements'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.OtherRequirements)
    
                ''' Parse sub-tables '''
                            

    def parse_languages(self, element):
        ''' Element paths '''
        xpLanguages = 'airs:Languages'
        xpName = 'airs:Name'
        xpNotes = 'airs:Notes'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Languages)
    
                ''' Parse sub-tables '''
                self.parse_time_open(item)            

    def parse_time_open(self, element):
        ''' Unique method that has 2nd loop for each day of week '''

        ''' Element paths '''
        xpTimeOpen = 'airs:TimeOpen'
        xpNotes = 'airs:Notes'
        
        itemElements = element.xpath(xpTimeOpen, namespaces={'airs': self.airs_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}

                self.existence_test_and_add('notes', item.xpath(xpNotes, namespaces={'airs': self.airs_namespace}), 'text')

                ''' Foreign Keys '''
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('languages_index_id', self.languages_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.TimeOpen)

                ''' parse each specific day of week '''
                weekDays = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
                for day in weekDays:
                    self.parse_time_open_day(item, day)

    def parse_time_open_day(self, element, day):
        ''' Unique method -- Loop each day of the week '''

        ''' Element Paths '''
        xpFrom = 'airs:From'
        xpTo = 'airs:To'
        xpDay = 'airs:%s' % (day)
        
        itemElements = element.xpath(xpDay, namespaces={'airs': self.airs_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}

                ''' Map elements to database columns '''
                self.existence_test_and_add('from', item.xpath(xpFrom, namespaces={'airs': self.airs_namespace}), 'text')
                self.existence_test_and_add('to', item.xpath(xpTo, namespaces={'airs': self.airs_namespace}), 'text')
                self.existence_test_and_add('day_of_week', day, 'text')

                ''' Foreign Keys '''
                self.existence_test_and_add('time_open_index_id', self.time_open_index_id, 'no_handling')

                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.TimeOpenDays)

    def parse_inventory(self, element):
        ''' Element paths '''
        xpInventory = 'hmis:Inventory'
        xpInventoryDeleteOccurredDate = '@hmis:deleteOccurredDate'
        xpInventoryDeleteEffective = '@hmis:deleteEffective'
        xpInventoryDelete = '@hmis:delete'
        xpHMISParticipationPeriodStartDate = 'hmis:HMISParticipationPeriod/hmis:StartDate'
        xpHMISParticipationPeriodEndDate = 'hmis:HMISParticipationPeriod/hmis:EndDate'
        xpInventoryIDIDNum = 'hmis:InventoryID/hmis:IDNum'
        xpInventoryIDIDStr = 'hmis:InventoryID/hmis:IDStr'
        xpBedInventory = 'hmis:BedInventory'
        xpBedAvailability = '@hmis:BedAvailability'
        xpBedType = '@hmis:BedType'
        xpBedIndividualFamilyType = '@hmis:BedIndividualFamilyType'
        xpChronicHomelessBed = '@hmis:ChronicHomelessBed'
        xpDomesticViolenceShelterBed = '@hmis:DomesticViolenceShelterBed'
        xpHouseholdType = '@hmis:HouseholdType'
        xpHMISParticipatingBeds = 'hmis:HMISParticipatingBeds'
        xpInventoryEffectivePeriodStartDate = 'hmis:InventoryEffectivePeriod/hmis:StartDate'
        xpInventoryEffectivePeriodEndDate = 'hmis:InventoryEffectivePeriod/hmis:EndDate'
        xpInventoryRecordedDate = 'hmis:InventoryRecordedDate'
        xpUnitInventory = 'hmis:UnitInventory'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('service_index_id', self.service_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Inventory)
    
                ''' Parse sub-tables '''
                            

    def parse_income_requirements(self, element):
        ''' Element paths '''
        xpIncomeRequirements = 'airs:IncomeRequirements'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.IncomeRequirements)
    
                ''' Parse sub-tables '''
                            

    def parse_hmis_asset(self, element):
        ''' Element paths '''
        xpHMISAsset = 'hmis:HMISAsset'
        xpAssetIDIDNum = 'hmis:AssetID/hmis:IDNum'
        xpAssetIDIDStr = 'hmis:AssetID/hmis:IDStr'
        xpAssetIDDelete = 'hmis:AssetID/@hmis:delete'
        xpAssetIDDeleteOccurredDate = 'hmis:AssetID/@hmis:deleteOccurredDate'
        xpAssetIDDeleteEffective = 'hmis:AssetID/@hmis:deleteEffective'
        xpAssetCount = 'hmis:AssetCount'
        xpAssetCountBedAvailability = 'hmis:AssetCount/@hmis:bedAvailability'
        xpAssetCountBedType = 'hmis:AssetCount/@hmis:bedType'
        xpAssetCountBedIndividualFamilyType = 'hmis:AssetCount/@hmis:bedIndividualFamilyType'
        xpAssetCountChronicHomelessBed = 'hmis:AssetCount/@hmis:chronicHomelessBed'
        xpAssetCountDomesticViolenceShelterBed = 'hmis:AssetCount/@hmis:domesticViolenceShelterBed'
        xpAssetCountHouseholdType = 'hmis:AssetCount/@hmis:householdType'
        xpAssetType = 'hmis:AssetType'
        xpAssetEffectivePeriodStartDate = 'hmis:AssetEffectivePeriod/hmis:StartDate'
        xpAssetEffectivePeriodEndDate = 'hmis:AssetEffectivePeriod/hmis:EndDate'
        xpAssetRecordedDate = 'hmis:RecordedDate'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.HmisAsset)
    
                ''' Parse sub-tables '''
                self.parse_assignment(item)            

    def parse_assignment(self, element):
        ''' Element paths '''
        xpAssignment = 'hmis:Assignment'
        xpAssignmentIDIDNum = 'hmis:AssignmentID/hmis:IDNum'
        xpAssignmentIDIDStr = 'hmis:AssignmentID/hmis:IDStr'
        xpAssignmentIDDelete = 'hmis:AssignmentID/@hmis:delete'
        xpAssignmentIDDeleteOccurredDate = 'hmis:AssignmentID/@hmis:deleteOccurredDate'
        xpAssignmentIDDeleteEffective = 'hmis:AssignmentID/@hmis:deleteEffective'
        xpPersonIDIDNum = 'hmis:PersonID/hmis:IDNum'
        xpPersonIDIDStr = 'hmis:PersonID/hmis:IDStr'
        xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
        xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('hmis_asset_index_id', self.hmis_asset_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Assignment)
    
                ''' Parse sub-tables '''
                self.parse_assignment_period(item)            

    def parse_assignment_period(self, element):
        ''' Element paths '''
        xpAssignmentPeriod = 'hmis:AssignmentPeriod'
        xpAssignmentPeriodStartDate = 'hmis:StartDate'
        xpAssignmentPeriodEndDate = 'hmis:EndDate'
        
        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('assignment_index_id', self.assignment_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.AssignmentPeriod)
    
                ''' Parse sub-tables '''
                            

    def parse_geographic_area_served(self, element):
        ''' Element paths '''
        xpGeographicAreaServed = 'airs:GeographicAreaServed'
        xpZipCode = 'airs:ZipCode'
        xpCensusTrack = 'airs:CensusTrack'
        xpCity = 'airs:City'
        xpCounty = 'airs:County'
        xpState = 'airs:State'
        xpCountry = 'airs:Country'
        xpDescription = 'airs:Description'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.GeographicAreaServed)
    
                ''' Parse sub-tables '''
                            

    def parse_documents_required(self, element):
        ''' Element paths '''
        xpDocumentsRequired = 'airs:DocumentsRequired'
        xpDescription = 'airs:Description'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.DocumentsRequired)
    
                ''' Parse sub-tables '''
                            

    def parse_aid_requirements(self, element):
        ''' Element paths '''
        xpAidRequirements = 'airs:AidRequirements'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.AidRequirements)
    
                ''' Parse sub-tables '''
                            

    def parse_age_requirements(self, element):
        ''' Element paths '''
        xpAgeRequirements = 'airs:AgeRequirements'
        xpGender = '@airs:Gender'
        xpMinimumAge = '@airs:MinimumAge'
        xpMaximumAge = '@airs:MaximumAge'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.AgeRequirements)
    
                ''' Parse sub-tables '''
                            

    def parse_site_service_participation(self, element):
        ''' Element paths '''
            xpSiteServiceParticipation = 'hmis:SiteServiceParticipation'
            xpSiteServiceParticipationIDIDNum = 'hmis:SiteServiceParticipationID/hmis:IDNum'
            xpSiteServiceParticipationIDIDStr = 'hmis:SiteServiceParticipationID/hmis:IDStr'
            xpSiteServiceParticipationIDDeleteOccurredDate = 'hmis:SiteServiceParticipationID/@hmis:deleteOccurredDate'
            xpSiteServiceParticipationIDDeleteEffective = 'hmis:SiteServiceParticipationID/@hmis:deleteEffective'
            xpSiteServiceParticipationIDDelete = 'hmis:SiteServiceParticipationID/@hmis:delete'            
            xpSiteServiceID = 'hmis:SiteServiceID'
            xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
            xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'
            xpStartDate = 'hmis:ParticipationDates/hmis:StartDate'
            xpEndDate = 'hmis:ParticipationDates/hmis:EndDate'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.SiteServiceParticipation)
    
                ''' Parse sub-tables '''
                self.parse_reasons_for_leaving(item)  
                self.parse_need(item)          
                self.parse_service_event(item)
                self.parse_person_historical(item)

    def parse_reasons_for_leaving(self, element):
        ''' Element paths '''
        xpReasonsForLeaving = 'hmis:ReasonsForLeaving'
        xpReasonsForLeavingIDIDNum = 'hmis:ReasonsForLeavingID/hmis:IDNum'
        xpReasonsForLeavingIDIDStr = 'hmis:ReasonsForLeavingID/hmis:IDStr'
        xpReasonsForLeavingIDDelete = 'hmis:ReasonsForLeavingID/@hmis:delete'
        xpReasonsForLeavingIDDeleteOccurredDate = 'hmis:ReasonsForLeavingID/@hmis:deleteOccurredDate'
        xpReasonsForLeavingIDDeleteEffective = 'hmis:ReasonsForLeavingID/@hmis:deleteEffective'
        xpReasonsForLeaving = 'hmis:ReasonsForLeaving'
        xpReasonsForLeavingDateCollected = 'hmis:ReasonsForLeaving/@hmis:dateCollected'
        xpReasonsForLeavingDateEffective = 'hmis:ReasonsForLeaving/@hmis:dateEffective'
        xpReasonsForLeavingDataCollectionStage = 'hmis:ReasonsForLeaving/@hmis:dataCollectionStage'
        xpReasonsForLeavingOther = 'hmis:ReasonsForLeavingOther'
        xpReasonsForLeavingOtherDateCollected = 'hmis:ReasonsForLeavingOther/@hmis:dateCollected'
        xpReasonsForLeavingOtherDateEffective = 'hmis:ReasonsForLeavingOther/@hmis:dateEffective'
        xpReasonsForLeavingOtherDataCollectionStage = 'hmis:ReasonsForLeavingOther/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_participation_index_id', self.site_service_participation_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ReasonsForLeaving)
    
                ''' Parse sub-tables '''
                            

    def parse_application_process(self, element):
        ''' Element paths '''
        xpApplicationProcess = 'airs:ApplicationProcess'
        xpStep = 'airs:Step'
        xpDescription = 'airs:Description'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ApplicationProcess)
    
                ''' Parse sub-tables '''
                            

    def parse_need(self, element):
        ''' Element paths '''
        xpNeed = 'hmis:Need'
        xpNeedIDIDNum = 'hmis:NeedID/hmis:IDNum'
        xpNeedIDIDStr = 'hmis:NeedID/hmis:IDStr'
        xpNeedIDDeleteOccurredDate = 'hmis:NeedID/@hmis:deleteOccurredDate'
        xpNeedIDDeleteEffective = 'hmis:NeedID/@hmis:deleteEffective'
        xpNeedIDDelete = 'hmis:NeedID/@hmis:delete'
        xpSiteServiceID = 'hmis:SiteServiceID'
        xpNeedEffectivePeriodStartDate = 'hmis:NeedEffectivePeriod/hmis:StartDate'
        xpNeedEffectivePeriodEndDate = 'hmis:NeedEffectivePeriod/hmis:EndDate'
        xpNeedRecordedDate = 'hmis:NeedRecordedDate'
        xpNeedStatus = 'hmis:NeedStatus'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_service_participation_index_id', self.site_service_participation_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Need)
    
                ''' Parse sub-tables '''
                self.parse_taxonomy(item)
                self.parse_service_event(item)

    def parse_taxonomy(self, element):
        ''' Element paths '''
        xpTaxonomy = 'airs:Taxonomy'
        xpCode = 'airs:Code'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('need_index_id', self.need_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Taxonomy)
    
                ''' Parse sub-tables '''
                            

    def parse_service_event(self, element):
        ''' Element paths '''
        xpServiceEvent = 'hmis:ServiceEvent'
        xpServiceEventIDIDNum = 'hmis:ServiceEventID/hmis:IDNum'
        xpServiceEventIDIDStr = 'hmis:ServiceEventID/hmis:IDStr'
        xpServiceEventIDDeleteOccurredDate = 'hmis:ServiceEventID/@hmis:deleteOccurredDate'
        xpServiceEventIDDeleteEffective = 'hmis:ServiceEventID/@hmis:deleteEffective'
        xpServiceEventIDDelete = 'hmis:ServiceEventID/@hmis:delete'        
        xpSiteServiceID = 'hmis:SiteServiceID'
        xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
        xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'
        xpIsReferral = 'hmis:IsReferral'
        xpQuantityOfServiceEvent = 'hmis:QuantityOfServiceEvent'
        xpQuantityOfServiceEventUnit = 'hmis:QuantityOfServiceEventUnit'
        xpServiceEventAIRSCode = 'hmis:ServiceEventAIRSCode'
        xpServiceEventEffectivePeriodStartDate = 'hmis:ServiceEventEffectivePeriod/hmis:StartDate'
        xpServiceEventEffectivePeriodEndDate = 'hmis:ServiceEventEffectivePeriod/hmis:EndDate'
        xpServiceEventProvisionDate = 'hmis:ServiceEventProvisionDate'
        xpServiceEventRecordedDate = 'hmis:ServiceEventRecordedDate'
        xpServiceEventIndFam = 'hmis:ServiceEventIndFam'
        xpHMISServiceEventCodeTypeOfService = 'hmis:HMISServiceEventCode/hmis:TypeOfService'
        xpHMISServiceEventCodeTypeOfServiceOther = 'hmis:HMISServiceEventCode/hmis:TypeOfServiceOther'
        xpHPRPFinancialAssistanceServiceEventCode = 'hmis:HPRPFinancialAssistanceService'
        xpHPRPRelocationStabilizationServiceEventCode = 'hmis:HPRPRelocationStabilizationServiceEventCode'
        
        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('need_index_id', self.need_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_service_participation_index_id', self.site_service_participation_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ServiceEvent)
    
                ''' Parse sub-tables '''
                self.parse_service_event_notes(item)     
                self.parse_funding_source(item)       

    def parse_service_event_notes(self, element):
        ''' Element paths '''
        xpServiceEventNotes = 'hmis:ServiceEventNotes/hmis:note'
        xpNoteIDIDNum = 'hmis:NoteID/hmis:IDNum'
        xpNoteIDIDStr = 'hmis:NoteID/hmis:IDStr'
        xpNoteIDDeleteOccurredDate = 'hmis:NoteID/@hmis:deleteOccurredDate'
        xpNoteIDDeleteEffective = 'hmis:NoteID/@hmis:deleteEffective'
        xpNoteIDDelete = 'hmis:NoteID/@hmis:delete'             
        xpNoteText = 'hmis:NoteText'
        xpNoteTextDateCollected = 'hmis:NoteText/@hmis:dateCollected'
        xpNoteTextDateEffective = 'hmis:NoteText/@hmis:dateEffective'
        xpNoteTextDataCollectionStage = 'hmis:NoteText/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('service_event_index_id', self.service_event_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ServiceEventNotes)
    
                ''' Parse sub-tables '''
                            

    def parse_family_requirements(self, element):
        ''' Element paths '''
        xpFamilyRequirements = 'airs:FamilyRequirements'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.FamilyRequirements)
    
                ''' Parse sub-tables '''
                            

    def parse_person_historical(self, element):
        ''' Element paths '''
        xpPersonHistorical = 'hmis:PersonHistorical'        
        xpPersonHistoricalIDIDNum = 'hmis:PersonHistoricalID/hmis:IDNum'
        xpPersonHistoricalIDIDStr = 'hmis:PersonHistoricalID/hmis:IDStr'
        xpSiteServiceID = 'hmis:SiteServiceID'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_service_participation_index_id', self.site_service_participation_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.PersonHistorical)
    
                ''' Parse sub-tables '''
                self.parse_housing_status(item)   
                self.parse_veteran(item)
                self.parse_vocational_training(item)         
                self.parse_substance_abuse_problem(item)         
                self.parse_pregnancy(item)         
                self.parse_prior_residence(item)         
                self.parse_physical_disability(item)         
                self.parse_non_cash_benefits(item)         
                self.parse_non_cash_benefits_last_30_days(item)         
                self.parse_mental_health_problem(item)         
                self.parse_length_of_stay_at_prior_residence(item)         
                self.parse_income_total_monthly(item)         
                self.parse_hud_chronic_homeless(item)         
                self.parse_income_last_30_days(item)         
                self.parse_highest_school_level(item)         
                self.parse_hiv_aids_status(item)         
                self.parse_health_status(item)         
                self.parse_engaged_date(item)         
                self.parse_employment(item)         
                self.parse_domestic_violence(item)         
                self.parse_disabling_condition(item)         
                self.parse_developmental_disability(item)         
                self.parse_destinations(item)         
                self.parse_degree(item)         
                self.parse_currently_in_school(item)         
                self.parse_contact_made(item)         
                self.parse_child_enrollment_status(item)         
                self.parse_chronic_health_condition(item) 
                self.parse_income_and_sources(item)
                self.parse_hud_homeless_episodes(item)
                self.parse_person_address(item)
                self.parse_email(item)                              
                self.parse_phone(item)      

    def parse_housing_status(self, element):
        ''' Element paths '''
        xpHousingStatus = 'hmis:HousingStatus'
        xpHousingStatusDateCollected = 'hmis:HousingStatus/@hmis:dateCollected'
        xpHousingStatusDateEffective = 'hmis:HousingStatus/@hmis:dateEffective'
        xpHousingStatusDataCollectionStage = 'hmis:HousingStatus/@hmis:dataCollectionStage'        

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.HousingStatus)
    
                ''' Parse sub-tables '''

    def parse_veteran(self, element):
        ''' Unique method -- loops all veteran elements and launches sub parsers '''

        ''' Element paths '''
        xpVeteran = 'hmis:Veteran'
        itemElements = element.xpath(xpVeteran, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}

                self.parse_veteran_military_branches(item)
                self.parse_veteran_military_service_duration(item)  
                self.parse_veteran_served_in_war_zone(item)         
                self.parse_veteran_service_era(item)         
                self.parse_veteran_veteran_status(item)         
                self.parse_veteran_warzones_served(item)                         
        
    def parse_veteran_military_branches(self, element):
        ''' Element paths '''
        xpMilitaryBranches = 'hmis:MilitaryBranches'
        xpMilitaryBranchIDIDNum = 'hmis:MilitaryBranchID/hmis:IDNum'
        xpMilitaryBranchIDIDStr = 'hmis:MilitaryBranchID/hmis:IDStr'
        xpMilitaryBranchIDDeleteOccurredDate = 'hmis:MilitaryBranchID/@hmis:deleteOccurredDate'
        xpMilitaryBranchIDDeleteEffective = 'hmis:MilitaryBranchID/@hmis:deleteEffective'
        xpMilitaryBranchIDDelete = 'hmis:MilitaryBranchID/@hmis:delete'
        xpDischargeStatus = 'hmis:DischargeStatus'
        xpDischargeStatusDateCollected = 'hmis:DischargeStatus/@hmis:dateCollected'
        xpDischargeStatusDateEffective = 'hmis:DischargeStatus/@hmis:dateEffective'
        xpDischargeStatusDataCollectionStage = 'hmis:DischargeStatus/@hmis:dataCollectionStage'
        xpDischargeStatusOther = 'hmis:DischargeStatusOther'
        xpDischargeStatusOtherDateCollected = 'hmis:DischargeStatusOther/@hmis:dateCollected'
        xpDischargeStatusOtherDateEffective = 'hmis:DischargeStatusOther/@hmis:dateEffective'
        xpDischargeStatusOtherDataCollectionStage = 'hmis:DischargeStatusOther/@hmis:dataCollectionStage'
        xpMilitaryBranch = 'hmis:MilitaryBranch'
        xpMilitaryBranchDateCollected = 'hmis:MilitaryBranch/@hmis:dateCollected'
        xpMilitaryBranchDateEffective = 'hmis:MilitaryBranch/@hmis:dateEffective'
        xpMilitaryBranchDataCollectionStage = 'hmis:MilitaryBranch/@hmis:dataCollectionStage'
        xpMilitaryBranchOther = 'hmis:MilitaryBranch'
        xpMilitaryBranchOtherDateCollected = 'hmis:MilitaryBranchOther/@hmis:dateCollected'
        xpMilitaryBranchOtherDateEffective = 'hmis:MilitaryBranchOther/@hmis:dateEffective'
        xpMilitaryBranchOtherDataCollectionStage = 'hmis:MilitaryBranchOther/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.VeteranMilitaryBranches)
    
                ''' Parse sub-tables '''
                            

    def parse_veteran_military_service_duration(self, element):
        ''' Element paths '''
        xpMilitaryServiceDuration = 'hmis:MilitaryServiceDuration'
        xpMilitaryServiceDurationDateCollected = 'hmis:MilitaryServiceDuration/@hmis:dateCollected'
        xpMilitaryServiceDurationDateEffective = 'hmis:MilitaryServiceDuration/@hmis:dateEffective'
        xpMilitaryServiceDurationDataCollectionStage = 'hmis:MilitaryServiceDuration/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.VeteranMilitaryServiceDuration)
    
                ''' Parse sub-tables '''
                            

    def parse_veteran_served_in_war_zone(self, element):
        ''' Element paths '''
        xpVeteranServedInWarZone = 'hmis:MilitaryServiceDuration'
        xpVeteranServedInWarZoneDurationDateCollected = 'hmis:VeteranServedInWarZone/@hmis:dateCollected'
        xpVeteranServedInWarZoneDurationDateEffective = 'hmis:VeteranServedInWarZone/@hmis:dateEffective'
        xpVeteranServedInWarZoneDurationDataCollectionStage = 'hmis:VeteranServedInWarZone/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.VeteranServedInWarZone)
    
                ''' Parse sub-tables '''
                            

    def parse_veteran_service_era(self, element):
        ''' Element paths '''
        xpServiceEra = 'hmis:ServiceEra'
        xpServiceEraDurationDateCollected = 'hmis:ServiceEra/@hmis:dateCollected'
        xpServiceEraDurationDateEffective = 'hmis:ServiceEra/@hmis:dateEffective'
        xpServiceEraDurationDataCollectionStage = 'hmis:ServiceEra/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.VeteranServiceEra)
    
                ''' Parse sub-tables '''
                            

    def parse_veteran_veteran_status(self, element):
        ''' Element paths '''
        xpVeteranStatus = 'hmis:VeteranStatus'
        xpVeteranStatusDurationDateCollected = 'hmis:VeteranStatus/@hmis:dateCollected'
        xpVeteranStatusDurationDateEffective = 'hmis:VeteranStatus/@hmis:dateEffective'
        xpVeteranStatusDurationDataCollectionStage = 'hmis:VeteranStatus/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.VeteranVeteranStatus)
    
                ''' Parse sub-tables '''
                            

    def parse_veteran_warzones_served(self, element):
        ''' Element paths '''
        xpVeteranWarZonesServed = 'hmis:WarZonesServed'
        xpWarZoneIDIDNum = 'hmis:WarZoneID/hmis:IDNum'
        xpWarZoneIDIDStr = 'hmis:WarZoneID/hmis:IDStr'
        xpWarZoneIDDeleteOccurredDate = 'hmis:MilitaryBranchID/@hmis:deleteOccurredDate'
        xpWarZoneIDDeleteEffective = 'hmis:MilitaryBranchID/@hmis:deleteEffective'
        xpWarZoneIDDelete = 'hmis:MilitaryBranchID/@hmis:delete'
        xpMonthsInWarZone = 'hmis:MonthsInWarZone'
        xpMonthsInWarZoneDateCollected = 'hmis:MonthsInWarZone/@hmis:dateCollected'
        xpMonthsInWarZoneDateEffective = 'hmis:MonthsInWarZone/@hmis:dateEffective'
        xpMonthsInWarZoneDataCollectionStage = 'hmis:MonthsInWarZone/@hmis:dataCollectionStage'
        xpReceivedFire = 'hmis:ReceivedFire'
        xpReceivedFireDateCollected = 'hmis:ReceivedFire/@hmis:dateCollected'
        xpReceivedFireDateEffective = 'hmis:ReceivedFire/@hmis:dateEffective'
        xpReceivedFireDataCollectionStage = 'hmis:ReceivedFire/@hmis:dataCollectionStage'
        xpWarZone = 'hmis:WarZone'
        xpWarZoneDateCollected = 'hmis:WarZone/@hmis:dateCollected'
        xpWarZoneDateEffective = 'hmis:WarZone/@hmis:dateEffective'
        xpWarZoneDataCollectionStage = 'hmis:WarZone/@hmis:dataCollectionStage'
        xpWarZoneOther = 'hmis:WarZoneOther'
        xpWarZoneOtherDateCollected = 'hmis:WarZoneOther/@hmis:dateCollected'
        xpWarZoneOtherDateEffective = 'hmis:WarZoneOther/@hmis:dateEffective'
        xpWarZoneOtherDataCollectionStage = 'hmis:WarZoneOther/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.VeteranWarzonesServed)
    
                ''' Parse sub-tables '''
                            

    def parse_vocational_training(self, element):
        ''' Element paths '''
        xpVocationalTraining = 'hmis:VocationalTraining'
        xpVocationalTrainingDateCollected = 'hmis:VocationalTraining/@hmis:dateCollected'
        xpVocationalTrainingDateEffective = 'hmis:VocationalTraining/@hmis:dateEffective'
        xpVocationalTrainingDataCollectionStage = 'hmis:VocationalTraining/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.VocationalTraining)
    
                ''' Parse sub-tables '''
                            

    def parse_substance_abuse_problem(self, element):
        ''' Element paths '''
        xpSubstanceAbuseProblem = 'hmis:SubstanceAbuseProblem'
        xpHasSubstanceAbuseProblem = 'hmis:HasSubstanceAbuseProblem'
        xpHasSubstanceAbuseProblemDateCollected = 'hmis:HasSubstanceAbuseProblem/@hmis:dateCollected'
        xpHasSubstanceAbuseProblemDateEffective = 'hmis:HasSubstanceAbuseProblem/@hmis:dateEffective'
        xpHasSubstanceAbuseProblemDataCollectionStage = 'hmis:HasSubstanceAbuseProblem/@hmis:dataCollectionStage'
        xpSubstanceAbuseIndefinite = 'hmis:SubstanceAbuseIndefinite'
        xpSubstanceAbuseIndefiniteDateCollected = 'hmis:SubstanceAbuseIndefinite/@hmis:dateCollected'
        xpSubstanceAbuseIndefiniteDateEffective = 'hmis:SubstanceAbuseIndefinite/@hmis:dateEffective'
        xpSubstanceAbuseIndefiniteDataCollectionStage = 'hmis:SubstanceAbuseIndefinite/@hmis:dataCollectionStage'
        xpReceiveSubstanceAbuseServices = 'hmis:ReceiveSubstanceAbuseServices'
        xpReceiveSubstanceAbuseServicesDateCollected = 'hmis:ReceiveSubstanceAbuseServices/@hmis:dateCollected'
        xpReceiveSubstanceAbuseServicesDateEffective = 'hmis:ReceiveSubstanceAbuseServices/@hmis:dateEffective'
        xpReceiveSubstanceAbuseServicesDataCollectionStage = 'hmis:ReceiveSubstanceAbuseServices/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.SubstanceAbuseProblem)
    
                ''' Parse sub-tables '''
                            

    def parse_pregnancy(self, element):
        ''' Element paths '''
        xpPregnancy = 'hmis:Pregnancy'
        xpPregnancyIDIDNum = 'hmis:PregnancyID/hmis:IDNum'
        xpPregnancyIDIDStr = 'hmis:PregnancyID/hmis:IDStr'
        xpPregnancyIDDeleteOccurredDate = 'hmis:PregnancyID/@hmis:deleteOccurredDate'
        xpPregnancyIDDeleteEffective = 'hmis:PregnancyID/@hmis:deleteEffective'
        xpPregnancyIDDelete = 'hmis:PregnancyID/@hmis:delete'
        xpPregnancyStatus = 'hmis:PregnancyStatus'
        xpPregnancyStatusDateCollected = 'hmis:PregnancyStatus/@hmis:dateCollected'
        xpPregnancyStatusDateEffective = 'hmis:PregnancyStatus/@hmis:dateEffective'
        xpPregnancyStatusDataCollectionStage = 'hmis:PregnancyStatus/@hmis:dataCollectionStage'
        xpDueDate = 'hmis:DueDate'
        xpDueDateDateCollected = 'hmis:DueDate/@hmis:dateCollected'
        xpDueDateDateEffective = 'hmis:DueDate/@hmis:dateEffective'
        xpDueDateDataCollectionStage = 'hmis:DueDate/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Pregnancy)
    
                ''' Parse sub-tables '''
                            

    def parse_prior_residence(self, element):
        ''' Element paths '''
        xpPriorResidence = 'hmis:PriorResidence'
        xpPriorResidenceIDIDNum = 'hmis:PriorResidenceID/hmis:IDNum'
        xpPriorResidenceIDIDStr = 'hmis:PriorResidenceID/hmis:IDStr'
        xpPriorResidenceIDDeleteOccurredDate = 'hmis:PriorResidenceID/@hmis:deleteOccurredDate'
        xpPriorResidenceIDDeleteEffective = 'hmis:PriorResidenceID/@hmis:deleteEffective'
        xpPriorResidenceIDDelete = 'hmis:PriorResidenceID/@hmis:delete'
        xpPriorResidenceCode = 'hmis:PriorResidenceCode'
        xpPriorResidenceCodeDateCollected = 'hmis:PriorResidenceCode/@hmis:dateCollected'
        xpPriorResidenceCodeDateEffective = 'hmis:PriorResidenceCode/@hmis:dateEffective'
        xpPriorResidenceCodeDataCollectionStage = 'hmis:PriorResidenceCode/@hmis:dataCollectionStage'
        xpPriorResidenceOther = 'hmis:PriorResidenceOther'
        xpPriorResidenceOtherDateCollected = 'hmis:PriorResidenceOther/@hmis:dateCollected'
        xpPriorResidenceOtherDateEffective = 'hmis:PriorResidenceOther/@hmis:dateEffective'
        xpPriorResidenceOtherDataCollectionStage = 'hmis:PriorResidenceOther/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.PriorResidence)
    
                ''' Parse sub-tables '''
                            

    def parse_physical_disability(self, element):
        ''' Element paths '''
        xpPhysicalDisability = 'hmis:PhysicalDisability'
        xpHasPhysicalDisability = 'hmis:HasPhysicalDisability'
        xpHasPhysicalDisabilityDateCollected = 'hmis:HasPhysicalDisability/@hmis:dateCollected'
        xpHasPhysicalDisabilityDateEffective = 'hmis:HasPhysicalDisability/@hmis:dateEffective'
        xpHasPhysicalDisabilityDataCollectionStage = 'hmis:HasPhysicalDisability/@hmis:dataCollectionStage'
        xpReceivePhysicalDisabilityServices = 'hmis:ReceivePhysicalDisabilityServices'
        xpReceivePhysicalDisabilityServicesDateCollected = 'hmis:ReceivePhysicalDisabilityServices/@hmis:dateCollected'
        xpReceivePhysicalDisabilityServicesDateEffective = 'hmis:ReceivePhysicalDisabilityServices/@hmis:dateEffective'
        xpReceivePhysicalDisabilityServicesDataCollectionStage = 'hmis:ReceivePhysicalDisabilityServices/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.PhysicalDisability)
    
                ''' Parse sub-tables '''
                            

    def parse_non_cash_benefits(self, element):
        ''' Element paths '''
        xpNonCashBenefit = 'hmis:NonCashBenefits/hmis:NonCashBenefit'
        xpNonCashBenefitIDIDNum = 'hmis:NonCashBenefitID/hmis:IDNum'
        xpNonCashBenefitIDIDStr = 'hmis:NonCashBenefitID/hmis:IDStr'
        xpNonCashBenefitIDDeleteOccurredDate = 'hmis:NonCashBenefitID/@hmis:deleteOccurredDate'
        xpNonCashBenefitIDDeleteEffective = 'hmis:NonCashBenefitID/@hmis:deleteEffective'
        xpNonCashBenefitIDDelete = 'hmis:NonCashBenefitID/@hmis:delete'

        xpNonCashSourceCode = 'hmis:NonCashSourceCode'
        xpNonCashSourceCodeDateCollected = 'hmis:NonCashSourceCode/@hmis:dateCollected'
        xpNonCashSourceCodeDateEffective = 'hmis:NonCashSourceCode/@hmis:dateEffective'
        xpNonCashSourceCodeDataCollectionStage = 'hmis:NonCashSourceCode/@hmis:dataCollectionStage'

        xpNonCashSourceOther = 'hmis:NonCashSourceOther'
        xpNonCashSourceOtherDateCollected = 'hmis:NonCashSourceOther/@hmis:dateCollected'
        xpNonCashSourceOtherDateEffective = 'hmis:NonCashSourceOther/@hmis:dateEffective'
        xpNonCashSourceOtherDataCollectionStage = 'hmis:NonCashSourceOther/@hmis:dataCollectionStage'

        xpReceivingNonCashSource = 'hmis:ReceivingNonCashSource'
        xpReceivingNonCashSourceDateCollected = 'hmis:ReceivingNonCashSource/@hmis:dateCollected'
        xpReceivingNonCashSourceDateEffective = 'hmis:ReceivingNonCashSource/@hmis:dateEffective'
        xpReceivingNonCashSourceDataCollectionStage = 'hmis:ReceivingNonCashSource/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.NonCashBenefits)
    
                ''' Parse sub-tables '''

    def parse_non_cash_benefits_last_30_days(self, element):
        ''' Element paths '''
        xpNonCashBenefitsLast30Days = 'hmis:NonCashBenefitsLast30Days'
        xpNonCashBenefitsLast30DaysDateCollected = 'hmis:NonCashBenefitsLast30Days/@hmis:dateCollected'
        xpNonCashBenefitsLast30DaysDateEffective = 'hmis:NonCashBenefitsLast30Days/@hmis:dateEffective'
        xpNonCashBenefitsLast30DaysDataCollectionStage = 'hmis:NonCashBenefitsLast30Days/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.NonCashBenefitsLast30Days)
    
                ''' Parse sub-tables '''
                            

    def parse_mental_health_problem(self, element):
        ''' Element paths '''
        xpMentalHealthProblem = 'hmis:MentalHealthProblem'
        xpHasMentalHealthProblem = 'hmis:HasMentalHealthProblem'
        xpHasMentalHealthProblemDateCollected = 'hmis:HasMentalHealthProblem/@hmis:dateCollected'
        xpHasMentalHealthProblemDateEffective = 'hmis:HasMentalHealthProblem/@hmis:dateEffective'
        xpHasMentalHealthProblemDataCollectionStage = 'hmis:HasMentalHealthProblem/@hmis:dataCollectionStage'
        xpMentalHealthIndefinite = 'hmis:MentalHealthIndefinite'
        xpMentalHealthIndefiniteDateCollected = 'hmis:MentalHealthIndefinite/@hmis:dateCollected'
        xpMentalHealthIndefiniteDateEffective = 'hmis:MentalHealthIndefinite/@hmis:dateEffective'
        xpMentalHealthIndefiniteDataCollectionStage = 'hmis:MentalHealthIndefinite/@hmis:dataCollectionStage'
        xpReceiveMentalHealthServices = 'hmis:ReceiveMentalHealthServices'
        xpReceiveMentalHealthServicesDateCollected = 'hmis:ReceiveMentalHealthServices/@hmis:dateCollected'
        xpReceiveMentalHealthServicesDateEffective = 'hmis:ReceiveMentalHealthServices/@hmis:dateEffective'
        xpReceiveMentalHealthServicesDataCollectionStage = 'hmis:ReceiveMentalHealthServices/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.MentalHealthProblem)
    
                ''' Parse sub-tables '''
                            

    def parse_length_of_stay_at_prior_residence(self, element):
        ''' Element paths '''
        xpLengthOfStaAtPriorResidence = 'hmis:LengthOfStaAtPriorResidence'
        xpLengthOfStaAtPriorResidenceDateCollected = 'hmis:LengthOfStaAtPriorResidence/@hmis:dateCollected'
        xpLengthOfStaAtPriorResidenceDateEffective = 'hmis:LengthOfStaAtPriorResidence/@hmis:dateEffective'
        xpLengthOfStaAtPriorResidenceDataCollectionStage = 'hmis:LengthOfStaAtPriorResidence/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.LengthOfStayAtPriorResidence)
    
                ''' Parse sub-tables '''
                            

    def parse_income_total_monthly(self, element):
        ''' Element paths '''
        xpIncomeTotalMonthly = 'hmis:IncomeTotalMonthly'
        xpIncomeTotalMonthlyDateCollected = 'hmis:IncomeTotalMonthly/@hmis:dateCollected'
        xpIncomeTotalMonthlyDateEffective = 'hmis:IncomeTotalMonthly/@hmis:dateEffective'
        xpIncomeTotalMonthlyDataCollectionStage = 'hmis:IncomeTotalMonthly/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.IncomeTotalMonthly)
    
                ''' Parse sub-tables '''
                            

    def parse_hud_chronic_homeless(self, element):
        ''' Element paths '''
        xpHUDChronicHomeless = 'hmis:HUDChronicHomeless'
        xpHUDChronicHomelessDateCollected = 'hmis:HUDChronicHomeless/@hmis:dateCollected'
        xpHUDChronicHomelessDateEffective = 'hmis:HUDChronicHomeless/@hmis:dateEffective'
        xpHUDChronicHomelessDataCollectionStage = 'hmis:HUDChronicHomeless/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.HudChronicHomeless)
    
                ''' Parse sub-tables '''
                            

    def parse_income_last_30_days(self, element):
        ''' Element paths '''
        xpIncomeLast30Days = 'hmis:IncomeLast30Days'
        xpIncomeLast30DaysDateCollected = 'hmis:IncomeLast30Days/@hmis:dateCollected'
        xpIncomeLast30DaysDateEffective = 'hmis:IncomeLast30Days/@hmis:dateEffective'
        xpIncomeLast30DaysDataCollectionStage = 'hmis:IncomeLast30Days/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.IncomeLast30Days)
    
                ''' Parse sub-tables '''
                            

    def parse_highest_school_level(self, element):
        ''' Element paths '''
        xpHighestSchoolLevel = 'hmis:HighestSchoolLevel'
        xpHighestSchoolLevelDateCollected = 'hmis:HighestSchoolLevel/@hmis:dateCollected'
        xpHighestSchoolLevelDateEffective = 'hmis:HighestSchoolLevel/@hmis:dateEffective'
        xpHighestSchoolLevelDataCollectionStage = 'hmis:HighestSchoolLevel/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.HighestSchoolLevel)
    
                ''' Parse sub-tables '''
                            

    def parse_hiv_aids_status(self, element):
        ''' Element paths '''
        xpHIVAIDSStatus = 'hmis:HIVAIDSStatus'
        xpHasHIVAIDS = 'hmis:HasHIVAIDS'
        xpHasHIVAIDSDateCollected = 'hmis:HasHIVAIDS/@hmis:dateCollected'
        xpHasHIVAIDSDateEffective = 'hmis:HasHIVAIDS/@hmis:dateEffective'
        xpHasHIVAIDSDataCollectionStage = 'hmis:HasHIVAIDS/@hmis:dataCollectionStage'
        xpReceiveHIVAIDSServices = 'hmis:ReceiveHIVAIDSServices'
        xpReceiveHIVAIDSServicesDateCollected = 'hmis:ReceiveHIVAIDSServices/@hmis:dateCollected'
        xpReceiveHIVAIDSServicesDateEffective = 'hmis:ReceiveHIVAIDSServices/@hmis:dateEffective'
        xpReceiveHIVAIDSServicesDataCollectionStage = 'hmis:ReceiveHIVAIDSServices/@hmis:dataCollectionStage'        

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.HivAidsStatus)
    
                ''' Parse sub-tables '''
                            

    def parse_health_status(self, element):
        ''' Element paths '''
        xpHealthStatus = 'hmis:HealthStatus'
        xpHealthStatusDateCollected = 'hmis:HealthStatus/@hmis:dateCollected'
        xpHealthStatusDateEffective = 'hmis:HealthStatus/@hmis:dateEffective'
        xpHealthStatusDataCollectionStage = 'hmis:HealthStatus/@hmis:dataCollectionStage'     

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.HealthStatus)
    
                ''' Parse sub-tables '''
                            

    def parse_engaged_date(self, element):
        ''' Element paths '''
        xpEngagedDate = 'hmis:EngagedDate'
        xpEngagedDateDateCollected = 'hmis:EngagedDate/@hmis:dateCollected'
        xpEngagedDateDateEffective = 'hmis:EngagedDate/@hmis:dateEffective'
        xpEngagedDateDataCollectionStage = 'hmis:EngagedDate/@hmis:dataCollectionStage'  

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.EngagedDate)
    
                ''' Parse sub-tables '''
                            

    def parse_employment(self, element):
        ''' Element paths '''
        xpEmployment = 'hmis:Employment'
        xpEmploymentIDIDNum = 'hmis:PriorResidenceID/hmis:IDNum'
        xpEmploymentIDIDStr = 'hmis:PriorResidenceID/hmis:IDStr'
        xpEmploymentIDDeleteOccurredDate = 'hmis:PriorResidenceID/@hmis:deleteOccurredDate'
        xpEmploymentIDDeleteEffective = 'hmis:PriorResidenceID/@hmis:deleteEffective'
        xpEmploymentIDDelete = 'hmis:PriorResidenceID/@hmis:delete'
        xpCurrentlyEmployed = 'hmis:CurrentlyEmployed'
        xpCurrentlyEmployedDateCollected = 'hmis:CurrentlyEmployed/@hmis:dateCollected'
        xpCurrentlyEmployedDateEffective = 'hmis:CurrentlyEmployed/@hmis:dateEffective'
        xpCurrentlyEmployedDataCollectionStage = 'hmis:CurrentlyEmployed/@hmis:dataCollectionStage'
        xpHoursWorkedLastWeek = 'hmis:HoursWorkedLastWeek'
        xpHoursWorkedLastWeekDateCollected = 'hmis:HoursWorkedLastWeek/@hmis:dateCollected'
        xpHoursWorkedLastWeekDateEffective = 'hmis:HoursWorkedLastWeek/@hmis:dateEffective'
        xpHoursWorkedLastWeekDataCollectionStage = 'hmis:HoursWorkedLastWeek/@hmis:dataCollectionStage'
        xpEmploymentTenure = 'hmis:EmploymentTenure'
        xpEmploymentTenureDateCollected = 'hmis:EmploymentTenure/@hmis:dateCollected'
        xpEmploymentTenureDateEffective = 'hmis:EmploymentTenure/@hmis:dateEffective'
        xpEmploymentTenureDataCollectionStage = 'hmis:EmploymentTenure/@hmis:dataCollectionStage'
        xpLookingForWork = 'hmis:LookingForWork'
        xpLookingForWorkDateCollected = 'hmis:LookingForWork/@hmis:dateCollected'
        xpLookingForWorkDateEffective = 'hmis:LookingForWork/@hmis:dateEffective'
        xpLookingForWorkDataCollectionStage = 'hmis:LookingForWork/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Employment)
    
                ''' Parse sub-tables '''
                            

    def parse_domestic_violence(self, element):
        ''' Element paths '''
        xpDomesticViolence = 'hmis:DomesticViolence'
        xpDomesticViolenceSurvivor = 'hmis:DomesticViolenceSurvivor'
        xpDomesticViolenceSurvivorDateCollected = 'hmis:DomesticViolenceSurvivor/@hmis:dateCollected'
        xpDomesticViolenceSurvivorDateEffective = 'hmis:DomesticViolenceSurvivor/@hmis:dateEffective'
        xpDomesticViolenceSurvivorDataCollectionStage = 'hmis:DomesticViolenceSurvivor/@hmis:dataCollectionStage'
        xpDVOccurred = 'hmis:DVOccurred'
        xpDVOccurredDateCollected = 'hmis:DVOccurred/@hmis:dateCollected'
        xpDVOccurredDateEffective = 'hmis:DVOccurred/@hmis:dateEffective'
        xpDVOccurredDataCollectionStage = 'hmis:DVOccurred/@hmis:dataCollectionStage'        

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.DomesticViolence)
    
                ''' Parse sub-tables '''
                            

    def parse_disabling_condition(self, element):
        ''' Element paths '''
        xpDisablingCondition = 'hmis:DisablingCondition'
        xpDisablingConditionDateCollected = 'hmis:DisablingCondition/@hmis:dateCollected'
        xpDisablingConditionDateEffective = 'hmis:DisablingCondition/@hmis:dateEffective'
        xpDisablingConditionDataCollectionStage = 'hmis:DisablingCondition/@hmis:dataCollectionStage'    

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.DisablingCondition)
    
                ''' Parse sub-tables '''
                            

    def parse_developmental_disability(self, element):
        ''' Element paths '''
        xpDevelopmentalDisability = 'hmis:DevelopmentalDisability'
        xpHasDevelopmentalDisability = 'hmis:HasDevelopmentalDisability'
        xpHasDevelopmentalDisabilityDateCollected = 'hmis:HasDevelopmentalDisability/@hmis:dateCollected'
        xpHasDevelopmentalDisabilityDateEffective = 'hmis:HasDevelopmentalDisability/@hmis:dateEffective'
        xpHasDevelopmentalDisabilityDataCollectionStage = 'hmis:HasDevelopmentalDisability/@hmis:dataCollectionStage'    
        xpReceiveDevelopmentalDisability = 'hmis:ReceiveDevelopmentalDisability'
        xpReceiveDevelopmentalDisabilityDateCollected = 'hmis:ReceiveDevelopmentalDisability/@hmis:dateCollected'
        xpReceiveDevelopmentalDisabilityDateEffective = 'hmis:ReceiveDevelopmentalDisability/@hmis:dateEffective'
        xpReceiveDevelopmentalDisabilityDataCollectionStage = 'hmis:ReceiveDevelopmentalDisability/@hmis:dataCollectionStage'    

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.DevelopmentalDisability)
    
                ''' Parse sub-tables '''
                            

    def parse_destinations(self, element):
        ''' Element paths '''
        xpDestinations = 'hmis:Destinations/hmis:Destination'
        xpDestinationIDIDNum = 'hmis:DestinationID/hmis:IDNum'
        xpDestinationIDIDStr = 'hmis:DestinationID/hmis:IDStr'
        xpDestinationIDDeleteOccurredDate = 'hmis:DestinationID/@hmis:deleteOccurredDate'
        xpDestinationIDDeleteEffective = 'hmis:DestinationID/@hmis:deleteEffective'
        xpDestinationIDDelete = 'hmis:DestinationID/@hmis:delete'
        xpDestinationCode = 'hmis:DestinationCode'
        xpDestinationCodeDateCollected = 'hmis:DestinationCode/@hmis:dateCollected'
        xpDestinationCodeDateEffective = 'hmis:DestinationCode/@hmis:dateEffective'
        xpDestinationCodeDataCollectionStage = 'hmis:DestinationCode/@hmis:dataCollectionStage'
        xpDestinationOther = 'hmis:DestinationOther'
        xpDestinationOtherDateCollected = 'hmis:DestinationOther/@hmis:dateCollected'
        xpDestinationOtherDateEffective = 'hmis:DestinationOther/@hmis:dateEffective'
        xpDestinationOtherDataCollectionStage = 'hmis:DestinationOther/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                try: self.existence_test_and_add('household_id_num', item.xpath(xpHouseholdIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                except: pass
                try: self.existence_test_and_add('household_id_num_date_collected', item.xpath(xpHouseholdIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                except: pass

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Destinations)
    
                ''' Parse sub-tables '''
                            

    def parse_degree(self, element):
        ''' Element paths '''
        xpDegree = 'hmis:Degree'
        xpDegreeIDIDNum = 'hmis:Degree/hmis:IDNum'
        xpDegreeIDIDStr = 'hmis:Degree/hmis:IDStr'
        xpDegreeIDDeleteOccurredDate = 'hmis:Degree/@hmis:deleteOccurredDate'
        xpDegreeIDDeleteEffective = 'hmis:Degree/@hmis:deleteEffective'
        xpDegreeIDDelete = 'hmis:Degree/@hmis:delete'
        xpDegreeOther = 'hmis:DegreeOther'
        xpDegreeOtherDateCollected = 'hmis:DegreeOther/@hmis:dateCollected'
        xpDegreeOtherDateEffective = 'hmis:DegreeOther/@hmis:dateEffective'
        xpDegreeOtherDataCollectionStage = 'hmis:DegreeOther/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Degree)
    
                ''' Parse sub-tables '''
                self.parse_degree_code(item)            

    def parse_degree_code(self, element):
        ''' Element paths '''
        xpDegreeCode = 'hmis:DegreeCode'
        xpDegreeCodeDateCollected = 'hmis:DegreeCode/@hmis:dateCollected'
        xpDegreeCodeDateEffective = 'hmis:DegreeCode/@hmis:dateEffective'
        xpDegreeCodeDataCollectionStage = 'hmis:DegreeCode/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('degree_index_id', self.degree_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.DegreeCode)
    
                ''' Parse sub-tables '''
                            

    def parse_currently_in_school(self, element):
        ''' Element paths '''
        xpCurrentlyInSchool = 'hmis:CurrentlyInSchool'
        xpCurrentlyInSchoolDateCollected = 'hmis:CurrentlyInSchool/@hmis:dateCollected'
        xpCurrentlyInSchoolDateEffective = 'hmis:CurrentlyInSchool/@hmis:dateEffective'
        xpCurrentlyInSchoolDataCollectionStage = 'hmis:CurrentlyInSchool/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.CurrentlyInSchool)
    
                ''' Parse sub-tables '''
                            

    def parse_contact_made(self, element):
        ''' Element paths '''
        xpContactsMade = 'hmis:ContactsMade/hmis:ContactMade'
        xpContactIDIDNum = 'hmis:ContactID/hmis:IDNum'
        xpContactIDIDStr = 'hmis:ContactID/hmis:IDStr'
        xpContactIDDeleteOccurredDate = 'hmis:ContactID/@hmis:deleteOccurredDate'
        xpContactIDDeleteEffective = 'hmis:ContactID/@hmis:deleteEffective'
        xpContactIDDelete = 'hmis:ContactID/@hmis:delete'
        xpContactDate = 'hmis:ContactDate'
        xpContactDateDataCollectionStage = 'hmis:ContactDate/@hmis:dataCollectionStage'
        xpContactLocation = 'hmis:ContactLocation'
        xpContactLocationDataCollectionStage = 'hmis:ContactLocation/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ContactMade)
    
                ''' Parse sub-tables '''
                            

    def parse_child_enrollment_status(self, element):
        ''' Element paths '''
        xpChildEnrollmentStatus = 'hmis:ChildEnrollmentStatus'
        xpChildEnrollmentStatusIDIDNum = 'hmis:ChildEnrollmentStatusID/hmis:IDNum'
        xpChildEnrollmentStatusIDIDStr = 'hmis:ChildEnrollmentStatusID/hmis:IDStr'
        xpChildEnrollmentStatusIDDeleteOccurredDate = 'hmis:ChildEnrollmentStatusID/@hmis:deleteOccurredDate'
        xpChildEnrollmentStatusIDDeleteEffective = 'hmis:ChildEnrollmentStatusID/@hmis:deleteEffective'
        xpChildEnrollmentStatusIDDelete = 'hmis:ChildEnrollmentStatusID/@hmis:delete'
        xpChildCurrentlyEnrolledInSchool = 'hmis:ChildCurrentlyEnrolledInSchool'
        xpChildCurrentlyEnrolledInSchoolDateCollected = 'hmis:ChildCurrentlyEnrolledInSchool/@hmis:dateCollected'
        xpChildCurrentlyEnrolledInSchoolDateEffective = 'hmis:ChildCurrentlyEnrolledInSchool/@hmis:dateEffective'
        xpChildCurrentlyEnrolledInSchoolDataCollectionStage = 'hmis:ChildCurrentlyEnrolledInSchool/@hmis:dataCollectionStage'
        xpChildSchoolName = 'hmis:ChildSchoolName'
        xpChildSchoolNameDateCollected = 'hmis:ChildSchoolName/@hmis:dateCollected'
        xpChildSchoolNameDateEffective = 'hmis:ChildSchoolName/@hmis:dateEffective'
        xpChildSchoolNameDataCollectionStage = 'hmis:ChildSchoolName/@hmis:dataCollectionStage'
        xpChildMcKinneyVentoLiaison = 'hmis:ChildMcKinneyVentoLiaison'
        xpChildMcKinneyVentoLiaisonDateCollected = 'hmis:ChildMcKinneyVentoLiaison/@hmis:dateCollected'
        xpChildMcKinneyVentoLiaisonDateEffective = 'hmis:ChildMcKinneyVentoLiaison/@hmis:dateEffective'
        xpChildMcKinneyVentoLiaisonDataCollectionStage = 'hmis:ChildMcKinneyVentoLiaison/@hmis:dataCollectionStage'
        xpChildSchoolType = 'hmis:ChildSchoolType'
        xpChildSchoolTypeDateCollected = 'hmis:ChildSchoolType/@hmis:dateCollected'
        xpChildSchoolTypeDateEffective = 'hmis:ChildSchoolType/@hmis:dateEffective'
        xpChildSchoolTypeDataCollectionStage = 'hmis:ChildSchoolType/@hmis:dataCollectionStage'
        xpChildSchoolLastEnrolledDate = 'hmis:ChildSchoolLastEnrolledDate'
        xpChildSchoolLastEnrolledDateDateCollected = 'hmis:ChildSchoolLastEnrolledDate/@hmis:dateCollected'
        xpChildSchoolLastEnrolledDateDateEffective = 'hmis:ChildSchoolLastEnrolledDate/@hmis:dateEffective'
        xpChildSchoolLastEnrolledDateDataCollectionStage = 'hmis:ChildSchoolLastEnrolledDate/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ChildEnrollmentStatus)
    
                ''' Parse sub-tables '''
                self.parse_child_enrollment_status_barrier(item)            

    def parse_child_enrollment_status_barrier(self, element):
        ''' Element paths '''
        xpChildEnrollmentBarrier = 'hmis:ChildEnrollmentBarrier'
        xpBarrierIDIDNum = 'hmis:BarrierID/hmis:IDNum'
        xpBarrierIDIDStr = 'hmis:BarrierID/hmis:IDStr'
        xpBarrierIDDeleteOccurredDate = 'hmis:BarrierID/@hmis:deleteOccurredDate'
        xpBarrierIDDeleteEffective = 'hmis:BarrierID/@hmis:deleteEffective'
        xpBarrierIDDelete = 'hmis:BarrierID/@hmis:delete'
        xpBarrierCode = 'hmis:BarrierCode'
        xpBarrierCodeDateCollected = 'hmis:BarrierCode/@hmis:dateCollected'
        xpBarrierCodeDateEffective = 'hmis:BarrierCode/@hmis:dateEffective'
        xpBarrierCodeDataCollectionStage = 'hmis:BarrierCode/@hmis:dataCollectionStage'
        xpBarrierOther = 'hmis:BarrierOther'
        xpBarrierOtherDateCollected = 'hmis:BarrierOther/@hmis:dateCollected'
        xpBarrierOtherDateEffective = 'hmis:BarrierOther/@hmis:dateEffective'
        xpBarrierOtherDataCollectionStage = 'hmis:BarrierOther/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('child_enrollment_status_index_id', self.child_enrollment_status_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ChildEnrollmentStatusBarrier)
    
                ''' Parse sub-tables '''
                            

    def parse_chronic_health_condition(self, element):
        ''' Element paths '''
        xpChronicHealthCondition = 'hmis:ChronicHealthCondition'
        xpHasChronicHealthCondition = 'hmis:HasChronicHealthCondition'
        xpHasChronicHealthConditionDateCollected = 'hmis:HasChronicHealthCondition/@hmis:dateCollected'
        xpHasChronicHealthConditionDateEffective = 'hmis:HasChronicHealthCondition/@hmis:dateEffective'
        xpHasChronicHealthConditionDataCollectionStage = 'hmis:HasChronicHealthCondition/@hmis:dataCollectionStage'
        xpReceiveChronicHealthServices = 'hmis:ReceiveChronicHealthServices'
        xpReceiveChronicHealthServicesDateCollected = 'hmis:ReceiveChronicHealthServices/@hmis:dateCollected'
        xpReceiveChronicHealthServicesDateEffective = 'hmis:ReceiveChronicHealthServices/@hmis:dateEffective'
        xpReceiveChronicHealthServicesDataCollectionStage = 'hmis:ReceiveChronicHealthServices/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ChronicHealthCondition)
    
                ''' Parse sub-tables '''
                            

    def parse_release_of_information(self, element):
        ''' Element paths '''
        xpReleaseOfInformation = 'hmis:ReleaseOfInformation'
        xpReleaseOfInformationIDIDNum = 'hmis:ReleaseOfInformationID/hmis:IDNum'
        xpReleaseOfInformationIDIDStr = 'hmis:ReleaseOfInformationID/hmis:IDStr'
        xpReleaseOfInformationIDDateCollected = 'hmis:ReleaseOfInformationID/@hmis:dateCollected'
        xpReleaseOfInformationIDDateEffective = 'hmis:ReleaseOfInformationID/@hmis:dateEffective'
        xpReleaseOfInformationIDDataCollectionStage = 'hmis:ReleaseOfInformationID/@hmis:dataCollectionStage'
        xpSiteServiceID = 'hmis:SiteServiceID'
        xpDocumentation = 'hmis:Documentation'
        xpDocumentationDateCollected = 'hmis:Documentation/@hmis:dateCollected'
        xpDocumentationDateEffective = 'hmis:Documentation/@hmis:dateEffective'
        xpDocumentationDataCollectionStage = 'hmis:Documentation/@hmis:dataCollectionStage'
        xpStartDate = 'hmis:EffectivePeriod/hmis:StartDate'
        xpEndDate = 'hmis:EffectivePeriod/hmis:EndDate'
        xpReleaseGranted = 'hmis:ReleaseGranted'
        xpReleaseGrantedDateCollected = 'hmis:ReleaseGranted/@hmis:dateCollected'
        xpReleaseGrantedDateEffective = 'hmis:ReleaseGranted/@hmis:dateEffective'
        xpReleaseGrantedDataCollectionStage = 'hmis:ReleaseGranted/@hmis:dataCollectionStage'
        
        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ReleaseOfInformation)
    
                ''' Parse sub-tables '''
                            

    def parse_income_and_sources(self, element):
        ''' Element paths '''
        xpIncomeAndSources = 'hmis:IncomeAndSources/IncomeAndSource'
        xpIncomeAndSourceIDIDNum = 'hmis:IncomeAndSourceID/hmis:IDNum'
        xpIncomeAndSourceIDIDStr = 'hmis:IncomeAndSourceID/hmis:IDStr'
        xpIncomeAndSourceIDDeleteOccurredDate = 'hmis:IncomeAndSourceID/@hmis:deleteOccurredDate'
        xpIncomeAndSourceIDDeleteEffective = 'hmis:IncomeAndSourceID/@hmis:deleteEffective'
        xpIncomeAndSourceIDDelete = 'hmis:IncomeAndSourceID/@hmis:delete'
        xpIncomeSourceCode = 'hmis:IncomeSourceCode'
        xpIncomeSourceCodeDateCollected = 'hmis:IncomeSourceCode/@hmis:dateCollected'
        xpIncomeSourceCodeDateEffective = 'hmis:IncomeSourceCode/@hmis:dateEffective'
        xpIncomeSourceCodeDataCollectionStage = 'hmis:IncomeSourceCode/@hmis:dataCollectionStage'
        xpIncomeSourceOther = 'hmis:IncomeSourceOther'
        xpIncomeSourceOtherDateCollected = 'hmis:IncomeSourceOther/@hmis:dateCollected'
        xpIncomeSourceOtherDateEffective = 'hmis:IncomeSourceOther/@hmis:dateEffective'
        xpIncomeSourceOtherDataCollectionStage = 'hmis:IncomeSourceOther/@hmis:dataCollectionStage'
        xpReceivingIncomingSource = 'hmis:ReceivingIncomingSource'
        xpReceivingIncomingSourceDateCollected = 'hmis:ReceivingIncomingSource/@hmis:dateCollected'
        xpReceivingIncomingSourceDateEffective = 'hmis:ReceivingIncomingSource/@hmis:dateEffective'
        xpReceivingIncomingSourceDataCollectionStage = 'hmis:ReceivingIncomingSource/@hmis:dataCollectionStage'
        xpIncomeSourceAmount = 'hmis:IncomeSourceAmount'
        xpIncomeSourceAmountDateCollected = 'hmis:IncomeSourceAmount/@hmis:dateCollected'
        xpIncomeSourceAmountDateEffective = 'hmis:IncomeSourceAmount/@hmis:dateEffective'
        xpIncomeSourceAmountDataCollectionStage = 'hmis:IncomeSourceAmount/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.IncomeAndSources)
    
                ''' Parse sub-tables '''
                            

    def parse_hud_homeless_episodes(self, element):
        ''' Element paths '''
            xpHudHomelessEpisodes = 'hmis:HUDHomelessEpisodes'
            xpStartDate = 'hmis:StartDate'
            xpEndDate = 'hmis:EndDate'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.HudHomelessEpisodes)
    
                ''' Parse sub-tables '''
                            

    def parse_person_address(self, element):
        ''' Element paths '''
        xpPersonAddress = 'hmis:PersonAddress'
        xpPersonAddressDateCollected = 'hmis:PersonAddress/@hmis:dateCollected'
        xpPersonAddressDateEffective = 'hmis:PersonAddress/@hmis:dateEffective'
        xpPersonAddressDataCollectionStage = 'hmis:PersonAddress/@hmis:dataCollectionStage'          
        xpAddressPeriodStartDate = 'hmis:AddressPeriod/hmis:StartDate'
        xpAddressPeriodEndDate = 'hmis:AddressPeriod/hmis:EndDate'
        xpPreAddressLine = 'hmis:PreAddressLine'
        xpPreAddressLineDateCollected = 'hmis:PreAddressLine/@hmis:dateCollected'
        xpPreAddressLineDateEffective = 'hmis:PreAddressLine/@hmis:dateEffective'
        xpPreAddressLineDataCollectionStage = 'hmis:PreAddressLine/@hmis:dataCollectionStage'
        xpLine1 = 'hmis:Line1'
        xpLine1DateCollected = 'hmis:Line1/@hmis:dateCollected'
        xpLine1DateEffective = 'hmis:Line1/@hmis:dateEffective'
        xpLine1DataCollectionStage = 'hmis:Line1/@hmis:dataCollectionStage'
        xpLine2 = 'hmis:Line2'
        xpLine2DateCollected = 'hmis:Line2/@hmis:dateCollected'
        xpLine2DateEffective = 'hmis:Line2/@hmis:dateEffective'
        xpLine2DataCollectionStage = 'hmis:Line2/@hmis:dataCollectionStage'
        xpCity = 'hmis:City'
        xpCityDateCollected = 'hmis:City/@hmis:dateCollected'
        xpCityDateEffective = 'hmis:City/@hmis:dateEffective'
        xpCityDataCollectionStage = 'hmis:City/@hmis:dataCollectionStage'
        xpCounty = 'hmis:County'
        xpCountyDateCollected = 'hmis:County/@hmis:dateCollected'
        xpCountyDateEffective = 'hmis:County/@hmis:dateEffective'
        xpCountyDataCollectionStage = 'hmis:County/@hmis:dataCollectionStage'
        xpState = 'hmis:State'
        xpStateDateCollected = 'hmis:State/@hmis:dateCollected'
        xpStateDateEffective = 'hmis:State/@hmis:dateEffective'
        xpStateDataCollectionStage = 'hmis:State/@hmis:dataCollectionStage'
        xpZIPCode = 'hmis:ZIPCode'
        xpZIPCodeDateCollected = 'hmis:ZIPCode/@hmis:dateCollected'
        xpZIPCodeDateEffective = 'hmis:ZIPCode/@hmis:dateEffective'
        xpZIPCodeDataCollectionStage = 'hmis:ZIPCode/@hmis:dataCollectionStage'
        xpCountry = 'hmis:Country'
        xpCountryDateCollected = 'hmis:Country/@hmis:dateCollected'
        xpCountryDateEffective = 'hmis:Country/@hmis:dateEffective'
        xpCountryDataCollectionStage = 'hmis:Country/@hmis:dataCollectionStage'
        xpIsLastPermanentZip = 'hmis:IsLastPermanentZIP'
        xpIsLastPermanentZIPDateCollected = 'hmis:IsLastPermanentZIP/@hmis:dateCollected'
        xpIsLastPermanentZIPDateEffective = 'hmis:IsLastPermanentZIP/@hmis:dateEffective'
        xpIsLastPermanentZIPDataCollectionStage = 'hmis:IsLastPermanentZIP/@hmis:dataCollectionStage'
        xpZipQualityCode = 'hmis:ZIPQualityCode'
        xpZIPQualityCodeDateCollected = 'hmis:ZIPQualityCode/@hmis:dateCollected'
        xpZIPQualityCodeDateEffective = 'hmis:ZIPQualityCode/@hmis:dateEffective'
        xpZIPQualityCodeDataCollectionStage = 'hmis:ZIPQualityCode/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.PersonAddress)
    
                ''' Parse sub-tables '''
                            

    def parse_other_names(self, element):
        ''' Element paths '''
        xpOtherNames = 'hmis:OtherNames'
        xpOtherFirstNameUnhashed = 'hmis:OtherFirstName/hmis:Unhashed'
        xpOtherFirstNameUnhashedDateCollected = 'hmis:OtherFirstName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherFirstNameUnhashedDateEffective = 'hmis:OtherFirstName/hmis:Unhashed/@hmis:dateEffective'
        xpOtherFirstNameUnhashedDataCollectionStage = 'hmis:OtherFirstName/hmis:Unhashed/@hmis:dataCollectionStage'

        xpOtherFirstNameHashed = 'hmis:OtherFirstName/hmis:Hashed'
        xpOtherFirstNameHashedDateCollected = 'hmis:OtherFirstName/hmis:Hashed/@hmis:dateCollected'
        xpOtherFirstNameHashedDateEffective = 'hmis:OtherFirstName/hmis:Hashed/@hmis:dateEffective'
        xpOtherFirstNameHashedDataCollectionStage = 'hmis:OtherFirstName/hmis:Hashed/@hmis:dataCollectionStage'

        xpOtherLastNameUnhashed = 'hmis:OtherLastName/hmis:Unhashed'
        xpOtherLastNameUnhashedDateCollected = 'hmis:OtherLastName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherLastNameUnhashedDateEffective = 'hmis:OtherLastName/hmis:Unhashed/@hmis:dateEffective'
        xpOtherLastNameUnhashedDataCollectionStage = 'hmis:OtherLastName/hmis:Unhashed/@hmis:dataCollectionStage'

        xpOtherLastNameHashed = 'hmis:OtherLastName/hmis:Hashed'
        xpOtherLastNameHashedDateCollected = 'hmis:OtherLastName/hmis:Hashed/@hmis:dateCollected'
        xpOtherLastNameHashedDateEffective = 'hmis:OtherLastName/hmis:Hashed/@hmis:dateEffective'
        xpOtherLastNameHashedDataCollectionStage = 'hmis:OtherLastName/hmis:Hashed/@hmis:dataCollectionStage'

        xpOtherMiddleNameUnhashed = 'hmis:OtherMiddleName/hmis:Unhashed'
        xpOtherMiddleNameUnhashedDateCollected = 'hmis:OtherMiddleName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherMiddleNameUnhashedDateEffective = 'hmis:OtherMiddleName/hmis:Unhashed/@hmis:dateEffective'
        xpOtherMiddleNameUnhashedDataCollectionStage = 'hmis:OtherMiddleName/hmis:Unhashed/@hmis:dataCollectionStage'

        xpOtherMiddleNameHashed = 'hmis:OtherMiddleName/hmis:Hashed'
        xpOtherMiddleNameHashedDateCollected = 'hmis:OtherMiddleName/hmis:Hashed/@hmis:dateCollected'
        xpOtherMiddleNameHashedDateEffective = 'hmis:OtherMiddleName/hmis:Hashed/@hmis:dateEffective'
        xpOtherMiddleNameHashedDataCollectionStage = 'hmis:OtherMiddleName/hmis:Hashed/@hmis:dataCollectionStage'

        xpOtherSuffixUnhashed = 'hmis:OtherSuffix/hmis:Unhashed'
        xpOtherSuffixUnhashedDateCollected = 'hmis:OtherSuffix/hmis:Unhashed/@hmis:dateCollected'
        xpOtherSuffixUnhashedDateEffective = 'hmis:OtherSuffix/hmis:Unhashed/@hmis:dateEffective'
        xpOtherSuffixUnhashedDataCollectionStage = 'hmis:OtherSuffix/hmis:Unhashed/@hmis:dataCollectionStage'

        xpOtherSuffixHashed = 'hmis:OtherSuffix/hmis:Hashed'
        xpOtherSuffixHashedDateCollected = 'hmis:OtherSuffix/hmis:Hashed/@hmis:dateCollected'
        xpOtherSuffixHashedDateEffective = 'hmis:OtherSuffix/hmis:Hashed/@hmis:dateEffective'
        xpOtherSuffixHashedDataCollectionStage = 'hmis:OtherSuffix/hmis:Hashed/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.OtherNames)
    
                ''' Parse sub-tables '''
                            

    def parse_races(self, element):
        ''' Element paths '''
        xpRaces = 'hmis:Race'
        xpRaceUnhashed = 'hmis:Unhashed'
        xpRaceUnhashedDateCollected = 'hmis:Unhashed/@hmis:dateCollected'
        xpRaceUnhashedDataCollectionStage = 'hmis:Unhashed/@hmis:dataCollectionStage'
        xpRaceHashed = 'hmis:Hashed'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Races)
    
                ''' Parse sub-tables '''
        
    def parse_funding_source(self, element):
        ''' Element paths '''
        xpFundingSource = 'hmis:FundingSources/hmis:FundingSource'
        xpFundingSourceIDIDNum = 'hmis:FundingSourceID/hmis:IDNum'
        xpFundingSourceIDIDStr = 'hmis:FundingSourceID/hmis:IDStr'
        xpFundingSourceIDDeleteOccurredDate = 'hmis:FundingSourceID/@hmis:deleteOccurredDate'
        xpFundingSourceIDDeleteEffective = 'hmis:FundingSourceID/@hmis:deleteEffective'
        xpFundingSourceIDDelete = 'hmis:FundingSourceID/@hmis:delete'
        xpFederalCFDA = 'hmis:FederalCFDA'
        xpReceivesMcKinneyFunding = 'hmis:ReceivesMcKinneyFunding'
        xpAdvanceOrArrears = 'hmis:AdvanceOrArrears'
        xpFinancialAssistanceAmount = 'hmis:FinancialAssistanceAmount'

        itemElements = element.xpath(xpFundingSource, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                self.existence_test_and_add('federal_cfda_number', item.xpath(xpFederalCFDA, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('receives_mckinney_funding', item.xpath(xpReceivesMcKinneyFunding, namespaces={'hmis': self.hmis_namespace}), 'text')

                ''' Foreign Keys '''
                try: self.existence_test_and_add('service_index_id', self.service_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('service_event_index_id', self.service_event_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.FundingSource)
    
                ''' Parse sub-tables '''
                            

    def parse_resource_info(self, element):
        ''' Element paths '''
        xpResourceInfo = 'airs:ResourceInfo'
        xpResourceSpecialist = 'airs:ResourceSpecialist'
        xpAvailableForDirectory = 'airs:AvailableForDirectory'
        xpAvailableForReferral = 'airs:AvailableForReferral'
        xpAvailableForResearch = 'airs:AvailableForResearch'
        xpDateAdded = 'airs:DateAdded'
        xpDateLastVerified = 'airs:DateLastVerified'
        xpDateOfLastAction = 'airs:DateOfLastAction'
        xpLastActionType = 'airs:LastActionType'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_service_index_id', self.site_service_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.ResourceInfo)
    
                ''' Parse sub-tables '''
                self.parse_contact(item)            
                self.parse_email(item)      
                self.parse_phone(item)      
            
    def parse_contact(self, element):
        ''' Element paths '''
        xpContact = 'airs:Contact'
        xpTitle = 'airs:Title'
        xpName = 'airs:Name'
        xpType = 'airs:Type'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('resource_info_index_id', self.resource_info_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Contact)
    
                ''' Parse sub-tables '''
                self.parse_email(item)      
                self.parse_phone(item)      

    def parse_email(self, element):
        ''' Element paths '''
        xpEmail = 'airs:Email'
        xpAddress = 'airs:Address'
        xpNote = 'airs:Note'
        xpPersonEmail = 'airs:PersonEmail'
        xpPersonEmailDateCollected = 'hmis:PersonEmail/@hmis:dateCollected'
        xpPersonEmailDateEffective = 'hmis:PersonEmail/@hmis:dateEffective'
        xpPersonEmailDataCollectionStage = 'hmis:PersonEmail/@hmis:dataCollectionStage'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('contact_index_id', self.contact_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('resource_info_index_id', self.resource_info_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Email)
    
                ''' Parse sub-tables '''
                            

    def parse_phone(self, element):
        ''' Element paths '''
        xpPhone = 'airs:Phone'
        xpPhoneNumber = 'airs:PhoneNumber'
        xpReasonWithheld = 'airs:ReasonWithheld'
        xpExtension = 'airs:Extension'
        xpDescription = 'airs:Description'
        xpType = 'airs:Type'
        xpFunction = 'airs:Function'
        xpTollFree = '@airs:TollFree'
        xpConfidential = '@airs:Confidential'

        itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''

                ''' Foreign Keys '''
                try: self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('contact_index_id', self.contact_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('resource_info_index_id', self.resource_info_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('site_index_id', self.site_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('service_index_id', self.service_index_id, 'no_handling')
                except: pass
                try: self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                except: pass
                                
                ''' Shred to database '''
                self.shred(self.parse_dict, DBObjects.Phone)
    
                ''' Parse sub-tables '''
                            

    ''' Build link/bridge tables '''
            
    def record_source_export_link(self):
        ''' record the link between source and export '''
        self.existence_test_and_add('source_index_id', self.source_index_id, 'no_handling')
        self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
        self.shred(self.parse_dict, DBObjects.SourceExportLink)
        return            

    def record_agency_child_link(self):
        ''' record the link between agency and any children '''
        self.existence_test_and_add('agency_index_id', self.agency_index_id, 'no_handling')
        self.existence_test_and_add('export_index_id', self.export_index_id, 'no_handling')
        self.shred(self.parse_dict, DBObjects.AgencyChild)
        return            

    ''' Utility methods '''
            
    def shred(self, parse_dict, mapping):
        ''' commits the record set to the database '''
        mapped = mapping(parse_dict)
        self.session.save(mapped)
        self.session.flush()
        
        ''' store foreign keys '''
        if mapping.__name__ == "Source":
            self.source_index_id = mapped.id
            print "Source:",self.source_index_id

        if mapping.__name__ == "Export":
            self.export_index_id = mapped.export_id
            print "Export:",self.export_index_id
            
        if mapping.__name__ == "Household":
            self.household_index_id = mapped.id
            print "Household:",self.household_index_id

        if mapping.__name__ == "Agency":
            self.agency_index_id = mapped.id
            print "Agency:",self.agency_index_id

        if mapping.__name__ == "Site":
            self.site_index_id = mapped.id
            print "Site:",self.site_index_id

        if mapping.__name__ == "SiteService":
            self.site_service_index_id = mapped.id
            print "SiteService:",self.site_service_index_id

        if mapping.__name__ == "PitCountSet":
            self.pit_count_set_index_id = mapped.id
            print "PitCountSet:",self.pit_count_set_index_id

        if mapping.__name__ == "Languages":
            self.languages_index_id = mapped.id
            print "Languages:",self.languages_index_id

        if mapping.__name__ == "Service":
            self.service_index_id = mapped.id
            print "Service:",self.service_index_id

        if mapping.__name__ == "HmisAsset":
            self.hmis_asset_index_id = mapped.id
            print "HmisAsset:",self.hmis_asset_index_id

        if mapping.__name__ == "Assignment":
            self.assignment_index_id = mapped.id
            print "Assignment:",self.assignment_index_id

        if mapping.__name__ == "Person":
            self.person_index_id = mapped.id
            print "Person:",self.person_index_id

        if mapping.__name__ == "SiteServiceParticipation":
            self.site_service_participation_index_id = mapped.id
            print "SiteServiceParticipation:",self.site_service_participation_index_id

        if mapping.__name__ == "Need":
            self.need_index_id = mapped.id
            print "Need:",self.need_index_id

        if mapping.__name__ == "ServiceEvent":
            self.service_event_index_id = mapped.id
            print "ServiceEvent:",self.service_event_index_id            
            
        if mapping.__name__ == "PersonHistorical":
            self.person_historical_index_id = mapped.id
            print "PersonHistorical:",self.person_historical_index_id                              
            
        if mapping.__name__ == "Degree":
            self.degree_index_id = mapped.id
            print "Degree:",self.degree_index_id                
            
        if mapping.__name__ == "ChildEnrollmentStatus":
            self.child_enrollment_status_index_id = mapped.id
            print "ChildEnrollmentStatus:",self.child_enrollment_status_index_id     
            
        if mapping.__name__ == "ResourceInfo":
            self.resource_info_index_id = mapped.id
            print "ResourceInfo:",self.resource_info_index_id               

        if mapping.__name__ == "Contact":
            self.contact_index_id = mapped.id
            print "Contact:",self.contact_index_id                                   
            
        if mapping.__name__ == "TimeOpen":
            self.time_open_index_id = mapped.id
            print "TimeOpen:",self.time_open_index_id   
                        
        self.session.commit()
        return
        
    def existence_test_and_add(self, db_column, query_string, handling):
        ''' Checks that the query actually has a result and adds to dictionary '''
        if handling == 'no_handling':
                self.persist(db_column, query_string = query_string)
                return True
        elif len(query_string) is not 0 or None:
            if handling == 'attribute_text':
                self.persist(db_column, query_string[0])
                return True
            if handling == 'text':
                self.persist(db_column, query_string = query_string[0].text)
                return True
            elif handling == 'attribute_date':
                self.persist(db_column, query_string = dateutil.parser.parse(query_string[0]))
                return True
            elif handling == 'element_date':
                self.persist(db_column, query_string = dateutil.parser.parse(query_string[0].text))
                return True
            else:
                print "Need to specify the handling"
                return False
        else:
            return False
            
    def persist(self, db_column, query_string):
        ''' Adds dictionary item with database column and associated data element '''
        self.parse_dict.__setitem__(db_column, query_string)
        return
        
def main(argv=None):  
    ''' Manually test this Reader class '''
    if argv is None:
        argv = sys.argv

    ## clear db tables (may have to run twice to get objects linked properly)
    import postgresutils
    UTILS = postgresutils.Utils()
    UTILS.blank_database()

    #inputFile = os.path.join("%s" % settings.BASE_PATH, "%s" % settings.INPUTFILES_PATH, "HUD_HMIS_3_0_Instance.xml")
    inputFile = "/mnt/mariah/HUD_HMIS_XML/HUD_HMIS_Instance.xml"
    
    if settings.DB_PASSWD == "":
        settings.DB_PASSWD = raw_input("Please enter your password: ")
    
    if os.path.isfile(inputFile) is True:#_adapted_further
        try:
            xml_file = open(inputFile,'r') 
        except:
            print "Error opening import file"
            
        reader = HMISXML30Reader(xml_file)
        tree = reader.read()
        reader.process_data(tree)
        xml_file.close()

if __name__ == "__main__":
    sys.exit(main())