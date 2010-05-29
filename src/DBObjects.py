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

    
    # instance variables
    pg_db = create_engine('postgres://%s:%s@%s:%s/%s' % \
            (settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_PORT, settings.DB_DATABASE) ,echo=settings.DEBUG_ALCHEMY)#, server_side_cursors=True)
    # this is needed to do real work.
    session = sessionmaker(bind=pg_db, autoflush=True, transactional=True)
    
    def __init__(self):
        try:
            
            # SBB20100210 Change the logging level based on configuration file.
            if settings.DEBUG_ALCHEMY:
                loglevel = 'info'
            else:
                loglevel = 'error'
                
            log = clsLogger.clsLogger(loglevel=loglevel)
                
            ###log.getLogger('sqlalchemy.engine').setLevel(log.LEVELS.get(loglevel))
            
            #log.getLogger('sqlalchemy.orm').setLevel(log.LEVELS.get(loglevel))
            #log.getLogger('sqlalchemy.orm.unitofwork').setLevel(log.LEVELS.get(loglevel))
            log.getLogger('sqlalchemy.orm.unitofwork').setLevel(log.logger.info)
            ###log.getLogger('sqlalchemy.orm.unitofwork').setLevel(log.LEVELS.get(loglevel))
            #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
            #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
                    
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
        #session = self.session()
        return self.session().query(object)
        
    def createMappings(self):
        self.export_map()
        self.source_map()
        self.source_export_link_2010_map()
        self.region_2010_map()
        self.agency_2010_map()
        self.agency_child_2010_map()
        self.service_2010_map()
        self.site_2010_map()
        self.site_service_2010_map()
        self.person_map()
        self.site_service_participation_map()
        self.need_map()
        self.service_event_map()
        self.person_historical_map()
        self.release_of_information_map()
        self.income_and_sources_map()
        self.veteran_map()
        self.drug_history_map()
        self.emergency_contact_map()
        self.hud_homeless_episodes_map()
        self.person_address_map()
        self.other_names_map()
        self.races_map()
        self.household_map()
        self.member_map()       
        self.funding_source_2010_map()       
        self.inventory_2010_map()       
                
        # SBB20100303 Adding objects to deduplicate the DB Entries
        self.dedup_link_map()
        # SBB20100327 adding object to maintain odbid's for each site.  Svcpoint requires these for valid xml uploads
        self.system_configuration_map()
        
    def system_configuration_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=True)
        system_configuration_table = Table(
        'sender_system_configuration', 
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('vendor_name', String(50)),
        Column('processing_mode', String(4)),                   # TEST or PROD
        Column('source_id', String(50)),
        Column('odbid', Integer),
        Column('providerid', Integer),
        Column('userid', Integer),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(SystemConfiguration, system_configuration_table) 
        return
        
    def dedup_link_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        #table_metadata = MetaData(bind=self.sqlite_db, reflect=True)
        dedup_link_table = Table(
        'dedup_link', 
        table_metadata, 
        Column('source_rec_id', String(50), primary_key=True),
        Column('destination_rec_id', String(50)), 
        Column('weight_factor', Integer),
        useexisting = True
        )
        table_metadata.create_all()
        #mapper(dedup_link, export_table, properties={'children': [relation(Person), relation(Database)]})
        #mapper(Export, export_table, properties={'children': relation(Person), 'children': relation(Database)})
        return
    
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
        
    # dbCol: type_of_service_par (Operations PARS)
        Column('type_of_service_par', Integer(2)),
        
    # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        ## HUD 3.0
        Column('person_index_id_2010', Integer, ForeignKey(Person.c.id)),
        Column('need_index_id_2010', Integer, ForeignKey(Need.c.id)),
        Column('service_event_id_delete_2010', Integer),
        Column('service_event_ind_fam_2010', Integer),
        Column('site_service_id_2010', String(50)),
        Column('hmis_service_event_code_type_of_service_2010', String(50)),
        Column('hmis_service_event_code_type_of_service_other_2010', String(50)),
        Column('hprp_financial_assistance_service_event_code_2010', String(50)),
        Column('hprp_relocation_stabilization_service_event_code_2010', String(50)),
        Column('service_event_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('service_event_id_delete_effective_2010', DateTime(timezone=True)),
        Column('service_event_provision_date_2010', DateTime(timezone=True)),
        Column('service_event_recorded_date_2010', DateTime(timezone=True)),


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
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        ## HUD 3.0
        Column('person_index_id_2010', Integer, ForeignKey(Person.c.id)),
        Column('need_id_delete_2010', Integer),
        Column('need_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('need_id_delete_delete_effective_2010', DateTime(timezone=True)),
        Column('need_effective_period_start_date_2010', DateTime(timezone=True)),
        Column('need_effective_period_end_date_2010', DateTime(timezone=True)),
        Column('need_recorded_date_2010', DateTime(timezone=True)),

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
        Column('person_index_id', Integer, ForeignKey(Person.c.id)),

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

    # dbCol: discharge_type (Operations PARS)
    #    Column('discharge_type', Integer(2)),
    #    Column('discharge_type_date_collected', DateTime(timezone=True)),
    #
    ## dbCol: health_status_at_discharge (Operations PARS)
    #    Column('health_status_at_discharge', Integer(2)),
    #    Column('health_status_at_discharge_date_collected', DateTime(timezone=True)),
    #
    ## dbCol: va_eligibility (Operations PARS)
    #    Column('va_eligibility', Integer(2)),
    #    Column('va_eligibility_date_collected', DateTime(timezone=True)),
        
        ###Need (subtable)

        ###ServiceEvent (subtable)
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        ## HUD 3.0
        Column('site_service_participation_id_delete_2010', Integer),
        Column('site_service_participation_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('site_service_participation_id_delete_effective_2010', DateTime(timezone=True)),
        
        useexisting = True)
        table_metadata.create_all()
        
        mapper(SiteServiceParticipation, site_service_participation_table, properties={'fk_participation_to_need': relation(Need, backref='fk_need_to_participation'),
                                                                                       'fk_participation_to_serviceevent' : relation(ServiceEvent),
                                                                                       'fk_participation_to_personhistorical' : relation(PersonHistorical),
                                                                                       'fk_participation_to_person' : relation(Person)
                                                                                       }
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
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        ## HUD 3.0
        Column('race_data_collection_stage_2010', Integer),
        Column('race_date_effective_2010', DateTime(timezone=True)),
                
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
        Column('export_id', String(50), primary_key=True, unique=True), 
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

        ## HUD 3.0
        Column('export_id_id_id_num_2010', String(50)),
        Column('export_id_id_id_str_2010', String(50)),
        Column('export_id_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('export_id_id_delete_effective_2010', DateTime(timezone=True)),        
        Column('export_id_id_delete_2010', Integer),        
        useexisting = True
        )
        table_metadata.create_all()
        #mapper(Export, export_table, properties={'children': [relation(Person), relation(Database)]})
        mapper(Export, export_table, properties={
            'fk_export_to_person': relation(Person, backref='fk_person_to_export')
            ,'fk_export_to_household': relation(Household, backref='fk_household_to_export')
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
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),
        
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Veteran, veteran_table)
        return

    def drug_history_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        drug_history_table = Table(
        'drug_history',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey(PersonHistorical.c.id)),

        # dbCol: drug_history_id
            Column('drug_history_id', String(32)),
            Column('drug_history_id_date_collected', DateTime(timezone=True)),
        # dbCol: drug_code
            Column('drug_code', Integer(2)),
            Column('drug_code_date_collected', DateTime(timezone=True)),    
        # dbCol: drug_use_frequency
            Column('drug_use_frequency', Integer(2)),
            Column('drug_use_frequency_date_collected', DateTime(timezone=True)),

        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        useexisting = True
        )
        table_metadata.create_all()
        mapper(DrugHistory, drug_history_table)
        return

    def emergency_contact_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        emergency_contact_table = Table(
        'emergency_contact',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey(PersonHistorical.c.id)),

        # dbCol: emergency_contact_id
            Column('emergency_contact_id', String(32)),
            Column('emergency_contact_id_date_collected', DateTime(timezone=True)),
        # dbCol: emergency_contact_name
            Column('emergency_contact_name', String(32)),
            Column('emergency_contact_name_date_collected', DateTime(timezone=True)),    
        # dbCol: emergency_contact_phone_number-0
            Column('emergency_contact_phone_number_0', String(32)),
            Column('emergency_contact_phone_number_date_collected_0', DateTime(timezone=True)),
            Column('emergency_contact_phone_number_type_0', String(32)),
        # dbCol: emergency_contact_phone_number-1
            Column('emergency_contact_phone_number_1', String(32)),
            Column('emergency_contact_phone_number_date_collected_1', DateTime(timezone=True)),
            Column('emergency_contact_phone_number_type_1', String(32)),
        # dbCol: emergency_contact_address
            Column('emergency_contact_address_date_collected', DateTime(timezone=True)),
        # dbCol: emergency_contact_address_start_date
            Column('emergency_contact_address_start_date', DateTime(timezone=True)),
            Column('emergency_contact_address_start_date_date_collected', DateTime(timezone=True)),
        # dbCol: emergency_contact_address_end_date
            Column('emergency_contact_address_end_date', DateTime(timezone=True)),
            Column('emergency_contact_address_end_date_date_collected', DateTime(timezone=True)),
        # dbCol: emergency_contact_address_line1
            Column('emergency_contact_address_line1', String(32)),
            Column('emergency_contact_address_line1_date_collected', DateTime(timezone=True)),
        # dbCol: emergency_contact_address_line2
            Column('emergency_contact_address_line2', String(32)),
            Column('emergency_contact_address_line2_date_collected', DateTime(timezone=True)),
        # dbCol: emergency_contact_address_city
            Column('emergency_contact_address_city', String(32)),
            Column('emergency_contact_address_city_date_collected', DateTime(timezone=True)),
        # dbCol: emergency_contact_address_state
            Column('emergency_contact_address_state', String(32)),
            Column('emergency_contact_address_state_date_collected', DateTime(timezone=True)),    
        # dbCol: emergency_contact_relation_to_client
            Column('emergency_contact_relation_to_client', String(32)),
            Column('emergency_contact_relation_to_client_date_collected', DateTime(timezone=True)),
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        useexisting = True
        )
        table_metadata.create_all()
        mapper(EmergencyContact, emergency_contact_table)
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
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        ## HUD 3.0
        Column('attr_delete_2010', Integer),
        Column('attr_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('attr_effective_2010', DateTime(timezone=True)),        
        
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
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),
        
        ## HUD 3.0
        Column('person_id_id_num_2010', String(50)),
        Column('person_id_id_str_2010', String(50)),
        Column('person_id_delete_2010', Integer),
        Column('person_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('person_id_delete_effective_2010', DateTime(timezone=True)),
        
        useexisting = True)
        table_metadata.create_all()
        
        mapper(Person, person_table, properties={
            'fk_person_to_other_names': relation(OtherNames, backref='fk_other_names_to_person')
            ,'fk_person_to_site_svc_part': relation(SiteServiceParticipation, backref='fk_site_svc_part_to_person')
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
        Column('site_service_index_id', Integer, ForeignKey(SiteServiceParticipation.c.id)),
        
    # dbCol: person_historical_idid_num
        Column('person_historical_idid_num', String(32)),
        Column('person_historical_idid_num_date_collected', DateTime(timezone=True)),
    
    # dbCol: person_historical_idid_str
        Column('person_historical_idid_str', String(32)),
        Column('person_historical_idid_str_date_collected', DateTime(timezone=True)),
    
    # dbCol: barrier_code
        Column('barrier_code', String(32)),
        Column('barrier_code_date_collected', DateTime(timezone=True)),
    
    # dbCol: barrier_other
        Column('barrier_other', String(32)),
        Column('barrier_other_date_collected', DateTime(timezone=True)),
    
    # dbCol: child_currently_enrolled_in_school
        Column('child_currently_enrolled_in_school', String(32)),
        Column('child_currently_enrolled_in_school_date_collected', DateTime(timezone=True)),
    
    # dbCol: currently_employed
        Column('currently_employed', String(32)),
        Column('currently_employed_date_collected', DateTime(timezone=True)),
    
    # dbCol: currently_in_school
        Column('currently_in_school', String(32)),
        Column('currently_in_school_date_collected', DateTime(timezone=True)),
    
    # dbCol: degree_code
        Column('degree_code', String(32)),
        Column('degree_code_date_collected', DateTime(timezone=True)),
    
    # dbCol: degree_other
        Column('degree_other', String(32)),
        Column('degree_other_date_collected', DateTime(timezone=True)),
    
    # dbCol: developmental_disability
        Column('developmental_disability', String(32)),
        Column('developmental_disability_date_collected', DateTime(timezone=True)),
    
    # dbCol: domestic_violence
        Column('domestic_violence', String(32)),
        Column('domestic_violence_date_collected', DateTime(timezone=True)),
    
    # dbCol: domestic_violence_how_long
        Column('domestic_violence_how_long', String(32)),
        Column('domestic_violence_how_long_date_collected', DateTime(timezone=True)),
    
    # dbCol: due_date
        Column('due_date', String(32)),
        Column('due_date_date_collected', DateTime(timezone=True)),
    
    # dbCol: employment_tenure
        Column('employment_tenure', String(32)),
        Column('employment_tenure_date_collected', DateTime(timezone=True)),
    
    # dbCol: health_status
        Column('health_status', String(32)),
        Column('health_status_date_collected', DateTime(timezone=True)),
    
    # dbCol: highest_school_level
        Column('highest_school_level', String(32)),
        Column('highest_school_level_date_collected', DateTime(timezone=True)),
    
    # dbCol: hivaids_status
        Column('hivaids_status', String(32)),
        Column('hivaids_status_date_collected', DateTime(timezone=True)),
    
    # dbCol: hours_worked_last_week
        Column('hours_worked_last_week', String(32)),
        Column('hours_worked_last_week_date_collected', DateTime(timezone=True)),
    
    # dbCol: hud_chronic_homeless
        Column('hud_chronic_homeless', String(32)),
        Column('hud_chronic_homeless_date_collected', DateTime(timezone=True)),
    
    # dbCol: hud_homeless
        Column('hud_homeless', String(32)),
        Column('hud_homeless_date_collected', DateTime(timezone=True)),
    
        ###HUDHomelessEpisodes (subtable)
    
        ###IncomeAndSources (subtable)
    
    # dbCol: length_of_stay_at_prior_residence
        Column('length_of_stay_at_prior_residence', String(32)),
        Column('length_of_stay_at_prior_residence_date_collected', DateTime(timezone=True)),
    
    # dbCol: looking_for_work
        Column('looking_for_work', String(32)),
        Column('looking_for_work_date_collected', DateTime(timezone=True)),
    
    # dbCol: mental_health_indefinite
        Column('mental_health_indefinite', String(32)),
        Column('mental_health_indefinite_date_collected', DateTime(timezone=True)),
    
    # dbCol: mental_health_problem
        Column('mental_health_problem', String(32)),
        Column('mental_health_problem_date_collected', DateTime(timezone=True)),
    
    # dbCol: non_cash_source_code
        Column('non_cash_source_code', String(32)),
        Column('non_cash_source_code_date_collected', DateTime(timezone=True)),
    
    # dbCol: non_cash_source_other
        Column('non_cash_source_other', String(32)),
        Column('non_cash_source_other_date_collected', DateTime(timezone=True)),
    
        ###PersonAddress (subtable)
    
    # dbCol: person_email
        Column('person_email', String(32)),
        Column('person_email_date_collected', DateTime(timezone=True)),
    
    # dbCol: person_phone_number
        Column('person_phone_number', String(32)),
        Column('person_phone_number_date_collected', DateTime(timezone=True)),
    
    # dbCol: physical_disability
        Column('physical_disability', String(32)),
        Column('physical_disability_date_collected', DateTime(timezone=True)),
    
    # dbCol: pregnancy_status
        Column('pregnancy_status', String(32)),
        Column('pregnancy_status_date_collected', DateTime(timezone=True)),
    
    # dbCol: prior_residence
        Column('prior_residence', String(32)),
        Column('prior_residence_date_collected', DateTime(timezone=True)),
    
    # dbCol: prior_residence_other
        Column('prior_residence_other', String(32)),
        Column('prior_residence_other_date_collected', DateTime(timezone=True)),
    
    # dbCol: reason_for_leaving
        Column('reason_for_leaving', String(32)),
        Column('reason_for_leaving_date_collected', DateTime(timezone=True)),
    
    # dbCol: reason_for_leaving_other
        Column('reason_for_leaving_other', String(32)),
        Column('reason_for_leaving_other_date_collected', DateTime(timezone=True)),
    
    # dbCol: school_last_enrolled_date
        Column('school_last_enrolled_date', String(32)),
        Column('school_last_enrolled_date_date_collected', DateTime(timezone=True)),
    
    # dbCol: school_name
        Column('school_name', String(32)),
        Column('school_name_date_collected', DateTime(timezone=True)),
    
    # dbCol: school_type
        Column('school_type', String(32)),
        Column('school_type_date_collected', DateTime(timezone=True)),
    
    # dbCol: subsidy_other
        Column('subsidy_other', String(32)),
        Column('subsidy_other_date_collected', DateTime(timezone=True)),
    
    # dbCol: subsidy_type
        Column('subsidy_type', String(32)),
        Column('subsidy_type_date_collected', DateTime(timezone=True)),
    
    # dbCol: substance_abuse_indefinite
        Column('substance_abuse_indefinite', String(32)),
        Column('substance_abuse_indefinite_date_collected', DateTime(timezone=True)),
    
    # dbCol: substance_abuse_problem
        Column('substance_abuse_problem', String(32)),
        Column('substance_abuse_problem_date_collected', DateTime(timezone=True)),
    
    # dbCol: total_income
        Column('total_income', String(32)),
        Column('total_income_date_collected', DateTime(timezone=True)),
    
        ###Veteran (subtable)
    
    # dbCol: vocational_training
        Column('vocational_training', String(32)),
        Column('vocational_training_date_collected', DateTime(timezone=True)),
        
    # dbCol: annual_personal_income
        #Column('annual_personal_income', Integer(2)),
        #Column('annual_personal_income_date_collected', DateTime(timezone=True)),
        
    # dbCol: employment_status
        #Column('employment_status', Integer(2)),
        #Column('employment_status_date_collected', DateTime(timezone=True)),
        
    # dbCol: family_size
        #Column('family_size', Integer(2)),
        #Column('family_size_date_collected', DateTime(timezone=True)),

    # dbCol: hearing_impaired
        #Column('hearing_impaired', Integer(2)),
        #Column('hearing_impaired_date_collected', DateTime(timezone=True)),            

    # dbCol: marital_status
        #Column('marital_status', Integer(2)),
        #Column('marital_status_date_collected', DateTime(timezone=True)),

    # dbCol: non_ambulatory
    #    Column('non_ambulatory', Integer(2)),
    #    Column('non_ambulatory_date_collected', DateTime(timezone=True)),
    #
    ## dbCol: residential_status
    #    Column('residential_status', Integer(2)),
    #    Column('residential_status_date_collected', DateTime(timezone=True)),
    #
    ## dbCol: visually_impaired
    #    Column('visually_impaired', Integer(2)),
    #    Column('visually_impaired_date_collected', DateTime(timezone=True)),
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        ## HUD 3.0
        Column('person_historical_id_delete_2010', Integer),
        Column('person_historical_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('person_historical_id_delete_effective_2010', DateTime(timezone=True)),        
        Column('site_service_id_2010', String(50)),

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

        ## HUD 3.0
        Column('income_and_source_id_id_id_num_2010', String(32)),
        Column('income_and_source_id_id_id_str_2010', String(32)),
        Column('income_and_source_id_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('income_and_source_id_id_delete_effective_2010', DateTime(timezone=True)),
        Column('income_source_code_date_effective_2010', DateTime(timezone=True)),
        Column('income_source_other_date_effective_2010', DateTime(timezone=True)),
        Column('receiving_income_source_date_collected_2010', DateTime(timezone=True)),
        Column('receiving_income_source_date_effective_2010', DateTime(timezone=True)),
        Column('income_source_amount_date_effective_2010', DateTime(timezone=True)),
        Column('income_and_source_id_id_delete_2010', Integer),
        Column('income_source_code_data_collection_stage_2010', Integer),
        Column('income_source_other_data_collection_stage_2010', Integer),
        Column('receiving_income_source_2010', Integer),
        Column('receiving_income_source_data_collection_stage_2010', Integer),
        Column('income_source_amount_data_collection_stage_2010', Integer),

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
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),
        
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
        
        Column('export_id', String(50), ForeignKey(Export.c.export_id)),

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
        
            # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
            Column('reported', Boolean),
        
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
        
        # SBB2009119 adding a reported column.  Hopefully this will append the column to the table def.
        Column('reported', Boolean),

        ## HUD 3.0
        Column('release_of_information_id_data_collection_stage_2010', Integer),
        Column('release_of_information_id_date_effective_2010', DateTime(timezone=True)),
        Column('documentation_data_collection_stage_2010', Integer),
        Column('documentation_date_effective_2010', DateTime(timezone=True)),
        Column('release_granted_data_collection_stage_2010', Integer),
        Column('release_granted_date_effective_2010', DateTime(timezone=True)),
        
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

        ## HUD 3.0
        Column('attr_version', String(50)),
        Column('source_id_id_id_num_2010', String(50)),
        Column('source_id_id_id_str_2010', String(50)),
        Column('source_id_id_delete_2010', Integer),
        Column('source_id_id_delete_occurred_date_2010', DateTime(timezone=True)),
        Column('source_id_id_delete_effective_2010', DateTime(timezone=True)),
        Column('software_vendor_2010', String(50)),
        Column('software_version_2010', String(50)),
        Column('source_contact_email_2010', String(50)),

        useexisting = True
        )
        table_metadata.create_all()
        mapper(Source, self.source_table)
#        assign_mapper(Database, database_table, properties=dict(
#designs=relation(Design, private=True, backref="type")
#))
        return
        
        
        ## HUD 3.0 NEW TABLES

    def source_export_link_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        source_export_link_2010_table = Table(
        'source_export_link_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('source_index_id', Integer, ForeignKey(Source.c.id)),
        Column('export_index_id', String(50), ForeignKey(Export.c.export_id)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(SourceExportLink, source_export_link_2010_table)
        return    
                
    def region_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        region_2010_table = Table(
        'region_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('export_index_id', String(50), ForeignKey(Export.c.export_id)), 
        Column('region_id_id_num', String(50)),
        Column('region_id_id_str', String(50)),
        Column('site_service_id', String(50)),
        Column('region_type', String(50)),
        Column('region_type_date_collected', DateTime(timezone=True)),
        Column('region_type_date_effective', DateTime(timezone=True)),
        Column('region_type_data_collection_stage', Integer),
        Column('region_description', String(50)),
        Column('region_description_date_collected', DateTime(timezone=True)),
        Column('region_description_date_effective', DateTime(timezone=True)),
        Column('region_description_data_collection_stage', Integer),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Region, region_2010_table)
        return
 
    def agency_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        agency_2010_table = Table(
        'agency_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('export_index_id', String(50), ForeignKey(Export.c.export_id)),
        Column('region_id_id_num', String(50)),
        Column('region_id_id_str', String(50)),
        Column('site_service_id', String(50)),
        Column('region_type', String(50)),
        Column('region_type_date_collected', DateTime(timezone=True)),
        Column('region_type_date_effective', DateTime(timezone=True)),
        Column('region_type_data_collection_stage', Integer),
        Column('region_description', String(50)),
        Column('region_description_date_collected', DateTime(timezone=True)),
        Column('region_description_date_effective', DateTime(timezone=True)),
        Column('region_description_data_collection_stage', Integer),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Agency, agency_2010_table)
        return       

    def agency_child_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        agency_child_2010_table = Table(
        'agency_child_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('export_index_id', String(50), ForeignKey(Export.c.export_id)),
        Column('agency_index_id', Integer, ForeignKey(Agency.c.id)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(AgencyChild, agency_child_2010_table)
        return       

    def service_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        service_2010_table = Table(
        'service_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('export_index_id', String(50), ForeignKey(Export.c.export_id)), 
        Column('attr_delete', Integer),
        Column('attr_delete_occurred_date', DateTime(timezone=True)),
        Column('attr_effective', DateTime(timezone=True)),
        Column('airs_key', String(50)),
        Column('airs_name', String(50)),
        Column('coc_code', String(50)),
        Column('configuration', String(50)),
        Column('direct_service_code', String(50)),
        Column('grantee_identifier', String(50)),
        Column('individual_family_code', String(50)),
        Column('residential_tracking_method', String(50)),
        Column('service_type', String(50)),
        Column('service_effective_period_start_date', DateTime(timezone=True)),
        Column('service_effective_period_end_date', DateTime(timezone=True)),
        Column('service_recorded_date', DateTime(timezone=True)),
        Column('target_population_a', String(50)),
        Column('target_population_b', String(50)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Service, service_2010_table)
        return

    def site_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        site_2010_table = Table(
        'site_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('export_index_id', String(50), ForeignKey(Export.c.export_id)), 
        Column('agency_index_id', Integer, ForeignKey(Agency.c.id)), 
        #Column('agency_location_index_id', Integer, ForeignKey(AgencyLocation.c.id)), 
        Column('attr_delete', Integer),
        Column('attr_delete_occurred_date', DateTime(timezone=True)),
        Column('attr_effective', DateTime(timezone=True)),
        Column('airs_key', String(50)),
        Column('airs_name', String(50)),
        Column('site_description', String(50)),
        Column('physical_address_pre_address_line', String(50)),
        Column('physical_address_line_1', String(50)),
        Column('physical_address_line_2', String(50)),
        Column('physical_address_city', String(50)),
        Column('physical_address_country', String(50)),
        Column('physical_address_state', String(50)),
        Column('physical_address_zip_code', String(50)),
        Column('physical_address_country', String(50)),
        Column('physical_address_reason_withheld', String(50)),
        Column('physical_address_confidential', String(50)),
        Column('physical_address_description', String(50)),
        Column('mailing_address_pre_address_line', String(50)),
        Column('mailing_address_line_1', String(50)),
        Column('mailing_address_line_2', String(50)),
        Column('mailing_address_city', String(50)),
        Column('mailing_address_country', String(50)),
        Column('mailing_address_state', String(50)),
        Column('mailing_address_zip_code', String(50)),
        Column('mailing_address_country', String(50)),
        Column('mailing_address_reason_withheld', String(50)),
        Column('mailing_address_confidential', String(50)),
        Column('mailing_address_description', String(50)),
        Column('no_physical_address_description', String(50)),
        Column('no_physical_address_explanation', String(50)),
        Column('disabilities_access', String(50)),
        Column('physical_location_description', String(50)),
        Column('bus_service_access', String(50)),
        Column('public_access_to_transportation', String(50)),
        Column('year_inc', String(50)),
        Column('annual_budget_total', String(50)),
        Column('legal_status', String(50)),
        Column('exclude_from_website', String(50)),
        Column('exclude_from_directory', String(50)),
        Column('agency_key', String(50)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Site, site_2010_table)
        return

    def site_service_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        site_service_2010_table = Table(
        'site_service_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('export_index_id', String(50), ForeignKey(Export.c.export_id)), 
        Column('site_index_id', Integer, ForeignKey(Site.c.id)), 
        Column('attr_delete', Integer),
        Column('attr_delete_occurred_date', DateTime(timezone=True)),
        Column('attr_effective', DateTime(timezone=True)),
        Column('name', String(50)),
        Column('key', String(50)),
        Column('description', String(50)),
        Column('fee_structure', String(50)),
        Column('gender_requirements', String(50)),
        Column('area_flexibility', String(50)),
        Column('service_not_always_available', String(50)),
        Column('service_group_key', String(50)),
        Column('service_id', String(50)),
        Column('site_id', String(50)),
        Column('geographic_code', String(50)),
        Column('geographic_code_date_collected', DateTime(timezone=True)),
        Column('geographic_code_date_effective', DateTime(timezone=True)),        
        Column('geographic_code_data_collection_stage', String(50)),
        Column('housing_type', String(50)),
        Column('housing_type_date_collected', DateTime(timezone=True)),
        Column('housing_type_date_effective', DateTime(timezone=True)),
        Column('housing_type_data_collection_stage', String(50)),
        Column('principal', String(50)),
        Column('site_service_effective_period_start_date', DateTime(timezone=True)),
        Column('site_service_effective_period_end_date', DateTime(timezone=True)),
        Column('site_service_recorded_date', DateTime(timezone=True)),
        Column('site_service_type', String(50)),        
        useexisting = True
        )
        table_metadata.create_all()
        mapper(SiteService, site_service_2010_table)
        return

    def funding_source_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        funding_source_2010_table = Table(
        'funding_source_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('service_index_id', Integer, ForeignKey(Service.c.id)), 
        Column('service_event_index_id', Integer, ForeignKey(ServiceEvent.c.id)), 
        Column('funding_source_id_id_num', String(50)),
        Column('funding_source_id_id_str', String(50)),
        Column('funding_source_id_delete', String(50)),
        Column('funding_source_id_delete_occurred_date', DateTime(timezone=True)),
        Column('funding_source_id_delete_effective', DateTime(timezone=True)),
        Column('federal_cfda_number', String(50)),
        Column('receives_mckinney_funding', String(50)),
        Column('advance_or_arrears', String(50)),
        Column('financial_assistance_amount', String(50)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(FundingSource, funding_source_2010_table)
        return
        
    def inventory_2010_map(self):
        table_metadata = MetaData(bind=self.pg_db, reflect=True)
        inventory_2010_table = Table(
        'inventory_2010',
        table_metadata,
        Column('id', Integer, primary_key=True),
        Column('service_index_id', Integer, ForeignKey(Service.c.id)), 
        Column('site_service_index_id', Integer, ForeignKey(SiteService.c.id)), 
        Column('attr_delete', Integer),
        Column('attr_delete_occurred_date', DateTime(timezone=True)),
        Column('attr_effective', DateTime(timezone=True)),
        Column('hmis_participation_period_start_date', DateTime(timezone=True)),
        Column('hmis_participation_period_end_date', DateTime(timezone=True)),
        Column('inventory_id_id_num', String(50)),
        Column('inventory_id_id_str', String(50)),
        Column('bed_availability', String(50)),
        Column('bed_type', String(50)),
        Column('bed_individual_family_type', String(50)),
        Column('chronic_homeless_bed', String(50)),
        Column('domestic_violence_shelter_bed', String(50)),
        Column('household_type', String(50)),
        Column('hmis_participating_beds', String(50)),        
        Column('inventory_effective_period_start_date', DateTime(timezone=True)),
        Column('inventory_effective_period_end_date', DateTime(timezone=True)),
        Column('inventory_recorded_date', DateTime(timezone=True)),
        Column('unit_inventory', String(50)),
        useexisting = True
        )
        table_metadata.create_all()
        mapper(Inventory, inventory_2010_table)
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

class SystemConfiguration(baseObject):
    pass
        
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

class DrugHistory(baseObject):
    pass
      
class EmergencyContact(baseObject):
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

class SourceExportLink(baseObject):
    pass
    
class Region(baseObject):
    pass
            
class Agency(baseObject):
    pass  
              
class AgencyChild(baseObject):
    pass  

class Service(baseObject):
    pass 

class Site(baseObject):
    pass 

class SiteService(baseObject):
    pass 
      
class FundingSource(baseObject):
    pass 

class Inventory(baseObject):
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
        person.reported = True
        person.person_legal_first_name_unhashed = "Scott"
        mappedObjects.session().commit()
        print 'Person: George Washington (SCOTT)'
        print '-----------------------------------'
        print person
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
            
            