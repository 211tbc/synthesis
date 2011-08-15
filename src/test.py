from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf import settings
import postgresutils

utils = postgresutils.Utils()
utils.blank_database()  
database_string = 'postgresql+psycopg2://' + settings.DB_USER + ':' + settings.DB_PASSWD + '@' + settings.DB_HOST + ':' + str(settings.DB_PORT) + '/' + settings.DB_DATABASE
engine = create_engine(database_string, echo=settings.DEBUG_ALCHEMY)
#mymetadata = MetaData(bind=pg_db_engine)
mymetadata = MetaData()
Base = declarative_base(metadata=mymetadata)
#engine = create_engine('sqlite://')
Session = sessionmaker(bind=engine)#(bind=pg_db_engine)

class Source(Base):
    __tablename__ = 'source'
    id = Column('id',Integer, primary_key=True)
    source_name = Column(String(50))
    export_index_id = Column(Integer, ForeignKey('export.id'))

class Export(Base):
    __tablename__ = 'export'
    id = Column('id',Integer, primary_key=True)
    export_name = Column(String(50))

def main():  
    new = Source(id = 1, source_name='Orange County Corrections')
    new2 = Export(id=3, export_name = 'hello' )
    Base.metadata.create_all(engine)
    session = Session()
    session.add(new)
    session.add(new2)
    session.commit()
    print "done"

if __name__ == "__main__":
    import sys
    sys.exit(main())