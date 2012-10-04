''' 
    Reads a HUD HMIS XML 3.0 Document into memory and parses its contents storing them into a postgresql database.
    This is a log database, so it holds everything and doesn't worry about deduplication.
    The only thing it enforces are exportids, which must be unique.
'''

import sys, os
from reader import Reader
from zope.interface import implements
from lxml import etree
from conf import settings
import dbobjects
import hmisxml30reader

class TBCHUDHMISXML30Reader: 
    ''' Implements reader interface '''
    implements (Reader) 

    ''' Define XML namespaces '''
    hmis_namespace = "http://www.hmis.info/schema/3_0/HUD_HMIS.xsd" 
    airs_namespace = "http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd"
    tbc_namespace = "http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd"
    nsmap = {"hmis" : hmis_namespace, "airs" : airs_namespace, "ext" : tbc_namespace}


    def __init__(self, xml_file, db):
        ''' Put XML file into local object '''
        self.xml_file = xml_file
        ''' Instantiate database object '''
        self.session = db.Session()

    def read(self):
        ''' Takes an XML instance file and reads it into memory as a node tree '''

        tree = etree.parse(self.xml_file)
        return tree

    def process_data(self, tree):
        ''' Shreds the XML document into the database '''
        root_element = tree.getroot()
        source_ids = self.parse_source(root_element)
        return source_ids


    ''' Parse each table '''
    def parse_source(self, root_element):
        ''' Loop through all sources and then traverse the tree for each export '''
        ''' There can be multiple sources with multiple exports inside each source '''
        
        xpSources = '/ext:Sources/ext:Source'
        source_list = root_element.xpath(xpSources, namespaces = self.nsmap)
        if source_list is not None:
            source_ids = []
            for item in source_list:
                self.parse_dict = {}
                ''' Element paths '''
                xpSourceVersion = '../../@ext:version'                
                xpSourceIDIDNum = 'ext:SourceID/hmis:IDNum'
                xpSourceIDIDStr = 'ext:SourceID/hmis:IDStr'
                xpSourceDelete = 'ext:SourceID/@hmis:delete'
                xpSourceDeleteOccurredDate = 'ext:SourceID/@hmis:deleteOccurredDate'
                xpSourceDeleteEffective = 'ext:SourceID/@hmis:deleteEffective'
                xpSourceSoftwareVendor = 'ext:SoftwareVendor'
                xpSourceSoftwareVersion = 'ext:SoftwareVersion'
                xpSourceContactEmail = 'ext:SourceContactEmail'
                xpSourceContactExtension = 'ext:SourceContactExtension'
                xpSourceContactFirst = 'ext:SourceContactFirst'        
                xpSourceContactLast = 'ext:SourceContactLast'        
                xpSourceContactPhone = 'ext:SourceContactPhone'
                xpSourceName = 'ext:SourceName'
                #xp_source_exports = 'ext:Export'
                               
                ''' Map elements to database columns '''
                hmisxml30reader.existence_test_and_add(self, 'schema_version', item.xpath(xpSourceVersion, namespaces = self.nsmap), 'attribute_text')
                hmisxml30reader.existence_test_and_add(self, 'source_id_id_num', item.xpath(xpSourceIDIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_id_id_str', item.xpath(xpSourceIDIDStr, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_id_delete', item.xpath(xpSourceDelete, namespaces = self.nsmap), 'attribute_text')
                hmisxml30reader.existence_test_and_add(self, 'source_id_delete_occurred_date', item.xpath(xpSourceDeleteOccurredDate, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'source_id_delete_effective', item.xpath(xpSourceDeleteEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'software_vendor', item.xpath(xpSourceSoftwareVendor, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'software_version', item.xpath(xpSourceSoftwareVersion, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_contact_email', item.xpath(xpSourceContactEmail, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_contact_extension', item.xpath(xpSourceContactExtension, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_contact_first', item.xpath(xpSourceContactFirst, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_contact_last', item.xpath(xpSourceContactLast, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_contact_phone', item.xpath(xpSourceContactPhone, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'source_name', item.xpath(xpSourceName, namespaces = self.nsmap), 'text')
                source_id_str = item.xpath(xpSourceIDIDStr, namespaces = self.nsmap)
                source_id_num = item.xpath(xpSourceIDIDNum, namespaces = self.nsmap)

                #if source_id_str is not None:
                if len(source_id_str) == 1:
                    #source_id = source_id_str[0].text 
                    hmisxml30reader.existence_test_and_add(self, 'source_id', source_id_str, 'text')

                #elif source_id_num is not None:
                elif len(source_id_num) == 1:
                    #source_id = source_id_num[0].text 
                    hmisxml30reader.existence_test_and_add(self, 'source_id', source_id_num, 'text')

                ''' Shred to database '''
                source_id = hmisxml30reader.shred(self, self.parse_dict, dbobjects.Source)
                if source_id != None:
                    source_ids.append(source_id)

                ''' Parse all exports for this specific source '''
                self.parse_export(item)
        return source_ids

    def parse_export(self, element):
        ''' loop through all exports and traverse the tree '''
        
        ''' Element paths '''
        xpExport = 'ext:Export'
        xpExportIDIDNum = 'ext:ExportID/hmis:IDNum'
        xpExportIDIDStr = 'ext:ExportID/hmis:IDStr'
        xpExportDelete = 'ext:ExportID/@hmis:Delete'
        xpExportDeleteOccurredDate = 'ext:ExportID/@hmis:DeleteOccurredDate'
        xpExportDeleteEffective = 'ext:ExportID/@hmis:DeleteEffective'
        xpExportExportDate = 'ext:ExportDate'
        xpExportPeriodStartDate = 'ext:ExportPeriod/hmis:StartDate'
        xpExportPeriodEndDate = 'ext:ExportPeriod/hmis:EndDate'
        
        itemElements = element.xpath(xpExport, namespaces = self.nsmap)
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}

                ''' Map elements to database columns '''
                test = item.xpath(xpExportIDIDNum, namespaces = self.nsmap) 
                if len(test) is 0:
                    test = item.xpath(xpExportIDIDStr, namespaces = self.nsmap)
                    self.export_id = test
                    hmisxml30reader.existence_test_and_add(self, 'export_id', test, 'text')
                else:
                    self.export_id = test
                    hmisxml30reader.existence_test_and_add(self, 'export_id', test, 'text')
                hmisxml30reader.existence_test_and_add(self, 'export_id_id_num', item.xpath(xpExportIDIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'export_id_id_str', item.xpath(xpExportIDIDStr, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'export_id_delete', item.xpath(xpExportDelete, namespaces = self.nsmap), 'attribute_text')
                hmisxml30reader.existence_test_and_add(self, 'export_id_delete_occurred_date', item.xpath(xpExportDeleteOccurredDate, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'export_id_delete_effective', item.xpath(xpExportDeleteEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'export_date', item.xpath(xpExportExportDate, namespaces = self.nsmap), 'element_date') 
                hmisxml30reader.existence_test_and_add(self, 'export_period_start_date', item.xpath(xpExportPeriodStartDate, namespaces = self.nsmap), 'element_date')
                hmisxml30reader.existence_test_and_add(self, 'export_period_end_date', item.xpath(xpExportPeriodEndDate, namespaces = self.nsmap), 'element_date')

                ''' Shred to database '''
                hmisxml30reader.shred(self, self.parse_dict, dbobjects.Export)
                
                ''' Create source to export link '''
                hmisxml30reader.record_source_export_link(self)

                ''' Parse sub-tables '''
                hmisxml30reader.parse_household(self, item)
                hmisxml30reader.parse_region(self, item)
                hmisxml30reader.parse_agency(self, item)
                self.parse_person(item)
                hmisxml30reader.parse_service(self, item)
                hmisxml30reader.parse_site(self, item)
                hmisxml30reader.parse_site_service(self, item)
        return
               
    def parse_person(self, element):
        ''' Element paths '''
        xpPerson = 'ext:Person'
        xpPersonIDNum = 'ext:PersonID/hmis:IDNum'
        xpPersonIDStr = 'ext:PersonID/hmis:IDStr'
        xpPersonIDDeleteOccurredDate = 'ext:PersonID/@hmis:DeleteOccurredDate'
        xpPersonIDDeleteEffective = 'ext:PersonID/@hmis:DeleteEffective'
        xpPersonDelete = 'ext:PersonID/@hmis:Delete'
        xpPersonDateOfBirthHashed = 'ext:DateOfBirth/hmis:Hashed'
        xpPersonDateOfBirthHashedDateCollected = 'ext:DateOfBirth/hmis:Hashed/@hmis:dateCollected'
        xpPersonDateOfBirthUnhashed = 'ext:DateOfBirth/hmis:Unhashed'
        xpPersonDateOfBirthUnhashedDateCollected = 'ext:DateOfBirth/hmis:Unhashed/@hmis:dateCollected'
        xpPersonDateOfBirthType = 'ext:DateOfBirth/hmis:DateOfBirthType'
        xpPersonDateOfBirthTypeDateCollected = 'ext:DateOfBirth/hmis:DateOfBirthType/@hmis:dateCollected'
        xpPersonEthnicityHashedDateCollected = 'ext:Ethnicity/hmis:Hashed/@hmis:dateCollected'
        xpPersonEthnicityUnhashedDateCollected = 'ext:Ethnicity/hmis:Unhashed/@hmis:dateCollected'
        xpPersonEthnicityHashed = 'ext:Ethnicity/hmis:Hashed'
        xpPersonEthnicityUnhashed = 'ext:Ethnicity/hmis:Unhashed'
        xpPersonGenderHashed = 'ext:Gender/hmis:Hashed'
        xpPersonGenderUnhashed = 'ext:Gender/hmis:Unhashed'
        xpPersonGenderHashedDateCollected = 'ext:Gender/hmis:Hashed/@hmis:dateCollected'
        xpPersonGenderUnhashedDateCollected = 'ext:Gender/hmis:Unhashed/@hmis:dateCollected'        
        xpPersonGenderHashedDateEffective = 'ext:Gender/hmis:Hashed/@hmis:dateEffective'
        xpPersonGenderUnhashedDateEffective = 'ext:Gender/hmis:Unhashed/@hmis:dateEffective'                
        xpPersonLegalFirstNameHashed = 'ext:LegalFirstName/hmis:Hashed'
        xpPersonLegalFirstNameUnhashed = 'ext:LegalFirstName/hmis:Unhashed'
        xpPersonLegalFirstNameHashedDateEffective = 'ext:LegalFirstName/hmis:Hashed/@hmis:dateEffective'
        xpPersonLegalFirstNameUnhashedDateEffective = 'ext:LegalFirstName/hmis:Unhashed/@hmis:dateEffective'        
        xpPersonLegalFirstNameHashedDateCollected = 'ext:LegalFirstName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalFirstNameUnhashedDateCollected = 'ext:LegalFirstName/hmis:Unhashed/@hmis:dateCollected'        
        xpPersonLegalLastNameHashed = 'ext:LegalLastName/hmis:Hashed'
        xpPersonLegalLastNameUnhashed = 'ext:LegalLastName/hmis:Unhashed'
        xpPersonLegalLastNameHashedDateEffective = 'ext:LegalLastName/hmis:Hashed/@hmis:dateEffective'
        xpPersonLegalLastNameUnhashedDateEffective = 'ext:LegalLastName/hmis:Unhashed/@hmis:dateEffective'        
        xpPersonLegalLastNameHashedDateCollected = 'ext:LegalLastName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalLastNameUnhashedDateCollected = 'ext:LegalLastName/hmis:Unhashed/@hmis:dateCollected'        
        xpPersonLegalMiddleNameHashed = 'ext:LegalMiddleName/hmis:Hashed'
        xpPersonLegalMiddleNameUnhashed = 'ext:LegalMiddleName/hmis:Unhashed'
        xpPersonLegalMiddleNameHashedDateEffective = 'ext:LegalMiddleName/hmis:Hashed/@hmis:dateEffective'
        xpPersonLegalMiddleNameUnhashedDateEffective = 'ext:LegalMiddleName/hmis:Unhashed/@hmis:dateEffective'        
        xpPersonLegalMiddleNameHashedDateCollected = 'ext:LegalMiddleName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalMiddleNameUnhashedDateCollected = 'ext:LegalMiddleName/hmis:Unhashed/@hmis:dateCollected'        
        xpPersonLegalSuffixHashed = 'ext:LegalSuffix/hmis:Hashed'
        xpPersonLegalSuffixUnhashed = 'ext:LegalSuffix/hmis:Unhashed'
        xpPersonLegalSuffixHashedDateEffective = 'ext:LegalSuffix/hmis:Hashed/@hmis:dateEffective'
        xpPersonLegalSuffixUnhashedDateEffective = 'ext:LegalSuffix/hmis:Unhashed/@hmis:dateEffective'        
        xpPersonLegalSuffixHashedDateCollected = 'ext:LegalSuffix/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalSuffixUnhashedDateCollected = 'ext:LegalSuffix/hmis:Unhashed/@hmis:dateCollected'        
        xpPersonSocialSecurityNumberHashed = 'ext:SocialSecurityNumber/hmis:Hashed'
        xpPersonSocialSecurityNumberUnhashed = 'ext:SocialSecurityNumber/hmis:Unhashed'
        xpPersonSocialSecurityNumberHashedDateCollected = 'ext:SocialSecurityNumber/hmis:Hashed/@hmis:dateCollected'
        xpPersonSocialSecurityNumberUnhashedDateCollected = 'ext:SocialSecurityNumber/hmis:Unhashed/@hmis:dateCollected'
        xpPersonSocialSecurityNumberHashedDateEffective = 'ext:SocialSecurityNumber/hmis:Hashed/@hmis:dateEffective'
        xpPersonSocialSecurityNumberUnhashedDateEffective = 'ext:SocialSecurityNumber/hmis:Unhashed/@hmis:dateEffective' 
        xpPersonSocialSecurityNumberQualityCode = 'ext:SocialSecurityNumber/hmis:SocialSecNumberQualityCode'
        xpPersonSocialSecurityNumberQualityCodeDateEffective = 'ext:SocialSecurityNumber/hmis:SocialSecNumberQualityCode/@hmis:dateEffective'
        xpPersonSocialSecurityNumberQualityCodeDateCollected = 'ext:SocialSecurityNumber/hmis:SocialSecNumberQualityCode/@hmis:dateCollected' 

        itemElements = element.xpath(xpPerson, namespaces = self.nsmap)
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                hmisxml30reader.existence_test_and_add(self, 'person_id_id_num', item.xpath(xpPersonIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_id_id_str', item.xpath(xpPersonIDStr, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_id_delete_occurred_date', item.xpath(xpPersonIDDeleteOccurredDate, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_id_delete_effective', item.xpath(xpPersonIDDeleteEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_id_delete', item.xpath(xpPersonDelete, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_date_of_birth_hashed', item.xpath(xpPersonDateOfBirthHashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_date_of_birth_hashed_date_collected', item.xpath(xpPersonDateOfBirthHashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_date_of_birth_unhashed', item.xpath(xpPersonDateOfBirthUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_date_of_birth_unhashed_date_collected', item.xpath(xpPersonDateOfBirthUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_date_of_birth_type', item.xpath(xpPersonDateOfBirthType, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_date_of_birth_type_date_collected', item.xpath(xpPersonDateOfBirthTypeDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_ethnicity_hashed', item.xpath(xpPersonEthnicityHashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_ethnicity_unhashed', item.xpath(xpPersonEthnicityUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_ethnicity_unhashed_date_collected', item.xpath(xpPersonEthnicityUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_ethnicity_hashed_date_collected', item.xpath(xpPersonEthnicityHashedDateCollected, namespaces = self.nsmap), 'attribute_date')                                
                hmisxml30reader.existence_test_and_add(self, 'person_gender_hashed', item.xpath(xpPersonGenderHashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_gender_unhashed', item.xpath(xpPersonGenderUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_gender_unhashed_date_collected', item.xpath(xpPersonGenderUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_gender_hashed_date_collected', item.xpath(xpPersonGenderHashedDateCollected, namespaces = self.nsmap), 'attribute_date')                                                
                hmisxml30reader.existence_test_and_add(self, 'person_gender_unhashed_date_effective', item.xpath(xpPersonGenderUnhashedDateEffective, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_gender_hashed_date_effective', item.xpath(xpPersonGenderHashedDateEffective, namespaces = self.nsmap), 'attribute_date')                                                                
                hmisxml30reader.existence_test_and_add(self, 'person_legal_first_name_hashed', item.xpath(xpPersonLegalFirstNameHashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_first_name_unhashed', item.xpath(xpPersonLegalFirstNameUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_first_name_hashed_date_collected', item.xpath(xpPersonLegalFirstNameHashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_first_name_unhashed_date_collected', item.xpath(xpPersonLegalFirstNameUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_first_name_hashed_date_effective', item.xpath(xpPersonLegalFirstNameHashedDateEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_first_name_unhashed_date_effective', item.xpath(xpPersonLegalFirstNameUnhashedDateEffective, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_legal_last_name_hashed', item.xpath(xpPersonLegalLastNameHashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_last_name_unhashed', item.xpath(xpPersonLegalLastNameUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_last_name_hashed_date_collected', item.xpath(xpPersonLegalLastNameHashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_last_name_unhashed_date_collected', item.xpath(xpPersonLegalLastNameUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_legal_last_name_hashed_date_effective', item.xpath(xpPersonLegalLastNameHashedDateEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_last_name_unhashed_date_effective', item.xpath(xpPersonLegalLastNameUnhashedDateEffective, namespaces = self.nsmap), 'attribute_date')                                
                hmisxml30reader.existence_test_and_add(self, 'person_legal_middle_name_hashed', item.xpath(xpPersonLegalMiddleNameHashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_middle_name_unhashed', item.xpath(xpPersonLegalMiddleNameUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_middle_name_hashed_date_collected', item.xpath(xpPersonLegalMiddleNameHashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_middle_name_unhashed_date_collected', item.xpath(xpPersonLegalMiddleNameUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_legal_middle_name_hashed_date_effective', item.xpath(xpPersonLegalMiddleNameHashedDateEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_middle_name_unhashed_date_effective', item.xpath(xpPersonLegalMiddleNameUnhashedDateEffective, namespaces = self.nsmap), 'attribute_date')                                           
                hmisxml30reader.existence_test_and_add(self, 'person_legal_suffix_hashed', item.xpath(xpPersonLegalSuffixHashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_suffix_unhashed', item.xpath(xpPersonLegalSuffixUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_suffix_hashed_date_collected', item.xpath(xpPersonLegalSuffixHashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_suffix_unhashed_date_collected', item.xpath(xpPersonLegalSuffixUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_legal_suffix_hashed_date_effective', item.xpath(xpPersonLegalSuffixHashedDateEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_legal_suffix_unhashed_date_effective', item.xpath(xpPersonLegalSuffixUnhashedDateEffective, namespaces = self.nsmap), 'attribute_date')                                           
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_unhashed', item.xpath(xpPersonSocialSecurityNumberUnhashed, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_hashed', item.xpath(xpPersonSocialSecurityNumberHashed, namespaces = self.nsmap), 'text')                
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_hashed_date_collected', item.xpath(xpPersonSocialSecurityNumberHashedDateCollected, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_unhashed_date_collected', item.xpath(xpPersonSocialSecurityNumberUnhashedDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_hashed_date_effective', item.xpath(xpPersonSocialSecurityNumberHashedDateEffective, namespaces = self.nsmap), 'attribute_date')                
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_unhashed_date_effective', item.xpath(xpPersonSocialSecurityNumberUnhashedDateEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_quality_code', item.xpath(xpPersonSocialSecurityNumberQualityCode, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_quality_code_date_effective', item.xpath(xpPersonSocialSecurityNumberQualityCodeDateEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'person_social_security_number_quality_code_date_collected', item.xpath(xpPersonSocialSecurityNumberQualityCodeDateCollected, namespaces = self.nsmap), 'attribute_date')
                
                ''' Foreign Keys '''
                hmisxml30reader.existence_test_and_add(self, 'export_index_id', self.export_index_id, 'no_handling')
                
                ''' Shred to database '''
                hmisxml30reader.shred(self, self.parse_dict, dbobjects.Person)
    
                ''' Parse sub-tables '''
                hmisxml30reader.parse_site_service_participation(self, item)
                hmisxml30reader.parse_need(self, item, 'ext:')
                print '====', self, item
                self.parse_service_event(item)  #(self, item)
                hmisxml30reader.parse_person_historical(self, item, pf = 'ext:')
                hmisxml30reader.parse_release_of_information(self, item)
                hmisxml30reader.parse_other_names(self, item)
                hmisxml30reader.parse_races(self, item, pf = 'ext:')

    def parse_service_event(self, element):
        
        ''' Element paths '''
        xpServiceEvent = 'ext:ServiceEvent'
        xpServiceEventIDIDNum = 'ext:ServiceEventID/hmis:IDNum'
        xpServiceEventIDIDStr = 'ext:ServiceEventID/hmis:IDStr'
        xpServiceEventIDDeleteOccurredDate = 'ext:ServiceEventID/@hmis:deleteOccurredDate'
        xpServiceEventIDDeleteEffective = 'ext:ServiceEventID/@hmis:deleteEffective'
        xpServiceEventIDDelete = 'ext:ServiceEventID/@hmis:delete'        
        xpSiteServiceID = 'ext:SiteServiceID'
        xpHouseholdIDIDNum = 'ext:HouseholdID/hmis:IDNum'
        xpHouseholdIDIDStr = 'ext:HouseholdID/hmis:IDStr'
        xpIsReferral = 'ext:IsReferral'
        xpQuantityOfServiceEvent = 'ext:QuantityOfServiceEvent'
        xpQuantityOfServiceEventUnit = 'ext:QuantityOfServiceEventUnit'
        #TODO: xpReferralsReferralNeedTaxonomy* = '' -> airs namespace No, it goes in standard Need/Taxonomy tables
        xpServiceEventAIRSCode = 'ext:ServiceEventAIRSCode'
        xpServiceEventEffectivePeriodStartDate = 'ext:ServiceEventEffectivePeriod/hmis:StartDate'
        xpServiceEventEffectivePeriodEndDate = 'ext:ServiceEventEffectivePeriod/hmis:EndDate'
        xpServiceEventProvisionDate = 'ext:ServiceEventProvisionDate'
        xpServiceEventRecordedDate = 'ext:ServiceEventRecordedDate'
        xpServiceEventIndFam = 'ext:ServiceEventIndFam'
        xpHMISServiceEventCodeTypeOfService = 'ext:HMISServiceEventCode/hmis:TypeOfService'
        xpHMISServiceEventCodeTypeOfServiceOther = 'ext:HMISServiceEventCode/hmis:TypeOfServiceOther'
        xpHPRPFinancialAssistanceServiceEventCode = 'ext:HPRPFinancialAssistanceService'
        xpHPRPRelocationStabilizationServiceEventCode = 'ext:HPRPRelocationStabilizationServiceEventCode'
        
        itemElements = element.xpath(xpServiceEvent, namespaces = self.nsmap)
        if itemElements is not None:
            for item in itemElements:
                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                hmisxml30reader.existence_test_and_add(self, 'service_event_idid_num', item.xpath(xpServiceEventIDIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'service_event_idid_str', item.xpath(xpServiceEventIDIDStr, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'service_event_id_delete_occurred_date', item.xpath(xpServiceEventIDDeleteOccurredDate, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'service_event_id_delete_effective_date', item.xpath(xpServiceEventIDDeleteEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'service_event_id_delete', item.xpath(xpServiceEventIDDelete, namespaces = self.nsmap), 'attribute_text')      
                hmisxml30reader.existence_test_and_add(self, 'site_service_id', item.xpath(xpSiteServiceID, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'household_idid_num', item.xpath(xpHouseholdIDIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'household_idid_str', item.xpath(xpHouseholdIDIDStr, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'is_referral', item.xpath(xpIsReferral, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'quantity_of_service', item.xpath(xpQuantityOfServiceEvent, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'quantity_of_service_measure', item.xpath(xpQuantityOfServiceEventUnit, namespaces = self.nsmap), 'text')

                #TODO: hmisxml30reader.existence_test_and_add(xpReferralsReferralNeedTaxonomy*) -> airs namespace, No
                
                hmisxml30reader.existence_test_and_add(self, 'service_airs_code', item.xpath(xpServiceEventAIRSCode, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'service_period_start_date', item.xpath(xpServiceEventEffectivePeriodStartDate, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'service_period_end_date', item.xpath(xpServiceEventEffectivePeriodEndDate, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'service_event_provision_date', item.xpath(xpServiceEventProvisionDate, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'service_event_recorded_date', item.xpath(xpServiceEventRecordedDate, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'service_event_ind_fam', item.xpath(xpServiceEventIndFam, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'hmis_service_event_code_type_of_service', item.xpath(xpHMISServiceEventCodeTypeOfService, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'hmis_service_event_code_type_of_service_other', item.xpath(xpHMISServiceEventCodeTypeOfServiceOther, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'hprp_financial_assistance_service_event_code', item.xpath(xpHPRPFinancialAssistanceServiceEventCode, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'hprp_relocation_stabilization_service_event_code', item.xpath(xpHPRPRelocationStabilizationServiceEventCode, namespaces = self.nsmap), 'text')

                ''' Foreign Keys '''
                try: hmisxml30reader.existence_test_and_add(self, 'export_index_id', self.export_index_id, 'no_handling')
                except: pass
                try: hmisxml30reader.existence_test_and_add(self, 'person_index_id', self.person_index_id, 'no_handling')
                except: pass
                try: hmisxml30reader.existence_test_and_add(self, 'need_index_id', self.need_index_id, 'no_handling')
                except: pass
                try: hmisxml30reader.existence_test_and_add(self, 'site_service_participation_index_id', self.site_service_participation_index_id, 'no_handling')
                except: pass
                
                ''' Shred to database '''
                hmisxml30reader.shred(self, self.parse_dict, dbobjects.ServiceEvent)

                ''' Parse sub-tables '''
                #TODO: check schema to see if these need to be extended
                hmisxml30reader.parse_service_event_notes(self, item, pf='ext:')     
                #hmisxml30reader.parse_funding_source(self, item)    # Not in test xml
                self.parse_referral(item)   #(self, item)


    def parse_referral(self, element):
        
        ''' Element paths '''
        xpReferrals = 'ext:Referrals/ext:Referral'
        xpReferralsReferralIDIDNum = 'ext:ReferralID/hmis:IDNum'
        xpReferralsReferralIDIDStr = 'ext:ReferralID/hmis:IDStr'
        xpReferralsReferralDelete = 'ext:ReferralID/@hmis:delete'
        xpReferralsReferralDeleteOccurredDate = 'ext:ReferralID/@hmis:deleteOccurredDate'
        xpReferralsReferralDeleteEffective = 'ext:ReferralID/@hmis:deleteEffective'
        xpReferralsReferralAgencyReferredToIDIDNum = 'ext:AgencyReferredToID/hmis:IDNum'
        xpReferralsReferralAgencyReferredToIDIDStr = 'ext:AgencyReferredToID/hmis:IDStr'
        xpReferralsReferralAgencyReferredToName = 'ext:AgencyReferredToName'
        xpReferralsReferralAgencyReferredToNameDataCollectionStage = 'ext:AgencyReferredToName/@hmis:dataCollectionStage'
        xpReferralsReferralAgencyReferredToNameDateCollected = 'ext:AgencyReferredToName/@hmis:dateCollected'
        xpReferralsReferralAgencyReferredToNameDateEffective = 'ext:AgencyReferredToName/@hmis:dateEffective'
        xpReferralsReferralNeedIDIDNum = 'ext:NeedID/hmis:IDNum'    # Points to Standalone Need 
        xpReferralsReferralNeedIDIDStr = 'ext:NeedID/hmis:IDStr'    # defined earlier in ext:Person/ext:Need
        
        itemElements = element.xpath(xpReferrals, namespaces = self.nsmap)
        if itemElements is not None:
            for item in itemElements:

                # Need to parse nested "Need" before put referral in DB, so we have the correct "self.need_index_id" (set in shred())
                hmisxml30reader.parse_need(self, item, pf='ext:')   # For nested Need

                dataToFind = item.xpath(xpReferralsReferralNeedIDIDNum,namespaces = self.nsmap)  # Returns: Element list
                if dataToFind == []:    # No <hmis:IDNum>. Means there is no standalone need to refer to. Need must be nested.
                    currentNeedID = self.need_index_id  # Just shredded above...
                else:   # Need was parsed (much) earlier, so have to look up Need.id
                    ididToSearch = dataToFind[0].text
                    relNeed = self.session.query(dbobjects.Need).filter(dbobjects.Need.need_idid_num == ididToSearch).one()
                    #print "======== Need:", relNeed.id, relNeed.site_service_idid_num, relNeed.need_idid_num, relNeed.person_index_id
                    currentNeedID = relNeed.id

                self.parse_dict = {}
                
                ''' Map elements to database columns '''
                hmisxml30reader.existence_test_and_add(self, 'referral_idid_num', item.xpath(xpReferralsReferralIDIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'referral_idid_str', item.xpath(xpReferralsReferralIDIDStr, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'referral_delete', item.xpath(xpReferralsReferralDelete, namespaces = self.nsmap), 'attribute_text')
                hmisxml30reader.existence_test_and_add(self, 'referral_delete_occurred_date', item.xpath(xpReferralsReferralDeleteOccurredDate, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'referral_delete_effective_date', item.xpath(xpReferralsReferralDeleteEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'referral_agency_referred_to_idid_num', item.xpath(xpReferralsReferralAgencyReferredToIDIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'referral_agency_referred_to_idid_str', item.xpath(xpReferralsReferralAgencyReferredToIDIDStr, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'referral_agency_referred_to_name', item.xpath(xpReferralsReferralAgencyReferredToName, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'referral_agency_referred_to_name_data_collection_stage', item.xpath(xpReferralsReferralAgencyReferredToNameDataCollectionStage, namespaces = self.nsmap), 'attribute_text')
                hmisxml30reader.existence_test_and_add(self, 'referral_agency_referred_to_name_date_collected', item.xpath(xpReferralsReferralAgencyReferredToNameDateCollected, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'referral_agency_referred_to_name_date_effective', item.xpath(xpReferralsReferralAgencyReferredToNameDateEffective, namespaces = self.nsmap), 'attribute_date')
                hmisxml30reader.existence_test_and_add(self, 'referral_need_idid_num', item.xpath(xpReferralsReferralNeedIDIDNum, namespaces = self.nsmap), 'text')
                hmisxml30reader.existence_test_and_add(self, 'referral_need_idid_str', item.xpath(xpReferralsReferralNeedIDIDStr, namespaces = self.nsmap), 'text')

                ''' Foreign Keys '''
                try: hmisxml30reader.existence_test_and_add(self, 'export_index_id', self.export_index_id, 'no_handling')
                except: pass
                try: hmisxml30reader.existence_test_and_add(self, 'person_index_id', self.person_index_id, 'no_handling')
                except: pass
                # In TBC, self.need_index_id might be bogus cuz need isn't a parent? or might need to be looked up with NeedIDIDNum?
                #try: hmisxml30reader.existence_test_and_add(self, 'need_index_id', self.need_index_id, 'no_handling')
                try: hmisxml30reader.existence_test_and_add(self, 'need_index_id', currentNeedID, 'no_handling')
                except: pass
                try: hmisxml30reader.existence_test_and_add(self, 'service_event_index_id', self.service_event_index_id, 'no_handling')
                except: pass
                #print '==== need_index_id - self:', self.need_index_id
                ''' Shred to database '''
                hmisxml30reader.shred(self, self.parse_dict, dbobjects.Referral)

                ''' Parse sub-tables '''
            # Need to parse the "Need" before the "Referral" so we have the correct "need_index_id"
            #    hmisxml30reader.parse_need(self, item, pf='ext:')   # For nested Need
            #    print '==== need_index_id - self:', self.need_index_id

def main(argv=None):  
    ''' Manually test this Reader class '''
    if argv is None:
        argv = sys.argv

    ## clear db tables (may have to run twice to get objects linked properly)
    import postgresutils
    UTILS = postgresutils.Utils()
    UTILS.blank_database()
    db = dbobjects.DB()
    print "Session = ", db.Session()

    #inputFile = os.path.join("%s" % settings.BASE_PATH, "%s" % settings.INPUTFILES_PATH, "HUD_HMIS_3_0_Instance.xml")
    inputFile = "/home/synthesis/myrestservice/synthesis/synthesis/test_files/HUD_HMIS_TBC.xml"
    
    if settings.DB_PASSWD == "":
        settings.DB_PASSWD = raw_input("Please enter your password: ")
    
    if os.path.isfile(inputFile) is True:#_adapted_further
        try:
            xml_file = open(inputFile,'r') 
        except:
            print "Error opening import file"
            
        reader = TBCHUDHMISXML30Reader(xml_file, db)
        #reader.source_index_id = 1
        #reader.export_index_id = 1
        tree = reader.read()
        reader.process_data(tree)
        #xml_file.close()
    print "my reader is now exiting"

if __name__ == "__main__":
    sys.exit(main())
