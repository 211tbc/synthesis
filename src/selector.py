'''Figures out what type of data format we are dealing with, using validation \                                                                                                                             
or whatever we can use to test, so the appropriate reader can be used.'''

import os
import fileutils
import sys
import time
from fileinputwatcher import FileInputWatcher
from hmisxml28reader import HMISXML28Reader
from hmisxml30reader import HMISXML30Reader
from tbchmisxml30reader import TBCHUDHMISXML30Reader	# JCS New 2012-01-05
from jfcsxmlreader import JFCSXMLReader
from occhmisxml30reader import OCCHUDHMISXML30Reader
#from synthesis.parxmlreader import PARXMLReader
from lxml import etree
import Queue
from conf import settings
from conf import inputConfiguration, outputConfiguration
from synthesis.emailprocessor import XMLProcessorNotifier
from filerouter import Router
from os import path
import traceback
import copy
from synthesis.socketcomm import ServiceController
import dbobjects
import threading
from multiprocessing import Array, Value
from smtplibrary import smtpInterface
from nodebuilder import NodeBuilder
from synthesis.queryobject import QueryObject
from selector_tests import HUDHMIS30XMLTest, HUDHMIS28XMLTest, OCCHUDHMIS30XMLTest, JFCSXMLTest, TBCExtendHUDHMISXMLTest
import socket
timeout = 30
socket.setdefaulttimeout(timeout)

class FileHandler:
    '''Sets up the watch on the directory, and handles the file once one comes in'''
    
    def __init__(self):
        # define thread list in shared memory so each thread can alter it
        self.thread_list = Array('i', [0 for i in range(0, settings.NUMBER_OF_THREADS)])
        self.exception = Value('i', 0)

        #change this so that it gets the watch_dir from the .ini file
        dir_to_watch = inputConfiguration.INPUTFILES_PATH 
        self.queue = Queue.Queue(0)
        self.file_input_watcher = FileInputWatcher(dir_to_watch, self.queue)
        #Check the file to see if it validates against one of the tests.
        self.selector = Selector()
        #ECJ20100815 Commented out for now until debugged 
        #self.crypto = Security()
       
        if settings.GUI:
            if settings.DEBUG:
                print "Now running the GUI ServiceController code"
                #ECJ 20100815 todo: make it so this also works for UNIX, not just win32
                # SBB20100612 adding listener for data comm (win32 shutdown from GUI)
                sc = ServiceController(True)                    # True is Server
                sc.listen()
        #If GUI to control the app being used, just run code with pyinotify or windows listener
        #ECJ 20100815 Make sure windows listener is working without the GUI
        else:
            if settings.DEBUG:
                print "Now running FileHandler.nonGUIRun()"
            self.nonGUIRun()
            print "returned to FileHandler.__init__ from nonGUIRun"
            print "calling sys.exit"
            sys.exit()

    def setProcessingOptions(self, docName):
        ''' ProcessingOptions is a dictionary on a per file/sender basis.
        Dictionary contains settings like does the sender use encryption etc.
        self.ProcessingOptions = 
            {
                'SMTPTOADDRESS': ['someone@domain.com,],
                'SMTPTOADDRESSCC': [],
                'SMTPTOADDRESSBCC': [],
                'FINGERPRINT':'',
                'USES_ENCRYPTION':True
            }
        '''
        folderName = path.split(docName)[0]
        if settings.DEBUG:
            print "folder name to email is", folderName
        if os.path.isdir(folderName): 
            try:
                self.ProcessingOptions = inputConfiguration.SMTPRECIPIENTS[folderName]
            except:
                raise
        else:
            print "folder", folderName, "is not a directory"
        
    def processFiles(self, new_file_loc):
        self.setProcessingOptions(new_file_loc)
        self.email = XMLProcessorNotifier(new_file_loc)
        self.Router = Router()
        valid = False
        # test if the sender encrypts data, if so, decrypt, if not, just process
        
        print "The settings indicate that, for this folder, encryption is:",self.ProcessingOptions['USES_ENCRYPTION']
        
        if self.ProcessingOptions['USES_ENCRYPTION']:
            # decrypt the file
            fileStream = self.crypto.decryptFile2Stream(new_file_loc)
            print "stream",fileStream
        else:
            if settings.DEBUG:
                print "No encryption, so just opening the file", new_file_loc
            # Work around bug? file object is not same as CstringIO object in that you can't copy a fileStream to another one, CStringIO you can.  So we convert this to a CStringIO object and we can make true copies.
            #fileStream = StringIO(fileStream.read())
            
        if settings.DEBUG:
            print "attempting validation tests on", new_file_loc
            #print "os.path.isfile(new_file_loc) is ", os.path.isfile(new_file_loc)
        if os.path.isfile(new_file_loc):
            results = self.selector.validate(new_file_loc)
            for item in results:
                if item == True:
                    valid = True
                    try:
                        self.email.notifyValidationSuccess()
                    except:
                        print traceback.print_exc(file=sys.stdout)
                        pass
                    if settings.DEBUG:
                        print "moving to used_files", 
                    new_file_name = self.Router.moveUsed(new_file_loc)
