#!/usr/bin/env python

from sqlalchemy import create_engine, Table, Column, Numeric, Integer, String, Boolean, MetaData, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, mapper, backref, relation, clear_mappers
from sqlalchemy.types import DateTime, Date
from sqlalchemy import exceptions as sqlalchemyexceptions
import sys
from conf import settings
import clsLogger

from fileUtils import fileUtilities

class databaseObjects:
    
    def __init__(self):
        try:
            self.pg_db = create_engine('postgres://%s:%s@localhost:%s/%s' % \
                        (settings.DB_USER, settings.DB_PASSWD, settings.DB_PORT, settings.DB_DATABASE), echo=settings.DEBUG_ALCHEMY)#, server_side_cursors=True)

            log = clsLogger.clsLogger()
            #logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
            #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
            log.getLogger('sqlalchemy.orm.unitofwork').setLevel(log.LEVELS.get('error'))
            #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
            #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
            
            self.session = sessionmaker(bind=self.pg_db, autoflush=True, transactional=True)
            
            # map the ORM
            clear_mappers()
            self.createMappings()
            
        except sqlalchemyexceptions.OperationalError:
            msg = "Database [%s] does not exist." % settings.DB_DATABASE
            FU = fileUtilities(settings.DEBUG, None)
            FU.makeBlock(msg)
            rc = raw_input('Would you like to create the database now? (y/N/C)')
            if rc == 'y':
                import postgresutils
                UTILS = postgresutils.Utils()
                UTILS.create_database(settings.DB_DATABASE)
            else:
                msg = "Please create Database [%s] and restart process." % settings.DB_DATABASE
                FU.makeBlock(msg)


        
    def queryDB(self, object):
        return self.session.query(object)
        
    def createMappings(self):
        self.export_map()
        self.source_map()
        self.person_map()
        self.site_service_participation_map()
        self.need_map()
        self.service_event_map()
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
        
    def service_event_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        service_event_table = Table(
        'service_event',
        table_metadata,
        
        Column('id', Integer, primary_key=True),
        Column('site_service_index_id', Integer, ForeignKey(SiteServiceParticipation.c.id)),

    # dbCol: service_event_idid_num
        Column('service_event_idid_num', String(32)),
        Column('service_event_idid_num_date_collected', DateTime(timezone=True)),
    
    # dbCol: service_event_idid_str
        Column('service_event_idid_str', String(32)),
        Column('service_event_idid_str_date_collected', DateTime(timezone=True)),
    
    # dbCol: household_idid_num
        Column('household_idid_num', String(32)),
        Column('household_idid_num_date_collected', DateTime(timezone=True)),
    
    # dbCol: household_idid_str
        Column('household_idid_str', String(32)),
        Column('household_idid_str_date_collected', DateTime(timezone=True)),
    
    # dbCol: is_referral
        Column('is_referral', String(32)),
        Column('is_referral_date_collected', DateTime(timezone=True)),
    
    # dbCol: quantity_of_service
        Column('quantity_of_service', String(32)),
        Column('quantity_of_service_date_collected', DateTime(timezone=True)),
    
    # dbCol: quantity_of_service_measure
        Column('quantity_of_service_measure', String(32)),
        Column('quantity_of_service_measure_date_collected', DateTime(timezone=True)),
    
    # dbCol: service_airs_code
        Column('service_airs_code', String(32)),
        Column('service_airs_code_date_collected', DateTime(timezone=True)),
    
        ###ServicePeriod (subtable)
    ### ServicePeriod
    # ParticipationDates (Start Date/End Date)
        Column('service_period_start_date', DateTime(timezone=True)),
        Column('service_period_start_date_date_collected', DateTime(timezone=True)),
        
        Column('service_period_end_date', DateTime(timezone=True)),
        Column('service_period_end_date_date_collected', DateTime(timezone=True)),
    
    # dbCol: service_unit
        Column('service_unit', String(32)),
        Column('service_unit_date_collected', DateTime(timezone=True)),
    
    # dbCol: type_of_service
        Column('type_of_service', String(32)),
        Column('type_of_service_date_collected', DateTime(timezone=True)),
    
    # dbCol: type_of_service_other
        Column('type_of_service_other', String(32)),
        Column('type_of_service_other_date_collected', DateTime(timezone=True)),
    
        useexisting = True)
        table_metadata.create_all()
    
        mapper(ServiceEvent, service_event_table)#, properties={'children': relation(#tablename#), 'children': relation(#tablename#), 'children': relation(#tablename#)})
        return

    def need_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        need_table = Table(
        'need',
        table_metadata,
        
        Column('id', Integer, primary_key=True),
        Column('site_service_index_id', Integer, ForeignKey(SiteServiceParticipation.c.id)),
    
    # dbCol: need_idid_num
        Column('need_idid_num', String(32)),
        Column('need_idid_num_date_collected', DateTime(timezone=True)),
    
    # dbCol: need_idid_str
        Column('need_idid_str', String(32)),
        Column('need_idid_str_date_collected', DateTime(timezone=True)),
    
    # dbCol: site_service_idid_num
        Column('site_service_idid_num', String(32)),
        Column('site_service_idid_num_date_collected', DateTime(timezone=True)),
    
    # dbCol: site_service_idid_str
        Column('site_service_idid_str', String(32)),
        Column('site_service_idid_str_date_collected', DateTime(timezone=True)),
    
    # dbCol: service_event_idid_num
        Column('service_event_idid_num', String(32)),
        Column('service_event_idid_num_date_collected', DateTime(timezone=True)),
    
    # dbCol: service_event_idid_str
        Column('service_event_idid_str', String(32)),
        Column('service_event_idid_str_date_collected', DateTime(timezone=True)),
    
    # dbCol: need_status
        Column('need_status', String(32)),
        Column('need_status_date_collected', DateTime(timezone=True)),
    
    # dbCol: taxonomy
        Column('taxonomy', String(32)),
    
        useexisting = True)
        table_metadata.create_all()
    
        mapper(Need, need_table)#, properties={'children': relation(#tablename#), 'children': relation(#tablename#), 'children': relation(#tablename#)})
        return

    def site_service_participation_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        site_service_participation_table = Table(
        'site_service_participation',
        table_metadata,
        
        Column('id', Integer, primary_key=True),

    # dbCol: site_service_participation_idid_num
        Column('site_service_participation_idid_num', String(32)),
        Column('site_service_participation_idid_num_date_collected', DateTime(timezone=True)),

    # dbCol: site_service_participation_idid_str
        Column('site_service_participation_idid_str', String(32)),
        Column('site_service_participation_idid_str_date_collected', DateTime(timezone=True)),

    # dbCol: site_service_idid_num
        Column('site_service_idid_num', String(32)),
        Column('site_service_idid_num_date_collected', DateTime(timezone=True)),

    # dbCol: site_service_idid_str
        Column('site_service_idid_str', String(32)),
        Column('site_service_idid_str_date_collected', DateTime(timezone=True)),

    # dbCol: household_idid_num
        Column('household_idid_num', String(32)),
        Column('household_idid_num_date_collected', DateTime(timezone=True)),

    # dbCol: household_idid_str
        Column('household_idid_str', String(32)),
        Column('household_idid_str_date_collected', DateTime(timezone=True)),

    # dbCol: destination
        Column('destination', String(32)),
        Column('destination_date_collected', DateTime(timezone=True)),

    # dbCol: destination_other
        Column('destination_other', String(32)),
        Column('destination_other_date_collected', DateTime(timezone=True)),

    # dbCol: destination_tenure
        Column('destination_tenure', String(32)),
        Column('destination_tenure_date_collected', DateTime(timezone=True)),

    # dbCol: disabling_condition
        Column('disabling_condition', String(32)),
        Column('disabling_condition_date_collected', DateTime(timezone=True)),

    # ParticipationDates (Start Date/End Date)
        Column('participation_dates_start_date', DateTime(timezone=True)),
        Column('participation_dates_start_date_date_collected', DateTime(timezone=True)),
        
        Column('participation_dates_end_date', DateTime(timezone=True)),
        Column('participation_dates_end_date_date_collected', DateTime(timezone=True)),

    # dbCol: veteran_status
        Column('veteran_status', String(32)),
        Column('veteran_status_date_collected', DateTime(timezone=True)),
        
        ###Need (subtable)

        ###ServiceEvent (subtable)

        useexisting = True)
        table_metadata.create_all()
        
        mapper(SiteServiceParticipation, site_service_participation_table, properties={'fk_participation_to_need': relation(Need, backref='fk_need_to_participation'),
                                                                                       'fk_participation_to_serviceevent' : relation(ServiceEvent) }
               )#, 'children': relation(#tablename#), 'children': relation(#tablename#)})
        return
        
    def races_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=False)
        races_table = Table(
        'races', 
        table_metadata, 
        Column('id', Integer, primary_key=True),
        Column('person_index_id', Integer, ForeignKey(Person.c.id)),
        Column('race_unhashed', Integer(2)),
        Column('race_hashed', String(32)),
        Column('race_date_collected', DateTime(timezone=True)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Races, races_table)
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
        mapper(Export, export_table, properties={
            'fk_export_to_person': relation(Person, backref='fk_person_to_export')
            ,'fk_export_to_database': relation(Source, backref='fk_database_to_export')
            })
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
        
        mapper(Person, person_table, properties={
            'fk_person_to_other_names': relation(OtherNames, backref='fk_other_names_to_person')
            ,'fk_person_to_person_historical': relation(PersonHistorical, backref='fk_person_historical_to_person')
            ,'fk_person_to_release_of_information': relation(ReleaseOfInformation, backref='fk_release_of_information_to_person')
            ,'fk_person_to_races': relation(Races, backref='fk_races_to_person')})
        #
        
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
        mapper(PersonHistorical, person_historical_table,
               properties={'fk_person_historical_to_income_and_sources': relation(IncomeAndSources, backref='fk_income_and_sources_to_person_historical')
                           ,'fk_person_historical_to_veteran': relation(Veteran, backref='fk_veteran_to_person_historical')
                           ,'fk_person_historical_to_hud_homeless_episodes': relation(HUDHomelessEpisodes, backref='fk_hud_homeless_episodes_to_person_historical')
                           ,'fk_person_historical_to_person_address': relation(PersonAddress, backref='fk_person_address_to_person_historical')
                           })
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
    
        mapper(Household, household_table, properties={'fk_household_to_members': relation(Members, backref='fk_members_to_household')})
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

    def source_map(self):
        '''Set up mapping'''
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=False)
        self.source_table = Table(
        'source', 
        table_metadata, 
        Column('id', Integer, primary_key=True),
        Column('export_id', String(50), ForeignKey(Export.c.export_id)), 
        Column('source_id', String(50)), 
        Column('source_id_date_collected', DateTime(timezone=True)),
        Column('source_email', String(50)),
        Column('source_email_date_collected', DateTime(timezone=True)),
        Column('source_contact_extension', String(10)),
        Column('source_contact_extension_date_collected', DateTime(timezone=True)),
        Column('source_contact_first', String(20)),
        Column('source_contact_first_date_collected', DateTime(timezone=True)),
        Column('source_contact_last', String(20)),
        Column('source_contact_last_date_collected', DateTime(timezone=True)),
        Column('source_contact_phone', String(20)),
        Column('source_contact_phone_date_collected', DateTime(timezone=True)),
        Column('source_name', String(50)),
        Column('source_name_date_collected', DateTime(timezone=True)), 
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Source, self.source_table)
#        assign_mapper(Database, database_table, properties=dict(
#designs=relation(Design, private=True, backref="type")
#))
        return

