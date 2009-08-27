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

class NodeBuilder(DBObjects.databaseObjects):

    def __init__(self, generateOutputformat):
        
        if generateOutputformat == 'svcpoint':
            self.writer = SvcPointXMLwriter()              
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
        
    def run(self, ):
        '''This is the main method controlling this entire program.'''
        
        # Load the data via DBObjects
        
        
        for writer,validate in map(None, self.writers, self.validators):
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

    
    def selectNodes(self, start_date, end_date, nodename):
        pass
    
    def flagNodes(self):
        pass
    
class SvcPointXMLwriter(SVCPOINTXML20Writer):
    
    def __init__(self):
        self.xML = SVCPOINTXML20Writer((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))

    def write(self):
        pass
    
class HmisXmlWriter(HMISXML28Writer):
    
    def __init__(self):
        self.xML = SVCPOINTXML20Writer((os.path.join(settings.BASE_PATH, settings.OUTPUTFILES_PATH)))

    def write(self):
        pass

if __name__ == '__main__':
    try:
        NODEBUILDER = NodeBuilder('svcpoint')
        RESULTS = NODEBUILDER.run()
    except clsExceptions.UndefinedXMLWriter:
        print "Please specify a format for outputting your XML"
        raise
    