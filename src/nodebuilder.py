from conf import settings
import exceptions as exceptions
import dbobjects

#from vendorxmlxxwriter import VendorXMLXXWriter

# for validation
from selector import HUDHMIS30XMLTest, HUDHMIS28XMLTest, JFCSXMLTest, VendorXMLTest, SvcPoint406XMLTest, SvcPoint5XMLTest, hl7CCDXMLTest
from errcatalog import catalog
import os
from queryobject import QueryObject
from conf import outputConfiguration
import postprocessing
import fileutils
from emailprocessor import XMLProcessorNotifier
import iniutils
import resttransport
import soaptransport
from Encryption import *
import uuid
import shutil
# from hmisxml30writer import HMISXMLWriter	# JCS 9/25/11
# from hmisxml28writer import HMISXML28Writer	# JCS 9/25/11
global hmiscsv30writer_loaded   # "global" does not make vars global - it is supposed to be used inside functions
global hmisxml28writer_loaded   # to say to use the definition of this name which is defined outside the function JCS
global hmisxml30writer_loaded
global svcptxml20writer_loaded 
global svcptxml406writer_loaded
global jfcsxmlwriter_loaded
global hl7CCDwriter_loaded


hmiscsv30writer_loaded = False
hmisxml28writer_loaded = False
hmisxml30writer_loaded = False
svcptxml20writer_loaded = False
svcptxml406writer_loaded = False
jfcsxmlwriter_loaded = False
hl7CCDwriter_loaded = False

class NodeBuilder():

    def __init__(self, queryOptions):
        print "initializing nodebuilder"
        # initialize dbobjects
    
        
        # fixme, need to decipher the query objects against the configuration (table, object, ini, conf..)
        # this should then pull the correct module below and run the process.
        self.generateOutputformat = outputConfiguration.Configuration[queryOptions.configID]['outputFormat']
        self.transport = outputConfiguration.Configuration[queryOptions.configID]['transportConfiguration']
        self.encryption = outputConfiguration.Configuration[queryOptions.configID]['encryption']
        self.outputFilesPath = outputConfiguration.Configuration[queryOptions.configID]['destination']
        
        self.queryOptions = queryOptions
        print '==== Output Format', self.generateOutputformat		# JCS
        if self.generateOutputformat == 'svcpoint5':
            try:
                from synthesis.svcpointxml5writer import SvcPointXML5Writer
                svcptxml5writer_loaded = True
                print "import of Svcpt XML Writer, version 5 was successful"
            except Exception as e:
                print "import of Svcpt XML Writer, version 5 failed", e
                svcptxml5writer_loaded = False
            if self.transport == "save":
                self.writer = SvcPointXML5Writer(self.outputFilesPath, queryOptions)
                print '==== self.writer:', self.writer
                self.validator = SvcPoint5XMLTest()
                print '==== self.validator:', self.validator
        
        elif self.generateOutputformat == 'hl7ccd':     # JCS
            try:
                from synthesis.hl7CCDwriter import hl7CCDwriter
                hl7CCDwriter_loaded = True
                print "import of HL7 XML Writer was successful"
            except Exception as e:
                print "import of HL7 XML Writer failed", e
                hl7CCDwriter_loaded = False
            if self.transport in ("save", "rest", "soap"):
                self.writer = hl7CCDwriter(self.outputFilesPath, queryOptions)
                print '==== self.writer:', self.writer
                self.validator = hl7CCDXMLTest()
                print '==== self.validator:', self.validator

        elif self.generateOutputformat == 'svcpoint406':	# JCS
            try:
                from synthesis.svcpointxml406writer import SvcPointXMLWriter
                svcptxml406writer_loaded = True
                print "import of Svcpt XML Writer, version 4.06 was successful"
            except:
                print "import of Svcpt XML Writer, version 4.06 failed"
                svcptxml406writer_loaded = False
            if self.transport == "save":
                self.writer = SvcPointXMLWriter(self.outputFilesPath, queryOptions)
                self.validator = SvcPoint406XMLTest()
            
