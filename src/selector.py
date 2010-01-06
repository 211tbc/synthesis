'''Figures out what type of data format we are dealing with, using validation \
or whatever we can use to test, so the appropriate reader correct \
implementation can be used.'''
import fileUtils 
from fileinputwatcher import FileInputWatcher
#import hmisxml28reader
from hmisxml28reader import HMISXML28Reader
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

	def setProcessingOptions(self, docName):
		''' ProcessingOptions is a dictionary on a perfile/sender basis.
		Dictionary contains settings like does the sender use encryption etc.
		self.ProcessingOptions = 
			{
				'SMTPTOADDRESS': ['sbenninghoff@yahoo.com',],
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
		if self.ProcessingOptions['USES_ENCRYPTION']:
			# decrypt the file
			fileStream = self.crypto.decryptFile2Stream(new_file)
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
		
class Selector:#IGNORE:R0903
	'''Figures out which data format is being received.'''
	#local_schema = {'hud_hmis_2_8_xml':'/home/eric/Alexandria_Consulting/Suncoast/JFCS/src/hmisparse/schema/HUD_HMIS_2_8.xsd'} #IGNORE:C0301
	local_schema = settings.SCHEMA_DOCS
	def __init__(self):
		#need to put this attribute in the .ini file
		
		pass

	# SBB20090917 modified to take a stream instead of a file
	#def validate(self, instance_doc, shred=True): #IGNORE:R0201
	def validate(self, instance_doc, shred=True): #IGNORE:R0201
		'''Validates against the various available schema and csv records.\
		If not specified in the configs, it keeps trying each available \
		test to find the first which successfully validates.  You just \
		pass it a test, and the xml instance data.'''
		#check if config specifies which schema should be used for this install
		#config_available = 'false'
		#output the results (which schema it did or did not validate against
		#if had a config specified
		FILEHANDLER = FileHandler()
		
		tests = [VendorXMLTest(), HUDHMIS28XMLTest(), JFCSXMLTest()]
		readers = [VendorXMLReader(instance_doc), HUDHMIS28XMLReader(instance_doc), JFCSXMLReader(instance_doc)]
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
	
class HUDHMIS28XMLTest:#IGNORE:R0903
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
	
class HUDHMIS28XMLReader(HMISXML28Reader):#IGNORE:R0903
	def __init__(self, instance_filename):
		self.reader = HMISXML28Reader(instance_filename)
		
	def shred(self):
		tree = self.reader.read()
		try:
			self.reader.process_data(tree)
		except:
			raise
	
class JFCSXMLReader():#IGNORE:R0903
	def __init__(self, instance_doc):
		pass
	
	def shred(self):
		'''implementation of interface's shred method'''
		print '\nThe', self.name, 'test not implemented.'
		print '...but intended to shred the XML Document: %s' % instance_filename
		return False
	
class VendorXMLReader():#IGNORE:R0903
	def __init__(self, instance_doc):
		pass

	def shred(self):
		'''implementation of interface's shred method'''
		print '\nThe', self.name, 'test not implemented.'
		print '...but intended to shred the XML Document: %s' % instance_filename
		return False
	
if __name__ == '__main__':
	
	if settings.DEBUG and settings.MODE == 'TEST':								# Only reset the DB in Test mode
		import postgresutils
		UTILS = postgresutils.Utils()
		UTILS.blank_database()
		
	
	FILEHANDLER = FileHandler()
	RESULTS = FILEHANDLER.run()