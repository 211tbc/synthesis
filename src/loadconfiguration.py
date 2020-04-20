from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import dbobjects
from .conf import settings

def loadData():
   ## pg_db = create_engine('postgres://%s:%s@%s:%s/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_PORT, settings.DB_DATABASE), echo=settings.DEBUG_ALCHEMY)#, server_side_cursors=True)
   ## dbobjects.DB()
   ## #model.init_model(self.pg_db)
   ## Session = sessionmaker(bind=pg_db, autoflush=True)
   ## session = Session()

    #### JCS New 28 sep 11
    db = dbobjects.DB()
    
    #### FBY 8 dec 11: since the loadconfiguration|nodebuilder step is now automated, drop the system_configuration_table before adding it again.
    db.Base.metadata.tables['system_configuration_table'].drop(checkfirst=True)

    db.Base.metadata.create_all()
    session = db.Session()

    #newRec = {
    #    'vendor_name': 'BASIX_JFCS',
    #    'processing_mode': 'TEST',
    #    'source_id': '2',
    #    'odbid': '873',
    #    'providerid': '115',
    #    'userid': '906'
    #    }
    #dbobjects.SystemConfiguration(newRec)	# Was
    new = dbobjects.SystemConfiguration(vendor_name='BASIX_JFCS',
					processing_mode='TEST',
					source_id='2',
					odbid='873',
					providerid='115',
					userid='906' )	# JCS
    session.add(new)					# JCS
    session.commit

    #newRec = {
    #    'vendor_name': 'BASIX_JFCS',
    #    'processing_mode': 'PROD',
    #    'source_id': '2',
    #    'odbid': '871',
    #    'providerid': '115',
    #    'userid': '906'
    #    }
    #dbobjects.SystemConfiguration(newRec)
    new = dbobjects.SystemConfiguration(vendor_name='BASIX_JFCS',
					processing_mode='PROD',
					source_id='2',
					odbid='871',
					providerid='115',
					userid='906' )	# JCS
    session.add(new)					# JCS
    session.commit
    
    #newRec = {
    #    'vendor_name': 'BASIX_HEART',
    #    'processing_mode': 'TEST',
    #    'source_id': '1',
    #    'odbid': '874',
    #    'providerid': '2105',
    #    'userid': '907'
    #    }
    #dbobjects.SystemConfiguration(newRec)
    new = dbobjects.SystemConfiguration(vendor_name='BASIX_HEART',
					processing_mode='TEST',
					source_id='1',
					odbid='874',
					providerid='2105',
					userid='907' )	# JCS
    session.add(new)					# JCS
    session.commit
    
    #newRec = {
    #    'vendor_name': 'BASIX_HEART',
    #    'processing_mode': 'PROD',
    #    'source_id': '1',
    #    'odbid': '872',
    #    'providerid': '2105',
    #    'userid': '907'
    #    }
    #dbobjects.SystemConfiguration(newRec)
    new = dbobjects.SystemConfiguration(vendor_name='BASIX_HEART',
					processing_mode='PROD',
					source_id='1',
					odbid='872',
					providerid='2105',
					userid='907' )	# JCS
    session.add(new)					# JCS
    session.commit
    
    new = dbobjects.SystemConfiguration(vendor_name='BOWMAN',
					processing_mode='PROD',
					source_id='003',
					odbid='899',
					providerid='3105',
					userid='911' )	# JCS
    session.add(new)					# JCS
    session.commit
    
    new = dbobjects.SystemConfiguration(vendor_name='BOWMAN',
					processing_mode='TEST',
					source_id='003',
					odbid='899',
					providerid='3105',
					userid='911' )	# JCS
    session.add(new)					# JCS
    session.commit

    new = dbobjects.SystemConfiguration(vendor_name='Vendor Name',
					processing_mode='PROD',
					source_id='iH9HiPbW40JbS5m_',
					odbid='999',
					providerid='4105',
					userid='913' )	# JCS
    session.add(new)					# JCS
    session.commit
    
    new = dbobjects.SystemConfiguration(vendor_name='Vendor Name',
					processing_mode='TEST',
					source_id='iH9HiPbW40JbS5m_',
					odbid='999',
					providerid='4105',
					userid='913' )	# JCS
    session.add(new)					# JCS
    session.commit

    new = dbobjects.SystemConfiguration(vendor_name='OCC',
					processing_mode='PROD',
					source_id='004',
					odbid='1899',
					providerid='14105',
					userid='1913' )	# JCS
    session.add(new)					# JCS
    session.commit
    
    new = dbobjects.SystemConfiguration(vendor_name='OCC',
					processing_mode='TEST',
					source_id='004',
					odbid='1899',
					providerid='14105',
					userid='1913' )	# JCS
    session.add(new)					# JCS
    session.commit
    
    new = dbobjects.SystemConfiguration(vendor_name='TBC',
					processing_mode='PROD',
					source_id='tbctest',
					odbid='1999',
					providerid='14106',
					userid='1914' )	# JCS
    session.add(new)					# JCS
    session.commit

    new = dbobjects.SystemConfiguration(vendor_name='TBC',
					processing_mode='TEST',
					source_id='tbctest',
					odbid='1999',
					providerid='14106',
					userid='1914' )	# JCS
    session.add(new)					# JCS
    session.commit

    session.flush()
    session.commit()
    
if __name__== '__main__':
    loadData()