#        elif self.generateOutputformat == 'svcpoint20':
#            #from svcPointXML20writer import SvcPointXML20Writer
#            # pick the plug-in to import
#            try:
#                from svcPointXML20writer import SvcPointXMLWriter 
#                svcptxml20writer_loaded = True
#                print "import of Svcpt XML Writer, version 2.0 was successful"
#            except:
#                print "import of Svcpt XML Writer, version 2.0 failed"
#                svcptxml20writer_loaded = False
#            self.writer = SvcPointXMLWriter(settings.OUTPUTFILES_PATH, queryOptions)
#            self.validator = SVCPOINT20XMLTest()
                
        elif self.generateOutputformat == 'hmisxml28':
            try:
                from hmisxml28writer import HMISXML28Writer#IGNORE:@ImportRedefinition
                hmisxml28writer_loaded = True
            except:
                print "import of HMISXMLWriter, version 2.8, failed"
                hmisxml28writer_loaded = False
            if self.transport == "save":
                if settings.DEBUG:
                    print "destination is ", self.outputFilesPath
                self.writer = HMISXML28Writer(self.outputFilesPath, queryOptions)           
                self.validator = HUDHMIS28XMLTest()
            
        elif self.generateOutputformat == 'hmisxml30':
            try:
                from hmisxml30writer import HMISXMLWriter#IGNORE:@ImportRedefinition
                print "import of HMISXMLWriter, version 3.0 occurred successfully"
                hmisxml30writer_loaded = True
            except Exception as e:
                print "import of HMISXMLWriter, version 3.0, failed", e
                hmisxml30writer_loaded = False
            if self.transport == "save":
                if settings.DEBUG:
                    print "destination is ", self.outputFilesPath
                self.writer = HMISXMLWriter(self.outputFilesPath, queryOptions)                    
                self.validator = HUDHMIS30XMLTest() 
            
        elif self.generateOutputformat == 'hmiscsv30':
            try:
                from hmiscsv30writer import HmisCsv30Writer
                hmiscsv30writer_loaded = True
            except:
                hmiscsv30writer_loaded = False
            if self.transport == "save":
                self.writer = HmisCsv30Writer(self.outputFilesPath, queryOptions, debug=True)                    
            #self.validator = HmisCsv30Test()           
        elif self.generateOutputformat == 'jfcsxml':
            print "Need to hook up the JFCSWriter in Nodebuilder"
