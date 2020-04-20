'''Document validation tests used by the selector module and the nodebuilder module.'''
from lxml import etree
from .conf import settings
from . import fileutils

class VendorXMLTest:
    '''Stub for any specific vendor's non-standardized XML format.'''
    def __init__(self):
        self.name = 'Vendor XML'
        print('running the', self.name, 'test')
        
    def validate(self, instance_filename):
        '''implementation of interface's validate method'''
        print('\nThe', self.name, 'test not implemented.')
        print('...but intended to validate', instance_filename)
        return False

class TBCExtendHUDHMISXMLTest:	# JCS New 2012-01-05
    '''Load in the HUD HMIS Schema, version 3.0.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'TBCExtendHUDHMISXML'
        print('running the', self.name, 'test')
        self.schema_filename = settings.SCHEMA_DOCS['tbc_extend_hud_hmis_xml']
        print("settings.SCHEMA_DOCS['tbc_extend_hud_hmis_xml'] is: ", settings.SCHEMA_DOCS['tbc_extend_hud_hmis_xml'])
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  ', error)
            pass

class HUDHMIS28XMLTest:
    '''Load in the HUD HMIS Schema, version 2.8.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'HUDHMIS28XML'
        print('running the', self.name, 'test')
        self.schema_filename = settings.SCHEMA_DOCS['hud_hmis_xml_2_8']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        #copy_instance_stream = copy.copy(instance_stream)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  ', error)
            pass   

class HUDHMIS30XMLTest:
    '''Load in the HUD HMIS Schema, version 3.0.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'HUDHMIS30XML'
        print('running the', self.name, 'test')
        self.schema_filename = settings.SCHEMA_DOCS['hud_hmis_xml_3_0']
        print("settings.SCHEMA_DOCS['hud_hmis_xml_3_0'] is: ", settings.SCHEMA_DOCS['hud_hmis_xml_3_0'])
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        #copy_instance_stream = copy.copy(instance_stream)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  ', error)
            pass


class OCCHUDHMIS30XMLTest:
    '''Load in the HUD HMIS Schema, version 3.0.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'OCCHUDHMIS30XML'
        print('running the', self.name, 'test')
        self.schema_filename = settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0']
        print("settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0'] is: ", settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0'])
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        try:
            schema = open(self.schema_filename,'r')
        except:
            print("couldn't open schema file", self.schema_filename)
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        #copy_instance_stream = copy.copy(instance_stream)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  ', error)
            pass
        
class SvcPoint20XMLTest:
    '''Load in the SVCPoint Schema, version 2.0.'''
    def __init__(self):
        self.name = 'Svcpt 2.0 XML'
        print('running the Svcpt 2.0 XML test')
        self.schema_filename = settings.SCHEMA_DOCS['svcpoint_2_0_xml']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        #copy_instance_stream = copy.copy(instance_stream)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  '\
            , error)
            raise 

class SvcPoint406XMLTest:
    '''Load in the SVCPoint Schema, version 4.06'''
    def __init__(self):
        self.name = 'Svc406 XML'
        print('running the Svcpt 4.06 XML test')
        self.schema_filename = settings.SCHEMA_DOCS['svcpoint_4_0_6_xml']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        #copy_instance_stream = copy.copy(instance_stream)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  '\
            , error)
            raise

class SvcPoint5XMLTest:
    '''Load in the SVCPoint Schema, version 5.00'''
    def __init__(self):
        self.name = 'Svc5 XML'
        print('running the Svcpt 5.00 XML test')
        self.schema_filename = settings.SCHEMA_DOCS['svcpoint_5_xml']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        #copy_instance_stream = copy.copy(instance_stream)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                    was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  ', error)
            raise

