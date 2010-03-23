from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)
#table_metadata = MetaData(bind=self.pg_db, reflect=True)

## load foreign key constraints
person_historical_table = Table('person_historical', meta, autoload=True, schema='public')

## add new tables
drug_history_table = Table(
        'drug_history',
        meta,
        Column('id', Integer, primary_key=True),
        Column('person_historical_index_id', Integer, ForeignKey('public.person_historical.id')),
        Column('drug_history_id', String(32)),
        Column('drug_history_id_date_collected', DateTime(timezone=True)),
        Column('drug_code', Integer(2)),
        Column('drug_code_date_collected', DateTime(timezone=True)),    
        Column('drug_use_frequency', Integer(2)),
        Column('drug_use_frequency_date_collected', DateTime(timezone=True)),
        Column('reported', Boolean),
        useexisting = True
        )

def upgrade():
    drug_history_table.create()

def downgrade():
    drug_history_table.drop()