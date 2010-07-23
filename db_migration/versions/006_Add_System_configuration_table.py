from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

system_configuration_odbid_table = Table(
        'sender_system_configuration', 
        meta,
        Column('id', Integer, primary_key=True),
        Column('vendor_name', String(50)),
	Column('processing_mode', String(4)),					# TEST or PROD
        Column('source_id', String(50)),                                        # Sending Organization ID (must be defined before we receive data from them)
        Column('odbid', Integer),
        Column('providerid', Integer),
        Column('userid', Integer),
        useexisting = True
        )

def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    system_configuration_odbid_table.create()

def downgrade():
    # Operations to reverse the above upgrade go here.
    system_configuration_odbid_table.drop()