class baseObject(object):
    def __init__(self, field_dict):
        if settings.DEBUG:
            print "Base Class created: %s" % self.__class__.__name__
    #def __init__(self, field_dict):
        if settings.DEBUG:
            print field_dict
        for x, y in field_dict.iteritems():
            self.__setattr__(x,y)
        
    def __repr__(self):
        field_dict = vars(self)
        out = ''
        if len(field_dict) > 0:
            for x, y in field_dict.iteritems():
                if x[0] != "_":
                    out = out + "%s = %s, " % (x,y)
                    
            return "<%s(%s)>" % (self.__class__.__name__, out)
        else:
            return ''
        
class Source(baseObject):
    pass

class Export(baseObject):
    pass
        
class OtherNames(baseObject):
    pass

class Person(baseObject):
    pass

class ServiceEvent(baseObject):
    pass

class Need(baseObject):
    pass

class SiteServiceParticipation(baseObject):
    pass
                        
class Veteran(baseObject):
    pass    
            
class HUDHomelessEpisodes(baseObject):
    pass
            
class IncomeAndSources(baseObject):
    pass
            
class PersonAddress(baseObject):
    pass
            
class PersonHistorical(baseObject):
    pass
   
class Races(baseObject):
    pass
            
class ReleaseOfInformation(baseObject):
    pass