#                    break
                    return (True, new_file_name)
            
        if valid == False:
            if settings.DEBUG:
                print "We did not have any successful validations"
            self.email.notifyValidationFailure()
            if settings.DEBUG:
                print "moving to Failed"
            if os.path.isfile(new_file_loc):
                new_file_name = self.Router.moveFailed(new_file_loc)
            else:
                if settings.DEBUG:
                    print "Can't move because file doesn't exist.  Shouldn't be trying to move anything to Failed if isn't there."
            return (False, None)
            
#        except etree.XMLSyntaxError, error:
#            self.email.notifyValidationFailure(error)
#            self.Router.moveFailed(new_file_loc)
#            
#        except DuplicateXMLDocumentError, inst:
#            print type(inst)     # the exception instance
#            print inst.args      # arguments stored in .args
#            print inst           # __str__ allows args to printed directly
#
#            self.email.notifyDuplicateDocumentError(inst.message)
#            self.Router.moveFailed(new_file_loc)
#            return False
        
    def processExisting(self):
        ''' this function churns through the input path(s) and processes files that are already there.
        iNotify only fires events since program was started so existing files don't get processed
        '''
        import loadconfiguration
        if settings.DEBUG:
            print "loading data from defined in the loadconfigation module"
        loadconfiguration.loadData()

        # get a list of files in the input path
        listOfFiles = list()
        # Loop over list of file locations [list]
        for folder in inputConfiguration.INPUTFILES_PATH:
            listOfFiles.extend(fileutils.grabFiles(path.join(folder,'*')))
            if settings.DEBUG:
                print "list of files grabbed in processExisting is", listOfFiles
            for inputFile in listOfFiles:
                successful, processed_file = self.processFiles(inputFile)
                if successful:
                    # Send processed files to the processed files folder:
                    if settings.DEBUG:
                        print 'Made it this far so send used files to the processed files folder.'
                    print 'Copying ' + inputConfiguration.USEDFILES_PATH + '/' + processed_file + ' to ' + outputConfiguration.PROCESSEDFILES_PATH + '/' + processed_file
                    fileutils.copyFile(inputConfiguration.USEDFILES_PATH + '/' + processed_file, outputConfiguration.PROCESSEDFILES_PATH  + '/' +  processed_file)

        # *******************************
        # transfer control to nodebuilder
        # *******************************

        # first, setup options for nodebuilder
        optParse = QueryObject(suppress_usage_message=True)

        for paired_id in self.selector.paired_ids:
            source_id = paired_id[0]
            export_id = paired_id[1]
            if settings.DEBUG:
                print "nodebuilder generating output for source id:", source_id
            # next call nodebuilder for each source id
            # options are: ['startDate', 'endDate', 'alldates', 'reported', 'unreported', 'configID']
            (options, args) = optParse.parser.parse_args(['-a', '-u', '-i%s' % source_id])
            try:
                NODEBUILDER = NodeBuilder(options, export_id=export_id)
            except:
                print "*****************************************************************"
                print "*****************************************************************"
                print "*****************************************************************"
                synthesis_error = traceback.format_exc()
                print synthesis_error
                smtp = smtpInterface(settings)
                smtp.setMessageSubject("ERROR -- Synthesis:FileHandler:processExisting")
                smtp.setRecipients(inputConfiguration.SMTPRECIPIENTS['testSource'])
                smtp.setMessage("%s\r\n" % synthesis_error )
                try:
                    print "trying to send message"
                    smtp.sendMessage()
                except:
                    print 'send failed'                
                print "*****************************************************************"
                print "*****************************************************************"
                print "*****************************************************************"
            RESULTS = NODEBUILDER.run()
        # empty list of paired ids
        self.selector.paired_ids = list()
    
    def nonGUIPOSIXRun(self):
        #First, see if there are any existing files and process them
        if settings.DEBUG:
            print "First, looking for preexisting files in input location."
        self.processExisting()
        
        # This will wait until files arrive, once processed, it will loop and start over (unless we get ctrl-C or break)
        if settings.DEBUG:
            print 'monitoring starting ...'
        new_files = self.monitor() 
        
        if settings.DEBUG:
            print 'monitoring done ...'
            print 'new_files is', new_files
        if not new_files:
            print "No new files, returning"
            return
        
        for new_file in new_files:
            if settings.DEBUG:
                print 'Processing: %s' % new_file
            self.processFiles(new_file)
    
    def nonGUIWindowsRun(self):
        BASE_PATH = os.getcwd()
        path_to_watch = os.path.join(BASE_PATH, "InputFiles")
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        try:
            while 1:
                time.sleep(10)
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
                
    def nonGUIRun(self): 
        '''looks for and handles files, if there is no gui controlling the daemon, as specified by the GUI option in settings.py.'''
        #Figure out if we are running POSIX or UNIX non-gui
        if os.name == 'nt':
            if settings.DEBUG:
                print "We have a Windows system, as determined by nonGUIRun.  So handing off to nonGUIWindowsRun()"
            self.nonGUIWindowsRun()
        else:
            if settings.DEBUG:
                print "We have a POSIX system, as determined by nonGUIRun().  So handing off to nonGUIPOSIXRun()"
            self.nonGUIPOSIXRun()  
            print "back to nonGUIRun, so returning" 

    def monitor(self):
        'function to start and stop the monitor' 
        try:
            self.file_input_watcher.monitor()
            if settings.DEBUG:
                print "waiting for new input..."
                #print "result of fileinputwatcher.monitor passed back up to selector.monitor is", result
            #now make a file whilst pyinotify thread is running need to keep pulling from the queue (set to timeout after 5 seconds: subsequent passes)
            #In other words, the Queue fills up while pyinotify is working.  This empties the Queue, without stopping its function
            
            files = list()
            processed_files = list()
            _QTO = 5
