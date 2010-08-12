'''Figures out what type of data format we are dealing with, using validation \
or whatever we can use to test, so the appropriate reader correct \
implementation can be used.'''
import os
import fileUtils
import sys
from fileinputwatcher import FileInputWatcher
from hmisxml28reader import HMISXML28Reader
from hmisxml30reader import HMISXML30Reader
from jfcsxmlreader import JFCSXMLReader
from parxmlreader import PARXMLReader
from lxml import etree
import Queue
from conf import settings
from emailProcessor import XMLProcessorNotifier
from fileRouter import router
from os import path
from clsExceptions import DuplicateXMLDocumentError
import traceback
from clsSecurity import clsSecurity
import copy
from StringIO import StringIO
from clsSocketComm import serviceController



class FileHandler:#IGNORE:R0903
    '''Sets up the watch on the directory, and handles the file once one comes \
    in'''
    def __init__(self):
        #change this so that it gets the watch_dir from the .ini file
        dir_to_watch = settings.INPUTFILES_PATH #IGNORE:C0301
        self.queue = Queue.Queue(0)
        self.file_input_watcher = FileInputWatcher(dir_to_watch, self.queue, settings.DEBUG)
        global FU
        FU = fileUtils.fileUtilities()
        #Check the file to see if it validates against one of the tests.
        self.selector = Selector()
        self.crypto = clsSecurity()
	
	# SBB20100612 adding listener for data comm (win32 shutdown from GUI)
	sc = serviceController(True)					# True is Server
	sc.listen()

    def setProcessingOptions(self, docName):
        ''' ProcessingOptions is a dictionary on a perfile/sender basis.
        Dictionary contains settings like does the sender use encryption etc.
        self.ProcessingOptions = 
            {
                'SMTPTOADDRESS': ['joe@t3ch.com,],
                'SMTPTOADDRESSCC': [],
                'SMTPTOADDRESSBCC': [],
                'FINGERPRINT':'',
                'USES_ENCRYPTION':True
            }
        '''
        folderName = path.split(docName)[0]
        try:
            self.ProcessingOptions = settings.SMTPRECIPIENTS[folderName]
        except:
            raise
        
    def processFiles(self, new_file):
        self.setProcessingOptions(new_file)
        self.email = XMLProcessorNotifier(new_file)
        self.router = router()
        
        # test if the sender encrypts data, if so, decrypt, if not, just process
        
        print "crypto",self.ProcessingOptions['USES_ENCRYPTION']
        
        if self.ProcessingOptions['USES_ENCRYPTION']:
            # decrypt the file
            fileStream = self.crypto.decryptFile2Stream(new_file)
            print "stream",fileStream
        else:
            # just open the file
            fileStream = open(new_file,'r')
            # Work around bug? file object is not same as CstringIO object in that you can't copy a fileStream to another one, CStringIO you can.  So we conver this to a CStringIO object and we can make true copies.
            fileStream = StringIO(fileStream.read())
            
        try:
            if self.selector.validate(fileStream):
                self.email.notifyValidationSuccess()
                self.router.moveUsed(new_file)
                return True
            else:
                self.email.notifyValidationFailure()
                self.router.moveFailed(new_file)
                return False
        except etree.XMLSyntaxError, error:
            self.email.notifyValidationFailure(error)
            self.router.moveFailed(new_file)
            
        except DuplicateXMLDocumentError, inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly

            self.email.notifyDuplicateDocumentError(inst.message)
            self.router.moveFailed(new_file)
            return False
        
    def processExisting(self):
        ''' this function churns through the input path(s) and processes files that are already there.
        iNotify only fires events since program was started so existing files don't get processed
        '''
        # get a list of files in the input path
        listOfFiles = list()
        # Loop over list of file locations [list]
        for folder in settings.INPUTFILES_PATH:
            listOfFiles.extend(FU.grabFiles(path.join(folder,'*.xml')))
            for inputFile in listOfFiles:
                self.processFiles(inputFile)
    
    def runWindows(self):
        import os, time
        BASE_PATH = os.getcwd()
        path_to_watch = os.path.join(BASE_PATH, "InputFiles")
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        try:
            while 1:
                time.sleep (10)
                after = dict ([(f, None) for f in os.listdir (path_to_watch)])
                added = [f for f in after if not f in before]
                removed = [f for f in before if not f in after]
                if added:
                    print "Added: ", ", ".join (added)
                    self.processExisting()
                if removed:
                    print "Removed: ", ", ".join (removed)
                before = after
        except KeyboardInterrupt:
            return
                
    def run(self): #IGNORE:R0201
        '''This is the main method controlling this entire program.'''
        #Start a monitoring thread.  It ends on its own.
        new_files = self.monitor()
        print 'monitoring..'
        print 'monitoring..2'
    
        #result = selector.validate(HUDHMIS28XMLTest(), new_file)
        for new_file in new_files:
            if settings.DEBUG:
                print 'Processing: %s' % new_file
        
            self.processFiles(new_file)
            
    #ECJ 05042009 indented this block as it needs specific class attributes \n
    #to work        
    def monitor(self):
        'function to start and stop the monitor' 
        self.file_input_watcher.monitor()
        print 'waiting..'
        print 'waiting 2'
        
        #now make a file whilst pyinotify thread is running need to keep pulling from the queue (set to timeout after 5 seconds: subsequent passes)
        files = list()
        _QTO = None
        while 1:
            try:
                result = self.queue.get(block='true', timeout=_QTO)
                if settings.DEBUG:
                    print 'found file: %s' % result
                _QTO = 5
            except Queue.Empty:
                result = None
                break
            
            # append all files into the file stack to be processed.
            if result != None:
                files.append(result)
        
        self.file_input_watcher.stop_monitoring()
        #return result
        return files
        
