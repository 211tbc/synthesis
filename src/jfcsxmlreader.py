#!/usr/bin/python env

import sys, os
from reader import Reader
from zope.interface import implements
from lxml import etree
import dateutil.parser
import dbobjects  as dbobjects

class JFCSXMLReader(dbobjects.DatabaseObjects):
    ''' Synthesis import plugin for JFCS XML 
        JFCS provides 2 simple XML files
        - 1 for service data
        - 1 for client data
        This module parses the XML, maps the
        elements to database fields and 
        commits data to the database
    '''
    
    implements (Reader)
    
    def __init__(self, xml_file):
        self.xml_file = xml_file
        ''' instantiate database object '''
        dbo = dbobjects.DatabaseObjects()
        self.session = dbo.Session()
    
    def read(self):
        ''' suck in raw xml file and build etree object '''
        tree = etree.parse(self.xml_file)
        return tree
    
    def process_data(self, tree, data_type):
        self.data_type = data_type
        ''' call parser based on incoming data type (client or service) '''
        if self.data_type == 'service': self.parse_service(tree)
        elif self.data_type == 'client':  self.parse_client(tree)
        return
    
    def parse_service(self, tree):
        ''' iterate through JFCS service simple xml calling appropriate parsers '''

        ''' we have to lookup person_index_id and site_service_participation_index_id '''
        self.mappedObjects = dbobjects.DatabaseObjects()
        ''' insert xml data into native data structure '''
        for row_element in tree.getiterator(tag="row"):
            self.row_dict = {}
            #print '** NEW ROW'
            for child in row_element:
                if child.text is not None:
                    #print "%s - %s" % (child.tag, child.text)
                    if child.tag == 'c4clientid': self.row_dict.__setitem__('c4clientid', child.text)
                    if child.tag == 'qprogram': self.row_dict.__setitem__('qprogram', child.text)
                    if child.tag == 'serv_code': self.row_dict.__setitem__('serv_code', child.text)
                    if child.tag == 'trdate': self.row_dict.__setitem__('trdate', child.text)
                    if child.tag == 'end_date': self.row_dict.__setitem__('end_date', child.text)
                    if child.tag == 'cunits': self.row_dict.__setitem__('cunits', child.text)
            ''' data fetched, now call the parsers '''
            self.parse_service_event()
        return
    
    def parse_client(self, tree):
        ''' iterate through JFCS service simple xml calling appropriate parsers '''

        ''' insert xml data into native data structure '''
        for row_element in tree.getiterator(tag="row"):
            self.row_dict = {}
            #print '** NEW ROW'
            for child in row_element:
                if child.text is not None:
                    #print "%s - %s" % (child.tag, child.text)
                    if child.tag == 'c4clientid': self.row_dict.__setitem__('c4clientid', child.text)
                    if child.tag == 'c4dob': self.row_dict.__setitem__('c4dob', child.text)
                    if child.tag == 'c4sex': self.row_dict.__setitem__('c4sex', child.text)
                    if child.tag == 'c4firstname': self.row_dict.__setitem__('c4firstname', child.text)
                    if child.tag == 'c4lastname': self.row_dict.__setitem__('c4lastname', child.text)
                    if child.tag == 'c4mi': self.row_dict.__setitem__('c4mi', child.text)
                    if child.tag == 'hispanic': self.row_dict.__setitem__('hispanic', child.text)
                    if child.tag == 'c4ssno': self.row_dict.__setitem__('c4ssno', child.text)
                    if child.tag == 'c4last_s01': self.row_dict.__setitem__('c4last_s01', child.text)
                    if child.tag == 'ethnicity': self.row_dict.__setitem__('ethnicity', child.text)
                    if child.tag == 'aprgcode': self.row_dict.__setitem__('aprgcode', child.text)
                    if child.tag == 'a_date': self.row_dict.__setitem__('a_date', child.text)
                    if child.tag == 't_date': self.row_dict.__setitem__('t_date', child.text)
                    if child.tag == 'family_id': self.row_dict.__setitem__('family_id', child.text)
            ''' data fetched, now call the parsers '''
            self.parse_person()
        return
    
    ''' Parsers for each database table and sub-table relative to input data source '''
    ''' service:
        - service_event
        client:
        - person -> other_names
        - person -> races
        - person -> site_service_participation
        - household -> members
    ''' 

    def parse_service_event(self):
        ''' parse data for service_event table '''
        self.parse_dict = {}
        self.person_index_id = ''
        self.service_index_id = ''
        ''' fetch person.id and site_service_participation.id from seperate imports of client data'''
        self.lookup_person()
        if self.person_index_id != '':
            self.existence_test_and_add('site_service_index_id', self.service_index_id, 'no_handling')
            if self.row_dict.has_key('qprogram'): self.existence_test_and_add('site_service_idid_num', self.row_dict.__getitem__('qprogram'), 'text')
            if self.row_dict.has_key('serv_code'): self.existence_test_and_add('jfcs_type_of_service', self.row_dict.__getitem__('serv_code'), 'text')
            ''' dates may come in filled, blank, or contain just dashes'''
            ''' normalize the date field before sending to db '''
            if self.row_dict.has_key('trdate'):
                test = self.normalize_date(self.row_dict.__getitem__('trdate'))
                if test == True: self.existence_test_and_add('service_period_start_date', self.row_dict.__getitem__('trdate'), 'element_date')
            if self.row_dict.has_key('end_date'):
                test = self.normalize_date(self.row_dict.__getitem__('end_date'))
                if test == True: self.existence_test_and_add('service_period_end_date', self.row_dict.__getitem__('end_date'), 'element_date')
            if self.row_dict.has_key('cunits'): self.existence_test_and_add('quantity_of_service', self.row_dict.__getitem__('cunits'), 'text')
            self.shred(self.parse_dict, dbobjects.ServiceEvent)
    
    def parse_person(self):
        ''' parse data for person table '''
        self.parse_dict = {}
        if self.row_dict.has_key('c4clientid'): self.existence_test_and_add('person_id_unhashed', self.row_dict.__getitem__('c4clientid'), 'text')
        if self.row_dict.has_key('c4dob'): self.existence_test_and_add('person_date_of_birth_unhashed', self.row_dict.__getitem__('c4dob'), 'text')
        if self.row_dict.has_key('c4sex'):
            ''' convert gender to code '''
            if self.row_dict.__getitem__('c4sex').upper() == 'F': gender = "0"
            elif self.row_dict.__getitem__('c4sex').upper() == 'M': gender = "1"
            if gender is not None:
                self.existence_test_and_add('person_gender_unhashed', gender, 'text')
        if self.row_dict.has_key('c4firstname'): self.existence_test_and_add('person_legal_first_name_unhashed', self.row_dict.__getitem__('c4firstname'), 'text')
        if self.row_dict.has_key('c4lastname'): self.existence_test_and_add('person_legal_last_name_unhashed', self.row_dict.__getitem__('c4lastname'), 'text')
        if self.row_dict.has_key('c4mi'): self.existence_test_and_add('person_legal_middle_name_unhashed', self.row_dict.__getitem__('c4mi'), 'text')
        ''' convert ethnicity to code '''
        if self.row_dict.has_key('hispanic'):
            if self.row_dict.__getitem__('hispanic').upper() == 'N': ethnicity = "0"
            elif self.row_dict.__getitem__('hispanic').upper() == 'Y': ethnicity = "1"
            if ethnicity is not None:
                self.existence_test_and_add('person_ethnicity_unhashed', ethnicity, 'text')
        if self.row_dict.has_key('c4ssno'): self.existence_test_and_add('person_social_security_number_unhashed', self.row_dict.__getitem__('c4ssno').replace('-', ''), 'text')     
        self.shred(self.parse_dict, dbobjects.Person)
        ''' person index id is now in memory, go to the sub-table parsers '''
        self.parse_other_names()
        self.parse_races()
        self.parse_site_service_participation()
        self.parse_household()
        
    def parse_other_names(self):
        ''' parse data for other_names table '''
        self.parse_dict = {}
        ''' check if other last name is unique '''
        if self.row_dict.has_key('c4last_s01') & self.row_dict.has_key('c4lastname'):
            if self.row_dict.__getitem__('c4lastname').lower() != self.row_dict.__getitem__('c4last_s01').lower():
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                self.existence_test_and_add('other_last_name_unhashed', self.row_dict.__getitem__('c4last_s01'), 'text')     
                self.shred(self.parse_dict, dbobjects.OtherNames)

    def parse_races(self):
        ''' parse data for races table '''
        self.parse_dict = {}
        ''' convert race to code '''
        ''' JFCS uses ethnicity to define race '''
        if self.row_dict.has_key('ethnicity'):
            if self.row_dict.__getitem__('ethnicity').upper() == 'M': race = '5'
            elif self.row_dict.__getitem__('ethnicity').upper() == 'H': race = '5'
            elif self.row_dict.__getitem__('ethnicity').upper() == 'W': race = '5'
            elif self.row_dict.__getitem__('ethnicity').upper() == 'B': race = '3'
            if race is not None:
                self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
                self.existence_test_and_add('race_unhashed', race, 'text')
                self.shred(self.parse_dict, dbobjects.Races)
        
    def parse_site_service_participation(self):
        ''' parse data for site_service_participation table '''
        self.parse_dict = {}
        self.existence_test_and_add('person_index_id', self.person_index_id, 'no_handling')
        if self.row_dict.has_key('aprgcode'): self.existence_test_and_add('site_service_idid_num', self.row_dict.__getitem__('aprgcode'), 'text')
        if self.row_dict.has_key('a_date'):
            test = self.normalize_date(self.row_dict.__getitem__('a_date'))
            if test == True: self.existence_test_and_add('participation_dates_start_date', self.row_dict.__getitem__('a_date'), 'element_date')
        if self.row_dict.has_key('t_date'):
            test = self.normalize_date(self.row_dict.__getitem__('t_date'))
            if test == True: self.existence_test_and_add('participation_dates_end_date', self.row_dict.__getitem__('t_date'), 'element_date')                
        self.shred(self.parse_dict, dbobjects.SiteServiceParticipation)
        
    def parse_household(self):
        ''' parse data for household table '''
        self.parse_dict = {}
        if self.row_dict.has_key('family_id'):
            self.existence_test_and_add('household_id_num', self.row_dict.__getitem__('family_id'), 'text')
            self.shred(self.parse_dict, dbobjects.Household)
            ''' household index id is now in memory, go to the sub-table parsers '''
            self.parse_members()
        
    def parse_members(self):
        ''' parse data for members table '''
        self.parse_dict = {}
        self.existence_test_and_add('household_index_id', self.household_index_id, 'no_handling')
        if self.row_dict.has_key('c4clientid'): self.existence_test_and_add('person_id_unhashed', self.row_dict.__getitem__('c4clientid'), 'text')
        self.shred(self.parse_dict, dbobjects.Members)
        
    def shred(self, parse_dict, mapping):
        '''Commits the record set to the database'''
        mapped = mapping(parse_dict)
        self.session.add(mapped)
        self.session.commit()
        #Save the indexes generated at run-time so can be used
        #in dependent tables
        if mapping.__name__ == "Household":
            self.household_index_id = mapped.id
        if mapping.__name__ == "PersonHistorical":
            self.person_historical_index_id = mapped.id
        if mapping.__name__ == "Person":
            self.person_index_id = mapped.id
            self.site_service_index_id = None
        if mapping.__name__ == "SiteServiceParticipation":
            self.site_service_index_id = mapped.id
        self.session.commit()
        
    def existence_test_and_add(self, db_column, query_string, handling):
        '''checks that the query actually has a result and adds to dict'''
        #if len(query_string) is not 0:
        if handling == 'no_handling':
                self.persist(db_column, query_string = query_string)
                return True
        elif len(query_string) is not 0 or None:
            if handling == 'attribute_text':
                self.persist(db_column, query_string)
                return True
            if handling == 'text':
                self.persist(db_column, query_string)
                return True
            elif handling == 'attribute_date':
                self.persist(db_column, query_string = dateutil.parser.parse(query_string))
                return True
            elif handling == 'element_date':
                self.persist(db_column, query_string = dateutil.parser.parse(query_string))
                return True
            else:
                print "need to specify the handling"
                return False
        else:
            return False
    
    def persist(self, db_column, query_string):
        ''' build dictionary of db_column:data '''
        self.parse_dict.__setitem__(db_column, query_string)
        return
    
    def normalize_date(self, raw_date):
        if raw_date.replace(' ', '') == '--':
            return False
        elif raw_date.replace(' ', '') == '':
            return False
        else:
            return True
    
    def lookup_person(self):
        ''' lookup person_index_id from person table '''
        Persons = self.session.query(dbobjects.Person).filter(dbobjects.Person.person_id_unhashed == self.row_dict.__getitem__('c4clientid'))
        for self.person in Persons:
            self.person_index_id = self.person.id
            self.lookup_service()
        
    def lookup_service(self):
        ''' lookup service_index_id from site_service_participation table '''  
        Services = self.session.query(dbobjects.SiteServiceParticipation).filter(dbobjects.SiteServiceParticipation.person_index_id == self.person_index_id)
        for self.service in Services:
            self.service_index_id = self.service.id        
    
def main(argv=None):
    ''' Test the JFCSXMLReader class '''
    
    ''' Check if arguments manually passed to main '''
    if argv is None:
        argv = sys.argv

    ''' Select input file '''
    inputFile = "/mnt/laptop01/Projects/Alexandria/DATA/StagingFiles/CRG.xml"
    #inputFile = "/mnt/laptop01/Projects/Alexandria/DATA/StagingFiles/CRG.xml.pgp"
    #inputFile = "/mnt/laptop01/Projects/Alexandria/DATA/StagingFiles/PEO.xml"
    #inputFile = "/mnt/laptop01/Projects/Alexandria/DATA/StagingFiles/PEO.xml.pgp"
    
    ''' Set the data_type '''
    data_type = 'service'
    
    ''' Test for existance and ability to read input file '''
    if os.path.isfile(inputFile) is True:
        try:
            xml_file = open(inputFile, 'r')
        except:
            print "Error opening input file"
                
        ''' Process input file '''
        reader = JFCSXMLReader(xml_file)
        tree = reader.read()
        reader.process_data(tree, data_type)
        xml_file.close()
            
if __name__ == "__main__":
    sys.exit(main())
    