#            if settings.DEBUG:    
#                wait_counter = 0
            while 1:
                # if an exception was encountered within a spawned thread, wait for all spawned
                # threads to stop then exit
                if self.exception.value == 1:
                    while self.thread_list[:].count(1) > 0:
                        pass
                    sys.exit(1)
                #Queue emptying while loop, this always runs until Ctrl+C is called.  If it ever stops, the found files get collected, but go nowhere
#                if settings.DEBUG:
#                    print "waiting for new files...", wait_counter
#                    wait_counter+=1
#                time.sleep(3)
                # Empty out list created in Selector class
                self.selector.issues = list()
                self.selector.current_tests = list()
                try:
                    if settings.USE_SPAWNED_THREADS:
                        file_found_path = self.queue.get(False)
                    else:
                        file_found_path = self.queue.get(block='true', timeout=_QTO)
                        _QTO = 5
                    
                    if file_found_path != None:
                        # append all files into the file stack to be processed.
                        if settings.DEBUG:
                            print "appending files"
                        files.append(file_found_path)
                        if settings.USE_SPAWNED_THREADS:
                            raise Queue.Empty
                    if settings.DEBUG:
                        print "files found so far in while loop are ", files
                    continue
                
                except Queue.Empty:
                #Stop emptying the Queue and process the result and let it fill up again, since pyinotify is still watching
                    if not files:
                        #if settings.DEBUG:
                            #print "Queue may be empty, but list of files is also empty, so let's keep monitoring"    
                        continue
                    if settings.USE_SPAWNED_THREADS:
                        # since this flag is True, spawn threads to process the files
                        for i, thread_state in enumerate(self.thread_list):
                            if thread_state == 0:
                                # signify that this thread is running by setting its value in the thread list to 1
                                self.thread_list[i] = 1
                                if settings.DEBUG:
                                    print "Thread list status: ", self.thread_list[:]
                                self._spawn_worker_thread(i, [files.pop(0), ])
                                print "number of files waiting to be processed: %d"  % len(files)
                                break
                    else:
                        while files:
                            if settings.DEBUG:
                                print "Queue.Empty exception, but files list is not empty, so files to process are", files
                            filepathitem = files.pop()
                            print "processing ", filepathitem
                            status, new_file_name = self.processFiles(filepathitem)
                            if settings.DEBUG:
                                print "Readying files to copy into the processed folder"
                            if status == True:
                                processed_files.append(new_file_name)
                        
                        # *******************************
                        # transfer control to nodebuilder
                        # *******************************

                        # first, setup options for nodebuilder
                        optParse = QueryObject(suppress_usage_message=True)

                        paired_ids = source_ids = list(set(self.selector.paired_ids))
                        for paired_id in paired_ids:
                            source_id = paired_id[0]
                            export_id = paired_id[1]
                            if settings.DEBUG:
                                print "nodebuilder generating output for source id:", source_id
                            # next call nodebuilder for each source id
                            # options are: ['startDate', 'endDate', 'alldates', 'reported', 'unreported', 'configID']
                            (options, args) = optParse.parser.parse_args(['-a', '-u', '-i%s' % source_id])
                            try:
                                NODEBUILDER = NodeBuilder(options)
                            except:
                                print "*****************************************************************"
                                print "*****************************************************************"
                                print "*****************************************************************"
                                synthesis_error = traceback.format_exc()
                                print synthesis_error
                                smtp = smtpInterface(settings)
                                smtp.setMessageSubject("ERROR -- Synthesis:FileHandler:monitor")
                                smtp.setRecipients(inputConfiguration.SMTPRECIPIENTS['testSource'])
                                smtp.setMessage("%s\r\n" % synthesis_error )
                                try:
                                    print "trying to send message"
                                    smtp.sendMessage()
                                except:
                                    print 'send failed'                
                                print "*****************************************************************"
                                print "*****************************************************************"
                                print "*****************************************************************"
                                continue
                            RESULTS = NODEBUILDER.run()
                    # empty list of paired ids
                    self.selector.paired_ids = list()
                    # Send processed files to the processed files folder:
                    if settings.DEBUG:
                        print 'Made it this far so send used files to the processed files folder.'
                    for processed_file in processed_files:
                        print 'Copying ' + inputConfiguration.USEDFILES_PATH + '/' + processed_file + ' to ' + outputConfiguration.PROCESSEDFILES_PATH + '/' + processed_file
                        fileutils.copyFile(inputConfiguration.USEDFILES_PATH + '/' + processed_file, outputConfiguration.PROCESSEDFILES_PATH  + '/' +  processed_file)
                        # Remove processed file from list
                        processed_files.pop(processed_files.index(processed_file))
                    #now go back to checking the Queue
                    continue

                except KeyboardInterrupt:
                    print "KeyboardInterrupt caught in selector.monitor() while loop"
                    print "shutting down..."
                    i = 0
                    while i < len(self.thread_list):
                        self.thread_list[i] = -1
                        i += 1

                    # comment the following for loop if you don't want spawned threads to finish
                    # processing files before exiting.
                    for thread_state in self.thread_list:
                        if thread_state == 1:
                            continue

                    self.file_input_watcher.stop_monitoring()
                    break

        except KeyboardInterrupt:
            print "KeyboardInterrupt caught in selector.monitor() main section"
            self.file_input_watcher.stop_monitoring()
        except:
            print "General Exception"
            self.file_input_watcher.stop_monitoring()
            raise
        
    def _spawn_worker_thread(self, id, files):  # @ReservedAssignment
        # spawn thread to process files. don't wait for spawned thread to finish
        threading._DummyThread._Thread__stop = lambda x: 42
        t = threading.Thread(target=self._worker_thread, args=(id, files, ))
        t.daemon = True
        t.start()

    def _worker_thread(self, id, files):  # @ReservedAssignment
        if settings.DEBUG:
            print "entering worker thread named: Thread-%d" % (id + 1)
        while files:
            # if the thread_list contains a -1, this means that someone stopped the
            # pyramid server. exit this spawned thread.
            if settings.DEBUG:
                print "self.thread_list", self.thread_list[:]
            if min(self.thread_list) == -1:
                print "The pyramid server was stopped.....exiting Thread-%d" % (id + 1)
                return
            # if an exception was encountered within a spawned thread, raise it
            if self.exception.value == 1:
                self.thread_list[id] = 0
                sys.exit(1)
            #if settings.DEBUG:
            #    print "Queue.Empty exception, but files list is not empty, so files to process are", files
            filepathitem = files.pop()
            if settings.DEBUG:
                print "%s" % ("*" * 32)
                print "Within Thread-%d" % (id + 1)
                print "%s" % ("*" * 32)
            print "processing ", filepathitem
            try:
                self.processFiles(filepathitem)
                print filepathitem
            except KeyboardInterrupt:
                self.thread_list[id] = 0
                print "KeyboardInterrupt caught in selector._worker_thread()"
                #self.file_input_watcher.stop_monitoring()
                self.exception.value = 1
            except:
                self.thread_list[id] = 0
                print "General Exception"
                #self.file_input_watcher.stop_monitoring()
                self.exception.value = 1
                raise
        # *******************************
        # transfer control to nodebuilder
        # *******************************
        try:
            # first, setup options for nodebuilder
            optParse = QueryObject(suppress_usage_message=True)

            if len(self.selector.paired_ids) > 0:
                paired_id = self.selector.paired_ids.pop(0)
                source_id = paired_id[0]
                export_id = paired_id[1]
                if settings.DEBUG:
                    print "nodebuilder generating output for source id:", source_id
                # next call nodebuilder for each source id
                # options are: ['startDate', 'endDate', 'alldates', 'reported', 'unreported', 'configID']
                (options, args) = optParse.parser.parse_args(['-a', '-u', '-i%s' % source_id])
                try:
                    NODEBUILDER = NodeBuilder(options, export_id=export_id)
                except:
                    print "*****************************************************************"
                    print "*****************************************************************"
                    print "*****************************************************************"
                    synthesis_error = traceback.format_exc()
                    print synthesis_error
                    smtp = smtpInterface(settings)
                    smtp.setMessageSubject("ERROR -- Synthesis:FileHandler:_worker_thread")
                    smtp.setRecipients(inputConfiguration.SMTPRECIPIENTS['testSource'])
                    smtp.setMessage("%s\r\n" % synthesis_error )
                    try:
                        print "trying to send message"
                        smtp.sendMessage()
                    except:
                        print 'send failed'                
                    print "*****************************************************************"
                    print "*****************************************************************"
                    print "*****************************************************************"
                RESULTS = NODEBUILDER.run()
        except KeyboardInterrupt:
            self.thread_list[id] = 0
            print "KeyboardInterrupt caught in selector._worker_thread()"
            #self.file_input_watcher.stop_monitoring()
            self.exception.value = 1
        except:
            self.thread_list[id] = 0
            print "General Exception"
            #self.file_input_watcher.stop_monitoring()
            self.exception.value = 1
            raise
        # signify that the thread is no longer running
        self.thread_list[id] = 0
        if settings.DEBUG:
            print "Thread list status: ", self.thread_list[:]
        if settings.DEBUG:
            print "exiting worker thread named: Thread-%d" % (id + 1)

