from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

system_configuration_odbid_table = Table(
        'system_configuration_odbid', 
        meta, 
        Column('vendor_name', String(50), primary_key=True),
	Column('processing_mode', String(4)),					# TEST or PROD 
        Column('odbid', Integer),
        useexisting = True
        )


def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    system_configuration_odbid_table.create()

def downgrade():
    # Operations to reverse the above upgrade go here.
    system_configuration_odbid_table.drop()
