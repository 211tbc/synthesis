import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Boolean, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import DateTime, Date, Interval
from sqlalchemy.pool import NullPool
from conf import settings
from logging import Logger

print("loaded dbobjects module")

class DB:
    #print "loaded DB Class" 
    database_string = 'postgresql+psycopg2://' + settings.DB_USER + ':' + settings.DB_PASSWD + '@' + settings.DB_HOST + ':' + str(settings.DB_PORT) + '/' + settings.DB_DATABASE
    pg_db_engine = create_engine(database_string, poolclass=NullPool, echo=settings.DEBUG_ALCHEMY)
    mymetadata = MetaData(bind=pg_db_engine)
    Base = declarative_base(metadata=mymetadata)
    
    def __init__(self):
        #postgresql[+driver]://<user>:<pass>@<host>/<dbname>    #, server_side_cursors=True)    
        self.Session = sessionmaker()	# Was
        #self.Session = sessionmaker(bind=self.pg_db_engine)	# JCS
        loglevel = 'DEBUG' 
        self.log = Logger(settings.LOGGING_INI, loglevel)

class MapBase():
        def __init__(self, field_dict):
            if settings.DEBUG:
                print("Base Class created: %s" % self.__class__.__name__)
        #def __init__(self, field_dict):
            if settings.DEBUG:
                print(field_dict)
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

class SiteServiceParticipation(DB.Base, MapBase):
    __tablename__ = 'site_service_participation'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    household_index_id = Column(Integer, ForeignKey('household.id'))
    site_service_participation_idid_num = Column(String(32))
    site_service_participation_idid_num_date_collected = Column(DateTime(timezone=False))
    site_service_participation_idid_str = Column(String(32))
    site_service_participation_idid_str_date_collected = Column(DateTime(timezone=False))
    site_service_idid_num = Column(String(32))					# JCS
    #site_service_idid_num_date_collected = Column(DateTime(timezone=False))	# JCS
    destination = Column(String(32))
    destination_date_collected = Column(DateTime(timezone=False))
    destination_other = Column(String(32))
    destination_other_date_collected = Column(DateTime(timezone=False))
    destination_tenure = Column(String(32))
    destination_tenure_date_collected = Column(DateTime(timezone=False))
    disabling_condition = Column(String(32))
    disabling_condition_date_collected = Column(DateTime(timezone=False))
    participation_dates_start_date = Column(DateTime(timezone=False))
    participation_dates_start_date_date_collected = Column(DateTime(timezone=False))
    participation_dates_end_date = Column(DateTime(timezone=False))
    participation_dates_end_date_date_collected = Column(DateTime(timezone=False))
    veteran_status = Column(String(32))
    veteran_status_date_collected = Column(DateTime(timezone=False))
    #adding a reported column.  Hopefully this will append the column to the table def.
    reported = Column(Boolean)
    site_service_participation_id_delete = Column(String(32))
    site_service_participation_id_delete_occurred_date = Column(DateTime(timezone=False))
    site_service_participation_id_delete_effective_date = Column(DateTime(timezone=False))
    fk_participation_to_need = relationship('Need', backref='fk_need_to_participation')
    fk_participation_to_serviceevent = relationship('ServiceEvent')
    fk_participation_to_personhistorical = relationship('PersonHistorical')
    fk_participation_to_person = Column(Integer, ForeignKey('person.id'))
    useexisting = True
    
 
class Need(DB.Base, MapBase):
    __tablename__ = 'need'
    id = Column(Integer, primary_key=True)
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))	# JCS
    site_service_participation_index_id = Column(Integer, ForeignKey('site_service_participation.id'))	# JCS
    export_index_id = Column(Integer, ForeignKey('export.id'))
    need_idid_num = Column(String(32))
    need_idid_num_date_collected = Column(DateTime(timezone=False))
    need_idid_str = Column(String(32))
    need_idid_str_date_collected = Column(DateTime(timezone=False))
    site_service_idid_num = Column(String(32))
    site_service_idid_num_date_collected = Column(DateTime(timezone=False))
    site_service_idid_str = Column(String(32))
    site_service_idid_str_date_collected = Column(DateTime(timezone=False))
    service_event_idid_num = Column(String(32))
    service_event_idid_num_date_collected = Column(DateTime(timezone=False))
    service_event_idid_str = Column(String(32))
    service_event_idid_str_date_collected = Column(DateTime(timezone=False))
    need_status = Column(String(32))
    need_status_date_collected = Column(DateTime(timezone=False))
    taxonomy = Column(String(32))
    reported = Column(Boolean)
    ## HUD 3.0
    person_index_id = Column(Integer, ForeignKey('person.id'))
    need_id_delete = Column(String(32))
    need_id_delete_occurred_date = Column(DateTime(timezone=False))
    need_id_delete_delete_effective_date = Column(DateTime(timezone=False))
    need_effective_period_start_date = Column(DateTime(timezone=False))
    need_effective_period_end_date = Column(DateTime(timezone=False))
    need_recorded_date = Column(DateTime(timezone=False))
    useexisting = True
    
 
class Races(DB.Base, MapBase):
    __tablename__ = 'races' 
    id = Column(Integer, primary_key=True)
    person_index_id = Column(Integer, ForeignKey('person.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    race_unhashed = Column(Integer)
    race_hashed = Column(String(32))
    race_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean)
    ## HUD 3.0
    race_data_collection_stage = Column(String(32))
    race_date_effective = Column(DateTime(timezone=False))
    useexisting = True
    
 
class OtherNames(DB.Base, MapBase):
    __tablename__ = 'other_names'
    id = Column(Integer, primary_key=True)
    person_index_id = Column(Integer, ForeignKey('person.id')) 
    export_index_id = Column(Integer, ForeignKey('export.id'))
    other_first_name_unhashed = Column(String(50))
    other_first_name_hashed = Column(String(50))
    other_first_name_date_collected = Column(DateTime(timezone=False))
    other_first_name_date_effective = Column(DateTime(timezone=False))
    other_first_name_data_collection_stage = Column(String(32))
    other_middle_name_unhashed = Column(String(50))
    other_middle_name_hashed = Column(String(50))
    other_middle_name_date_collected = Column(DateTime(timezone=False))
    other_middle_name_date_effective = Column(DateTime(timezone=False))
    other_middle_name_data_collection_stage = Column(String(32))
    other_last_name_unhashed = Column(String(50))
    other_last_name_hashed = Column(String(50))
    other_last_name_date_collected = Column(DateTime(timezone=False))
    other_last_name_date_effective = Column(DateTime(timezone=False))
    other_last_name_data_collection_stage = Column(String(32))
    other_suffix_unhashed = Column(String(50))
    other_suffix_hashed = Column(String(50))
    other_suffix_date_collected = Column(DateTime(timezone=False))
    other_suffix_date_effective = Column(DateTime(timezone=False))
    other_suffix_data_collection_stage = Column(String(32))
    useexisting = True
    
 
class HUDHomelessEpisodes(DB.Base, MapBase):
    __tablename__ = 'hud_homeless_episodes'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))        
    start_date = Column(String(32))
    start_date_date_collected = Column(DateTime(timezone=False))
    end_date = Column(String(32))
    end_date_date_collected = Column(DateTime(timezone=False))
    useexisting = True
    
 
class Veteran(DB.Base, MapBase):
    __tablename__ = 'veteran'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    service_era = Column(Integer)
    service_era_date_collected = Column(DateTime(timezone=False))
    military_service_duration = Column(Integer)
    military_service_duration_date_collected = Column(DateTime(timezone=False))
    served_in_war_zone = Column(Integer)
    served_in_war_zone_date_collected = Column(DateTime(timezone=False))
    war_zone = Column(Integer)
    war_zone_date_collected = Column(DateTime(timezone=False))
    war_zone_other = Column(String(50))
    war_zone_other_date_collected = Column(DateTime(timezone=False))
    months_in_war_zone = Column(Integer)
    months_in_war_zone_date_collected = Column(DateTime(timezone=False))
    received_fire = Column(Integer)
    received_fire_date_collected = Column(DateTime(timezone=False))
    military_branch = Column(Integer)
    military_branch_date_collected = Column(DateTime(timezone=False))
    military_branch_other = Column(String(50))
    military_branch_other_date_collected = Column(DateTime(timezone=False))
    discharge_status = Column(Integer)
    discharge_status_date_collected = Column(DateTime(timezone=False))
    discharge_status_other = Column(String(50))
    discharge_status_other_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean) 
    useexisting = True
    
 
class DrugHistory(DB.Base, MapBase):
    __tablename__ = 'drug_history'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    drug_history_id = Column(String(32))
    drug_history_id_date_collected = Column(DateTime(timezone=False))
    drug_code = Column(Integer)
    drug_code_date_collected = Column(DateTime(timezone=False))    
    drug_use_frequency = Column(Integer)
    drug_use_frequency_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean)
    useexisting = True
    
 
class EmergencyContact(DB.Base, MapBase):
    __tablename__ = 'emergency_contact'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    emergency_contact_id = Column(String(32))
    emergency_contact_id_date_collected = Column(DateTime(timezone=False))
    emergency_contact_name = Column(String(32))
    emergency_contact_name_date_collected = Column(DateTime(timezone=False))    
    emergency_contact_phone_number_0 = Column(String(32))
    emergency_contact_phone_number_date_collected_0 = Column(DateTime(timezone=False))
    emergency_contact_phone_number_type_0 = Column(String(32))
    emergency_contact_phone_number_1 = Column(String(32))
    emergency_contact_phone_number_date_collected_1 = Column(DateTime(timezone=False))
    emergency_contact_phone_number_type_1 = Column(String(32))
    emergency_contact_address_date_collected = Column(DateTime(timezone=False))
    emergency_contact_address_start_date = Column(DateTime(timezone=False))
    emergency_contact_address_start_date_date_collected = Column(DateTime(timezone=False))
    emergency_contact_address_end_date = Column(DateTime(timezone=False))
    emergency_contact_address_end_date_date_collected = Column(DateTime(timezone=False))
    emergency_contact_address_line1 = Column(String(32))
    emergency_contact_address_line1_date_collected = Column(DateTime(timezone=False))
    emergency_contact_address_line2 = Column(String(32))
    emergency_contact_address_line2_date_collected = Column(DateTime(timezone=False))
    emergency_contact_address_city = Column(String(32))
    emergency_contact_address_city_date_collected = Column(DateTime(timezone=False))
    emergency_contact_address_state = Column(String(32))
    emergency_contact_address_state_date_collected = Column(DateTime(timezone=False))    
    emergency_contact_relation_to_client = Column(String(32))
    emergency_contact_relation_to_client_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean)
    useexisting = True
    
   