class Selector:
    '''Figures out which data format is being received.'''
    
    def __init__(self):
        self.db = dbobjects.DB()
        self.db.Base.metadata.create_all()

        self.paired_ids = []

        if settings.DEBUG:
            print "selector instantiated and figuring out what schema are available"
            for item in settings.SCHEMA_DOCS:
                print 'schema to potentially load: ' + settings.SCHEMA_DOCS[item]

        self.current_tests = [] # Added by FBY on 2012-01-19
        self.issues = [] # Added by FBY on 2012-01-19

    def validate(self, instance_file_loc, shred=True): 
        '''Validates against the various available schema and csv records.\
        If not specified in the configs, it keeps trying each available \
        test to find the first which successfully validates.  You just \
        pass it a test, and the xml instance data.'''
        
        #tests = [HUDHMIS28XMLTest, HUDHMIS30XMLTest, JFCSXMLTest, PARXMLTest]
        #tests = [HUDHMIS30XMLTest,HUDHMIS28XMLTest]
        #tests = [HUDHMIS30XMLTest, HUDHMIS28XMLTest, OCCHUDHMIS30XMLTest, JFCSXMLTest, TBCExtendHUDHMISXMLTest]
        tests = [HUDHMIS30XMLTest, HUDHMIS28XMLTest, JFCSXMLTest, TBCExtendHUDHMISXMLTest]
        #tests = [HUDHMIS30XMLTest]
        #tests = [HUDHMIS28XMLTest]
        if settings.DEBUG:
            print "tests are", tests
        #readers = [HUDHMIS28XMLReader, HUDHMIS30XMLReader, JFCSXMLInputReader, PARXMLInputReader]
        readers = {HUDHMIS30XMLTest:HUDHMIS30XMLInputReader, HUDHMIS28XMLTest:HUDHMIS28XMLInputReader, OCCHUDHMIS30XMLTest:OCCHUDHMIS30XMLInputReader, JFCSXMLTest:JFCSXMLInputReader, TBCExtendHUDHMISXMLTest:TBCHUDHMISXML30InputReader}
        #readers = {HUDHMIS30XMLTest:GenericXMLReader,HUDHMIS28XMLTest:GenericXMLReader,OCCHUDHMIS30XMLTest:GenericXMLReader}

        self.current_tests = tests # Added by FBY on 2012-01-19
        
        if settings.SKIP_VALIDATION_TEST is True:
            print 'skipping tests battery for debugging'
            print "just shredding with JFCSXMLReader service_event schema"
            JFCSXMLInputReader.data_type = 'service_event'
            readers[JFCSXMLTest](instance_file_loc, self.db).shred()
            return
        
        if settings.DEBUG:
            print "readers are", readers
        results = []

        for test in tests:
            test_instance = test()
            result = test_instance.validate(instance_file_loc)
            self.issues.append(test_instance.issues)
            results.append(result)
            if settings.DEBUG:
                print "validation return result is", result
                print "results are cumulatively", results
            if True in results:
                #finds the first 'True' in the list; even if there are many, it gets the first one 
                loc_true = results.index(True)
                #if settings.DEBUG:
                    #print "loc_true is", loc_true
                length_list = len(results)
                #if settings.DEBUG:
                    #print "len(results) is: ", length_list
                #if the first 'True' validation was the last validation result, go shred/move
                if loc_true  == (length_list-1):
                        #if settings.DEBUG:
                        #print "loc_true is", (loc_true), "and that matches (length_list - 1) of ", (length_list - 1)
                    if settings.DEBUG:
                        print "we haven't had a positive validation until now, so go ahead and shred/move it"
                    if result:
                        if settings.DEBUG:
                            print "shredding..."
                        if shred:
                            if settings.DEBUG:
                                print "readers[test] is: ", readers[test]
                                print "instance_file_loc: ", instance_file_loc
                            source_id, export_id = readers[test](instance_file_loc, self.db).shred()
                            if source_id != None:
                                self.paired_ids.append((source_id, export_id))
                            
        if not results:
            print "results empty"
        self.results = results # Added by FBY on 2012-01-19
        return results

