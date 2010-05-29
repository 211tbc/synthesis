## Adding tables to support HUD 3.0 data standard

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
        Column('reported', Boolean),
        useexisting = True
        )

def upgrade():
    emergency_contact_table.create()

def downgrade():
    emergency_contact_table.drop()