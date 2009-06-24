'''reads an HMIS XML Document into memory and parses its contents\n
storing them into a postgresql database.  This is a log database, so it holds 
everything and doesn't worry about deduplication.  The only thing it enforces 
are exportids, which must be unique.'''
import sys, os
from reader import Reader
from zope.interface import implements
from lxml import etree
from sqlalchemy import create_engine, Table, Column, Numeric, Integer, String, Boolean, MetaData, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, mapper, backref, relation
from sqlalchemy.types import DateTime, Date
import dateutil.parser
#import logging
import settings

class HMISXML28Reader:
    '''Implements reader interface.'''
    implements (Reader) 
    
    hmis_namespace = "http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd" 
    airs_namespace = "http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd"
    nsmap = {"hmis" : hmis_namespace, "airs" : airs_namespace}

    def __init__(self, xml_file):
        self.pg_db = create_engine('postgres://%s:%s@localhost:5432/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_DATABASE) , echo=True)#, server_side_cursors=True)
        #self.sqlite_db = create_engine('sqlite:///:memory:', echo=True)
        self.xml_file = xml_file
        self.db_metadata = MetaData(self.pg_db)
        #self.db_metadata = MetaData(self.sqlite_db)
        Session = sessionmaker(bind=self.pg_db, autoflush=True, transactional=True)
        #Session = sessionmaker(bind=self.sqlite_db, autoflush=True, transactional=True)
        
        self.session = Session()
        #logging.basicConfig(filename='./sql.log')
        #logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG) 
        
        self.export_map()
        self.database_map()
        self.person_map()
        self.person_historical_map()
        self.other_names_map()
        self.races_map()
        
        #only client information needed for this project
        #self.site_service_map()
        
    def read(self):
        '''Takes an XML instance file and reads it into \n
        memory as a node tree.'''
        #print 'inside read', self.xml_file
        tree = etree.parse(self.xml_file)
        return tree
        
    def process_data(self, tree):
        '''Shreds the XML document into the database.'''
        root_element = tree.getroot()
        self.parse_export(root_element)
        #test join
        #for u,a in self.session.query(Person, Export).filter(Person.export_id==Export.export_id): 
        #    print 'Person', u.export_id, 'Export', a.export_software_version
        return
    
    def database_map(self):
        '''Set up mapping'''
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=False)
        self.database_table = Table(
        'database', 
        table_metadata, 
        Column('id', Integer, primary_key=True),
        Column('export_id', String(50), ForeignKey(Export.c.export_id)), 
        Column('database_id', String(50)), 
        Column('database_id_date_collected', DateTime(timezone=True)),
        Column('database_email', String(50)),
        Column('database_email_date_collected', DateTime(timezone=True)),
        Column('database_contact_extension', String(10)),
        Column('database_contact_extension_date_collected', DateTime(timezone=True)),
        Column('database_contact_last', String(20)),
        Column('database_contact_last_date_collected', DateTime(timezone=True)),
        Column('database_contact_phone', String(20)),
        Column('database_contact_phone_date_collected', DateTime(timezone=True)),
        Column('database_name', String(50)),
        Column('database_name_date_collected', DateTime(timezone=True)), 
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Database, self.database_table)
#        assign_mapper(Database, database_table, properties=dict(
#designs=relation(Design, private=True, backref="type")
#))
        return
    
    def export_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=True)
        export_table = Table(
        'export', 
        table_metadata, 
        Column('export_id', String(50), primary_key=True), 
        Column('export_id_date_collected', DateTime(timezone=True)),
        Column('export_date', DateTime(timezone=True)),
        Column('export_date_date_collected', DateTime(timezone=True)),
        Column('export_period_start_date', DateTime(timezone=True)),
        Column('export_period_start_date_date_collected', DateTime(timezone=True)),
        Column('export_period_end_date', DateTime(timezone=True)),
        Column('export_period_end_date_date_collected', DateTime(timezone=True)),
        Column('export_software_vendor', String(50)),
        Column('export_software_vendor_date_collected', DateTime(timezone=True)),
        Column('export_software_version', String(10)),
        Column('export_software_version_date_collected', DateTime(timezone=True)),
        useexisting = True
        )
        table_metadata.create_all()
        #mapper(Export, export_table, properties={'children': [relation(Person), relation(Database)]})
        mapper(Export, export_table, properties={'children': relation(Person), 'children': relation(Database)})
        return
    
    def other_names_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=False)
        other_names_table = Table(
        'other_names', 
        table_metadata, 
        Column('id', Integer, primary_key=True),
        Column('person_index_id', Integer, ForeignKey(Person.c.id)), 
        Column('other_first_name_unhashed', String(50)),
        Column('other_first_name_hashed', String(32)),
        Column('other_first_name_date_collected', DateTime(timezone=True)),
        Column('other_middle_name_unhashed', String(50)),
        Column('other_middle_name_hashed', String(32)),
        Column('other_middle_name_date_collected', DateTime(timezone=True)),
        Column('other_last_name_unhashed', String(50)),
        Column('other_last_name_hashed', String(32)),
        Column('other_last_name_date_collected', DateTime(timezone=True)),
        Column('other_suffix_unhashed', String(50)),
        Column('other_suffix_hashed', String(32)),
        Column('other_suffix_date_collected', DateTime(timezone=True)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(OtherNames, other_names_table)
        return
        
    def person_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=True)
        person_table = Table(
        'person', 
        table_metadata, 
        #Doesn't handle hashed personal identifiers yet
        #How do we handle dups?  We don't.  It's a log of what was submitted.
        #So remove primary key, as that will bar dups.
        Column('id', Integer, primary_key=True),
        Column('export_id', String(50), ForeignKey(Export.c.export_id)), 
        Column('person_id_hashed', String(32)),
        Column('person_id_unhashed', String(50)),
        Column('person_id_date_collected', DateTime(timezone=True)),
        Column('person_date_of_birth_hashed', String(32)),
        Column('person_date_of_birth_unhashed', Date(timezone=False)),
        Column('person_date_of_birth_date_collected', DateTime(timezone=True)),
        Column('person_ethnicity_hashed', String(32)),
        Column('person_ethnicity_unhashed', Integer(2)),
        Column('person_ethnicity_date_collected', DateTime(timezone=True)),
        Column('person_gender_hashed', String(32)),
        Column('person_gender_unhashed', Integer(2)),
        Column('person_gender_date_collected', DateTime(timezone=True)),
        Column('person_legal_first_name_hashed', String(32)),   
        Column('person_legal_first_name_unhashed', String(50)),
        Column('person_legal_first_name_date_collected', DateTime(timezone=True)),
        Column('person_legal_last_name_hashed', String(32)),
        Column('person_legal_last_name_unhashed', String(50)),
        Column('person_legal_last_name_date_collected', DateTime(timezone=True)),
        Column('person_legal_middle_name_hashed', String(32)),
        Column('person_legal_middle_name_unhashed', String(50)),
        Column('person_legal_middle_name_date_collected', DateTime(timezone=True)),
        Column('person_legal_suffix_hashed', String(32)),
        Column('person_legal_suffix_unhashed', String(50)),
        Column('person_legal_suffix_date_collected', DateTime(timezone=True)),
        #OtherNames is in its own table as there can be multiple OtherNames
        #Race is in its own table as there can be multiple races
        Column('person_social_security_number_hashed', String(32)),
        Column('person_social_security_number_unhashed', String(9)),
        Column('person_social_security_number_date_collected', DateTime(timezone=True)),
        Column('person_social_sec_number_quality_code', String(2)),
        Column('person_social_sec_number_quality_code_date_collected', DateTime(timezone=True)),
        #PersonHistorical has its own table
        #SiteServiceParticipation has its own table
        #ReleaseOfInformation has its own table
        useexisting = True)
        table_metadata.create_all()
        
        mapper(Person, person_table, properties={'children': relation(OtherNames), 'children': relation(Races), 'children': relation(PersonHistorical)})
        
        return 

    def person_historical_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=False)
        person_historical_table = Table(
        'person_historical', 
        table_metadata, 
        Column('id', Integer, primary_key=True),
        Column('person_historical_id', String(32)),
        Column('person_index_id', Integer, ForeignKey(Person.c.id)),
        
    # dbCol: child_currently_enrolled_in_school
        Column('child_currently_enrolled_in_school', Integer),
        Column('child_currently_enrolled_in_school_date_collected', DateTime(timezone=True)),

	# dbCol: currently_employed
		Column('currently_employed', Integer),
		Column('currently_employed_date_collected', DateTime(timezone=True)),

	# dbCol: degree_code
		Column('degree_code', Integer),
		Column('degree_code_date_collected', DateTime(timezone=True)),

	# dbCol: employment_tenure
		Column('employment_tenure', Integer),
		Column('employment_tenure_date_collected', DateTime(timezone=True)),

	# dbCol: health_status
		Column('health_status', Integer),
		Column('health_status_date_collected', DateTime(timezone=True)),

	# dbCol: highest_school_level
		Column('highest_school_level', Integer),
		Column('highest_school_level_date_collected', DateTime(timezone=True)),

	# dbCol: hivaids_status
		Column('hivaids_status', Integer),
		Column('hivaids_status_date_collected', DateTime(timezone=True)),

	# dbCol: hours_worked_last_week
		Column('hours_worked_last_week', Integer),
		Column('hours_worked_last_week_date_collected', DateTime(timezone=True)),

	# dbCol: hud_homeless
		Column('hud_homeless', Integer),
		Column('hud_homeless_date_collected', DateTime(timezone=True)),

    # IncomeAndSources (has its own table) FIXME
    
    # dbCol: mental_health_indefinite
        Column('mental_health_indefinite', Integer),
        Column('mental_health_indefinite_date_collected', DateTime(timezone=True)),

	# dbCol: mental_health_problem
		Column('mental_health_problem', Integer),
		Column('mental_health_problem_date_collected', DateTime(timezone=True)),

    # PersonAddress (has its own table) FIXME
    
    # dbCol: physical_disability
        Column('physical_disability', Integer),
        Column('physical_disability_data_col_stage', Integer),
        Column('physical_disability_date_collected', DateTime(timezone=True)),
        Column('physical_disability_date_effective', DateTime(timezone=True)),

	# dbCol: reason_for_leaving
		Column('reason_for_leaving', Integer),
		Column('reason_for_leaving_date_collected', DateTime(timezone=True)),

	# dbCol: substance_abuse_indefinite
		Column('substance_abuse_indefinite', Integer),
		Column('substance_abuse_indefinite_date_collected', DateTime(timezone=True)),

	# dbCol: substance_abuse_problem
		Column('substance_abuse_problem', Integer),
		Column('substance_abuse_problem_date_collected', DateTime(timezone=True)),

    # dbCol: total_income
        Column('total_income', Numeric(5,2)),
        Column('total_income_date_collected', DateTime(timezone=True)),
        
    # Veteran (has its own table) FIXME
    
        useexisting = True
        )
        table_metadata.create_all()
        mapper(PersonHistorical, person_historical_table)
        return
    
    def races_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=False)
        races_table = Table(
        'races', 
        table_metadata, 
        Column('id', Integer, primary_key=True),
        #Column('person_index_id', Integer, ForeignKey(Person.c.id)),
        Column('race_unhashed', Integer(2)),
        Column('race_hashed', String(32)),
        Column('race_date_collected', DateTime(timezone=True)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Races, races_table)
        return    
    
#current projects only using client sections, not resources    
#    def site_service_map(self):
#        table_metadata = MetaData(bind=self.pg_db, reflect=False)
#        site_service_table = Table(
#        'site_service', 
#        table_metadata, 
#        Column('site_service_id', String(50), primary_key=True),
#        Column('site_service_id_date_collected', DateTime(timezone=True)),
#        Column('site_service_fips_code', String(10)),
#        Column('site_service_fips_code_date_collected', DateTime(timezone=True)),
#        Column('site_service_facility_code', String(10)),
#        Column('site_service_facility_code_date_collected', DateTime(timezone=True)),
#        Column('site_service_coc_code', String(5)),
#        Column('site_service_coc_code_date_collected', DateTime(timezone=True)),
#        Column('site_service_type', Integer(3)),
#        Column('site_service_type_date_collected', DateTime(timezone=True)),
#        Column('site_service_type_other', String(50)),
#        Column('site_service_type_other_date_collected', DateTime(timezone=True)),
#        Column('site_service_individual_family_code', Integer(3)),
#        Column('site_service_individual_family_code_date_collected', DateTime(timezone=True)),
#        Column('site_service_target_population', String(50)),
#        Column('site_service_target_population_date_collected', DateTime(timezone=True)),
#        Column('site_service_site_id', String(50)), 
#        Column('site_service_site_id_date_collected', DateTime(timezone=True)),
#        Column('site_service_name', String(100)),         
#        #Phone is in its own table to support many-to-one relation
#        )
#        table_metadata.create_all()
#        mapper(SiteService, site_service_table)
#        return

#current projects only using client sections, not resources        
#    def site_service_phone_map(self):
#        table_metadata = MetaData(bind=self.pg_db, reflect=False)
#        site_service_phone_table = Table(
#        'site_service', 
#        table_metadata, 
#        Column('site_service_id', ForeignKey("site_service.site_service_id"), nullable=False),
#        Column('phone_toll_free', Boolean),
#        Column('phone_confidential', Boolean),
#        Column('phone_number', String(50)),     
#        Column('extension', String(20)),
#        Column('description', String(200)),
#        Column('type', String(50)),
#        Column('function', String(50)),
#        Column('reason_withheld', String(200)),
#        )
#        table_metadata.create_all()
#        mapper(SiteService, site_service_phone_table)
#        return
        
    def parse_database(self, root_element):
        '''Look for a DatabaseID and related fields in the XML and persists it.'''      
        #Now populate the mapping
        #Xpath query strings
        xpDatabaseID = '/hmis:SourceDatabase/hmis:DatabaseID'
        xpDatabaseIDIDNum = 'hmis:IDNum'
        xpDatabaseIDIDStr = 'hmis:IDStr'
        xpExportIDIDNum = '../hmis:Export/hmis:ExportID/hmis:IDNum'
        xpExportIDIDStr = '../hmis:Export/hmis:ExportID/hmis:IDStr'
        xpIDNumdateCollected = 'hmis:IDNum/@hmis:dateCollected'
        xpIDStrdateCollected = 'hmis:IDStr/@hmis:dateCollected'
        xpDatabaseContactEmail = '../hmis:DatabaseContactEmail'
        xpDatabaseContactEmaildateCollected = '../hmis:DatabaseContactEmail/@hmis:dateCollected'
        xpDatabaseContactExtension = '../hmis:DatabaseContactExtension'
        xpDatabaseContactExtensiondateCollected = '../hmis:DatabaseContactExtension/@hmis:dateCollected'
        xpDatabaseContactLast = '../hmis:DatabaseContactLast'        
        xpDatabaseContactLastdateCollected = '../hmis:DatabaseContactLast/@hmis:dateCollected'        
        xpDatabaseContactPhone = '../hmis:DatabaseContactPhone'
        xpDatabaseContactPhonedateCollected = '../hmis:DatabaseContactPhone/@hmis:dateCollected'
        xpDatabaseName = '../hmis:DatabaseName'
        xpDatabaseNamedateCollected = '../hmis:DatabaseName/@hmis:dateCollected'
        #find each occurrence of database_id in the XML, make a new table 
        #schema allows for multiple database tags, but that's both unlikely and problematic.
        #enforce only one database tag (by only taking the first element in the list in the next line [0])
        database_id_tag = root_element.xpath(xpDatabaseID, namespaces={'hmis': self.hmis_namespace})[0]
        #and make a fake list so the code still works
        database_id_tag = [database_id_tag]
        if database_id_tag is not None:
            for item in database_id_tag:
                self.parse_dict = {}
                database_id_val = item.xpath(xpDatabaseIDIDNum, namespaces={'hmis': self.hmis_namespace})
                
                if len(database_id_val) is 0:
                    database_id_val = item.xpath(xpDatabaseIDIDStr, namespaces={'hmis': self.hmis_namespace})
                    self.parse_dict.__setitem__('database_id', database_id_val[0].text)
                    self.existence_test_and_add('database_id_date_collected', item.xpath(xpIDStrdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                else:
                    self.parse_dict.__setitem__('database_id', database_id_val[0].text)
                    self.existence_test_and_add('database_id', item.xpath(xpIDNumdateCollected, namespaces={'hmis': self.hmis_namespace})[0], 'attribute_date')
                    
                test = item.xpath(xpExportIDIDNum, namespaces={'hmis': self.hmis_namespace})
                if len(test) is 0:
                    self.existence_test_and_add('export_id', item.xpath(xpExportIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                else:
                    self.existence_test_and_add('export_id', test, 'text')
                self.existence_test_and_add('database_email', item.xpath(xpDatabaseContactEmail, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('database_email_date_collected', item.xpath(xpDatabaseContactEmaildateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('database_contact_extension', item.xpath(xpDatabaseContactExtension, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('database_contact_extension_date_collected', item.xpath(xpDatabaseContactExtensiondateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('database_contact_last', item.xpath(xpDatabaseContactLast, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('database_contact_last_date_collected', item.xpath(xpDatabaseContactLastdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('database_contact_phone', item.xpath(xpDatabaseContactPhone, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('database_contact_phone_date_collected', item.xpath(xpDatabaseContactPhonedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('database_name', item.xpath(xpDatabaseName, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('database_name_date_collected', item.xpath(xpDatabaseNamedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, Database)
                #had to hard code this to just use root element, since we're not allowing multiple database_ids per XML file
                self.parse_person(root_element)
            return
    
    def parse_export(self, root_element):
        '''Looks for an ExportID and related fields in the XML and persists it.'''      
        "this code allows for multiple export ids per file, but that's problematic."
        #Xpath query strings
        xpExport = 'hmis:Export'
        xpExportIDIDNum = 'hmis:ExportID/hmis:IDNum'
        xpExportIDIDStr = 'hmis:ExportID/hmis:IDStr'
        xpIDNumdateCollected = 'hmis:ExportID/hmis:IDNum/@hmis:dateCollected'
        xpIDStrdateCollected = 'hmis:ExportID/hmis:IDStr/@hmis:dateCollected'
        xpExportExportDate = 'hmis:ExportDate'
        xpExportExportDatedateCollected = 'hmis:ExportDate/@hmis:dateCollected'
        xpExportPeriodStartDate = 'hmis:ExportPeriod/hmis:StartDate'
        xpExportPeriodStartDatedateCollected = 'hmis:ExportPeriod/hmis:StartDate/@hmis:dateCollected'
        xpExportPeriodEndDate = 'hmis:ExportPeriod/hmis:EndDate'
        xpExportPeriodEndDatedateCollected = 'hmis:ExportPeriod/hmis:EndDate/@hmis:dateCollected'
        xpExportSoftwareVendor = 'hmis:SoftwareVendor'
        xpExportSoftwareVendordateCollected = 'hmis:SoftwareVendor/@hmis:dateCollected'
        xpExportSoftwareVendor = 'hmis:SoftwareVendor'
        xpExportSoftwareVendordateCollected = 'hmis:SoftwareVendor/@hmis:dateCollected'
        xpExportSoftwareVersion = 'hmis:SoftwareVersion'
        xpExportSoftwareVersiondateCollected = 'hmis:SoftwareVersion/@hmis:dateCollected'
        
        "enforce only one export tag (by only taking the first element in the list in the next line [0])"
        export = root_element.xpath(xpExport, namespaces={'hmis': self.hmis_namespace})[0]
        #and make a fake list so the code still works
        export = [export]
        if export is not None:
            for item in export:
                self.parse_dict = {}
                test = item.xpath(xpExportIDIDNum, namespaces={'hmis': self.hmis_namespace}) 
                if len(test) is 0:
                    test = item.xpath(xpExportIDIDStr, namespaces={'hmis': self.hmis_namespace})
                    self.export_id = test
                    value = self.existence_test_and_add('export_id', test, 'text')
                    self.existence_test_and_add('export_id_date_collected', item.xpath(xpIDStrdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                else:
                    self.export_id = test
                    self.existence_test_and_add('export_id', test, 'text')
                    self.existence_test_and_add('export_id_date_collected', item.xpath(xpIDNumdateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')    
                self.existence_test_and_add('export_date', item.xpath(xpExportExportDate, namespaces={'hmis': self.hmis_namespace}), 'element_date') 
                self.existence_test_and_add('export_date_date_collected', item.xpath(xpExportExportDatedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_period_start_date', item.xpath(xpExportPeriodStartDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                self.existence_test_and_add('export_period_start_date_date_collected', item.xpath(xpExportPeriodStartDatedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_period_end_date', item.xpath(xpExportPeriodEndDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                self.existence_test_and_add('export_period_end_date_date_collected', item.xpath(xpExportPeriodEndDatedateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_software_vendor', item.xpath(xpExportSoftwareVendor, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('export_software_vendor_date_collected', item.xpath(xpExportSoftwareVendordateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.existence_test_and_add('export_software_version', item.xpath(xpExportSoftwareVersion, namespaces={'hmis': self.hmis_namespace}), 'text')
                self.existence_test_and_add('export_software_version_date_collected', item.xpath(xpExportSoftwareVersiondateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
#                self.session.flush()
#                print 'export id is', Export.c.id
                self.shred(self.parse_dict, Export)
                self.parse_database(root_element)
                #current projects only using client sections, not resources    
                #self.parse_site_service(database_id_tag)

        #current projects only using client sections, not resources      
        else:
            self.shred(self.parse_dict, Export)
            return

    def parse_other_names(self, person_tag):
        '''Looks for an OtherNames tag and related fields in the XML and persists it.'''      
        '''This code allows for multiple OtherNames per Person'''
        #Xpath query strings
        xpOtherNames = 'hmis:OtherNames'
        #I don't want the PersonID from the XML, as there could be two of the 
        #same PersonID within the same export.  Need the Person Table Index
        #So that's what is used.  See where this index is retrieved after the 
        #session flush.
        xpOtherFirstNameUnhashed = 'hmis:OtherFirstName/hmis:Unhashed'
        xpOtherFirstNameHashed = 'hmis:OtherFirstName/hmis:Hashed'
        xpOtherFirstNameDateCollectedUnhashed = 'hmis:OtherFirstName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherFirstNameDateCollectedHashed = 'hmis:OtherFirstName/hmis:Hashed/@hmis:dateCollected'
        xpOtherLastNameUnhashed = 'hmis:OtherLastName/hmis:Unhashed'
        xpOtherLastNameHashed = 'hmis:OtherLastName/hmis:Hashed'
        xpOtherLastNameDateCollectedUnhashed = 'hmis:OtherLastName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherLastNameDateCollectedHashed = 'hmis:OtherLastName/hmis:Hashed/@hmis:dateCollected'        
        xpOtherMiddleNameUnhashed = 'hmis:OtherMiddleName/hmis:Unhashed'
        xpOtherMiddleNameHashed = 'hmis:OtherMiddleName/hmis:Hashed'
        xpOtherMiddleNameDateCollectedUnhashed = 'hmis:OtherMiddleName/hmis:Unhashed/@hmis:dateCollected'
        xpOtherMiddleNameDateCollectedHashed = 'hmis:OtherMiddleName/hmis:Hashed/@hmis:dateCollected'
        xpOtherSuffixUnhashed = 'hmis:OtherSuffix/hmis:Unhashed'
        xpOtherSuffixHashed = 'hmis:OtherSuffix/hmis:Hashed'
        xpOtherSuffixDateCollectedUnhashed = 'hmis:OtherSuffix/hmis:Unhashed/@hmis:dateCollected'
        xpOtherSuffixDateCollectedHashed = 'hmis:OtherSuffix/hmis:Hashed/@hmis:dateCollected'
        
        other_names = person_tag.xpath(xpOtherNames, namespaces={'hmis': self.hmis_namespace})
        if other_names is not None:
            for item in other_names:
                self.parse_dict = {}
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                test = self.existence_test_and_add('other_first_name_unhashed', item.xpath(xpOtherFirstNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('other_first_name_date_collected', item.xpath(xpOtherFirstNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                if test is False:
                    test = self.existence_test_and_add('other_first_name_hashed', item.xpath(xpOtherFirstNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('other_first_name_date_collected', item.xpath(xpOtherFirstNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                test = self.existence_test_and_add('other_last_name_unhashed', item.xpath(xpOtherLastNameUnhashed, namespaces={'hmis': self.hmis_namespace}),'text')
                if test is True:
                    self.existence_test_and_add('other_last_name_date_collected', item.xpath(xpOtherLastNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                if test is False:
                    self.existence_test_and_add('other_last_name_hashed', item.xpath(xpOtherLastNameHashed, namespaces={'hmis': self.hmis_namespace}),'text')
                    self.existence_test_and_add('other_last_name_date_collected', item.xpath(xpOtherLastNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                test = self.existence_test_and_add('other_middle_name_unhashed', item.xpath(xpOtherMiddleNameUnhashed, namespaces={'hmis': self.hmis_namespace}),'text')
                if test is True:
                    self.existence_test_and_add('other_middle_name_date_collected', item.xpath(xpOtherMiddleNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                if test is False:
                    self.existence_test_and_add('other_middle_name_hashed', item.xpath(xpOtherMiddleNameHashed, namespaces={'hmis': self.hmis_namespace}),'text')
                    self.existence_test_and_add('other_middle_name_date_collected', item.xpath(xpOtherMiddleNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                test = self.existence_test_and_add('other_suffix_unhashed', item.xpath(xpOtherSuffixUnhashed, namespaces={'hmis': self.hmis_namespace}),'text')
                if test is True:
                    self.existence_test_and_add('other_suffix_date_collected', item.xpath(xpOtherSuffixDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                if test is False:
                    self.existence_test_and_add('other_suffix_hashed', item.xpath(xpOtherSuffixHashed, namespaces={'hmis': self.hmis_namespace}),'text')
                    self.existence_test_and_add('other_suffix_date_collected', item.xpath(xpOtherSuffixDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                self.shred(self.parse_dict, OtherNames)
        else:
            self.shred(self.parse_dict, OtherNames)
            return
    ########################################################################
    ########################################################################
    #   parsing of the person_historical tag
    ########################################################################
    ########################################################################
    
    def parse_person_historical(self, person_tag):
        '''Looks for an PersonHistorical tag and related fields in the XML and persists it.'''      
        '''This code allows for multiple PersonHistorical per Person'''
        #Xpath query strings
        xpPersonHistorical = 'hmis:SiteServiceParticipation/hmis:PersonHistorical'
        #I don't want the PersonID from the XML, as there could be two of the 
        #same PersonID within the same export.  Need the Person Table Index
        #So that's what is used.  See where this index is retrieved after the 
        #session flush.
        xpPersonHistoricalID = 'hmis:PersonHistoricalID/hmis:IDNum'
        xpPersonHistoricalIDDateCollected = 'hmis:PersonHistoricalID/@hmis:dateCollected'
        xpPersonHistoricalChildCurrentlyEnrolledInSchool = 'hmis:ChildCurrentlyEnrolledInSchool'
        xpPersonHistoricalChildCurrentlyEnrolledInSchoolDateCollected = 'hmis:ChildCurrentlyEnrolledInSchool/@hmis:dateCollected'
        xpPersonHistoricalCurrentlyEmployed = 'hmis:CurrentlyEmployed'
        xpPersonHistoricalCurrentlyEmployedDateCollected = 'hmis:CurrentlyEmployed/@hmis:dateCollected'
        xpPersonHistoricalDegreeCode = 'hmis:DegreeCode'
        xpPersonHistoricalDegreeCodeDateCollected = 'hmis:DegreeCode/@hmis:dateCollected'
        xpPersonHistoricalEmploymentTenure = 'hmis:EmploymentTenure'
        xpPersonHistoricalEmploymentTenureDateCollected = 'hmis:EmploymentTenure/@hmis:dateCollected'
        
        xpPersonHistoricalHealthStatus = 'hmis:HealthStatus'
        xpPersonHistoricalHealthStatusDateCollected = 'hmis:HealthStatus/@hmis:dateCollected'
        xpPersonHistoricalHighestSchoolLevel = 'hmis:HighestSchoolLevel'
        xpPersonHistoricalHighestSchoolLevelDateCollected = 'hmis:HighestSchoolLevel/@hmis:dateCollected'
        xpPersonHistoricalHIVAIDSStatus = 'hmis:HIVAIDSStatus'
        xpPersonHistoricalHIVAIDSStatusDateCollected = 'hmis:HIVAIDSStatus/@hmis:dateCollected'
        xpPersonHistoricalHoursWorkedLastWeek = 'hmis:HoursWorkedLastWeek'
        xpPersonHistoricalHoursWorkedLastWeekDateCollected = 'hmis:HoursWorkedLastWeek/@hmis:dateCollected'
        xpPersonHistoricalHUDHomeless = 'hmis:HUDHomeless'
        xpPersonHistoricalHUDHomelessDateCollected = 'hmis:HUDHomeless/@hmis:dateCollected'
        # IncomeAndSources (separte table 1 to many) FIXME
        
        xpPersonHistoricalMentalHealthIndefinite = 'hmis:MentalHealthIndefinite'
        xpPersonHistoricalMentalHealthIndefiniteDateCollected = 'hmis:MentalHealthIndefinite/@hmis:dateCollected'
        xpPersonHistoricalMentalHealthProblem = 'hmis:MentalHealthProblem'
        xpPersonHistoricalMentalHealthProblemDateCollected = 'hmis:MentalHealthProblem/@hmis:dateCollected'
        #xpPersonHistoricalPersonAddress = 'hmis:PersonAddress' (Mutiple addresses - should have it's own table) FIXME
        
        xpPersonHistoricalPhysicalDisability = 'hmis:PhysicalDisability'
        xpPersonHistoricalPhysicalDisabilityDataCollectionStage = 'hmis:PhysicalDisability/@hmis:dataCollectionStage'
        xpPersonHistoricalPhysicalDisabilityDateCollected = 'hmis:PhysicalDisability/@hmis:dateCollected'
        xpPersonHistoricalPhysicalDisabilityDateEffective = 'hmis:PhysicalDisability/@hmis:dateEffective'
        xpPersonHistoricalReasonForLeaving = 'hmis:ReasonForLeaving'
        xpPersonHistoricalReasonForLeavingDateCollected = 'hmis:ReasonForLeaving/@hmis:dateCollected'
        xpPersonHistoricalSubstanceAbuseIndefinite = 'hmis:SubstanceAbuseIndefinite'
        xpPersonHistoricalSubstanceAbuseIndefiniteDateCollected = 'hmis:SubstanceAbuseIndefinite/@hmis:dateCollected'
        xpPersonHistoricalSubstanceAbuseProblem = 'hmis:SubstanceAbuseProblem'
        xpPersonHistoricalSubstanceAbuseProblemDateCollected = 'hmis:SubstanceAbuseProblem/@hmis:dateCollected'
        xpPersonHistoricalTotalIncome = 'hmis:TotalIncome'
        xpPersonHistoricalTotalIncomeDateCollected = 'hmis:TotalIncome/@hmis:dateCollected'
        # Veteran tag should have a table 1 to many
        
        person_historical = person_tag.xpath(xpPersonHistorical, namespaces={'hmis': self.hmis_namespace})
        
        if person_historical is not None:
            for item in person_historical:
                self.parse_dict = {}
                
                fldName='person_historical_id'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalID, namespaces={'hmis': self.hmis_namespace}), 'text')
                
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                
                fldName='child_currently_enrolled_in_school'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalChildCurrentlyEnrolledInSchool, namespaces={'hmis': self.hmis_namespace}), 'text')
                
                
                
                
                fldName='child_currently_enrolled_in_school_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalChildCurrentlyEnrolledInSchoolDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                
                fldName='currently_employed'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalCurrentlyEmployed, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='currently_employed_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalCurrentlyEmployedDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='degree_code'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalDegreeCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='degree_code_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalDegreeCodeDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='employment_tenure'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalEmploymentTenure, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='employment_tenure_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalEmploymentTenureDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='health_status'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHealthStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='health_status_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHealthStatusDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='highest_school_level'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHighestSchoolLevel, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='highest_school_level_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHighestSchoolLevelDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='hivaids_status'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHIVAIDSStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='hivaids_status_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHIVAIDSStatusDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='hours_worked_last_week'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHoursWorkedLastWeek, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='hours_worked_last_week_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHoursWorkedLastWeekDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='hud_homeless'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHUDHomeless, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='hud_homeless_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalHUDHomelessDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='mental_health_indefinite'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalMentalHealthIndefinite, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='mental_health_indefinite_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalMentalHealthIndefiniteDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='mental_health_problem'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalMentalHealthProblem, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='mental_health_problem_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalMentalHealthProblemDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='physical_disability'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalPhysicalDisability, namespaces={'hmis': self.hmis_namespace}), 'text')
                # FIXME
                
                fldName='physical_disability_data_col_stage'
                # FIXME
                #if test is True:
                #    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalPhysicalDisabilityDataCollectionStage, namespaces={'hmis': self.hmis_namespace}), 'attribute_text')
                    
                fldName='physical_disability_date_collected'    
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalPhysicalDisabilityDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='physical_disability_date_effective'    
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalPhysicalDisabilityDateEffective, namespaces={'hmis': self.hmis_namespace}),'attribute_date')                    
                
                fldName='reason_for_leaving'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalReasonForLeaving, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='reason_for_leaving_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalReasonForLeavingDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='substance_abuse_indefinite'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalSubstanceAbuseIndefinite, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='substance_abuse_indefinite_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalSubstanceAbuseIndefiniteDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='substance_abuse_problem'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalSubstanceAbuseProblem, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='substance_abuse_problem_date_collected'
                if test is True:
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalSubstanceAbuseProblemDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')
                    
                fldName='total_income'
                test = self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalTotalIncome, namespaces={'hmis': self.hmis_namespace}), 'text')
                
                if test is True:
                    fldName='total_income_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalTotalIncomeDateCollected, namespaces={'hmis': self.hmis_namespace}),'attribute_date')                    
                
                self.shred(self.parse_dict, PersonHistorical)
                
        else:
            self.shred(self.parse_dict, PersonHistorical)
            return

    def parse_person(self, root_element):
        '''Looks for a Person tag and related fields in the XML and persists \n
        it.  This code allows for multiple persons per file'''
        #Xpath query strings
        xpPerson = 'hmis:Person'
        xpExportID = '../hmis:Export/hmis:ExportID/hmis:IDNum'
        xpPersonIDHashed = 'hmis:PersonID/hmis:Hashed'
        xpPersonIDUnhashed = 'hmis:PersonID/hmis:Unhashed'
        #need to handle IDStr
        xpPersonIDDateCollectedHashed = 'hmis:PersonID/hmis:Hashed/@hmis:dateCollected'
        xpPersonIDDateCollectedUnhashed = 'hmis:PersonID/hmis:Unhashed/@hmis:dateCollected'
        xpPersonDateOfBirthHashed = 'hmis:DateOfBirth/hmis:Hashed'
        xpPersonDateOfBirthUnhashed = 'hmis:DateOfBirth/hmis:Unhashed'
        xpPersonDateOfBirthDateCollectedHashed = 'hmis:DateOfBirth/hmis:Hashed/@hmis:dateCollected'
        xpPersonDateOfBirthDateCollectedUnhashed = 'hmis:DateOfBirth/hmis:Unhashed/@hmis:dateCollected'
        xpPersonEthnicityHashed = 'hmis:Ethnicity/hmis:Hashed'
        xpPersonEthnicityUnhashed = 'hmis:Ethnicity/hmis:Unhashed'
        xpPersonEthnicityDateCollectedHashed = 'hmis:Ethnicity/hmis:Hashed/@hmis:dateCollected'
        xpPersonEthnicityDateCollectedUnhashed = 'hmis:Ethnicity/hmis:Unhashed/@hmis:dateCollected'
        xpPersonGenderHashed = 'hmis:Gender/hmis:Hashed'
        xpPersonGenderUnhashed = 'hmis:Gender/hmis:Unhashed'
        xpPersonGenderDateCollectedHashed = 'hmis:Gender/hmis:Hashed/@hmis:dateCollected'
        xpPersonGenderDateCollectedUnhashed = 'hmis:Gender/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalFirstNameHashed = 'hmis:LegalFirstName/hmis:Hashed'
        xpPersonLegalFirstNameUnhashed = 'hmis:LegalFirstName/hmis:Unhashed'
        xpPersonLegalFirstNameDateCollectedHashed = 'hmis:LegalFirstName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalFirstNameDateCollectedUnhashed = 'hmis:LegalFirstName/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalLastNameHashed = 'hmis:LegalLastName/hmis:Hashed'
        xpPersonLegalLastNameUnhashed = 'hmis:LegalLastName/hmis:Unhashed'
        xpPersonLegalLastNameDateCollectedHashed = 'hmis:LegalLastName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalLastNameDateCollectedUnhashed = 'hmis:LegalLastName/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalMiddleNameHashed = 'hmis:LegalMiddleName/hmis:Hashed'
        xpPersonLegalMiddleNameUnhashed = 'hmis:LegalMiddleName/hmis:Unhashed'
        xpPersonLegalMiddleNameDateCollectedHashed = 'hmis:LegalMiddleName/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalMiddleNameDateCollectedUnhashed = 'hmis:LegalMiddleName/hmis:Unhashed/@hmis:dateCollected'
        xpPersonLegalSuffixHashed = 'hmis:LegalSuffix/hmis:Hashed'
        xpPersonLegalSuffixUnhashed = 'hmis:LegalSuffix/hmis:Unhashed'
        xpPersonLegalSuffixDateCollectedHashed = 'hmis:LegalSuffix/hmis:Hashed/@hmis:dateCollected'
        xpPersonLegalSuffixDateCollectedUnhashed = 'hmis:LegalSuffix/hmis:Unhashed/@hmis:dateCollected'
        xpPersonSocialSecurityNumberHashed = 'hmis:SocialSecurityNumber/hmis:Hashed'
        xpPersonSocialSecurityNumberUnhashed = 'hmis:SocialSecurityNumber/hmis:Unhashed'
        xpPersonSocialSecurityNumberDateCollectedHashed = 'hmis:SocialSecurityNumber/hmis:Hashed/@hmis:dateCollected'
        xpPersonSocialSecurityNumberDateCollectedUnhashed = 'hmis:SocialSecurityNumber/hmis:Unhashed/@hmis:dateCollected'
        xpPersonSocialSecNumberQualityCode = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode'
        xpPersonSocialSecNumberQualityCodeDateCollected = 'hmis:SocialSecurityNumber/hmis:SocialSecNumberQualityCode/@hmis:dateCollected'
        person = root_element.xpath(xpPerson, namespaces={'hmis': self.hmis_namespace})
        if person is not None:
            for item in person:
                self.parse_dict = {}
                test = self.existence_test_and_add('person_id_unhashed', item.xpath(xpPersonIDUnhashed, namespaces={'hmis': self.hmis_namespace}), "text")
                if test is True:
                    self.existence_test_and_add('person_id_date_collected', item.xpath(xpPersonIDDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_id_hashed', item.xpath(xpPersonIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_id_date_collected', item.xpath(xpPersonIDDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date') 
                self.existence_test_and_add('export_id', self.export_id, 'text')
                #self.existence_test_and_add('export_id', item.xpath(xpExportID, namespaces={'hmis': self.hmis_namespace}), 'text')
                test = self.existence_test_and_add('person_date_of_birth_unhashed', item.xpath(xpPersonDateOfBirthUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_date_of_birth_date_collected', item.xpath(xpPersonDateOfBirthDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')      
                if test is False:
                    self.existence_test_and_add('person_date_of_birth_hashed', item.xpath(xpPersonDateOfBirthHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_date_of_birth_date_collected', item.xpath(xpPersonDateOfBirthDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')      
                test = self.existence_test_and_add('person_ethnicity_unhashed', item.xpath(xpPersonEthnicityUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_ethnicity_date_collected', item.xpath(xpPersonEthnicityDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')     
                if test is False:
                    self.existence_test_and_add('person_ethnicity_hashed', item.xpath(xpPersonEthnicityHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_ethnicity_date_collected', item.xpath(xpPersonEthnicityDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')     
                test = self.existence_test_and_add('person_gender_unhashed', item.xpath(xpPersonGenderUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_gender_date_collected', item.xpath(xpPersonGenderDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')                    
                if test is False:
                    self.existence_test_and_add('person_gender_hashed', item.xpath(xpPersonGenderHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_gender_date_collected', item.xpath(xpPersonGenderDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_legal_first_name_unhashed', item.xpath(xpPersonLegalFirstNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')         
                if test is True:
                    self.existence_test_and_add('person_legal_first_name_date_collected', item.xpath(xpPersonLegalFirstNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_first_name_hashed', item.xpath(xpPersonLegalFirstNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')         
                    self.existence_test_and_add('person_legal_first_name_date_collected', item.xpath(xpPersonLegalFirstNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_legal_last_name_unhashed', item.xpath(xpPersonLegalLastNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_legal_last_name_date_collected', item.xpath(xpPersonLegalLastNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_last_name_hashed', item.xpath(xpPersonLegalLastNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_legal_last_name_date_collected', item.xpath(xpPersonLegalLastNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                test = self.existence_test_and_add('person_legal_middle_name_unhashed', item.xpath(xpPersonLegalMiddleNameUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_legal_middle_name_date_collected', item.xpath(xpPersonLegalMiddleNameDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_middle_name_hashed', item.xpath(xpPersonLegalMiddleNameHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_legal_middle_name_date_collected', item.xpath(xpPersonLegalMiddleNameDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')                        
                test = self.existence_test_and_add('person_legal_suffix_unhashed', item.xpath(xpPersonLegalSuffixUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_legal_suffix_date_collected', item.xpath(xpPersonLegalSuffixDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_legal_suffix_hashed', item.xpath(xpPersonLegalSuffixHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_legal_suffix_date_collected', item.xpath(xpPersonLegalSuffixDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')                        
                test = self.existence_test_and_add('person_social_security_number_unhashed', item.xpath(xpPersonSocialSecurityNumberUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('person_social_security_number_date_collected', item.xpath(xpPersonSocialSecurityNumberDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('person_social_security_number_hashed', item.xpath(xpPersonSocialSecurityNumberHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('person_social_security_number_date_collected', item.xpath(xpPersonSocialSecurityNumberDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')                    
                self.existence_test_and_add('person_social_sec_number_quality_code', item.xpath(xpPersonSocialSecNumberQualityCode, namespaces={'hmis': self.hmis_namespace}), 'text')                
                self.existence_test_and_add('person_social_sec_number_quality_code_date_collected', item.xpath(xpPersonSocialSecNumberQualityCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')                
                self.shred(self.parse_dict, Person)
                self.parse_person_historical(item)
                self.parse_other_names(item)
                self.parse_races(item)
#                self.session.flush()
#                print 'export id is', Export.c.
            return
        else:
            self.shred(self.parse_dict, Person)
            return
        
    def parse_races(self, person_tag):
        '''Looks for a Race tag and related fields in the XML and persists it.'''      
        '''This code allows for multiple Races per Person'''
        #Xpath query strings
        xpRaces = 'hmis:Race'
        xpRaceUnhashed = 'hmis:Unhashed'
        xpRaceHashed = 'hmis:Hashed'
        xpRaceDateCollectedUnhashed = 'hmis:Unhashed/@hmis:dateCollected'
        xpRaceDateCollectedHashed = 'hmis:Hashed/@hmis:dateCollected'

        races = person_tag.xpath(xpRaces, namespaces={'hmis': self.hmis_namespace})
        if races is not None:
            for item in races:
                self.parse_dict = {}
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                test = self.existence_test_and_add('race_unhashed', item.xpath(xpRaceUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                if test is True:
                    self.existence_test_and_add('race_date_collected', item.xpath(xpRaceDateCollectedUnhashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                if test is False:
                    self.existence_test_and_add('race_hashed', item.xpath(xpRaceHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    self.existence_test_and_add('race_date_collected', item.xpath(xpRaceDateCollectedHashed, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                self.shred(self.parse_dict, Races)           
        else:
            self.shred(self.parse_dict, Races)
            return
    
#current projects only using client sections, not resources    
#    def parse_site_service(self, database_id_tag):
#        '''Looks for a SiteService and related fields in the XML and persists the data set.'''
#        #Xpath query strings
#        xpSiteService = '/hmis:SourceDatabase/hmis:SiteService'
#        xpSiteServiceName = '/hmis:SourceDatabase/hmis:SiteService/airs:Name'
#       
#        site_service = database_id_tag.xpath(xpSiteService, namespaces={'airs': self.airs_namespace})
#        if site_service is not None:
#            for item in site_service:
#               self.parse_dict = {}
#               self.parse_dict.__setitem__('site_service_name', item.text)
#                #xpIDNumdateCollected = '/hmis:SourceDatabase/hmis:Export/hmis:ExportID/hmis:IDNum/@hmis:dateCollected'
#                #parse_dict.__setitem__('export_id_date_collected', dateutil.parser.parse(root_element.xpath(xpIDNumdateCollected, namespaces={'hmis': self.hmis_namespace})[0]))
#                self.shred(parse_dict, SiteService)
#        return

    def shred(self, parse_dict, mapping):
        '''Commits the record set to the database'''
        mapped = mapping(parse_dict)
        self.session.save(mapped)
        self.session.flush()
        #Save the indexes generated at run-time so can be used
        #in dependent tables
        if mapping.__name__ == "Person":
            self.person_index_id = mapped.id
        self.session.commit()
        return
    
    def existence_test_and_add(self, db_column, query_string, handling):
        '''checks that the query actually has a result and adds to dict'''
        #if len(query_string) is not 0:
        if handling == 'no_handling':
                self.persist(db_column, query_string = query_string)
                return True
        elif len(query_string) is not 0 or None:
            if handling == 'attribute_text':
                self.persist(db_column, query_string = query_string[0])
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
                print "need to specify the handling"
                return False
        else:
            return False
            
    def persist(self, db_column, query_string):
        self.parse_dict.__setitem__(db_column, query_string)
        return
    
class Database(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
            #print 'self.' + x + ' is', self.__getattribute__(x)

#    def __repr__(self):
#        return "<Database_ID('%s')>" % (self.database_id)

class Export(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
        print 'Export has been created'
    
class OtherNames(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
            
class Person(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
   
class PersonHistorical(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
   
class Races(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)       
   
#current projects only using client sections, not resources    
#class SiteService(object):
#    def __init__(self, field_dict):
#        print field_dict
#        for x, y in field_dict.iteritems():
#            self.__setattr__(x,y) 
         
#current projects only using client sections, not resources                
#class SiteServicePhone(object):
#    def __init__(self, field_dict):
#        print field_dict
#        for x, y in field_dict.iteritems():
#            self.__setattr__(x,y)                     

def main(argv=None):  
    if argv is None:
        argv = sys.argv
    import postgresutils
    UTILS = postgresutils.Utils()
    UTILS.blank_database()

    inputFile = os.path.join("%s" % settings.INPUTFILES_PATH, "Example_HUD_HMIS_2_8_Instance.xml")
    
    if os.path.isfile(inputFile) is True:#_adapted_further
        try:
            xml_file = open(inputFile,'r') 
        except:
            print "error"
            
        reader = HMISXML28Reader(xml_file)
        tree = reader.read()
        reader.process_data(tree)
        xml_file.close()

if __name__ == "__main__":
    sys.exit(main()) 