class PersonAddress(DB.Base, MapBase):
    __tablename__ = 'person_address'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    address_period_start_date = Column(DateTime(timezone=False))
    address_period_start_date_date_collected = Column(DateTime(timezone=False))
    address_period_end_date = Column(DateTime(timezone=False))
    address_period_end_date_date_collected = Column(DateTime(timezone=False))
    pre_address_line = Column(String(100))
    pre_address_line_date_collected = Column(DateTime(timezone=False))
    pre_address_line_date_effective = Column(DateTime(timezone=False))
    pre_address_line_data_collection_stage = Column(String(32))
    line1 = Column(String(100))
    line1_date_collected = Column(DateTime(timezone=False))
    line1_date_effective = Column(DateTime(timezone=False))
    line1_data_collection_stage = Column(String(32))
    line2 = Column(String(100))
    line2_date_collected = Column(DateTime(timezone=False))
    line2_date_effective = Column(DateTime(timezone=False))
    line2_data_collection_stage = Column(String(32))
    city = Column(String(100))
    city_date_collected = Column(DateTime(timezone=False))
    city_date_effective = Column(DateTime(timezone=False))
    city_data_collection_stage = Column(String(32))
    county = Column(String(32))
    county_date_collected = Column(DateTime(timezone=False))
    county_date_effective = Column(DateTime(timezone=False))
    county_data_collection_stage = Column(String(32))
    state = Column(String(32))
    state_date_collected = Column(DateTime(timezone=False))
    state_date_effective = Column(DateTime(timezone=False))
    state_data_collection_stage = Column(String(32))
    zipcode = Column(String(10))
    zipcode_date_collected = Column(DateTime(timezone=False))
    zipcode_date_effective = Column(DateTime(timezone=False))
    zipcode_data_collection_stage = Column(String(32))
    country = Column(String(32))
    country_date_collected = Column(DateTime(timezone=False))
    country_date_effective = Column(DateTime(timezone=False))
    country_data_collection_stage = Column(String(32))
    is_last_permanent_zip = Column(Integer)
    is_last_permanent_zip_date_collected = Column(DateTime(timezone=False))
    is_last_permanent_zip_date_effective = Column(DateTime(timezone=False))
    is_last_permanent_zip_data_collection_stage = Column(String(32))
    zip_quality_code = Column(Integer)
    zip_quality_code_date_collected = Column(DateTime(timezone=False))
    zip_quality_code_date_effective = Column(DateTime(timezone=False))
    zip_quality_code_data_collection_stage = Column(String(32))
    reported = Column(Boolean)
    ## HUD 3.0
    person_address_delete = Column(String(32))
    person_address_delete_occurred_date = Column(DateTime(timezone=False))
    person_address_delete_effective_date = Column(DateTime(timezone=False))
    useexisting = True

class PersonHistorical(DB.Base, MapBase):
    __tablename__ = 'person_historical'
    id = Column(Integer, primary_key=True)
    call_index_id = Column(Integer, ForeignKey('call.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_index_id = Column(Integer, ForeignKey('person.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))	# JCS
    site_service_participation_index_id = Column(Integer, ForeignKey('site_service_participation.id'))	# JCS
    person_historical_id_id_num = Column(String(32))
    person_historical_id_id_str = Column(String(32))
    person_historical_id_delete_effective_date = Column(DateTime(timezone=False))
    person_historical_id_delete = Column(Integer)
    person_historical_id_delete_occurred_date = Column(DateTime(timezone=False))
    barrier_code = Column(String(32))
    barrier_code_date_collected = Column(DateTime(timezone=False))
    barrier_other = Column(String(32))
    barrier_other_date_collected = Column(DateTime(timezone=False))
    child_currently_enrolled_in_school = Column(String(32))
    child_currently_enrolled_in_school_date_collected = Column(DateTime(timezone=False))
    currently_employed = Column(String(32))
    currently_employed_date_collected = Column(DateTime(timezone=False))
    currently_in_school = Column(String(32))
    currently_in_school_date_collected = Column(DateTime(timezone=False))
    degree_code = Column(String(32))
    degree_code_date_collected = Column(DateTime(timezone=False))
    degree_other = Column(String(32))
    degree_other_date_collected = Column(DateTime(timezone=False))
    developmental_disability = Column(String(32))
    developmental_disability_date_collected = Column(DateTime(timezone=False))
    domestic_violence = Column(String(32))
    domestic_violence_date_collected = Column(DateTime(timezone=False))
    domestic_violence_how_long = Column(String(32))
    domestic_violence_how_long_date_collected = Column(DateTime(timezone=False))
    due_date = Column(String(32))
    due_date_date_collected = Column(DateTime(timezone=False))
    employment_tenure = Column(String(32))
    employment_tenure_date_collected = Column(DateTime(timezone=False))
    health_status = Column(String(32))
    health_status_date_collected = Column(DateTime(timezone=False))
    highest_school_level = Column(String(32))
    highest_school_level_date_collected = Column(DateTime(timezone=False))
    hivaids_status = Column(String(32))
    hivaids_status_date_collected = Column(DateTime(timezone=False))
    hours_worked_last_week = Column(String(32))
    hours_worked_last_week_date_collected = Column(DateTime(timezone=False))
    hud_chronic_homeless = Column(String(32))
    hud_chronic_homeless_date_collected = Column(DateTime(timezone=False))
    hud_homeless = Column(String(32))
    hud_homeless_date_collected = Column(DateTime(timezone=False))
    site_service_id = Column(Integer)
    ###HUDHomelessEpisodes (subtable)
    ###IncomeAndSources (subtable)
    length_of_stay_at_prior_residence = Column(String(32))
    length_of_stay_at_prior_residence_date_collected = Column(DateTime(timezone=False))
    looking_for_work = Column(String(32))
    looking_for_work_date_collected = Column(DateTime(timezone=False))
    mental_health_indefinite = Column(String(32))
    mental_health_indefinite_date_collected = Column(DateTime(timezone=False))
    mental_health_problem = Column(String(32))
    mental_health_problem_date_collected = Column(DateTime(timezone=False))
    non_cash_source_code = Column(String(32))
    non_cash_source_code_date_collected = Column(DateTime(timezone=False))
    non_cash_source_other = Column(String(32))
    non_cash_source_other_date_collected = Column(DateTime(timezone=False))
    ###PersonAddress (subtable)
    person_email = Column(String(32))
    person_email_date_collected = Column(DateTime(timezone=False))
    person_phone_number = Column(String(32))
    person_phone_number_date_collected = Column(DateTime(timezone=False))
    physical_disability = Column(String(32))
    physical_disability_date_collected = Column(DateTime(timezone=False))
    pregnancy_status = Column(String(32))
    pregnancy_status_date_collected = Column(DateTime(timezone=False))
    prior_residence = Column(String(32))
    prior_residence_date_collected = Column(DateTime(timezone=False))
    prior_residence_other = Column(String(32))
    prior_residence_other_date_collected = Column(DateTime(timezone=False))
    reason_for_leaving = Column(String(32))
    reason_for_leaving_date_collected = Column(DateTime(timezone=False))
    reason_for_leaving_other = Column(String(32))
    reason_for_leaving_other_date_collected = Column(DateTime(timezone=False))
    school_last_enrolled_date = Column(String(32))
    school_last_enrolled_date_date_collected = Column(DateTime(timezone=False))
    school_name = Column(String(32))
    school_name_date_collected = Column(DateTime(timezone=False))
    school_type = Column(String(32))
    school_type_date_collected = Column(DateTime(timezone=False))
    subsidy_other = Column(String(32))
    subsidy_other_date_collected = Column(DateTime(timezone=False))
    subsidy_type = Column(String(32))
    subsidy_type_date_collected = Column(DateTime(timezone=False))
    substance_abuse_indefinite = Column(String(32))
    substance_abuse_indefinite_date_collected = Column(DateTime(timezone=False))
    substance_abuse_problem = Column(String(32))
    substance_abuse_problem_date_collected = Column(DateTime(timezone=False))
    total_income = Column(String(32))
    total_income_date_collected = Column(DateTime(timezone=False))
    ###Veteran (subtable)
    vocational_training = Column(String(32))
    vocational_training_date_collected = Column(DateTime(timezone=False))
    annual_personal_income = Column(Integer)
    annual_personal_income_date_collected = Column(DateTime(timezone=False))
    employment_status = Column(Integer)
    employment_status_date_collected = Column(DateTime(timezone=False))
    family_size = Column(Integer)
    family_size_date_collected = Column(DateTime(timezone=False))
    hearing_impaired = Column(Integer)
    hearing_impaired_date_collected = Column(DateTime(timezone=False))
    marital_status = Column(Integer)
    marital_status_date_collected = Column(DateTime(timezone=False))
    non_ambulatory = Column(Integer)
    non_ambulatory_date_collected = Column(DateTime(timezone=False))
    residential_status = Column(Integer)
    residential_status_date_collected = Column(DateTime(timezone=False))
    visually_impaired = Column(Integer)
    visually_impaired_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean)
    fk_person_historical_to_income_and_sources = relationship('IncomeAndSources',
        backref='fk_income_and_sources_to_person_historical')
    fk_person_historical_to_veteran = relationship('Veteran', backref='fk_veteran_to_person_historical')
    fk_person_historical_to_hud_homeless_episodes = relationship('HUDHomelessEpisodes',
        backref='fk_hud_homeless_episodes_to_person_historical')
    fk_person_historical_to_person_address = relationship('PersonAddress', backref='fk_person_address_to_person_historical')
    useexisting = True
    
    
class IncomeAndSources(DB.Base, MapBase):
    __tablename__ = 'income_and_sources'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    amount = Column(Integer)
    amount_date_collected = Column(DateTime(timezone=False))
    income_source_code = Column(Integer)
    income_source_code_date_collected = Column(DateTime(timezone=False))
    income_source_other = Column(String(32))
    income_source_other_date_collected = Column(DateTime(timezone=False))
    ## HUD 3.0
    income_and_source_id_id_num = Column(String(32))
    income_and_source_id_id_str = Column(String(32))
    income_and_source_id_id_delete_occurred_date = Column(DateTime(timezone=False))
    income_and_source_id_id_delete_effective_date = Column(DateTime(timezone=False))
    income_source_code_date_effective = Column(DateTime(timezone=False))
    income_source_other_date_effective = Column(DateTime(timezone=False))
    receiving_income_source_date_collected = Column(DateTime(timezone=False))
    receiving_income_source_date_effective = Column(DateTime(timezone=False))
    income_source_amount_date_effective = Column(DateTime(timezone=False))
    income_and_source_id_id_delete = Column(Integer)
    income_source_code_data_collection_stage = Column(String(32))
    income_source_other_data_collection_stage = Column(String(32))
    receiving_income_source = Column(Integer)
    receiving_income_source_data_collection_stage = Column(String(32))
    income_source_amount_data_collection_stage = Column(String(32))
    useexisting = True
    
 