class VendorXMLTest:
    '''Stub for any specific vendor's non-standardized XML format.'''
    def __init__(self):
        self.name = 'Vendor XML'
        print 'running the', self.name, 'test'
        
    def validate(self, instance_filename):
        '''implementation of interface's validate method'''
        print '\nThe', self.name, 'test not implemented.'
        print '...but intended to validate', instance_filename
        return False

class TBCExtendHUDHMISXMLTest:	# JCS New 2012-01-05
    '''Load in the HUD HMIS Schema, version 3.0.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'TBCExtendHUDHMISXML'
        print 'running the', self.name, 'test'
        self.schema_filename = settings.SCHEMA_DOCS['tbc_extend_hud_hmis_xml']
        print "settings.SCHEMA_DOCS['tbc_extend_hud_hmis_xml'] is: ", settings.SCHEMA_DOCS['tbc_extend_hud_hmis_xml']
    
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
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error
            pass

class HUDHMIS28XMLTest:
    '''Load in the HUD HMIS Schema, version 2.8.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'HUDHMIS28XML'
        print 'running the', self.name, 'test'
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
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error
            pass   

class HUDHMIS30XMLTest:
    '''Load in the HUD HMIS Schema, version 3.0.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'HUDHMIS30XML'
        print 'running the', self.name, 'test'
        self.schema_filename = settings.SCHEMA_DOCS['hud_hmis_xml_3_0']
        print "settings.SCHEMA_DOCS['hud_hmis_xml_3_0'] is: ", settings.SCHEMA_DOCS['hud_hmis_xml_3_0']
    
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
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error
            pass


class OCCHUDHMIS30XMLTest:
    '''Load in the HUD HMIS Schema, version 3.0.'''
    def __init__(self):
        self.issues = "" # Added by FBY on 2012-01-19
        self.name = 'OCCHUDHMIS30XML'
        print 'running the', self.name, 'test'
        self.schema_filename = settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0']
        print "settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0'] is: ", settings.SCHEMA_DOCS['occ_hud_hmis_xml_3_0']
    
    def validate(self, instance_stream):
        '''This specific data format's validation process.'''
        try:
            schema = open(self.schema_filename,'r')
        except:
            print "couldn't open schema file", self.schema_filename
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
                print 'The xml did not successfully validate against %s' % self.name
                try:
                    detailed_results = schema_parsed_xsd.assertValid\
                    (instance_parsed)
                    print detailed_results
                    self.issues = detailed_results # Added by FBY on 2012-01-19
                    return results
                except etree.DocumentInvalid, error:
                    print 'Document Invalid Exception.  Here is the detail:'
                    print error
                    self.issues = error # Added by FBY on 2012-01-19
                    return results
            if results == None:
                print "The validator erred and couldn't determine if the xml \
                was either valid or invalid."
                return results
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error
            pass
        
