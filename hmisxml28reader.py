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
import clsExceptions

class HMISXML28Reader:
    '''Implements reader interface.'''
    implements (Reader) 
    
    hmis_namespace = "http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd" 
    airs_namespace = "http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd"
    nsmap = {"hmis" : hmis_namespace, "airs" : airs_namespace}

    def __init__(self, xml_file):
        
        # Validate that we have a valid username & password to access the database
        if settings.DB_USER == "":
            raise clsExceptions.DatabaseAuthenticationError(1001, "Invalid user to access database", self.__init__)
        if settings.DB_PASSWD == "":
            raise clsExceptions.DatabaseAuthenticationError(1002, "Invalid password to access database", self.__init__)
            
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
        self.release_of_information_map()
        self.income_and_sources_map()
        self.veteran_map()
        self.hud_homeless_episodes_map()
        self.person_address_map()
        self.other_names_map()
        self.races_map()
        self.household_map()
        self.member_map()
        
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
    
    
    def hud_homeless_episodes_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        hud_homeless_episodes_table = Table(
        'hud_homeless_episodes',
        table_metadata,
        
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey(PersonHistorical.c.id)),
        
    # dbCol: start_date
        Column('start_date', String(32)),
        Column('start_date_date_collected', DateTime(timezone=True)),
    
    # dbCol: end_date
        Column('end_date', String(32)),
        Column('end_date_date_collected', DateTime(timezone=True)),
    
        useexisting = True)
        table_metadata.create_all()
    
        mapper(HUDHomelessEpisodes, hud_homeless_episodes_table)
            
        return
    
    
    def veteran_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=True)
        veteran_table = Table(
        'veteran', 
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey(PersonHistorical.c.id)),
    # dbCol: service_era
        Column('service_era', Integer),
        Column('service_era_date_collected', DateTime(timezone=True)),

	# dbCol: military_service_duration
		Column('military_service_duration', Integer),
		Column('military_service_duration_date_collected', DateTime(timezone=True)),

	# dbCol: served_in_war_zone
		Column('served_in_war_zone', Integer),
		Column('served_in_war_zone_date_collected', DateTime(timezone=True)),

	# dbCol: war_zone
		Column('war_zone', Integer),
		Column('war_zone_date_collected', DateTime(timezone=True)),

	# dbCol: war_zone_other
		Column('war_zone_other', String(50)),
		Column('war_zone_other_date_collected', DateTime(timezone=True)),

	# dbCol: months_in_war_zone
		Column('months_in_war_zone', Integer),
		Column('months_in_war_zone_date_collected', DateTime(timezone=True)),

	# dbCol: received_fire
		Column('received_fire', Integer),
		Column('received_fire_date_collected', DateTime(timezone=True)),

	# dbCol: military_branch
		Column('military_branch', Integer),
		Column('military_branch_date_collected', DateTime(timezone=True)),

	# dbCol: military_branch_other
		Column('military_branch_other', String(50)),
		Column('military_branch_other_date_collected', DateTime(timezone=True)),

	# dbCol: discharge_status
		Column('discharge_status', Integer),
		Column('discharge_status_date_collected', DateTime(timezone=True)),

    # dbCol: discharge_status_other
        Column('discharge_status_other', String(50)),
        Column('discharge_status_other_date_collected', DateTime(timezone=True)),
        
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Veteran, veteran_table)
        return
        
    def person_address_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=True)
        person_address_table = Table(
        'person_address', 
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey(PersonHistorical.c.id)),
        Column('address_period_start_date',DateTime(timezone=True)),
        Column('address_period_start_date_date_collected',DateTime(timezone=True)),
        Column('address_period_end_date',DateTime(timezone=True)),
        Column('address_period_end_date_date_collected',DateTime(timezone=True)),
        Column('pre_address_line', String(32)),
        Column('pre_address_line_date_collected',DateTime(timezone=True)),
        Column('line1', String(32)),
        Column('line1_date_collected',DateTime(timezone=True)),
        Column('line2', String(32)),
        Column('line2_date_collected',DateTime(timezone=True)),
        Column('city', String(32)),
        Column('city_date_collected',DateTime(timezone=True)),
        Column('county', String(32)),
        Column('county_date_collected',DateTime(timezone=True)),
        Column('state', String(32)),
        Column('state_date_collected',DateTime(timezone=True)),
        
        #<xsd:element name="ZIPCode" type="hmis:zIPCode" minOccurs="0"/>
        Column('zipcode', String(10)),          # 5+4+1 33626-1827
        Column('zipcode_date_collected',DateTime(timezone=True)),
        
        Column('country', String(32)),
        Column('country_date_collected',DateTime(timezone=True)),
        #*# dbCol: is_last_permanent_zip
        Column('is_last_permanent_zip', Integer),
        Column('is_last_permanent_zip_date_collected', DateTime(timezone=True)),
        
        #*# dbCol: zip_quality_code
        Column('zip_quality_code', Integer),
        Column('zip_quality_code_date_collected', DateTime(timezone=True)),    
        
        useexisting = True)
        table_metadata.create_all()
        mapper(PersonAddress, person_address_table)
    
        
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
        
        mapper(Person, person_table, properties={'children': relation(OtherNames), 'children': relation(Races), 'children': relation(PersonHistorical), 'children': relation(ReleaseOfInformation)})
        
        return

    

    def person_historical_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=False)
        person_historical_table = Table(
        'person_historical', 
        table_metadata, 
        Column('id', Integer, primary_key=True),
        Column('person_index_id', Integer, ForeignKey(Person.c.id)),
        
    # dbCol: person_historical_id_num
        Column('person_historical_id_num', Integer),
        Column('person_historical_id_num_date_collected', DateTime(timezone=True)),

	# dbCol: person_historical_id_str
		Column('person_historical_id_str', String(32)),
		Column('person_historical_id_str_date_collected', DateTime(timezone=True)),

	# dbCol: barrier_code
		Column('barrier_code', Integer),
		Column('barrier_code_date_collected', DateTime(timezone=True)),

	# dbCol: barrier_other
		Column('barrier_other', String(50)),
		Column('barrier_other_date_collected', DateTime(timezone=True)),

	# dbCol: child_currently_enrolled_in_school
		Column('child_currently_enrolled_in_school', Integer),
		Column('child_currently_enrolled_in_school_date_collected', DateTime(timezone=True)),

	# dbCol: currently_employed
		Column('currently_employed', Integer),
		Column('currently_employed_date_collected', DateTime(timezone=True)),

	# dbCol: currently_in_school
		Column('currently_in_school', Integer),
		Column('currently_in_school_date_collected', DateTime(timezone=True)),

	# dbCol: degree_code
		Column('degree_code', Integer),
		Column('degree_code_date_collected', DateTime(timezone=True)),

	# dbCol: degree_other
		Column('degree_other', String(50)),
		Column('degree_other_date_collected', DateTime(timezone=True)),

	# dbCol: developmental_disability
		Column('developmental_disability', Integer),
		Column('developmental_disability_date_collected', DateTime(timezone=True)),

	# dbCol: domestic_violence
		Column('domestic_violence', Integer),
		Column('domestic_violence_date_collected', DateTime(timezone=True)),

	# dbCol: domestic_violence_how_long
		Column('domestic_violence_how_long', Integer),
		Column('domestic_violence_how_long_date_collected', DateTime(timezone=True)),

	# dbCol: due_date (Is this right xsd:date)
		Column('due_date', Date),
		Column('due_date_date_collected', DateTime(timezone=True)),

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

	# dbCol: hud_chronic_homeless
		Column('hud_chronic_homeless', Integer),
		Column('hud_chronic_homeless_date_collected', DateTime(timezone=True)),

	# dbCol: hud_homeless
		Column('hud_homeless', Integer),
		Column('hud_homeless_date_collected', DateTime(timezone=True)),

		###HUDHomelessEpisodes (subtable)

		###IncomeAndSources (subtable)

	# dbCol: length_of_stay_at_prior_residence
		Column('length_of_stay_at_prior_residence', Integer),
		Column('length_of_stay_at_prior_residence_date_collected', DateTime(timezone=True)),

	# dbCol: looking_for_work
		Column('looking_for_work', Integer),
		Column('looking_for_work_date_collected', DateTime(timezone=True)),

	# dbCol: mental_health_indefinite
		Column('mental_health_indefinite', Integer),
		Column('mental_health_indefinite_date_collected', DateTime(timezone=True)),

	# dbCol: mental_health_problem
		Column('mental_health_problem', Integer),
		Column('mental_health_problem_date_collected', DateTime(timezone=True)),

	# dbCol: non_cash_source_code
		Column('non_cash_source_code', Integer),
		Column('non_cash_source_code_date_collected', DateTime(timezone=True)),

	# dbCol: non_cash_source_other
		Column('non_cash_source_other', String(50)),
		Column('non_cash_source_other_date_collected', DateTime(timezone=True)),

        ### person_address (subtable)

	# dbCol: person_email (What is a String?  How long if undefined?  Is this VarChar(max))
		Column('person_email', String),
		Column('person_email_date_collected', DateTime(timezone=True)),

	# dbCol: person_phone_number (What is a String?  How long if undefined?  Is this VarChar(max))
		Column('person_phone_number', String),
		Column('person_phone_number_date_collected', DateTime(timezone=True)),

    # dbCol: physical_disability
        Column('physical_disability', Integer),
        Column('physical_disability_data_col_stage', Integer),
        Column('physical_disability_date_collected', DateTime(timezone=True)),
        Column('physical_disability_date_effective', DateTime(timezone=True)),

	# dbCol: pregnancy_status
		Column('pregnancy_status', Integer),
		Column('pregnancy_status_date_collected', DateTime(timezone=True)),

	# dbCol: prior_residence
		Column('prior_residence', Integer),
		Column('prior_residence_date_collected', DateTime(timezone=True)),

	# dbCol: prior_residence_other
		Column('prior_residence_other', String(50)),
		Column('prior_residence_other_date_collected', DateTime(timezone=True)),

	# dbCol: reason_for_leaving
		Column('reason_for_leaving', Integer),
		Column('reason_for_leaving_date_collected', DateTime(timezone=True)),

	# dbCol: reason_for_leaving_other
		Column('reason_for_leaving_other', String(50)),
		Column('reason_for_leaving_other_date_collected', DateTime(timezone=True)),

	# dbCol: school_last_enrolled_date
		Column('school_last_enrolled_date', Date),
		Column('school_last_enrolled_date_date_collected', DateTime(timezone=True)),

	# dbCol: school_name
		Column('school_name', String(50)),
		Column('school_name_date_collected', DateTime(timezone=True)),

	# dbCol: school_type
		Column('school_type', Integer),
		Column('school_type_date_collected', DateTime(timezone=True)),

	# dbCol: subsidy_other
		Column('subsidy_other', String(50)),
		Column('subsidy_other_date_collected', DateTime(timezone=True)),

	# dbCol: subsidy_type
		Column('subsidy_type', Integer),
		Column('subsidy_type_date_collected', DateTime(timezone=True)),

	# dbCol: substance_abuse_indefinite
		Column('substance_abuse_indefinite', Integer),
		Column('substance_abuse_indefinite_date_collected', DateTime(timezone=True)),

	# dbCol: substance_abuse_problem
		Column('substance_abuse_problem', Integer),
		Column('substance_abuse_problem_date_collected', DateTime(timezone=True)),

	# dbCol: total_income
		Column('total_income', Numeric(5,2)),
		Column('total_income_date_collected', DateTime(timezone=True)),

		###Veteran (subtable)

	# dbCol: vocational_training
		Column('vocational_training', Integer),
		Column('vocational_training_date_collected', DateTime(timezone=True)),

        useexisting = True
        )
        table_metadata.create_all()
        mapper(PersonHistorical, person_historical_table, properties={'children': relation(IncomeAndSources), 'children': relation(Veteran),'children': relation(HUDHomelessEpisodes),'children': relation(PersonAddress)})
        return
    
    def income_and_sources_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=True)
        income_and_sources_table = Table(
        'income_and_sources', 
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey(PersonHistorical.c.id)),
        Column('amount', Integer),
        Column('amount_date_collected', DateTime(timezone=True)),
        Column('income_source_code', Integer),
        Column('income_source_code_date_collected', DateTime(timezone=True)),
        Column('income_source_other', String(32)),
        Column('income_source_other_date_collected', DateTime(timezone=True)),
        useexisting = True)
        table_metadata.create_all()
        mapper(IncomeAndSources, income_and_sources_table)
        
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
        
    
    
    def member_map(self):
		table_metadata = MetaData(bind=self.pg_db, reflect=True)
		member_table = Table(
		'members',
		table_metadata,
        
        Column('id', Integer, primary_key=True),
        Column('household_index_id', Integer, ForeignKey(Household.c.id)),

	# dbCol: person_id_unhashed
		Column('person_id_unhashed', String(32)),
		Column('person_id_unhashed_date_collected', DateTime(timezone=True)),

	# dbCol: person_id_hashed
		Column('person_id_hashed', String(32)),
		Column('person_id_hashed_date_collected', DateTime(timezone=True)),

	# dbCol: relationship_to_head_of_household
		Column('relationship_to_head_of_household', String(32)),
		Column('relationship_to_head_of_household_date_collected', DateTime(timezone=True)),

		useexisting = True)
		table_metadata.create_all()

		mapper(Members, member_table)
		return
    
    def household_map(self):
		table_metadata = MetaData(bind=self.pg_db, reflect=True)
		household_table = Table(
		'household',
		table_metadata,
        
        Column('id', Integer, primary_key=True),

	# dbCol: household_idid_num
		Column('household_id_num', String(32)),
		Column('household_id_num_date_collected', DateTime(timezone=True)),

	# dbCol: household_idid_str
		Column('household_id_str', String(32)),
		Column('household_id_str_date_collected', DateTime(timezone=True)),

	# dbCol: head_of_household_id_unhashed
		Column('head_of_household_id_unhashed', String(32)),
		Column('head_of_household_id_unhashed_date_collected', DateTime(timezone=True)),

	# dbCol: head_of_household_id_hashed
		Column('head_of_household_id_hashed', String(32)),
		Column('head_of_household_id_hashed_date_collected', DateTime(timezone=True)),

		###Members (subtable)
        
		useexisting = True)
		table_metadata.create_all()

		mapper(Household, household_table, properties={'children': relation(Members)})
		return
    
    def release_of_information_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        release_of_information_table = Table(
        'release_of_information',
        table_metadata,
        
        Column('id', Integer, primary_key=True),
        Column('person_index_id', Integer, ForeignKey(Person.c.id)),

	# dbCol: release_of_information_idid_num
		Column('release_of_information_idid_num', String(32)),
		Column('release_of_information_idid_num_date_collected', DateTime(timezone=True)),

	# dbCol: release_of_information_idid_str
		Column('release_of_information_idid_str', String(32)),
		Column('release_of_information_idid_str_date_collected', DateTime(timezone=True)),

	# dbCol: site_service_idid_num
		Column('site_service_idid_num', String(32)),
		Column('site_service_idid_num_date_collected', DateTime(timezone=True)),

	# dbCol: site_service_idid_str
		Column('site_service_idid_str', String(32)),
		Column('site_service_idid_str_date_collected', DateTime(timezone=True)),

	# dbCol: documentation
		Column('documentation', String(32)),
		Column('documentation_date_collected', DateTime(timezone=True)),

	###EffectivePeriod (subtable)
    # dbCol: start_date
        Column('start_date', String(32)),
        Column('start_date_date_collected', DateTime(timezone=True)),
    
    # dbCol: end_date
        Column('end_date', String(32)),
        Column('end_date_date_collected', DateTime(timezone=True)),

	# dbCol: release_granted
		Column('release_granted', String(32)),
		Column('release_granted_date_collected', DateTime(timezone=True)),

		useexisting = True)

        table_metadata.create_all()
        
        mapper(ReleaseOfInformation, release_of_information_table)
        return

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
                self.parse_household(root_element)
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
        
    
    def parse_hud_homeless_episodes(self, element):
        ### xpPath Definitions
            xpHudHomelessEpisodes = 'hmis:HUDHomelessEpisodes'
        ### StartDate
            xpStartDate = 'hmis:StartDate'
            xpStartDateDateCollected = 'hmis:StartDate/@hmis:dateCollected'
        ### EndDate
            xpEndDate = 'hmis:EndDate'
            xpEndDateDateCollected = 'hmis:EndDate/@hmis:dateCollected'
        
        ### xpPath Parsing
            itemElements = element.xpath(xpHudHomelessEpisodes, namespaces={'hmis': self.hmis_namespace})
            if itemElements is not None:
                for item in itemElements:
                ### StartDate
                    fldName='start_date'
                    self.existence_test_and_add(fldName, item.xpath(xpStartDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='start_date_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### EndDate
                    fldName='end_date'
                    self.existence_test_and_add(fldName, item.xpath(xpEndDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='end_date_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    
                    self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                    
                ### HudHomelessEpisodes (Shred)
                    self.shred(self.parse_dict, HudHomelessEpisodes)

		### Parse any subtables
    def parse_veteran(self, element):
    ### xpPath Definitions
        xpVeteran = 'hmis:Veteran'
    ### ServiceEra
        xpServiceEra = 'hmis:ServiceEra'
        xpServiceEraDateCollected = 'hmis:ServiceEra/@hmis:dateCollected'
    ### MilitaryServiceDuration
        xpMilitaryServiceDuration = 'hmis:MilitaryServiceDuration'
        xpMilitaryServiceDurationDateCollected = 'hmis:MilitaryServiceDuration/@hmis:dateCollected'
    ### ServedInWarZone
        xpServedInWarZone = 'hmis:ServedInWarZone'
        xpServedInWarZoneDateCollected = 'hmis:ServedInWarZone/@hmis:dateCollected'
    ### WarZone
        xpWarZone = 'hmis:WarZone'
        xpWarZoneDateCollected = 'hmis:WarZone/@hmis:dateCollected'
    ### WarZoneOther
        xpWarZoneOther = 'hmis:WarZoneOther'
        xpWarZoneOtherDateCollected = 'hmis:WarZoneOther/@hmis:dateCollected'
    ### MonthsInWarZone
        xpMonthsInWarZone = 'hmis:MonthsInWarZone'
        xpMonthsInWarZoneDateCollected = 'hmis:MonthsInWarZone/@hmis:dateCollected'
    ### ReceivedFire
        xpReceivedFire = 'hmis:ReceivedFire'
        xpReceivedFireDateCollected = 'hmis:ReceivedFire/@hmis:dateCollected'
    ### MilitaryBranch
        xpMilitaryBranch = 'hmis:MilitaryBranch'
        xpMilitaryBranchDateCollected = 'hmis:MilitaryBranch/@hmis:dateCollected'
    ### MilitaryBranchOther
        xpMilitaryBranchOther = 'hmis:MilitaryBranchOther'
        xpMilitaryBranchOtherDateCollected = 'hmis:MilitaryBranchOther/@hmis:dateCollected'
    ### DischargeStatus
        xpDischargeStatus = 'hmis:DischargeStatus'
        xpDischargeStatusDateCollected = 'hmis:DischargeStatus/@hmis:dateCollected'
    ### DischargeStatusOther
        xpDischargeStatusOther = 'hmis:DischargeStatusOther'
        xpDischargeStatusOtherDateCollected = 'hmis:DischargeStatusOther/@hmis:dateCollected'
        
    ### xpPath Parsing
        itemElements = element.xpath(xpVeteran, namespaces={'hmis': self.hmis_namespace})
        
        if itemElements is not None:
            for item in itemElements:
            ### ServiceEra
                fldName='service_era'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEra, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='service_era_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServiceEraDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### MilitaryServiceDuration
                fldName='military_service_duration'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryServiceDuration, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='military_service_duration_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryServiceDurationDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### ServedInWarZone
                fldName='served_in_war_zone'
                self.existence_test_and_add(fldName, item.xpath(xpServedInWarZone, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='served_in_war_zone_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpServedInWarZoneDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### WarZone
                fldName='war_zone'
                self.existence_test_and_add(fldName, item.xpath(xpWarZone, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='war_zone_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpWarZoneDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### WarZoneOther
                fldName='war_zone_other'
                self.existence_test_and_add(fldName, item.xpath(xpWarZoneOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='war_zone_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpWarZoneOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### MonthsInWarZone
                fldName='months_in_war_zone'
                self.existence_test_and_add(fldName, item.xpath(xpMonthsInWarZone, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='months_in_war_zone_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMonthsInWarZoneDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### ReceivedFire
                fldName='received_fire'
                self.existence_test_and_add(fldName, item.xpath(xpReceivedFire, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='received_fire_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReceivedFireDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### MilitaryBranch
                fldName='military_branch'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranch, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='military_branch_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranchDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### MilitaryBranchOther
                fldName='military_branch_other'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranchOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='military_branch_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpMilitaryBranchOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### DischargeStatus
                fldName='discharge_status'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatus, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='discharge_status_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatusDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### DischargeStatusOther
                fldName='discharge_status_other'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatusOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='discharge_status_other_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDischargeStatusOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                
                self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
    
            ### Veteran (Shred)
                self.shred(self.parse_dict, Veteran)
    
    def parse_person_address(self, element):
        ### xpPath Definitions
            xpPersonAddress = 'hmis:PersonAddress'
        ### StartDate
            xpAddressPeriodStartDate = 'hmis:AddressPeriod/hmis:StartDate'
            xpAddressPeriodStartDateDateCollected = 'hmis:AddressPeriod/hmis:StartDate/@hmis:dateCollected'
        ### EndDate
            xpAddressPeriodEndDate = 'hmis:AddressPeriod/hmis:EndDate'
            xpAddressPeriodEndDateDateCollected = 'hmis:AddressPeriod/hmis:EndDate/@hmis:dateCollected'
        ### PreAddressLine
            xpPreAddressLine = 'hmis:PreAddressLine'
            xpPreAddressLineDateCollected = 'hmis:PreAddressLine/@hmis:dateCollected'
		### Line1
            xpLine1 = 'hmis:Line1'
            xpLine1DateCollected = 'hmis:Line1/@hmis:dateCollected'
		### Line2
            xpLine2 = 'hmis:Line2'
            xpLine2DateCollected = 'hmis:Line2/@hmis:dateCollected'
            ### City
            xpCity = 'hmis:City'
            xpCityDateCollected = 'hmis:City/@hmis:dateCollected'
            ### County
            xpCounty = 'hmis:County'
            xpCountyDateCollected = 'hmis:County/@hmis:dateCollected'
            ### State
            xpState = 'hmis:State'
            xpStateDateCollected = 'hmis:State/@hmis:dateCollected'
            ### ZIPCode
            xpZIPCode = 'hmis:ZIPCode'
            xpZIPCodeDateCollected = 'hmis:ZIPCode/@hmis:dateCollected'
            ### Country
            xpCountry = 'hmis:Country'
            xpCountryDateCollected = 'hmis:Country/@hmis:dateCollected'
            
            #*# is_last_permanent_zip
            xpIsLastPermanentZip = 'hmis:IsLastPermanentZIP'
            xpIsLastPermanentZipDateCollected = 'hmis:IsLastPermanentZIP/@hmis:dateCollected'
            
            #*# zip_quality_code
            xpZipQualityCode = 'hmis:ZIPQualityCode'
            xpZipQualityCodeDateCollected = 'hmis:ZIPQualityCode/@hmis:dateCollected'

            ### xpPath Parsing
            itemElements = element.xpath(xpPersonAddress, namespaces={'hmis': self.hmis_namespace})
            if itemElements is not None:
                for item in itemElements:
                    
                ### StartDate
                    test = item.xpath(xpAddressPeriodStartDate, namespaces={'hmis': self.hmis_namespace})
                    if len(test) > 0:
                        fldName='address_period_start_date'
                        self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodStartDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                        fldName='line2_date_collected'
                        self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    
                ### EndDate
                    test = item.xpath(xpAddressPeriodEndDate, namespaces={'hmis': self.hmis_namespace})
                    if len(test) > 0:
                        fldName='address_period_end_date'
                        self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodEndDate, namespaces={'hmis': self.hmis_namespace}), 'element_date')
                        fldName='address_period_end_date_date_collected'
                        self.existence_test_and_add(fldName, item.xpath(xpAddressPeriodEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    
                ### PreAddressLine
                    fldName='pre_address_line'
                    self.existence_test_and_add(fldName, item.xpath(xpPreAddressLine, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='pre_address_line_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpPreAddressLineDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### Line1
                    fldName='line1'
                    self.existence_test_and_add(fldName, item.xpath(xpLine1, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='line1_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpLine1DateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### Line2
                    fldName='line2'
                    self.existence_test_and_add(fldName, item.xpath(xpLine2, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='line2_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpLine2DateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### City
                    fldName='city'
                    self.existence_test_and_add(fldName, item.xpath(xpCity, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='city_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpCityDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### County
                    fldName='county'
                    self.existence_test_and_add(fldName, item.xpath(xpCounty, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='county_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpCountyDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### State
                    fldName='state'
                    self.existence_test_and_add(fldName, item.xpath(xpState, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='state_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpStateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### ZIPCode
                    fldName='zip_code'
                    self.existence_test_and_add(fldName, item.xpath(xpZIPCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='zip_code_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpZIPCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### Country
                    fldName='country'
                    self.existence_test_and_add(fldName, item.xpath(xpCountry, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='country_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpCountryDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    
                ### IsLastPermanentZip
                    fldName='is_last_permanent_zip'
                    self.existence_test_and_add(fldName, item.xpath(xpIsLastPermanentZip, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='is_last_permanent_zip_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpIsLastPermanentZipDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    
                ### ZipQualityCode
                    fldName='zip_quality_code'
                    self.existence_test_and_add(fldName, item.xpath(xpZipQualityCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='zip_quality_code_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpZipQualityCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')

                    self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
                
                    ### PersonAddress (Shred)
                    self.shred(self.parse_dict, PersonAddress)
            
    def parse_income_and_sources(self, item):
        ### xpPath Definitions
        ### Amount
            xpIncomeAndSources = 'hmis:IncomeAndSources'
            xpAmount = 'hmis:Amount'
            xpAmountDateCollected = 'hmis:Amount/@hmis:dateCollected'
        ### IncomeSourceCode
            xpIncomeSourceCode = 'hmis:IncomeSourceCode'
            xpIncomeSourceCodeDateCollected = 'hmis:IncomeSourceCode/@hmis:dateCollected'
        ### IncomeSourceOther
            xpIncomeSourceOther = 'hmis:IncomeSourceOther'
            xpIncomeSourceOtherDateCollected = 'hmis:IncomeSourceOther/@hmis:dateCollected'
            
        ### xpPath Parsing
            incomeSources =  item.xpath(xpIncomeAndSources, namespaces={'hmis': self.hmis_namespace})
            
            if incomeSources is not None:
                for income in incomeSources:
                ### Amount
                    fldName='amount'
                    self.existence_test_and_add(fldName, income.xpath(xpAmount, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='amount_date_collected'
                    self.existence_test_and_add(fldName, income.xpath(xpAmountDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### IncomeSourceCode
                    fldName='income_source_code'
                    self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceCode, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='income_source_code_date_collected'
                    self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceCodeDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### IncomeSourceOther
                    fldName='income_source_other'
                    self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceOther, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='income_source_other_date_collected'
                    self.existence_test_and_add(fldName, income.xpath(xpIncomeSourceOtherDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            
                    self.existence_test_and_add('person_historical_index_id', self.person_historical_index_id, 'no_handling')
        
                ### IncomeAndSources (Shred)
                    self.shred(self.parse_dict, IncomeAndSources)
        
    def parse_person_historical(self, person_tag):
        '''Looks for an PersonHistorical tag and related fields in the XML and persists it.'''      
        '''This code allows for multiple PersonHistorical per Person'''
        #Xpath query strings
        xpSvcParticipationPersonHistorical = 'hmis:SiteServiceParticipation/hmis:PersonHistorical'
        xpPersonHistorical = 'hmis:PersonHistorical'
        #I don't want the PersonID from the XML, as there could be two of the 
        #same PersonID within the same export.  Need the Person Table Index
        #So that's what is used.  See where this index is retrieved after the 
        #session flush.
        xpPersonHistoricalID = 'hmis:PersonHistoricalID/hmis:IDNum'
        xpPersonHistoricalIDDateCollected = 'hmis:PersonHistoricalID/hmis:IDNum/@hmis:dateCollected'
        xpPersonHistoricalIDStr = 'hmis:PersonHistoricalID/hmis:IDStr'
        xpPersonHistoricalIDStrDateCollected = 'hmis:PersonHistoricalID/hmis:IDStr/@hmis:dateCollected'
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
        # test if nothign was found, if so, run against the personHistorical as part of service participation
        if len(person_historical) == 0:
            person_historical = person_tag.xpath(xpSvcParticipationPersonHistorical, namespaces={'hmis': self.hmis_namespace})
        
        if (person_historical is not None) and len(person_historical) > 0:
            for item in person_historical:
                self.parse_dict = {}
                
                fldName='person_historical_id_num'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalID, namespaces={'hmis': self.hmis_namespace}), 'text')
                
                fldName='person_historical_id_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalIDDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                
                fldName='person_historical_id_str'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                
                fldName='person_historical_id_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpPersonHistoricalIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                
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
            
            ### Parse any subtables
                self.parse_hud_homeless_episodes(item) 
                self.parse_income_and_sources(item)
                self.parse_person_address(item) 
                self.parse_veteran(item)
                
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
                self.parse_release_of_information(item)
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
        
    def parse_household(self, element):
        ### xpPath Definitions
            xpHousehold = 'hmis:Household'
        ### HouseholdIDIDNum
            xpHouseholdIDIDNum = 'hmis:HouseholdID/hmis:IDNum'
            xpHouseholdIDIDNumDateCollected = 'hmis:HouseholdIDIDNum/@hmis:dateCollected'
        ### HouseholdIDIDStr
            xpHouseholdIDIDStr = 'hmis:HouseholdID/hmis:IDStr'
            xpHouseholdIDIDStrDateCollected = 'hmis:HouseholdID/hmis:IDStr/@hmis:dateCollected'
        ### HeadOfHouseholdIDUnhashed
            xpHeadOfHouseholdIDUnhashed = 'hmis:HeadOfHouseholdID/hmis:Unhashed'
            xpHeadOfHouseholdIDUnhashedDateCollected = 'hmis:HeadOfHouseholdID/hmis:Unhashed/@hmis:dateCollected'
        ### HeadOfHouseholdIDHashed
            xpHeadOfHouseholdIDHashed = 'hmis:HeadOfHouseholdID/hmis:Hashed'
            xpHeadOfHouseholdIDHashedDateCollected = 'hmis:HeadOfHouseholdID/hmis:Hashed/@hmis:dateCollected'
        ### xpPath Parsing
            itemElements = element.xpath(xpHousehold, namespaces={'hmis': self.hmis_namespace})
            if itemElements is not None:
                for item in itemElements:
                    self.parse_dict = {}
                ### HouseholdIDIDNum
                    fldName='household_id_num'
                    self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='household_id_num_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### HouseholdIDIDStr
                    fldName='household_id_str'
                    self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='household_id_str_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpHouseholdIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### HeadOfHouseholdIDUnhashed
                    fldName='head_of_household_id_unhashed'
                    self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='head_of_household_id_unhashed_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDUnhashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### HeadOfHouseholdIDHashed
                    fldName='head_of_household_id_hashed'
                    self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                    fldName='head_of_household_id_hashed_date_collected'
                    self.existence_test_and_add(fldName, item.xpath(xpHeadOfHouseholdIDHashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                ### Household (Shred)
                    self.shred(self.parse_dict, Household)
        
                ### Parse any subtables
                    self.parse_members(item)
            
    
    def parse_members(self, element):
        ### xpPath Definitions
            xpMembers = 'hmis:Members'
            xpMember = 'hmis:Member'
        ### PersonIDUnhashed
            xpPersonIDUnhashed = 'hmis:PersonID/hmis:Unhashed'
            xpPersonIDUnhashedDateCollected = 'hmis:PersonID/hmis:Unhashed/@hmis:dateCollected'
        ### PersonIDHashed
            xpPersonIDHashed = 'hmis:PersonID/hmis:Hashed'
            xpPersonIDHashedDateCollected = 'hmis:PersonID/hmis:Hashed/@hmis:dateCollected'
        ### RelationshipToHeadOfHousehold
            xpRelationshipToHeadOfHousehold = 'hmis:RelationshipToHeadOfHousehold'
            xpRelationshipToHeadOfHouseholdDateCollected = 'hmis:RelationshipToHeadOfHousehold/@hmis:dateCollected'
            
            ### xpPath Parsing
            # put a test first
            test = element.xpath(xpMembers, namespaces={'hmis': self.hmis_namespace})
            if len(test) > 0:
                # if the tag exists (under household) it will always be 1.  with many 'members' underneath it.
                itemElements = test[0].xpath(xpMember, namespaces={'hmis': self.hmis_namespace})
                if itemElements is not None:
                    for item in itemElements:
                        self.parse_dict = {}
                    ### PersonIDUnhashed
                        fldName='person_id_unhashed'
                        self.existence_test_and_add(fldName, item.xpath(xpPersonIDUnhashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                        fldName='person_id_unhashed_date_collected'
                        self.existence_test_and_add(fldName, item.xpath(xpPersonIDUnhashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    ### PersonIDHashed
                        fldName='person_id_hashed'
                        self.existence_test_and_add(fldName, item.xpath(xpPersonIDHashed, namespaces={'hmis': self.hmis_namespace}), 'text')
                        fldName='person_id_hashed_date_collected'
                        self.existence_test_and_add(fldName, item.xpath(xpPersonIDHashedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
                    ### RelationshipToHeadOfHousehold
                        fldName='relationship_to_head_of_household'
                        self.existence_test_and_add(fldName, item.xpath(xpRelationshipToHeadOfHousehold, namespaces={'hmis': self.hmis_namespace}), 'text')
                        fldName='relationship_to_head_of_household_date_collected'
                        self.existence_test_and_add(fldName, item.xpath(xpRelationshipToHeadOfHouseholdDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            
                        # Stuff the forgeign key in 
                        self.existence_test_and_add('household_index_id', self.household_index_id, 'no_handling')
            
                    ### Member (Shred)
                        self.shred(self.parse_dict, Members)
            
                    ### Parse any subtables
    
    def parse_release_of_information(self, element):
    ### xpPath Definitions
        xpReleaseOfInformation = 'hmis:ReleaseOfInformation'
    ### ReleaseOfInformationIDIDNum
        xpReleaseOfInformationIDIDNum = 'hmis:ReleaseOfInformationID/hmis:IDNum'
        xpReleaseOfInformationIDIDNumDateCollected = 'hmis:ReleaseOfInformationID/hmis:IDNum/@hmis:dateCollected'
    ### ReleaseOfInformationIDIDStr
        xpReleaseOfInformationIDIDStr = 'hmis:ReleaseOfInformationID/hmis:IDStr'
        xpReleaseOfInformationIDIDStrDateCollected = 'hmis:ReleaseOfInformationID/hmis:IDStr/@hmis:dateCollected'
    ### SiteServiceIDIDNum
        xpSiteServiceIDIDNum = 'hmis:SiteServiceID/hmis:IDNum'
        xpSiteServiceIDIDNumDateCollected = 'hmis:SiteServiceID/hmis:IDNum/@hmis:dateCollected'
    ### SiteServiceIDIDStr
        xpSiteServiceIDIDStr = 'hmis:SiteServiceID/hmis:IDStr'
        xpSiteServiceIDIDStrDateCollected = 'hmis:SiteServiceID/hmis:IDStr/@hmis:dateCollected'
    ### Documentation
        xpDocumentation = 'hmis:Documentation'
        xpDocumentationDateCollected = 'hmis:Documentation/@hmis:dateCollected'
    ### StartDate
        xpStartDate = 'hmis:EffectivePeriod/hmis:StartDate'
        xpStartDateDateCollected = 'hmis:EffectivePeriod/hmis:StartDate/@hmis:dateCollected'
    ### EndDate
        xpEndDate = 'hmis:EffectivePeriod/hmis:EndDate'
        xpEndDateDateCollected = 'hmis:EffectivePeriod/hmis:EndDate/@hmis:dateCollected'
    ### ReleaseGranted
        xpReleaseGranted = 'hmis:ReleaseGranted'
        xpReleaseGrantedDateCollected = 'hmis:ReleaseGranted/@hmis:dateCollected'

    ### xpPath Parsing
        itemElements = element.xpath(xpReleaseOfInformation, namespaces={'hmis': self.hmis_namespace})
        if itemElements is not None:
            for item in itemElements:
                
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                
            ### ReleaseOfInformationIDIDNum
                fldName='release_of_information_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='release_of_information_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### ReleaseOfInformationIDIDStr
                fldName='release_of_information_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='release_of_information_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseOfInformationIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### SiteServiceIDIDNum
                fldName='site_service_idid_num'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNum, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='site_service_idid_num_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDNumDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### SiteServiceIDIDStr
                fldName='site_service_idid_str'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStr, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='site_service_idid_str_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpSiteServiceIDIDStrDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ### Documentation
                fldName='documentation'
                self.existence_test_and_add(fldName, item.xpath(xpDocumentation, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='documentation_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpDocumentationDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ###* StartDate (DateRange)
                fldName='start_date'
                self.existence_test_and_add(fldName, item.xpath(xpStartDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='start_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpStartDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
            ###* EndDate (DateRange)
                fldName='end_date'
                self.existence_test_and_add(fldName, item.xpath(xpEndDate, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='end_date_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpEndDateDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')                
            ### ReleaseGranted
                fldName='None'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseGranted, namespaces={'hmis': self.hmis_namespace}), 'text')
                fldName='None_date_collected'
                self.existence_test_and_add(fldName, item.xpath(xpReleaseGrantedDateCollected, namespaces={'hmis': self.hmis_namespace}), 'attribute_date')
    
            ### ReleaseOfInformation (Shred)
                self.shred(self.parse_dict, ReleaseOfInformation)
            
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
        if mapping.__name__ == "Household":
            self.household_index_id = mapped.id
        if mapping.__name__ == "PersonHistorical":
            self.person_historical_index_id = mapped.id
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
            
class Veteran(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
            
class HUDHomelessEpisodes(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
            
class IncomeAndSources(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
            
class PersonAddress(object):
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
            
class ReleaseOfInformation(object):
    def __init__(self, field_dict):
		print field_dict
		for x, y in field_dict.iteritems():
			self.__setattr__(x,y)

class Household(object):
    def __init__(self, field_dict):
        print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
            
class Members(object):
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
    
    if settings.DB_PASSWD == "":
        settings.DB_PASSWD = raw_input("Please enter your password: ")
    
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