class Selector:
    '''Figures out which data format is being received.'''
    
    def __init__(self):
        
        local_schema = settings.SCHEMA_DOCS
        if settings.DEBUG:
            for item in local_schema:
                print 'found schema: ' + local_schema[item]
        
        global FU
        FU = fileUtils.fileUtilities()

    def validate(self, instance_doc, shred=True): 
        '''Validates against the various available schema and csv records.\
        If not specified in the configs, it keeps trying each available \
        test to find the first which successfully validates.  You just \
        pass it a test, and the xml instance data.'''
        #check if config specifies which schema should be used for this install
        #config_available = 'false'
        #output the results (which schema it did or did not validate against
        #if had a config specified
        FILEHANDLER = FileHandler()
        
        tests = [HUDHMIS28XMLTest(), HUDHMIS30XMLTest(), JFCSXMLTest(), PARXMLTest()]
        readers = [HUDHMIS28XMLReader(instance_doc), HUDHMIS30XMLReader(instance_doc), JFCSXMLInputReader(instance_doc), PARXMLInputReader(instance_doc)]
        results = []
        #for item in tests:
        for item,read in map(None, tests, readers):
            result = item.validate(instance_doc)
            # if results is True, we can process against this reader.
            if result and shred:
                read.shred()
                
            results.append(result) 
            print item, result
        print results
        #print 'This is the result before it goes back to the test_unit:', \
        #results
        return results

class VendorXMLTest:#IGNORE:R0903
    '''Stub for any specific vendor's non-standardized XML format.'''
    def __init__(self):
        self.name = 'Vendor XML'
        print 'running the', self.name, 'test'
        
    def validate(self, instance_filename):
        '''implementation of interface's validate method'''
        print '\nThe', self.name, 'test not implemented.'
        print '...but intended to validate', instance_filename
        return False
    
