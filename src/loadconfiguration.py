from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dbobjects
from conf import settings

def loadData():
   ## pg_db = create_engine('postgres://%s:%s@%s:%s/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_PORT, settings.DB_DATABASE), echo=settings.DEBUG_ALCHEMY)#, server_side_cursors=True)
   ## dbobjects.DatabaseObjects()
   ## #model.init_model(self.pg_db)
   ## Session = sessionmaker(bind=pg_db, autoflush=True)
   ## session = Session()

    #### JCS New 28 sep 11
    db = dbobjects.DB()
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


    session.flush()
    session.commit()
    
if __name__== '__main__':
    loadData()
