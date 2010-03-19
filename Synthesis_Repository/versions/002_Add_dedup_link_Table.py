from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)
#table_metadata = MetaData(bind=self.pg_db, reflect=True)

dedup_link_table = Table(
                        'dedup_link', 
                        meta, 
                            Column('source_rec_id', String(50), primary_key=True),
                            Column('destination_rec_id', String(50)), 
                            Column('weight_factor', Integer),
                            useexisting = True
                            )

def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    dedup_link_table.create()

def downgrade():
    # Operations to reverse the above upgrade go here.
    dedup_link_table.drop()