class Household(baseObject):
    pass
            
class Members(baseObject):
    pass
            
            
def main(argv=None):  
    if argv is None:
        argv = sys.argv
    
    if settings.DB_PASSWD == "":
        settings.DB_PASSWD = raw_input("Please enter your password: ")
        
    #pg_db = create_engine('postgres://%s:%s@localhost:5432/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_DATABASE), echo=settings.DEBUG_ALCHEMY)#, server_side_cursors=True)
    
    mappedObjects = databaseObjects()
    
    # Query Exports for Data
    print 'Export'
    for export in mappedObjects.queryDB(Export):
        print export.export_software_vendor
        dbo = export.fk_export_to_database
        dir(dbo)
    
    # Person records
    print 'All Persons'
    print '-----------------------------------'
    for field in mappedObjects.queryDB(Person):
        print "New Person"
        print '------'
        print field.person_date_of_birth_unhashed
        print field.person_legal_first_name_unhashed
        print field.person_legal_last_name_unhashed
        print '------'
        
    print 'Person: George Washington'
    print '-----------------------------------'
    for person in mappedObjects.queryDB(Person).filter(Person.person_legal_first_name_unhashed=='George'):
        print person.person_legal_first_name_unhashed
    print '-----------------------------------'
        
    # All Persons
    query = mappedObjects.queryDB(Person).filter("export_id='1'")
    print query.count()
    query = mappedObjects.queryDB(Person).filter("export_id='1'").first()
    print query
    
    # get their PersonHistorical records
    print 'Person: George Washington'
    print '-----------------------------------'
    for person in mappedObjects.queryDB(Person).filter(Person.person_legal_first_name_unhashed=='George'):
        print person.person_legal_first_name_unhashed
        #print person.person_historical
        for ph in person.fk_person_to_person_historical:
            print '-------'
            print ph.employment_tenure
            print '-------'
            for ias in ph.fk_person_historical_to_income_and_sources:
                print "IAS:Amount: %s" % ias.amount
    print '-----------------------------------'

if __name__ == "__main__":
    sys.exit(main())             
            
            