class SvcPoint20XMLTest:
    '''Load in the SVCPoint Schema, version 2.0.'''
    def __init__(self):
        self.name = 'Svcpt 2.0 XML'
        print 'running the Svcpt 2.0 XML test'
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

class SvcPoint406XMLTest:
    '''Load in the SVCPoint Schema, version 4.06'''
    def __init__(self):
        self.name = 'Svc406 XML'
        print 'running the Svcpt 4.06 XML test'
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

class SvcPoint5XMLTest:
    '''Load in the SVCPoint Schema, version 5.00'''
    def __init__(self):
        self.name = 'Svc5 XML'
        print 'running the Svcpt 5.00 XML test'
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
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error
            raise

class hl7CCDXMLTest:
    '''Load in the HL7 CCD Schema'''
    def __init__(self):
        self.name = 'hl7 CCD XML'
        print 'running the hl7 CCD XML test'
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
            print 'XML Syntax Error.  There appears to be malformed XML.  ', error
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
        print 'running the', self.name, 'test'
        
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
            print "Determining by service event schema"
            results = self.schemaTest(copy_instance_stream, self.service_event_schema_filename)
            if results == True:
                fileutils.makeBlock('JFCS service event XML data found.  Determined by service event schema.')
                JFCSXMLInputReader.data_type = 'service_event'
                return results
            print "Determining by client schema"
            results = self.schemaTest(copy_instance_stream, self.client_schema_filename)
            if results == True:
                fileutils.makeBlock('JFCS client XML data found.  Determined by client schema.')
                JFCSXMLInputReader.data_type = 'client'
                return results
            print "Determining by service event elements."
            if self.service_event_elements is not None:
                print self.service_event_elements
                results = self.elementTest(copy_instance_stream, self.service_event_elements)
                if results == True:
                    fileutils.makeBlock('JFCS service event XML data found.  Determined by service event elements.')
                    JFCSXMLInputReader.data_type = 'service_event'
                    return results
            print "Determining by client elements."
            if self.client_elements is not None:
                print self.client_elements
                results = self.elementTest(copy_instance_stream, self.client_elements)
                if results == True:
                    fileutils.makeBlock('JFCS client XML data found.  Determined by client elements.')
                    JFCSXMLInputReader.data_type = 'client'
                    return results
                print "returning False"
                return False
            else:
                print "All the JFCS Tests Failed, returning False"
                self.issues = "All the JFCS Tests Failed, returning False"
                return False
        except Exception, exception:
            print 'XML Syntax Error in validate.  There appears to be malformed XML.  ', exception
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
        except etree.XMLSyntaxError, error:
            print 'XML Syntax Error in schemaTest.  There appears to be malformed XML.  ', error
            return False
        
    def elementTest(self, copy_instance_stream, elements):
        '''Attempt to find elements in the input file by searching the tree'''
        print "inside element test"
        print "elements are: ", elements
        xml_doc = etree.parse(copy_instance_stream)
        for e in elements:
            search_term = ".//" + e
            if xml_doc.find(search_term) is None:
                print "returning False from inside elementTest"
                return False
        print "returning True  from inside elementTest"
        return True
    
