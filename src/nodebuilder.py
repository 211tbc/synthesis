#!/usr/bin/env python

from conf import settings
import clsExceptions 
import DBObjects

#from svcpointxml20writer import SVCPOINTXML20Writer
# pick the plug-in to import
import_string = "from svcpointxml_%s_writer import SVCPOINTXMLWriter" % settings.SVCPT_VERSION
exec import_string

from hmisxml28writer import HMISXML28Writer
from vendorxmlxxwriter import VendorXMLXXWriter
# for validation
from selector import HUDHMIS28XMLTest, JFCSXMLTest, VendorXMLTest, SVCPOINTXMLTest
from errcatalog import catalog
import os
import sys
from queryObject import queryObject
from conf import outputConfiguration
import clsPostProcessing
import fileUtils
from emailProcessor import XMLProcessorNotifier
from datetime import datetime
import iniUtils

class NodeBuilder(DBObjects.databaseObjects):

    def __init__(self, queryOptions):
        
        # initialize DBObjects
        DBObjects.databaseObjects()
        
        # fixme, need to decipher the query objects against the configuration (table, object, ini, conf..)
        # this should then pull the correct module below and run the process.
        generateOutputformat = outputConfiguration.Configuration[queryOptions.configID]['outputFormat']
        self.transport = outputConfiguration.Configuration[queryOptions.configID]['transportConfiguration']
        
        self.queryOptions = queryOptions
        
        if generateOutputformat == 'svcpoint':
            self.writer = SVCPOINTXMLWriter(settings.OUTPUTFILES_PATH, queryOptions)
            self.validator = SVCPOINTXMLTest()               
        elif generateOutputformat == 'hmisxml':
            self.writer = HmisXmlWriter()                   
            self.validator = HUDHMIS28XMLTest()              
        elif generateOutputformat == 'jfcsxml':
            self.writer = JFCSXMLWriter()                   
            self.validator = JFCSXMLTest()                 
        else:
            # new error cataloging scheme, pull the error from the catalog, then raise the exception (centralize error catalog management)
            err = catalog.errorCatalog[1001]
            raise clsExceptions.UndefinedXMLWriter, (err[0], err[1], 'NodeBuilder.__init__() ' + generateOutputformat)
            
        #fileStream = open(new_file,'r')
        ## validate the file prior to uploading it
        #if self.validator.validate(fileStream):
        
        # setup the postprocessing module    
        self.pprocess = clsPostProcessing.clsPostProcessing(queryOptions.configID)
        self.FILEUTIL = fileUtils.fileUtilities()
        
    def run(self):
        '''This is the main method controlling this entire program.'''
        
        # Load the data via DBObjects
        
        
        # try to write the output file and then validate it.
        #for writer,validator in map(None, self.writer, self.validator):
            #result = item.validate(instance_doc)
            # if results is True, we can process against this reader.
        if self.writer.write():
            filesToTransfer = self.FILEUTIL.grabFiles(os.path.join(settings.OUTPUTFILES_PATH, "*.xml"))
            
            # create a list of valid files to upload
            validFiles = []
            # Loop over each file and validate it.
            for eachFile in filesToTransfer:
                fs = open(eachFile, 'r')
                if self.validator.validate(fs):
                    validFiles.append(eachFile)
                    print 'oK'
                else:
                    pass                # Fixme append invalid files to list and report this.
                
                fs.close()
            
            # upload the valid files
            # how to transport the files (debugging)
            if self.transport == '':
                print 'Output Complete...Please see output file: %s' % filesToTransfer
                
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
                    pd = iniUtils.LoadConfig('fileConverter.ini')
                    self.pprocess.setINI(pd)
                    self.pprocess.processFileVPN(validFiles)
            elif self.transport == 'vpncp':
                pass
                    
                #print results
                #print 'This is the result before it goes back to the test_unit:', \
                #results
                #return results
        
    def formatMsgBody(self):
        msgBody = "Your report was requested on %s. /r/n" \
                  'The report criteria is: \r\n' \
                  '\t StartDate: %s /r/n \t EndDate: %s /r/n /t Previously Reported: %s /r/n /t Previously UnReported: %s' % (datetime.today() ,self.queryOptions.startDate, self.queryOptions.endDate, self.queryOptions.reported, self.queryOptions.unreported)

    
    def selectNodes(self, start_date, end_date, nodename):
        pass
    
    def flagNodes(self):
        pass
    
class SvcPointXMLwriter(SVCPOINTXMLWriter):
    
    def __init__(self):
        self.xML = SVCPOINTXMLWriter((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))

    def write(self):
        self.xML.processXML()
        self.xML.writeOutXML()
    
class HmisXmlWriter(HMISXML28Writer):
    
    def __init__(self):
        self.xML = SVCPOINTXML20Writer((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))

    def write(self):
        pass

if __name__ == '__main__':
    
    optParse = queryObject()
    options = optParse.getOptions()
    if options != None:
        try:
            NODEBUILDER = NodeBuilder(options)
            RESULTS = NODEBUILDER.run()
            
        except clsExceptions.UndefinedXMLWriter:
            print "Please specify a format for outputting your XML"
            raise
    