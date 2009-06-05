'''Figures out what type of data format we are dealing with, using validation \
or whatever we can use to test, so the appropriate reader correct \
implementation can be used.'''
from fileinputwatcher import FileInputWatcher
from lxml import etree
import Queue

class FileHandler:#IGNORE:R0903
    '''Sets up the watch on the directory, and handles the file once one comes \
	in'''
    def __init__(self):
        #change this so that it gets the watch_dir from the .ini file
        dir_to_watch = '/home/eric/Alexandria_Consulting/Suncoast/JFCS/input_xml' #IGNORE:C0301
        self.queue = Queue.Queue(0)
        self.file_input_watcher = FileInputWatcher(dir_to_watch, self.queue)
        
    def run(self): #IGNORE:R0201
        '''This is the main method controlling this entire program.'''
        #Start a monitoring thread.  It ends on its own.
        new_file = self.monitor()
        #Check the file to see if it validates against one of the tests.
        selector = Selector()
        #result = selector.validate(HUDHMIS28XMLTest(), new_file)
        selector.validate(new_file)
    #ECJ 05042009 indented this block as it needs specific class attributes \n
    #to work        
    def monitor(self):
        'function to start and stop the monitor' 
        self.file_input_watcher.monitor()
        #now make a file whilst pyinotify thread is running
        try:
            result = self.queue.get(block='true')
        except Queue.Empty:
            result = None
        self.file_input_watcher.stop_monitoring()
        return result        
        
class Selector:#IGNORE:R0903
    '''Figures out which data format is being received.'''
    local_schema = {'hud_hmis_2_8_xml':'/home/eric/Alexandria_Consulting/Suncoast/JFCS/src/hmisparse/schema/HUD_HMIS_2_8.xsd'} #IGNORE:C0301
    def __init__(self):
        #need to put this attribute in the .ini file
        pass
    
    def validate(self, instance_doc): #IGNORE:R0201
        '''Validates against the various available schema and csv records.\
        If not specified in the configs, it keeps trying each available \
        test to find the first which successfully validates.  You just \
        pass it a test, and the xml instance data.'''
        #check if config specifies which schema should be used for this install
        #config_available = 'false'
        #output the results (which schema it did or did not validate against
        #if had a config specified
        tests = [VendorXMLTest(), HUDHMIS28XMLTest(), JFCSXMLTest()]
        results = []
        for item in tests:
            result = item.validate(instance_doc)
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
    
      
class HUDHMIS28XMLTest:#IGNORE:R0903
    '''Load in the HUD HMIS Schema, version 2.8.'''
    def __init__(self):
        global name
        name = 'HUDHMIS28XML'
        print 'running the', name, 'test'
        self.schema_filename = Selector.local_schema['hud_hmis_2_8_xml']

        
    def validate(self, instance_filename):
        '''This specific data format's validation process.'''
        schema = open(self.schema_filename,'r')
        instance = open(instance_filename,'r')
        schema_parsed = etree.parse(schema)
        schema_parsed_xsd = etree.XMLSchema(schema_parsed)
        try:
            instance_parsed = etree.parse(instance)
            results = schema_parsed_xsd.validate(instance_parsed)
            if results == True:
                print 'The HMIS 2.8 XML successfully validated.'
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
            return
            
class JFCSXMLTest:#IGNORE:R0903,W0232
    '''A stub for a specific non-profit's supplied non-standard XML format.'''
    def __init__(self):
        self.name = 'JFCS'
        print 'running the', self.name, 'test'
        
    def validate(self, instance_filename):
        '''implementation of interface's validate method'''
        print '\nThe', self.name, 'test not implemented.'
        print '...but intended to validate', instance_filename
        return False
    
if __name__ == '__main__':
    FILEHANDLER = FileHandler()
    RESULTS = FILEHANDLER.run()