class PARXMLTest:
    '''Load in the HUD HMIS Extended Schema for Operation PAR'''
    def __init__(self):
        self.name = 'PARXML'
        print 'running the', self.name, 'test'
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
                            print 'XML Error.  Value %s exceeds database field length.' % str(e.tag)
                            return False    ## remove this when testing and perform manual truncate in PARXMLReader()
                
                #return False ## return invalid, use this to only test validation of string lengths and exit                        
                
                fileutils.makeBlock('The Operation PAR XML successfully validated.')
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
        
#class GenericXMLInputReader(readertype):
#    def __init__(self, instance_filename):
#        self.reader = OCCHUDHMISXML30Reader(instance_filename)
#        if settings.DEBUG:
#            print "self.reader to be read is: ", self.reader
#            print "does self.reader exist?", os.path.exists(self.reader)
#        
#    def shred(self):
#        tree = self.reader.read()
#        try:
#            self.reader.process_data(tree)
#        except:
#            raise        

class TBCHUDHMISXML30InputReader(TBCHUDHMISXML30Reader):
    def __init__(self, instance_filename, db):
        self.reader = TBCHUDHMISXML30Reader(instance_filename, db)
        
    def shred(self):
        tree = self.reader.read()
        try:
            source_id, export_id = self.reader.process_data(tree)
            if source_id != None:
                return source_id, export_id
        except:
            raise