class hl7CCDXMLTest:
    '''Load in the HL7 CCD Schema'''
    def __init__(self):
        self.name = 'hl7 CCD XML'
        print('running the hl7 CCD XML test')
        self.schema_filename = settings.SCHEMA_DOCS['hl7_ccd_xml']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        
        try:
            instance_parsed = etree.parse(instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                fileutils.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print('The xml did not successfully validate against %s' % self.name)
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                    was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  ', error)
            raise

class JFCSXMLTest:
    ''' Tests for JFCS data 
        * There are 2 possible data source types ('service_event' or 'client')
        Steps: (will stop and return True on first success)
            1 - Attempt to validate against 'service_event' schema: 'JFCS_SERVICE.xsd'
            2 - Attempt to validate against 'client' schema: 'JFCS_CLIENT.xsd'
            3 - Check for known 'service_event' elements anywhere in the tree
            4 - Check for known 'client' elements anywhere in the tree
    '''
    
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'JFCS'
        print('running the', self.name, 'test')
        
        ''' Define schemas and elements for testing '''
        self.service_event_schema_filename = settings.SCHEMA_DOCS['jfcs_service_event_xml']
        self.client_schema_filename = settings.SCHEMA_DOCS['jfcs_client_xml']
        self.service_event_elements = ['c4clientid','qprogram','serv_code','trdate','end_date','cunits']
        #self.client_elements = ['aprgcode','a_date','t_date','family_id','c4clientid','c4dob','hispanic','c4sex','c4firstname','c4lastname','c4mi','ethnicity','c4ssno','c4last_s01']
        self.client_elements = ['aprgcode','a_date','t_date','family_id','c4clientid','c4dob','hispanic','c4sex','c4firstname','c4lastname','c4mi','ethnicity','c4ssno']

        
    def validate(self, instance_filename, ):
        '''JFCS data format validation process'''
        
        copy_instance_stream = copy.copy(instance_filename)
       
        try: 
            print("Determining by service event schema")
            results = self.schemaTest(copy_instance_stream, self.service_event_schema_filename)
            if results == True:
                fileutils.makeBlock('JFCS service event XML data found.  Determined by service event schema.')
                JFCSXMLInputReader.data_type = 'service_event'
                return results
            print("Determining by client schema")
            results = self.schemaTest(copy_instance_stream, self.client_schema_filename)
            if results == True:
                fileutils.makeBlock('JFCS client XML data found.  Determined by client schema.')
                JFCSXMLInputReader.data_type = 'client'
                return results
            print("Determining by service event elements.")
            if self.service_event_elements is not None:
                print(self.service_event_elements)
                results = self.elementTest(copy_instance_stream, self.service_event_elements)
                if results == True:
                    fileutils.makeBlock('JFCS service event XML data found.  Determined by service event elements.')
                    JFCSXMLInputReader.data_type = 'service_event'
                    return results
            print("Determining by client elements.")
            if self.client_elements is not None:
                print(self.client_elements)
                results = self.elementTest(copy_instance_stream, self.client_elements)
                if results == True:
                    fileutils.makeBlock('JFCS client XML data found.  Determined by client elements.')
                    JFCSXMLInputReader.data_type = 'client'
                    return results
                print("returning False")
                return False
            else:
                print("All the JFCS Tests Failed, returning False")
                self.issues = "All the JFCS Tests Failed, returning False"
                return False
        except Exception as exception:
            print('XML Syntax Error in validate.  There appears to be malformed XML.  ', exception)
            self.issues = 'XML Syntax Error in validate.  There appears to be malformed XML.  %s' % str(exception)
            return False
    
    def schemaTest(self, copy_instance_stream, schema_filename):
        '''Attempt to validate input file against specific schema'''
        schema = open(schema_filename,'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(copy_instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error in schemaTest.  There appears to be malformed XML.  ', error)
            return False
        
    def elementTest(self, copy_instance_stream, elements):
        '''Attempt to find elements in the input file by searching the tree'''
        print("inside element test")
        print("elements are: ", elements)
        xml_doc = etree.parse(copy_instance_stream)
        for e in elements:
            search_term = ".//" + e
            if xml_doc.find(search_term) is None:
                print("returning False from inside elementTest")
                return False
        print("returning True  from inside elementTest")
        return True
    
class PARXMLTest:
    '''Load in the HUD HMIS Extended Schema for Operation PAR'''
    def __init__(self):
        self.name = 'PARXML'
        print('running the', self.name, 'test')
        self.schema_filename = settings.SCHEMA_DOCS['operation_par_xml']

    '''Find elements with or without specific xsd type'''
    def find_elements_by_type(self, schema_doc, type_content):
        element_names = schema_doc.xpath("//xsd:element[@type != $n]/@name", namespaces={"xsd":"http://www.w3.org/2001/XMLSchema", 'ext':'http://xsd.alexandriaconsulting.com/cgi-bin/trac.cgi/export/344/trunk/synthesis/xsd/Operation_PAR_Extend_HUD_HMIS_2_8.xsd', 'hmis':'http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd'},n=type_content)
        return element_names
    
    def validate(self, instance_stream):
        
        #return True  ## use this to skip the validation test
        #return False ## use this to fail validation test
        
        '''This specific data format's validation process.'''

        '''Import schema for Operation PARS'''
        schema = open(self.schema_filename,'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        
        ## if schema fails to compile, catch exception here (except Exception, e: print e.error_log)
        
        # make a copy of the file stream, validate against the copy not the real stream
        copy_instance_stream = copy.copy(instance_stream)
        xml_doc = etree.parse(copy_instance_stream)
        
        ''' 
            Explicit check for 'ext' namespace since HUD_HMIS_2.8 xml
            validates against the extended Operation PAR schema
        '''
        ext_namespace_check = xml_doc.xpath('/ext:SourceDatabase', namespaces={'ext': 'http://xsd.alexandriaconsulting.com/cgi-bin/trac.cgi/export/344/trunk/synthesis/xsd/Operation_PAR_Extend_HUD_HMIS_2_8.xsd'})
        if len(ext_namespace_check) != 1: return False
        
        try:
            instance_parsed = etree.parse(copy_instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                ''' 
                    Elements that do not have the maxLength attribute
                    in schema must be checked to ensure string length
                    conforms to database field.  Lengths exceeding 32
                    characters will cause the xml to be deemed invalid.
                    This adds extra weight to this process and should
                    be removed if maxLength is implemented for all 
                    elements in the schema.
                '''
                
                '''import original HUD HMIS 2.8 xsd that Operation PARS extended'''
                schema_hudhmis_filename = settings.SCHEMA_DOCS['hud_hmis_2_8_xml']
                schema_hudhmis_raw = open(schema_hudhmis_filename,'r')
                schema_hudhmis_parsed = etree.parse(schema_hudhmis_raw)
                
                '''get lists of elements with maxLength attribute greater than 32'''
                elements_string50 = self.find_elements_by_type(schema_parsed, 'hmis:string50')
                elements_string50_ns = []
                for e in elements_string50:
                    elem_with_ns = '{http://xsd.alexandriaconsulting.com/cgi-bin/trac.cgi/export/344/trunk/synthesis/xsd/Operation_PAR_Extend_HUD_HMIS_2_8.xsd}' + e
                    elements_string50_ns.append(elem_with_ns)
                elements_string50 = self.find_elements_by_type(schema_hudhmis_parsed, 'hmis:string50')
                for e in elements_string50:
                    elem_with_ns = '{http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd}' + e
                    elements_string50_ns.append(elem_with_ns)

                '''combine lists if your looking for multiple types'''
                elements_maxlength = elements_string50_ns

                '''find elements without specific attribute and check length'''
                xml_root = xml_doc.getroot()
                for e in xml_root.iter():
                    if str(e.tag) in elements_maxlength:
                        if len(e.text) > 32:
                            print('XML Error.  Value %s exceeds database field length.' % str(e.tag))
                            return False    ## remove this when testing and perform manual truncate in PARXMLReader()
                
                #return False ## return invalid, use this to only test validation of string lengths and exit                        
                
                fileutils.makeBlock('The Operation PAR XML successfully validated.')
                return results
            if results == False:
                print('The xml did not successfully validate against \
                Operation PAR XML.')
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print(detailed_results)
                    return results
                except etree.DocumentInvalid as error:
                    print('Document Invalid Exception.  Here is the detail:')
                    print(error)
                    return results
            if results == None:
                print("The validator erred and couldn't determine if the xml \
                was either valid or invalid.")
                return results
        except etree.XMLSyntaxError as error:
            print('XML Syntax Error.  There appears to be malformed XML.  '\
            , error)
            raise 
        
#The MIT License
#
#Copyright (c) 2011, Alexandria Consulting LLC
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