class Members(DB.Base, MapBase):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    household_index_id = Column(Integer, ForeignKey('household.id'))
    person_index_id = Column(Integer, ForeignKey('person.id'))
    relationship_to_head_of_household = Column(String(32))
    relationship_to_head_of_household_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean)
    useexisting = True
    
 
class ReleaseOfInformation(DB.Base, MapBase):
    __tablename__ = 'release_of_information'
    id = Column(Integer, primary_key=True)
    person_index_id = Column(Integer, ForeignKey('person.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    release_of_information_idid_num = Column(String(32))
    release_of_information_idid_num_date_collected = Column(DateTime(timezone=False))
    release_of_information_idid_str = Column(String(32))
    release_of_information_idid_str_date_collected = Column(DateTime(timezone=False))
    site_service_idid_num = Column(String(32))
    site_service_idid_num_date_collected = Column(DateTime(timezone=False))
    site_service_idid_str = Column(String(32))
    site_service_idid_str_date_collected = Column(DateTime(timezone=False))
    documentation = Column(String(32))
    documentation_date_collected = Column(DateTime(timezone=False))
    #EffectivePeriod (subtable)
    start_date = Column(String(32))
    start_date_date_collected = Column(DateTime(timezone=False))
    end_date = Column(String(32))
    end_date_date_collected = Column(DateTime(timezone=False))
    release_granted = Column(String(32))
    release_granted_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean)
    ## HUD 3.0
    release_of_information_id_data_collection_stage = Column(String(32))
    release_of_information_id_date_effective = Column(DateTime(timezone=False))
    documentation_data_collection_stage = Column(String(32))
    documentation_date_effective = Column(DateTime(timezone=False))
    release_granted_data_collection_stage = Column(String(32))
    release_granted_date_effective = Column(DateTime(timezone=False))
    useexisting = True
    
 
class SourceExportLink(DB.Base, MapBase):
    __tablename__ = 'source_export_link'
    id = Column(Integer, primary_key=True)
    source_index_id = Column(Integer, ForeignKey('source.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_index_id = Column(String(50), ForeignKey('report.report_id'))
    useexisting = True
    
            
class Region(DB.Base, MapBase):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_index_id = Column(String(50), ForeignKey('report.report_id')) 
    region_id_id_num = Column(String(50))
    region_id_id_str = Column(String(32))
    site_service_id = Column(String(50))
    region_type = Column(String(50))
    region_type_date_collected = Column(DateTime(timezone=False))
    region_type_date_effective = Column(DateTime(timezone=False))
    region_type_data_collection_stage = Column(String(32))
    region_description = Column(String(30))
    region_description_date_collected = Column(DateTime(timezone=False))
    region_description_date_effective = Column(DateTime(timezone=False))
    region_description_data_collection_stage = Column(String(32))
    useexisting = True
    
 
class Agency(DB.Base, MapBase):
    __tablename__ = 'agency'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_index_id = Column(String(50), ForeignKey('report.report_id'))
    agency_delete = Column(Integer)
    agency_delete_occurred_date = Column(DateTime(timezone=False))
    agency_delete_effective_date = Column(DateTime(timezone=False))
    airs_key = Column(String(50))
    airs_name = Column(String(50))
    agency_description = Column(String(50))
    irs_status = Column(String(50))
    source_of_funds = Column(String(50))
    record_owner = Column(String(50))
    fein = Column(String(50))
    year_inc = Column(String(50))
    annual_budget_total = Column(String(50))
    legal_status = Column(String(50))
    exclude_from_website = Column(String(50))
    exclude_from_directory = Column(String(50))        
    useexisting = True
    
 
class AgencyChild(DB.Base, MapBase):
    __tablename__ = 'agency_child'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_index_id = Column(String(50), ForeignKey('report.report_id'))
    agency_index_id = Column(Integer, ForeignKey('agency.id'))
    useexisting = True
    
 
class Service(DB.Base, MapBase):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    service_id = Column(String(50))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_index_id = Column(String(50), ForeignKey('report.report_id')) 
    service_delete = Column(Integer)
    service_delete_occurred_date = Column(DateTime(timezone=False))
    service_delete_effective_date = Column(DateTime(timezone=False))
    airs_key = Column(String(50))
    airs_name = Column(String(50))
    coc_code = Column(String(5))
    configuration = Column(String(50))
    direct_service_code = Column(String(50))
    grantee_identifier = Column(String(10))
    individual_family_code = Column(String(50))
    residential_tracking_method = Column(String(50))
    service_type = Column(String(50))
    jfcs_service_type = Column(String(50))
    service_effective_period_start_date = Column(DateTime(timezone=False))
    service_effective_period_end_date = Column(DateTime(timezone=False))
    service_recorded_date = Column(DateTime(timezone=False))
    target_population_a = Column(String(50))
    target_population_b = Column(String(50))
    useexisting = True
    
 
class Site(DB.Base, MapBase):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_index_id = Column(String(50), ForeignKey('report.report_id')) 
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    #agency_location_index_id = Column(Integer, ForeignKey('agency_location.id')) 
    site_delete = Column(Integer)
    site_delete_occurred_date = Column(DateTime(timezone=False))
    site_delete_effective_date = Column(DateTime(timezone=False))
    airs_key = Column(String(50))
    airs_name = Column(String(50))
    site_description = Column(String(50))
    physical_address_pre_address_line = Column(String(100))
    physical_address_line_1 = Column(String(100))
    physical_address_line_2 = Column(String(100))
    physical_address_city = Column(String(50))
    physical_address_country = Column(String(50))
    physical_address_state = Column(String(50))
    physical_address_zip_code = Column(String(50))
    physical_address_country = Column(String(50))
    physical_address_reason_withheld = Column(String(50))
    physical_address_confidential = Column(String(50))
    physical_address_description = Column(String(50))
    mailing_address_pre_address_line = Column(String(100))
    mailing_address_line_1 = Column(String(100))
    mailing_address_line_2 = Column(String(100))
    mailing_address_city = Column(String(50))
    mailing_address_country = Column(String(50))
    mailing_address_state = Column(String(50))
    mailing_address_zip_code = Column(String(50))
    mailing_address_country = Column(String(50))
    mailing_address_reason_withheld = Column(String(50))
    mailing_address_confidential = Column(String(50))
    mailing_address_description = Column(String(50))
    no_physical_address_description = Column(String(50))
    no_physical_address_explanation = Column(String(50))
    disabilities_access = Column(String(50))
    physical_location_description = Column(String(50))
    bus_service_access = Column(String(50))
    public_access_to_transportation = Column(String(50))
    year_inc = Column(String(50))
    annual_budget_total = Column(String(50))
    legal_status = Column(String(50))
    exclude_from_website = Column(String(50))
    exclude_from_directory = Column(String(50))
    agency_key = Column(String(50))
    useexisting = True
    
 
class SiteService(DB.Base, MapBase):
    __tablename__ = 'site_service'
    id = Column(Integer, primary_key=True)
    site_service_id = Column(String(50))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_index_id = Column(String(50), ForeignKey('report.report_id')) 
    site_index_id = Column(Integer, ForeignKey('site.id'))
    service_index_id = Column(Integer, ForeignKey(Service.id))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    site_service_delete = Column(Integer)
    site_service_delete_occurred_date = Column(DateTime(timezone=False))
    site_service_delete_effective_date = Column(DateTime(timezone=False))
    name = Column(String(50))
    key = Column(String(50))
    description = Column(String(50))
    fee_structure = Column(String(50))
    gender_requirements = Column(String(50))
    area_flexibility = Column(String(50))
    service_not_always_available = Column(String(50))
    service_group_key = Column(String(50))
    site_id = Column(String(50))
    geographic_code = Column(String(50))
    geographic_code_date_collected = Column(DateTime(timezone=False))
    geographic_code_date_effective = Column(DateTime(timezone=False))        
    geographic_code_data_collection_stage = Column(String(50))
    housing_type = Column(String(50))
    housing_type_date_collected = Column(DateTime(timezone=False))
    housing_type_date_effective = Column(DateTime(timezone=False))
    housing_type_data_collection_stage = Column(String(50))
    principal = Column(String(50))
    site_service_effective_period_start_date = Column(DateTime(timezone=False))
    site_service_effective_period_end_date = Column(DateTime(timezone=False))
    site_service_recorded_date = Column(DateTime(timezone=False))
    site_service_type = Column(String(50))        
    useexisting = True
    
 
class FundingSource(DB.Base, MapBase):
    __tablename__ = 'funding_source'
    id = Column(Integer, primary_key=True)
    service_index_id = Column(Integer, ForeignKey('service.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    service_event_index_id = Column(Integer, ForeignKey('service_event.id')) 
    funding_source_id_id_num = Column(String(50))
    funding_source_id_id_str = Column(String(32))
    funding_source_id_delete = Column(String(50))
    funding_source_id_delete_occurred_date = Column(DateTime(timezone=False))
    funding_source_id_delete_effective_date = Column(DateTime(timezone=False))
    federal_cfda_number = Column(String(50))
    receives_mckinney_funding = Column(String(50))
    advance_or_arrears = Column(String(50))
    financial_assistance_amount = Column(String(50))
    useexisting = True
    
 
class ResourceInfo(DB.Base, MapBase):
    __tablename__ = 'resource_info'
    id = Column(Integer, primary_key=True)
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    resource_specialist = Column(String(50))
    available_for_directory = Column(String(50))
    available_for_referral = Column(String(50))
    available_for_research = Column(String(50))
    date_added = Column(DateTime(timezone=False))
    date_last_verified = Column(DateTime(timezone=False))
    date_of_last_action = Column(DateTime(timezone=False))
    last_action_type = Column(String(50))
    useexisting = True
    
 
class Inventory(DB.Base, MapBase):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    service_index_id = Column(Integer, ForeignKey(Service.id)) 
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    inventory_delete = Column(Integer)
    inventory_delete_occurred_date = Column(DateTime(timezone=False))
    inventory_delete_effective_delete = Column(DateTime(timezone=False))
    hmis_participation_period_start_date = Column(DateTime(timezone=False))
    hmis_participation_period_end_date = Column(DateTime(timezone=False))
    inventory_id_id_num = Column(String(50))
    inventory_id_id_str = Column(String(32))
    bed_inventory = Column(String(50))
    bed_availability = Column(String(50))
    bed_type = Column(String(50))
    bed_individual_family_type = Column(String(50))
    chronic_homeless_bed = Column(String(50))
    domestic_violence_shelter_bed = Column(String(50))
    household_type = Column(String(50))
    hmis_participating_beds = Column(String(50))        
    inventory_effective_period_start_date = Column(DateTime(timezone=False))
    inventory_effective_period_end_date = Column(DateTime(timezone=False))
    inventory_recorded_date = Column(DateTime(timezone=False))
    unit_inventory = Column(String(50))
    useexisting = True
    
 
class AgeRequirements(DB.Base, MapBase):
    __tablename__ = 'age_requirements'
    id = Column(Integer, primary_key=True)
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    gender = Column(String(50))
    minimum_age = Column(String(50))
    maximum_age = Column(String(50))
    useexisting = True
    
 
class AidRequirements(DB.Base, MapBase):
    __tablename__ = 'aid_requirements'
    id = Column(Integer, primary_key=True)
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    aid_requirements = Column(String(50))
    useexisting = True
    
 
class Aka(DB.Base, MapBase):
    __tablename__ = 'aka'
    id = Column(Integer, primary_key=True)
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    site_index_id = Column(Integer, ForeignKey('site.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    # SBB20100914 Added Agency Location foreign key
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    name = Column(String(50))
    confidential = Column(String(50))
    description = Column(String(50))
    useexisting = True
    
 
class ApplicationProcess(DB.Base, MapBase):
    __tablename__ = 'application_process'
    id = Column(Integer, primary_key=True)
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    step = Column(String(50))
    description = Column(String(50))
    useexisting = True
    
 
class Assignment(DB.Base, MapBase):
    __tablename__ = 'assignment'
    id = Column(Integer, primary_key=True)
    hmis_asset_index_id = Column(Integer, ForeignKey('hmis_asset.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    assignment_id_id_num = Column(String(50))
    assignment_id_id_str = Column(String(32))
    assignment_id_delete = Column(Integer)
    assignment_id_delete_occurred_date = Column(DateTime(timezone=False))
    assignment_id_delete_effective_date = Column(DateTime(timezone=False))
    person_id_id_num = Column(String(50))
    person_id_id_str = Column(String(32))
    household_id_id_num = Column(String(50))
    household_id_id_str = Column(String(32))
    useexisting = True
    
 
class AssignmentPeriod(DB.Base, MapBase):
    __tablename__ = 'assignment_period'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    assignment_index_id = Column(Integer, ForeignKey(Assignment.id)) 
    assignment_period_start_date = Column(DateTime(timezone=False))
    assignment_period_end_date = Column(DateTime(timezone=False))
    useexisting = True
    
class Call(DB.Base, MapBase):
    __tablename__ = 'call'
    id = Column(Integer, primary_key=True)
    site_service_id = Column(String(50))
    call_id_id_num = Column(String(50))
    call_id_id_str = Column(String(32))
    call_time = Column(DateTime(timezone=False))
    call_duration = Column(Interval())
    caseworker_id_id_num = Column(String(50))
    caseworker_id_id_str = Column(String(32))
    # FBY : TBC requested|required fields
    caller_zipcode = Column(String(10))
    caller_city = Column(String(128))
    caller_state = Column(String(2))
    caller_home_phone = Column(String(10))

 
class ChildEnrollmentStatus(DB.Base, MapBase):
    __tablename__ = 'child_enrollment_status'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    child_enrollment_status_id_id_num = Column(String(50))
    child_enrollment_status_id_id_str = Column(String(32))
    child_enrollment_status_id_delete = Column(Integer)
    child_enrollment_status_id_delete_occurred_date = Column(DateTime(timezone=False))
    child_enrollment_status_id_delete_effective_date = Column(DateTime(timezone=False))
    child_currently_enrolled_in_school = Column(String(50))
    child_currently_enrolled_in_school_date_effective = Column(DateTime(timezone=False))
    child_currently_enrolled_in_school_date_collected = Column(DateTime(timezone=False))        
    child_currently_enrolled_in_school_data_collection_stage = Column(String(50))
    child_school_name = Column(String(50))
    child_school_name_date_effective = Column(DateTime(timezone=False))
    child_school_name_date_collected = Column(DateTime(timezone=False))        
    child_school_name_data_collection_stage = Column(String(50))        
    child_mckinney_vento_liaison = Column(String(50))
    child_mckinney_vento_liaison_date_effective = Column(DateTime(timezone=False))
    child_mckinney_vento_liaison_date_collected = Column(DateTime(timezone=False))        
    child_mckinney_vento_liaison_data_collection_stage = Column(String(50))   
    child_school_type = Column(String(50))
    child_school_type_date_effective = Column(DateTime(timezone=False))
    child_school_type_date_collected = Column(DateTime(timezone=False))        
    child_school_type_data_collection_stage = Column(String(50))   
    child_school_last_enrolled_date = Column(DateTime(timezone=False))
    child_school_last_enrolled_date_date_collected = Column(DateTime(timezone=False))        
    child_school_last_enrolled_date_data_collection_stage = Column(String(50))           
    useexisting = True
    
 
class ChildEnrollmentStatusBarrier(DB.Base, MapBase):
    __tablename__ = 'child_enrollment_status_barrier'
    id = Column(Integer, primary_key=True)
    child_enrollment_status_index_id = Column(Integer, ForeignKey(ChildEnrollmentStatus.id))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    barrier_id_id_num = Column(String(50))
    barrier_id_id_str = Column(String(32))
    barrier_id_delete = Column(Integer)
    barrier_id_delete_occurred_date = Column(DateTime(timezone=False))
    barrier_id_delete_effective_date = Column(DateTime(timezone=False))
    barrier_code = Column(String(50))
    barrier_code_date_collected = Column(DateTime(timezone=False))
    barrier_code_date_effective = Column(DateTime(timezone=False))        
    barrier_code_data_collection_stage = Column(String(50))
    barrier_other = Column(String(50))
    barrier_other_date_collected = Column(DateTime(timezone=False))
    barrier_other_date_effective = Column(DateTime(timezone=False))        
    barrier_other_data_collection_stage = Column(String(50))        
    useexisting = True
    
 
class ChronicHealthCondition(DB.Base, MapBase):
    __tablename__ = 'chronic_health_condition'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    has_chronic_health_condition = Column(String(50))
    has_chronic_health_condition_date_collected = Column(DateTime(timezone=False))
    has_chronic_health_condition_date_effective = Column(DateTime(timezone=False))        
    has_chronic_health_condition_data_collection_stage = Column(String(50))
    receive_chronic_health_services = Column(String(50))
    receive_chronic_health_services_date_collected = Column(DateTime(timezone=False))
    receive_chronic_health_services_date_effective = Column(DateTime(timezone=False))        
    receive_chronic_health_services_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class Contact(DB.Base, MapBase):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    agency_index_id = Column(Integer, ForeignKey('agency.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    resource_info_index_id = Column(Integer, ForeignKey('resource_info.id'))
    site_index_id = Column(Integer, ForeignKey('site.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    title = Column(String(50))
    name = Column(String(50))
    type = Column(String(50))
    useexisting = True
    
 
class ContactMade(DB.Base, MapBase):
    __tablename__ = 'contact_made'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    contact_id_id_num = Column(String(50))
    contact_id_id_str = Column(String(32))
    contact_id_delete = Column(Integer)
    contact_id_delete_occurred_date = Column(DateTime(timezone=False))
    contact_id_delete_effective_date = Column(DateTime(timezone=False))
    contact_date = Column(DateTime(timezone=False))
    contact_date_data_collection_stage = Column(String(50))
    contact_location = Column(String(50))
    contact_location_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class CrossStreet(DB.Base, MapBase):
    __tablename__ = 'cross_street'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_index_id = Column(Integer, ForeignKey('site.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    cross_street = Column(String(50))
    useexisting = True
    
 
class CurrentlyInSchool(DB.Base, MapBase):
    __tablename__ = 'currently_in_school'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    currently_in_school = Column(String(50))
    currently_in_school_date_collected = Column(DateTime(timezone=False))
    currently_in_school_date_effective = Column(DateTime(timezone=False))        
    currently_in_school_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class LicenseAccreditation(DB.Base, MapBase):
    __tablename__ = 'license_accreditation'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    license = Column(String(50))
    licensed_by = Column(String(50))
    useexisting = True
    
 
class MentalHealthProblem(DB.Base, MapBase):
    __tablename__ = 'mental_health_problem'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    has_mental_health_problem = Column(String(50))
    has_mental_health_problem_date_collected = Column(DateTime(timezone=False))
    has_mental_health_problem_date_effective = Column(DateTime(timezone=False))        
    has_mental_health_problem_data_collection_stage = Column(String(50))
    mental_health_indefinite = Column(String(50))
    mental_health_indefinite_date_collected = Column(DateTime(timezone=False))
    mental_health_indefinite_date_effective = Column(DateTime(timezone=False))        
    mental_health_indefinite_data_collection_stage = Column(String(50))
    receive_mental_health_services = Column(String(50))
    receive_mental_health_services_date_collected = Column(DateTime(timezone=False))
    receive_mental_health_services_date_effective = Column(DateTime(timezone=False))        
    receive_mental_health_services_data_collection_stage = Column(String(50))        
    useexisting = True
    
    
class NonCashBenefits(DB.Base, MapBase):
    __tablename__ = 'non_cash_benefits'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    non_cash_benefit_id_id_num = Column(String(50))
    non_cash_benefit_id_id_str = Column(String(32))
    non_cash_benefit_id_id_delete = Column(Integer)
    non_cash_benefit_id_id_delete_occurred_date = Column(DateTime(timezone=False))
    non_cash_benefit_id_id_delete_effective_date = Column(DateTime(timezone=False))
    non_cash_source_code = Column(String(50))
    non_cash_source_code_date_collected = Column(DateTime(timezone=False))
    non_cash_source_code_date_effective = Column(DateTime(timezone=False))        
    non_cash_source_code_data_collection_stage = Column(String(50))
    non_cash_source_other = Column(String(50))
    non_cash_source_other_date_collected = Column(DateTime(timezone=False))
    non_cash_source_other_date_effective = Column(DateTime(timezone=False))        
    non_cash_source_other_data_collection_stage = Column(String(50))
    receiving_non_cash_source = Column(String(50))
    receiving_non_cash_source_date_collected = Column(DateTime(timezone=False))
    receiving_non_cash_source_date_effective = Column(DateTime(timezone=False))        
    receiving_non_cash_source_data_collection_stage = Column(String(50))     
    useexisting = True
    
    
class AgencyLocation(DB.Base, MapBase):
    __tablename__ = 'agency_location'
    id = Column(Integer, primary_key=True)
    agency_index_id = Column(Integer, ForeignKey('agency.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    key = Column(String(50))
    name = Column(String(50))
    site_description = Column(String(50))
    physical_address_pre_address_line = Column(String(100))
    physical_address_line_1 = Column(String(100))
    physical_address_line_2 = Column(String(100))
    physical_address_city = Column(String(50))
    physical_address_country = Column(String(50))
    physical_address_state = Column(String(50))
    physical_address_zip_code = Column(String(50))
    physical_address_county = Column(String(50))
    physical_address_reason_withheld = Column(String(50))
    physical_address_confidential = Column(String(50))
    physical_address_description = Column(String(50))
    mailing_address_pre_address_line = Column(String(100))
    mailing_address_line_1 = Column(String(100))
    mailing_address_line_2 = Column(String(100))
    mailing_address_city = Column(String(50))
    mailing_address_county = Column(String(50))
    mailing_address_state = Column(String(50))
    mailing_address_zip_code = Column(String(50))
    mailing_address_country = Column(String(50))
    mailing_address_reason_withheld = Column(String(50))
    mailing_address_confidential = Column(String(50))
    mailing_address_description = Column(String(50))
    no_physical_address_description = Column(String(50))
    no_physical_address_explanation = Column(String(50))
    disabilities_access = Column(String(50))
    physical_location_description = Column(String(50))
    bus_service_access = Column(String(50))
    public_access_to_transportation = Column(String(50))
    year_inc = Column(String(50))
    annual_budget_total = Column(String(50))
    legal_status = Column(String(50))
    exclude_from_website = Column(String(50))
    exclude_from_directory = Column(String(50))
    useexisting = True
    
 
class AgencyService(DB.Base, MapBase):
    __tablename__ = 'agency_service'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    key = Column(String(50))
    agency_key = Column(String(50))
    name = Column(String(50))
    useexisting = True
    
 
class NonCashBenefitsLast30Days(DB.Base, MapBase):
    __tablename__ = 'non_cash_benefits_last_30_days'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    income_last_30_days = Column(String(50))
    income_last_30_days_date_collected = Column(DateTime(timezone=False))
    income_last_30_days_date_effective = Column(DateTime(timezone=False))        
    income_last_30_days_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class OtherAddress(DB.Base, MapBase):
    __tablename__ = 'other_address'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_index_id = Column(Integer, ForeignKey('site.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    pre_address_line = Column(String(100))
    line_1 = Column(String(100))
    line_2 = Column(String(100))
    city = Column(String(50))
    county = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(50))
    country = Column(String(50))
    reason_withheld = Column(String(50))
    confidential = Column(String(50))
    description = Column(String(50))
    useexisting = True
    
 
class OtherRequirements(DB.Base, MapBase):
    __tablename__ = 'other_requirements'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    other_requirements = Column(String(50))
    useexisting = True
    
 
class Phone(DB.Base, MapBase):
    __tablename__ = 'phone'
    id = Column(Integer, primary_key=True)
    agency_index_id = Column(Integer, ForeignKey('agency.id'))
    export_index_id = Column(Integer, ForeignKey('export.id')) 
    contact_index_id = Column(Integer, ForeignKey(Contact.id)) 
    resource_info_index_id = Column(Integer, ForeignKey('resource_info.id')) 
    site_index_id = Column(Integer, ForeignKey('site.id')) 
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    phone_number = Column(String(50))
    reason_withheld = Column(String(50))
    extension = Column(String(50))
    description = Column(String(50))
    type = Column(String(50))
    function = Column(String(50))
    toll_free = Column(String(50))
    confidential = Column(String(50))
    person_phone_number = Column(String(50))
    person_phone_number_date_collected = Column(DateTime(timezone=False))
    person_phone_number_date_effective = Column(DateTime(timezone=False))        
    person_phone_number_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class PhysicalDisability(DB.Base, MapBase):
    __tablename__ = 'physical_disability'
    id = Column(Integer, primary_key=True)
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    has_physical_disability = Column(String(50))
    has_physical_disability_date_collected = Column(DateTime(timezone=False))
    has_physical_disability_date_effective = Column(DateTime(timezone=False))        
    has_physical_disability_data_collection_stage = Column(String(50))
    receive_physical_disability_services = Column(String(50))
    receive_physical_disability_services_date_collected = Column(DateTime(timezone=False))
    receive_physical_disability_services_date_effective = Column(DateTime(timezone=False))        
    receive_physical_disability_services_data_collection_stage = Column(String(50))        
    useexisting = True
    
 
class PitCountSet(DB.Base, MapBase):
    __tablename__ = 'pit_count_set'
    id = Column(Integer, primary_key=True)
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    export_index_id = Column(Integer, ForeignKey('export.id'))
    pit_count_set_id_id_num = Column(String(50))
    pit_count_set_id_id_str = Column(String(32))
    pit_count_set_id_delete = Column(Integer)
    pit_count_set_id_delete_occurred_date = Column(DateTime(timezone=False))
    pit_count_set_id_delete_effective_date = Column(DateTime(timezone=False))
    hud_waiver_received = Column(String(50))
    hud_waiver_date = Column(DateTime(timezone=False))
    hud_waiver_effective_period_start_date = Column(DateTime(timezone=False))
    hud_waiver_effective_period_end_date = Column(DateTime(timezone=False))
    last_pit_sheltered_count_date = Column(DateTime(timezone=False))
    last_pit_unsheltered_count_date = Column(DateTime(timezone=False))
    useexisting = True
    
 
class PitCounts(DB.Base, MapBase):
    __tablename__ = 'pit_counts'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    pit_count_set_index_id = Column(Integer, ForeignKey(PitCountSet.id)) 
    pit_count_value = Column(String(50))
    pit_count_effective_period_start_date = Column(DateTime(timezone=False))
    pit_count_effective_period_end_date = Column(DateTime(timezone=False))
    pit_count_recorded_date = Column(DateTime(timezone=False))
    pit_count_household_type = Column(String(50))
    useexisting = True
    
 
class Pregnancy(DB.Base, MapBase):
    __tablename__ = 'pregnancy'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    pregnancy_id_id_num = Column(String(50))
    pregnancy_id_id_str = Column(String(32))
    pregnancy_id_id_delete = Column(Integer)
    pregnancy_id_id_delete_occurred_date = Column(DateTime(timezone=False))
    pregnancy_id_id_delete_effective_date = Column(DateTime(timezone=False))
    pregnancy_status = Column(String(50))
    pregnancy_status_date_collected = Column(DateTime(timezone=False))
    pregnancy_status_date_effective = Column(DateTime(timezone=False))        
    pregnancy_status_data_collection_stage = Column(String(50))
    due_date = Column(DateTime(timezone=False))
    due_date_date_collected = Column(DateTime(timezone=False))        
    due_date_data_collection_stage = Column(String(50))        
    useexisting = True
    
 
class Degree(DB.Base, MapBase):
    __tablename__ = 'degree'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    degree_id_id_num = Column(String(50))
    degree_id_id_str = Column(String(32))
    degree_id_delete = Column(Integer)
    degree_id_delete_occurred_date = Column(DateTime(timezone=False))
    degree_id_delete_effective_date = Column(DateTime(timezone=False))
    degree_other = Column(String(50))
    degree_other_date_collected = Column(DateTime(timezone=False))
    degree_other_date_effective = Column(DateTime(timezone=False))        
    degree_other_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class PriorResidence(DB.Base, MapBase):
    __tablename__ = 'prior_residence'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    prior_residence_id_id_num = Column(String(50))
    prior_residence_id_id_str = Column(String(32))
    prior_residence_id_delete = Column(Integer)
    prior_residence_id_delete_occurred_date = Column(DateTime(timezone=False))
    prior_residence_id_delete_effective_date = Column(DateTime(timezone=False))
    prior_residence_code = Column(String(50))
    prior_residence_code_date_collected = Column(DateTime(timezone=False))
    prior_residence_code_date_effective = Column(DateTime(timezone=False))        
    prior_residence_code_data_collection_stage = Column(String(50))
    prior_residence_other = Column(String(50))
    prior_residence_other_date_collected = Column(DateTime(timezone=False))
    prior_residence_other_date_effective = Column(DateTime(timezone=False))        
    prior_residence_other_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class DegreeCode(DB.Base, MapBase):
    __tablename__ = 'degree_code'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    degree_index_id = Column(Integer, ForeignKey(Degree.id)) 
    degree_code = Column(String(50))
    degree_date_collected = Column(DateTime(timezone=False))
    degree_date_effective = Column(DateTime(timezone=False))        
    degree_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class Destinations(DB.Base, MapBase):
    __tablename__ = 'destinations'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    destination_id_id_num = Column(String(50))
    destination_id_id_str = Column(String(32))
    destination_id_delete = Column(Integer)
    destination_id_delete_occurred_date = Column(DateTime(timezone=False))
    destination_id_delete_effective_date = Column(DateTime(timezone=False))
    destination_code = Column(String(50))
    destination_code_date_collected = Column(DateTime(timezone=False))
    destination_code_date_effective = Column(DateTime(timezone=False))        
    destination_code_data_collection_stage = Column(String(50))
    destination_other = Column(String(50))
    destination_other_date_collected = Column(DateTime(timezone=False))
    destination_other_date_effective = Column(DateTime(timezone=False))        
    destination_other_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class ReasonsForLeaving(DB.Base, MapBase):
    __tablename__ = 'reasons_for_leaving'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_participation_index_id = Column(Integer, ForeignKey('site_service_participation.id')) 
    reason_for_leaving_id_id_num = Column(String(50))
    reason_for_leaving_id_id_str = Column(String(32))
    reason_for_leaving_id_delete = Column(Integer)
    reason_for_leaving_id_delete_occurred_date = Column(DateTime(timezone=False))
    reason_for_leaving_id_delete_effective_date = Column(DateTime(timezone=False))
    reason_for_leaving = Column(String(50))
    reason_for_leaving_date_collected = Column(DateTime(timezone=False))
    reason_for_leaving_date_effective = Column(DateTime(timezone=False))        
    reason_for_leaving_data_collection_stage = Column(String(50))
    reason_for_leaving_other = Column(String(50))
    reason_for_leaving_other_date_collected = Column(DateTime(timezone=False))
    reason_for_leaving_other_date_effective = Column(DateTime(timezone=False))        
    reason_for_leaving_other_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class DevelopmentalDisability(DB.Base, MapBase):
    __tablename__ = 'developmental_disability'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    has_developmental_disability = Column(String(50))
    has_developmental_disability_date_collected = Column(DateTime(timezone=False))
    has_developmental_disability_date_effective = Column(DateTime(timezone=False))        
    has_developmental_disability_data_collection_stage = Column(String(50))
    receive_developmental_disability = Column(String(50))
    receive_developmental_disability_date_collected = Column(DateTime(timezone=False))
    receive_developmental_disability_date_effective = Column(DateTime(timezone=False))        
    receive_developmental_disability_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class DisablingCondition(DB.Base, MapBase):
    __tablename__ = 'disabling_condition'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    disabling_condition = Column(String(50))
    disabling_condition_date_collected = Column(DateTime(timezone=False))
    disabling_condition_date_effective = Column(DateTime(timezone=False))        
    disabling_condition_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class DocumentsRequired(DB.Base, MapBase):
    __tablename__ = 'documents_required'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    documents_required = Column(String(50))
    description = Column(String(50))
    useexisting = True
    
 
class ResidencyRequirements(DB.Base, MapBase):
    __tablename__ = 'residency_requirements'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    residency_requirements = Column(String(50))
    useexisting = True
    
 
class DomesticViolence(DB.Base, MapBase):
    __tablename__ = 'domestic_violence'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    domestic_violence_survivor = Column(String(50))
    domestic_violence_survivor_date_collected = Column(DateTime(timezone=False))
    domestic_violence_survivor_date_effective = Column(DateTime(timezone=False))        
    domestic_violence_survivor_data_collection_stage = Column(String(50))
    dv_occurred = Column(String(50))
    dv_occurred_date_collected = Column(DateTime(timezone=False))
    dv_occurred_date_effective = Column(DateTime(timezone=False))        
    dv_occurred_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class Email(DB.Base, MapBase):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    contact_index_id = Column(Integer, ForeignKey(Contact.id)) 
    resource_info_index_id = Column(Integer, ForeignKey('resource_info.id')) 
    site_index_id = Column(Integer, ForeignKey('site.id')) 
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    address = Column(String(100))
    note = Column(String(50))
    person_email = Column(String(50))
    person_email_date_collected = Column(DateTime(timezone=False))
    person_email_date_effective = Column(DateTime(timezone=False))        
    person_email_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class Seasonal(DB.Base, MapBase):
    __tablename__ = 'seasonal'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    description = Column(String(50))
    start_date = Column(String(50))
    end_date = Column(String(50))
    useexisting = True
    
 
class Employment(DB.Base, MapBase):
    __tablename__ = 'employment'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    employment_id_id_num = Column(String(50))
    employment_id_id_str = Column(String(32))
    employment_id_id_delete = Column(Integer)
    employment_id_id_delete_occurred_date = Column(DateTime(timezone=False))
    employment_id_id_delete_effective_date = Column(DateTime(timezone=False))
    currently_employed = Column(String(50))
    currently_employed_date_collected = Column(DateTime(timezone=False))
    currently_employed_date_effective = Column(DateTime(timezone=False))        
    currently_employed_data_collection_stage = Column(String(50))
    hours_worked_last_week = Column(String(50))
    hours_worked_last_week_date_collected = Column(DateTime(timezone=False))
    hours_worked_last_week_date_effective = Column(DateTime(timezone=False))        
    hours_worked_last_week_data_collection_stage = Column(String(50))
    employment_tenure = Column(String(50))
    employment_tenure_date_collected = Column(DateTime(timezone=False))
    employment_tenure_date_effective = Column(DateTime(timezone=False))        
    employment_tenure_data_collection_stage = Column(String(50))
    looking_for_work = Column(String(50))
    looking_for_work_date_collected = Column(DateTime(timezone=False))
    looking_for_work_date_effective = Column(DateTime(timezone=False))        
    looking_for_work_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class EngagedDate(DB.Base, MapBase):
    __tablename__ = 'engaged_date'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    engaged_date = Column(DateTime(timezone=False))
    engaged_date_date_collected = Column(DateTime(timezone=False))        
    engaged_date_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class ServiceEventNotes(DB.Base, MapBase):
    __tablename__ = 'service_event_notes'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    service_event_index_id = Column(Integer, ForeignKey('service_event.id')) 
    note_id_id_num = Column(String(50))
    note_id_id_str = Column(String(32))
    note_delete = Column(Integer)
    note_delete_occurred_date = Column(DateTime(timezone=False))
    note_delete_effective_date = Column(DateTime(timezone=False))
    note_text = Column(String(255))
    note_text_date_collected = Column(DateTime(timezone=False))
    note_text_date_effective = Column(DateTime(timezone=False))        
    note_text_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class FamilyRequirements(DB.Base, MapBase):
    __tablename__ = 'family_requirements'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    family_requirements = Column(String(50))
    useexisting = True
    
 
class ServiceGroup(DB.Base, MapBase):
    __tablename__ = 'service_group'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    key = Column(String(50))
    name = Column(String(50))
    program_name = Column(String(50))
    useexisting = True
    
 
class GeographicAreaServed(DB.Base, MapBase):
    __tablename__ = 'geographic_area_served'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    zipcode = Column(String(50))
    census_track = Column(String(50))
    city = Column(String(50))
    county = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    description = Column(String(50))
    useexisting = True
    
 
class HealthStatus(DB.Base, MapBase):
    __tablename__ = 'health_status'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    health_status = Column(String(50))
    health_status_date_collected = Column(DateTime(timezone=False))
    health_status_date_effective = Column(DateTime(timezone=False))        
    health_status_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class HighestSchoolLevel(DB.Base, MapBase):
    __tablename__ = 'highest_school_level'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    highest_school_level = Column(String(50))
    highest_school_level_date_collected = Column(DateTime(timezone=False))
    highest_school_level_date_effective = Column(DateTime(timezone=False))        
    highest_school_level_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class HivAidsStatus(DB.Base, MapBase):
    __tablename__ = 'hiv_aids_status'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    has_hiv_aids = Column(String(50))
    has_hiv_aids_date_collected = Column(DateTime(timezone=False))
    has_hiv_aids_date_effective = Column(DateTime(timezone=False))        
    has_hiv_aids_data_collection_stage = Column(String(50))
    receive_hiv_aids_services = Column(String(50))
    receive_hiv_aids_services_date_collected = Column(DateTime(timezone=False))
    receive_hiv_aids_services_date_effective = Column(DateTime(timezone=False))        
    receive_hiv_aids_services_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class SpatialLocation(DB.Base, MapBase):
    __tablename__ = 'spatial_location'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_index_id = Column(Integer, ForeignKey('site.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    description = Column(String(50))
    datum = Column(String(50))
    latitude = Column(String(50))
    longitude = Column(String(50))
    useexisting = True
    
 
class HmisAsset(DB.Base, MapBase):
    __tablename__ = 'hmis_asset'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_index_id = Column(Integer, ForeignKey('site.id')) 
    asset_id_id_num = Column(String(50))
    asset_id_id_str = Column(String(32))
    asset_id_delete = Column(Integer)
    asset_id_delete_occurred_date = Column(DateTime(timezone=False))
    asset_id_delete_effective_date = Column(DateTime(timezone=False))
    asset_count = Column(String(50))
    asset_count_bed_availability = Column(String(50))
    asset_count_bed_type = Column(String(50))
    asset_count_bed_individual_family_type = Column(String(50))
    asset_count_chronic_homeless_bed = Column(String(50))
    asset_count_domestic_violence_shelter_bed = Column(String(50))
    asset_count_household_type = Column(String(50))
    asset_type = Column(String(50))
    asset_effective_period_start_date = Column(DateTime(timezone=False))
    asset_effective_period_end_date = Column(DateTime(timezone=False))
    asset_recorded_date = Column(DateTime(timezone=False))
    useexisting = True
    
 
class SubstanceAbuseProblem(DB.Base, MapBase):
    __tablename__ = 'substance_abuse_problem'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    has_substance_abuse_problem = Column(String(50))
    has_substance_abuse_problem_date_collected = Column(DateTime(timezone=False))
    has_substance_abuse_problem_date_effective = Column(DateTime(timezone=False))        
    has_substance_abuse_problem_data_collection_stage = Column(String(50))
    substance_abuse_indefinite = Column(String(50))
    substance_abuse_indefinite_date_collected = Column(DateTime(timezone=False))
    substance_abuse_indefinite_date_effective = Column(DateTime(timezone=False))        
    substance_abuse_indefinite_data_collection_stage = Column(String(50))
    receive_substance_abuse_services = Column(String(50))
    receive_substance_abuse_services_date_collected = Column(DateTime(timezone=False))
    receive_substance_abuse_services_date_effective = Column(DateTime(timezone=False))        
    receive_substance_abuse_services_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class HousingStatus(DB.Base, MapBase):
    __tablename__ = 'housing_status'        
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    housing_status = Column(String(50))
    housing_status_date_collected = Column(DateTime(timezone=False))
    housing_status_date_effective = Column(DateTime(timezone=False))        
    housing_status_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class Taxonomy(DB.Base, MapBase):
    __tablename__ = 'taxonomy'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    need_index_id = Column(Integer, ForeignKey('need.id')) 
    code = Column(String(300))
    useexisting = True
    
 
class HudChronicHomeless(DB.Base, MapBase):
    __tablename__ = 'hud_chronic_homeless'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    hud_chronic_homeless = Column(String(50))
    hud_chronic_homeless_date_collected = Column(DateTime(timezone=False))
    hud_chronic_homeless_date_effective = Column(DateTime(timezone=False))        
    hud_chronic_homeless_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class TimeOpen(DB.Base, MapBase):
    __tablename__ = 'time_open'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_index_id = Column(Integer, ForeignKey('site.id')) 
    languages_index_id = Column(Integer, ForeignKey('languages.id')) 
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    notes = Column(String(50))
    useexisting = True
    
 
class TimeOpenDays(DB.Base, MapBase):
    __tablename__ = 'time_open_days'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    time_open_index_id = Column(Integer, ForeignKey(TimeOpen.id)) 
    day_of_week = Column(String(50))
    from_time = Column(String(50))
    to_time = Column(String(50))
    useexisting = True
    
 
class Url(DB.Base, MapBase):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    agency_index_id = Column(Integer, ForeignKey('agency.id')) 
    site_index_id = Column(Integer, ForeignKey('site.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    address = Column(String(50))
    note = Column(String(50))
    useexisting = True
    
 
class VeteranMilitaryBranches(DB.Base, MapBase):
    __tablename__ = 'veteran_military_branches'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    military_branch_id_id_num = Column(String(50))
    military_branch_id_id_str = Column(String(32))
    military_branch_id_id_delete = Column(Integer)
    military_branch_id_id_delete_occurred_date = Column(DateTime(timezone=False))
    military_branch_id_id_delete_effective_date = Column(DateTime(timezone=False))
    discharge_status = Column(String(50))
    discharge_status_date_collected = Column(DateTime(timezone=False))
    discharge_status_date_effective = Column(DateTime(timezone=False))        
    discharge_status_data_collection_stage = Column(String(50))
    discharge_status_other = Column(String(50))
    discharge_status_other_date_collected = Column(DateTime(timezone=False))
    discharge_status_other_date_effective = Column(DateTime(timezone=False))        
    discharge_status_other_data_collection_stage = Column(String(50))
    military_branch = Column(String(50))
    military_branch_date_collected = Column(DateTime(timezone=False))
    military_branch_date_effective = Column(DateTime(timezone=False))        
    military_branch_data_collection_stage = Column(String(50))
    military_branch_other = Column(String(50))
    military_branch_other_date_collected = Column(DateTime(timezone=False))
    military_branch_other_date_effective = Column(DateTime(timezone=False))        
    military_branch_other_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class IncomeLast30Days(DB.Base, MapBase):
    __tablename__ = 'income_last_30_days'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    income_last_30_days = Column(String(50))
    income_last_30_days_date_collected = Column(DateTime(timezone=False))
    income_last_30_days_date_effective = Column(DateTime(timezone=False))        
    income_last_30_days_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class VeteranMilitaryServiceDuration(DB.Base, MapBase):
    __tablename__ = 'veteran_military_service_duration'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    military_service_duration = Column(String(50))
    military_service_duration_date_collected = Column(DateTime(timezone=False))
    military_service_duration_date_effective = Column(DateTime(timezone=False))        
    military_service_duration_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class IncomeRequirements(DB.Base, MapBase):
    __tablename__ = 'income_requirements'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id')) 
    income_requirements = Column(String(50))
    useexisting = True
    
 
class VeteranServedInWarZone(DB.Base, MapBase):
    __tablename__ = 'veteran_served_in_war_zone'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    served_in_war_zone = Column(String(50))
    served_in_war_zone_date_collected = Column(DateTime(timezone=False))
    served_in_war_zone_date_effective = Column(DateTime(timezone=False))        
    served_in_war_zone_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class IncomeTotalMonthly(DB.Base, MapBase):
    __tablename__ = 'income_total_monthly'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    income_total_monthly = Column(String(50))
    income_total_monthly_date_collected = Column(DateTime(timezone=False))
    income_total_monthly_date_effective = Column(DateTime(timezone=False))        
    income_total_monthly_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class VeteranServiceEra(DB.Base, MapBase):
    __tablename__ = 'veteran_service_era'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    service_era = Column(String(50))
    service_era_date_collected = Column(DateTime(timezone=False))
    service_era_date_effective = Column(DateTime(timezone=False))        
    service_era_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class VeteranVeteranStatus(DB.Base, MapBase):
    __tablename__ = 'veteran_veteran_status'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    veteran_status = Column(String(50))
    veteran_status_date_collected = Column(DateTime(timezone=False))
    veteran_status_date_effective = Column(DateTime(timezone=False))        
    veteran_status_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class Languages(DB.Base, MapBase):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_index_id = Column(Integer, ForeignKey('site.id')) 
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    agency_location_index_id = Column(Integer, ForeignKey('agency_location.id'))
    name = Column(String(50))
    notes = Column(String(50))
    useexisting = True
    
 
class VeteranWarzonesServed(DB.Base, MapBase):
    __tablename__ = 'veteran_warzones_served'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    war_zone_id_id_num = Column(String(50))
    war_zone_id_id_str = Column(String(32))
    war_zone_id_id_delete = Column(Integer)
    war_zone_id_id_delete_occurred_date = Column(DateTime(timezone=False))
    war_zone_id_id_delete_effective_date = Column(DateTime(timezone=False))
    months_in_war_zone = Column(String(50))
    months_in_war_zone_date_collected = Column(DateTime(timezone=False))
    months_in_war_zone_date_effective = Column(DateTime(timezone=False))        
    months_in_war_zone_data_collection_stage = Column(String(50))
    received_fire = Column(String(50))
    received_fire_date_collected = Column(DateTime(timezone=False))
    received_fire_date_effective = Column(DateTime(timezone=False))        
    received_fire_data_collection_stage = Column(String(50))
    war_zone = Column(String(50))
    war_zone_date_collected = Column(DateTime(timezone=False))
    war_zone_date_effective = Column(DateTime(timezone=False))        
    war_zone_data_collection_stage = Column(String(50))
    war_zone_other = Column(String(50))
    war_zone_other_date_collected = Column(DateTime(timezone=False))
    war_zone_other_date_effective = Column(DateTime(timezone=False))        
    war_zone_other_data_collection_stage = Column(String(50))                
    useexisting = True
    
 
class LengthOfStayAtPriorResidence(DB.Base, MapBase):
    __tablename__ = 'length_of_stay_at_prior_residence'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    length_of_stay_at_prior_residence = Column(String(50))
    length_of_stay_at_prior_residence_date_collected = Column(DateTime(timezone=False))
    length_of_stay_at_prior_residence_date_effective = Column(DateTime(timezone=False))        
    length_of_stay_at_prior_residence_data_collection_stage = Column(String(50))
    useexisting = True
    
   
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
 
class VocationalTraining(DB.Base, MapBase):
    __tablename__ = 'vocational_training'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    vocational_training = Column(String(50))
    vocational_training_date_collected = Column(DateTime(timezone=False))
    vocational_training_date_effective = Column(DateTime(timezone=False))        
    vocational_training_data_collection_stage = Column(String(50))
    useexisting = True
    
 
class Export(DB.Base, MapBase):
    __tablename__ = 'export'
    id = Column(Integer, primary_key=True)
    export_id = Column(String(50), primary_key=False, unique=False)
    export_id_date_collected = Column(DateTime(timezone=False))
    export_date = Column(DateTime(timezone=False))
    export_date_date_collected = Column(DateTime(timezone=False))
    export_period_start_date = Column(DateTime(timezone=False))
    export_period_start_date_date_collected = Column(DateTime(timezone=False))
    export_period_end_date = Column(DateTime(timezone=False))
    export_period_end_date_date_collected = Column(DateTime(timezone=False))
    export_software_vendor = Column(String(50))
    export_software_vendor_date_collected = Column(DateTime(timezone=False))
    export_software_version = Column(String(10))
    export_software_version_date_collected = Column(DateTime(timezone=False))
    #HUD 3.0
    export_id_id_num = Column(String(50))
    export_id_id_str = Column(String(50))
    export_id_delete_occurred_date = Column(DateTime(timezone=False))
    export_id_delete_effective_date = Column(DateTime(timezone=False))
    export_id_delete = Column(String(32))
    fk_export_to_person = relationship('Person', backref='fk_person_to_export')
    #$fk_export_to_household = relationship('Household', backref='fk_household_to_export')
    # 'fk_export_to_database': relation(Source, backref='fk_database_to_export')
    useexisting = True
    
 
class Report(DB.Base, MapBase):
    __tablename__ = 'report' 
    report_id = Column(String(50), primary_key=True, unique=True) 
    report_id_date_collected = Column(DateTime(timezone=False))
    report_date = Column(DateTime(timezone=False))
    report_date_date_collected = Column(DateTime(timezone=False))
    report_period_start_date = Column(DateTime(timezone=False))
    report_period_start_date_date_collected = Column(DateTime(timezone=False))
    report_period_end_date = Column(DateTime(timezone=False))
    report_period_end_date_date_collected = Column(DateTime(timezone=False))
    report_software_vendor = Column(String(50))
    report_software_vendor_date_collected = Column(DateTime(timezone=False))
    report_software_version = Column(String(10))
    report_software_version_date_collected = Column(DateTime(timezone=False))
    #HUD 3.0
    report_id_id_num = Column(String(50))
    report_id_id_str = Column(String(50))
    report_id_id_delete_occurred_date = Column(DateTime(timezone=False))
    report_id_id_delete_effective_date = Column(DateTime(timezone=False))       
    report_id_id_delete = Column(String(32)) 
    export_index_id = Column(Integer, ForeignKey('export.id'))
    #fk_report_to_person = relationship('Person', backref='fk_person_to_report')
    #fk_report_to_household = relationship('Household', backref='fk_household_to_report')
    #fk_report_to_database = relationship('Source', backref='fk_database_to_report')
    
    useexisting = True
     
class FosterChildEver(DB.Base, MapBase):
    __tablename__ = 'foster_child_ever'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_historical_index_id = Column(Integer, ForeignKey('person_historical.id')) 
    foster_child_ever = Column(Integer)
    foster_child_ever_date_collected = Column(DateTime(timezone=False))
    foster_child_ever_date_effective = Column(DateTime(timezone=False))        
    useexisting = True
    
 
class Household(DB.Base, MapBase):
    __tablename__ = 'household'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_id = Column(String(50), ForeignKey('report.report_id'))
    household_id_num = Column(String(32))
    household_id_num_date_collected = Column(DateTime(timezone=False))
    household_id_str = Column(String(32))
    household_id_str_date_collected = Column(DateTime(timezone=False))
    head_of_household_id_unhashed = Column(String(32))
    head_of_household_id_unhashed_date_collected = Column(DateTime(timezone=False))
    head_of_household_id_hashed = Column(String(32))
    head_of_household_id_hashed_date_collected = Column(DateTime(timezone=False))
    reported = Column(Boolean)
    useexisting = True
    fk_household_to_members = relationship('Members', backref='fk_members_to_household')
    
 
class Person(DB.Base, MapBase):
    __tablename__ = 'person' 
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    report_id = Column(String(50), ForeignKey('report.report_id'))
    person_id_hashed = Column(String(32))
    person_id_unhashed = Column(String(50))
    person_id_date_collected = Column(DateTime(timezone=False))
    person_date_of_birth_hashed = Column(String(32))
    person_date_of_birth_hashed_date_collected = Column(DateTime(timezone=False))
    person_date_of_birth_unhashed = Column(DateTime(timezone=False))
    person_date_of_birth_unhashed_date_collected = Column(DateTime(timezone=False))
    person_ethnicity_hashed = Column(String(32))
    person_ethnicity_unhashed = Column(Integer)
    person_ethnicity_hashed_date_collected = Column(DateTime(timezone=False))
    person_ethnicity_unhashed_date_collected = Column(DateTime(timezone=False))
    person_gender_hashed = Column(String(32))
    person_gender_unhashed = Column(Integer)
    person_gender_hashed_date_collected = Column(DateTime(timezone=False))
    person_gender_unhashed_date_collected = Column(DateTime(timezone=False))
    person_gender_unhashed_date_effective = Column(DateTime(timezone=False))
    person_gender_hashed_date_effective = Column(DateTime(timezone=False))
    person_legal_first_name_hashed = Column(String(32))
    person_legal_first_name_unhashed = Column(String(50))
    person_legal_first_name_hashed_date_collected = Column(DateTime(timezone=False))
    person_legal_first_name_hashed_date_effective = Column(DateTime(timezone=False))
    person_legal_first_name_unhashed_date_collected = Column(DateTime(timezone=False))        
    person_legal_first_name_unhashed_date_effective = Column(DateTime(timezone=False)) # JCS Added
    person_legal_last_name_hashed = Column(String(32))
    person_legal_last_name_unhashed = Column(String(50))
    person_legal_last_name_unhashed_date_collected = Column(DateTime(timezone=False))
    person_legal_last_name_unhashed_date_effective = Column(DateTime(timezone=False))
    person_legal_last_name_hashed_date_collected = Column(DateTime(timezone=False))        
    person_legal_middle_name_hashed = Column(String(32))
    person_legal_middle_name_unhashed = Column(String(50))
    person_legal_middle_name_unhashed_date_collected = Column(DateTime(timezone=False))
    person_legal_middle_name_hashed_date_collected = Column(DateTime(timezone=False))
    person_legal_suffix_hashed = Column(String(32))
    person_legal_suffix_unhashed = Column(String(50))
    person_legal_suffix_unhashed_date_collected = Column(DateTime(timezone=False))
    person_legal_suffix_hashed_date_collected = Column(DateTime(timezone=False))
    #OtherNames is in its own table as there can be multiple OtherNames
    #Race is in its own table as there can be multiple races
    person_social_security_number_hashed = Column(String(32))
    person_social_security_number_unhashed = Column(String(9))
    person_social_security_number_unhashed_date_collected = Column(DateTime(timezone=False))
    person_social_security_number_hashed_date_effective = Column(DateTime(timezone=False))
    person_social_security_number_unhashed_date_effective = Column(DateTime(timezone=False))
    person_social_security_number_hashed_date_collected = Column(DateTime(timezone=False))
    person_social_security_number_quality_code = Column(String(2))
    person_social_security_number_quality_code_date_collected = Column(DateTime(timezone=False))
    person_social_security_number_quality_code_date_effective = Column(DateTime(timezone=False))  
    #PersonHistorical has its own table
    #SiteServiceParticipation has its own table
    #ReleaseOfInformation has its own table
    reported = Column(Boolean)
    # HUD 3.0
    person_id_id_num = Column(String(50))
    person_id_id_str = Column(String(50))
    person_id_delete = Column(String(32))
    person_id_delete_occurred_date = Column(DateTime(timezone=False))
    person_id_delete_effective_date = Column(DateTime(timezone=False))
    person_date_of_birth_type = Column(Integer)
    person_date_of_birth_type_date_collected = Column(DateTime(timezone=False))
    fk_person_to_other_names = relationship('OtherNames', backref='fk_other_names_to_person')
    site_service_participations = relationship("SiteServiceParticipation", backref="person")
    fk_person_to_person_historical = relationship('PersonHistorical', backref='fk_person_historical_to_person')
    fk_person_to_release_of_information = relationship('ReleaseOfInformation', backref='fk_release_of_information_to_person')
    fk_person_to_races = relationship('Races', backref='fk_races_to_person')
    useexisting = True
    
#class DeduplicationLink(DB.Base, MapBase):
 
 
class ServiceEvent(DB.Base, MapBase):
    __tablename__ = 'service_event'
    id = Column(Integer, primary_key=True)
    export_index_id = Column(Integer, ForeignKey('export.id'))
    site_service_index_id = Column(Integer, ForeignKey('site_service.id'))
    household_index_id = Column(Integer, ForeignKey('household.id'))
    person_index_id = Column(Integer, ForeignKey('person.id'))
    need_index_id = Column(Integer, ForeignKey('need.id'))
    site_service_participation_index_id = Column(Integer, ForeignKey('site_service_participation.id'))
    service_event_idid_num = Column(String(32))
    service_event_idid_num_date_collected = Column(DateTime(timezone=False))
    service_event_idid_str = Column(String(32))
    service_event_idid_str_date_collected = Column(DateTime(timezone=False))
    household_idid_num = Column(String(32))
    is_referral = Column(String(32))
    is_referral_date_collected = Column(DateTime(timezone=False))
    quantity_of_service = Column(String(32))
    quantity_of_service_date_collected = Column(DateTime(timezone=False))
    quantity_of_service_measure = Column(String(32))
    quantity_of_service_measure_date_collected = Column(DateTime(timezone=False))
    service_airs_code = Column(String(300))
    service_airs_code_date_collected = Column(DateTime(timezone=False))
    service_period_start_date = Column(DateTime(timezone=False))
    service_period_start_date_date_collected = Column(DateTime(timezone=False))
    service_period_end_date = Column(DateTime(timezone=False))
    service_period_end_date_date_collected = Column(DateTime(timezone=False))
    service_unit = Column(String(32))
    service_unit_date_collected = Column(DateTime(timezone=False))
    type_of_service = Column(String(32))
    type_of_service_date_collected = Column(DateTime(timezone=False))
    type_of_service_other = Column(String(32))
    type_of_service_other_date_collected = Column(DateTime(timezone=False))
    type_of_service_par = Column(Integer)
    #adding a reported column.  Hopefully this will append the column to the table def.
    reported = Column(Boolean)
    service_event_id_delete = Column(String(32))
    service_event_ind_fam = Column(Integer)
    site_service_id = Column(String(50))
    hmis_service_event_code_type_of_service = Column(String(50))
    hmis_service_event_code_type_of_service_other = Column(String(50))
    hprp_financial_assistance_service_event_code = Column(String(50))
    hprp_relocation_stabilization_service_event_code = Column(String(50))
    service_event_id_delete_occurred_date = Column(DateTime(timezone=False))
    service_event_id_delete_effective_date = Column(DateTime(timezone=False))
    service_event_provision_date = Column(DateTime(timezone=False))
    service_event_recorded_date = Column(DateTime(timezone=False))
    useexisting = True
    
class Referral(DB.Base, MapBase):
    __tablename__ = 'referral'
    id = Column(Integer, primary_key=True)
    service_event_index_id = Column(Integer, ForeignKey('service_event.id')) 
    export_index_id = Column(Integer, ForeignKey('export.id'))
    person_index_id = Column(Integer, ForeignKey('person.id'))
    need_index_id = Column(Integer, ForeignKey('need.id'))  # ??
    #referral_id_date_effective = Column(DateTime(timezone=False))
    referral_idid_num = Column(String(50))
    referral_idid_str = Column(String(32))
    referral_delete = Column(Integer)
    referral_delete_occurred_date = Column(DateTime(timezone=False))
    referral_delete_effective_date = Column(DateTime(timezone=False))
    referral_agency_referred_to_idid_num = Column(String(50))
    referral_agency_referred_to_idid_str = Column(String(50))
    referral_agency_referred_to_name = Column(String(50))
    referral_agency_referred_to_name_data_collection_stage = Column(String(50))
    referral_agency_referred_to_name_date_collected = Column(DateTime(timezone=False))
    referral_agency_referred_to_name_date_effective = Column(DateTime(timezone=False))
    referral_call_idid_num = Column(String(50))
    referral_call_idid_str = Column(String(50))
    referral_need_idid_num = Column(String(50)) # In TBC, these refer to an already defined Need
    referral_need_idid_str = Column(String(50))
    useexisting = True
    # FBY : TBC requested|required field
    referral_need_notes = Column(String)

class Source(DB.Base, MapBase):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True)
    report_id = Column(String(50), ForeignKey('report.report_id')) 
    source_id = Column(String(50)) 
    source_id_date_collected = Column(DateTime(timezone=False))
    source_email = Column(String(255))
    source_email_date_collected = Column(DateTime(timezone=False))
    source_contact_extension = Column(String(10))
    source_contact_extension_date_collected = Column(DateTime(timezone=False))
    source_contact_first = Column(String(20))
    source_contact_first_date_collected = Column(DateTime(timezone=False))
    source_contact_last = Column(String(20))
    source_contact_last_date_collected = Column(DateTime(timezone=False))
    source_contact_phone = Column(String(20))
    source_contact_phone_date_collected = Column(DateTime(timezone=False))
    source_name = Column(String(50))
    source_name_date_collected = Column(DateTime(timezone=False)) 
    #HUD 3.0
    schema_version = Column(String(50))
    source_id_id_num = Column(String(50))
    source_id_id_str = Column(String(50))
    source_id_delete = Column(Integer)
    source_id_delete_occurred_date = Column(DateTime(timezone=False))
    source_id_delete_effective_date = Column(DateTime(timezone=False))
    software_vendor = Column(String(50))
    software_version = Column(String(50))
    source_contact_email = Column(String(255))
    useexisting = True
    #properties={'fk_source_to_export': relation(Export, backref='fk_export_to_source')})
        
class SystemConfiguration(DB.Base, MapBase):
    __tablename__ = 'system_configuration_table'
    id = Column(Integer, primary_key=True)
    vendor_name = Column(String(50))
    processing_mode = Column(String(4)) # TEST or PROD
    source_id = Column(String(50))
    odbid = Column(Integer)
    providerid = Column(Integer)
    userid = Column(Integer)
    useexisting = True

class LastDateTime(DB.Base, MapBase):
    # FBY: This table is used to record the document lifecycle: received, shredded, transmitted via SOAP
    __tablename__ = 'last_date_time'
    id = Column(Integer, primary_key=True)
    event = Column(String(50))
    event_date_time = Column(DateTime(timezone=False))        
    useexisting = True

def test():  
    from . import postgresutils
    utils = postgresutils.Utils()
    utils.blank_database()  
    print("instantiating db")
    db = DB()
    session = db.Session()
    db.Base.metadata.create_all(db.pg_db_engine)
    new = Source(source_id_id_num = 1, source_name='Orange County Corrections')
    session.add(new)
    session.commit()
    print("done")

if __name__ == "__main__":
    import sys
    sys.exit(test())    

#The MIT License
#
#Copyright (c) 2011, Alexandria Consulting LLC
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE 