class HUDHMIS28XMLInputReader(HMISXML28Reader):
    def __init__(self, instance_filename, db):
        self.reader = HMISXML28Reader(instance_filename, db)
        
    def shred(self):
        tree = self.reader.read()
        try:
            source_ids = self.reader.process_data(tree)
            if source_ids != None:
                return source_ids
        except:
            raise

class HUDHMIS30XMLInputReader(HMISXML30Reader):
    def __init__(self, instance_filename, db):
        self.reader = HMISXML30Reader(instance_filename, db)
        
    def shred(self):
        tree = self.reader.read()
        try:
            source_ids = self.reader.process_data(tree)
            if source_ids != None:
                return source_ids
        except:
            raise
        
class OCCHUDHMIS30XMLInputReader(OCCHUDHMISXML30Reader):
    def __init__(self, instance_filename, db):
        #if settings.DEBUG:
            #print "does ", instance_filename, "exist?", os.path.exists(instance_filename)
        self.reader = OCCHUDHMISXML30Reader(instance_filename, db)
        if settings.DEBUG:    
            print "self.reader to be read is: ", self.reader
    def shred(self):
        tree = self.reader.read()
        try:
            source_ids = self.reader.process_data(tree)
            if source_ids != None:
                return source_ids
        except:
            raise        

class JFCSXMLInputReader(JFCSXMLReader):
    def __init__(self, instance_filename):
        self.reader = JFCSXMLReader(instance_filename)
        
    def shred(self):
        tree = self.reader.read()
        try:
            source_ids = self.reader.process_data(tree, self.data_type)
            if source_ids != None:
                return source_ids
        except:
            raise

#class PARXMLInputReader(PARXMLReader):
#    def __init__(self, instance_filename):
#        self.reader = PARXMLReader(instance_filename)
#        
#    def shred(self):
#        tree = self.reader.read()
#        try:
#            self.reader.process_data(tree)
#        except:
#            raise
    
class VendorXMLInputReader():
    def __init__(self, xml_instance_file):
        self.name = 'Vendor XML'
        pass

    def shred(self):
        '''implementation of interface's shred method'''
        print '\nThe', self.name, 'test not implemented.'
        print '...but intended to shred the XML Document: %s' % self.instance_filename
        return False


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
