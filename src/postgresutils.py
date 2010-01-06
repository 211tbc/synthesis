'''A set of simple utilities to manage the postgres database \n
associated with this code.'''

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, mapper
from conf import settings
import sys
import os

class Employee(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<Employee('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

class Utils:    
    '''Contains some utility methods for a Postgres database'''
    def __init__(self):
        self.table_metadata = MetaData()
        self.employee_table = Table(
        'employee', 
        self.table_metadata, 
        Column('id', Integer, primary_key=True),
        Column('name', String(40)),
        Column('fullname', String(100)),
        Column('password', String(15))
        )
        mapper(Employee, self.employee_table)
        print 'entered the module'
        #self.pg_db = create_engine('postgres://eric:f4rk1r@localhost:5432/coastaldb')
        self.pg_db = create_engine('postgres://%s:%s@localhost:%s/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_PORT, settings.DB_DATABASE) , echo=settings.DEBUG_DB)#, server_side_cursors=True)
        
        self.db_metadata = MetaData(self.pg_db)
        Session = sessionmaker(bind=self.pg_db, autoflush=True, transactional=True)
        self.session = Session()

    def blank_table(self):
        print 'entered the function'
        #self.metadata.drop(bind=self.pg_db)
        self.employee_table.drop(bind=self.pg_db)
        self.session.commit()
        print 'cleared the database'
        
    def create_database(self, databaseName):
        
        if not databaseName == '':
             
            parameters = ['--host=localhost', '--username=%s' % settings.DB_USER, settings.DB_DATABASE, "Synthesis Project Database for %s" % settings.MODE]
            compileCommand = '/usr/bin/createdb'
            if settings.DEBUG:
                print 'creating db with command: %s %s' % (compileCommand, parameters)
            
            rc = os.spawnv(os.P_WAIT, compileCommand, parameters)
            return rc
            
        else:
            raise dbCreateError()
        

    
#def create_database():
#    '''creates a new, empty database.'''
#    metadata = MetaData()
#    metadata.create_all(bind=pg_db)

    def create_test_table(self): 
        print 'entered the function'
        self.table_metadata.create_all(bind=self.pg_db)
        self.session.commit()
        print 'created the employee table'

    def blank_database(self):
        print 'entered the function'
        self.session
        
        self.db_metadata.reflect()
        self.db_metadata.drop_all()
        self.session.commit()
        print 'all tables dropped'
        
if __name__ == '__main__':
    UTILS = Utils()
    UTILS.create_test_table()
    UTILS.blank_table()
    UTILS.blank_database()
