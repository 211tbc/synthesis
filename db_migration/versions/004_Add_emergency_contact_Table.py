from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)
#table_metadata = MetaData(bind=self.pg_db, reflect=True)

## load foreign key constraints
person_historical_table = Table('person_historical', meta, autoload=True, schema='public')

## add new tables
emergency_contact_table = Table(
        'emergency_contact',
        meta,
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey('public.person_historical.id')),
        Column('emergency_contact_id', String(32)),
        Column('emergency_contact_id_date_collected', DateTime(timezone=True)),
        Column('emergency_contact_name', String(32)),
        Column('emergency_contact_name_date_collected', DateTime(timezone=True)),    
        Column('emergency_contact_phone_number_0', String(32)),
        Column('emergency_contact_phone_number_date_collected_0', DateTime(timezone=True)),
        Column('emergency_contact_phone_number_type_0', String(32)),
        Column('emergency_contact_phone_number_1', String(32)),
        Column('emergency_contact_phone_number_date_collected_1', DateTime(timezone=True)),
        Column('emergency_contact_phone_number_type_1', String(32)),
        Column('emergency_contact_address_date_collected', DateTime(timezone=True)),
        Column('emergency_contact_address_start_date', DateTime(timezone=True)),
        Column('emergency_contact_address_start_date_date_collected', DateTime(timezone=True)),
        Column('emergency_contact_address_end_date', DateTime(timezone=True)),
        Column('emergency_contact_address_end_date_date_collected', DateTime(timezone=True)),
        Column('emergency_contact_address_line1', String(32)),
        Column('emergency_contact_address_line1_date_collected', DateTime(timezone=True)),
        Column('emergency_contact_address_line2', String(32)),
        Column('emergency_contact_address_line2_date_collected', DateTime(timezone=True)),
        Column('emergency_contact_address_city', String(32)),
        Column('emergency_contact_address_city_date_collected', DateTime(timezone=True)),
        Column('emergency_contact_address_state', String(32)),
        Column('emergency_contact_address_state_date_collected', DateTime(timezone=True)),    
        Column('emergency_contact_relation_to_client', String(32)),
        Column('emergency_contact_relation_to_client_date_collected', DateTime(timezone=True)),
        Column('reported', Boolean),
        useexisting = True
        )

def upgrade():
    emergency_contact_table.create()

def downgrade():
    emergency_contact_table.drop()