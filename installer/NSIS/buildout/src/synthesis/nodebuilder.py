#!/usr/bin/env python

from conf import settings
import clsExceptions 
import DBObjects
from svcpointxml20writer import SVCPOINTXML20Writer
from hmisxml28writer import HMISXML28Writer
from vendorxmlxxwriter import VendorXMLXXWriter
# for validation
from selector import HUDHMIS28XMLTest, JFCSXMLTest, VendorXMLTest
from errcatalog import catalog
import os
import sys
from queryObject import queryObject
from conf import outputConfiguration
import clsPostProcessing
import fileUtils

class NodeBuilder(DBObjects.databaseObjects):

    def __init__(self, queryOptions):
        
        # fixme, need to decipher the query objects against the configuration (table, object, ini, conf..)
        # this should then pull the correct module below and run the process.
        generateOutputformat = outputConfiguration.Configuration[queryOptions.configID]['outputFormat']
        self.transport = outputConfiguration.Configuration[queryOptions.configID]['transportConfiguration']
        
        if generateOutputformat == 'svcpoint':
            self.writer = SVCPOINTXML20Writer(settings.OUTPUTFILES_PATH, queryOptions)
            self.validator = VendorXMLTest()               
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
            if self.validator.validate(xmlDoc):
                print 'oK'        
        
        filesToTransfer = self.FILEUTIL.grabFiles(os.path.join(settings.OUTPUTFILES_PATH, "*.xml"))
        
        # how to transport the files
        if self.transport == 'sftp':
            self.pprocess.processFileSFTP(filesToTransfer)
        elif self.transport == 'email':
            pass
        elif self.transport == 'vpnftp':
            self.pprocess.processXML()
        elif self.transport == 'vpncp':
            pass
            
        #print results
        #print 'This is the result before it goes back to the test_unit:', \
        #results
        #return results

    
    def selectNodes(self, start_date, end_date, nodename):
        pass
    
    def flagNodes(self):
        pass
    
class SvcPointXMLwriter(SVCPOINTXML20Writer):
    
    def __init__(self):
        self.xML = SVCPOINTXML20Writer((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))

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
    