#            self.writer = JFCSXMLWriter()                   
#            self.validator = JFCSXMLTest()
        elif self.generateOutputformat == 'pseudo':
            print "Pseudo writer encounted. Skipping..."
        else:
            # new error cataloging scheme, pull the error from the catalog, then raise the exception (centralize error catalog management)
            err = catalog.errorCatalog[1001]
            raise exceptions.UndefinedXMLWriter, (err[0], err[1], 'NodeBuilder.__init__() ' + self.generateOutputformat)
            
        #fileStream = open(new_file,'r')
        # validate the file prior to uploading it
        #if self.validator.validate(fileStream):
        
        #setup the postprocessing module    
        self.pprocess = postprocessing.PostProcessing(queryOptions.configID)
        #print '==== self.pprocess:', self.pprocess	# JCS - empty??

    def encrypt_file(self, filename):
        if self.encryption == "openpgp":
            gpg = GPG()
            gpg.encryptFile(filename, os.path.splitext(filename)[0] + '.gpg')
            shutil.move(filename, outputConfiguration.PROCESSEDFILES_PATH)
            return os.path.splitext(filename)[0] + '.gpg'
        elif self.encryption == "3des":
            fo = open(filename, 'r')
            data = fo.read()
            fo.close()
            des = DES3()
            encrypted_data = des.encrypt(data, settings.DES3_KEY)
            fo = open(os.path.splitext(filename)[0] + '.des3', 'w')
            fo.write(encrypted_data)
            fo.flush()
            fo.close()
            shutil.move(filename, outputConfiguration.PROCESSEDFILES_PATH)
            return os.path.splitext(filename)[0] + '.des3'
        else:
            # do nothing. return as is
            return filename
        
    def run(self):
        '''This is the main method controlling this entire program.'''
        
        # Load the data via dbobjects
        
        
        # try to write the output file and then validate it.
        #for writer,validator in map(None, self.writer, self.validator):
            #result = item.validate(instance_doc)
            # if results is True, we can process against this reader.
        if self.transport == 'soap':
            ccd_data = self.writer.get() #TODO: (FBY) The data return from this call be a list of documents. Is this correct?
            soap = soaptransport.SoapEnv(self.queryOptions.configID)
            #assert (soap.send_soap_envelope(ccd_data)[0] == True), "Sending CCD via SOAP transport failed!"
            result, details = soap.send_soap_envelope(ccd_data)
            print result, details
        elif self.transport == 'rest':
            ccd_data = self.writer.get() #TODO: (FBY) The data return from this call be a list of documents. Is this correct?
            rest = resttransport.REST(self.queryOptions.configID)
            #assert (rest.post(ccd_data)[0] == True), "Sending CCD via REST transport failed!"
            result, details = rest.post('CCD_%s' % str(uuid.uuid4()).replace('-',''), ccd_data)
            print result, details
        else:
            # the remaining transport require file IO
            if self.generateOutputformat != "pseudo":
                if self.writer.write():
                    #filesToTransfer = fileutils.grabFiles(os.path.join(settings.OUTPUTFILES_PATH, "*.xml"))
                    filesToTransfer = fileutils.grabFiles(os.path.join(self.outputFilesPath, "*.xml"))
                    
                    # create a list of valid files to upload
                    validFiles = []
                    # Loop over each file and validate it.
                    for eachFile in filesToTransfer:
                        fs = open(eachFile, 'r')
                        if self.validator.validate(fs):
                            gpg = GPG()
                            validFiles.append(eachFile)
                            print 'oK'
                            # since the file was validated, its OK to encrypt it now.
                            possible_new_file_name = self.encrypt_file(eachFile)
                            validFiles[validFiles.index(eachFile)] = possible_new_file_name
                            filesToTransfer[filesToTransfer.index(eachFile)] = possible_new_file_name
                        else:
                            pass                # Fixme append invalid files to list and report this.
                        
                        fs.close()
                    
                    # upload the valid files
                    # how to transport the files (debugging)
                    if self.transport == 'save':
                        print 'Output Complete...Please see output files: %s' % filesToTransfer
                        
                    if self.transport == 'sys.stdout':
                        for eachFile in validFiles:
                            fs = open(eachFile, 'r')
                            # open the file and echo it to stdout
                            lines = fs.readlines()
                            fs.close()              # done with file close handle
                            for line in lines:
                                print line        
                                
                    if self.transport == 'sftp':
                        self.pprocess.processFileSFTP(validFiles)
                    elif self.transport == 'email':
                        # Loop over the list and each file needs to be emailed separately (size)
                        for eachFile in validFiles:
                            self.email = XMLProcessorNotifier("", eachFile)     # fixme (zip and encrypt?)
                            msgBody = self.formatMsgBody()
                            self.email.sendDocumentAttachment('Your report results', msgBody, eachFile)
                    elif self.transport == 'vpnftp':
                        # SBB20100430 Only upload if we have a validated file(s)
                        if len(validFiles) > 0:
                            pd = iniutils.LoadConfig('fileConverter.ini')
                            self.pprocess.setINI(pd)
                            self.pprocess.processFileVPN(validFiles)
                    elif self.transport == 'vpncp':
                        pass
                            
                        #print results
                        #print 'This is the result before it goes back to the test_unit:', \
                        #results
                        #return results
        
    def formatMsgBody(self):
        msgBody = "Your report was requested on %s. /r/n The report criteria is: \r\n\t StartDate: %s /r/n \t EndDate: %s /r/n /t Previously Reported: %s /r/n /t Previously UnReported: %s' % (datetime.today() ,self.queryOptions.startDate, self.queryOptions.endDate, self.queryOptions.reported, self.queryOptions.unreported)"#IGNORE:@UnusedVariable

    def selectNodes(self, start_date, end_date, nodename):
        pass
    
    def flagNodes(self):
        pass

#if svcptxml406writer_loaded is True:
#    if settings.DEBUG:
#        print "svcptxmlwriter not loaded"
#    class SvcPointXMLwriter(SvcPointXMLWriter):
#        
#        def __init__(self):
#            self.xML = SvcPointXMLWriter((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))
#    
#        def write(self):
#            self.xML.processXML()
#            self.xML.writeOutXML()
#else: 
#    pass

#if hmiscsv30writer_loaded is True:
#    class HmisCsvWriter(HmisCsv30Writer):     
#         def __init__(self): 
#             self.csv = HmisCsv30Writer((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH))) 
#    
#         def write(self): 
#             pass
#else: 
#    #if settings.DEBUG:
#        #print "hmiscsv30writer not found in conf yet, so not initializing class: HmisCsvWriter yet"
#    pass

#if hmisxml30writer_loaded is True:
#    class HmisXmlWriter(HMISXMLWriter):
#        
#        def __init__(self):
#            self.xML = HMISXMLWriter((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))
#    
#        def write(self):
#            pass
#else: 
#    pass

#if hmisxml28writer_loaded is True:
#    class HmisXmlWriter(HMISXML28Writer):
#        
#        def __init__(self):
#            self.xML = HMISXML28Writer((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))
#    
#        def write(self):
#            pass
#else: 
#    pass

if __name__ == '__main__':
    
    optParse = QueryObject()
    options = optParse.getOptions()
    if options != None:
        try:
            NODEBUILDER = NodeBuilder(options)
            RESULTS = NODEBUILDER.run()
            
        except exceptions.UndefinedXMLWriter:
            print "Please specify a format for outputting your XML"
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
