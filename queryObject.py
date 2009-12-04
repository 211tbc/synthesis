#!/usr/bin/env python

from optparse import OptionParser

'''
Formats the processing options for "nodebuilder.py" module.

Usage: nodebuilder.py [options] arg

Options:
  -h, --help            show this help message and exit
  -i ID, --IDvendor=ID  ID of vendor requesting report
  -s StartDate, --startdate=StartDate
                        start date of reporting
  -e EndDate, --enddate=EndDate
                        end date of reporting
                        
'''

class queryObject:
    def __init__(self):
        
        usage = "usage: %prog [options] arg"
        
        parser = OptionParser(usage)
        parser.add_option("-i", "--IDconfig", dest="configID", type="string",
                          help="Configuration ID of Vendor requesting report", metavar="ID")
        parser.add_option("-s", "--startdate", dest="startDate", type="string",
                          help="start date of reporting", metavar="StartDate")
        
        parser.add_option("-e", "--enddate", dest="endDate", type="string",
                          help="end date of reporting", metavar="EndDate")
        
        (self.options, self.arg) = parser.parse_args()
        
        #print 'options' ,options
        #print "arg:", arg
        
        #print 'options.vendorID=%s' % options.vendorID
        if self.options.configID == None or self.options.startDate == None or self.options.endDate == None:
            parser.print_help()
            self.options = None
            #raise 'error'
            
        
    def getOptions(self):
        return self.options

def main():
    optParse = queryObject()
    options = optParse.getOptions()
    if options != None:
        print options.vendorID
    
if __name__ == '__main__':
    main()
    

    
    