class HUDHMIS28XMLTest:
    '''Load in the HUD HMIS Schema, version 2.8.'''
    def __init__(self):
        global name
        name = 'HUDHMIS28XML'
        print 'running the', name, 'test'
        self.schema_filename = Selector.local_schema['hud_hmis_2_8_xml']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        copy_instance_stream = copy.copy(instance_stream)
        
        
        
        try:
            instance_parsed = etree.parse(copy_instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                #print 'The HMIS 2.8 XML successfully validated.'
                FU.makeBlock('The HMIS 2.8 XML successfully validated.')
                return results
            if results == False:
                print 'The xml did not successfully validate against \
                HMIS 2.8 XML.'
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  '\
            , error
            raise 

class HUDHMIS30XMLTest:
    '''Load in the HUD HMIS Schema, version 3.0.'''
    def __init__(self):
        global name
        name = 'HUDHMIS30XML'
        print 'running the', name, 'test'
        self.schema_filename = Selector.local_schema['hud_hmis_3_0_xml']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        # make a copy of the stream, validate against the copy not the real stream
        copy_instance_stream = copy.copy(instance_stream)

        try:
            instance_parsed = etree.parse(copy_instance_stream)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                print 'The HMIS 3.0 XML successfully validated.'
                FU.makeBlock('The HMIS 3.0 XML successfully validated.')
                return results
            if results == False:
                print 'The xml did not successfully validate against \
                HMIS 3.0 XML.'
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  '\
            , error
            raise

class SVCPOINTXMLTest:
    '''Load in the SVCPoint Schema, version 2.0.'''
    def __init__(self):
        global name
        self.name = 'SVCPOINT_%s_XML' % settings.SERVICEPOINT_VERSION
        print 'running the', self.name, 'test'
        self.schema_filename = Selector.local_schema['svcpoint_2_0_xml']
    
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
                #print 'The HMIS 2.8 XML successfully validated.'
                FU.makeBlock('The %s successfully validated.' % self.name)
                return results
            if results == False:
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  '\
            , error
            raise 

    
class JFCSXMLTest:
    ''' Tests for JFCS data 
        * There are 2 possible data source types ('service' or 'client')
        Steps: (will stop and return True on first success)
            1 - Attempt to validate against 'service' schema: 'JFCS_service.xsd'
            2 - Attempt to validate against 'client' schema: 'JFCS_client.xsd'
            3 - Check for known 'service' elements anywhere in the tree
            4 - Check for known 'client' elements anywhere in the tree
    '''
    
    def __init__(self):
        self.name = 'JFCS'
        print 'running the', self.name, 'test'
        
        ''' Define schemas and elements for testing '''
        self.service_schema_filename = Selector.local_schema['jfcs_service_xml']
        self.client_schema_filename = Selector.local_schema['jfcs_client_xml']
        self.service_elements = ['c4clientid','qprogram','serv_code','trdate','end_date','cunits']
        self.client_elements = ['aprgcode','a_date','t_date','family_id','c4clientid','c4dob','hispanic','c4sex','c4firstname','c4lastname','c4mi','ethnicity','c4ssno','c4last_s01']
        
    def validate(self, instance_filename, ):
        '''JCFS data format validation process'''
        
        copy_instance_stream = copy.copy(instance_filename)
        
        results = self.schemaTest(copy_instance_stream, self.service_schema_filename)
        if results == True:
            FU.makeBlock('JFCS service XML data found.  Determined by service schema.')
            JFCSXMLInputReader.data_type = 'service'
            return results
        
        results = self.schemaTest(copy_instance_stream, self.client_schema_filename)
        if results == True:
            FU.makeBlock('JFCS client XML data found.  Determined by client schema.')
            JFCSXMLInputReader.data_type = 'client'
            return results

        results = self.elementTest(copy_instance_stream, self.service_elements)
        if results == True:
            FU.makeBlock('JFCS service XML data found.  Determined by service elements.')
            JFCSXMLInputReader.data_type = 'service'
            return results
        
        results = self.elementTest(copy_instance_stream, self.client_elements)
        if results == True:
            FU.makeBlock('JFCS client XML data found.  Determined by client elements.')
            JFCSXMLInputReader.data_type = 'client'
            return results  
        
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
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.    '\
            , error
            raise
        return False
        
    def elementTest(self, copy_instance_stream, elements):
        '''Attempt to find elements in the input file by searching the tree'''
        xml_doc = etree.parse(copy_instance_stream)
        for e in elements:
            search_term = ".//" + e
            if xml_doc.find(search_term) is None:
                return False
        return True
    
class PARXMLTest:
    '''Load in the HUD HMIS Extended Schema for Operation PAR'''
    def __init__(self):
        global name
        name = 'PARXML'
        print 'running the', name, 'test'
        self.schema_filename = Selector.local_schema['operation_par_xml']

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
                schema_hudhmis_filename = Selector.local_schema['hud_hmis_2_8_xml']
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
                            print 'XML Error.  Value %s exceeds database field length.' % str(e.tag)
                            return False    ## remove this when testing and perform manual truncate in PARXMLReader()
                
                #return False ## return invalid, use this to only test validation of string lengths and exit                        
                
                FU.makeBlock('The Operation PAR XML successfully validated.')
                return results
            if results == False:
                print 'The xml did not successfully validate against \
                Operation PAR XML.'
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  '\
            , error
            raise 
    
class HUDHMIS28XMLReader(HMISXML28Reader):
    def __init__(self, instance_filename):
        self.reader = HMISXML28Reader(instance_filename)
        
    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree)
        except:
            raise

class HUDHMIS30XMLReader(HMISXML30Reader):
    def __init__(self, instance_filename):
        self.reader = HMISXML30Reader(instance_filename)
        
    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree)
        except:
            raise

class JFCSXMLInputReader(JFCSXMLReader):
    def __init__(self, instance_filename):
        self.reader = JFCSXMLReader(instance_filename)
        
    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree, self.data_type)
        except:
            raise

class PARXMLInputReader(PARXMLReader):
    def __init__(self, instance_filename):
        self.reader = PARXMLReader(instance_filename)
        
    def shred(self):
        tree = self.reader.read()
        try:
            self.reader.process_data(tree)
        except:
            raise
    
class VendorXMLReader():
    def __init__(self, instance_doc):
        pass

    def shred(self):
        '''implementation of interface's shred method'''
        print '\nThe', self.name, 'test not implemented.'
        print '...but intended to shred the XML Document: %s' % instance_filename
        return False
    
if __name__ == '__main__':
        
    if settings.DEBUG and settings.MODE == 'TEST':                              # Only reset the DB in Test mode
        import postgresutils
        UTILS = postgresutils.Utils()
        UTILS.blank_database()
     
    
    FILEHANDLER = FileHandler()
    RESULTS = FILEHANDLER.run()