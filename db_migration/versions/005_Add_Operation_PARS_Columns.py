from sqlalchemy import *
from migrate import *
import migrate.changeset

meta = MetaData(migrate_engine)
#table_metadata = MetaData(bind=self.pg_db, reflect=True)

## tables to alter

service_event_table = Table('service_event', meta, autoload=True, schema='public')
site_service_participation_table = Table('site_service_participation', meta, autoload=True, schema='public')
person_historical_table = Table('person_historical', meta, autoload=True, schema='public')

## additional columns

type_of_service_par_col = Column('type_of_service_par', Integer(2))

discharge_type_col = Column('discharge_type', Integer(2))
discharge_type_date_collected_col = Column('discharge_type_date_collected', DateTime(timezone=True))

health_status_at_discharge_col = Column('health_status_at_discharge', Integer(2))
health_status_at_discharge_date_collected_col = Column('health_status_at_discharge_date_collected', DateTime(timezone=True))

va_eligibility_col = Column('va_eligibility', Integer(2))
va_eligibility_date_collected_col = Column('va_eligibility_date_collected', DateTime(timezone=True))

annual_personal_income_col = Column('annual_personal_income', Integer(2))
annual_personal_income_date_collected_col = Column('annual_personal_income_date_collected', DateTime(timezone=True))

employment_status_col = Column('employment_status', Integer(2))
employment_status_date_collected_col = Column('employment_status_date_collected', DateTime(timezone=True))

family_size_col = Column('family_size', Integer(2))
family_size_date_collected_col = Column('family_size_date_collected', DateTime(timezone=True))

hearing_impaired_col = Column('hearing_impaired', Integer(2))
hearing_impaired_date_collected_col = Column('hearing_impaired_date_collected', DateTime(timezone=True))

marital_status_col = Column('marital_status', Integer(2))
marital_status_date_collected_col = Column('marital_status_date_collected', DateTime(timezone=True))

non_ambulatory_col = Column('non_ambulatory', Integer(2))
non_ambulatory_date_collected_col = Column('non_ambulatory_date_collected', DateTime(timezone=True))

residential_status_col = Column('residential_status', Integer(2))
residential_status_date_collected_col = Column('residential_status_date_collected', DateTime(timezone=True))

visually_impaired_col = Column('visually_impaired', Integer(2))
visually_impaired_date_collected_col = Column('visually_impaired_date_collected', DateTime(timezone=True))


def upgrade():
    
    type_of_service_par_col.create(service_event_table)

    discharge_type_col.create(site_service_participation_table)
    discharge_type_date_collected_col.create(site_service_participation_table)
    
    health_status_at_discharge_col.create(site_service_participation_table)
    health_status_at_discharge_date_collected_col.create(site_service_participation_table)
    
    va_eligibility_col.create(site_service_participation_table)
    va_eligibility_date_collected_col.create(site_service_participation_table)

    annual_personal_income_col.create(person_historical_table)
    annual_personal_income_date_collected_col.create(person_historical_table)
    
    employment_status_col.create(person_historical_table)
    employment_status_date_collected_col.create(person_historical_table)
    
    family_size_col.create(person_historical_table)
    family_size_date_collected_col.create(person_historical_table)
    
    hearing_impaired_col.create(person_historical_table)
    hearing_impaired_date_collected_col.create(person_historical_table)
    
    marital_status_col.create(person_historical_table)
    marital_status_date_collected_col.create(person_historical_table)
    
    non_ambulatory_col.create(person_historical_table)
    non_ambulatory_date_collected_col.create(person_historical_table)
    
    residential_status_col.create(person_historical_table)
    residential_status_date_collected_col.create(person_historical_table)
    
    visually_impaired_col.create(person_historical_table)
    visually_impaired_date_collected_col.create(person_historical_table)
    

def downgrade():
    
    type_of_service_par_col.drop(service_event_table)

    discharge_type_col.drop(site_service_participation_table)
    discharge_type_date_collected_col.drop(site_service_participation_table)

    health_status_at_discharge_col.drop(site_service_participation_table)
    health_status_at_discharge_date_collected_col.drop(site_service_participation_table)

    va_eligibility_col.drop(site_service_participation_table)
    va_eligibility_date_collected_col.drop(site_service_participation_table)

    annual_personal_income_col.drop(person_historical_table)
    annual_personal_income_date_collected_col.drop(person_historical_table)
    
    employment_status_col.drop(person_historical_table)
    employment_status_date_collected_col.drop(person_historical_table)
    
    family_size_col.drop(person_historical_table)
    family_size_date_collected_col.drop(person_historical_table)
    
    hearing_impaired_col.drop(person_historical_table)
    hearing_impaired_date_collected_col.drop(person_historical_table)
    
    marital_status_col.drop(person_historical_table)
    marital_status_date_collected_col.drop(person_historical_table)
    
    non_ambulatory_col.drop(person_historical_table)
    non_ambulatory_date_collected_col.drop(person_historical_table)
    
    residential_status_col.drop(person_historical_table)
    residential_status_date_collected_col.drop(person_historical_table)
    
    visually_impaired_col.drop(person_historical_table)
    visually_impaired_date_collected_col.drop(person_historical_table)